"""Stage 5 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def carboprost(d):
    # The label has no pregnancy contraindication; the matched sentence is about completing a failed termination.
    d['populations']['pregnancy'].update(level='avoid',
        text=T('برچسب: دارو برای ختم بارداری و خونریزی پس از زایمان است، نه بارداری ادامه‌دار؛ ختم ناموفق باید با روش دیگری تکمیل شود.', 'Label: used for pregnancy termination and postpartum haemorrhage, not in an ongoing pregnancy; a failed termination must be completed by other means.'))

def infant_only(*keys):
    # Infant-only products: the label's pregnancy/lactation text says the drug is not for adult women.
    def fn(d):
        for k in keys:
            if k in d.get('populations', {}):
                d['populations'][k].update(level='no-data', text=T('برچسب: داروی نوزاد/شیرخوار است و برای زنان بزرگسال اندیکاسیون ندارد.', 'Label: an infant product; not indicated for adult women.'))
    return fn

edit('carboprost', carboprost)
edit('nirsevimab', infant_only('pregnancy', 'lactation'))
edit('caffeine-citrate', infant_only('pregnancy'))
print('s5_post ok')
