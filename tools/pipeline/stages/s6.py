"""Stage 6 — cardiovascular, endocrine, blood and renal."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's6_setids.json')))
sid = lambda k: S[k][0]

add_disease('hypertensive-emergency', 'اورژانس فشار خون (بیمارستانی)', 'Hypertensive emergency (hospital)', ['hypertensive crisis', 'بحران فشار خون', 'فشار خون بدخیم'], ['I16.1'], 'cardiology')
add_disease('intermittent-claudication', 'لنگش متناوب (بیماری شریان محیطی)', 'Intermittent claudication (peripheral artery disease)', ['claudication', 'PAD', 'لنگش', 'تنگی عروق پا'], ['I73.9'], 'cardiology')
add_disease('stroke-tia', 'سکته مغزی ایسکمیک خفیف یا TIA', 'Minor ischaemic stroke or TIA', ['TIA', 'stroke', 'سکته مغزی', 'حمله ایسکمیک گذرا'], ['I63.9', 'G45.9'], 'neurology')
add_disease('anemia-ckd', 'کم‌خونی بیماری مزمن کلیه', 'Anaemia of chronic kidney disease', ['CKD anemia', 'کم خونی کلیوی', 'اریتروپویتین'], ['D63.1'], 'nephrology')
add_disease('iron-overload', 'بار اضافی آهن (تالاسمی و تزریق خون مکرر)', 'Iron overload (thalassaemia and chronic transfusion)', ['iron overload', 'تالاسمی', 'شلاتور آهن', 'هموکروماتوز'], ['E83.111'], 'hematology')
add_disease('sickle-cell', 'کم‌خونی داسی‌شکل', 'Sickle cell anaemia', ['sickle cell', 'داسی شکل', 'SCD'], ['D57.1'], 'hematology')
add_disease('hyperphosphatemia', 'افزایش فسفات خون در دیالیز', 'Hyperphosphataemia in dialysis', ['hyperphosphatemia', 'فسفر بالا', 'باندر فسفات'], ['E83.39'], 'nephrology')
add_disease('hyperkalemia', 'افزایش پتاسیم خون', 'Hyperkalaemia', ['hyperkalemia', 'پتاسیم بالا', 'هایپرکالمی'], ['E87.5'], 'nephrology')
ONE = {'min': 1, 'max': 1}
inj = lambda id, label, amt, ml, src, sec, route='iv', unit='mg': liquid(id, amt, ml, label, [R(src, sec)], form_='injection', route=route, unit=unit)
PREG_RAS = lambda src, sec: W('هشدار جعبه‌ای: سمیت جنینی — با تشخیص بارداری فوراً قطع شود.', 'Boxed warning: fetal toxicity — stop as soon as pregnancy is detected.', [R(src, sec)])

# --- cardiovascular ---
En = fda('entresto', 'FDA Entresto', 'Entresto (sacubitril/valsartan) — Prescribing Information', sid('entresto'))
sv = lambda id, s, v: form(id, 'tablet', 'oral', f'Sacubitril {s} mg / valsartan {v} mg tablet', s + v, 'mg', [R(En, '3')], per='tablet',
                         components={'sacubitril': {'name': T('ساکوبیتریل', 'Sacubitril'), 'amount': s, 'unit': 'mg'}, 'valsartan': {'name': T('والسارتان', 'Valsartan'), 'amount': v, 'unit': 'mg'}})
drug('sacubitril-valsartan', 'cardiovascular', 'ساکوبیتریل + والسارتان', 'Sacubitril + valsartan', T('مهارکننده نپریلیزین و گیرنده آنژیوتانسین (ARNI)', 'Angiotensin receptor–neprilysin inhibitor (ARNI)'), [{'name': 'Entresto', 'market': 'US'}], ['entresto', 'انترستو', 'ساکوبیتریل', 'ARNI'],
     [sv('tab-24-26', 24, 26), sv('tab-49-51', 49, 51), sv('tab-97-103', 97, 103), liquid('susp-4', 4, 1, '4 mg/mL oral suspension (prepared from 49/51 mg tablets; combined)', [R(En, '2.4')])],
     [reg('adult', 'heart-failure', T('نارسایی قلب بزرگسال — شروع ۴۹/۵۱ mg دو بار در روز، هدف ۹۷/۱۰۳ mg', 'Adult heart failure — start 49/51 mg twice daily, target 97/103 mg'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 200, 'increment': 200, 'incrementEveryDays': 14, 'targetMin': 400, 'targetMax': 400, 'max': 400}}, [R(En, '2.2')],
          allowed=['tab-24-26', 'tab-49-51', 'tab-97-103'],
          notes=[note('اعداد بر حسب مجموع ساکوبیتریل + والسارتان (۴۹/۵۱ = ۱۰۰ mg). دوز پس از ۲ تا ۴ هفته دو برابر شود. از مهارکننده ACE دست‌کم ۳۶ ساعت فاصله.', 'Amounts are sacubitril + valsartan combined (49/51 = 100 mg). Double the dose after 2–4 weeks. At least 36 h apart from an ACE inhibitor.', [R(En, '2.2'), R(En, '2.1')])]),
      reg('child-lt40', 'heart-failure', T('کودک ۱ سال به بالا زیر ۴۰ kg — شروع ۱٫۶ mg/kg دو بار در روز (مجموع)', 'Child ≥1 y, <40 kg — start 1.6 mg/kg twice daily (combined)'), {'minAge': age(1, 'year'), 'maxWeightKg': 39.99}, 'weightBased', {'perKgPerDose': 1.6, 'intervalHours': 12}, [R(En, '2.3, Table 1')],
          allowed=['susp-4'], notes=[note('هر ۲ هفته به ۲٫۳ و سپس ۳٫۱ mg/kg دو بار در روز. سوسپانسیون یا پلت توصیه می‌شود.', 'Every 2 weeks increase to 2.3 then 3.1 mg/kg twice daily. Suspension or pellets recommended.', [R(En, '2.3, Table 1')])]),
      reg('child-40plus', 'heart-failure', T('کودک ۴۰ kg و بیشتر — شروع بر اساس وزن، دو بار در روز', 'Child ≥40 kg — starting dose by weight, twice daily'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 40}, 'weightBand',
          {'weightBands': [{'minWeightKg': 40, 'maxWeightKg': 49.99, 'perDose': 50, 'dosesPerDay': 2}, {'minWeightKg': 50, 'maxWeightKg': None, 'perDose': 100, 'dosesPerDay': 2}]}, [R(En, '2.3, Table 1')],
          allowed=['tab-24-26', 'tab-49-51', 'tab-97-103'],
          notes=[note('۴۰ تا ۵۰ kg: ۲۴/۲۶ → ۴۹/۵۱ → ۷۲/۷۸ mg؛ ۵۰ kg و بیشتر: ۴۹/۵۱ → ۷۲/۷۸ → ۹۷/۱۰۳ mg، هر ۲ هفته.', '40–50 kg: 24/26 → 49/51 → 72/78 mg; ≥50 kg: 49/51 → 72/78 → 97/103 mg, every 2 weeks.', [R(En, '2.3, Table 1')])])],
     [CI('ci', 'سابقه آنژیوادم با ACEi یا ARB؛ مصرف همزمان مهارکننده ACE (۳۶ ساعت فاصله)؛ آلیسکیرن در دیابت؛ حساسیت.', 'History of angioedema with ACEi or ARB; concomitant ACE inhibitor (36 h washout); aliskiren in diabetes; hypersensitivity.', [R(En, '4')])],
     warn=[PREG_RAS(En, 'Boxed Warning')],
     exs=[ex('adult', 'tab-49-51', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80), ex('child-lt40', 'susp-4', {'perDose': 32, 'mlPerDose': 8}, ageYears=6, weightKg=20), ex('child-40plus', 'tab-49-51', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=15, weightKg=55)])

Iv = fda('corlanor', 'FDA Corlanor', 'Corlanor (ivabradine) — Prescribing Information', sid('corlanor'))
drug('ivabradine', 'cardiovascular', 'ایوابرادین', 'Ivabradine', T('مهارکننده کانال If گره سینوسی', 'Sinus node If-channel inhibitor'), [{'name': 'Corlanor', 'market': 'US'}], ['corlanor', 'procoralan', 'کورلانور', 'ایوابرادین'],
     [tab('tab-5', 5, '5 mg tablet (scored)', [R(Iv, '3')], scored=True), tab('tab-7-5', 7.5, '7.5 mg tablet', [R(Iv, '3')]), liquid('sol-1', 5, 5, '5 mg/5 mL oral solution', [R(Iv, '3')], form_='solution')],
     [reg('adult', 'heart-failure', T('نارسایی قلب بزرگسال — شروع ۵ mg دو بار در روز با غذا', 'Adult heart failure — start 5 mg twice daily with food'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 2}, [R(Iv, '2.1')], limits={'maxPerDose': 7.5, 'refs': [R(Iv, '2.1')]},
          notes=[note('پس از ۲ هفته بر اساس ضربان استراحت (هدف ۵۰ تا ۶۰): بالای ۶۰ → ۲٫۵ mg بیشتر تا حداکثر ۷٫۵ mg دو بار؛ زیر ۵۰ یا برادی‌کاردی → ۲٫۵ mg کمتر. در اختلال هدایت از ۲٫۵ mg دو بار شروع.', 'After 2 weeks adjust to resting HR 50–60: >60 → +2.5 mg up to 7.5 mg twice daily; <50 or bradycardia → −2.5 mg. Start 2.5 mg twice daily with conduction defects.', [R(Iv, '2.1')])]),
      reg('child-lt40', 'heart-failure', T('کودک ۶ ماه به بالا زیر ۴۰ kg — شروع ۰٫۰۵ mg/kg دو بار در روز (محلول)', 'Child ≥6 months, <40 kg — start 0.05 mg/kg twice daily (solution)'), {'minAge': age(6, 'month'), 'maxWeightKg': 39.99}, 'weightBased', {'perKgPerDose': 0.05, 'intervalHours': 12}, [R(Iv, '2.2')], allowed=['sol-1'],
          notes=[note('هر ۲ هفته ۰٫۰۵ mg/kg افزایش تا کاهش ضربان دست‌کم ۲۰٪. حداکثر: ۶ ماه تا ۱ سال ۰٫۲ mg/kg، ۱ سال به بالا ۰٫۳ mg/kg دو بار در روز (تا ۷٫۵ mg).', 'Increase by 0.05 mg/kg every 2 weeks to a ≥20% HR reduction. Max: 6 months–1 y 0.2 mg/kg, ≥1 y 0.3 mg/kg twice daily (up to 7.5 mg).', [R(Iv, '2.2')])]),
      reg('child-40plus', 'heart-failure', T('کودک ۴۰ kg و بیشتر — شروع ۲٫۵ mg دو بار در روز', 'Child ≥40 kg — start 2.5 mg twice daily'), {'minAge': age(6, 'month'), 'maxAge': age(18, 'year'), 'minWeightKg': 40}, 'fixed', {'perDose': 2.5, 'dosesPerDay': 2}, [R(Iv, '2.2')], allowed=['tab-5'])],
     [CI('ci', 'نارسایی حاد جبران‌نشده قلب؛ افت فشار مهم؛ سندرم سینوس بیمار، بلوک SA یا AV درجه ۳ بدون پیس‌میکر؛ برادی‌کاردی مهم؛ نارسایی شدید کبد؛ وابستگی به پیس‌میکر؛ مهارکننده‌های قوی CYP3A4.',
         'Acute decompensated HF; significant hypotension; sick sinus, SA block or 3rd-degree AV block without pacemaker; significant bradycardia; severe hepatic impairment; pacemaker dependence; strong CYP3A4 inhibitors.', [R(Iv, '4')])],
     exs=[ex('adult', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=75), ex('child-lt40', 'sol-1', {'perDose': 1, 'mlPerDose': 1}, ageYears=6, weightKg=20), ex('child-40plus', 'tab-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 0.5}, ageYears=14, weightKg=45)])

Bu = fda('bumetanide', 'FDA Bumetanide', 'Bumetanide tablets (Northstar) — Prescribing Information', sid('bumetanide')); d = R(Bu, 'Dosage and Administration')
drug('bumetanide', 'cardiovascular', 'بومتانید', 'Bumetanide', T('دیورتیک لوپ', 'Loop diuretic'), [{'name': 'Bumex', 'market': 'US'}], ['bumex', 'burinex', 'بومتانید'],
     [tab(f'tab-{n}', m, f'{m} mg tablet', [R(Bu, 'How Supplied')]) for n, m in (('0-5', 0.5), ('1', 1), ('2', 2))],
     [reg('edema', 'edema', T('ادم — ۰٫۵ تا ۲ mg معمولاً یک بار در روز', 'Oedema — 0.5–2 mg usually once daily'), A18, 'fixed', {'perDose': 0.5, 'perDoseMax': 2, 'dosesPerDay': 1}, [d], limits={'maxPerDay': 10, 'refs': [d]},
          notes=[note('اگر پاسخ کافی نبود، دوز دوم یا سوم با فاصله ۴ تا ۵ ساعت تا حداکثر ۱۰ mg در روز. برای ادم مزمن مصرف یک روز در میان یا ۳ تا ۴ روز با ۱ تا ۲ روز استراحت ایمن‌تر است. حدوداً ۱ mg بومتانید ≈ ۴۰ mg فوروزماید.', 'If inadequate, a 2nd or 3rd dose at 4–5 h intervals up to 10 mg/day. For chronic oedema alternate-day or 3–4 days on, 1–2 days off is safest. About 1 mg bumetanide ≈ 40 mg furosemide.', [d])])],
     [CI('ci', 'آنوری؛ کمای کبدی؛ کمبود شدید الکترولیت تا اصلاح؛ حساسیت.', 'Anuria; hepatic coma; severe electrolyte depletion until corrected; hypersensitivity.', [R(Bu, 'Contraindications')])],
     exs=[ex('edema', 'tab-0-5', {'perDose': 0.5, 'upperPerDose': 2}, ageYears=60, weightKg=75)])

To = fda('torsemide', 'FDA Torsemide', 'Torsemide tablets (AvKARE) — Prescribing Information', sid('torsemide'))
drug('torsemide', 'cardiovascular', 'تورسماید', 'Torsemide', T('دیورتیک لوپ', 'Loop diuretic'), [{'name': 'Demadex', 'market': 'US'}], ['demadex', 'torasemide', 'تورسماید', 'تورازماید'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(To, '3')], scored=True) for m in (5, 10, 20, 100)],
     [reg('hf', 'edema', T('ادم نارسایی قلب — شروع ۱۰ یا ۲۰ mg یک بار در روز', 'Heart-failure oedema — start 10 or 20 mg once daily'), A18, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [R(To, '2.1')],
          notes=[note('در صورت پاسخ ناکافی تقریباً دو برابر شود؛ بالای ۲۰۰ mg بررسی نشده. نارسایی مزمن کلیه: شروع ۲۰ mg؛ سیروز: ۵ یا ۱۰ mg (بالای ۴۰ mg بررسی نشده).', 'If inadequate, roughly double; >200 mg not studied. CKD: start 20 mg; cirrhosis: 5 or 10 mg (>40 mg not studied).', [R(To, '2.1')])]),
      reg('htn', 'hypertension', T('فشار خون — ۵ mg یک بار در روز، در صورت نیاز ۱۰ mg', 'Hypertension — 5 mg once daily, 10 mg if needed'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(To, '2.2')], limits={'maxPerDose': 10, 'refs': [R(To, '2.2')]})],
     [CI('ci', 'حساسیت به تورسماید؛ آنوری؛ کمای کبدی.', 'Hypersensitivity to torsemide; anuria; hepatic coma.', [R(To, '4')])],
     exs=[ex('hf', 'tab-10', {'perDose': 10, 'upperPerDose': 20}, ageYears=65, weightKg=75), ex('htn', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=80)])

Ep = fda('eplerenone', 'FDA Eplerenone', 'Eplerenone tablets (Breckenridge) — Prescribing Information', sid('eplerenone'))
drug('eplerenone', 'cardiovascular', 'اپلرنون', 'Eplerenone', T('آنتاگونیست گیرنده مینرالوکورتیکوئید', 'Mineralocorticoid receptor antagonist'), [{'name': 'Inspra', 'market': 'US'}], ['inspra', 'اینسپرا', 'اپلرنون'],
     [tab('tab-25', 25, '25 mg tablet', [R(Ep, '3')]), tab('tab-50', 50, '50 mg tablet', [R(Ep, '3')])],
     [reg('hf', 'heart-failure', T('نارسایی قلب پس از MI — شروع ۲۵ mg یک بار در روز، تا ۵۰ mg ظرف ۴ هفته', 'HF after MI — start 25 mg once daily, up to 50 mg within 4 weeks'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 25, 'increment': 25, 'incrementEveryDays': 28, 'targetMin': 50, 'targetMax': 50, 'max': 50}}, [R(Ep, '2.1')],
          notes=[note('دوز بر اساس پتاسیم سرم طبق جدول ۱ برچسب تنظیم شود. پتاسیم پیش از شروع و به‌طور دوره‌ای.', 'Adjust by serum potassium per label Table 1. Check potassium before starting and periodically.', [R(Ep, '2.1'), R(Ep, '2.3')])]),
      reg('htn', 'hypertension', T('فشار خون — ۵۰ mg یک بار در روز (تا ۵۰ mg دو بار)', 'Hypertension — 50 mg once daily (up to 50 mg twice daily)'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Ep, '2.2')], limits={'maxPerDay': 100, 'refs': [R(Ep, '2.2')]})],
     [CI('all', 'همه بیماران: پتاسیم بالای ۵٫۵ هنگام شروع؛ CrCl ≤ ۳۰؛ مهارکننده قوی CYP3A.', 'All patients: K >5.5 at start; CrCl ≤30; strong CYP3A inhibitors.', [R(Ep, '4')]),
      CI('htn', 'فشار خون: دیابت نوع ۲ با میکروآلبومینوری؛ کراتینین بالای ۲ (مرد) یا ۱٫۸ (زن)؛ CrCl زیر ۵۰؛ مکمل پتاسیم یا دیورتیک نگهدارنده پتاسیم.', 'Hypertension: type 2 diabetes with microalbuminuria; creatinine >2.0 (men) or >1.8 (women); CrCl <50; potassium supplements or potassium-sparing diuretics.', [R(Ep, '4')])],
     exs=[ex('hf', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=80), ex('htn', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=80)])

Ol = fda('olmesartan', 'FDA Olmesartan', 'Olmesartan medoxomil tablets (Umedica) — Prescribing Information', sid('olmesartan'))
drug('olmesartan', 'cardiovascular', 'اولمسارتان', 'Olmesartan', T('مسدودکننده گیرنده آنژیوتانسین (ARB)', 'Angiotensin receptor blocker (ARB)'), [{'name': 'Benicar', 'market': 'US'}], ['benicar', 'olmetec', 'اولمسارتان', 'اولمتک'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Ol, '3')]) for m in (5, 20, 40)],
     [reg('adult', 'hypertension', T('فشار خون بزرگسال — ۲۰ mg یک بار در روز (تا ۴۰ mg)', 'Adult hypertension — 20 mg once daily (up to 40 mg)'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [R(Ol, '2.1')]),
      reg('child', 'hypertension', T('فشار خون کودک ۶ سال به بالا — بر اساس وزن', 'Pediatric hypertension ≥6 y — by weight'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 20}, 'weightBand',
          {'weightBands': [{'minWeightKg': 20, 'maxWeightKg': 34.99, 'perDose': 10, 'dosesPerDay': 1}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 20, 'dosesPerDay': 1}]}, [R(Ol, '2.2'), R(Ol, '2')],
          notes=[note('بازه: ۲۰ تا ۳۵ kg ← ۱۰ تا ۲۰ mg؛ ۳۵ kg و بیشتر ← ۲۰ تا ۴۰ mg. زیر ۱ سال توصیه نمی‌شود.', 'Range: 20–35 kg → 10–20 mg; ≥35 kg → 20–40 mg. Not recommended under 1 year.', [R(Ol, '2')])])],
     [CI('aliskiren', 'آلیسکیرن همزمان در دیابت.', 'Concomitant aliskiren in diabetes.', [R(Ol, '4')])],
     warn=[PREG_RAS(Ol, 'Boxed Warning')],
     exs=[ex('adult', 'tab-20', {'perDose': 20, 'upperPerDose': 40}, ageYears=50, weightKg=80), ex('child', 'tab-5', {'perDose': 10, 'tabletsPerDoseRounded': 2}, ageYears=8, weightKg=28)])

Nb = fda('nebivolol', 'FDA Nebivolol', 'Nebivolol tablets (Solco) — Prescribing Information', sid('nebivolol'))
drug('nebivolol', 'cardiovascular', 'نبیولول', 'Nebivolol', T('بتابلاکر انتخابی β1 با اثر گشادکنندگی عروق', 'β1-selective beta-blocker with vasodilating action'), [{'name': 'Bystolic', 'market': 'US'}], ['bystolic', 'nebilet', 'نبیولول', 'نبیلت'],
     [tab(f'tab-{n}', m, f'{m} mg tablet', [R(Nb, '3')]) for n, m in (('2-5', 2.5), ('5', 5), ('10', 10), ('20', 20))],
     [reg('htn', 'hypertension', T('فشار خون — شروع ۵ mg یک بار در روز (تا ۴۰ mg)', 'Hypertension — start 5 mg once daily (up to 40 mg)'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(Nb, '2.1')],
          notes=[note('هر ۲ هفته در صورت نیاز تا ۴۰ mg. CrCl زیر ۳۰: شروع ۲٫۵ mg.', 'Increase at 2-week intervals as needed up to 40 mg. CrCl <30: start 2.5 mg.', [R(Nb, '2.1')])])],
     [CI('ci', 'برادی‌کاردی شدید؛ بلوک بالاتر از درجه ۱؛ شوک کاردیوژنیک؛ نارسایی قلب جبران‌نشده؛ سندرم سینوس بیمار بدون پیس‌میکر؛ نارسایی شدید کبد؛ حساسیت.', 'Severe bradycardia; heart block above first degree; cardiogenic shock; decompensated HF; sick sinus without pacemaker; severe hepatic impairment; hypersensitivity.', [R(Nb, '4')])],
     exs=[ex('htn', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=80)])

Tc = fda('brilinta', 'FDA Brilinta', 'Brilinta (ticagrelor) tablets — Prescribing Information', sid('brilinta'))
drug('ticagrelor', 'blood', 'تیکاگرلور', 'Ticagrelor', T('مهارکننده P2Y12 (ضدپلاکت)', 'P2Y12 inhibitor (antiplatelet)'), [{'name': 'Brilinta', 'market': 'US'}], ['brilinta', 'brilique', 'بریلینتا', 'تیکاگرلور'],
     [tab('tab-60', 60, '60 mg tablet', [R(Tc, '3')]), tab('tab-90', 90, '90 mg tablet', [R(Tc, '3')])],
     [reg('acs-load', 'acute-coronary-syndrome', T('ACS — دوز بارگذاری ۱۸۰ mg', 'ACS — 180 mg loading dose'), A18, 'fixed', {'perDose': 180, 'dosesPerDay': 1}, [R(Tc, '2.2')], allowed=['tab-90'], dur=ONE),
      reg('acs', 'acute-coronary-syndrome', T('ACS یا سابقه MI — ۹۰ mg دو بار در روز (سال اول)، سپس ۶۰ mg دو بار', 'ACS or prior MI — 90 mg twice daily (first year), then 60 mg twice daily'), A18, 'fixed', {'perDose': 90, 'dosesPerDay': 2}, [R(Tc, '2.2')], allowed=['tab-90'],
          notes=[note('اولین دوز نگهدارنده ۶ تا ۱۲ ساعت پس از بارگذاری. همراه آسپرین ۷۵ تا ۱۰۰ mg روزانه؛ آسپرین بیشتر نه.', 'First maintenance dose 6–12 h after loading. With aspirin 75–100 mg daily; avoid higher aspirin doses.', [R(Tc, '2.2'), R(Tc, '2.1')])]),
      reg('cad', 'atherothrombotic-prevention', T('بیماری عروق کرونر بدون سکته یا MI قبلی — ۶۰ mg دو بار در روز', 'CAD without prior stroke or MI — 60 mg twice daily'), A18, 'fixed', {'perDose': 60, 'dosesPerDay': 2}, [R(Tc, '2.3')], allowed=['tab-60']),
      reg('stroke', 'stroke-tia', T('سکته ایسکمیک خفیف یا TIA — بارگذاری ۱۸۰ mg سپس ۹۰ mg دو بار تا ۳۰ روز', 'Minor ischaemic stroke or TIA — 180 mg load then 90 mg twice daily up to 30 days'), A18, 'fixed', {'perDose': 90, 'dosesPerDay': 2}, [R(Tc, '2.4')], allowed=['tab-90'], dur={'min': 30, 'max': 30},
          notes=[note('همراه آسپرین بارگذاری ۳۰۰ تا ۳۲۵ mg و سپس ۷۵ تا ۱۰۰ mg روزانه.', 'With an aspirin load of 300–325 mg then 75–100 mg daily.', [R(Tc, '2.4')])])],
     [CI('ci', 'سابقه خونریزی داخل جمجمه؛ خونریزی پاتولوژیک فعال؛ حساسیت.', 'History of intracranial haemorrhage; active pathological bleeding; hypersensitivity.', [R(Tc, '4')])],
     warn=[W('هشدار جعبه‌ای: خطر خونریزی جدی و گاهی کشنده؛ پیش از CABG فوری شروع نشود؛ قطع زودهنگام خطر حوادث قلبی را بالا می‌برد.', 'Boxed warning: significant, sometimes fatal bleeding; do not start before urgent CABG; premature discontinuation increases cardiovascular events.', [R(Tc, 'Boxed Warning')])],
     exs=[ex('acs-load', 'tab-90', {'perDose': 180, 'tabletsPerDoseRounded': 2}, ageYears=60, weightKg=80), ex('acs', 'tab-90', {'perDose': 90, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80),
          ex('cad', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80), ex('stroke', 'tab-90', {'perDose': 90, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80)])

Rn = fda('ranolazine', 'FDA Ranolazine ER', 'Ranolazine extended-release tablets (Zydus) — Prescribing Information', sid('ranolazine'))
drug('ranolazine', 'cardiovascular', 'رانولازین', 'Ranolazine', T('ضدآنژین', 'Antianginal'), [{'name': 'Ranexa', 'market': 'US'}], ['ranexa', 'رانکسا', 'رانولازین'],
     [tab('tab-500', 500, '500 mg extended-release tablet', [R(Rn, '3')]), tab('tab-1000', 1000, '1000 mg extended-release tablet', [R(Rn, '3')])],
     [reg('std', 'angina', T('آنژین مزمن — ۵۰۰ mg دو بار در روز، تا ۱۰۰۰ mg دو بار', 'Chronic angina — 500 mg twice daily, up to 1,000 mg twice daily'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 1000, 'dosesPerDay': 2}, [R(Rn, '2.1')],
          notes=[note('قرص کامل بلعیده شود (نشکند، نجود). با برخی داروها حداکثر دوز کمتر (بخش ۷).', 'Swallow whole (do not crush, break or chew). Lower maximum with some drugs (section 7).', [R(Rn, '2.1'), R(Rn, '2.2')])])],
     [CI('ci', 'مهارکننده‌های قوی CYP3A (کتوکونازول، کلاریترومایسین)؛ القاکننده‌های CYP3A (ریفامپین، فنوباربیتال، علف چای)؛ سیروز کبد.', 'Strong CYP3A inhibitors (ketoconazole, clarithromycin); CYP3A inducers (rifampin, phenobarbital, St John’s wort); liver cirrhosis.', [R(Rn, '4')])],
     exs=[ex('std', 'tab-500', {'perDose': 500, 'upperPerDose': 1000}, ageYears=65, weightKg=75)])

Ci = fda('cilostazol', 'FDA Cilostazol', 'Cilostazol tablets (Apotex) — Prescribing Information', sid('cilostazol'))
drug('cilostazol', 'blood', 'سیلوستازول', 'Cilostazol', T('مهارکننده فسفودی‌استراز III', 'Phosphodiesterase III inhibitor'), [{'name': 'Pletal', 'market': 'US'}], ['pletal', 'پلتال', 'سیلوستازول'],
     [tab('tab-50', 50, '50 mg tablet', [R(Ci, '3')]), tab('tab-100', 100, '100 mg tablet', [R(Ci, '3')])],
     [reg('std', 'intermittent-claudication', T('لنگش متناوب — ۱۰۰ mg دو بار در روز، ناشتا', 'Intermittent claudication — 100 mg twice daily, fasting'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [R(Ci, '2.1')],
          notes=[note('نیم ساعت پیش یا ۲ ساعت پس از صبحانه و شام. با مهارکننده‌های CYP3A4 یا CYP2C19 (کتوکونازول، اریترومایسین، دیلتیازم، امپرازول، فلوکونازول): ۵۰ mg دو بار. اگر پس از ۳ ماه بهتر نشد قطع.', '30 min before or 2 h after breakfast and dinner. With CYP3A4 or CYP2C19 inhibitors (ketoconazole, erythromycin, diltiazem, omeprazole, fluconazole): 50 mg twice daily. Stop if no improvement after 3 months.', [R(Ci, '2.1'), R(Ci, '2.2')])])],
     [CI('ci', 'نارسایی قلب با هر شدت؛ حساسیت.', 'Heart failure of any severity; hypersensitivity.', [R(Ci, '4')])],
     exs=[ex('std', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

Px = fda('pentoxifylline', 'FDA Pentoxifylline ER', 'Pentoxifylline extended-release tablets 400 mg — Prescribing Information', sid('pentoxifylline')); d = R(Px, 'Dosage and Administration')
drug('pentoxifylline', 'cardiovascular', 'پنتوکسی‌فیلین', 'Pentoxifylline', T('مشتق گزانتین (بهبود جریان خون)', 'Xanthine derivative (haemorheologic)'), [{'name': 'Trental', 'market': 'US'}], ['trental', 'ترنتال', 'پنتوکسی فیلین'],
     [tab('tab-400', 400, '400 mg extended-release tablet', [R(Px, 'How Supplied')])],
     [reg('std', 'intermittent-claudication', T('لنگش متناوب — ۴۰۰ mg سه بار در روز با غذا', 'Intermittent claudication — 400 mg three times daily with meals'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 3}, [d],
          notes=[note('دست‌کم ۸ هفته ادامه. با عوارض گوارشی یا عصبی: ۴۰۰ mg دو بار. CrCl زیر ۳۰: ۴۰۰ mg یک بار در روز.', 'Continue at least 8 weeks. With GI or CNS effects: 400 mg twice daily. CrCl <30: 400 mg once daily.', [d])])],
     [CI('ci', 'خونریزی اخیر مغزی یا شبکیه؛ عدم تحمل به پنتوکسی‌فیلین یا متیل‌گزانتین‌ها (کافئین، تئوفیلین).', 'Recent cerebral or retinal haemorrhage; intolerance to pentoxifylline or methylxanthines (caffeine, theophylline).', [R(Px, 'Contraindications')])],
     exs=[ex('std', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

Lb = fda('labetalol-inj', 'FDA Labetalol inj.', 'Labetalol hydrochloride injection 5 mg/mL (Hospira) — Prescribing Information', sid('labinj')); d = R(Lb, 'Dosage and Administration — Repeated Intravenous Injection')
patch('labetalol', add_forms=[inj('inj-5', '5 mg/mL injection (20 or 40 mL vial)', 5, 1, Lb, 'How Supplied')],
      add_regs=[reg('iv', 'hypertensive-emergency', T('فشار خون شدید — ۲۰ mg وریدی آهسته در ۲ دقیقه، سپس ۴۰ تا ۸۰ mg هر ۱۰ دقیقه', 'Severe hypertension — 20 mg slow IV over 2 min, then 40–80 mg every 10 min'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [d], allowed=['inj-5'],
                    notes=[note('بیمار خوابیده؛ فشار پیش از تزریق و ۵ و ۱۰ دقیقه بعد. تزریق‌های بعدی ۴۰ یا ۸۰ mg هر ۱۰ دقیقه تا فشار مطلوب یا مجموع ۳۰۰ mg. جایگزین: انفوزیون آهسته ۱ mg/mL.', 'Supine; BP before and 5 and 10 min after. Further 40 or 80 mg every 10 min until target BP or a total of 300 mg. Alternative: slow infusion of 1 mg/mL.', [d, R(Lb, 'Dosage and Administration — Slow Continuous Infusion')])])],
      add_exs=[ex('iv', 'inj-5', {'perDose': 20, 'mlPerDose': 4}, ageYears=50, weightKg=80)], pin_old=True)
p = find('labetalol'); dd = json.load(open(p))
if not any(c['id'] == 'inj-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('inj-ci', 'تزریقی: آسم، نارسایی آشکار قلب، بلوک بالاتر از درجه ۱، شوک کاردیوژنیک، برادی‌کاردی شدید، افت فشار شدید طولانی.', 'Injection: asthma, overt heart failure, heart block above first degree, cardiogenic shock, severe bradycardia, severe prolonged hypotension.', [R(Lb, 'Contraindications')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Hd = fda('hydralazine-inj', 'FDA Hydralazine inj.', 'Hydralazine hydrochloride injection 20 mg/mL (Zydus) — Prescribing Information', sid('hydinj')); d = R(Hd, 'Dosage and Administration')
patch('hydralazine', add_forms=[inj('inj-20', '20 mg/mL injection (1 mL vial)', 20, 1, Hd, 'How Supplied')],
      add_regs=[reg('iv', 'hypertensive-emergency', T('فشار خون شدید (وقتی خوراکی ممکن نیست) — ۲۰ تا ۴۰ mg وریدی یا عضلانی، تکرار در صورت نیاز', 'Severe hypertension (when oral not possible) — 20–40 mg IV or IM, repeat as needed'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [d], allowed=['inj-20'],
                    notes=[note('فشار مکرر کنترل شود؛ اثر حداکثر ۱۰ تا ۸۰ دقیقه. در آسیب کلیوی دوز کمتر. معمولاً ظرف ۲۴ تا ۴۸ ساعت به خوراکی.', 'Check BP frequently; maximal fall at 10–80 min. Lower dose with marked renal damage. Usually switch to oral within 24–48 h.', [d])]),
                reg('iv-preg', 'hypertension-pregnancy', T('فشار خون شدید بارداری (بیمارستانی) — ۲۰ تا ۴۰ mg وریدی یا عضلانی', 'Severe hypertension in pregnancy (hospital) — 20–40 mg IV or IM'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [d], allowed=['inj-20'],
                    notes=[note('دوز برچسب عمومی است؛ برچسب دوز جداگانه بارداری ندارد.', 'General label dose; the label has no separate pregnancy dose.', [d])])],
      add_exs=[ex('iv', 'inj-20', {'perDose': 20, 'upperPerDose': 40}, ageYears=50, weightKg=80), ex('iv-preg', 'inj-20', {'perDose': 20, 'upperPerDose': 40}, ageYears=28, weightKg=70)], pin_old=True)
p = find('hydralazine'); dd = json.load(open(p))
if not any(c['id'] == 'inj-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('inj-ci', 'تزریقی: حساسیت؛ بیماری عروق کرونر؛ بیماری روماتیسمی دریچه میترال.', 'Injection: hypersensitivity; coronary artery disease; rheumatic mitral valve disease.', [R(Hd, 'Contraindications')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

# --- endocrine ---
GLP_CI = lambda src: CI('mtc', 'سابقه شخصی یا خانوادگی کارسینوم مدولاری تیروئید یا MEN 2؛ حساسیت جدی.', 'Personal or family history of medullary thyroid carcinoma or MEN 2; serious hypersensitivity.', [R(src, '4')])
GLP_W = lambda src: W('هشدار جعبه‌ای: تومور سلول C تیروئید در جوندگان؛ در سابقه MTC یا MEN 2 ممنوع.', 'Boxed warning: thyroid C-cell tumours in rodents; contraindicated with MTC or MEN 2 history.', [R(src, 'Boxed Warning')])
Oz = fda('ozempic', 'FDA Ozempic', 'Ozempic (semaglutide) injection — Prescribing Information', sid('ozempic'))
drug('semaglutide', 'alimentary-metabolism', 'سماگلوتاید (تزریقی هفتگی)', 'Semaglutide (weekly injection)', T('آگونیست گیرنده GLP-1', 'GLP-1 receptor agonist'), [{'name': 'Ozempic', 'market': 'US'}], ['ozempic', 'اوزمپیک', 'سماگلوتاید'],
     [unitform('pen', 'injection', 'sc', 'Pen 0.25/0.5 mg, 1 mg or 2 mg per dose (0.68, 1.34 or 2.68 mg/mL)', [R(Oz, '3')], unit='mg', per='application')],
     [reg('t2d', 'type-2-diabetes', T('دیابت نوع ۲ — هفته‌ای یک بار: ۰٫۲۵ mg × ۴ هفته، سپس ۰٫۵ mg', 'Type 2 diabetes — once weekly: 0.25 mg × 4 weeks, then 0.5 mg'), A18, 'notCalculated',
          {'reason': T('هفته‌ای یک بار زیرجلدی (نه روزانه). ۴ هفته ۰٫۲۵ mg (فقط برای تحمل)، سپس ۰٫۵ mg. در صورت نیاز پس از دست‌کم ۴ هفته ۱ mg و سپس ۲ mg؛ حداکثر ۲ mg در هفته.', 'Once WEEKLY subcutaneous (not daily). 0.25 mg for 4 weeks (tolerability only), then 0.5 mg. If needed after at least 4 weeks go to 1 mg, then 2 mg; max 2 mg weekly.')}, [R(Oz, '2.2'), R(Oz, '2.1')])],
     [GLP_CI(Oz)], warn=[GLP_W(Oz)])

Vc = fda('victoza', 'FDA Victoza', 'Victoza (liraglutide) injection — Prescribing Information', sid('victoza'))
drug('liraglutide', 'alimentary-metabolism', 'لیراگلوتاید', 'Liraglutide', T('آگونیست گیرنده GLP-1', 'GLP-1 receptor agonist'), [{'name': 'Victoza', 'market': 'US'}], ['victoza', 'ویکتوزا', 'لیراگلوتاید'],
     [liquid('pen-6', 6, 1, '6 mg/mL pen (18 mg/3 mL; doses 0.6, 1.2, 1.8 mg)', [R(Vc, '3')], form_='injection', route='sc')],
     [reg('t2d', 'type-2-diabetes', T('دیابت نوع ۲ (۱۰ سال به بالا) — ۰٫۶ mg روزانه، سپس ۱٫۲ و تا ۱٫۸ mg', 'Type 2 diabetes (≥10 y) — 0.6 mg daily, then 1.2 up to 1.8 mg'), {'minAge': age(10, 'year')}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 0.6, 'increment': 0.6, 'incrementEveryDays': 7, 'targetMin': 1.2, 'targetMax': 1.8, 'max': 1.8}}, [R(Vc, '2.1')],
          notes=[note('۰٫۶ mg فقط برای تحمل گوارشی است. اگر بیش از ۳ روز قطع شد، از ۰٫۶ mg دوباره شروع.', '0.6 mg is only for GI tolerability. If more than 3 days missed, restart at 0.6 mg.', [R(Vc, '2.1'), R(Vc, '2.2')])])],
     [GLP_CI(Vc)], warn=[GLP_W(Vc)], exs=[ex('t2d', 'pen-6', {'perDose': 0.6, 'mlPerDose': 0.1}, ageYears=50, weightKg=90)])

Mj = fda('mounjaro', 'FDA Mounjaro', 'Mounjaro (tirzepatide) injection — Prescribing Information', sid('mounjaro'))
drug('tirzepatide', 'alimentary-metabolism', 'تیرزپاتاید (تزریقی هفتگی)', 'Tirzepatide (weekly injection)', T('آگونیست دوگانه GIP و GLP-1', 'Dual GIP/GLP-1 receptor agonist'), [{'name': 'Mounjaro', 'market': 'US'}], ['mounjaro', 'مونجارو', 'تیرزپاتاید'],
     [unitform('pen', 'injection', 'sc', 'Pen or vial 2.5–15 mg per dose', [R(Mj, '3')], unit='mg', per='application')],
     [reg('t2d', 'type-2-diabetes', T('دیابت نوع ۲ — هفته‌ای یک بار: شروع ۲٫۵ mg', 'Type 2 diabetes — once weekly: start 2.5 mg'), {}, 'notCalculated',
          {'reason': T('هفته‌ای یک بار زیرجلدی (نه روزانه). شروع ۲٫۵ mg؛ در صورت نیاز هر دست‌کم ۴ هفته ۲٫۵ mg افزایش. حداکثر: بزرگسال ۱۵ mg و کودک ۱۰ mg در هفته.', 'Once WEEKLY subcutaneous (not daily). Start 2.5 mg; increase by 2.5 mg after at least 4 weeks as needed. Max: adults 15 mg, children 10 mg weekly.')}, [R(Mj, '2.1')])],
     [GLP_CI(Mj)], warn=[GLP_W(Mj)])

Gv = uk('uk-galvus', 'UK Galvus SmPC', 'Galvus 50 mg tablets (vildagliptin) — SmPC', 'Novartis Pharmaceuticals UK Ltd', '22 June 2023', 6225)
drug('vildagliptin', 'alimentary-metabolism', 'ویلداگلیپتین', 'Vildagliptin', T('مهارکننده DPP-4', 'DPP-4 inhibitor'), [{'name': 'Galvus', 'market': 'UK'}], ['galvus', 'گالووس', 'ویلداگلیپتین'],
     [tab('tab-50', 50, '50 mg tablet', [R(Gv, '4.2')], markets=('UK',))],
     [reg('std', 'type-2-diabetes', T('دیابت نوع ۲ — ۵۰ mg دو بار در روز (با سولفونیل‌اوره: ۵۰ mg صبح)', 'Type 2 diabetes — 50 mg twice daily (with a sulphonylurea: 50 mg in the morning)'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 2}, [R(Gv, '4.2')],
          notes=[note('بیش از ۱۰۰ mg در روز توصیه نمی‌شود. در ترکیب دوگانه با سولفونیل‌اوره ۵۰ mg یک بار صبح کافی است.', 'Doses above 100 mg/day not recommended. In dual combination with a sulphonylurea, 50 mg once in the morning.', [R(Gv, '4.2')])])],
     [CI('hyper', 'حساسیت به ویلداگلیپتین.', 'Hypersensitivity to vildagliptin.', [R(Gv, '4.3')])],
     warn=[W('در نارسایی کبد یا ALT/AST بیش از ۳ برابر مصرف نشود؛ پایش آنزیم‌های کبد.', 'Not for hepatic impairment or ALT/AST >3× ULN; monitor liver enzymes.', [R(Gv, '4.4')])],
     exs=[ex('std', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=80)])

Rp = fda('repaglinide', 'FDA Repaglinide', 'Repaglinide tablets (Northstar) — Prescribing Information', sid('repaglinide')); d = R(Rp, '2.1')
drug('repaglinide', 'alimentary-metabolism', 'رپاگلینید', 'Repaglinide', T('گلینید (محرک ترشح انسولین)', 'Glinide (insulin secretagogue)'), [{'name': 'Prandin', 'market': 'US'}], ['prandin', 'novonorm', 'رپاگلینید'],
     [tab(f'tab-{n}', m, f'{m} mg tablet', [R(Rp, 'How Supplied')]) for n, m in (('0-5', 0.5), ('1', 1), ('2', 2))],
     [reg('std', 'type-2-diabetes', T('دیابت نوع ۲ — ۰٫۵ mg پیش از هر وعده (HbA1c ≥ ۸٪: ۱ تا ۲ mg)', 'Type 2 diabetes — 0.5 mg before each meal (HbA1c ≥8%: 1–2 mg)'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 3}, [d],
          limits={'maxPerDose': 4, 'maxPerDay': 16, 'refs': [d]},
          notes=[note('ظرف ۳۰ دقیقه پیش از غذا؛ اگر وعده حذف شد دوز هم حذف. هر هفته تا ۴ mg با هر وعده دو برابر شود. با سیکلوسپورین حداکثر ۶ mg در روز.', 'Within 30 min before meals; skip the dose if the meal is skipped. Double weekly up to 4 mg with each meal. With cyclosporine max 6 mg/day.', [d, R(Rp, '7')])])],
     [CI('ci', 'مصرف همزمان جم‌فیبروزیل؛ حساسیت.', 'Concomitant gemfibrozil; hypersensitivity.', [R(Rp, '4')])],
     exs=[ex('std', 'tab-0-5', {'perDose': 0.5, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80)])

# --- blood ---
Vf = fda('venofer', 'FDA Venofer', 'Venofer (iron sucrose) injection — Prescribing Information', sid('venofer'))
IRON = note('دوز بر حسب آهن المنتال. فقط وریدی (تزریق آهسته یا انفوزیون).', 'Dose is elemental iron. IV only (slow injection or infusion).', [R(Vf, '2.1')])
drug('iron-sucrose', 'blood', 'آهن سوکروز (ونوفر)', 'Iron sucrose (Venofer)', T('آهن تزریقی', 'Parenteral iron'), [{'name': 'Venofer', 'market': 'US'}], ['venofer', 'ونوفر', 'آهن وریدی', 'آیرون سوکروز'],
     [inj('vial-20', '20 mg iron/mL (50, 100 or 200 mg vial)', 20, 1, Vf, '3')],
     [reg('hdd', 'anemia-ckd', T('کم‌خونی فقر آهن در همودیالیز — ۱۰۰ mg در هر جلسه دیالیز (مجموع ۱۰۰۰ mg)', 'Iron deficiency on haemodialysis — 100 mg per dialysis session (course 1,000 mg)'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Vf, '2.2')],
          notes=[note('تزریق بدون رقیق‌سازی در ۲ تا ۵ دقیقه یا انفوزیون در ۱۰۰ mL سالین در ۱۵ دقیقه، اوایل دیالیز.', 'Undiluted over 2–5 min or infusion in 100 mL saline over 15 min, early in dialysis.', [R(Vf, '2.2')]), IRON]),
      reg('ndd', 'anemia-ckd', T('بیماری مزمن کلیه بدون دیالیز — ۲۰۰ mg در ۵ نوبت طی ۱۴ روز', 'Non-dialysis CKD — 200 mg on 5 occasions within 14 days'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Vf, '2.3')], notes=[IRON]),
      reg('child', 'anemia-ckd', T('کودک ۲ سال به بالا در دیالیز (نگهدارنده) — ۰٫۵ mg/kg هر ۲ هفته', 'Child ≥2 y on dialysis (maintenance) — 0.5 mg/kg every 2 weeks'), {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 0.5, 'dividedDoses': 1}, [R(Vf, '2.5')],
          limits={'maxPerDose': 100, 'refs': [R(Vf, '2.5')]}, notes=[note('هر ۲ هفته به مدت ۱۲ هفته (نه روزانه). درمان جایگزینی در کودک ثابت نشده.', 'Every 2 weeks for 12 weeks (not daily). Replacement dosing in children not established.', [R(Vf, '2.5')]), IRON])],
     [CI('hyper', 'حساسیت به ونوفر.', 'Hypersensitivity to Venofer.', [R(Vf, '4')])],
     exs=[ex('hdd', 'vial-20', {'perDose': 100, 'mlPerDose': 5}, ageYears=60, weightKg=70), ex('ndd', 'vial-20', {'perDose': 200, 'mlPerDose': 10}, ageYears=60, weightKg=70), ex('child', 'vial-20', {'perDose': 15, 'mlPerDose': 0.75}, ageYears=10, weightKg=30)])

Fc = fda('injectafer', 'FDA Injectafer', 'Injectafer (ferric carboxymaltose) injection — Prescribing Information', sid('injectafer')); d = R(Fc, '2.2')
drug('ferric-carboxymaltose', 'blood', 'فریک کربوکسی‌مالتوز', 'Ferric carboxymaltose', T('آهن تزریقی', 'Parenteral iron'), [{'name': 'Injectafer', 'market': 'US'}], ['injectafer', 'ferinject', 'فرینجکت', 'آهن وریدی'],
     [inj('vial-50', '50 mg iron/mL (100, 500, 750, 1000 mg vials)', 50, 1, Fc, '3')],
     [reg('ge50', 'iron-deficiency-anemia', T('کم‌خونی فقر آهن — ۵۰ kg و بیشتر: ۷۵۰ mg وریدی، دو دوز با فاصله ۷ روز', 'Iron deficiency anaemia — ≥50 kg: 750 mg IV, two doses ≥7 days apart'), {'minAge': age(1, 'year'), 'minWeightKg': 50}, 'fixed', {'perDose': 750, 'dosesPerDay': 1}, [d], dur=ONE,
          notes=[note('مجموع ۱۵۰۰ mg در هر دوره. بزرگسال: جایگزین یک دوز ۱۵ mg/kg تا ۱۰۰۰ mg. برای بیمار با عدم تحمل یا پاسخ ناکافی به آهن خوراکی.', 'Total 1,500 mg per course. Adults: alternatively a single 15 mg/kg dose up to 1,000 mg. For intolerance or poor response to oral iron.', [d, R(Fc, '1')])]),
      reg('lt50', 'iron-deficiency-anemia', T('کم‌خونی فقر آهن — زیر ۵۰ kg (۱ سال به بالا): ۱۵ mg/kg وریدی، دو دوز با فاصله ۷ روز', 'Iron deficiency anaemia — <50 kg (≥1 y): 15 mg/kg IV, two doses ≥7 days apart'), {'minAge': age(1, 'year'), 'maxWeightKg': 49.99}, 'weightBased', {'perKgPerDay': 15, 'dividedDoses': 1}, [d], dur=ONE)],
     [CI('hyper', 'حساسیت به Injectafer.', 'Hypersensitivity to Injectafer.', [R(Fc, '4')])],
     warn=[W('هشدار جعبه‌ای: هیپوفسفاتمی شدید و طولانی (استئومالاسی، شکستگی)؛ فسفات پیش از دوره تکراری چک و هیپوفسفاتمی قبلی اصلاح شود.', 'Boxed warning: severe prolonged hypophosphataemia (osteomalacia, fractures); check phosphate before a repeat course and correct prior hypophosphataemia.', [R(Fc, 'Boxed Warning'), R(Fc, '2.1')])],
     exs=[ex('ge50', 'vial-50', {'perDose': 750, 'mlPerDose': 15}, ageYears=35, weightKg=60), ex('lt50', 'vial-50', {'perDose': 300, 'mlPerDose': 6}, ageYears=6, weightKg=20)])

Eg = fda('epogen', 'FDA Epogen', 'Epogen (epoetin alfa) — Prescribing Information', sid('epogen')); d = R(Eg, '2.2')
TIW = note('سه بار در هفته (نه روزانه)، وریدی یا زیرجلدی (در همودیالیز وریدی). کمترین دوزی که نیاز به تزریق خون را کم کند؛ هموگلوبین بالای ۱۱ هدف نشود. هموگلوبین هفتگی تا پایدار شدن.', 'Three times WEEKLY (not daily), IV or SC (IV on haemodialysis). Lowest dose that reduces transfusion need; do not target Hb above 11. Weekly Hb until stable.', [d])
EPOIR = note('سرنگ‌های ایرانی (دارویاب) مثل ۲۰۰۰، ۴۰۰۰ یا ۱۰۰۰۰ واحد در ۰٫۵ mL هستند، نه در ۱ mL؛ حجم را از واحد و غلظت همان سرنگ حساب کنید.', 'Iranian syringes (Darooyab) such as 2,000, 4,000 or 10,000 units are in 0.5 mL, not 1 mL; compute the volume from the units and that syringe’s strength.', [R('darooyab-generic', 'G-1393/Recombinant-Erythropoietin')])
drug('epoetin-alfa', 'blood', 'اپوئتین آلفا (اریتروپویتین)', 'Epoetin alfa (erythropoietin)', T('محرک اریتروپویز (ESA)', 'Erythropoiesis-stimulating agent'), [{'name': 'Epogen', 'market': 'US'}], ['epogen', 'eprex', 'اپرکس', 'اریتروپویتین', 'EPO'],
     [inj('vial-4000', '4,000 units/mL single-dose vial', 4000, 1, Eg, 'Description', route='sc', unit='unit'), inj('vial-10000', '10,000 units/mL single-dose vial', 10000, 1, Eg, 'Description', route='sc', unit='unit')],
     [reg('adult', 'anemia-ckd', T('کم‌خونی بیماری مزمن کلیه — بزرگسال: ۵۰ تا ۱۰۰ واحد/kg سه بار در هفته', 'Anaemia of CKD — adult: 50–100 units/kg three times weekly'), A18, 'weightBased', {'perKgPerDay': 50, 'perKgPerDayMax': 100, 'dividedDoses': 1}, [d], unit='unit', notes=[TIW, EPOIR]),
      reg('child', 'anemia-ckd', T('کم‌خونی بیماری مزمن کلیه — کودک ۱ ماه به بالا: ۵۰ واحد/kg سه بار در هفته', 'Anaemia of CKD — child ≥1 month: 50 units/kg three times weekly'), {'minAge': age(1, 'month'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 50, 'dividedDoses': 1}, [d], unit='unit',
          notes=[TIW, note('ویال چنددوزی (بنزیل الکل) در نوزاد و شیرخوار ممنوع است؛ ویال تک‌دوز مصرف شود.', 'Multiple-dose vials (benzyl alcohol) are contraindicated in neonates and infants; use single-dose vials.', [R(Eg, '4')]), EPOIR])],
     [CI('ci', 'فشار خون کنترل‌نشده؛ آپلازی خالص گلبول قرمز پس از اریتروپویتین؛ حساسیت جدی؛ ویال چنددوزی (بنزیل الکل) در نوزاد، شیرخوار، بارداری و شیردهی.', 'Uncontrolled hypertension; pure red cell aplasia after an erythropoietin; serious allergy; multiple-dose vials (benzyl alcohol) in neonates, infants, pregnancy and lactation.', [R(Eg, '4')])],
     warn=[W('هشدار جعبه‌ای: ESA خطر مرگ، MI، سکته، ترومبوز و پیشرفت تومور را افزایش می‌دهد؛ هموگلوبین بالای ۱۱ هدف نشود.', 'Boxed warning: ESAs increase the risk of death, MI, stroke, thrombosis and tumour progression; do not target Hb above 11 g/dL.', [R(Eg, 'Boxed Warning')])],
     exs=[ex('adult', 'vial-10000', {'perDose': 3500, 'upperPerDose': 7000}, ageYears=60, weightKg=70), ex('child', 'vial-4000', {'perDose': 1000, 'mlPerDose': 0.25}, ageYears=6, weightKg=20)])

Jd = fda('jadenu', 'FDA Jadenu', 'Jadenu (deferasirox) tablets and granules — Prescribing Information', sid('jadenu'))
drug('deferasirox', 'various', 'دفراسیروکس', 'Deferasirox', T('شلاتور خوراکی آهن', 'Oral iron chelator'), [{'name': 'Jadenu', 'market': 'US'}], ['jadenu', 'exjade', 'جادنو', 'اکسجید', 'دفراسیروکس', 'اسوسیرال'],
     [tab(f'tab-{m}', m, f'{m} mg film-coated tablet (Jadenu)', [R(Jd, '3')]) for m in (90, 180, 360)],
     [reg('transfusional', 'iron-overload', T('بار آهن ناشی از تزریق خون — ۲ سال به بالا: شروع ۱۴ mg/kg یک بار در روز', 'Transfusional iron overload — ≥2 y: start 14 mg/kg once daily'), {'minAge': age(2, 'year')}, 'weightBased', {'perKgPerDay': 14, 'dividedDoses': 1}, [R(Jd, '2.1')],
          notes=[note('فقط با تزریق دست‌کم ۱۰۰ mL/kg گلبول قرمز و فریتین پایدار بالای ۱۰۰۰. ناشتا یا با غذای سبک؛ نه با آنتی‌اسید آلومینیومی. دوز به نزدیک‌ترین قرص کامل. فریتین ماهانه؛ هر ۳ تا ۶ ماه تنظیم. eGFR ۴۰ تا ۶۰: کاهش دوز.', 'Only after ≥100 mL/kg packed RBC and ferritin consistently >1,000. Empty stomach or light meal; not with aluminium antacids. Round to the nearest whole tablet. Monthly ferritin; adjust every 3–6 months. eGFR 40–60: reduce dose.', [R(Jd, '2.1'), R(Jd, '2.3')])]),
      reg('ntdt', 'iron-overload', T('تالاسمی وابسته‌نبودن به تزریق (NTDT) — شروع ۷ mg/kg یک بار در روز', 'Non-transfusion-dependent thalassaemia — start 7 mg/kg once daily'), {'minAge': age(10, 'year')}, 'weightBased', {'perKgPerDay': 7, 'dividedDoses': 1}, [R(Jd, '2.2')],
          notes=[note('فقط با LIC دست‌کم ۵ mg Fe/g و فریتین بالای ۳۰۰. اگر LIC بالای ۱۵، پس از ۴ هفته تا ۱۴ mg/kg.', 'Only with LIC ≥5 mg Fe/g dw and ferritin >300. If LIC >15, consider 14 mg/kg after 4 weeks.', [R(Jd, '2.2')])])],
     [CI('ci', 'eGFR زیر ۴۰؛ وضعیت عمومی ضعیف؛ MDS پرخطر؛ بدخیمی پیشرفته؛ پلاکت زیر ۵۰ هزار؛ حساسیت.', 'eGFR <40; poor performance status; high-risk MDS; advanced malignancy; platelets <50 × 10⁹/L; hypersensitivity.', [R(Jd, '4')])],
     warn=[W('هشدار جعبه‌ای: نارسایی کلیه، نارسایی کبد و خونریزی گوارشی (گاهی کشنده)؛ کراتینین دوبار پیش از شروع و ماهانه.', 'Boxed warning: renal failure, hepatic failure and GI haemorrhage (sometimes fatal); duplicate creatinine before starting, then monthly.', [R(Jd, 'Boxed Warning')])],
     exs=[ex('transfusional', 'tab-90', {'perDose': 280}, ageYears=8, weightKg=20), ex('ntdt', 'tab-90', {'perDose': 280}, ageYears=20, weightKg=40)])

Sk = fda('siklos', 'FDA Siklos', 'Siklos (hydroxyurea) tablets — Prescribing Information', sid('siklos')); d = R(Sk, '2.1, Table 1')
drug('hydroxyurea', 'antineoplastic-immunomodulating', 'هیدروکسی‌اوره', 'Hydroxyurea', T('آنتی‌متابولیت', 'Antimetabolite'), [{'name': 'Siklos', 'market': 'US'}], ['siklos', 'hydrea', 'هیدروکسی اوره', 'هیدرآ'],
     [tab('tab-100', 100, '100 mg tablet (scored)', [R(Sk, '3')], scored=True)],
     [reg('adult', 'sickle-cell', T('کم‌خونی داسی‌شکل — بزرگسال: شروع ۱۵ mg/kg یک بار در روز', 'Sickle cell anaemia — adult: start 15 mg/kg once daily'), A18, 'weightBased', {'perKgPerDay': 15, 'dividedDoses': 1}, [d],
          limits={'maxPerKgPerDay': 35, 'refs': [d]}, notes=[note('بر اساس وزن واقعی یا ایده‌آل (هر کدام کمتر). شمارش خون هر ۲ هفته؛ هر ۸ هفته ۵ mg/kg افزایش تا حداکثر ۳۵ mg/kg. CrCl زیر ۶۰: نصف دوز.', 'Use actual or ideal weight, whichever is less. Blood count every 2 weeks; increase 5 mg/kg every 8 weeks up to 35 mg/kg. CrCl <60: half dose.', [d, R(Sk, '2.2')])]),
      reg('child', 'sickle-cell', T('کم‌خونی داسی‌شکل — کودک ۲ سال به بالا: شروع ۲۰ mg/kg یک بار در روز', 'Sickle cell anaemia — child ≥2 y: start 20 mg/kg once daily'), {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 20, 'dividedDoses': 1}, [d],
          limits={'maxPerKgPerDay': 35, 'refs': [d]}, notes=[note('شمارش خون هر ۲ هفته؛ هر ۸ هفته ۵ mg/kg افزایش تا حداکثر ۳۵ mg/kg. CrCl زیر ۶۰: ۱۰ mg/kg.', 'Blood count every 2 weeks; increase 5 mg/kg every 8 weeks up to 35 mg/kg. CrCl <60: 10 mg/kg.', [d, R(Sk, '2.2')])])],
     [CI('hyper', 'حساسیت به هیدروکسی‌اوره.', 'Hypersensitivity to hydroxyurea.', [R(Sk, '4')])],
     warn=[W('هشدار جعبه‌ای: سرکوب مغز استخوان و بدخیمی؛ شمارش خون مکرر و محافظت از آفتاب.', 'Boxed warning: myelosuppression and malignancies; frequent blood counts and sun protection.', [R(Sk, 'Boxed Warning')])],
     exs=[ex('adult', 'tab-100', {'perDose': 1050}, ageYears=30, weightKg=70), ex('child', 'tab-100', {'perDose': 400, 'tabletsPerDoseRounded': 4}, ageYears=6, weightKg=20)])

# --- renal ---
Rv = fda('renvela', 'FDA Renvela', 'Renvela (sevelamer carbonate) — Prescribing Information', sid('renvela')); d = R(Rv, '2.1, Table 1')
drug('sevelamer', 'various', 'سولامر', 'Sevelamer carbonate', T('باندر فسفات', 'Phosphate binder'), [{'name': 'Renvela', 'market': 'US'}], ['renvela', 'renagel', 'رنولا', 'سولامر'],
     [tab('tab-800', 800, '800 mg tablet', [R(Rv, '3')])],
     [reg('std', 'hyperphosphatemia', T('فسفات بالا در دیالیز — ۰٫۸ تا ۱٫۶ g سه بار در روز با غذا', 'Hyperphosphataemia on dialysis — 0.8–1.6 g three times daily with meals'), A18, 'fixed', {'perDose': 800, 'perDoseMax': 1600, 'dosesPerDay': 3}, [d],
          notes=[note('فسفر ۵٫۵ تا ۷٫۵: ۰٫۸ g؛ ۷٫۵ و بیشتر: ۱٫۶ g سه بار با غذا. هر ۲ هفته ۰٫۸ g در هر وعده افزایش تا رسیدن به هدف.', 'Phosphorus >5.5–<7.5: 0.8 g; ≥7.5: 1.6 g three times daily with meals. Titrate by 0.8 g per meal every 2 weeks to target.', [d])])],
     [CI('ci', 'انسداد روده؛ حساسیت به سولامر.', 'Bowel obstruction; hypersensitivity to sevelamer.', [R(Rv, '4')])],
     exs=[ex('std', 'tab-800', {'perDose': 800, 'upperPerDose': 1600}, ageYears=55, weightKg=70)])

Ca = fda('calcium-acetate', 'FDA Calcium acetate', 'Calcium acetate capsules 667 mg (Rising) — Prescribing Information', sid('caacetate'))
drug('calcium-acetate', 'various', 'کلسیم استات', 'Calcium acetate', T('باندر فسفات کلسیمی', 'Calcium-based phosphate binder'), [{'name': 'PhosLo', 'market': 'US'}], ['phoslo', 'کلسیم استات'],
     [tab('cap-667', 667, '667 mg capsule', [R(Ca, '3')], per='capsule', form_='capsule')],
     [reg('std', 'hyperphosphatemia', T('فسفات بالا در دیالیز — شروع ۲ کپسول با هر وعده', 'Hyperphosphataemia on dialysis — start 2 capsules with each meal'), A18, 'fixed', {'perDose': 1334, 'dosesPerDay': 3}, [R(Ca, '2')],
          notes=[note('به‌تدریج تا رسیدن فسفر به هدف بدون هیپرکلسمی؛ بیشتر بیماران ۳ تا ۴ کپسول با هر وعده.', 'Increase gradually to target phosphorus without hypercalcaemia; most need 3–4 capsules per meal.', [R(Ca, '2')])])],
     [CI('ci', 'هیپرکلسمی.', 'Hypercalcaemia.', [R(Ca, '4')])],
     exs=[ex('std', 'cap-667', {'perDose': 1334, 'tabletsPerDoseRounded': 2}, ageYears=55, weightKg=70)])

Sp = fda('sps', 'FDA SPS suspension', 'Sodium polystyrene sulfonate suspension 15 g/60 mL (Burel) — Prescribing Information', sid('sps')); d = R(Sp, 'Dosage and Administration')
drug('sodium-polystyrene-sulfonate', 'various', 'سدیم پلی‌استایرن سولفونات (کی‌اگزالات)', 'Sodium polystyrene sulfonate', T('رزین تبادل کاتیون', 'Cation-exchange resin'), [{'name': 'Kayexalate', 'market': 'US'}], ['kayexalate', 'SPS', 'کی اگزالات', 'رزین پتاسیم'],
     [liquid('susp-15-60', 15, 60, '15 g / 60 mL oral suspension', [R(Sp, 'How Supplied')], unit='g')],
     [reg('std', 'hyperkalemia', T('هیپرکالمی — بزرگسال: ۱۵ g (۶۰ mL) یک تا چهار بار در روز', 'Hyperkalaemia — adult: 15 g (60 mL) one to four times daily'), A18, 'fixed', {'perDose': 15, 'dosesPerDay': 1}, [d], unit='g', limits={'maxPerDay': 60, 'refs': [d]},
          notes=[note('میانگین روزانه ۱۵ تا ۶۰ g. دست‌کم ۳ ساعت فاصله با سایر داروهای خوراکی (گاستروپارزی ۶ ساعت). بیمار نشسته. هر ۶۰ mL حاوی ۱۵۰۰ mg سدیم. کودک: دوز کمتر بر پایه ۱ mEq پتاسیم به ازای هر گرم رزین.', 'Average 15–60 g/day. Separate from other oral drugs by ≥3 h (6 h with gastroparesis). Upright position. Each 60 mL contains 1,500 mg sodium. Children: lower doses based on 1 mEq K per g resin.', [d])])],
     [CI('ci', 'هیپوکالمی؛ حساسیت به رزین؛ بیماری انسدادی روده؛ مصرف خوراکی یا رکتال در نوزاد.', 'Hypokalaemia; resin hypersensitivity; obstructive bowel disease; oral or rectal use in neonates.', [R(Sp, 'Contraindications')])],
     warn=[W('نکروز روده (گاهی کشنده) و عوارض جدی گوارشی؛ با سوربیتول مصرف نشود.', 'Intestinal necrosis (sometimes fatal) and serious GI events; avoid with sorbitol.', [R(Sp, 'Warnings')])],
     exs=[ex('std', 'susp-15-60', {'perDose': 15, 'mlPerDose': 60}, ageYears=60, weightKg=70)])

Lk = fda('lokelma', 'FDA Lokelma', 'Lokelma (sodium zirconium cyclosilicate) — Prescribing Information', sid('lokelma'))
drug('sodium-zirconium-cyclosilicate', 'various', 'سدیم زیرکونیوم سیکلوسیلیکات', 'Sodium zirconium cyclosilicate', T('جاذب پتاسیم', 'Potassium binder'), [{'name': 'Lokelma', 'market': 'US'}], ['lokelma', 'لوکلما'],
     [form('sachet-5', 'sachet', 'oral', '5 g sachet', 5, 'g', [R(Lk, '3')], per='sachet'), form('sachet-10', 'sachet', 'oral', '10 g sachet', 10, 'g', [R(Lk, '3')], per='sachet')],
     [reg('initial', 'hyperkalemia', T('هیپرکالمی — شروع ۱۰ g سه بار در روز تا ۴۸ ساعت', 'Hyperkalaemia — initial 10 g three times daily for up to 48 h'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 3}, [R(Lk, '2.1')], unit='g', dur={'min': 1, 'max': 2},
          notes=[note('در حدود ۳ قاشق آب. سایر داروهای خوراکی ۲ ساعت قبل یا بعد.', 'In about 3 tablespoons of water. Other oral drugs 2 h before or after.', [R(Lk, '2.3')])]),
      reg('maint', 'hyperkalemia', T('هیپرکالمی — نگهدارنده ۱۰ g یک بار در روز', 'Hyperkalaemia — maintenance 10 g once daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Lk, '2.1')], unit='g',
          notes=[note('بر اساس پتاسیم هر یک هفته یا بیشتر ۵ g تنظیم. همودیالیز: فقط روزهای غیر دیالیز، شروع ۵ g (پتاسیم بالای ۶٫۵: ۱۰ g).', 'Adjust by 5 g at intervals of ≥1 week by potassium. Haemodialysis: non-dialysis days only, start 5 g (K >6.5: 10 g).', [R(Lk, '2.1'), R(Lk, '2.2')])])],
     exs=[ex('initial', 'sachet-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70), ex('maint', 'sachet-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Sn = fda('sensipar', 'FDA Sensipar', 'Sensipar (cinacalcet) tablets — Prescribing Information', sid('sensipar'))
drug('cinacalcet', 'systemic-hormones', 'سیناکلست', 'Cinacalcet', T('کلسیمیمتیک', 'Calcimimetic'), [{'name': 'Sensipar', 'market': 'US'}], ['sensipar', 'mimpara', 'سیناکلست'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Sn, '3')]) for m in (30, 60, 90)],
     [reg('shpt', 'secondary-hyperparathyroidism-ckd', T('هیپرپاراتیروئیدی ثانویه در دیالیز — شروع ۳۰ mg یک بار در روز', 'Secondary hyperparathyroidism on dialysis — start 30 mg once daily'), A18, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Sn, '2.2')], limits={'maxPerDay': 180, 'refs': [R(Sn, '2.2')]},
          notes=[note('هر ۲ تا ۴ هفته: ۳۰ → ۶۰ → ۹۰ → ۱۲۰ → ۱۸۰ mg تا iPTH ۱۵۰ تا ۳۰۰. کلسیم و فسفر ظرف ۱ هفته، iPTH ۱ تا ۴ هفته پس از هر تغییر. با غذا؛ قرص کامل.', 'Every 2–4 weeks: 30 → 60 → 90 → 120 → 180 mg to iPTH 150–300. Calcium and phosphorus within 1 week, iPTH 1–4 weeks after each change. With food; swallow whole.', [R(Sn, '2.2'), R(Sn, '2.1')])])],
     [CI('ca', 'شروع درمان در کلسیم کمتر از حد طبیعی.', 'Starting treatment when serum calcium is below normal.', [R(Sn, '4')])],
     exs=[ex('shpt', 'tab-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=70)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['labetalol', 'hydralazine', 'sodium-polystyrene-sulfonate', 'sodium-zirconium-cyclosilicate', 'ticagrelor'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s6 ok')
