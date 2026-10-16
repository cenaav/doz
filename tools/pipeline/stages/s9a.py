"""Stage 9a — ICU infusions (mcg/kg/min → mL/h), thrombolysis, bicarbonate, potassium (mEq), tolvaptan."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's9_setids.json')))
sid = lambda k: S[k][0]

add_disease('shock', 'شوک (سپتیک، کاردیوژنیک، افت فشار حاد) — ICU', 'Shock (septic, cardiogenic, acute hypotension) — ICU', ['shock', 'septic shock', 'شوک', 'افت فشار شدید', 'وازوپرسور'], ['R57.9', 'R65.21'], 'emergency')
add_disease('acute-ischemic-stroke', 'سکته مغزی ایسکمیک حاد (ترومبولیز)', 'Acute ischaemic stroke (thrombolysis)', ['acute stroke', 'tPA', 'سکته حاد', 'ترومبولیز'], ['I63.9'], 'neurology')
add_disease('pulmonary-embolism', 'آمبولی ریه', 'Pulmonary embolism', ['PE', 'آمبولی ریوی', 'لخته ریه'], ['I26.99'], 'cardiology')
add_disease('metabolic-acidosis', 'اسیدوز متابولیک', 'Metabolic acidosis', ['acidosis', 'اسیدوز', 'بیکربنات'], ['E87.20'], 'nephrology')
add_disease('hypokalemia', 'کمبود پتاسیم خون (هیپوکالمی)', 'Hypokalaemia', ['hypokalemia', 'پتاسیم پایین', 'هیپوکالمی'], ['E87.6'], 'nephrology')
add_disease('hyponatremia', 'کمبود سدیم خون (هیپوناترمی)', 'Hyponatraemia', ['hyponatremia', 'سدیم پایین', 'هیپوناترمی', 'SIADH'], ['E87.1'], 'nephrology')
ONE = {'min': 1, 'max': 1}
bag = lambda id, label, amt, unit, src, sec, per=1: form(id, 'injection', 'iv', label, amt, unit, [R(src, sec)], vol=per)
inf = lambda id, dis, fa, en, pop, dose, refs, unit='mcg', notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'infusion', dose, refs, unit=unit, notes=notes, allowed=allowed)
TITRATE = lambda src, sec: note('شروع با کمترین سرعت و تیتراسیون بر اساس فشار، ضربان و پرفیوژن. حجم کم شود قبل از شروع اصلاح شود. از ورید بزرگ؛ نشت دارو نکروز می‌دهد.', 'Start at the lowest rate and titrate to blood pressure, heart rate and perfusion. Correct hypovolaemia first. Use a large vein; extravasation causes necrosis.', [R(src, sec)])

# --- vasoactive infusions ---
Ne = fda('norepinephrine', 'FDA Norepinephrine bag', 'Norepinephrine bitartrate in sodium chloride injection (WG Critical Care) — Prescribing Information', sid('levophed'))
drug('norepinephrine', 'cardiovascular', 'نوراپی‌نفرین (لووفد)', 'Norepinephrine', T('وازوپرسور (آگونیست آلفا و بتا-۱)', 'Vasopressor (alpha and beta-1 agonist)'), [{'name': 'Levophed', 'market': 'US'}], ['levophed', 'noradrenaline', 'نوراپی نفرین', 'نورآدرنالین', 'لووفد'],
     [bag(f'bag-{c}', f'{m} mg/250 mL ready-to-use bag ({c} mcg/mL)', c, 'mcg', Ne, '3') for m, c in ((4, 16), (8, 32), (16, 64))],
     [inf('start', 'shock', 'افت فشار حاد — بزرگسال: شروع ۸ تا ۱۲ mcg/دقیقه', 'Acute hypotension — adult: start 8–12 mcg/min', A18, {'perMin': 8, 'perMinMax': 12}, [R(Ne, '2.2')], notes=[TITRATE(Ne, '2.1')]),
      inf('maint', 'shock', 'نگهدارنده — بزرگسال: معمولاً ۲ تا ۴ mcg/دقیقه', 'Maintenance — adult: usually 2–4 mcg/min', A18, {'perMin': 2, 'perMinMax': 4}, [R(Ne, '2.2')],
          notes=[note('قطع تدریجی؛ قطع ناگهانی افت شدید فشار می‌دهد.', 'Taper gradually; abrupt stop causes marked hypotension.', [R(Ne, '2.1'), R(Ne, '5')])])],
     warn=[W('ایسکمی بافت با نشت دارو؛ افت فشار با قطع ناگهانی؛ آریتمی.', 'Tissue ischaemia with extravasation; hypotension on abrupt stop; arrhythmias.', [R(Ne, '5')])],
     exs=[ex('start', 'bag-16', {'perMin': 8, 'mlPerHour': 30, 'upperPerMin': 12, 'upperMlPerHour': 45}, ageYears=60, weightKg=70), ex('maint', 'bag-16', {'perMin': 2, 'mlPerHour': 7.5}, ageYears=60, weightKg=70)])

Dp = fda('dopamine', 'FDA Dopamine premix', 'Dopamine hydrochloride and 5% dextrose injection (Baxter) — Prescribing Information', sid('dopamine')); d = R(Dp, 'Dosage and Administration — Suggested Regimen')
drug('dopamine', 'cardiovascular', 'دوپامین', 'Dopamine', T('اینوتروپ و وازوپرسور', 'Inotrope and vasopressor'), [{'name': 'Dopamine', 'market': 'US'}], ['intropin', 'دوپامین'],
     [bag(f'bag-{c}', f'{c} mcg/mL in D5W premixed bag', c, 'mcg', Dp, 'How Supplied') for c in (800, 1600, 3200)],
     [inf('mild', 'shock', 'شروع — بیمار با پاسخ احتمالی به افزایش متوسط: ۲ تا ۵ mcg/kg/دقیقه', 'Start — patients likely to respond to modest increments: 2–5 mcg/kg/min', A18, {'perKgPerMin': 2, 'perKgPerMinMax': 5}, [d], notes=[TITRATE(Dp, 'Dosage and Administration')]),
      inf('severe', 'shock', 'بیمار بدحال — شروع ۵ mcg/kg/دقیقه، افزایش ۵ تا ۱۰ تا ۲۰–۵۰', 'Seriously ill — start 5 mcg/kg/min, increase by 5–10 up to 20–50', A18, {'perKgPerMin': 5, 'perKgPerMinMax': 50}, [d],
          notes=[note('بالای ۵۰ mcg/kg/دقیقه برون‌ده ادرار مرتب چک شود.', 'Above 50 mcg/kg/min check urine output frequently.', [d]), TITRATE(Dp, 'Dosage and Administration')])],
     [CI('ci', 'فئوکروموسیتوم؛ تاکی‌آریتمی یا VF اصلاح‌نشده؛ حساسیت به ذرت (محلول دکستروز).', 'Phaeochromocytoma; uncorrected tachyarrhythmia or VF; corn allergy (dextrose solution).', [R(Dp, 'Contraindications')])],
     inter=[IA('maoi', 'بیمار با سابقه MAOI به دوز خیلی کمتر نیاز دارد.', 'Patients previously on MAOIs need substantially reduced doses.', [R(Dp, 'Warnings')])],
     exs=[ex('mild', 'bag-1600', {'perMin': 140, 'mlPerHour': 5.25, 'upperPerMin': 350, 'upperMlPerHour': 13.13}, ageYears=60, weightKg=70), ex('severe', 'bag-1600', {'perMin': 350, 'mlPerHour': 13.13}, ageYears=60, weightKg=70)])

Db = fda('dobutamine', 'FDA Dobutamine', 'Dobutamine injection 12.5 mg/mL (Hospira) — Prescribing Information', sid('dobutamine')); d = R(Db, 'Dosage and Administration — Recommended Dosage')
drug('dobutamine', 'cardiovascular', 'دوبوتامین', 'Dobutamine', T('اینوتروپ (آگونیست بتا-۱)', 'Inotrope (beta-1 agonist)'), [{'name': 'Dobutrex', 'market': 'US'}], ['dobutrex', 'دوبوتامین'],
     [bag(f'dil-{c}', f'Diluted to {c} mcg/mL (label Table 1)', c, 'mcg', Db, 'Dosage and Administration — Table 1') for c in (250, 500, 1000)],
     [inf('std', 'shock', 'افزایش برون‌ده قلب — بزرگسال: معمولاً ۲٫۵ تا ۱۵ mcg/kg/دقیقه', 'Increase cardiac output — adult: usually 2.5–15 mcg/kg/min', A18, {'perKgPerMin': 2.5, 'perKgPerMinMax': 15}, [d],
          notes=[note('به‌ندرت تا ۴۰ mcg/kg/دقیقه. ویال ۱۲٫۵ mg/mL باید دست‌کم در ۵۰ mL رقیق شود؛ با بیکربنات یا محلول قلیایی مخلوط نشود.', 'Rarely up to 40 mcg/kg/min. The 12.5 mg/mL vial must be diluted to at least 50 mL; not with bicarbonate or alkaline solutions.', [d, R(Db, 'Dosage and Administration')])])],
     [CI('ci', 'تنگی ساب‌آئورتیک هیپرتروفیک ایدیوپاتیک؛ حساسیت.', 'Idiopathic hypertrophic subaortic stenosis; hypersensitivity.', [R(Db, 'Contraindications')])],
     exs=[ex('std', 'dil-1000', {'perMin': 175, 'mlPerHour': 10.5, 'upperPerMin': 1050, 'upperMlPerHour': 63}, ageYears=60, weightKg=70)])

Vp = fda('vasostrict', 'FDA Vasostrict', 'Vasostrict (vasopressin) injection — Prescribing Information', sid('vasostrict'))
drug('vasopressin', 'systemic-hormones', 'وازوپرسین', 'Vasopressin', T('وازوپرسور (آگونیست V1)', 'Vasopressor (V1 agonist)'), [{'name': 'Vasostrict', 'market': 'US'}], ['vasostrict', 'pitressin', 'وازوپرسین'],
     [bag(f'pre-{n}', f'{u} units/100 mL premixed ({c} units/mL)', c, 'unit', Vp, '3') for n, u, c in (('02', 20, 0.2), ('04', 40, 0.4), ('06', 60, 0.6))],
     [inf('septic', 'shock', 'شوک سپتیک — ۰٫۰۱ تا ۰٫۰۷ واحد/دقیقه', 'Septic shock — 0.01–0.07 units/min', A18, {'perMin': 0.01, 'perMinMax': 0.07}, [R(Vp, '2.2')], unit='unit'),
      inf('cardiotomy', 'shock', 'شوک پس از جراحی قلب — ۰٫۰۳ تا ۰٫۱ واحد/دقیقه', 'Post-cardiotomy shock — 0.03–0.1 units/min', A18, {'perMin': 0.03, 'perMinMax': 0.1}, [R(Vp, '2.2')], unit='unit')],
     [CI('hyper', 'حساسیت به وازوپرسین (ویال چنددوزی: یا کلروبوتانول).', 'Hypersensitivity to vasopressin (multiple-dose vial: or chlorobutanol).', [R(Vp, '4')])],
     exs=[ex('septic', 'pre-02', {'perMin': 0.01, 'mlPerHour': 3, 'upperPerMin': 0.07, 'upperMlPerHour': 21}, ageYears=60, weightKg=70), ex('cardiotomy', 'pre-04', {'perMin': 0.03, 'mlPerHour': 4.5}, ageYears=60, weightKg=70)])

Es = fda('brevibloc', 'FDA Brevibloc', 'Brevibloc (esmolol) injection — Prescribing Information', sid('brevibloc'))
drug('esmolol', 'cardiovascular', 'اسمولول', 'Esmolol', T('بتابلاکر وریدی کوتاه‌اثر', 'Short-acting IV beta-blocker'), [{'name': 'Brevibloc', 'market': 'US'}], ['brevibloc', 'اسمولول'],
     [bag('bag-10', '10 mg/mL premixed bag or vial (10,000 mcg/mL)', 10000, 'mcg', Es, '3'), bag('bag-20', '20 mg/mL double-strength bag (20,000 mcg/mL)', 20000, 'mcg', Es, '3')],
     [inf('svt', 'svt', 'SVT یا تاکی‌کاردی سینوسی — نگهدارنده ۵۰ mcg/kg/دقیقه (تا ۲۰۰)', 'SVT or sinus tachycardia — maintenance 50 mcg/kg/min (up to 200)', A18, {'perKgPerMin': 50, 'perKgPerMinMax': 200}, [R(Es, '2.1')],
          notes=[note('بارگذاری اختیاری ۵۰۰ mcg/kg در ۱ دقیقه، سپس ۵۰ mcg/kg/دقیقه برای ۴ دقیقه؛ تیتراسیون هر ≥۴ دقیقه بر اساس ضربان یا فشار.', 'Optional load 500 mcg/kg over 1 min, then 50 mcg/kg/min for 4 min; titrate at ≥4-min intervals by rate or BP.', [R(Es, '2.1')])]),
      inf('periop', 'hypertensive-emergency', 'تاکی‌کاردی و فشار خون حین و پس از عمل — ۵۰ تا ۲۰۰ mcg/kg/دقیقه', 'Perioperative tachycardia and hypertension — 50–200 mcg/kg/min', A18, {'perKgPerMin': 50, 'perKgPerMinMax': 200}, [R(Es, '2.2')],
          notes=[note('بارگذاری ۵۰۰ mcg/kg در ۱ دقیقه (کنترل تدریجی) یا ۱ mg/kg در ۳۰ ثانیه (کنترل فوری) طبق برچسب.', 'Load 500 mcg/kg over 1 min (gradual control) or 1 mg/kg over 30 s (immediate control) per label.', [R(Es, '2.2')])])],
     [CI('ci', 'برادی‌کاردی سینوسی شدید؛ بلوک بالاتر از درجه ۱؛ سندرم سینوس بیمار؛ نارسایی قلب جبران‌نشده؛ شوک کاردیوژنیک؛ پرفشاری ریوی؛ مصرف وریدی وراپامیل اخیر.',
         'Severe sinus bradycardia; heart block above first degree; sick sinus syndrome; decompensated heart failure; cardiogenic shock; pulmonary hypertension; recent IV verapamil.', [R(Es, '4')])],
     exs=[ex('svt', 'bag-10', {'perMin': 3500, 'mlPerHour': 21, 'upperPerMin': 14000, 'upperMlPerHour': 84}, ageYears=50, weightKg=70), ex('periop', 'bag-20', {'perMin': 3500, 'mlPerHour': 10.5}, ageYears=50, weightKg=70)])

# --- thrombolysis ---
Av = fda('activase', 'FDA Activase', 'Activase (alteplase) for injection — Prescribing Information', sid('activase'))
drug('alteplase', 'blood', 'آلتپلاز (اکتیلیز)', 'Alteplase', T('ترومبولیتیک (tPA)', 'Thrombolytic (tPA)'), [{'name': 'Activase', 'market': 'US'}], ['activase', 'actilyse', 'tPA', 'آلتپلاز', 'اکتیلیز'],
     [form('vial-50', 'powder-for-injection', 'iv', '50 mg vial (1 mg/mL after reconstitution with 50 mL)', 1, 'mg', [R(Av, '3')], vol=1), form('vial-100', 'powder-for-injection', 'iv', '100 mg vial (1 mg/mL after reconstitution with 100 mL)', 1, 'mg', [R(Av, '3')], vol=1)],
     [reg('stroke', 'acute-ischemic-stroke', T('سکته ایسکمیک حاد (ظرف ۳ ساعت) — ۰٫۹ mg/kg کل (حداکثر ۹۰ mg)', 'Acute ischaemic stroke (within 3 h) — 0.9 mg/kg total (max 90 mg)'), A18, 'weightBased', {'perKgPerDay': 0.9, 'dividedDoses': 1}, [R(Av, '2.1'), R(Av, '2')],
          limits={'maxPerDose': 90, 'refs': [R(Av, '2')]}, dur=ONE,
          notes=[note('۱۰٪ کل دوز به‌صورت بولوس در ۱ دقیقه، بقیه در ۶۰ دقیقه انفوزیون. فقط پس از رد خونریزی مغزی و رعایت معیارهای منع مصرف.', '10% of the total as a bolus over 1 min, the rest infused over 60 min. Only after excluding haemorrhage and checking contraindications.', [R(Av, '2'), R(Av, '4.1')])]),
      reg('pe', 'pulmonary-embolism', T('آمبولی ریه حاد وسیع — ۱۰۰ mg وریدی در ۲ ساعت', 'Acute massive pulmonary embolism — 100 mg IV over 2 h'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Av, '2.3')], dur=ONE,
          notes=[note('هپارین پس از پایان انفوزیون وقتی PTT یا زمان ترومبین به ۲ برابر یا کمتر برگشت.', 'Start heparin after the infusion once PTT or thrombin time is ≤2× normal.', [R(Av, '2.3')])]),
      reg('ami', 'acute-coronary-syndrome', T('انفارکتوس حاد قلبی — رژیم سریع بر اساس وزن (حداکثر ۱۰۰ mg)', 'Acute MI — accelerated weight-based regimen (max 100 mg)'), A18, 'notCalculated',
          {'reason': T('برچسب، جدول ۱: بالای ۶۷ kg ← بولوس ۱۵ mg، ۵۰ mg در ۳۰ دقیقه، ۳۵ mg در ۶۰ دقیقه بعد. ۶۷ kg و کمتر ← بولوس ۱۵ mg، ۰٫۷۵ mg/kg در ۳۰ دقیقه، ۰٫۵ mg/kg در ۶۰ دقیقه. همراه هپارین و آسپرین. جمع حداکثر ۱۰۰ mg.',
                       'Label Table 1: >67 kg → 15 mg bolus, 50 mg over 30 min, 35 mg over the next 60 min. ≤67 kg → 15 mg bolus, 0.75 mg/kg over 30 min, 0.5 mg/kg over 60 min. With heparin and aspirin. Total ≤100 mg.')}, [R(Av, '2.2, Table 1')])],
     [CI('general', 'خونریزی داخلی فعال؛ جراحی یا ضربه اخیر مغز یا نخاع؛ ضایعه داخل جمجمه با خطر خونریزی؛ اختلال خونریزی؛ فشار خون شدید کنترل‌نشده. سکته: خونریزی داخل جمجمه یا زیر عنکبوتیه. MI و PE: سکته اخیر.',
         'Active internal bleeding; recent intracranial or intraspinal surgery or serious head trauma; intracranial conditions raising bleeding risk; bleeding diathesis; severe uncontrolled hypertension. Stroke: intracranial or subarachnoid haemorrhage. MI and PE: recent stroke.', [R(Av, '4')])],
     exs=[ex('stroke', 'vial-100', {'perDose': 63, 'mlPerDose': 63}, ageYears=65, weightKg=70), ex('stroke', 'vial-100', {'perDose': 90}, ageYears=65, weightKg=120), ex('pe', 'vial-100', {'perDose': 100, 'mlPerDose': 100}, ageYears=50, weightKg=80)])

Sk = dy('ir-darooyab-streptokinase', 'Darooyab Streptokinase', 'استرپتوکیناز — موارد مصرف، منع مصرف و اشکال دارویی', 'G-1889/Streptokinase')
drug('streptokinase', 'blood', 'استرپتوکیناز', 'Streptokinase', T('ترومبولیتیک', 'Thrombolytic'), [{'name': 'Streptokinase', 'market': 'IR'}], ['streptokinase', 'استرپتوکیناز', 'SK'],
     [form('vial-15', 'powder-for-injection', 'iv', '1,500,000 IU vial', 1500000, 'unit', [R(Sk, 'اشکال دارویی')], per='vial', markets=('IR',))],
     [reg('ami', 'acute-coronary-syndrome', T('انفارکتوس حاد قلبی، DVT، آمبولی ریه، ترومبوز شریانی', 'Acute MI, DVT, pulmonary embolism, arterial thromboembolism'), A18, 'notCalculated',
          {'reason': T('رفرنس مطمئن نیست: برچسب آمریکا یا انگلیس در دسترس نیست و اطلاعات از دارویاب است. دارویاب موارد مصرف را ذکر کرده ولی دوز عددی درمانی نداده است. دوز محاسبه نمی‌شود.', 'Reference not reliable: no US/UK label; information is from Darooyab, which lists indications but no numeric dosing. No dose is calculated.')}, [R(Sk, 'موارد مصرف')])],
     [CI('ci', 'آنوریسم دیسکان؛ خونریزی فعال؛ تومور مغزی یا ضایعه عروق مغز؛ جراحی مغز یا نخاع ظرف ۲ ماه؛ جراحی اخیر قفسه سینه؛ فشار خون شدید کنترل‌نشده؛ پانکراتیت حاد؛ نارسایی شدید کبد.',
         'Dissecting aneurysm; active bleeding; brain tumour or cerebrovascular lesion; intracranial or spinal surgery within 2 months; recent chest surgery; severe uncontrolled hypertension; acute pancreatitis; severe hepatic failure.', [R(Sk, 'منع مصرف')])])

# --- electrolytes ---
Bc = fda('bicarbonate', 'FDA NaHCO3 1.26%', 'Sodium bicarbonate injection 12.6 mg/mL (0.150 mEq/mL) (Baxter) — Prescribing Information', sid('bicarb'))
BCIR = note('در ایران بیشتر ویال ۷٫۵٪ و ۸٫۴٪ (حدود ۰٫۹ و ۱ mEq/mL) موجود است (دارویاب)؛ حجم را از mEq و غلظت همان ویال حساب کنید. حجم نمایش‌داده‌شده برای محلول ایزوتونیک ۰٫۱۵ mEq/mL است.',
            'In Iran 7.5% and 8.4% vials (about 0.9 and 1 mEq/mL) are common (Darooyab); compute volume from the mEq dose and that vial’s strength. The volume shown is for the isotonic 0.15 mEq/mL solution.', [R('darooyab-generic', 'G-2505/Sodium-Bicarbonate')])
drug('sodium-bicarbonate', 'blood', 'بیکربنات سدیم (تزریقی)', 'Sodium bicarbonate (injection)', T('قلیایی‌کننده', 'Alkalinising agent'), [{'name': 'Sodium bicarbonate', 'market': 'US'}], ['bicarbonate', 'بی کربنات', 'جوش شیرین تزریقی', 'NaHCO3'],
     [bag('bag-015', '12.6 mg/mL (0.150 mEq/mL) isotonic 1000 mL', 0.15, 'mEq', Bc, '3')],
     [reg('adult', 'metabolic-acidosis', T('اسیدوز متابولیک — بزرگسال و کودک ۲ سال به بالا: ۲ تا ۵ mEq/kg در ۴ تا ۸ ساعت', 'Metabolic acidosis — adults and children ≥2 y: 2–5 mEq/kg over 4–8 h'), {'minAge': age(2, 'year')}, 'weightBased', {'perKgPerDay': 2, 'perKgPerDayMax': 5, 'dividedDoses': 1}, [R(Bc, '2.2')], unit='mEq', dur=ONE,
          notes=[note('بر اساس بیکربنات سرم، CO2 کل، pH و وضعیت بالینی. رقیق نشود.', 'Guided by serum bicarbonate, total CO2, pH and clinical state. Do not dilute.', [R(Bc, '2.2'), R(Bc, '2.1')]), BCIR]),
      reg('child', 'metabolic-acidosis', T('اسیدوز متابولیک — زیر ۲ سال و نوزاد: ۱ تا ۲ mEq/kg در ۴ تا ۸ ساعت', 'Metabolic acidosis — under 2 y and neonates: 1–2 mEq/kg over 4–8 h'), {'maxAge': age(2, 'year')}, 'weightBased', {'perKgPerDay': 1, 'perKgPerDayMax': 2, 'dividedDoses': 1}, [R(Bc, '2.2')], unit='mEq', dur=ONE,
          notes=[note('بولوس یا تزریق سریع نه.', 'Avoid rapid or bolus administration.', [R(Bc, '2.2')]), BCIR])],
     [CI('ci', 'از دست دادن کلر با استفراغ یا ساکشن معده؛ مصرف دیورتیک‌های ایجادکننده آلکالوز هیپوکلرمیک.', 'Chloride loss from vomiting or GI suction; diuretics causing hypochloraemic alkalosis.', [R(Bc, '4')])],
     exs=[ex('adult', 'bag-015', {'perDose': 140, 'mlPerDose': 933.33, 'upperPerDose': 350}, ageYears=40, weightKg=70), ex('child', 'bag-015', {'perDose': 7.5, 'mlPerDose': 50}, ageMonths=6, weightKg=7.5)])

Ks = fda('kcl-solution', 'FDA KCl oral solution', 'Potassium chloride oral solution 10%/20% (Granules) — Prescribing Information', sid('kclsol'))
Ke = fda('kcl-er', 'FDA KCl ER tablet', 'Potassium chloride extended-release tablets 10 mEq (Granules) — Prescribing Information', sid('kcler'))
Ki = fda('kcl-iv', 'FDA KCl concentrate', 'Potassium chloride for injection concentrate 2 mEq/mL (Hospira) — Prescribing Information', sid('kcliv'))
ORALK = ['sol-10', 'sol-20', 'er-10']
KIR = note('در ایران: ویال ۱۵٪ (۲ mEq/mL)، شربت ۸٪ و ساشه ۲۰ mEq (دارویاب). شربت قبل از مصرف رقیق و با غذا.', 'In Iran: 15% vial (2 mEq/mL), 8% syrup and 20 mEq sachets (Darooyab). Dilute oral liquid and take with meals.', [R('darooyab-generic', 'G-2509/Potassium-chloride'), R(Ks, '2.1')])
drug('potassium-chloride', 'alimentary-metabolism', 'کلرید پتاسیم', 'Potassium chloride', T('مکمل الکترولیت', 'Electrolyte supplement'), [{'name': 'K-Dur / Klor-Con', 'market': 'US'}], ['KCl', 'klor-con', 'پتاسیم کلراید', 'کلرور پتاسیم'],
     [liquid('sol-10', 20, 15, '10% oral solution, 20 mEq/15 mL (1.3 mEq/mL)', [R(Ks, '3')], form_='solution', unit='mEq'), liquid('sol-20', 40, 15, '20% oral solution, 40 mEq/15 mL (2.6 mEq/mL)', [R(Ks, '3')], form_='solution', unit='mEq'),
      form('er-10', 'tablet', 'oral', '10 mEq (750 mg) extended-release tablet', 10, 'mEq', [R(Ke, 'How Supplied')], per='tablet'),
      form('iv-2', 'injection', 'iv', '2 mEq/mL concentrate — MUST be diluted', 2, 'mEq', [R(Ki, 'How Supplied')], vol=1)],
     [reg('adult-tx', 'hypokalemia', T('درمان هیپوکالمی — بزرگسال: ۴۰ تا ۱۰۰ mEq/روز در ۲ تا ۵ دوز (هر دوز حداکثر ۴۰)', 'Hypokalaemia treatment — adult: 40–100 mEq/day in 2–5 doses (max 40 per dose)'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 2}, [R(Ks, '2.2')], unit='mEq', allowed=ORALK,
          limits={'maxPerDose': 40, 'maxPerDay': 200, 'refs': [R(Ks, '2.2')]},
          notes=[note('پتاسیم سرم روزانه یا بیشتر تا طبیعی شدن. قرص آهسته‌رهش: هر دوز حداکثر ۲۰ mEq.', 'Check potassium daily or more until normal. ER tablets: no more than 20 mEq per dose.', [R(Ks, '2.1'), R(Ke, 'Dosage and Administration')]), KIR]),
      reg('adult-maint', 'hypokalemia', T('پیشگیری یا نگهدارنده — بزرگسال: معمولاً ۲۰ mEq/روز', 'Prevention or maintenance — adult: typically 20 mEq/day'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Ks, '2.2')], unit='mEq', allowed=ORALK, notes=[KIR]),
      reg('child-tx', 'hypokalemia', T('درمان هیپوکالمی — تولد تا ۱۶ سال: ۲ تا ۴ mEq/kg/روز در دوزهای منقسم', 'Hypokalaemia treatment — birth to 16 y: 2–4 mEq/kg/day in divided doses'), {'maxAge': age(16, 'year')}, 'weightBased', {'perKgPerDay': 2, 'perKgPerDayMax': 4, 'dividedDoses': 2}, [R(Ks, '2.3')], unit='mEq', allowed=['sol-10', 'sol-20'],
          limits={'maxPerKgPerDose': 1, 'maxPerDose': 40, 'maxPerDay': 100, 'refs': [R(Ks, '2.3')]}, notes=[note('هر دوز حداکثر ۱ mEq/kg یا ۴۰ mEq (هر کدام کمتر). کمبود شدید یا از دست دادن مداوم: درمان وریدی.', 'Single dose max 1 mEq/kg or 40 mEq, whichever is lower. Severe deficit or ongoing loss: consider IV.', [R(Ks, '2.3')]), KIR]),
      reg('child-maint', 'hypokalemia', T('نگهدارنده — تولد تا ۱۶ سال: ۱ mEq/kg/روز (حداکثر ۳ mEq/kg)', 'Maintenance — birth to 16 y: 1 mEq/kg/day (max 3 mEq/kg)'), {'maxAge': age(16, 'year')}, 'weightBased', {'perKgPerDay': 1, 'dividedDoses': 1}, [R(Ks, '2.3')], unit='mEq', allowed=['sol-10', 'sol-20'],
          limits={'maxPerKgPerDay': 3, 'refs': [R(Ks, '2.3')]}),
      reg('iv', 'hypokalemia', T('وریدی (رقیق‌شده) — پتاسیم بالای ۲٫۵: حداکثر ۱۰ mEq/ساعت', 'IV (diluted) — K >2.5: max 10 mEq/h'), A18, 'notCalculated',
          {'reason': T('برچسب: حتماً رقیق شود (تزریق مستقیم بی‌درنگ کشنده است). پتاسیم سرم بالای ۲٫۵: حداکثر ۱۰ mEq/ساعت با غلظت تا ۴۰ mEq/لیتر. زیر ۲ با تغییرات ECG یا فلج: با احتیاط تا ۴۰ mEq/ساعت با پایش مداوم ECG. حداکثر ۲۰۰ mEq در ۲۴ ساعت.',
                       'Label: must be diluted (direct injection can be instantly fatal). K >2.5: max 10 mEq/h at up to 40 mEq/L. K <2.0 with ECG changes or paralysis: cautiously up to 40 mEq/h with continuous ECG. Max 200 mEq per 24 h.')}, [R(Ki, 'Dosage and Administration'), R(Ki, 'Warnings')], allowed=['iv-2'])],
     [CI('ksparing', 'مصرف همزمان دیورتیک نگهدارنده پتاسیم.', 'Concomitant potassium-sparing diuretics.', [R(Ks, '4')]),
      CI('iv', 'تزریقی: هیپرکالمی، نارسایی کلیه و حالت‌های احتباس پتاسیم.', 'Injection: hyperkalaemia, renal failure and potassium retention.', [R(Ki, 'Contraindications')]),
      CI('solid', 'قرص: هر علتی برای توقف یا تأخیر عبور قرص در دستگاه گوارش (مثلاً گاستروپارزی دیابتی، داروهای آنتی‌کولینرژیک).', 'Tablets: any cause of arrested or delayed tablet transit (e.g. diabetic gastroparesis, anticholinergics).', [R(Ke, 'Contraindications')])],
     warn=[W('هیپرکالمی کشنده (به‌ویژه در نارسایی کلیه)؛ تزریق رقیق‌نشده فوراً کشنده است.', 'Fatal hyperkalaemia (especially in renal impairment); undiluted injection is instantly fatal.', [R(Ki, 'Warnings'), R(Ke, 'Warnings')])],
     exs=[ex('adult-tx', 'sol-10', {'perDose': 20, 'mlPerDose': 15, 'upperPerDose': 40}, ageYears=50, weightKg=70), ex('adult-maint', 'er-10', {'perDose': 20, 'tabletsPerDoseRounded': 2}, ageYears=50, weightKg=70),
          ex('child-tx', 'sol-10', {'perDose': 20, 'mlPerDose': 15}, ageYears=6, weightKg=20), ex('child-maint', 'sol-10', {'perDose': 20, 'mlPerDose': 15}, ageYears=6, weightKg=20)])

Tv = fda('samsca', 'FDA Samsca', 'Samsca (tolvaptan) tablets — Prescribing Information', sid('samsca'))
drug('tolvaptan', 'cardiovascular', 'تولواپتان', 'Tolvaptan', T('آنتاگونیست گیرنده وازوپرسین V2', 'Vasopressin V2 receptor antagonist'), [{'name': 'Samsca', 'market': 'US'}], ['samsca', 'سامسکا', 'تولواپتان'],
     [tab('tab-15', 15, '15 mg tablet', [R(Tv, '3')]), tab('tab-30', 30, '30 mg tablet', [R(Tv, '3')])],
     [reg('hyponat', 'hyponatremia', T('هیپوناترمی هیپرولمیک یا یوولمیک — شروع ۱۵ mg روزانه در بیمارستان (تا ۶۰ mg)', 'Hypervolaemic or euvolaemic hyponatraemia — start 15 mg daily in hospital (up to 60 mg)'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 15, 'increment': 15, 'incrementEveryDays': 1, 'max': 60}}, [R(Tv, '2.1')],
          notes=[note('فقط در بیمارستان شروع شود؛ اصلاح سریع سدیم دمیلیناسیون اسمزی می‌دهد. افزایش به ۳۰ و سپس حداکثر ۶۰ mg با فاصله دست‌کم ۲۴ ساعت.', 'Start only in hospital; over-rapid correction causes osmotic demyelination. Increase to 30 then up to 60 mg at ≥24-h intervals.', [R(Tv, '2.1'), R(Tv, 'Boxed Warning')])])],
     [CI('ci', 'هیپوناترمی هیپوولمیک؛ ناتوانی در حس یا پاسخ به تشنگی؛ مهارکننده‌های قوی CYP3A؛ آنوری؛ ADPKD خارج از REMS؛ حساسیت.', 'Hypovolaemic hyponatraemia; inability to sense or respond to thirst; strong CYP3A inhibitors; anuria; ADPKD outside REMS; hypersensitivity.', [R(Tv, '4')])],
     warn=[W('هشدار جعبه‌ای: شروع و شروع مجدد فقط در بیمارستان با پایش سدیم؛ برای ADPKD نیست.', 'Boxed warning: initiate and re-initiate only in hospital with sodium monitoring; not for ADPKD.', [R(Tv, 'Boxed Warning')])],
     exs=[ex('hyponat', 'tab-15', {'perDose': 15, 'tabletsPerDoseRounded': 1}, ageYears=70, weightKg=65)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['norepinephrine', 'dopamine', 'dobutamine', 'vasopressin', 'esmolol', 'alteplase', 'sodium-bicarbonate', 'potassium-chloride'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s9a ok')
