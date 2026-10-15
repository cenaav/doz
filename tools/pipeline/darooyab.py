import html, re, sys
from net import fetch
BASE = 'https://www.darooyab.ir/'

def search(q):
    t = fetch(BASE + 'Home/PartialNewSearch', data={'autocomplete': q, 'DrugName_pageNumber': 1}, min_size=2000, wait=1.2)
    return sorted(set(re.findall(r'href="[^"]*?/(G-\d+/[^"#?]+)"', t)))

def page(slug): return fetch(BASE + slug, min_size=5000, wait=1.0)
def ptext(slug):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', page(slug), flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))

def forms(slug):
    rows = re.findall(r'<td>\s*(\d{5})\s*</td>\s*<td[^>]*>\s*<label[^>]*>([^<]+)</label>\s*<br\s*/?>\s*<h3>([^<]*)</h3>', page(slug))
    return [{'code': c, 'en': html.unescape(e).strip(), 'fa': html.unescape(f).strip()} for c, e, f in rows]

def brands(slug):
    t = page(slug); i = t.find('Brand names')
    if i < 0: return []
    seg = t[i:t.find('</tbody>', i)]
    return [re.sub(r'\s+', ' ', html.unescape(n)).strip() for n in re.findall(r'href="/B-[^"]+">\s*([^<]+?)\s*<br />', seg)]

LV = {'X': 'contraindicated', 'D': 'avoid', 'C': 'caution', 'B': 'caution', 'A': 'ok'}
def pregnancy(slug):
    x = ptext(slug)
    m = re.search(r'مصرف در بارداری\s+[^:]{0,60}?گروه\s+([ABCDX])\s+([^:]{0,80}):', x)
    if not m: return None
    letter = m.group(1); quote = x[m.start():m.end()].strip()
    if letter in 'XD' and 'منع مصرف مطلق ندارد' in x:
        return {'level': 'caution', 'quote': quote, 'text': {'fa': f'دارویاب این دارو را گروه {letter} نوشته، ولی در متن همان صفحه آمده در بارداری منع مصرف مطلق ندارد. منبع متناقض است؛ فقط با نظر متخصص.', 'en': f'Darooyab lists category {letter}, but the same page says it is not absolutely contraindicated in pregnancy. The source contradicts itself; specialist advice only.'}}
    fa = {'contraindicated': f'دارویاب: گروه {letter} — در بارداری نباید مصرف شود.', 'avoid': f'دارویاب: گروه {letter} — شواهد خطر برای جنین؛ فقط در شرایط ضروری.', 'caution': f'دارویاب: گروه {letter} — فقط اگر فایده بیشتر از خطر باشد.', 'ok': f'دارویاب: گروه {letter}.'}[LV[letter]]
    en = {'contraindicated': f'Darooyab: category {letter} — must not be used in pregnancy.', 'avoid': f'Darooyab: category {letter} — evidence of fetal risk; only when essential.', 'caution': f'Darooyab: category {letter} — only if benefit outweighs risk.', 'ok': f'Darooyab: category {letter}.'}[LV[letter]]
    return {'level': LV[letter], 'quote': quote, 'text': {'fa': fa, 'en': en}}

if __name__ == '__main__':
    if sys.argv[1] == 'search':
        for q in sys.argv[2:]: print(q, '=>', ' '.join(search(q))[:300])
    elif sys.argv[1] == 'forms':
        for s in sys.argv[2:]: print(s, [f['en'] for f in forms(s)], '| brands', len(brands(s)))
