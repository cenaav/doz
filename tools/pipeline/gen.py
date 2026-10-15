"""Helpers for stage scripts that write drugs, sources and diseases into data/."""
import json, os, re
import labels
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
TODAY = '2026-10-15'

def _load(n): return json.load(open(os.path.join(ROOT, n)))
def _save(n, v):
    p = os.path.join(ROOT, n); json.dump(v, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def add_src(**kw):
    s = _load('sources.json')
    assert len(kw['short']) <= 24, kw['short']
    if not any(x['id'] == kw['id'] for x in s): s.append(kw); _save('sources.json', s)
    return kw['id']

def fda(key, short, title, setid):
    eff, ver = labels.meta(setid)
    return add_src(id='fda-' + key, type='fda-label', short=short, title=title, publisher='U.S. FDA label via DailyMed (NLM)',
                   edition=f'SPL effective {eff}, version {ver}', url=f'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={setid}', accessed=TODAY, license='public')

def uk(id, short, title, pub, rev, pid):
    return add_src(id=id, type='uk-smpc', short=short, title=title, publisher=f'{pub}, via eMC (medicines.org.uk)', edition=f'Revised {rev}',
                   url=f'https://www.medicines.org.uk/emc/product/{pid}/smpc', accessed=TODAY, license='public')

def dy(id, short, title, slug):
    return add_src(id=id, type='secondary-web', short=short, title=title, publisher='Darooyab (Iran)', url='https://www.darooyab.ir/' + slug, accessed=TODAY, license='public')

def add_disease(id, fa, en, syn, icd, sp):
    d = _load('diseases.json')
    if not any(x['id'] == id for x in d):
        d.append({'id': id, 'name': {'fa': fa, 'en': en}, 'synonyms': syn, 'icd10': icd, 'specialty': sp}); _save('diseases.json', d)

def R(src, section=None, page=None):
    r = {'source': src}
    if section: r['section'] = section
    if page: r['page'] = page
    return r
def T(fa, en): return {'fa': fa, 'en': en}
def age(v, u): return {'value': v, 'unit': u}
A18 = {'minAge': age(18, 'year')}
def note(fa, en, refs): return {'text': T(fa, en), 'refs': refs}
def W(fa, en, refs): return {'text': T(fa, en), 'refs': refs}
def CI(id, fa, en, refs, sev='block', rule=None):
    c = {'id': id, 'severity': sev, 'text': T(fa, en), 'refs': refs}
    if rule: c['rule'] = rule
    return c
def IA(w, fa, en, refs): return {'with': w, 'text': T(fa, en), 'refs': refs}

def form(id, form_, route, label, amt, unit, refs, per=None, vol=None, scored=None, markets=('US',), components=None):
    c = {'amount': amt, 'unit': unit}
    if vol is not None: c['perVolumeMl'] = vol
    if per: c['perUnit'] = per
    if scored is not None: c['scored'] = scored
    f = {'id': id, 'form': form_, 'route': route, 'label': label, 'concentration': c, 'markets': list(markets), 'refs': refs}
    if components: f['components'] = components
    return f
def tab(id, mg, label, refs, scored=False, per='tablet', form_='tablet', markets=('US',)):
    return form(id, form_, 'oral', label, mg, 'mg', refs, per=per, scored=scored, markets=markets)
def liquid(id, mg, ml, label, refs, form_='suspension', route='oral', unit='mg', markets=('US',)):
    return form(id, form_, route, label, mg, unit, refs, vol=ml, markets=markets)
def unitform(id, form_, route, label, refs, unit='application', per='application', markets=('US',)):
    return form(id, form_, route, label, 1, unit, refs, per=per, markets=markets)

def reg(id, disease, label, pop, type_, dose, refs, unit='mg', limits=None, dur=None, allowed=None, notes=None, doseComponent=None):
    r = {'id': id, 'disease': disease, 'label': label, 'population': pop, 'type': type_, 'unit': unit, 'dose': dose, 'refs': refs}
    if doseComponent: r['doseComponent'] = doseComponent
    if limits: r['limits'] = limits
    if dur: r['durationDays'] = dur
    if allowed: r['allowedFormulations'] = allowed
    if notes: r['notes'] = notes
    return r
def ex(reg_, form_, exp, **inp): return {'regimen': reg_, 'formulation': form_, 'input': inp, 'expect': exp}

def fix_bands(d):
    """The engine matches a weight band as min < weight ≤ max. Bands are written inclusive ([15, 24.99], [25, …]),
    so make them contiguous (each min = previous max) and start the first just below the regimen's minimum weight."""
    for r in d['regimens']:
        if r['type'] != 'weightBand': continue
        b = sorted(r['dose']['weightBands'], key=lambda x: x['minWeightKg'])
        for prev, cur in zip(b, b[1:]): cur['minWeightKg'] = prev['maxWeightKg']
        pm = r['population'].get('minWeightKg')
        if pm is not None and b[0]['minWeightKg'] >= pm: b[0]['minWeightKg'] = round(pm - 0.01, 2)
        r['dose']['weightBands'] = b
    return d

def find(id):
    for c in os.listdir(os.path.join(ROOT, 'drugs')):
        p = os.path.join(ROOT, 'drugs', c, id + '.json')
        if os.path.exists(p): return p
    return None

def drug(id, cat, fa, en, cls, brands, syn, forms, regs, ci=(), warn=(), renal=(), mon=(), inter=(), exs=()):
    """Write a drug file. If it already exists, the category on disk wins (enrich may have moved it) and enrichment fields are kept."""
    old_p = find(id); old = json.load(open(old_p)) if old_p else {}
    if old_p: cat = old['category']
    d = {'id': id, 'schemaVersion': 1, 'name': T(fa, en), 'category': cat, 'class': cls, 'brands': brands, 'synonyms': list(syn),
         'formulations': forms, 'regimens': regs, 'contraindications': list(ci), 'warnings': list(warn), 'renal': list(renal),
         'monitoring': list(mon), 'interactions': list(inter), 'review': {'status': 'unverified', 'reviewer': None, 'date': None}, 'examples': list(exs)}
    for k in ('atc', 'iran', 'links', 'populations', 'usApproval'):
        if k in old: d[k] = old[k]
    fix_bands(d)
    p = os.path.join(ROOT, 'drugs', cat, id + '.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def patch(id, add_forms=(), add_regs=(), add_exs=(), pin_old=False):
    """Add formulations/regimens/examples to an existing drug (idempotent by id)."""
    p = find(id); d = json.load(open(p))
    fids = {f['id'] for f in add_forms}; rids = {r['id'] for r in add_regs}
    old_forms = [f['id'] for f in d['formulations'] if f['id'] not in fids]
    if pin_old:  # existing regimens keep only the formulations they were written for
        for r in d['regimens']:
            if r['id'] not in rids and not r.get('allowedFormulations'): r['allowedFormulations'] = old_forms
    d['formulations'] = [f for f in d['formulations'] if f['id'] not in fids] + list(add_forms)
    d['regimens'] = [r for r in d['regimens'] if r['id'] not in rids] + list(add_regs)
    pairs = {(x['regimen'], x['formulation']) for x in add_exs}
    d['examples'] = [e for e in d['examples'] if (e['regimen'], e['formulation']) not in pairs] + list(add_exs)
    fix_bands(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return d
