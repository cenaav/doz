"""Stage 7 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def ped(level, fa, en, quote, section='8.4'):
    # The classifier matched an unrelated sentence (accidental ingestion or an under-2 contraindication).
    def fn(d):
        src = d['populations']['pediatric']['refs'][0]['source']
        d['populations']['pediatric'].update(level=level, text=T(fa, en), quote=quote, refs=[{'source': src, 'section': section}])
    return fn

edit('oxycodone', ped('not-established', 'برچسب: ایمنی و اثربخشی در کودکان بررسی نشده است. مصرف تصادفی حتی یک دوز در کودک می‌تواند کشنده باشد.', 'Label: not evaluated in children. Accidental ingestion of even one dose by a child can be fatal.',
                      'The safety and efficacy of oxycodone hydrochloride tablets in pediatric patients have not been evaluated.'))
edit('morphine-oral', ped('not-established', 'برچسب: در کودک زیر ۵۰ kg ثابت نشده (دوز با قرص قابل دستیابی نیست). مصرف تصادفی در کودک می‌تواند کشنده باشد.', 'Label: not established in children under 50 kg (dose not achievable with tablets). Accidental ingestion by a child can be fatal.',
                          'The safety and effectiveness of morphine sulfate tablets have not been established for the management of pediatric patients weighing less than 50 kg'))
edit('linaclotide', ped('caution', 'برچسب: زیر ۲ سال ممنوع (کم‌آبی شدید)؛ یبوست عملکردی از ۲ سال و IBS-C از ۷ سال تأیید شده.', 'Label: contraindicated under 2 years (serious dehydration); approved for functional constipation from 2 y and IBS-C from 7 y.',
                        'LINZESS is contraindicated in: Patients less than 2 years of age due to the risk of serious dehydration', '4'))
edit('pimecrolimus', ped('caution', 'برچسب: فقط ۲ سال به بالا و خط دوم؛ زیر ۲ سال اندیکاسیون ندارد.', 'Label: only ≥2 years and second line; not indicated under 2 years.',
                         'Pimecrolimus Cream, 1% is not indicated for use in children less than 2 years of age'))
def no_patch(d):
    # Darooyab's general lidocaine page lists sprays, gels and cartridges but no 5% patch.
    d['iran'] = {'status': 'not-found', 'refs': [{'source': 'darooyab-generic', 'section': 'search', 'url': 'https://www.darooyab.ir/Search?q=Lidocaine%20patch'}]}

edit('lidocaine-patch', no_patch)
print('s7_post ok')
