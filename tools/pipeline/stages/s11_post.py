"""Stage 11 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
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

# Pediatric: the classifier matched boxed warnings (accidental exposure, TNF-blocker malignancy), not the pediatric-use statement.
edit('fentanyl-patch', pop('pediatric', 'caution', 'برچسب: در کودکان ۲ سال به بالا فقط اگر مقاوم به اپیوئید باشند. مواجهه تصادفی حتی یک چسب در کودک کشنده است.', 'Label: children ≥2 y only if opioid-tolerant. Accidental exposure to even one patch is fatal in children.',
                             'The safety of fentanyl transdermal system was evaluated in three open-label trials in 289 pediatric patients with chronic pain, 2 years of age through 18 years of age.', '8.4'))
edit('adalimumab', pop('pediatric', 'caution', 'برچسب: در JIA از ۲ سالگی و برخی اندیکاسیون‌های دیگر ثابت شده؛ هشدار جعبه‌ای لنفوم و بدخیمی در کودکان و نوجوانان.', 'Label: established for JIA from 2 y and some other indications; boxed warning of lymphoma and malignancy in children and adolescents.',
                         'The safety and effectiveness of HUMIRA have been established for: reducing signs and symptoms of moderately to severely active polyarticular JIA in pediatric patients 2 years of age and older.', '8.4'))
edit('etanercept', pop('pediatric', 'caution', 'برچسب: در pJIA از ۲ سالگی ثابت شده؛ هشدار جعبه‌ای لنفوم و بدخیمی در کودکان و نوجوانان.', 'Label: established for pJIA from 2 y; boxed warning of lymphoma and malignancy in children and adolescents.',
                         'The safety and effectiveness of Enbrel have been established in pediatric patients 2 years of age and older with pJIA.', '8.4'))
edit('infliximab', pop('pediatric', 'caution', 'برچسب: در کرون و کولیت اولسروز ۶ تا ۱۷ سال ثابت شده؛ هشدار جعبه‌ای لنفوم و بدخیمی در کودکان و نوجوانان.', 'Label: established for CD and UC at 6–17 y; boxed warning of lymphoma and malignancy in children and adolescents.',
                         'The safety and effectiveness of REMICADE have been established in pediatric patients 6 to 17 years of age for induction and maintenance treatment of CD and UC.', '8.4'))
# Pregnancy: the classifier matched a study/kinetics sentence, not the risk summary.
edit('etanercept', pop('pregnancy', 'caution', 'برچسب: مطالعات موجود ارتباط قابل‌اعتمادی با نقص مادرزادی بزرگ نشان نمی‌دهند.', 'Label: available studies do not reliably support an association with major birth defects.',
                        'Available studies with use of etanercept during pregnancy do not reliably support an association between etanercept and major birth defects.', '8.1'))
edit('filgrastim', pop('pregnancy', 'caution', 'برچسب: داده‌های موجود ارتباطی با نقص مادرزادی، سقط یا پیامد بد نشان نداده‌اند.', 'Label: available data have not established an association with birth defects, miscarriage or adverse outcomes.',
                        'Available data from published studies, including several observational studies of pregnancy outcomes in women exposed to filgrastim products and those who were unexposed, have not established an association with NEUPOGEN use during pregnancy and major birth defects, miscarriage, or adverse maternal or fetal outcomes.', '8.1'))
# Dinoprostone is used only in pregnancy (cervical ripening); the matched sentence is about obstetric contraindications.
edit('dinoprostone', pop('pregnancy', 'caution', 'فقط برای آماده‌سازی دهانه رحم در بارداری ترم و در بیمارستان؛ در شرایط منع داروی اکسی‌توسیک (سزارین قبلی، عدم تناسب سر و لگن...) نه.', 'Used only for cervical ripening in term pregnancy, in hospital; not where oxytocics are contraindicated (previous Caesarean, cephalopelvic disproportion…).',
                          'Patients in whom oxytocic drugs are generally contraindicated or where prolonged contractions of the uterus are considered inappropriate', 'Contraindications'))
print('s11_post ok')
