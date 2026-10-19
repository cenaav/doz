"""Stage 13 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py.
No WHO code (left empty): levalbuterol (levosalbutamol not listed). Older drugs still without a code: fosaprepitant, calamine, crotamiton, carbamide peroxide, spinosad, scorpion antivenom and combination products."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'abiraterone': ['L02BX03'], 'alogliptin': ['A10BH04'], 'amphetamine': ['N06BA01'], 'bevacizumab': ['L01FG01'], 'bortezomib': ['L01XG01'], 'brinzolamide': ['S01EC04'],
       'carboplatin': ['L01XA02'], 'ceftaroline': ['J01DI02'], 'ciclesonide': ['R03BA08'], 'cisplatin': ['L01XA01'], 'colesevelam': ['C10AC04'], 'cyclophosphamide': ['L01AA01'],
       'cytarabine': ['L01BC01'], 'dexrazoxane': ['V03AF02'], 'docetaxel': ['L01CD02'], 'doxorubicin': ['L01DB01'], 'dtp-vaccine': ['J07AJ51'], 'enzalutamide': ['L02BB04'],
       'etoposide': ['L01CB01'], 'exemestane': ['L02BG06'], 'fesoterodine': ['G04BD11'], 'fluorouracil': ['L01BC02'], 'gemcitabine': ['L01BC05'], 'glecaprevir-pibrentasvir': ['J05AP57'],
       'lanreotide': ['H01CB03'], 'ledipasvir-sofosbuvir': ['J05AP51'], 'lenalidomide': ['L04AX04'], 'leucovorin': ['V03AF03'], 'lopinavir-ritonavir': ['J05AR10'], 'mannitol': ['B05BC01'],
       'mercaptopurine': ['L01BB02'], 'mesna': ['V03AF01'], 'methylnaltrexone': ['A06AH01'], 'mexiletine': ['C01BB02'], 'molnupiravir': ['J05AB18'], 'naloxegol': ['A06AH03'],
       'nevirapine': ['J05AG01'], 'niacin': ['C10AD02'], 'nivolumab': ['L01FF01'], 'opv-vaccine': ['J07BF02'], 'oxaliplatin': ['L01XA03'], 'paclitaxel': ['L01CD01'],
       'pembrolizumab': ['L01FF02'], 'pentavalent-vaccine': ['J07CA11'], 'peramivir': ['J05AH03'], 'pretomanid': ['J04AK08'], 'rasburicase': ['V03AF07'], 'rifabutin': ['J04AB04'],
       'rifapentine': ['J04AB05'], 'saxagliptin': ['A10BH03'], 'trastuzumab': ['L01FD01'], 'urokinase': ['B01AD04'], 'vincristine': ['L01CA02']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
