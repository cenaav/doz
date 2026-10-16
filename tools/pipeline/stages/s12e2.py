"""Stage 12e (part 2) — respiratory: umeclidinium, aclidinium, olodaterol, fluticasone furoate/vilanterol, mepolizumab, benralizumab, tezepelumab, zafirlukast, dornase alfa; glycopyrrolate injection."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
inh = lambda id, mcg, label, src, sec='3': form(id, 'inhaler', 'inhaled', label, mcg, 'mcg', [R(src, sec)], per='actuation')
LAMA_W = lambda src: W('برای حمله حاد نیست؛ برونکواسپاسم متناقض؛ تشدید گلوکوم زاویه بسته و احتباس ادرار؛ حساسیت.', 'Not for acute episodes; paradoxical bronchospasm; worsening narrow-angle glaucoma and urinary retention; hypersensitivity.', [R(src, '5')])
MILK = lambda src, drug_fa, drug_en: CI('ci', f'حساسیت شدید به پروتئین شیر؛ حساسیت به {drug_fa}.', f'Severe hypersensitivity to milk proteins; hypersensitivity to {drug_en}.', [R(src, '4')])
BIO_W = lambda src: W('واکنش حساسیتی؛ برای حمله حاد آسم نیست؛ کورتیکواستروئید را ناگهانی قطع نکنید؛ عفونت کرمی پیش از شروع درمان شود.', 'Hypersensitivity; not for acute asthma; do not stop corticosteroids abruptly; treat helminth infection before starting.', [R(src, '5')])

add_disease('cystic-fibrosis', 'فیبروز کیستیک', 'Cystic fibrosis', ['CF', 'سیستیک فیبروزیس', 'فیبروز سیستیک'], ['E84.9'], 'pulmonology')
add_disease('nasal-polyps', 'رینوسینوزیت مزمن با پولیپ بینی', 'Chronic rhinosinusitis with nasal polyps', ['CRSwNP', 'پولیپ بینی', 'nasal polyps'], ['J33.9'], 'ent')
add_disease('egpa', 'گرانولوماتوز ائوزینوفیلیک با پلی‌آنژئیت (چرگ-استراوس)', 'Eosinophilic granulomatosis with polyangiitis (Churg-Strauss)', ['EGPA', 'چرگ استراوس', 'Churg-Strauss'], ['M30.1'], 'rheumatology')
add_disease('hypereosinophilic-syndrome', 'سندرم هیپرائوزینوفیلیک', 'Hypereosinophilic syndrome', ['HES', 'ائوزینوفیلی بالا'], ['D72.11'], 'hematology')

In = fda('incruse', 'FDA Incruse Ellipta', 'Incruse Ellipta (umeclidinium) inhalation powder — Prescribing Information', sid('umeclidinium'))
drug('umeclidinium', 'respiratory', 'یومکلیدینیوم', 'Umeclidinium', T('آنتی‌موسکارینی طولانی‌اثر (LAMA)', 'Long-acting muscarinic antagonist (LAMA)'), [{'name': 'Incruse Ellipta', 'market': 'US'}], ['incruse', 'اینکروز', 'یومکلیدینیوم'],
     [inh('ellipta', 62.5, '62.5 mcg per actuation (Ellipta)', In)],
     [reg('copd', 'copd', T('نگهدارنده COPD — یک استنشاق (۶۲٫۵ mcg) یک بار در روز', 'COPD maintenance — 1 inhalation (62.5 mcg) once daily'), A18, 'fixed', {'perDose': 62.5, 'dosesPerDay': 1}, [R(In, '2')], unit='mcg',
          notes=[note('هر روز یک ساعت ثابت؛ بیش از یک بار در ۲۴ ساعت نه. سالمند، نارسایی کلیه یا نارسایی متوسط کبد تنظیم ندارد.', 'Same time every day; not more than once every 24 h. No adjustment for elderly, renal impairment or moderate hepatic impairment.', [R(In, '2')])])],
     [MILK(In, 'یومکلیدینیوم', 'umeclidinium')], warn=[LAMA_W(In)],
     exs=[ex('copd', 'ellipta', {'perDose': 62.5, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

Tu = fda('tudorza', 'FDA Tudorza Pressair', 'Tudorza Pressair (aclidinium bromide) inhalation powder — Prescribing Information', sid('aclidinium'))
drug('aclidinium', 'respiratory', 'آکلیدینیوم', 'Aclidinium', T('آنتی‌موسکارینی طولانی‌اثر (LAMA)', 'Long-acting muscarinic antagonist (LAMA)'), [{'name': 'Tudorza Pressair', 'market': 'US'}], ['tudorza', 'eklira', 'آکلیدینیوم'],
     [inh('pressair', 400, '400 mcg per actuation (Pressair)', Tu)],
     [reg('copd', 'copd', T('نگهدارنده COPD — یک استنشاق ۴۰۰ mcg دو بار در روز (صبح و شب)', 'COPD maintenance — 1 inhalation of 400 mcg twice daily (morning and evening)'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 2}, [R(Tu, '2')], unit='mcg')],
     [MILK(Tu, 'آکلیدینیوم', 'aclidinium')], warn=[LAMA_W(Tu)],
     exs=[ex('copd', 'pressair', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

So = fda('striverdi', 'FDA Striverdi Respimat', 'Striverdi Respimat (olodaterol) inhalation spray — Prescribing Information', sid('olodaterol'))
drug('olodaterol', 'respiratory', 'اولوداترول', 'Olodaterol', T('آگونیست بتا-۲ طولانی‌اثر (LABA)', 'Long-acting beta2-agonist (LABA)'), [{'name': 'Striverdi Respimat', 'market': 'US'}], ['striverdi', 'استریوردی', 'اولوداترول'],
     [inh('respimat', 2.5, '2.5 mcg per actuation (Respimat); 1 dose = 2 actuations', So)],
     [reg('copd', 'copd', T('نگهدارنده COPD — دو استنشاق (۵ mcg) یک بار در روز', 'COPD maintenance — 2 inhalations (5 mcg) once daily'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(So, '2')], unit='mcg',
          notes=[note('بیش از ۲ استنشاق در ۲۴ ساعت نه. برای آسم اندیکاسیون ندارد.', 'Not more than 2 inhalations every 24 h. Not indicated for asthma.', [R(So, '2'), R(So, '4')])])],
     [CI('asthma', 'LABA بدون کورتیکواستروئید استنشاقی در آسم.', 'LABA without an inhaled corticosteroid in asthma.', [R(So, '4')])],
     warn=[W('رویدادهای جدی مرتبط با آسم؛ برای حمله حاد نیست؛ مصرف بیش از حد خطرناک است؛ برونکواسپاسم متناقض؛ اثرات قلبی؛ هیپوکالمی و هیپرگلیسمی.', 'Serious asthma-related events; not for acute episodes; excessive use is dangerous; paradoxical bronchospasm; cardiovascular effects; hypokalaemia and hyperglycaemia.', [R(So, '5')])],
     exs=[ex('copd', 'respimat', {'perDose': 5, 'tabletsPerDoseRounded': 2}, ageYears=65, weightKg=70)])

Br = fda('breo', 'FDA Breo Ellipta', 'Breo Ellipta (fluticasone furoate/vilanterol) inhalation powder — Prescribing Information', sid('breo'))
ff = lambda id, f, label: form(id, 'inhaler', 'inhaled', label, f, 'mcg', [R(Br, '3')], per='actuation')
drug('fluticasone-vilanterol', 'respiratory', 'فلوتیکازون فوروات/ویلانترول', 'Fluticasone furoate/vilanterol', T('کورتیکواستروئید استنشاقی + LABA', 'Inhaled corticosteroid + LABA'), [{'name': 'Breo Ellipta', 'market': 'US'}], ['breo', 'relvar', 'رلوار', 'برئو', 'vilanterol', 'ویلانترول'],
     [ff('e-100', 100, '100/25 mcg per actuation (fluticasone furoate dose shown)'), ff('e-200', 200, '200/25 mcg per actuation'), ff('e-50', 50, '50/25 mcg per actuation')],
     [reg('copd', 'copd', T('نگهدارنده COPD — یک استنشاق ۱۰۰/۲۵ mcg یک بار در روز', 'COPD maintenance — 1 inhalation of 100/25 mcg once daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Br, '2.1')], unit='mcg', allowed=['e-100'], doseComponent='fluticasone furoate',
          notes=[note('پس از استنشاق دهان شسته شود (کاندیدیاز). بیش از یک بار در ۲۴ ساعت نه. برای تنگی نفس بین دوزها از SABA استفاده شود.', 'Rinse mouth after use (candidiasis). Not more than once every 24 h. Use a SABA for breathlessness between doses.', [R(Br, '2.3'), R(Br, '2.1')])]),
      reg('asthma', 'asthma', T('آسم بزرگسال — یک استنشاق ۱۰۰/۲۵ یا ۲۰۰/۲۵ mcg یک بار', 'Asthma, adults — 1 inhalation of 100/25 or 200/25 mcg once daily'), A18, 'fixed', {'perDose': 100, 'perDoseMax': 200, 'dosesPerDay': 1}, [R(Br, '2.2')], unit='mcg', doseComponent='fluticasone furoate'),
      reg('asthma-teen', 'asthma', T('آسم ۱۲ تا ۱۷ سال — یک استنشاق ۱۰۰/۲۵ mcg یک بار', 'Asthma, 12–17 y — 1 inhalation of 100/25 mcg once daily'), {'minAge': age(12, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Br, '2')], unit='mcg', allowed=['e-100'], doseComponent='fluticasone furoate')],
     [CI('ci', 'درمان اولیه استاتوس آسماتیکوس یا حمله حاد COPD/آسم؛ حساسیت شدید به پروتئین شیر یا فلوتیکازون فوروات/ویلانترول.', 'Primary treatment of status asthmaticus or acute COPD/asthma episodes; severe milk-protein hypersensitivity or hypersensitivity to fluticasone furoate/vilanterol.', [R(Br, '4')])],
     warn=[W('رویدادهای جدی آسم با LABA؛ کاندیدیاز دهان؛ پنومونی در COPD؛ سرکوب ایمنی و آدرنال؛ مهارکننده قوی CYP3A4؛ کاهش تراکم استخوان؛ تأثیر بر رشد؛ گلوکوم و آب مروارید.', 'Serious asthma events with LABA; oral candidiasis; pneumonia in COPD; immunosuppression and adrenal suppression; strong CYP3A4 inhibitors; reduced bone density; effect on growth; glaucoma and cataract.', [R(Br, '5')])],
     exs=[ex('copd', 'e-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70), ex('asthma', 'e-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('asthma-teen', 'e-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=14, weightKg=50)])

Nu = fda('nucala', 'FDA Nucala', 'Nucala (mepolizumab) for injection and injection — Prescribing Information', sid('mepolizumab'))
pfs = lambda id, mg, ml, label, src: form(id, 'injection', 'sc', label, mg, 'mg', [R(src, '3')], vol=ml)
drug('mepolizumab', 'respiratory', 'مپولیزوماب', 'Mepolizumab', T('آنتی‌بادی ضد IL-5', 'Anti-IL-5 antibody'), [{'name': 'Nucala', 'market': 'US'}], ['nucala', 'نوکالا', 'مپولیزوماب'],
     [pfs('pfs-100', 100, 1, '100 mg/mL prefilled syringe or autoinjector', Nu), pfs('pfs-40', 40, 0.4, '40 mg/0.4 mL prefilled syringe', Nu)],
     [reg('asthma', 'asthma', T('آسم شدید ائوزینوفیلیک (۱۲ سال به بالا) — ۱۰۰ mg زیرجلدی هر ۴ هفته', 'Severe eosinophilic asthma (≥12 y) — 100 mg SC every 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Nu, '2.1, Table 1')], dur=ONE, allowed=['pfs-100']),
      reg('asthma-child', 'asthma', T('آسم شدید ائوزینوفیلیک کودک ۶ تا ۱۱ سال — ۴۰ mg هر ۴ هفته', 'Severe eosinophilic asthma, children 6–11 y — 40 mg every 4 weeks'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 40, 'dosesPerDay': 1}, [R(Nu, '2.1, Table 1')], dur=ONE, allowed=['pfs-40']),
      reg('crswnp', 'nasal-polyps', T('رینوسینوزیت مزمن با پولیپ بینی بزرگسال — ۱۰۰ mg هر ۴ هفته', 'CRSwNP, adults — 100 mg every 4 weeks'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Nu, '2.1')], dur=ONE, allowed=['pfs-100']),
      reg('copd', 'copd', T('COPD با فنوتیپ ائوزینوفیلیک (افزودنی) بزرگسال — ۱۰۰ mg هر ۴ هفته', 'COPD with eosinophilic phenotype (add-on), adults — 100 mg every 4 weeks'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Nu, '2.1')], dur=ONE, allowed=['pfs-100']),
      reg('egpa', 'egpa', T('EGPA بزرگسال — ۳۰۰ mg هر ۴ هفته (سه تزریق ۱۰۰ mg با ۵ cm فاصله)', 'EGPA, adults — 300 mg every 4 weeks (three 100 mg injections ≥5 cm apart)'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Nu, '2.1, Table 1')], dur=ONE, allowed=['pfs-100']),
      reg('hes', 'hypereosinophilic-syndrome', T('سندرم هیپرائوزینوفیلیک (۱۲ سال به بالا) — ۳۰۰ mg هر ۴ هفته', 'Hypereosinophilic syndrome (≥12 y) — 300 mg every 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Nu, '2.1')], dur=ONE, allowed=['pfs-100'])],
     [CI('hyper', 'سابقه حساسیت به مپولیزوماب.', 'History of hypersensitivity to mepolizumab.', [R(Nu, '4')])],
     warn=[BIO_W(Nu), W('هرپس زوستر (واکسن پیش از شروع در نظر گرفته شود).', 'Herpes zoster (consider vaccination before starting).', [R(Nu, '5.3')])],
     exs=[ex('asthma', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=40, weightKg=70), ex('asthma-child', 'pfs-40', {'perDose': 40, 'mlPerDose': 0.4}, ageYears=8, weightKg=25), ex('crswnp', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=40, weightKg=70),
          ex('copd', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=65, weightKg=70), ex('egpa', 'pfs-100', {'perDose': 300, 'mlPerDose': 3}, ageYears=50, weightKg=70), ex('hes', 'pfs-100', {'perDose': 300, 'mlPerDose': 3}, ageYears=40, weightKg=70)])

Fs = fda('fasenra', 'FDA Fasenra', 'Fasenra (benralizumab) injection — Prescribing Information', sid('benralizumab'))
drug('benralizumab', 'respiratory', 'بنرالیزوماب', 'Benralizumab', T('آنتی‌بادی ضد گیرنده IL-5', 'Anti-IL-5 receptor antibody'), [{'name': 'Fasenra', 'market': 'US'}], ['fasenra', 'فاسنرا', 'بنرالیزوماب'],
     [pfs('pfs-30', 30, 1, '30 mg/mL prefilled syringe or pen', Fs), pfs('pfs-10', 10, 0.5, '10 mg/0.5 mL prefilled syringe', Fs)],
     [reg('asthma', 'asthma', T('آسم شدید ائوزینوفیلیک (۱۲ سال به بالا) — ۳۰ mg زیرجلدی هر ۴ هفته برای ۳ دوز، سپس هر ۸ هفته', 'Severe eosinophilic asthma (≥12 y) — 30 mg SC every 4 weeks for 3 doses, then every 8 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Fs, '2.1')], dur=ONE, allowed=['pfs-30']),
      reg('asthma-child', 'asthma', T('آسم شدید کودک ۶ تا ۱۱ سال — زیر ۳۵ kg: ۱۰ mg؛ ۳۵ kg و بالاتر: ۳۰ mg (هر ۴ هفته ×۳، سپس هر ۸ هفته)', 'Severe asthma, children 6–11 y — <35 kg: 10 mg; ≥35 kg: 30 mg (every 4 weeks ×3, then every 8 weeks)'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 34.99, 'perDose': 10, 'dosesPerDay': 1}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 30, 'dosesPerDay': 1}]}, [R(Fs, '2.1, Table 1')], dur=ONE),
      reg('egpa', 'egpa', T('EGPA بزرگسال — ۳۰ mg هر ۴ هفته', 'EGPA, adults — 30 mg every 4 weeks'), A18, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Fs, '2.2')], dur=ONE, allowed=['pfs-30']),
      reg('hes', 'hypereosinophilic-syndrome', T('سندرم هیپرائوزینوفیلیک — ۳۰ mg هر ۴ هفته', 'Hypereosinophilic syndrome — 30 mg every 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Fs, '2.3')], dur=ONE, allowed=['pfs-30'])],
     [CI('hyper', 'حساسیت به بنرالیزوماب.', 'Hypersensitivity to benralizumab.', [R(Fs, '4')])], warn=[BIO_W(Fs)],
     exs=[ex('asthma', 'pfs-30', {'perDose': 30, 'mlPerDose': 1}, ageYears=40, weightKg=70), ex('asthma-child', 'pfs-10', {'perDose': 10, 'mlPerDose': 0.5}, ageYears=8, weightKg=25), ex('asthma-child', 'pfs-30', {'perDose': 30, 'mlPerDose': 1}, ageYears=11, weightKg=40),
          ex('egpa', 'pfs-30', {'perDose': 30, 'mlPerDose': 1}, ageYears=50, weightKg=70), ex('hes', 'pfs-30', {'perDose': 30, 'mlPerDose': 1}, ageYears=40, weightKg=70)])

Tz = fda('tezspire', 'FDA Tezspire', 'Tezspire (tezepelumab-ekko) injection — Prescribing Information', sid('tezepelumab'))
drug('tezepelumab', 'respiratory', 'تزپلوماب', 'Tezepelumab', T('آنتی‌بادی ضد TSLP', 'Anti-TSLP antibody'), [{'name': 'Tezspire', 'market': 'US'}], ['tezspire', 'تزسپایر', 'تزپلوماب'],
     [pfs('pfs-210', 210, 1.91, '210 mg/1.91 mL (110 mg/mL) syringe, pen or vial', Tz)],
     [reg('asthma', 'asthma', T('آسم شدید (افزودنی، ۱۲ سال به بالا) — ۲۱۰ mg زیرجلدی هر ۴ هفته', 'Severe asthma (add-on, ≥12 y) — 210 mg SC every 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 210, 'dosesPerDay': 1}, [R(Tz, '2.1')], dur=ONE)],
     [CI('hyper', 'حساسیت به تزپلوماب.', 'Hypersensitivity to tezepelumab.', [R(Tz, '4')])], warn=[BIO_W(Tz), W('واکسن زنده در طول درمان نه.', 'Avoid live attenuated vaccines.', [R(Tz, '5.5')])],
     exs=[ex('asthma', 'pfs-210', {'perDose': 210, 'mlPerDose': 1.91}, ageYears=40, weightKg=70)])

Za = fda('zafirlukast', 'FDA Zafirlukast', 'Zafirlukast tablets 10/20 mg — Prescribing Information', sid('zafirlukast')); d = R(Za, 'Dosage and Administration')
drug('zafirlukast', 'respiratory', 'زافیرلوکاست', 'Zafirlukast', T('آنتاگونیست گیرنده لکوترین', 'Leukotriene receptor antagonist'), [{'name': 'Accolate', 'market': 'US'}], ['accolate', 'آکولیت', 'زافیرلوکاست'],
     [tab('tab-20', 20, '20 mg tablet', [R(Za, 'How Supplied')]), tab('tab-10', 10, '10 mg tablet', [R(Za, 'How Supplied')])],
     [reg('adult', 'asthma', T('پیشگیری و درمان مزمن آسم (۱۲ سال به بالا) — ۲۰ mg دو بار در روز', 'Asthma prophylaxis and chronic treatment (≥12 y) — 20 mg twice daily'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 20, 'dosesPerDay': 2}, [d], allowed=['tab-20'],
          notes=[note('دست‌کم ۱ ساعت قبل یا ۲ ساعت بعد از غذا. برای برونکواسپاسم حاد نیست.', 'At least 1 h before or 2 h after meals. Not for acute bronchospasm.', [d])]),
      reg('child', 'asthma', T('کودک ۵ تا ۱۱ سال — ۱۰ mg دو بار در روز', 'Children 5–11 y — 10 mg twice daily'), {'minAge': age(5, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 2}, [d], allowed=['tab-10'])],
     [CI('ci', 'حساسیت به زافیرلوکاست؛ نارسایی کبد از جمله سیروز.', 'Hypersensitivity to zafirlukast; hepatic impairment including cirrhosis.', [R(Za, 'Contraindications')])],
     warn=[W('سمیت کبدی و نارسایی کبد تهدیدکننده حیات — با علائم کبدی قطع و آزمایش.', 'Hepatotoxicity including life-threatening hepatic failure — stop and test if hepatic symptoms.', [R(Za, 'Warnings')])],
     exs=[ex('adult', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('child', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=8, weightKg=25)])

Pz = fda('pulmozyme', 'FDA Pulmozyme', 'Pulmozyme (dornase alfa) inhalation solution — Prescribing Information', sid('dornase'))
drug('dornase-alfa', 'respiratory', 'دورناز آلفا', 'Dornase alfa', T('آنزیم موکولیتیک (DNase)', 'Mucolytic enzyme (DNase)'), [{'name': 'Pulmozyme', 'market': 'US'}], ['pulmozyme', 'پالموزایم', 'dornase', 'دورناز'],
     [form('amp-2-5', 'solution', 'inhaled', '2.5 mg/2.5 mL ampule for nebulizer', 1, 'mg', [R(Pz, '3')], vol=1)],
     [reg('cf', 'cystic-fibrosis', T('فیبروز کیستیک — ۲٫۵ mg (یک آمپول) یک بار در روز با نبولایزر توصیه‌شده', 'Cystic fibrosis — 2.5 mg (one ampule) once daily via a recommended nebulizer'), {}, 'fixed', {'perDose': 2.5, 'dosesPerDay': 1}, [R(Pz, '2.1')],
          notes=[note('برخی بیماران از دو بار در روز سود می‌برند. با سایر داروها در نبولایزر مخلوط نشود.', 'Some patients may benefit from twice daily. Do not mix with other drugs in the nebulizer.', [R(Pz, '2.1'), R(Pz, '2.2')])])],
     [CI('hyper', 'حساسیت به دورناز آلفا یا فرآورده‌های سلول تخمدان همستر چینی.', 'Hypersensitivity to dornase alfa or Chinese hamster ovary cell products.', [R(Pz, '4')])],
     exs=[ex('cf', 'amp-2-5', {'perDose': 2.5, 'mlPerDose': 2.5}, ageYears=10, weightKg=30)])

Gp = fda('glycopyrrolate-inj', 'FDA Glycopyrrolate inj', 'Glycopyrrolate injection USP 0.2 mg/mL (American Regent) — Prescribing Information', sid('glycopyrrolate')); d = R(Gp, 'Dosage and Administration')
drug('glycopyrrolate', 'alimentary-metabolism', 'گلیکوپیرولات (تزریقی)', 'Glycopyrrolate (injection)', T('آنتی‌کولینرژیک (آنتی‌موسکارینی)', 'Anticholinergic (antimuscarinic)'), [{'name': 'Robinul', 'market': 'US'}], ['robinul', 'روبینول', 'glycopyrronium', 'گلیکوپیرونیوم', 'گلیکوپیرولات'],
     [form('vial-0-2', 'injection', 'iv', '0.2 mg/mL vial (IM or IV)', 0.2, 'mg', [R(Gp, 'How Supplied')], vol=1)],
     [once('premed', 'general-anesthesia', 'پیش‌دارو پیش از بیهوشی (کاهش ترشحات، مهار رفلکس واگ) — ۰٫۰۰۴ mg/kg عضلانی ۳۰ تا ۶۰ دقیقه پیش از القا', 'Pre-anaesthetic medication (reduce secretions, block vagal reflexes) — 0.004 mg/kg IM 30–60 min before induction', {'minAge': age(2, 'year')}, 0.004, None, [d]),
      once('premed-inf', 'general-anesthesia', 'پیش‌دارو — شیرخوار ۱ ماه تا ۲ سال: ۰٫۰۰۴ تا ۰٫۰۰۹ mg/kg عضلانی', 'Pre-anaesthetic — infants 1 month–2 y: 0.004–0.009 mg/kg IM', {'minAge': age(1, 'month'), 'maxAge': age(2, 'year')}, 0.004, 0.009, [d]),
      reg('rev', 'general-anesthesia', T('برگشت بلوک عصبی-عضلانی — ۰٫۲ mg به‌ازای هر ۱ mg نئوستیگمین (یا ۵ mg پیریدوستیگمین)، وریدی همزمان', 'Reversal of neuromuscular blockade — 0.2 mg per 1 mg neostigmine (or 5 mg pyridostigmine), IV together'), {}, 'fixed', {'perDose': 0.2, 'dosesPerDay': 1}, [d], dur=ONE,
          notes=[note('عدد ماشین‌حساب به‌ازای هر ۱ mg نئوستیگمین است؛ برای دوز کل در mg نئوستیگمین ضرب شود. می‌تواند در یک سرنگ مخلوط شود.', 'The calculator figure is per 1 mg neostigmine; multiply by the neostigmine mg for the total. May be mixed in the same syringe.', [d])]),
      reg('pud', 'peptic-ulcer-disease', T('زخم پپتیک بزرگسال (کمکی، وقتی خوراکی ممکن نیست) — ۰٫۱ mg وریدی یا عضلانی هر ۴ ساعت، ۳ تا ۴ بار', 'Peptic ulcer, adults (adjunct when oral not tolerated) — 0.1 mg IV or IM every 4 h, 3–4 times daily'), A18, 'fixed', {'perDose': 0.1, 'perDoseMax': 0.2, 'dosesPerDay': 4}, [d],
          notes=[note('اثر قوی‌تر: ۰٫۲ mg. حداکثر ۴ بار در روز. برای زخم پپتیک در کودکان توصیه نمی‌شود.', 'Stronger effect: 0.2 mg. Max four times daily. Not recommended for peptic ulcer in children.', [d])])],
     [CI('ci', 'حساسیت؛ در درمان طولانی زخم پپتیک: گلوکوم، انسداد ادراری، انسداد گوارشی، ایلئوس فلجی، آتونی روده، وضعیت قلبی ناپایدار، کولیت اولسراتیو شدید، میاستنی گراو.', 'Hypersensitivity; for prolonged peptic-ulcer therapy: glaucoma, obstructive uropathy, GI obstruction, paralytic ileus, intestinal atony, unstable cardiovascular status, severe ulcerative colitis, myasthenia gravis.', [R(Gp, 'Contraindications')])],
     warn=[W('گلوکوم؛ بنزیل الکل (سمیت و کرن‌ایکتروس در نوزاد نارس).', 'Glaucoma; benzyl alcohol (toxicity and kernicterus in preterm neonates).', [R(Gp, 'Warnings')])],
     exs=[ex('premed', 'vial-0-2', {'perDose': 0.28, 'mlPerDose': 1.4}, ageYears=40, weightKg=70), ex('premed-inf', 'vial-0-2', {'perDose': 0.04, 'mlPerDose': 0.2, 'upperPerDose': 0.09}, ageMonths=10, weightKg=10),
          ex('rev', 'vial-0-2', {'perDose': 0.2, 'mlPerDose': 1}, ageYears=40, weightKg=70), ex('pud', 'vial-0-2', {'perDose': 0.1, 'mlPerDose': 0.5, 'upperPerDose': 0.2}, ageYears=40, weightKg=70)])
print('s12e2 ok')
