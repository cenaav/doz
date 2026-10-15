"""Stage 8 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def ped(level, fa, en, quote, section='8.4'):
    def fn(d):
        src = d['populations']['pediatric']['refs'][0]['source']
        d['populations']['pediatric'].update(level=level, text=T(fa, en), quote=quote, refs=[{'source': src, 'section': section}])
    return fn

# The classifier matched the accidental-ingestion warning, not the pediatric-use statement.
edit('methadone', ped('not-established', 'برچسب: زیر ۱۸ سال ثابت نشده. مصرف تصادفی در کودک کشنده است.', 'Label: not established under 18. Accidental ingestion by a child is fatal.',
                      'The safety, effectiveness, and pharmacokinetics of methadone in pediatric patients below the age of 18 years have not been established.'))
# The contraindication is only for children under 2.
edit('brimonidine', ped('caution', 'برچسب: زیر ۲ سال ممنوع؛ از ۲ سالگی با احتیاط.', 'Label: contraindicated under 2 years; use with caution from 2 years.',
                        'Neonates and infants (pediatric patients younger than 2 years old).', '4'))
print('s8_post ok')
