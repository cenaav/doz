"""Enrich drugs: move to ATC category, Iran status (Darooyab), US approval, reference links, special-population tags.
Usage: enrich.py id[=G-123/Slug] ...   (=slug sets the Darooyab generic page; otherwise the existing one or an exact search hit)"""
import collections, json, os, re, sys, urllib.parse
import atc, darooyab, labels
from classify import FUN, TXT, cut, sec_label, smpc_sections
from gen import ROOT, find
from net import fetch

S = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'sources.json')))}
CAT = {c['atc']: c['id'] for c in json.load(open(os.path.join(ROOT, 'categories.json')))}
KIND = {'otc monograph drug': 'OTC monograph', 'unapproved drug other': 'unapproved', 'nda': 'NDA', 'anda': 'ANDA', 'bla': 'BLA',
        'nda authorized generic': 'NDA authorized generic', 'dietary supplement': 'dietary supplement'}

def refs(o):
    if isinstance(o, dict):
        if isinstance(o.get('source'), str): yield o['source']
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)

def rxcui(name):
    t = fetch('https://rxnav.nlm.nih.gov/REST/rxcui.json?search=2&name=' + urllib.parse.quote(name))
    m = re.search(r'"rxnormId":\["(\d+)"', t); return m.group(1) if m else None

def medline(cui):
    t = fetch(f'https://connect.medlineplus.gov/service?mainSearchCriteria.v.cs=2.16.840.1.113883.6.88&mainSearchCriteria.v.c={cui}&knowledgeResponseType=application/json')
    try: d = json.loads(t)
    except Exception: return []
    return [(l['href'].split('?')[0], e['title']['_value']) for e in d['feed'].get('entry', []) for l in e['link'] if '/druginfo/meds/' in l['href']]

def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

def enrich(id, slug=None):
    p = find(id); d = json.load(open(p))
    c = collections.Counter(refs(d))
    fdas = [s for s, _ in c.most_common() if S[s]['type'] == 'fda-label']
    uks = [s for s, _ in c.most_common() if S[s]['type'] == 'uk-smpc']
    # ATC category
    for code in d.get('atc', []):
        assert atc.name(code), f'{id}: ATC {code} not found on WHO index'
    if d.get('atc'):
        cat = CAT[d['atc'][0][0]]
        if cat != d['category']:
            d['category'] = cat; os.remove(p); p = os.path.join(ROOT, 'drugs', cat, id + '.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
    # Iran
    if not slug and d.get('iran'):
        u = d['iran']['refs'][0].get('url', '')
        if '/G-' in u: slug = u.split('darooyab.ir/')[1]
    if not slug:
        base = re.split(r'[(+/,]| and ', d['name']['en'])[0].strip()
        hits = [h for h in darooyab.search(base) if norm(h.split('/', 1)[1]) == norm(base)]
        slug = hits[0] if len(hits) == 1 else None
    if slug:
        fs = darooyab.forms(slug); bs = darooyab.brands(slug)
        iran_only = all(set(f['markets']) == {'IR'} for f in d['formulations'])
        d['iran'] = {'status': 'iran-only' if iran_only else ('registered' if fs or bs else 'not-found')}
        if fs: d['iran']['forms'] = fs
        d['iran']['refs'] = [{'source': 'darooyab-generic', 'section': slug, 'url': 'https://www.darooyab.ir/' + slug}]
    else:
        q = re.split(r'[(]', d['name']['en'])[0].strip()
        d['iran'] = {'status': 'not-found', 'refs': [{'source': 'darooyab-generic', 'section': 'search', 'url': 'https://www.darooyab.ir/Search?q=' + urllib.parse.quote(q)}]}
    # US approval + links
    links = []; d.pop('usApproval', None); setid = None
    if fdas:
        m = re.search(r'setid=([0-9a-f-]{36})', S[fdas[0]]['url'])
        if m:
            setid = m.group(1); kind, aid = labels.approval(labels.spl(setid))
            if kind and kind.lower() in KIND:
                d['usApproval'] = {'kind': KIND[kind.lower()], 'refs': [{'source': fdas[0], 'section': 'SPL approval / marketing category'}]}
                if aid: d['usApproval']['id'] = aid
                if aid and re.match(r'(NDA|ANDA|BLA)', aid):
                    links.append({'kind': 'fda', 'url': 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=' + re.sub(r'\D', '', aid).zfill(6), 'label': aid})
    for sid in fdas: links.append({'kind': 'dailymed', 'url': S[sid]['url'], 'label': S[sid]['short']})
    cui = rxcui(re.split(r'[(+/,]', d['name']['en'])[0].strip())
    for u, title in (medline(cui) if cui else [])[:2]: links.append({'kind': 'medlineplus', 'url': u, 'label': title})
    for code in d.get('atc', []): links.append({'kind': 'who-atc', 'url': f'https://atcddd.fhi.no/atc_ddd_index/?code={code}', 'label': code})
    if slug: links.append({'kind': 'darooyab', 'url': 'https://www.darooyab.ir/' + slug, 'label': slug.split('/')[1]})
    for sid in uks: links.append({'kind': 'emc', 'url': S[sid]['url'], 'label': S[sid]['short']})
    seen = set(); d['links'] = [l for l in links if not (l['url'] in seen or seen.add(l['url']))]
    # populations
    sec = None; src = None
    if setid:
        sec = labels.sections(labels.spl(setid)); src = fdas[0]
        if not any(sec.get(k) for k in ('pregnancy', 'lactation', 'pediatric', 'geriatric')) and uks: sec = None
    if sec is None and uks:
        pid = re.search(r'product/(\d+)', S[uks[0]]['url']).group(1); sec = smpc_sections(labels.emc_text(pid)); src = uks[0]
    pops = {}
    if sec:
        for k, fn in FUN.items():
            r = fn(sec)
            if not r: continue
            lvl, quote, key = r
            section = {'boxed': 'Boxed Warning'}.get(key) or sec_label(sec.get(key + '_title', ''), key)
            fa, en = TXT[k][lvl]
            pops[k] = {'level': lvl, 'text': {'fa': fa, 'en': en}, 'quote': cut(quote or ''), 'refs': [{'source': src, 'section': section}]}
    if 'pregnancy' not in pops and slug:
        r = darooyab.pregnancy(slug)
        if r: pops['pregnancy'] = {**r, 'refs': [{'source': 'darooyab-generic', 'section': slug + ' — مصرف در بارداری', 'url': 'https://www.darooyab.ir/' + slug}]}
    if pops: d['populations'] = pops
    else: d.pop('populations', None)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    print(f"{id:30} {d['category']:20} iran={d['iran']['status']:10} us={d.get('usApproval', {}).get('kind', '-'):14} links={len(d['links'])} pops={ {k: v['level'] for k, v in pops.items()} }")

if __name__ == '__main__':
    for a in sys.argv[1:]:
        i, _, s = a.partition('='); enrich(i, s or None)
