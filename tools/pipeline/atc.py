import html, re, sys
from net import fetch
def name(code):
    """WHO ATC name for a code (any level), or None."""
    t = fetch(f'https://atcddd.fhi.no/atc_ddd_index/?code={code}&showdescription=no')
    hits = [html.unescape(n).strip() for c, n in re.findall(r'code=([A-Z0-9]+)&[^>]*>([^<]+)<', t) if c == code and 'Guidelines' not in n]
    if hits: return hits[0]
    x = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    m = re.search(re.escape(code) + r' ([a-z][^0-9]{2,60}?)(?: \d| List)', x)
    return m.group(1).strip() if m else None
def search(q):
    t = fetch('https://atcddd.fhi.no/atc_ddd_index/?name=' + q.replace(' ', '+'))
    return [(c, html.unescape(n).strip()) for c, n in re.findall(r'code=([A-Z]\d\d[A-Z]{2}\d\d)[^>]*>([^<]+)<', t)]
if __name__ == '__main__':
    if sys.argv[1] == 'name':
        for c in sys.argv[2:]: print(c, name(c))
    else:
        for q in sys.argv[2:]: print(q, search(q))
