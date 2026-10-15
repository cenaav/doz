"""Stage 4 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def cerebyx(d):
    # The classifier matched the boxed infusion-rate warning; the label indicates the drug in all pediatric age groups.
    d['populations']['pediatric'].update(level='caution', refs=[{'source': 'fda-cerebyx', 'section': '8.4'}],
        text=T('برچسب: برای همه گروه‌های سنی کودکان اندیکاسیون دارد؛ سرعت انفوزیون در کودک حداکثر ۲ mg PE/kg/min یا ۱۵۰ mg PE/min (هر کدام کندتر).', 'Label: indicated in all pediatric age groups; pediatric infusion rate max 2 mg PE/kg/min or 150 mg PE/min, whichever is slower.'),
        quote='CEREBYX is indicated for the treatment of generalized tonic-clonic status epilepticus and prevention and treatment of seizures occurring during neurosurgery in all pediatric age groups')

def vaccine_preg(name):
    # The classifier matched registry miscarriage rates, which the label presents as background risk.
    def fn(d):
        d['populations']['pregnancy'].update(level='caution',
            text=T('برچسب: داده‌های موجود افزایش خطر نقص مادرزادی یا سقط را نشان نمی‌دهد؛ مطالعه کنترل‌شده کافی نیست.', 'Label: available data do not suggest an increased risk of major birth defects or miscarriage; no adequate controlled studies.'),
            quote=f'Available data do not suggest an increased risk of major birth defects and miscarriage in women who received {name} during pregnancy')
    return fn

edit('fosphenytoin', cerebyx)
edit('hepatitis-b-vaccine', vaccine_preg('ENGERIX-B'))
edit('hepatitis-a-vaccine', vaccine_preg('HAVRIX'))
print('s4_post ok')
