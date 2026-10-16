"""MedlinePlus Medical Encyclopedia: find articles by title and read their Symptoms section.
CLI: medline.py find <title regex> | medline.py symptoms <article-id>"""
import html, re, sys
from net import fetch

def _text(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

def find(title_rx):
    """Encyclopedia articles whose title matches the regex → [(article id, title)]."""
    pat = re.compile(title_rx, re.I); out = []
    letters = {c.upper() for c in re.sub(r'[^a-zA-Z]', '', title_rx)[:1]} or set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for L in sorted(letters):
        t = fetch(f'https://medlineplus.gov/ency/encyclopedia_{L}.htm')
        out += [(a, html.unescape(n).strip()) for a, n in re.findall(r'href="article/(\d+)\.htm">([^<]+)<', t) if pat.search(html.unescape(n))]
    return out

def article(aid):
    t = fetch(f'https://medlineplus.gov/ency/article/{aid}.htm')
    title = _text(re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1))
    rev = re.search(r'Review Date[^0-9]*(\d{1,2}/\d{1,2}/\d{4})', t)
    secs = {}
    for m in re.finditer(r'<section>.*?<h2>(.*?)</h2>.*?<div class="section-body"[^>]*>(.*?)</div></div></section>', t, re.S):
        secs[_text(m.group(1))] = _text(m.group(2))
    return {'title': title, 'review': rev.group(1) if rev else None, 'sections': secs, 'url': f'https://medlineplus.gov/ency/article/{aid}.htm'}

if __name__ == '__main__':
    if sys.argv[1] == 'find':
        for a in find(sys.argv[2]): print(*a)
    else:
        a = article(sys.argv[2]); print(a['title'], '| review', a['review'], '|', list(a['sections']))
        print(a['sections'].get('Symptoms', '— no Symptoms section —'))
