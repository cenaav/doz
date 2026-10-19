"""Stage 14 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py.
No WHO code (left empty): succimer. iron-dextran uses group B03AC like the other parenteral irons (no substance-level entry found)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'remifentanil': ['N01AH06'], 'sufentanil': ['N01AH03'], 'vecuronium': ['M03AC03'], 'cisatracurium': ['M03AC11'], 'ropivacaine': ['N01BB09'], 'sevoflurane': ['N01AB08'],
       'isoflurane': ['N01AB06'], 'desflurane': ['N01AB07'], 'albumin': ['B05AA01'], 'potassium-phosphate': ['B05XA06'], 'factor-viii': ['B02BD02'], 'kcentra': ['B02BD01'],
       'fibrinogen': ['B02BB01'], 'ivig': ['J06BA02'], 'physostigmine': ['V03AB19'], 'dimercaprol': ['V03AB09'], 'edetate-calcium-disodium': ['V03AB03'], 'penicillamine': ['M01CC01'],
       'botulism-antitoxin': ['J06AA04'], 'terlipressin': ['H01BA04'], 'ceftazidime-avibactam': ['J01DD52'], 'ceftolozane-tazobactam': ['J01DI54'], 'meropenem-vaborbactam': ['J01DH52'],
       'bosentan': ['C02KX01'], 'ambrisentan': ['C02KX02'], 'macitentan': ['C02KX04'], 'riociguat': ['C02KX05'], 'treprostinil': ['B01AC21'], 'epoprostenol': ['B01AC09'], 'iloprost': ['B01AC11'],
       'mifepristone': ['G03XB01'], 'etonogestrel-implant': ['G03AC08'], 'levonorgestrel-ius': ['G02BA03'], 'chorionic-gonadotropin': ['G03GA01'], 'menotropins': ['G03GA02'],
       'calcitonin': ['H05BA01'], 'iron-dextran': ['B03AC'],
       'ifosfamide': ['L01AA06'], 'irinotecan': ['L01CE02'], 'bleomycin': ['L01DC01'], 'vinblastine': ['L01CA01'], 'vinorelbine': ['L01CA04'], 'daunorubicin': ['L01DB02'], 'epirubicin': ['L01DB03'],
       'melphalan': ['L01AA03'], 'chlorambucil': ['L01AA02'], 'busulfan': ['L01AB01'], 'bendamustine': ['L01AA09'], 'azacitidine': ['L01BC07'], 'fludarabine': ['L01BB05'], 'pemetrexed': ['L01BA04'],
       'temozolomide': ['L01AX03'], 'dasatinib': ['L01EA02'], 'nilotinib': ['L01EA03'], 'ibrutinib': ['L01EL01'], 'osimertinib': ['L01EB04'], 'erlotinib': ['L01EB02'], 'gefitinib': ['L01EB01'],
       'sorafenib': ['L01EX02'], 'sunitinib': ['L01EX01'], 'pazopanib': ['L01EX03'], 'olaparib': ['L01XK01'], 'palbociclib': ['L01EF01'], 'thalidomide': ['L04AX02'], 'atezolizumab': ['L01FF05'],
       'durvalumab': ['L01FF03'], 'ipilimumab': ['L01FX04'], 'cetuximab': ['L01FE01'], 'panitumumab': ['L01FE02'], 'pertuzumab': ['L01FD02'], 'daratumumab': ['L01FC01'], 'blinatumomab': ['L01FX07'],
       'flutamide': ['L02BB01'], 'megestrol': ['L02AB01'], 'pegfilgrastim': ['L03AA13']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
