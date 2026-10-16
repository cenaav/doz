"""Stage 11a — anaesthesia and OR: induction agents, sedation infusions, neuromuscular blockers and reversal, bupivacaine, fentanyl patch."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's11_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
inj = lambda id, mg, ml, label, src, sec='3', unit='mg': form(id, 'injection', 'iv', label, mg, unit, [R(src, sec)], vol=ml)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
inf = lambda id, dis, fa, en, pop, dose, refs, unit='mcg', notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'infusion', dose, refs, unit=unit, notes=notes, allowed=allowed)
TRAINED = lambda src, sec, fa='', en='': note('فقط توسط فرد آموزش‌دیده در بیهوشی با امکانات کنترل راه هوایی، اکسیژن و احیا.' + fa, 'Only by persons trained in anaesthesia, with airway management, oxygen and resuscitation available.' + en, [R(src, sec)])

add_disease('icu-sedation', 'آرام‌بخشی در ICU و حین پروسیجر', 'ICU and procedural sedation', ['sedation', 'آرام بخشی', 'سدیشن', 'ICU sedation', 'procedural sedation'], ['Z51.89'], 'procedures')
add_disease('intubation-nmb', 'لوله‌گذاری تراشه و شل‌کردن عضلات (بلوک عصبی-عضلانی)', 'Tracheal intubation and neuromuscular blockade', ['intubation', 'RSI', 'لوله گذاری', 'شل کننده عضلانی', 'neuromuscular blocker'], ['Z01.818'], 'procedures')
add_disease('nmb-reversal', 'برگرداندن اثر شل‌کننده عضلانی', 'Reversal of neuromuscular blockade', ['reversal', 'ریورس', 'برگشت شل کننده'], ['Z01.818'], 'procedures')
add_disease('spinal-anesthesia', 'بی‌حسی نخاعی و اپیدورال', 'Spinal and epidural anaesthesia', ['spinal', 'epidural', 'بی حسی نخاعی', 'اسپاینال', 'اپیدورال'], ['Z01.818'], 'procedures')

Pp = fda('diprivan', 'FDA Diprivan', 'Diprivan (propofol) injectable emulsion — Prescribing Information', sid('propofol')); T1 = R(Pp, '2.7, Table 1')
drug('propofol', 'nervous-system', 'پروپوفول', 'Propofol', T('بیهوش‌کننده وریدی', 'IV general anaesthetic'), [{'name': 'Diprivan', 'market': 'US'}], ['diprivan', 'دیپریوان', 'پروپوفول'],
     [inj('em-10', 10, 1, '10 mg/mL emulsion (10, 20, 50, 100 mL vials)', Pp), inj('em-10-mcg', 10000, 1, '10 mg/mL emulsion = 10,000 mcg/mL (for infusion rate)', Pp, unit='mcg')],
     [once('ind-adult', 'general-anesthesia', 'القای بیهوشی — بزرگسال سالم زیر ۶۵ سال: ۲ تا ۲٫۵ mg/kg تا شروع اثر', 'Induction — healthy adult <65 y: 2–2.5 mg/kg titrated to onset', {'minAge': age(18, 'year'), 'maxAge': age(65, 'year')}, 2, 2.5, [T1, R(Pp, '2.2')],
           allowed=['em-10'], notes=[TRAINED(Pp, '2.1'), note('سالمند، ناتوان یا ASA III/IV: ۱ تا ۱٫۵ mg/kg؛ بیهوشی قلب: ۰٫۵ تا ۱٫۵؛ جراحی اعصاب: ۱ تا ۲ mg/kg. بولوس سریع در سالمند نه.', 'Elderly, debilitated or ASA III/IV: 1–1.5 mg/kg; cardiac: 0.5–1.5; neurosurgical: 1–2 mg/kg. No rapid boluses in the elderly.', [T1])]),
      once('ind-elderly', 'general-anesthesia', 'القای بیهوشی — سالمند، ناتوان یا ASA III/IV: ۱ تا ۱٫۵ mg/kg', 'Induction — elderly, debilitated or ASA III/IV: 1–1.5 mg/kg', {'minAge': age(65, 'year')}, 1, 1.5, [T1], allowed=['em-10'], notes=[TRAINED(Pp, '2.1')]),
      once('ind-child', 'general-anesthesia', 'القای بیهوشی — کودک سالم ۳ تا ۱۶ سال: ۲٫۵ تا ۳٫۵ mg/kg', 'Induction — healthy child 3–16 y: 2.5–3.5 mg/kg', {'minAge': age(3, 'year'), 'maxAge': age(17, 'year')}, 2.5, 3.5, [T1, R(Pp, '2.2')], allowed=['em-10'],
           notes=[TRAINED(Pp, '2.1'), note('کودکان کوچک‌تر ممکن است دوز بیشتری لازم داشته باشند. ایمنی القا زیر ۳ سال ثابت نشده است.', 'Younger children may need higher doses. Induction safety under 3 y not established.', [R(Pp, '2.2'), R(Pp, '2.7')])]),
      inf('maint', 'general-anesthesia', 'نگهداری بیهوشی — بزرگسال سالم: ۱۰۰ تا ۲۰۰ mcg/kg/دقیقه', 'Maintenance — healthy adult: 100–200 mcg/kg/min', {'minAge': age(18, 'year'), 'maxAge': age(65, 'year')}, {'perKgPerMin': 100, 'perKgPerMinMax': 200}, [T1],
          allowed=['em-10-mcg'], notes=[note('سالمند یا ASA III/IV: ۵۰ تا ۱۰۰ mcg/kg/دقیقه؛ بیهوشی قلب: ۲۵ تا ۱۰۰. کودک ۲ ماه تا ۱۶ سال: انفوزیون جداگانه طبق جدول برچسب.', 'Elderly or ASA III/IV: 50–100 mcg/kg/min; cardiac: 25–100. Children 2 months–16 y: separate infusion per label table.', [T1])]),
      inf('mac', 'icu-sedation', 'آرام‌بخشی حین پروسیجر (MAC) — بزرگسال: ۲۵ تا ۷۵ mcg/kg/دقیقه', 'Monitored anaesthesia care sedation — adult: 25–75 mcg/kg/min', A18, {'perKgPerMin': 25, 'perKgPerMinMax': 75}, [R(Pp, '2.4')], allowed=['em-10-mcg'],
          notes=[note('شروع با انفوزیون یا تزریق آهسته، نه بولوس سریع.', 'Start with a slow infusion or slow injection, not a rapid bolus.', [R(Pp, '2.4')])]),
      inf('icu', 'icu-sedation', 'آرام‌بخشی ICU بیمار اینتوبه — شروع ۵ mcg/kg/دقیقه، افزایش ۵ تا ۱۰ هر ۵ تا ۱۰ دقیقه', 'ICU sedation of intubated adults — start 5 mcg/kg/min, increase by 5–10 every 5–10 min', A18, {'perKgPerMin': 5, 'perKgPerMinMax': 50}, [T1, R(Pp, '2.6')],
          allowed=['em-10-mcg'], notes=[note('شروع ۵ mcg/kg/دقیقه دست‌کم ۵ دقیقه؛ افزایش تا رسیدن به سطح آرام‌بخشی. تغییر سرعت آهسته (بیش از ۵ دقیقه) برای پیشگیری از افت فشار. چربی خون پایش شود.', 'Start 5 mcg/kg/min for at least 5 min; increase until the desired sedation. Change rates slowly (>5 min) to avoid hypotension. Monitor blood lipids.', [T1, R(Pp, '2.6')])])],
     [CI('hyper', 'حساسیت به پروپوفول یا اجزای آن؛ سابقه آنافیلاکسی به تخم‌مرغ یا سویا.', 'Hypersensitivity to propofol or its components; history of anaphylaxis to eggs or soy.', [R(Pp, '4')])],
     warn=[W('افت فشار و دپرسیون تنفسی؛ سندرم انفوزیون پروپوفول در دوز بالا و طولانی؛ امولسیون چربی — رعایت سترونی (رشد میکروب).', 'Hypotension and respiratory depression; propofol infusion syndrome with high-dose prolonged use; lipid emulsion — strict asepsis (supports microbial growth).', [R(Pp, '5')])],
     exs=[ex('ind-adult', 'em-10', {'perDose': 140, 'mlPerDose': 14, 'upperPerDose': 175}, ageYears=40, weightKg=70), ex('ind-elderly', 'em-10', {'perDose': 70, 'mlPerDose': 7}, ageYears=75, weightKg=70),
          ex('ind-child', 'em-10', {'perDose': 50, 'mlPerDose': 5, 'upperPerDose': 70}, ageYears=6, weightKg=20), ex('maint', 'em-10-mcg', {'perMin': 7000, 'mlPerHour': 42, 'upperPerMin': 14000, 'upperMlPerHour': 84}, ageYears=40, weightKg=70),
          ex('mac', 'em-10-mcg', {'perMin': 1750, 'mlPerHour': 10.5, 'upperPerMin': 5250, 'upperMlPerHour': 31.5}, ageYears=40, weightKg=70), ex('icu', 'em-10-mcg', {'perMin': 350, 'mlPerHour': 2.1, 'upperPerMin': 3500, 'upperMlPerHour': 21}, ageYears=60, weightKg=70)])

Kt = fda('ketamine', 'FDA Ketamine', 'Ketamine hydrochloride injection (Eugia) — Prescribing Information', sid('ketamine'))
drug('ketamine', 'nervous-system', 'کتامین', 'Ketamine', T('بیهوش‌کننده تجزیه‌ای (آنتاگونیست NMDA)', 'Dissociative anaesthetic (NMDA antagonist)'), [{'name': 'Ketalar', 'market': 'US'}], ['ketalar', 'کتالار', 'کتامین'],
     [inj(f'inj-{c}', c, 1, f'{c} mg/mL multiple-dose vial', Kt) for c in (10, 50, 100)],
     [once('iv', 'general-anesthesia', 'القای بیهوشی وریدی — ۱ تا ۴٫۵ mg/kg آهسته در ۶۰ ثانیه', 'IV induction — 1–4.5 mg/kg slowly over 60 s', {'minAge': age(16, 'year')}, 1, 4.5, [R(Kt, '2.2')],
           notes=[TRAINED(Kt, '2.1'), note('یا ۱ تا ۲ mg/kg با سرعت ۰٫۵ mg/kg/دقیقه. نگهداری: نصف تا کل دوز القا در صورت نیاز تکرار شود.', 'Or 1–2 mg/kg at 0.5 mg/kg/min. Maintenance: repeat one-half to the full induction dose as needed.', [R(Kt, '2.2')])]),
      once('im', 'general-anesthesia', 'القای بیهوشی عضلانی — ۶٫۵ تا ۱۳ mg/kg', 'IM induction — 6.5–13 mg/kg', {'minAge': age(16, 'year')}, 6.5, 13, [R(Kt, '2.2')], allowed=['inj-50', 'inj-100'],
           notes=[note('۹ تا ۱۳ mg/kg معمولاً ظرف ۳ تا ۴ دقیقه بیهوشی جراحی می‌دهد که ۱۲ تا ۲۵ دقیقه طول می‌کشد.', '9–13 mg/kg usually gives surgical anaesthesia within 3–4 min, lasting 12–25 min.', [R(Kt, '2.2')])])],
     [CI('ci', 'هر جا افزایش قابل‌توجه فشار خون خطر جدی دارد؛ حساسیت به کتامین.', 'Patients in whom a significant rise in blood pressure would be a serious hazard; hypersensitivity to ketamine.', [R(Kt, '4')])],
     warn=[W('افزایش فشار و ضربان؛ واکنش‌های هنگام بیداری (توهم، رؤیا، هذیان)؛ دپرسیون تنفسی با تزریق سریع؛ ایمنی زیر ۱۶ سال ثابت نشده.', 'Raised BP and heart rate; emergence reactions (hallucinations, dreams, delirium); respiratory depression with rapid injection; safety under 16 y not established.', [R(Kt, '5'), R(Kt, '8.4')])],
     exs=[ex('iv', 'inj-10', {'perDose': 70, 'mlPerDose': 7, 'upperPerDose': 315}, ageYears=40, weightKg=70), ex('im', 'inj-100', {'perDose': 455, 'mlPerDose': 4.55, 'upperPerDose': 910}, ageYears=40, weightKg=70)])

Et = fda('amidate', 'FDA Amidate', 'Amidate (etomidate) injection 2 mg/mL — Prescribing Information', sid('etomidate')); d = R(Et, 'Dosage and Administration')
drug('etomidate', 'nervous-system', 'اتومیدیت', 'Etomidate', T('بیهوش‌کننده وریدی', 'IV general anaesthetic'), [{'name': 'Amidate', 'market': 'US'}], ['amidate', 'اتومیدیت'],
     [inj('inj-2', 2, 1, '2 mg/mL (20 mg/10 mL, 40 mg/20 mL)', Et, 'How Supplied')],
     [once('ind', 'general-anesthesia', 'القای بیهوشی — بزرگسال و کودک بالای ۱۰ سال: معمولاً ۰٫۳ mg/kg (۰٫۲ تا ۰٫۶) در ۳۰ تا ۶۰ ثانیه', 'Induction — adults and children >10 y: usually 0.3 mg/kg (0.2–0.6) over 30–60 s', {'minAge': age(10, 'year')}, 0.3, 0.6, [d],
           notes=[TRAINED(Et, 'Warnings'), note('زیر ۱۰ سال داده کافی نیست و توصیه نمی‌شود. سالمندان ممکن است دوز کمتری بخواهند. برای انفوزیون طولانی نه (سرکوب کورتیزول و آلدوسترون).', 'Insufficient data under 10 y — not recommended. Elderly may need less. Not for prolonged infusion (suppresses cortisol and aldosterone).', [d, R(Et, 'Warnings')])])],
     [CI('hyper', 'حساسیت به اتومیدیت.', 'Hypersensitivity to etomidate.', [R(Et, 'Contraindications')])],
     exs=[ex('ind', 'inj-2', {'perDose': 21, 'mlPerDose': 10.5, 'upperPerDose': 42}, ageYears=40, weightKg=70)])

Dx = fda('precedex', 'FDA Precedex', 'Precedex (dexmedetomidine) in 0.9% NaCl 4 mcg/mL — Prescribing Information', sid('dexmed'))
HR = note('دوز برچسب «mcg/kg/ساعت» است؛ ماشین‌حساب همان را به دقیقه و mL/ساعت تبدیل کرده است.', 'The label dose is in mcg/kg/HOUR; the calculator converts it to per minute and mL/h.', [R(Dx, '2.2')])
drug('dexmedetomidine', 'nervous-system', 'دکسمدتومیدین', 'Dexmedetomidine', T('آگونیست آلفا-۲ (آرام‌بخش)', 'Alpha-2 agonist (sedative)'), [{'name': 'Precedex', 'market': 'US'}], ['precedex', 'پرسدکس', 'دکس مدتومیدین'],
     [inj('bag-4', 4, 1, '4 mcg/mL ready-to-use (200 mcg/50 mL, 400 mcg/100 mL)', Dx, unit='mcg')],
     [once('load', 'icu-sedation', 'دوز بارگذاری ICU یا پروسیجر — بزرگسال: ۱ mcg/kg در ۱۰ دقیقه', 'Loading for ICU or procedural sedation — adult: 1 mcg/kg over 10 min', A18, 1, None, [R(Dx, '2.2, Table 1')], unit='mcg',
           notes=[note('بیمار در حال تعویض از آرام‌بخش دیگر ممکن است بارگذاری نخواهد. پروسیجر کم‌تهاجمی (مثلاً چشم): ۰٫۵ mcg/kg. سالمند و نارسایی کبد: کاهش دوز.', 'Patients switched from another sedative may not need a load. Less invasive procedures (e.g. eye): 0.5 mcg/kg. Elderly and hepatic impairment: consider reduction.', [R(Dx, '2.2, Table 1')])]),
      inf('icu', 'icu-sedation', 'نگهدارنده ICU — بزرگسال: ۰٫۲ تا ۰٫۷ mcg/kg/ساعت', 'ICU maintenance — adult: 0.2–0.7 mcg/kg/hour', A18, {'perKgPerMin': round(0.2 / 60, 5), 'perKgPerMinMax': round(0.7 / 60, 5)}, [R(Dx, '2.2, Table 1')],
          notes=[HR, note('بیش از ۲۴ ساعت انفوزیون اندیکاسیون ندارد.', 'Not indicated for infusions longer than 24 h.', [R(Dx, '2.1')])]),
      once('load-child', 'icu-sedation', 'بارگذاری پروسیجر غیرتهاجمی کودک — ۱ ماه تا <۲ سال: ۱٫۵ mcg/kg؛ ۲ تا <۱۸ سال: ۲ mcg/kg (در ۱۰ دقیقه)', 'Pediatric non-invasive procedure load — 1 month–<2 y: 1.5 mcg/kg; 2–<18 y: 2 mcg/kg (over 10 min)', {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 2, None,
           [R(Dx, '2.2, Table 2')], unit='mcg', notes=[note('نگهدارنده کودک: معمولاً شروع ۱٫۵ mcg/kg/ساعت، محدوده ۰٫۵ تا ۱٫۵.', 'Pediatric maintenance: usually start 1.5 mcg/kg/hour, range 0.5–1.5.', [R(Dx, '2.2, Table 2')])])],
     warn=[W('برادی‌کاردی، افت فشار و ایست سینوسی؛ افزایش گذرای فشار با بارگذاری؛ قطع ناگهانی پس از مصرف طولانی علائم ترک می‌دهد.', 'Bradycardia, hypotension and sinus arrest; transient hypertension with loading; withdrawal on abrupt stop after prolonged use.', [R(Dx, '5')])],
     exs=[ex('load', 'bag-4', {'perDose': 70, 'mlPerDose': 17.5}, ageYears=60, weightKg=70), ex('icu', 'bag-4', {'mlPerHour': 3.5, 'upperMlPerHour': 12.25}, ageYears=60, weightKg=70),
          ex('load-child', 'bag-4', {'perDose': 40, 'mlPerDose': 10}, ageYears=6, weightKg=20)])

Sx = fda('quelicin', 'FDA Quelicin', 'Quelicin (succinylcholine) injection 20 mg/mL — Prescribing Information', sid('sux'))
SXN = note('فقط با امکانات کامل راه هوایی و تهویه.', 'Only with full airway and ventilation support available.', [R(Sx, '2.1')])
drug('succinylcholine', 'musculoskeletal', 'سوکسینیل‌کولین (ساکسامتونیوم)', 'Succinylcholine (suxamethonium)', T('شل‌کننده عضلانی دپلاریزان', 'Depolarising neuromuscular blocker'), [{'name': 'Quelicin / Anectine', 'market': 'US'}], ['quelicin', 'anectine', 'suxamethonium', 'ساکسینیل کولین', 'سوکسامتونیوم'],
     [inj('inj-20', 20, 1, '20 mg/mL (200 mg/10 mL multiple-dose vial)', Sx)],
     [once('adult', 'intubation-nmb', 'لوله‌گذاری — بزرگسال: میانگین ۰٫۶ mg/kg وریدی (۰٫۳ تا ۱٫۱)', 'Intubation — adult: average 0.6 mg/kg IV (0.3–1.1)', A18, 0.6, 1.1, [R(Sx, '2.2')], notes=[SXN]),
      once('infant', 'intubation-nmb', 'لوله‌گذاری اورژانس — شیرخوار و کودک کوچک: ۲ mg/kg وریدی', 'Emergency intubation — infants and small children: 2 mg/kg IV', {'maxAge': age(2, 'year')}, 2, None, [R(Sx, '2.3')], notes=[SXN]),
      once('child', 'intubation-nmb', 'لوله‌گذاری اورژانس — کودک بزرگ‌تر و نوجوان: ۱ mg/kg وریدی', 'Emergency intubation — older children and adolescents: 1 mg/kg IV', {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 1, None, [R(Sx, '2.3')], notes=[SXN]),
      once('im', 'intubation-nmb', 'عضلانی (بدون راه وریدی) — تا ۳ تا ۴ mg/kg، حداکثر ۱۵۰ mg', 'IM (no IV access) — up to 3–4 mg/kg, max 150 mg total', {}, 3, 4, [R(Sx, '2.4')], limits={'maxPerDose': 150, 'refs': [R(Sx, '2.4')]})],
     [CI('ci', 'میوپاتی عضلات اسکلتی؛ پس از مرحله حاد سوختگی وسیع، ترومای متعدد، دنرواسیون گسترده یا آسیب نورون حرکتی فوقانی (هیپرکالمی و ایست قلب)؛ سابقه شخصی یا خانوادگی هیپرترمی بدخیم؛ حساسیت.',
         'Skeletal muscle myopathies; after the acute phase of major burns, multiple trauma, extensive denervation or upper motor neuron injury (hyperkalaemia and cardiac arrest); personal or family history of malignant hyperthermia; hypersensitivity.', [R(Sx, '4')])],
     warn=[W('هشدار جعبه‌ای: رابدومیولیز با هیپرکالمی، آریتمی بطنی، ایست قلبی و مرگ در کودکان ظاهراً سالم با میوپاتی تشخیص‌داده‌نشده (اغلب دوشن). هیپرترمی بدخیم.', 'Boxed warning: rhabdomyolysis with hyperkalaemia, ventricular dysrhythmias, cardiac arrest and death in apparently healthy children with undiagnosed myopathy (mostly Duchenne). Malignant hyperthermia.', [R(Sx, 'Boxed Warning'), R(Sx, '5')])],
     exs=[ex('adult', 'inj-20', {'perDose': 42, 'mlPerDose': 2.1, 'upperPerDose': 77}, ageYears=40, weightKg=70), ex('infant', 'inj-20', {'perDose': 16, 'mlPerDose': 0.8}, ageMonths=8, weightKg=8),
          ex('child', 'inj-20', {'perDose': 30, 'mlPerDose': 1.5}, ageYears=10, weightKg=30), ex('im', 'inj-20', {'perDose': 60, 'mlPerDose': 3, 'upperPerDose': 80}, ageYears=6, weightKg=20)])

Rc = fda('rocuronium', 'FDA Rocuronium', 'Rocuronium bromide injection 10 mg/mL (Baxter) — Prescribing Information', sid('roc'))
NMB = note('دوز با محرک عصب محیطی (TOF) تنظیم شود. فقط توسط فرد مجرب.', 'Titrate with a peripheral nerve stimulator (TOF). Experienced clinicians only.', [R(Rc, '2.1')])
drug('rocuronium', 'musculoskeletal', 'روکورونیوم', 'Rocuronium', T('شل‌کننده عضلانی غیردپلاریزان', 'Non-depolarising neuromuscular blocker'), [{'name': 'Zemuron', 'market': 'US'}], ['zemuron', 'esmeron', 'روکورونیوم', 'اسمرون'],
     [inj('inj-10', 10, 1, '10 mg/mL (50 mg/5 mL, 100 mg/10 mL)', Rc), inj('inj-10-mcg', 10000, 1, '10 mg/mL = 10,000 mcg/mL (for infusion rate)', Rc, unit='mcg')],
     [once('intub', 'intubation-nmb', 'لوله‌گذاری — ۰٫۶ mg/kg (بزرگسال و کودک)', 'Intubation — 0.6 mg/kg (adults and children)', {'minAge': age(3, 'month')}, 0.6, None, [R(Rc, '2.2'), R(Rc, '2.6')], allowed=['inj-10'],
           notes=[NMB, note('کودک: بسته به روش بیهوشی ۰٫۴۵ mg/kg هم کافی است.', 'Children: 0.45 mg/kg may suffice depending on the anaesthetic technique.', [R(Rc, '2.6')])]),
      once('rsi', 'intubation-nmb', 'لوله‌گذاری سریع (RSI) — ۰٫۶ تا ۱٫۲ mg/kg', 'Rapid sequence intubation — 0.6–1.2 mg/kg', A18, 0.6, 1.2, [R(Rc, '2.3')], allowed=['inj-10'], notes=[NMB]),
      once('maint', 'intubation-nmb', 'دوز نگهدارنده — ۰٫۱ تا ۰٫۲ mg/kg در بازگشت ۲۵٪ T1', 'Maintenance bolus — 0.1–0.2 mg/kg at 25% T1 recovery', A18, 0.1, 0.2, [R(Rc, '2.4')], allowed=['inj-10'], notes=[NMB]),
      inf('inf', 'intubation-nmb', 'انفوزیون — شروع ۱۰ تا ۱۲ mcg/kg/دقیقه پس از بازگشت اولیه', 'Infusion — start 10–12 mcg/kg/min after early recovery', A18, {'perKgPerMin': 10, 'perKgPerMinMax': 12}, [R(Rc, '2.5')], allowed=['inj-10-mcg'], notes=[NMB])],
     [CI('hyper', 'حساسیت (مثلاً آنافیلاکسی) به روکورونیوم یا سایر شل‌کننده‌ها.', 'Hypersensitivity (e.g. anaphylaxis) to rocuronium or other neuromuscular blockers.', [R(Rc, '4')])],
     warn=[W('آنافیلاکسی؛ فقط با بیهوشی کافی (فلج بدون آرام‌بخشی نه)؛ اشتباه دارویی کشنده است.', 'Anaphylaxis; only with adequate anaesthesia (no paralysis without sedation); accidental administration can be fatal.', [R(Rc, '5'), R(Rc, '2.1')])],
     exs=[ex('intub', 'inj-10', {'perDose': 42, 'mlPerDose': 4.2}, ageYears=40, weightKg=70), ex('rsi', 'inj-10', {'perDose': 42, 'mlPerDose': 4.2, 'upperPerDose': 84}, ageYears=40, weightKg=70),
          ex('maint', 'inj-10', {'perDose': 7, 'mlPerDose': 0.7, 'upperPerDose': 14}, ageYears=40, weightKg=70), ex('inf', 'inj-10-mcg', {'perMin': 700, 'mlPerHour': 4.2, 'upperPerMin': 840, 'upperMlPerHour': 5.04}, ageYears=40, weightKg=70)])

Ns = fda('neostigmine', 'FDA Neostigmine', 'Neostigmine methylsulfate injection 0.5/1 mg/mL (Par) — Prescribing Information', sid('neost'))
NSN = note('فقط وقتی پاسخ اول TOF دست‌کم ۱۰٪ پایه باشد. آتروپین یا گلیکوپیرولات قبل یا همزمان (با سرنگ جدا). کودکان مانند بزرگسال.', 'Only when the first TOF twitch is at least 10% of baseline. Atropine or glycopyrrolate before or with it (separate syringe). Children dosed as adults.', [R(Ns, '2.2'), R(Ns, '2.4'), R(Ns, '2.3')])
drug('neostigmine', 'nervous-system', 'نئوستیگمین', 'Neostigmine', T('مهارکننده کولین‌استراز', 'Cholinesterase inhibitor'), [{'name': 'Bloxiverz', 'market': 'US'}], ['bloxiverz', 'prostigmin', 'نئوستیگمین', 'پروستیگمین'],
     [inj('inj-05', 0.5, 1, '0.5 mg/mL (10 mL vial)', Ns), inj('inj-1', 1, 1, '1 mg/mL (10 mL vial)', Ns)],
     [once('short', 'nmb-reversal', 'برگرداندن شل‌کننده کوتاه‌اثر یا پاسخ اول TOF خیلی بیشتر از ۱۰٪ — ۰٫۰۳ mg/kg', 'Reversal of shorter-acting NMBA, or first twitch well above 10% — 0.03 mg/kg', {}, 0.03, None, [R(Ns, '2.2')], limits={'maxPerDose': 5, 'refs': [R(Ns, '2.2')]}, notes=[NSN]),
      once('long', 'nmb-reversal', 'برگرداندن شل‌کننده طولانی‌اثر یا پاسخ اول نزدیک ۱۰٪ — ۰٫۰۷ mg/kg (حداکثر ۵ mg)', 'Reversal of longer-acting NMBA, or first twitch near 10% — 0.07 mg/kg (max 5 mg)', {}, 0.07, None, [R(Ns, '2.2')], limits={'maxPerDose': 5, 'refs': [R(Ns, '2.2')]}, notes=[NSN])],
     [CI('ci', 'حساسیت به نئوستیگمین؛ پریتونیت یا انسداد مکانیکی روده یا مجاری ادرار.', 'Hypersensitivity to neostigmine; peritonitis or mechanical obstruction of the intestinal or urinary tract.', [R(Ns, '4')])],
     warn=[W('برادی‌کاردی، برونکواسپاسم؛ حداکثر کل ۰٫۰۷ mg/kg یا ۵ mg (هر کدام کمتر).', 'Bradycardia, bronchospasm; maximum total 0.07 mg/kg or 5 mg (whichever is less).', [R(Ns, '5'), R(Ns, '2.2')])],
     exs=[ex('short', 'inj-1', {'perDose': 2.1, 'mlPerDose': 2.1}, ageYears=40, weightKg=70), ex('long', 'inj-1', {'perDose': 4.9, 'mlPerDose': 4.9}, ageYears=40, weightKg=70)])

Sg = fda('bridion', 'FDA Bridion', 'Bridion (sugammadex) injection 100 mg/mL — Prescribing Information', sid('sugam'))
SGN = note('بر اساس وزن واقعی؛ زمان و دوز با پایش TOF؛ یک بولوس واحد.', 'Based on actual body weight; timing and dose by TOF monitoring; single bolus.', [R(Sg, '2.1')])
drug('sugammadex', 'various', 'شوگامادکس', 'Sugammadex', T('برگرداننده انتخابی روکورونیوم و وکورونیوم', 'Selective reversal agent for rocuronium/vecuronium'), [{'name': 'Bridion', 'market': 'US'}], ['bridion', 'بریدیون', 'سوگامادکس'],
     [inj('inj-100', 100, 1, '100 mg/mL (200 mg/2 mL, 500 mg/5 mL)', Sg)],
     [once('moderate', 'nmb-reversal', 'برگشت بلوک متوسط (ظهور پاسخ دوم TOF) — ۲ mg/kg', 'Moderate block (second TOF twitch reappeared) — 2 mg/kg', {}, 2, None, [R(Sg, '2.2')], notes=[SGN]),
      once('deep', 'nmb-reversal', 'برگشت بلوک عمیق (۱ تا ۲ پاسخ پس از تتانیک، بدون پاسخ TOF) — ۴ mg/kg', 'Deep block (1–2 post-tetanic counts, no TOF response) — 4 mg/kg', {}, 4, None, [R(Sg, '2.2')], notes=[SGN]),
      once('immediate', 'nmb-reversal', 'برگشت فوری ۳ دقیقه پس از ۱٫۲ mg/kg روکورونیوم — ۱۶ mg/kg (فقط بزرگسال)', 'Immediate reversal ~3 min after rocuronium 1.2 mg/kg — 16 mg/kg (adults only)', A18, 16, None, [R(Sg, '2.2')],
           notes=[SGN, note('برگشت فوری در کودکان بررسی نشده است.', 'Immediate reversal has not been studied in children.', [R(Sg, '2.2')])])],
     [CI('hyper', 'حساسیت به شوگامادکس (حتی بدون مواجهه قبلی آنافیلاکسی رخ داده).', 'Hypersensitivity to sugammadex (anaphylaxis has occurred without prior exposure).', [R(Sg, '4')])],
     warn=[W('آنافیلاکسی؛ برادی‌کاردی شدید؛ کاهش اثر قرص ضدبارداری هورمونی (۷ روز روش کمکی).', 'Anaphylaxis; marked bradycardia; reduces hormonal contraceptive effect (backup method for 7 days).', [R(Sg, '5')])],
     exs=[ex('moderate', 'inj-100', {'perDose': 140, 'mlPerDose': 1.4}, ageYears=40, weightKg=70), ex('deep', 'inj-100', {'perDose': 280, 'mlPerDose': 2.8}, ageYears=40, weightKg=70), ex('immediate', 'inj-100', {'perDose': 1120, 'mlPerDose': 11.2}, ageYears=40, weightKg=70)])

Bs = fda('marcaine-spinal', 'FDA Marcaine Spinal', 'Marcaine Spinal (bupivacaine 0.75% in dextrose 8.25%) — Prescribing Information', sid('bupispinal'))
Bp = fda('marcaine', 'FDA Marcaine', 'Marcaine (bupivacaine hydrochloride) injection 0.25/0.5/0.75% — Prescribing Information', sid('bupi'))
BSN = note('کمترین دوز و غلظت مؤثر. فقط توسط فرد مجرب با امکانات احیا.', 'Smallest effective dose and concentration. Only by experienced clinicians with resuscitation available.', [R(Bs, '2.2')])
spinal = lambda id, mg, fa, en: reg(id, 'spinal-anesthesia', T(fa, en), A18, 'fixed', {'perDose': mg, 'dosesPerDay': 1}, [R(Bs, '2.2')], dur=ONE, allowed=['spinal'], notes=[BSN])
drug('bupivacaine', 'nervous-system', 'بوپیواکائین (مارکائین)', 'Bupivacaine', T('بی‌حس‌کننده موضعی آمیدی طولانی‌اثر', 'Long-acting amide local anaesthetic'), [{'name': 'Marcaine / Sensorcaine', 'market': 'US'}], ['marcaine', 'sensorcaine', 'بوپیواکائین', 'مارکایین', 'بوپی'],
     [form('spinal', 'injection', 'intrathecal', 'Spinal 0.75% in 8.25% dextrose — 15 mg/2 mL (7.5 mg/mL)', 7.5, 'mg', [R(Bs, '3')], vol=1),
      inj('p025', 2.5, 1, '0.25% (2.5 mg/mL)', Bp), inj('p05', 5, 1, '0.5% (5 mg/mL)', Bp), inj('p075', 7.5, 1, '0.75% (7.5 mg/mL)', Bp)],
     [spinal('vaginal', 6, 'بی‌حسی نخاعی — زایمان طبیعی: ۶ mg', 'Spinal — vaginal delivery: 6 mg'),
      spinal('perineal', 7.5, 'بی‌حسی نخاعی — اندام تحتانی و پرینه: ۷٫۵ mg', 'Spinal — lower extremity and perineal procedures: 7.5 mg'),
      spinal('abdominal', 12, 'بی‌حسی نخاعی — جراحی پایین شکم: ۱۲ mg', 'Spinal — lower abdominal procedures: 12 mg'),
      reg('cs', 'spinal-anesthesia', T('بی‌حسی نخاعی — سزارین: ۷٫۵ تا ۱۰٫۵ mg', 'Spinal — Caesarean section: 7.5–10.5 mg'), A18, 'fixed', {'perDose': 7.5, 'perDoseMax': 10.5, 'dosesPerDay': 1}, [R(Bs, '2.2')], dur=ONE, allowed=['spinal'], notes=[BSN]),
      reg('local', 'local-anesthesia', T('بی‌حسی موضعی، بلوک عصب و اپیدورال (۰٫۲۵ تا ۰٫۷۵٪) — دوز بر اساس پروسیجر؛ حداکثر ۴۰۰ mg در ۲۴ ساعت', 'Infiltration, nerve block and epidural (0.25–0.75%) — dose by procedure; max 400 mg per 24 h'), A18, 'notCalculated',
          {'reason': T('دوز بر اساس نوع بلوک، عروقی بودن ناحیه و وضعیت بیمار طبق جدول ۳ برچسب؛ هر ۳ ساعت قابل تکرار؛ حداکثر کل ۴۰۰ mg در ۲۴ ساعت. اپیدورال: دوز آزمایشی و تزریق تدریجی ۳ تا ۵ mL با آسپیراسیون مکرر. ۰٫۷۵٪ برای بی‌حسی زایمان توصیه نمی‌شود.',
                       'Dose by block type, site vascularity and patient status per label Table 3; may repeat every 3 h; max 400 mg total in 24 h. Epidural: test dose and 3–5 mL increments with frequent aspiration. 0.75% not recommended for obstetric anaesthesia.')}, [R(Bp, '2.2'), R(Bp, '2.3')], allowed=['p025', 'p05', 'p075'])],
     [CI('ci', 'بلوک پاراسرویکال مامایی (برادی‌کاردی و مرگ جنین)؛ بی‌حسی وریدی ناحیه‌ای (Bier)؛ حساسیت به بی‌حس‌کننده‌های آمیدی. نخاعی: سپتی‌سمی، خونریزی شدید، شوک، آریتمی مهم، عفونت محل.', 'Obstetric paracervical block (fetal bradycardia and death); IV regional anaesthesia (Bier block); hypersensitivity to amide local anaesthetics. Spinal: septicaemia, severe haemorrhage, shock, significant arrhythmia, local infection.', [R(Bp, '4'), R(Bs, '4')])],
     warn=[W('مسمومیت سیستمیک (تشنج، ایست قلبی) با تزریق داخل‌عروقی؛ آماده بودن احیا و امولسیون چربی.', 'Systemic toxicity (seizures, cardiac arrest) with intravascular injection; have resuscitation ready.', [R(Bp, '5')])],
     exs=[ex('vaginal', 'spinal', {'perDose': 6, 'mlPerDose': 0.8}, ageYears=30, weightKg=70), ex('perineal', 'spinal', {'perDose': 7.5, 'mlPerDose': 1}, ageYears=50, weightKg=75),
          ex('abdominal', 'spinal', {'perDose': 12, 'mlPerDose': 1.6}, ageYears=50, weightKg=75), ex('cs', 'spinal', {'perDose': 7.5, 'mlPerDose': 1, 'upperPerDose': 10.5}, ageYears=30, weightKg=75)])

Fp = fda('fentanyl-patch', 'FDA Fentanyl patch', 'Fentanyl transdermal system (SpecGx) — Prescribing Information', sid('fentpatch'))
drug('fentanyl-patch', 'nervous-system', 'چسب پوستی فنتانیل', 'Fentanyl transdermal patch', T('آگونیست اپیوئیدی طولانی‌اثر', 'Long-acting opioid agonist'), [{'name': 'Duragesic', 'market': 'US'}], ['duragesic', 'چسب فنتانیل', 'fentanyl patch'],
     [unitform('patch', 'patch', 'transdermal', 'Patches 12 / 25 / 37.5 / 50 / 62.5 / 75 / 87.5 / 100 mcg/hour', [R(Fp, '3')])],
     [reg('chronic', 'severe-pain', T('درد شدید مداوم در بیمار مقاوم به اپیوئید — یک چسب هر ۷۲ ساعت', 'Severe persistent pain in opioid-TOLERANT patients — one patch every 72 h'), {'minAge': age(2, 'year')}, 'notCalculated',
          {'reason': T('فقط بیمار مقاوم به اپیوئید (دست‌کم ۶۰ mg مورفین خوراکی در روز یا معادل به مدت ≥۱ هفته). دوز اولیه بر اساس تبدیل از اپیوئید فعلی طبق برچسب؛ کمتر تخمین زدن امن‌تر است. هر ۷۲ ساعت؛ چسب مصرف‌شده تا شده و دفع شود. نارسایی خفیف/متوسط کبد یا کلیه: نصف دوز.',
                       'Opioid-tolerant patients only (≥60 mg oral morphine/day or equivalent for ≥1 week). Starting dose by conversion from the current opioid per label; underestimating is safer. Every 72 h; fold used patches and dispose. Mild/moderate hepatic or renal impairment: half the dose.')},
          [R(Fp, '2.1'), R(Fp, '2.3'), R(Fp, '2.5'), R(Fp, '2.6'), R(Fp, '2.8')])],
     [CI('ci', 'بیمار غیرمقاوم به اپیوئید؛ درد حاد، متناوب، پس از عمل یا خفیف؛ دپرسیون تنفسی؛ آسم شدید بدون پایش؛ انسداد روده؛ حساسیت.', 'Not opioid-tolerant; acute, intermittent, postoperative or mild pain; respiratory depression; severe asthma without monitoring; GI obstruction; hypersensitivity.', [R(Fp, '4')])],
     warn=[W('هشدار جعبه‌ای: دپرسیون تنفسی کشنده (به‌ویژه بیمار غیرمقاوم)، مواجهه تصادفی کودک کشنده است، گرما (تب، پد گرم، سونا) جذب را بالا می‌برد، تداخل با بنزودیازپین و مهارکننده CYP3A4.', 'Boxed warning: fatal respiratory depression (especially if not opioid-tolerant), accidental exposure in children is fatal, heat (fever, heating pads, saunas) raises absorption, interactions with benzodiazepines and CYP3A4 inhibitors.', [R(Fp, 'Boxed Warning')])])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['propofol', 'ketamine', 'etomidate', 'succinylcholine', 'rocuronium', 'sugammadex'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s11a ok')
