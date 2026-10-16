"""Stage 10 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py.
dichlorphenamide gets none: its only WHO code (S01EC02) is the glaucoma group and would file it under eye drugs."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'sinecatechins': ['D06BB12'], 'pyrethrins-pbo': ['P03AC51'], 'ertapenem': ['J01DH03'], 'amphotericin-b': ['J02AA01'], 'isavuconazonium': ['J02AC05'], 'riluzole': ['N07XX02'],
       'edaravone': ['N07XX14'], 'tetrabenazine': ['N07XX06'], 'deutetrabenazine': ['N07XX16'], 'valbenazine': ['N07XX13'], 'deflazacort': ['H02AB13'], 'amifampridine': ['N07XX05'],
       'dimethyl-fumarate': ['L04AX07'], 'teriflunomide': ['L04AK02'], 'fingolimod': ['L04AE01']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
