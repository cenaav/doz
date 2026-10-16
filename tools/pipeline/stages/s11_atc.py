"""Stage 11 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'propofol': ['N01AX10'], 'ketamine': ['N01AX03'], 'etomidate': ['N01AX07'], 'dexmedetomidine': ['N05CM18'], 'succinylcholine': ['M03AB01'], 'rocuronium': ['M03AC09'], 'neostigmine': ['N07AA01'],
       'sugammadex': ['V03AB35'], 'bupivacaine': ['N01BB01'], 'fentanyl-patch': ['N02AB03'], 'ipv-vaccine': ['J07BF03'], 'rotavirus-vaccine': ['J07BH01'], 'meningococcal-vaccine': ['J07AH08'],
       'typhoid-vaccine': ['J07AP03'], 'zoster-vaccine': ['J07BK03'], 'rsv-vaccine': ['J07BX05'], 'covid-vaccine': ['J07BN01'], 'bcg-vaccine': ['J07AN01'], 'tuberculin-ppd': ['V04CF01'], 'palivizumab': ['J06BD01'],
       'adalimumab': ['L04AB04'], 'etanercept': ['L04AB01'], 'infliximab': ['L04AB02'], 'rituximab': ['L01FA01'], 'dupilumab': ['D11AH05'], 'omalizumab': ['R03DX05'], 'ustekinumab': ['L04AC05'],
       'secukinumab': ['L04AC10'], 'mycophenolate': ['L04AA06'], 'tacrolimus-oral': ['L04AD02'], 'cyclosporine-oral': ['L04AD01'], 'tofacitinib': ['L04AF01'], 'baricitinib': ['L04AF02'], 'upadacitinib': ['L04AF03'],
       'apremilast': ['L04AA32'], 'tamoxifen': ['L02BA01'], 'anastrozole': ['L02BG03'], 'bicalutamide': ['L02BB03'], 'imatinib': ['L01EA01'], 'capecitabine': ['L01BC06'], 'filgrastim': ['L03AA02'],
       'edoxaban': ['B01AF03'], 'fondaparinux': ['B01AX05'], 'argatroban': ['B01AE03'], 'bivalirudin': ['B01AE06'], 'tenecteplase': ['B01AD11'], 'evolocumab': ['C10AX13'], 'alirocumab': ['C10AX14'],
       'inclisiran': ['C10AX16'], 'bempedoic-acid': ['C10AX15'], 'icosapent-ethyl': ['C10AX06'], 'finerenone': ['C03DA05'], 'vericiguat': ['C01DX22'], 'perampanel': ['N03AX22'], 'cenobamate': ['N03AX25'],
       'rufinamide': ['N03AF03'], 'vigabatrin': ['N03AG04'], 'entacapone': ['N04BX02'], 'opicapone': ['N04BX04'], 'safinamide': ['N04BD03'], 'modafinil': ['N06BA07'], 'sodium-oxybate': ['N07XX04'],
       'pitolisant': ['N07XX11'], 'suvorexant': ['N05CJ01'], 'erenumab': ['N02CD01'], 'galcanezumab': ['N02CD02'], 'ubrogepant': ['N02CD04'], 'cariprazine': ['N05AX15'], 'brexpiprazole': ['N05AX16'],
       'esketamine': ['N06AX27'], 'agomelatine': ['N06AX22'], 'caspofungin': ['J02AX04'], 'remdesivir': ['J05AB16'], 'dinoprostone': ['G02AD02'], 'insulin-detemir': ['A10AE05'], 'insulin-glulisine': ['A10AB06'],
       'romosozumab': ['M05BX06']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
