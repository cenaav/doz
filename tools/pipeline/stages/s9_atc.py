"""Stage 9 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'norepinephrine': ['C01CA03'], 'dopamine': ['C01CA04'], 'dobutamine': ['C01CA07'], 'vasopressin': ['H01BA01'], 'esmolol': ['C07AB09'], 'alteplase': ['B01AD02'],
       'streptokinase': ['B01AD01'], 'sodium-bicarbonate': ['B05XA02'], 'potassium-chloride': ['A12BA01', 'B05XA01'], 'tolvaptan': ['C03XA01'], 'streptomycin': ['J01GA01'],
       'hydrocortisone-suppository': ['C05AA01'], 'nitroglycerin-ointment': ['C05AE01'], 'lotilaner-eye': ['S01AX25'], 'orlistat': ['A08AB01'], 'ruxolitinib-cream': ['D11AH09'],
       'glycopyrronium-cloth': ['D11AA01'], 'berdazimer': ['D06BB13'], 'rabeprazole': ['A02BC04'], 'granisetron': ['A04AA02'], 'prasugrel': ['B01AC22'], 'doxazosin': ['C02CA04'],
       'terazosin': ['G04CA03'], 'sotalol': ['C07AA07'], 'propafenone': ['C01BC03'], 'flecainide': ['C01BC04'], 'amiloride': ['C03DB01'], 'metolazone': ['C03BA08'],
       'insulin-lispro': ['A10AB04'], 'insulin-degludec': ['A10AE06'], 'dulaglutide': ['A10BJ05'], 'teriparatide': ['H05AA02'], 'ibandronate': ['M05BA06'], 'liothyronine': ['H03AA02'],
       'octreotide': ['H01CB02'], 'meropenem': ['J01DH02'], 'imipenem-cilastatin': ['J01DH51'], 'piperacillin-tazobactam': ['J01CR05'], 'cefepime': ['J01DE01'], 'linezolid': ['J01XX08'],
       'colistimethate': ['J01XB01'], 'dolutegravir': ['J05AJ03'], 'lamivudine': ['J05AF05'], 'zidovudine': ['J05AF01'], 'hydromorphone': ['N02AA03'], 'tapentadol': ['N02AX06'],
       'fentanyl-injection': ['N01AH01'], 'orphenadrine': ['M03BC01'], 'etoricoxib': ['M01AH05'], 'melatonin': ['N05CH01'], 'desvenlafaxine': ['N06AX23'], 'paliperidone': ['N05AX13'],
       'lurasidone': ['N05AE05'], 'zonisamide': ['N03AX15'], 'brivaracetam': ['N03AX23'], 'roflumilast': ['R03DX07'], 'dutasteride': ['G04CB02'], 'mirabegron': ['G04BD12']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
