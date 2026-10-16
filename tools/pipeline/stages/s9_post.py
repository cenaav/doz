"""Stage 9 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def pop(key, level, fa, en, quote, section):
    def fn(d):
        src = d['populations'][key]['refs'][0]['source']
        d['populations'][key].update(level=level, text=T(fa, en), quote=quote, refs=[{'source': src, 'section': section}])
    return fn

# The classifier matched the accidental-ingestion warning, not the pediatric-use statement.
edit('hydromorphone', pop('pediatric', 'not-established', 'برچسب: ایمنی و اثربخشی در کودکان ثابت نشده. مصرف تصادفی حتی یک دوز در کودک می‌تواند کشنده باشد.', 'Label: not established in children. Accidental ingestion of even one dose by a child can be fatal.',
                          'The safety and effectiveness of hydromorphone hydrochloride tablets in pediatric patients have not been established.', '8.4'))
edit('tapentadol', pop('pediatric', 'caution', 'برچسب: فقط ۶ سال به بالا با وزن دست‌کم ۴۰ kg. مصرف تصادفی در کودک کشنده است.', 'Label: only ≥6 years weighing at least 40 kg. Accidental ingestion by a child can be fatal.',
                       'The safety and effectiveness of NUCYNTA (tapentadol) tablets in pediatric patients ages 6 years and older who weigh at least 40 kg have been established.', '8.4'))
# The classifier matched a sentence about the MACDP registry, not a risk statement.
for i, n in (('lamivudine', 'lamivudine'), ('zidovudine', 'zidovudine')):
    edit(i, pop('pregnancy', 'caution', 'برچسب: داده‌های رجیستری بارداری افزایش نقص مادرزادی نسبت به جمعیت عمومی نشان نمی‌دهد.', 'Label: pregnancy registry data show no increase in birth defects over the background rate.',
                f'Available data from the APR show no difference in the overall risk of birth defects for {n} compared with the background rate for birth defects of 2.7% in the Metropolitan Atlanta Congenital Defects Program (MACDP) reference population.', '8.1'))
print('s9_post ok')
