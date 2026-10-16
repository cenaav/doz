"""Stage 12 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def pop(key, level, fa, en, quote, section):
    def fn(d):
        src = d['populations'][key]['refs'][0]['source']
        d['populations'][key].update(level=level, text=T(fa, en), quote=quote, refs=[{'source': src, 'section': section}])
    return fn

# Pregnancy: the classifier matched the registry-methodology sentence (MACDP), not the risk summary.
APR_FA, APR_EN = 'برچسب: داده‌های رجیستری بارداری (APR) تفاوتی با میزان زمینه‌ای نقص مادرزادی نشان نمی‌دهد.', 'Label: Antiretroviral Pregnancy Registry data show no difference from the background birth-defect rate.'
edit('abacavir', pop('pregnancy', 'caution', APR_FA, APR_EN, 'Available data from the APR show no difference in the overall risk of birth defects for abacavir compared with the background rate for birth defects of 2.7% in the Metropolitan Atlanta Congenital Defects Program (MACDP) reference population.', '8.1'))
edit('raltegravir', pop('pregnancy', 'caution', APR_FA, APR_EN, 'Available data from the APR show no difference in the rate of overall birth defects for raltegravir compared to the background rate for major birth defects of 2.7% in the U.S. reference population of the Metropolitan Atlanta Congenital Defects Program (MACDP).', '8.1'))
edit('rilpivirine', pop('pregnancy', 'caution', APR_FA, APR_EN, 'Available data from the APR show no difference in the overall risk of birth defects for rilpivirine compared with the background rate for major birth defects of 2.7% in the Metropolitan Atlanta Congenital Defects Program (MACDP) reference population.', '8.1'))
edit('tenofovir-alafenamide', pop('pregnancy', 'caution', APR_FA, APR_EN, 'Available data from the APR show no statistically significant difference in the overall risk of birth defects for tenofovir alafenamide (TAF) compared with the background rate for major birth defects of 2.7% in the U.S. reference population of the Metropolitan Atlanta Congenital Defects Program (MACDP).', '8.1'))
edit('biktarvy', pop('pregnancy', 'caution', 'برچسب: داده‌های مشاهده‌ای و رجیستری خطر دارویی نقص مادرزادی بزرگ، سقط یا پیامد بد را ثابت نکرده‌اند.', 'Label: observational and registry data have not established a drug-associated risk of major birth defects, miscarriage or adverse outcomes.',
                     'Available data from observational studies and the APR with BIC, FTC and TAF use during pregnancy have not established a drug-associated risk of major birth defects, miscarriage or other adverse maternal or fetal outcomes.', '8.1'))
edit('cabenuva', pop('pregnancy', 'caution', 'برچسب: داده انسانی کافی نیست؛ سود و خطر با فرد بارور یا باردار بحث شود (دارو تا ۱۲ ماه در گردش خون می‌ماند).', 'Label: insufficient human data; discuss benefit-risk with people who could become or are pregnant (drug persists up to 12 months).',
                     'There are insufficient human data on the use of CABENUVA during pregnancy to adequately assess a drug-associated risk of birth defects and miscarriage. Discuss the benefit-risk of using CABENUVA with individuals of childbearing potential or during pregnancy.', '8.1'))
# Pediatric: the classifier matched boxed warnings (TNF-blocker malignancy, toxin spread), not the pediatric-use statement.
edit('certolizumab', pop('pediatric', 'caution', 'برچسب: در JIA پلی‌آرتیکولار از ۲ سالگی ثابت شده؛ هشدار جعبه‌ای لنفوم و بدخیمی در کودکان و نوجوانان.', 'Label: established for polyarticular JIA from 2 y; boxed warning of lymphoma and malignancy in children and adolescents.',
                         'The safety and effectiveness of CIMZIA for active polyarticular juvenile idiopathic arthritis has been established in pediatric patients 2 years of age and older.', '8.4'))
edit('golimumab', pop('pediatric', 'caution', 'برچسب: در کولیت اولسراتیو کودکان ≥۱۵ kg ثابت شده؛ هشدار جعبه‌ای لنفوم و بدخیمی در کودکان و نوجوانان.', 'Label: established for ulcerative colitis in children ≥15 kg; boxed warning of lymphoma and malignancy in children and adolescents.',
                      'The safety and effectiveness of SIMPONI for the treatment of moderately to severely active ulcerative colitis have been established in pediatric patients weighing at least 15 kg.', '8.4'))
edit('onabotulinumtoxina', pop('pediatric', 'caution', 'برچسب: در برخی اندیکاسیون‌ها (اسپاستیسیته، مثانه نوروژنیک از ۵ سالگی) ثابت شده؛ خطر انتشار سم در کودکان با اسپاستیسیته بیشتر است.', 'Label: established for some indications (spasticity, neurogenic bladder from 5 y); toxin-spread risk is greatest in children treated for spasticity.',
                               'The safety and effectiveness of BOTOX for detrusor overactivity associated with a neurologic condition have been established in pediatric patients 5 years of age and older.', '8.4'))
# Pediatric: the classifier matched a narrower "not established" sentence although the label supports paediatric use.
edit('daptomycin', pop('pediatric', 'caution', 'برچسب: در عفونت پوست و باکتریمی استاف از ۱ تا ۱۷ سال ثابت شده؛ زیر ۱ سال نه.', 'Label: established for cSSSI and S. aureus bacteraemia at 1–17 y; not under 1 y.',
                       'The safety and effectiveness of CUBICIN RF in the treatment of cSSSI and S. aureus bloodstream infections (bacteremia) have been established in the age groups 1 to 17 years of age.', '8.4'))
edit('anakinra', pop('pediatric', 'caution', 'برچسب: در NOMID کودکان (از زیر ۲ سال) با ۱ تا ۲ mg/kg/روز استفاده شده؛ در JRA ثابت نشده.', 'Label: used in paediatric NOMID (including under 2 y) at 1–2 mg/kg/day; not established for JRA.',
                     'The NOMID study included 36 pediatric patients: 13 below 2 years, 18 between 2 and 11 years, and 5 between 12 and 17 years of age.', '8.4'))
edit('felbamate', pop('pediatric', 'caution', 'برچسب: فقط در لنوکس-گاستو کودکان ثابت شده؛ سایر کودکان ثابت نشده.', 'Label: established only for Lennox-Gastaut in children; not established in other children.',
                      'The safety and effectiveness of Felbatol in children other than those with Lennox-Gastaut syndrome has not been established.', 'Pediatric Use'))
edit('glycopyrrolate', pop('pediatric', 'caution', 'برچسب: پیش‌داروی بیهوشی در کودکان (۰٫۰۰۴ mg/kg) دارد؛ نوزاد زیر ۱ ماه نه (بنزیل الکل)؛ برای زخم پپتیک ثابت نشده.', 'Label: paediatric pre-anaesthetic dosing (0.004 mg/kg); not in neonates under 1 month (benzyl alcohol); not established for peptic ulcer.',
                           'Due to its benzyl alcohol content, glycopyrrolate injection should not be used in neonates, i.e., patients less than 1 month of age.', 'Pediatric Use'))
edit('ethacrynic-acid', pop('pediatric', 'caution', 'برچسب: مصرف خوراکی در کودکان (غیر از شیرخوار) بر اساس تجربه؛ شیرخوار و وریدی در کودکان ثابت نشده.', 'Label: oral use in children (not infants) supported by empiric use; infants and IV use in children not established.',
                            'The information on oral dosing in pediatric patients, other than infants, is supported by evidence from empiric use in this age group.', 'Pediatric Use'))
print('s12_post ok')
