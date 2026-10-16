"""Stage 12 — WHO ATC codes (checked on atcddd.fhi.no) for the new drugs; run before enrich.py. Fosaprepitant has no WHO entry."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find
ATC = {'abacavir': ['J05AF06'], 'abatacept': ['L04AA24'], 'acitretin': ['D05BB02'], 'aclidinium': ['R03BB05'], 'aflibercept': ['S01LA05'], 'alfuzosin': ['G04CA01'], 'alosetron': ['A03AE01'], 
       'aminocaproic-acid': ['B02AA01'], 'anakinra': ['L04AC03'], 'andexanet': ['V03AB38'], 'anidulafungin': ['J02AX06'], 'apomorphine': ['N04BC07'], 'aprepitant': ['A04AD12'], 
       'asenapine': ['N05AH05'], 'atazanavir': ['J05AE08'], 'atogepant': ['N02CD07'], 'aztreonam': ['J01DF01'], 'bedaquiline': ['J04AK05'], 'belimumab': ['L04AG04'], 
       'benralizumab': ['R03DX10'], 'benztropine': ['N04AC01'], 'biktarvy': ['J05AR20'], 'bimatoprost': ['S01EE03'], 'cabenuva': ['J05AJ04', 'J05AG05'], 'canagliflozin': ['A10BK02'], 
       'cangrelor': ['B01AC25'], 'cannabidiol': ['N03AX24'], 'cefoxitin': ['J01DC01'], 'certolizumab': ['L04AB05'], 'cladribine': ['L04AA40'], 'clevidipine': ['C08CA16'], 
       'cyanocobalamin': ['B03BA01'], 'dalteparin': ['B01AB04'], 'dantrolene': ['M03CA01'], 'dapsone': ['J04BA02'], 'daptomycin': ['J01XX09'], 'darbepoetin': ['B03XA02'], 
       'daridorexant': ['N05CJ03'], 'darifenacin': ['G04BD10'], 'darunavir': ['J05AE10'], 'degarelix': ['L02BX02'], 'dexlansoprazole': ['A02BC06'], 'dexmethylphenidate': ['N06BA11'], 
       'diazoxide': ['V03AH01'], 'dipyridamole': ['B01AC07'], 'dofetilide': ['C01BD04'], 'dornase-alfa': ['R05CB13'], 'dronabinol': ['A04AD10'], 'dronedarone': ['C01BD07'], 
       'efavirenz': ['J05AG03'], 'efinaconazole': ['D01AC19'], 'eletriptan': ['N02CC06'], 'eltrombopag': ['B02BX05'], 'eluxadoline': ['A07DA06'], 'emicizumab': ['B02BX06'], 
       'eptinezumab': ['N02CD05'], 'ertugliflozin': ['A10BK04'], 'eslicarbazepine': ['N03AF04'], 'eszopiclone': ['N05CF04'], 'ethacrynic-acid': ['C03CC01'], 'exenatide': ['A10BJ01'], 
       'felbamate': ['N03AX10'], 'fenfluramine': ['N03AX26'], 'fidaxomicin': ['A07AA12'], 'flucytosine': ['J02AX01'], 'fluphenazine': ['N05AB02'], 'fluticasone-vilanterol': ['R03AK10'], 
       'foscarnet': ['J05AD01'], 'fremanezumab': ['N02CD03'], 'frovatriptan': ['N02CC07'], 'galantamine': ['N06DA04'], 'ganciclovir': ['J05AB06'], 'glatiramer': ['L03AX13'], 
       'glycopyrrolate': ['A03AB02'], 'golimumab': ['L04AB06'], 'goserelin': ['L02AE03'], 'guselkumab': ['L04AC16'], 'idarucizumab': ['V03AB37'], 'iloperidone': ['N05AX14'], 
       'interferon-beta-1a': ['L03AB07'], 'isoproterenol': ['C01CA02'], 'ixekizumab': ['L04AC13'], 'lasmiditan': ['N02CC08'], 'lecanemab': ['N06DX04'], 'lemborexant': ['N05CJ02'], 
       'leuprolide': ['L02AE02'], 'levomilnacipran': ['N06AX28'], 'lifitegrast': ['S01XA25'], 'loxapine': ['N05AH01'], 'lubiprostone': ['A06AX03'], 'lumateperone': ['N05AD10'], 
       'mepolizumab': ['R03DX09'], 'micafungin': ['J02AX05'], 'milnacipran': ['N06AX17'], 'milrinone': ['C01CE02'], 'nadolol': ['C07AA12'], 'naratriptan': ['N02CC02'], 
       'natalizumab': ['L04AG03'], 'nefazodone': ['N06AX06'], 'nicardipine-iv': ['C08CA04'], 'nitroprusside': ['C02DD01'], 'ocrelizumab': ['L04AG08'], 'ofatumumab': ['L04AG12'], 
       'olodaterol': ['R03AC19'], 'onabotulinumtoxina': ['M03AX01'], 'ozanimod': ['L04AE02'], 'palonosetron': ['A04AA05'], 'paricalcitol': ['H05BX02'], 'pasireotide': ['H01CB05'], 
       'pegloticase': ['M04AX02'], 'phenelzine': ['N06AF03'], 'pilocarpine-presbyopia': ['S01EB01'], 'pimozide': ['N05AG02'], 'plecanatide': ['A06AX07'], 'posaconazole': ['J02AC04'], 
       'pramlintide': ['A10BX05'], 'primidone': ['N03AA03'], 'probenecid': ['M04AB01'], 'pyrimethamine': ['P01BD01'], 'raltegravir': ['J05AJ01'], 'ramelteon': ['N05CH02'], 
       'ranibizumab': ['S01LA04'], 'ribavirin': ['J05AP01'], 'rilpivirine': ['J05AG05'], 'risankizumab': ['L04AC18'], 'romiplostim': ['B02BX04'], 'rotigotine': ['N04BC09'], 
       'selegiline': ['N04BD01'], 'silodosin': ['G04CA04'], 'siponimod': ['L04AE03'], 'somatropin': ['H01AC01'], 'stiripentol': ['N03AX17'], 'tavaborole': ['D01AE24'], 
       'tazarotene': ['D05AX05'], 'tedizolid': ['J01XX11'], 'tenofovir-alafenamide': ['J05AF13'], 'tezepelumab': ['R03DX11'], 'tigecycline': ['J01AA12'], 'tildrakizumab': ['L04AC17'], 
       'tocilizumab': ['L04AC07'], 'tranylcypromine': ['N06AF04'], 'travoprost': ['S01EE04'], 'trospium': ['G04BD09'], 'umeclidinium': ['R03BB07'], 'valganciclovir': ['J05AB14'], 
       'vedolizumab': ['L04AG05'], 'vibegron': ['G04BD15'], 'vilazodone': ['N06AX24'], 'viloxazine': ['N06AX09'], 'zafirlukast': ['R03DC01'], 'zaleplon': ['N05CF03'], 
       'zanamivir': ['J05AH01'], 'zolmitriptan': ['N02CC03']}
for i, codes in ATC.items():
    p = find(i); d = json.load(open(p)); d['atc'] = codes
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
print(len(ATC), 'atc set')
