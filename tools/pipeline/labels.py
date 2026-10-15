import html, json, re, sys, urllib.parse
from net import fetch

REPACK = re.compile(r'repack|a-s medication|bryant|preferred|direct.?rx|nucare|proficient|pd-rx|quality care|st\. mary|northwind|redpharm|medsource|henry schein|aphena|asclemed|denton|lake erie|unit dose|golden state|american health packaging|cardinal|major pharm|rpk|stat rx|rebel|physicians total|aidarex|coupler|medical purchasing|safecor|advanced rx|chartwell rx|quallent|hf acquisition|healthfirst|general injectables|covetrus|veterinary|zoetis|sportpharm|remedy repack', re.I)

def plain(s):
    s = re.sub(r'<(?:br|paragraph|item|tr)[^>]*>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def search(drug_name, title_rx, pages=3):
    """First non-repackager SPL whose title matches title_rx → (setid, title) or None."""
    pat = re.compile(title_rx, re.I); cands = []
    for pg in range(1, pages + 1):
        t = fetch(f'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?pagesize=100&page={pg}&drug_name=' + urllib.parse.quote(drug_name))
        try: data = json.loads(t)['data']
        except Exception: break
        cands += [x for x in data if pat.search(x['title'])]
        if len(data) < 100: break
    pick = next((x for x in cands if not REPACK.search(x['title'])), None)
    return (pick['setid'], pick['title']) if pick else None

def spl(setid):
    return fetch(f'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml', min_size=2000)

def meta(setid):
    t = spl(setid)
    e = re.search(r'<effectiveTime value="(\d{8})', t); v = re.search(r'<versionNumber value="(\d+)"', t)
    return (f'{e.group(1)[:4]}-{e.group(1)[4:6]}-{e.group(1)[6:]}' if e else None), (v.group(1) if v else None)

def text(setid): return plain(spl(setid))

def grab(setid, phrase, n=600, nth=0):
    t = text(setid); ms = [m.start() for m in re.finditer(phrase, t)]
    return t[ms[nth]:ms[nth] + n] if len(ms) > nth else None

def approval(t):
    m = re.search(r'<approval>(.*?)</approval>', t, re.S)
    if not m: return None, None
    a = m.group(1)
    i = re.search(r'extension="([^"]+)"', a); d = re.search(r'displayName="([^"]+)"', a)
    return (d.group(1) if d else None), (i.group(1).replace(' ', '') if i else None)

def _blocks(t):
    for m in re.finditer(r'<section\b', t):
        start = m.start(); depth = 0; end = None
        for mm in re.finditer(r'<(/?)section\b', t[start:]):
            depth += -1 if mm.group(1) else 1
            if depth == 0: end = start + mm.end(); break
        if end is None: continue
        s = t[start:end]
        head = s[:s.find('<section', 8)] if s.find('<section', 8) > 0 else s
        tm = re.search(r'<title[^>]*>(.*?)</title>', head, re.S); cm = re.search(r'<code code="([^"]+)"', head)
        yield (plain(tm.group(1)) if tm else ''), re.sub(r'<title[^>]*>.*?</title>', '', s, count=1, flags=re.S), (cm.group(1) if cm else '')

TITLES = {'pregnancy': r'^(?:\d+(?:\.\d+)?\s*)?pregnancy\b(?!.*lactation)', 'lactation': r'^(?:\d+(?:\.\d+)?\s*)?(?:lactation|nursing mothers)\b',
          'reproductive': r'^(?:\d+(?:\.\d+)?\s*)?females and males of reproductive potential', 'pediatric': r'^(?:\d+(?:\.\d+)?\s*)?pediatric use',
          'geriatric': r'^(?:\d+(?:\.\d+)?\s*)?geriatric use', 'contra': r'^(?:\d+\s*)?contraindications\b', 'boxed': r'^(?:boxed warning|warning:)'}

def sections(t):
    out = {}
    for title, body, code in _blocks(t):
        for key, rx in TITLES.items():
            if key in out: continue
            if re.search(rx, title, re.I) or (key == 'boxed' and code == '34066-1'):
                out[key] = plain(body); out[key + '_title'] = title
    full = plain(t)
    HEAD = r'(?:Usage in Pregnancy|Pregnancy(?: Category [ABCDX])?|Nursing Mothers|Lactation|Pediatric Use|Geriatric Use|Information for Patients|Drug Interactions|Carcinogenesis|ADVERSE REACTIONS|OVERDOSAGE|DOSAGE AND ADMINISTRATION|Labor and Delivery|Teratogenic Effects|Nonteratogenic Effects)'
    INLINE = {'pregnancy': r'(?:Usage in Pregnancy|Pregnancy)\s*:?\s', 'lactation': r'Nursing Mothers\s*:?\s', 'pediatric': r'Pediatric Use\s*:?\s', 'geriatric': r'Geriatric Use\s*:?\s'}
    for key, rx in INLINE.items():
        if out.get(key): continue
        for m in re.finditer(r'(?:(?<=[.:\]]\s)|(?<=[.:\]]))' + rx, full):
            rest = full[m.end():]; stop = re.search(r'\s' + HEAD + r'\s*:?\s', rest[20:])
            body = rest[:20 + stop.start()] if stop else rest[:1500]
            if len(body) > 30:
                out[key] = body.strip(); out[key + '_title'] = 'Precautions/Warnings – ' + m.group(0).strip(' :'); break
    if not out.get('pregnancy'):
        if re.search(r'if breast-?feeding:?\s*not recommended', full, re.I):
            out['lactation'] = 'If breast-feeding: not recommended.'; out['lactation_title'] = 'Drug Facts – Warnings'
            m = re.search(r'if pregnant:\s*(ask[^.]*\.)', full, re.I)
            if m: out['pregnancy'] = 'If pregnant: ' + m.group(1).strip(); out['pregnancy_title'] = 'Drug Facts – Warnings'
        m = re.search(r'If pregnant or breast-?feeding,?\s*(ask[^.]*\.)', full, re.I)
        if m:
            q = 'If pregnant or breast-feeding, ' + m.group(1).strip()
            for key in ('pregnancy', 'lactation'):
                if not out.get(key): out[key] = q; out[key + '_title'] = 'Drug Facts – Warnings'
    m = re.search(r'It is especially important not to use [^.]*pregnancy[^.]*\.', full)
    if m and out.get('pregnancy', '').startswith('If pregnant'): out['pregnancy'] += ' ' + m.group(0)
    return out

def digest(setid, n=500):
    """Key dosing/contra/peds sections as short lines for reading."""
    t = spl(setid); lines = []
    for title, body, code in _blocks(t):
        if re.match(r'^(\d+(\.\d+)* )?(DOSAGE|HOW SUPPLIED|DOSAGE FORMS|CONTRAINDICATIONS|Pediatric Use|BOXED|WARNING:|Directions|Active ingredient|Uses|Warnings)', title or '', re.I) or re.match(r'^(2(\.\d+)* |3 |4 |8\.4)', title or ''):
            own = plain(re.sub(r'<section\b.*', '', body[body.find('>') + 1:], flags=re.S)) if '<section' in body[10:] else plain(body)
            if own: lines.append(f'## {title[:60]} :: {own[:n]}')
    return '\n'.join(lines)

# UK eMC SmPC
def emc(pid): return fetch(f'https://www.medicines.org.uk/emc/product/{pid}/smpc', min_size=5000)
def emc_text(pid): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style).*?</\1>', '', emc(pid)))))
def emc_section(pid, num, n=900):
    t = emc_text(pid); ms = [m.start() for m in re.finditer(re.escape(num) + r'\s+[A-Z]', t)]
    return t[ms[-1]:ms[-1] + n] if ms else None
def emc_meta(pid):
    t = emc_text(pid)
    title = re.search(r'<title>([^<]*)', emc(pid)); rev = re.search(r'10\. Date of revision of the text\s*(.{0,40})', t)
    return (html.unescape(title.group(1)).strip() if title else ''), (rev.group(1).strip() if rev else '')

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'search': print(search(sys.argv[2], sys.argv[3]))
    elif cmd == 'digest': print(meta(sys.argv[2])); print(digest(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 500))
    elif cmd == 'grab':
        for p in sys.argv[4:]: print(f'[{p[:30]}]', grab(sys.argv[2], p, int(sys.argv[3])))
    elif cmd == 'emc':
        print(emc_meta(sys.argv[2]))
        for s in sys.argv[4:]: print('##', emc_section(sys.argv[2], s, int(sys.argv[3])))
