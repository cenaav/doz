"""Stage 6 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def epogen(d):
    # The contraindication covers only the benzyl-alcohol multiple-dose vial.
    for k in ('pregnancy', 'lactation'):
        d['populations'][k].update(level='caution', text=T('برچسب: فقط ویال چنددوزی (حاوی بنزیل الکل) در بارداری و شیردهی ممنوع است؛ از ویال تک‌دوز استفاده شود.', 'Label: only the multiple-dose vial (benzyl alcohol) is contraindicated in pregnancy and lactation; use single-dose vials.'))

def jadenu(d):
    # The matched sentence is the eGFR contraindication, which applies to all ages; the drug is approved from 2 years.
    d['populations']['pediatric'].update(level='caution', text=T('برچسب: از ۲ سالگی تأیید شده؛ در eGFR زیر ۴۰ (همه سنین) ممنوع؛ دوز با تغییر وزن کودک تنظیم شود.', 'Label: approved from 2 years; contraindicated with eGFR <40 at any age; adjust for the child’s changing weight.'))

edit('epoetin-alfa', epogen)
edit('deferasirox', jadenu)
print('s6_post ok')
