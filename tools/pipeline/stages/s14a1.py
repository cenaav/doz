"""Stage 14a (part 1) — anaesthesia: remifentanil, sufentanil, vecuronium, cisatracurium, ropivacaine, sevoflurane, isoflurane, desflurane.
Nitrous oxide skipped: its medical-gas SPL carries no dosing section."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
inf = lambda id, dis, fa, en, pop, dose, refs, unit='mcg', notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'infusion', dose, refs, unit=unit, notes=notes, allowed=allowed)
TRAINED = lambda src, sec: note('فقط توسط فرد آموزش‌دیده در بیهوشی، با امکانات راه هوایی، تهویه و احیا.', 'Only by personnel trained in anaesthesia, with airway, ventilation and resuscitation equipment at hand.', [R(src, sec)])
OPI_W = lambda src: W('هشدار جعبه‌ای: اعتیاد و سوءمصرف؛ دپرسیون تنفسی تهدیدکننده حیات؛ خطر با بنزودیازپین‌ها و سایر مضعف‌های CNS.', 'Boxed warning: addiction and misuse; life-threatening respiratory depression; risks with benzodiazepines and other CNS depressants.', [R(src, 'Boxed Warning')])
NMB_W = lambda src, sec: W('فقط با امکانات تنفس مصنوعی؛ هوشیاری را از بین نمی‌برد (بیهوشی کافی لازم)؛ آنافیلاکسی؛ فلج باقی‌مانده — پایش با محرک عصب محیطی.', 'Only with ventilatory support available; does not cause unconsciousness (adequate anaesthesia required); anaphylaxis; residual paralysis — monitor with a peripheral nerve stimulator.', [R(src, sec)])
VOL_CI = lambda src, sec, extra_fa='', extra_en='': CI('ci', 'استعداد ژنتیکی (شناخته یا مشکوک) هیپرترمی بدخیم؛ حساسیت به این دارو یا سایر هوشبرهای هالوژنه' + extra_fa + '.', 'Known or suspected genetic susceptibility to malignant hyperthermia; sensitivity to this or other halogenated anaesthetics' + extra_en + '.', [R(src, sec)])
VOL_W = lambda src, sec: W('هیپرترمی بدخیم؛ هیپرکالمی حین عمل (به‌ویژه میوپاتی‌ها)؛ طولانی شدن QT؛ آسیب کبد؛ نوروتوکسیسیتی احتمالی در کودک زیر ۳ سال با بیهوشی طولانی.', 'Malignant hyperthermia; perioperative hyperkalaemia (especially myopathies); QT prolongation; hepatic injury; possible neurotoxicity in children under 3 with prolonged anaesthesia.', [R(src, sec)])

Ul = fda('ultiva', 'FDA Ultiva', 'Ultiva (remifentanil) for injection 1/2/5 mg — Prescribing Information', sid('remifentanil'))
drug('remifentanil', 'nervous-system', 'رمی‌فنتانیل', 'Remifentanil', T('اپیوئید بسیار کوتاه‌اثر', 'Ultra-short-acting opioid'), [{'name': 'Ultiva', 'market': 'US'}], ['ultiva', 'اولتیوا', 'رمیفنتانیل'],
     [form('dil-50', 'injection', 'iv', 'Diluted 50 mcg/mL (1 mg in 20 mL)', 50, 'mcg', [R(Ul, '2, Table 5')], vol=1), form('vial-1', 'powder-for-injection', 'iv', '1 mg vial (dilute before use)', 1000, 'mcg', [R(Ul, '3')], per='vial')],
     [inf('maint', 'general-anesthesia', 'نگهداری بیهوشی (با پروپوفول یا ایزوفلوران) — ۰٫۲۵ mcg/kg/دقیقه (۰٫۰۵ تا ۲)', 'Maintenance of anaesthesia (with propofol or isoflurane) — 0.25 mcg/kg/min (0.05–2)', A18, {'perKgPerMin': 0.25, 'perKgPerMinMax': 2}, [R(Ul, '2.2, Table 1')], allowed=['dil-50'],
          notes=[note('القا: ۰٫۵ تا ۱ mcg/kg/دقیقه؛ بولوس اولیه ۱ mcg/kg طی ۳۰ تا ۶۰ ثانیه. با نیتروس اکساید ۰٫۴ mcg/kg/دقیقه. سالمند بالای ۶۵: نصف دوز شروع. چاقی: وزن ایده‌آل. فقط با پمپ؛ به‌تنهایی برای بیهوشی کافی نیست.', 'Induction: 0.5–1 mcg/kg/min; initial bolus 1 mcg/kg over 30–60 s. With nitrous oxide 0.4 mcg/kg/min. Over 65: halve the starting dose. Obesity: ideal body weight. Infusion device only; not adequate as sole anaesthetic.', [R(Ul, '2.2, Table 1'), R(Ul, '2.6'), R(Ul, '2.9'), R(Ul, '2.1')]),
                 TRAINED(Ul, '2.1')]),
      inf('postop', 'severe-pain', 'ادامه به‌عنوان مسکن در ریکاوری یا ICU — شروع ۰٫۱ mcg/kg/دقیقه (۰٫۰۲۵ تا ۰٫۲)', 'Continuation as analgesic into recovery/ICU — start 0.1 mcg/kg/min (0.025–0.2)', A18, {'perKgPerMin': 0.1, 'perKgPerMinMax': 0.2}, [R(Ul, '2.3')], allowed=['dil-50'],
          notes=[note('هر ۵ دقیقه ۰٫۰۲۵ mcg/kg/دقیقه تنظیم؛ بولوس برای درد پس از عمل توصیه نمی‌شود. پیش از قطع، مسکن جایگزین شروع شود.', 'Adjust by 0.025 mcg/kg/min every 5 min; boluses not recommended for postoperative pain. Establish alternative analgesia before stopping.', [R(Ul, '2.3'), R(Ul, '2.5')])])],
     [CI('ci', 'تزریق اپیدورال یا اینتراتکال (گلیسین)؛ حساسیت به رمی‌فنتانیل.', 'Epidural or intrathecal use (contains glycine); hypersensitivity to remifentanil.', [R(Ul, '4')])],
     warn=[OPI_W(Ul), W('سفتی عضلات اسکلتی؛ برادیکاردی و افت فشار؛ قطع سریع اثر؛ هایپرآلژزی.', 'Skeletal muscle rigidity; bradycardia and hypotension; rapid offset; opioid-induced hyperalgesia.', [R(Ul, '5')])],
     exs=[ex('maint', 'dil-50', {'perMin': 17.5, 'mlPerHour': 21, 'upperPerMin': 140, 'upperMlPerHour': 168}, ageYears=40, weightKg=70),
          ex('postop', 'dil-50', {'perMin': 7, 'mlPerHour': 8.4, 'upperPerMin': 14, 'upperMlPerHour': 16.8}, ageYears=40, weightKg=70)])

Sf = fda('sufentanil', 'FDA Sufentanil', 'Sufentanil citrate injection 50 mcg/mL (Hospira) — Prescribing Information', sid('sufentanil'))
drug('sufentanil', 'nervous-system', 'سوفنتانیل', 'Sufentanil', T('اپیوئید قوی (بیهوشی)', 'Potent opioid (anaesthesia)'), [{'name': 'Sufenta', 'market': 'US'}], ['sufenta', 'سوفنتا', 'سوفنتانیل'],
     [form('amp-50', 'injection', 'iv', '50 mcg/mL (1 mL vial)', 50, 'mcg', [R(Sf, '3')], vol=1)],
     [once('short', 'general-anesthesia', 'جزء مسکن بیهوشی عمومی (۱ تا ۲ ساعت) — کل ۱ تا ۲ mcg/kg', 'Analgesic component of general anaesthesia (1–2 h) — total 1–2 mcg/kg', A18, 1, 2, [R(Sf, '2, Table 1')], unit='mcg',
           notes=[note('حدود ۷۵٪ یا بیشتر پیش از لوله‌گذاری؛ سپس ۱۰ تا ۲۵ mcg در صورت نیاز. نیاز کل ۱ mcg/kg/ساعت یا کمتر توصیه می‌شود. دوز فردی بر اساس سن، وزن و وضعیت.', 'About 75% or more before intubation; then 10–25 mcg increments as needed. Total requirements of ≤1 mcg/kg/h recommended. Individualise by age, weight and status.', [R(Sf, '2, Table 1'), R(Sf, '2')]),
                  TRAINED(Sf, '2')])],
     [CI('hyper', 'حساسیت به سوفنتانیل.', 'Hypersensitivity to sufentanil.', [R(Sf, '4')])],
     warn=[OPI_W(Sf), W('سفتی عضلانی؛ دپرسیون شدید قلبی‌عروقی؛ تزریق اپیدورال نادرست؛ افزایش فشار داخل جمجمه.', 'Muscle rigidity; severe cardiovascular depression; improper epidural injection; raised intracranial pressure.', [R(Sf, '5')])],
     exs=[ex('short', 'amp-50', {'perDose': 70, 'mlPerDose': 1.4, 'upperPerDose': 140}, ageYears=40, weightKg=70)])

Vc = fda('vecuronium', 'FDA Vecuronium', 'Vecuronium bromide for injection 10/20 mg (Sun) — Prescribing Information', sid('vecuronium')); d = R(Vc, 'Dosage and Administration')
drug('vecuronium', 'musculoskeletal', 'وکورونیوم', 'Vecuronium', T('شل‌کننده عضلانی غیردپلاریزان', 'Non-depolarising neuromuscular blocker'), [{'name': 'Vecuronium', 'market': 'US'}], ['norcuron', 'نورکورون', 'وکورونیوم'],
     [form('vial-10', 'powder-for-injection', 'iv', '10 mg vial', 10, 'mg', [R(Vc, 'How Supplied')], per='vial')],
     [once('intub', 'intubation-nmb', 'لوله‌گذاری تراشه — ۰٫۰۸ تا ۰٫۱ mg/kg وریدی (بزرگسال و کودک ۱۰ سال به بالا)', 'Tracheal intubation — 0.08–0.1 mg/kg IV (adults and children ≥10 y)', {'minAge': age(10, 'year')}, 0.08, 0.1, [d],
           notes=[note('نگهدارنده ۰٫۰۱ تا ۰٫۰۱۵ mg/kg، اولین بار ۲۵ تا ۴۰ دقیقه بعد و سپس هر ۱۲ تا ۱۵ دقیقه. با هوشبرهای استنشاقی اثر بیشتر. شیرخوار ۷ هفته تا ۱ سال حساس‌تر و بهبود کندتر.', 'Maintenance 0.01–0.015 mg/kg, first at 25–40 min then about every 12–15 min. Potentiated by inhaled anaesthetics. Infants 7 weeks–1 y are more sensitive and recover more slowly.', [d, R(Vc, 'Pediatric Use')]), TRAINED(Vc, 'Dosage and Administration')])],
     [CI('hyper', 'حساسیت به وکورونیوم.', 'Hypersensitivity to vecuronium.', [R(Vc, 'Contraindications')])], warn=[NMB_W(Vc, 'Warnings')],
     exs=[ex('intub', 'vial-10', {'perDose': 5.6, 'upperPerDose': 7}, ageYears=40, weightKg=70)])

Cs = fda('cisatracurium', 'FDA Cisatracurium', 'Cisatracurium besylate injection 10 mg/mL (Avenacy) — Prescribing Information', sid('cisatracurium'))
drug('cisatracurium', 'musculoskeletal', 'سیس‌آتراکوریوم', 'Cisatracurium', T('شل‌کننده عضلانی غیردپلاریزان (بنزیل‌ایزوکینولین)', 'Non-depolarising neuromuscular blocker (benzylisoquinolinium)'), [{'name': 'Nimbex', 'market': 'US'}], ['nimbex', 'نیمبکس', 'سیس آتراکوریوم'],
     [form('vial-10', 'injection', 'iv', '10 mg/mL (200 mg/20 mL)', 10, 'mg', [R(Cs, '3')], vol=1)],
     [once('intub', 'intubation-nmb', 'لوله‌گذاری تراشه بزرگسال — ۰٫۱۵ تا ۰٫۲ mg/kg بولوس وریدی', 'Tracheal intubation, adults — 0.15–0.2 mg/kg IV bolus', A18, 0.15, 0.2, [R(Cs, '2.2')],
           notes=[note('نگهدارنده ۰٫۰۳ mg/kg، اولین بار ۴۰ تا ۵۰ دقیقه پس از ۰٫۱۵ mg/kg. شیرخوار ۱ تا ۲۳ ماه: ۰٫۱۵ mg/kg. سوختگی: مقاومت (دوز بیشتر). پایش با محرک عصب محیطی.', 'Maintenance 0.03 mg/kg, first at 40–50 min after 0.15 mg/kg. Infants 1–23 months: 0.15 mg/kg. Burns: resistance (higher doses). Monitor with a nerve stimulator.', [R(Cs, '2.3'), R(Cs, '2.2'), R(Cs, '2.4'), R(Cs, '2')]), TRAINED(Cs, '2')]),
      once('infant', 'intubation-nmb', 'لوله‌گذاری شیرخوار ۱ تا ۲۳ ماه — ۰٫۱۵ mg/kg طی ۵ تا ۱۰ ثانیه', 'Intubation, infants 1–23 months — 0.15 mg/kg over 5–10 s', {'minAge': age(1, 'month'), 'maxAge': age(2, 'year')}, 0.15, None, [R(Cs, '2.2')])],
     [CI('hyper', 'حساسیت شناخته‌شده به سیس‌آتراکوریوم.', 'Known hypersensitivity to cisatracurium.', [R(Cs, '4')])],
     warn=[NMB_W(Cs, '5'), W('خطای دارویی مرگبار (برچسب‌گذاری و نگهداری جدا)؛ تشنج (لادانوزین)؛ هیپرترمی بدخیم.', 'Fatal medication errors (separate storage and labelling); seizures (laudanosine); malignant hyperthermia.', [R(Cs, '5')])],
     exs=[ex('intub', 'vial-10', {'perDose': 10.5, 'mlPerDose': 1.05, 'upperPerDose': 14}, ageYears=40, weightKg=70), ex('infant', 'vial-10', {'perDose': 1.5, 'mlPerDose': 0.15}, ageMonths=10, weightKg=10)])

Np = fda('naropin', 'FDA Naropin', 'Naropin (ropivacaine HCl) injection — Prescribing Information', sid('ropivacaine'))
drug('ropivacaine', 'nervous-system', 'روپیواکائین', 'Ropivacaine', T('بی‌حس‌کننده موضعی آمیدی', 'Amide local anaesthetic'), [{'name': 'Naropin', 'market': 'US'}], ['naropin', 'ناروپین', 'روپیواکائین'],
     [form('vial-5', 'injection', 'percutaneous', '5 mg/mL (0.5%), 30 mL vial', 5, 'mg', [R(Np, '3')], vol=1)],
     [NC('regional', 'local-anesthesia', 'بی‌حسی جراحی (اپیدورال، بلوک اعصاب، انفیلتراسیون) و درد حاد (انفوزیون اپیدورال) بزرگسال — طبق جدول ۱', 'Surgical anaesthesia (epidural, nerve block, infiltration) and acute pain (epidural infusion), adults — per Table 1', A18,
         'دوز به محل، غلظت و حجم بستگی دارد (جدول ۱ برچسب). تا ۷۷۰ mg در ۲۴ ساعت (حین عمل + انفوزیون پس از عمل) و انفوزیون اپیدورال تا ۲۸ mg/ساعت به مدت ۷۲ ساعت تحمل شده است. آسپیره پیش از تزریق؛ دوز آزمایشی.',
         'Dose depends on site, concentration and volume (label Table 1). Up to 770 mg over 24 h (intraoperative block plus postoperative infusion) and epidural infusion up to 28 mg/h for 72 h have been tolerated. Aspirate before injecting; use a test dose.', [R(Np, '2.2, Table 1')])],
     [CI('hyper', 'حساسیت به روپیواکائین یا سایر بی‌حس‌کننده‌های آمیدی.', 'Hypersensitivity to ropivacaine or other amide local anaesthetics.', [R(Np, '4')])],
     warn=[W('تزریق داخل‌عروقی ناخواسته (سمیت CNS و قلب)؛ کندرولیز با انفوزیون داخل مفصل؛ مت‌هموگلوبینمی؛ احتیاط در بیماری کبد و قلب.', 'Unintended intravascular injection (CNS and cardiac toxicity); chondrolysis with intra-articular infusion; methaemoglobinaemia; caution in hepatic and cardiac disease.', [R(Np, '5')])])

Sv = fda('sevoflurane', 'FDA Sevoflurane', 'Sevoflurane, USP inhalation liquid (Baxter) — Prescribing Information', sid('sevoflurane'))
drug('sevoflurane', 'nervous-system', 'سووفلوران', 'Sevoflurane', T('هوشبر استنشاقی هالوژنه', 'Halogenated inhalational anaesthetic'), [{'name': 'Ultane', 'market': 'US'}], ['ultane', 'sevorane', 'سووران', 'سووفلوران'],
     [unitform('liq', 'solution', 'inhaled', 'Volatile liquid for vaporizer (100%)', [R(Sv, 'Description')])],
     [NC('ga', 'general-anesthesia', 'القا و نگهداری بیهوشی عمومی (بزرگسال و کودک) — غلظت دمی با ویپوریزر اختصاصی، فردی', 'Induction and maintenance of general anaesthesia (adults and children) — inspired concentration via a dedicated vaporizer, individualised', {},
         'دوز به‌صورت درصد غلظت دمی/MAC و بر اساس پاسخ بیمار تنظیم می‌شود؛ عدد قابل محاسبه با وزن ندارد. فقط با ویپوریزر کالیبره‌شده برای سووفلوران.', 'Dosed as inspired concentration/MAC and titrated to response; no weight-based number. Only with a vaporizer calibrated for sevoflurane.', [R(Sv, 'Dosage and Administration')])],
     [VOL_CI(Sv, 'Contraindications')], warn=[VOL_W(Sv, 'Warnings')])

Is = fda('terrell', 'FDA Terrell (isoflurane)', 'Terrell (isoflurane, USP) inhalation liquid — Prescribing Information', sid('isoflurane'))
drug('isoflurane', 'nervous-system', 'ایزوفلوران', 'Isoflurane', T('هوشبر استنشاقی هالوژنه', 'Halogenated inhalational anaesthetic'), [{'name': 'Forane', 'market': 'US'}], ['forane', 'terrell', 'فوران', 'ایزوفلوران'],
     [unitform('liq', 'solution', 'inhaled', 'Volatile liquid for vaporizer (100%)', [R(Is, '3')])],
     [NC('ga', 'general-anesthesia', 'القا و نگهداری بیهوشی عمومی — غلظت دمی ۱٫۵ تا ۳٪ برای القا (۷ تا ۱۰ دقیقه)؛ نگهداری بر اساس MAC سن', 'Induction and maintenance of general anaesthesia — inspired 1.5–3% for induction (7–10 min); maintenance by age-specific MAC', {},
         'دوز درصد غلظت دمی است، نه وزنی. القا ممکن است سرفه، حبس نفس و لارنگواسپاسم بدهد. فقط با ویپوریزر ویژه ایزوفلوران.', 'Dosed as inspired %, not by weight. Induction may cause coughing, breath-holding and laryngospasm. Only with an isoflurane-specific vaporizer.', [R(Is, '2.3'), R(Is, '2.4'), R(Is, '2.1')])],
     [VOL_CI(Is, '4', '؛ موارد منع بیهوشی عمومی؛ سابقه هپاتیت ناشی از هوشبر هالوژنه', '; patients in whom general anaesthesia is contraindicated; prior hepatitis from a halogenated anaesthetic')], warn=[VOL_W(Is, '5')])

Sp = fda('suprane', 'FDA Suprane', 'Suprane (desflurane, USP) inhalation liquid — Prescribing Information', sid('desflurane'))
drug('desflurane', 'nervous-system', 'دسفلوران', 'Desflurane', T('هوشبر استنشاقی هالوژنه', 'Halogenated inhalational anaesthetic'), [{'name': 'Suprane', 'market': 'US'}], ['suprane', 'سوپران', 'دسفلوران'],
     [unitform('liq', 'solution', 'inhaled', 'Volatile liquid for dedicated vaporizer (100%)', [R(Sp, '3')])],
     [NC('ga', 'general-anesthesia', 'نگهداری بیهوشی — بزرگسال ۲٫۵ تا ۸٫۵٪، کودک اینتوبه ۵٫۲ تا ۱۰٪', 'Maintenance of anaesthesia — adults 2.5–8.5%, intubated children 5.2–10%', {},
         'دوز درصد غلظت است. القا در بزرگسال (شروع ۳٪ با افزایش ۰٫۵ تا ۱٪)؛ برای القای کودکان ممنوع (تحریک راه هوایی). در بیماری کرونر به‌تنهایی برای القا نه.', 'Dosed as concentration %. Adult induction start 3% in 0.5–1% steps; contraindicated for induction in children (airway irritation). Not as sole induction agent in coronary disease.', [R(Sp, '2.3'), R(Sp, '2.2'), R(Sp, '2.6'), R(Sp, '4')])],
     [VOL_CI(Sp, '4', '؛ القای بیهوشی در کودکان؛ سابقه اختلال کبد پس از بیهوشی', '; induction in children; history of hepatic dysfunction after anaesthesia')], warn=[VOL_W(Sp, '5')])
print('s14a1 ok')
