"""Stage 12a — ICU/emergency infusions, reversal agents and cardiac drugs."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
inf = lambda id, dis, fa, en, pop, dose, refs, unit='mcg', notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'infusion', dose, refs, unit=unit, notes=notes, allowed=allowed)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
bag = lambda id, label, amt, unit, src, sec='3': form(id, 'injection', 'iv', label, amt, unit, [R(src, sec)], vol=1)

add_disease('malignant-hyperthermia', 'هیپرترمی بدخیم (حین بیهوشی)', 'Malignant hyperthermia', ['malignant hyperthermia', 'هیپرترمی بدخیم', 'MH'], ['T88.3'], 'emergency')
add_disease('anticoagulant-reversal', 'خونریزی تهدیدکننده حیات با داروی ضدانعقاد (برگرداندن اثر)', 'Life-threatening bleeding on anticoagulants (reversal)', ['reversal', 'خونریزی با ضدانعقاد', 'آنتی دوت ضدانعقاد', 'antidote'], ['D68.32'], 'emergency')
add_disease('fibrinolytic-bleeding', 'خونریزی ناشی از فیبرینولیز زیاد', 'Bleeding from excessive fibrinolysis', ['fibrinolysis', 'فیبرینولیز', 'خونریزی جراحی قلب'], ['D65'], 'hematology')
add_disease('valve-thromboprophylaxis', 'پیشگیری از لخته پس از تعویض دریچه قلب', 'Thromboprophylaxis after heart-valve replacement', ['prosthetic valve', 'دریچه مصنوعی', 'تعویض دریچه'], ['Z95.2'], 'cardiology')

# --- IV antihypertensives / inotropes ---
Nc = fda('cardene-iv', 'FDA Cardene IV', 'Cardene I.V. (nicardipine) premixed 0.1/0.2 mg/mL — Prescribing Information', sid('nicardipine'))
NCH = note('شروع ۵ mg/ساعت؛ هر ۵ تا ۱۵ دقیقه ۲٫۵ mg/ساعت بیشتر تا حداکثر ۱۵ mg/ساعت. ماشین‌حساب سرعت mL/ساعت کیسه را نشان می‌دهد. از ورید مرکزی یا محیطی بزرگ؛ محل محیطی هر ۱۲ ساعت عوض شود.', 'Start 5 mg/h; increase by 2.5 mg/h every 5–15 min to max 15 mg/h. The calculator shows bag mL/h. Central or large peripheral vein; change peripheral site every 12 h.', [R(Nc, '2.1'), R(Nc, '2.3')])
drug('nicardipine-iv', 'cardiovascular', 'نیکاردیپین وریدی', 'Nicardipine (IV)', T('مسدودکننده کانال کلسیم دی‌هیدروپیریدینی', 'Dihydropyridine calcium channel blocker'), [{'name': 'Cardene IV', 'market': 'US'}], ['cardene', 'کاردن', 'نیکاردیپین'],
     [bag('bag-01', '20 mg/200 mL premixed (0.1 mg/mL)', 0.1, 'mg', Nc), bag('bag-02', '40 mg/200 mL premixed (0.2 mg/mL)', 0.2, 'mg', Nc)],
     [inf('htn', 'hypertensive-emergency', 'افزایش شدید فشار خون (وقتی خوراکی ممکن نیست) — شروع ۵ mg/ساعت، حداکثر ۱۵ mg/ساعت', 'Severe hypertension when oral therapy is not feasible — start 5 mg/h, max 15 mg/h', A18, {'perMin': round(5 / 60, 5), 'perMinMax': 0.25}, [R(Nc, '2.1')], unit='mg', notes=[NCH])],
     [CI('as', 'تنگی پیشرفته دریچه آئورت.', 'Advanced aortic stenosis.', [R(Nc, '4')])],
     warn=[W('پایش دقیق در آنژین، نارسایی قلب، کبد یا کلیه؛ از وریدهای کوچک دست استفاده نشود (ترومبوز و فلبیت)؛ از تزریق داخل شریان یا نشت پرهیز.', 'Monitor closely in angina, heart failure, hepatic or renal impairment; avoid small hand/wrist veins (thrombosis, phlebitis); avoid intra-arterial injection or extravasation.', [R(Nc, '5')])],
     exs=[ex('htn', 'bag-01', {'mlPerHour': 50, 'upperMlPerHour': 150}, ageYears=60, weightKg=80)])

Cl = fda('cleviprex', 'FDA Cleviprex', 'Cleviprex (clevidipine) emulsion 0.5 mg/mL — Prescribing Information', sid('clevidipine'))
drug('clevidipine', 'cardiovascular', 'کلودیپین', 'Clevidipine', T('مسدودکننده کانال کلسیم وریدی', 'IV calcium channel blocker'), [{'name': 'Cleviprex', 'market': 'US'}], ['cleviprex', 'کلودیپین'],
     [bag('vial-05', '0.5 mg/mL emulsion (50, 100, 250 mL)', 0.5, 'mg', Cl)],
     [inf('htn', 'hypertensive-emergency', 'کاهش فشار خون وقتی خوراکی ممکن نیست — شروع ۱ تا ۲ mg/ساعت؛ نگهدارنده معمولاً ۴ تا ۶ mg/ساعت', 'Blood pressure reduction when oral therapy is not feasible — start 1–2 mg/h; usual maintenance 4–6 mg/h', A18,
          {'perMin': round(1 / 60, 5), 'perMinMax': round(2 / 60, 5)}, [R(Cl, '2.2')], unit='mg',
          notes=[note('ابتدا هر ۹۰ ثانیه دو برابر؛ نزدیک هدف هر ۵ تا ۱۰ دقیقه کمتر از دو برابر. بیشتر بیماران تا ۱۶ mg/ساعت؛ به‌خاطر بار چربی حداکثر ۱۰۰۰ mL یا میانگین ۲۱ mg/ساعت در ۲۴ ساعت.', 'Double every 90 s initially; near goal less-than-double every 5–10 min. Most patients ≤16 mg/h; because of lipid load, no more than 1000 mL or an average 21 mg/h per 24 h.', [R(Cl, '2.2')])])],
     [CI('ci', 'حساسیت به سویا یا تخم‌مرغ؛ اختلال متابولیسم چربی؛ تنگی شدید آئورت.', 'Soy or egg allergy; defective lipid metabolism; severe aortic stenosis.', [R(Cl, '4')])],
     warn=[W('افت فشار و تاکی‌کاردی رفلکسی؛ امولسیون چربی (رعایت سترونی)؛ فشار برگشتی تا ۸ ساعت پس از قطع.', 'Hypotension and reflex tachycardia; lipid emulsion (aseptic technique); rebound hypertension up to 8 h after stopping.', [R(Cl, '5'), R(Cl, '2.1')])],
     exs=[ex('htn', 'vial-05', {'mlPerHour': 2, 'upperMlPerHour': 4}, ageYears=60, weightKg=80)])

Np = fda('nipride', 'FDA Nipride RTU', 'Nipride RTU (sodium nitroprusside) 0.2/0.5 mg/mL — Prescribing Information', sid('nitroprusside'))
drug('nitroprusside', 'cardiovascular', 'سدیم نیتروپروساید', 'Sodium nitroprusside', T('گشادکننده مستقیم عروق', 'Direct vasodilator'), [{'name': 'Nipride RTU', 'market': 'US'}], ['nipride', 'nitropress', 'نیتروپروساید', 'نیپراید'],
     [bag('vial-200', '0.2 mg/mL ready-to-use (= 200 mcg/mL)', 200, 'mcg', Np), bag('vial-500', '0.5 mg/mL ready-to-use (= 500 mcg/mL)', 500, 'mcg', Np)],
     [inf('htn', 'hypertensive-emergency', 'بحران فشار خون، نارسایی حاد قلب، کاهش کنترل‌شده فشار — شروع ۰٫۳ mcg/kg/دقیقه، حداکثر ۱۰', 'Hypertensive crisis, acute heart failure, controlled hypotension — start 0.3 mcg/kg/min, max 10', {},
          {'perKgPerMin': 0.3, 'perKgPerMinMax': 10}, [R(Np, '2.2')],
          notes=[note('پایش مداوم فشار؛ دست‌کم ۵ دقیقه صبر پیش از تغییر. فقط با پمپ حجمی. محلول آبی، سبز یا قرمز روشن مصرف نشود. با حداکثر سرعت، ظرف کمتر از ۱ ساعت ظرفیت سم‌زدایی سیانید پر می‌شود.', 'Continuous BP monitoring; wait ≥5 min before changing. Volumetric pump only. Do not use blue, green or bright-red solution. At the maximum rate, cyanide buffering capacity is exceeded in under 1 h.', [R(Np, '2.2'), R(Np, '2.3'), R(Np, '2.1'), R(Np, 'Boxed Warning')])])],
     [CI('ci', 'فشار جبرانی (کوآرکتاسیون آئورت، شانت شریانی-وریدی)؛ خونرسانی ناکافی مغز یا بیمار در حال مرگ (ASA 5E)؛ آتروفی عصب بینایی لبر یا آمبلیوپی تنباکو؛ نارسایی حاد قلب با مقاومت عروقی پایین؛ سیلدنافیل، تادالافیل، واردنافیل یا ریوسیگوات.',
         'Compensatory hypertension (aortic coarctation, AV shunting); inadequate cerebral circulation or moribund patients (ASA 5E); Leber’s optic atrophy or tobacco amblyopia; acute heart failure with reduced peripheral resistance; sildenafil, tadalafil, vardenafil or riociguat.', [R(Np, '4')])],
     warn=[W('هشدار جعبه‌ای: افت شدید فشار (آسیب ایسکمیک یا مرگ)؛ مسمومیت سیانید وابسته به دوز — مدت انفوزیون با حداکثر سرعت محدود شود.', 'Boxed warning: precipitous hypotension (ischaemic injury or death); dose-related, potentially lethal cyanide toxicity — limit time at the maximum rate.', [R(Np, 'Boxed Warning')])],
     exs=[ex('htn', 'vial-200', {'perMin': 21, 'mlPerHour': 6.3, 'upperPerMin': 700, 'upperMlPerHour': 210}, ageYears=60, weightKg=70)])

Ml = fda('milrinone', 'FDA Milrinone', 'Milrinone lactate injection 1 mg/mL (Mullan) — Prescribing Information', sid('milrinone')); d = R(Ml, 'Dosage and Administration')
drug('milrinone', 'cardiovascular', 'میلرینون', 'Milrinone', T('مهارکننده فسفودی‌استراز ۳ (اینوتروپ)', 'PDE3 inhibitor (inotrope)'), [{'name': 'Primacor', 'market': 'US'}], ['primacor', 'میلرینون', 'میلرینون لاکتات'],
     [bag('dil-200', 'Diluted to 200 mcg/mL (per label table)', 200, 'mcg', Ml, 'Dosage and Administration'), bag('vial-1', '1 mg/mL vial (= 1000 mcg/mL, for loading)', 1000, 'mcg', Ml, 'How Supplied')],
     [once('load', 'heart-failure', 'نارسایی حاد قلب — دوز بارگذاری ۵۰ mcg/kg آهسته در ۱۰ دقیقه', 'Acute decompensated heart failure — loading 50 mcg/kg slowly over 10 min', A18, 50, None, [d], unit='mcg', allowed=['vial-1']),
      inf('maint', 'heart-failure', 'نگهدارنده — ۰٫۳۷۵ تا ۰٫۷۵ mcg/kg/دقیقه (استاندارد ۰٫۵)', 'Maintenance — 0.375–0.75 mcg/kg/min (standard 0.5)', A18, {'perKgPerMin': 0.375, 'perKgPerMinMax': 0.75}, [d], allowed=['dil-200'],
          notes=[note('بیش از ۴۸ ساعت ایمنی یا اثر ثابت نشده. نارسایی کلیه: کاهش سرعت طبق جدول برچسب.', 'Not shown safe or effective beyond 48 h. Renal impairment: reduce rate per label table.', [R(Ml, 'Warnings'), d])])],
     [CI('hyper', 'حساسیت به میلرینون.', 'Hypersensitivity to milrinone.', [R(Ml, 'Contraindications')])],
     warn=[W('آریتمی بطنی و فوق‌بطنی؛ افت فشار؛ مصرف طولانی خوراکی در نارسایی شدید مرگ بیشتر.', 'Ventricular and supraventricular arrhythmias; hypotension; long-term oral use in severe HF increased mortality.', [R(Ml, 'Warnings')])],
     exs=[ex('load', 'vial-1', {'perDose': 3500, 'mlPerDose': 3.5}, ageYears=60, weightKg=70), ex('maint', 'dil-200', {'perMin': 26.25, 'mlPerHour': 7.88, 'upperPerMin': 52.5, 'upperMlPerHour': 15.75}, ageYears=60, weightKg=70)])

Ip = fda('isoproterenol', 'FDA Isoproterenol', 'Isoproterenol hydrochloride injection 0.2 mg/mL (Amphastar) — Prescribing Information', sid('isoproterenol'))
drug('isoproterenol', 'cardiovascular', 'ایزوپروترنول', 'Isoproterenol', T('آگونیست بتا-آدرنرژیک', 'Beta-adrenergic agonist'), [{'name': 'Isuprel', 'market': 'US'}], ['isuprel', 'isoprenaline', 'ایزوپرنالین', 'ایزوپروترنول'],
     [bag('dil-2', '1 mg in 500 mL D5W (2 mcg/mL)', 2, 'mcg', Ip, '2.2'), form('amp', 'injection', 'iv', '0.2 mg/mL vial', 200, 'mcg', [R(Ip, '3')], vol=1)],
     [inf('shock', 'shock', 'شوک و کاهش خونرسانی — بزرگسال ۰٫۵ تا ۵ mcg/دقیقه', 'Shock and hypoperfusion — adult 0.5–5 mcg/min', A18, {'perMin': 0.5, 'perMinMax': 5}, [R(Ip, '2.2')], allowed=['dil-2'],
          notes=[note('شروع با کمترین دوز و افزایش تدریجی. بالای ۳۰ mcg/دقیقه در شوک پیشرفته به کار رفته است.', 'Start at the lowest dose and increase gradually. Rates over 30 mcg/min have been used in advanced shock.', [R(Ip, '2.2')])]),
      reg('bronch', 'asthma', T('برونکواسپاسم حین بیهوشی — ۱۰ تا ۲۰ mcg وریدی', 'Bronchospasm during anaesthesia — 10–20 mcg IV'), A18, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [R(Ip, '2.2')], unit='mcg', dur=ONE, allowed=['amp'])],
     [CI('ci', 'تاکی‌کاردی؛ آریتمی بطنی؛ آنژین صدری.', 'Tachycardia; ventricular arrhythmias; angina pectoris.', [R(Ip, '4')])],
     exs=[ex('shock', 'dil-2', {'perMin': 0.5, 'mlPerHour': 15, 'upperPerMin': 5, 'upperMlPerHour': 150}, ageYears=60, weightKg=70), ex('bronch', 'amp', {'perDose': 10, 'mlPerDose': 0.05, 'upperPerDose': 20}, ageYears=40, weightKg=70)])

# --- antiplatelet / anticoagulant / reversal ---
Kg = fda('kengreal', 'FDA Kengreal', 'Kengreal (cangrelor) for injection 50 mg — Prescribing Information', sid('cangrelor'))
drug('cangrelor', 'blood', 'کانگرلور', 'Cangrelor', T('مهارکننده وریدی P2Y12', 'IV P2Y12 inhibitor'), [{'name': 'Kengreal', 'market': 'US'}], ['kengreal', 'کانگرلور'],
     [bag('dil-200', '50 mg vial diluted in 250 mL (200 mcg/mL)', 200, 'mcg', Kg, '2.3')],
     [once('bolus', 'acute-coronary-syndrome', 'PCI — بولوس ۳۰ mcg/kg پیش از PCI', 'PCI — 30 mcg/kg bolus before PCI', A18, 30, None, [R(Kg, '2.1')], unit='mcg'),
      inf('inf', 'acute-coronary-syndrome', 'انفوزیون ۴ mcg/kg/دقیقه بلافاصله پس از بولوس، دست‌کم ۲ ساعت یا تا پایان PCI', 'Infusion 4 mcg/kg/min right after the bolus, ≥2 h or the duration of PCI', A18, {'perKgPerMin': 4}, [R(Kg, '2.1')],
          notes=[note('پس از قطع، P2Y12 خوراکی: تیکاگرلور ۱۸۰ mg حین یا بلافاصله پس از انفوزیون؛ پراسوگرل ۶۰ mg یا کلوپیدوگرل ۶۰۰ mg بلافاصله پس از قطع.', 'After stopping, oral P2Y12: ticagrelor 180 mg during or right after; prasugrel 60 mg or clopidogrel 600 mg immediately after discontinuation.', [R(Kg, '2.2')])])],
     [CI('ci', 'خونریزی فعال قابل‌توجه؛ حساسیت به کانگرلور.', 'Significant active bleeding; hypersensitivity to cangrelor.', [R(Kg, '4')])],
     exs=[ex('bolus', 'dil-200', {'perDose': 2100, 'mlPerDose': 10.5}, ageYears=60, weightKg=70), ex('inf', 'dil-200', {'perMin': 280, 'mlPerHour': 84}, ageYears=60, weightKg=70)])

Fr = fda('fragmin', 'FDA Fragmin', 'Fragmin (dalteparin) injection — Prescribing Information', sid('dalteparin'))
drug('dalteparin', 'blood', 'دالته‌پارین', 'Dalteparin', T('هپارین با وزن مولکولی کم', 'Low-molecular-weight heparin'), [{'name': 'Fragmin', 'market': 'US'}], ['fragmin', 'فرگمین', 'دالتپارین'],
     [form('syr-5000', 'injection', 'sc', '5,000 units/0.2 mL syringe (also 2,500–18,000 units)', 25000, 'unit', [R(Fr, '3')], vol=1), form('syr-2500', 'injection', 'sc', '2,500 units/0.2 mL syringe', 12500, 'unit', [R(Fr, '3')], vol=1)],
     [reg('acs', 'acute-coronary-syndrome', T('آنژین ناپایدار و MI بدون موج Q — ۱۲۰ واحد/kg هر ۱۲ ساعت (حداکثر ۱۰٬۰۰۰ واحد)', 'Unstable angina and non-Q-wave MI — 120 units/kg every 12 h (max 10,000 units)'), A18, 'weightBased', {'perKgPerDose': 120, 'intervalHours': 12}, [R(Fr, '2.1')], unit='unit',
          limits={'maxPerDose': 10000, 'refs': [R(Fr, '2.1')]}, dur={'min': 5, 'max': 8}, allowed=['syr-5000'], notes=[note('همراه آسپرین ۷۵ تا ۱۶۵ mg روزانه تا پایداری بالینی.', 'With aspirin 75–165 mg daily until clinically stable.', [R(Fr, '2.1')])]),
      reg('proph', 'dvt-prophylaxis', T('پیشگیری DVT در بیمار داخلی یا جراحی شکم پرخطر — ۵۰۰۰ واحد یک بار در روز', 'DVT prophylaxis in medical or high-risk abdominal surgery — 5,000 units once daily'), A18, 'fixed', {'perDose': 5000, 'dosesPerDay': 1}, [R(Fr, '2.2')], unit='unit', allowed=['syr-5000'],
          notes=[note('جراحی شکم کم‌خطر: ۲۵۰۰ واحد. تعویض لگن: شروع ۲۵۰۰ واحد ۴ تا ۸ ساعت پس از جراحی سپس ۵۰۰۰ واحد روزانه (یا رژیم‌های پیش از عمل طبق برچسب).', 'Lower-risk abdominal surgery: 2,500 units. Hip replacement: 2,500 units 4–8 h after surgery then 5,000 units daily (or the pre-operative schemes per label).', [R(Fr, '2.2')])]),
      reg('vte-cancer', 'venous-thromboembolism', T('VTE در بیمار سرطانی — ماه اول ۲۰۰ واحد/kg یک بار در روز (حداکثر ۱۸٬۰۰۰ واحد)', 'Cancer-associated VTE — first month 200 units/kg once daily (max 18,000 units)'), A18, 'weightBased', {'perKgPerDose': 200, 'intervalHours': 24}, [R(Fr, '2.3')], unit='unit',
          limits={'maxPerDose': 18000, 'refs': [R(Fr, '2.3')]}, allowed=['syr-5000'], notes=[note('ماه ۲ تا ۶: حدود ۱۵۰ واحد/kg روزانه طبق جدول برچسب. ClCr زیر ۳۰: پایش anti-Xa.', 'Months 2–6: about 150 units/kg daily per label table. CrCl <30: monitor anti-Xa.', [R(Fr, '2.3'), R(Fr, '2.6')])])],
     [CI('ci', 'خونریزی فعال شدید؛ سابقه HIT؛ حساسیت به دالته‌پارین؛ بی‌حسی نخاعی/اپیدورال حین درمان دوز درمانی (آنژین ناپایدار، VTE).', 'Active major bleeding; history of HIT; hypersensitivity to dalteparin; neuraxial anaesthesia during therapeutic-dose treatment (unstable angina, VTE).', [R(Fr, '4')])],
     warn=[W('هشدار جعبه‌ای: هماتوم نخاعی یا اپیدورال با بی‌حسی نخاعی یا پونکسیون (فلج).', 'Boxed warning: spinal/epidural haematoma with neuraxial anaesthesia or puncture (paralysis).', [R(Fr, 'Boxed Warning')])],
     exs=[ex('acs', 'syr-5000', {'perDose': 8400, 'mlPerDose': 0.34}, ageYears=60, weightKg=70), ex('proph', 'syr-5000', {'perDose': 5000, 'mlPerDose': 0.2}, ageYears=60, weightKg=70), ex('vte-cancer', 'syr-5000', {'perDose': 14000, 'mlPerDose': 0.56}, ageYears=60, weightKg=70)])

Px = fda('praxbind', 'FDA Praxbind', 'Praxbind (idarucizumab) 2.5 g/50 mL — Prescribing Information', sid('idarucizumab'))
drug('idarucizumab', 'various', 'ایداروسیزوماب', 'Idarucizumab', T('آنتی‌دوت اختصاصی دابیگاتران', 'Specific dabigatran reversal agent'), [{'name': 'Praxbind', 'market': 'US'}], ['praxbind', 'پراکسبایند', 'آنتی دوت دابیگاتران'],
     [form('vial-25', 'injection', 'iv', '2.5 g/50 mL vial (dose = 2 vials)', 2500, 'mg', [R(Px, '3')], vol=50)],
     [reg('rev', 'anticoagulant-reversal', T('برگرداندن اثر دابیگاتران (جراحی اورژانس یا خونریزی تهدیدکننده) — ۵ g وریدی', 'Dabigatran reversal (emergency surgery or life-threatening bleeding) — 5 g IV'), {}, 'fixed', {'perDose': 5000, 'dosesPerDay': 1}, [R(Px, '2.1')], dur=ONE,
          notes=[note('دو ویال ۲٫۵ g پشت سر هم (انفوزیون یا بولوس). داده محدود برای ۵ g دوم. ضدانعقاد هرچه زودتر از نظر پزشکی شروع مجدد شود؛ دابیگاتران ۲۴ ساعت بعد.', 'Two 2.5 g vials consecutively (infusions or bolus). Limited data for a second 5 g. Restart anticoagulation as soon as medically appropriate; dabigatran after 24 h.', [R(Px, '2.1'), R(Px, '2.3'), R(Px, '2.4')])])],
     exs=[ex('rev', 'vial-25', {'perDose': 5000, 'mlPerDose': 100}, ageYears=75, weightKg=70)])

Ax = fda('andexxa', 'FDA Andexxa', 'Andexxa (andexanet alfa) 200 mg vial — Prescribing Information', sid('andexanet'))
drug('andexanet', 'various', 'آندگزانت آلفا', 'Andexanet alfa', T('آنتی‌دوت مهارکننده فاکتور Xa', 'Factor Xa inhibitor reversal agent'), [{'name': 'Andexxa', 'market': 'US'}], ['andexxa', 'آندکسا', 'آنتی دوت ریواروکسابان'],
     [form('vial-200', 'powder-for-injection', 'iv', '200 mg vial (10 mg/mL after reconstitution)', 200, 'mg', [R(Ax, '3')], per='vial')],
     [NC('rev', 'anticoagulant-reversal', 'خونریزی تهدیدکننده با ریواروکسابان یا آپیکسابان — دوز کم یا زیاد بر اساس دارو، دوز و زمان آخرین دوز', 'Life-threatening bleeding on rivaroxaban or apixaban — low or high dose by drug, dose and time since last dose', A18,
         'دوز کم: بولوس ۴۰۰ mg (۳۰ mg/دقیقه) سپس ۴ mg/دقیقه ۱۲۰ دقیقه. دوز زیاد: ۸۰۰ mg سپس ۸ mg/دقیقه ۱۲۰ دقیقه. انتخاب طبق جدول برچسب. بیش از یک دوز بررسی نشده.', 'Low dose: 400 mg bolus (30 mg/min) then 4 mg/min for 120 min. High dose: 800 mg then 8 mg/min for 120 min. Choice per label table. More than one dose not studied.', [R(Ax, '2.1')])],
     warn=[W('هشدار جعبه‌ای: ترومبوآمبولی، ایسکمی، ایست قلبی و مرگ ناگهانی.', 'Boxed warning: thromboembolic and ischaemic events, cardiac arrest and sudden death.', [R(Ax, 'Boxed Warning')])])

Ac = fda('aminocaproic', 'FDA Aminocaproic acid', 'Aminocaproic acid tablets 500/1000 mg — Prescribing Information', sid('aminocaproic')); d = R(Ac, 'Dosage and Administration')
drug('aminocaproic-acid', 'blood', 'آمینوکاپروئیک اسید', 'Aminocaproic acid', T('ضدفیبرینولیز', 'Antifibrinolytic'), [{'name': 'Amicar', 'market': 'US'}], ['amicar', 'آمیکار', 'آمینوکاپروئیک'],
     [tab('tab-500', 500, '500 mg tablet (scored)', [R(Ac, 'How Supplied')], scored=True), tab('tab-1000', 1000, '1000 mg tablet (scored)', [R(Ac, 'How Supplied')], scored=True)],
     [reg('bleed', 'fibrinolytic-bleeding', T('خونریزی حاد از فیبرینولیز زیاد — ساعت اول ۵ g، سپس ۱ g در ساعت حدود ۸ ساعت', 'Acute bleeding from elevated fibrinolysis — 5 g in the first hour, then 1 g per hour for about 8 h'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 8}, [d],
          dur=ONE, notes=[note('عدد ماشین‌حساب دوز ساعتی ۱ g است؛ ساعت اول ۵ g. تا کنترل خونریزی. فقط با تأیید فیبرینولیز اولیه، نه DIC.', 'The calculator gives the hourly 1 g dose; the first hour is 5 g. Continue until bleeding is controlled. Only with confirmed primary fibrinolysis, not DIC.', [d, R(Ac, 'Contraindications')])])],
     [CI('dic', 'شواهد فرایند انعقاد فعال داخل عروقی (DIC).', 'Evidence of an active intravascular clotting process (DIC).', [R(Ac, 'Contraindications')])],
     warn=[W('خونریزی دستگاه ادراری فوقانی: خطر انسداد با لخته؛ میوپاتی و رابدومیولیز در مصرف طولانی.', 'Upper urinary tract bleeding: risk of obstructing clots; myopathy and rhabdomyolysis with prolonged use.', [R(Ac, 'Warnings')])],
     exs=[ex('bleed', 'tab-1000', {'perDose': 1000, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=75)])

Dp = fda('dipyridamole', 'FDA Dipyridamole', 'Dipyridamole tablets 25/50/75 mg (Amneal) — Prescribing Information', sid('dipyridamole')); d = R(Dp, 'Dosage and Administration')
drug('dipyridamole', 'blood', 'دی‌پیریدامول', 'Dipyridamole', T('مهارکننده پلاکت', 'Platelet inhibitor'), [{'name': 'Persantine', 'market': 'US'}], ['persantine', 'پرسانتین', 'دیپیریدامول'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Dp, 'How Supplied')]) for m in (25, 50, 75)],
     [reg('valve', 'valve-thromboprophylaxis', T('پیشگیری از ترومبوآمبولی پس از تعویض دریچه (همراه وارفارین) — ۷۵ تا ۱۰۰ mg چهار بار در روز', 'After heart-valve replacement (with warfarin) — 75–100 mg four times daily'), A18, 'fixed', {'perDose': 75, 'perDoseMax': 100, 'dosesPerDay': 4}, [d],
          notes=[note('همراه وارفارین؛ آسپرین همزمان با کومارین داده نشود.', 'With warfarin; do not give aspirin with coumarin anticoagulants.', [d])])],
     [CI('hyper', 'حساسیت به دی‌پیریدامول.', 'Hypersensitivity to dipyridamole.', [R(Dp, 'Contraindications')])],
     exs=[ex('valve', 'tab-75', {'perDose': 75, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Ry = fda('ryanodex', 'FDA Ryanodex', 'Ryanodex (dantrolene sodium) 250 mg for injectable suspension — Prescribing Information', sid('dantrolene'))
drug('dantrolene', 'musculoskeletal', 'دانترولن', 'Dantrolene', T('شل‌کننده عضلانی مستقیم', 'Direct-acting muscle relaxant'), [{'name': 'Ryanodex / Dantrium', 'market': 'US'}], ['ryanodex', 'dantrium', 'دانترولن', 'دانتریوم'],
     [form('vial-250', 'powder-for-injection', 'iv', '250 mg vial → 50 mg/mL suspension after 5 mL water', 50, 'mg', [R(Ry, '3'), R(Ry, '2.4')], vol=1)],
     [once('tx', 'malignant-hyperthermia', 'درمان هیپرترمی بدخیم — دست‌کم ۱ mg/kg وریدی سریع؛ تکرار تا حداکثر تجمعی ۱۰ mg/kg', 'Treatment of malignant hyperthermia — at least 1 mg/kg IV push; repeat up to 10 mg/kg cumulative', {}, 1, None, [R(Ry, '2.1'), R(Ry, '2.3')],
           limits={'maxPerKgPerDay': 10, 'refs': [R(Ry, '2.1')]}, notes=[note('همزمان: قطع گازهای بیهوشی و سوکسینیل‌کولین، اصلاح اسیدوز، سرد کردن، دیورتیک (مانیتول فرآورده کافی نیست). کودک همان دوز بر kg.', 'Also: stop volatile agents and succinylcholine, correct acidosis, cool, give diuretics (product mannitol is insufficient). Children: same mg/kg.', [R(Ry, '2.1'), R(Ry, '2.3')])]),
      once('prev', 'malignant-hyperthermia', 'پیشگیری در بیمار پرخطر — ۲٫۵ mg/kg وریدی حدود ۷۵ دقیقه پیش از جراحی', 'Prevention in high-risk patients — 2.5 mg/kg IV about 75 min before surgery', {}, 2.5, None, [R(Ry, '2.2'), R(Ry, '2.3')])],
     warn=[W('ضعف عضلانی و اشکال بلع یا تنفس پس از تزریق؛ خواب‌آلودگی.', 'Muscle weakness and difficulty swallowing or breathing after administration; drowsiness.', [R(Ry, '5')])],
     exs=[ex('tx', 'vial-250', {'perDose': 70, 'mlPerDose': 1.4}, ageYears=30, weightKg=70), ex('prev', 'vial-250', {'perDose': 175, 'mlPerDose': 3.5}, ageYears=30, weightKg=70)])

# --- oral antiarrhythmics / diuretics / beta-blocker ---
Mt = fda('multaq', 'FDA Multaq', 'Multaq (dronedarone) 400 mg tablets — Prescribing Information', sid('dronedarone'))
drug('dronedarone', 'cardiovascular', 'درونادارون', 'Dronedarone', T('ضدآریتمی', 'Antiarrhythmic'), [{'name': 'Multaq', 'market': 'US'}], ['multaq', 'مولتاک', 'درونادارون'],
     [tab('tab-400', 400, '400 mg tablet', [R(Mt, '3')])],
     [reg('af', 'atrial-fibrillation', T('کاهش بستری در AF حمله‌ای یا پایدار (غیردائمی) — ۴۰۰ mg دو بار با صبحانه و شام', 'Reduce hospitalisation in paroxysmal or persistent (non-permanent) AF — 400 mg twice daily with meals'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 2}, [R(Mt, '2')],
          notes=[note('ضدآریتمی‌های کلاس I یا III و مهارکننده قوی CYP3A پیش از شروع قطع شوند. رد بارداری در زن در سن باروری.', 'Stop class I/III antiarrhythmics and strong CYP3A inhibitors before starting. Exclude pregnancy in women of reproductive potential.', [R(Mt, '2')])])],
     [CI('ci', 'AF دائمی؛ نارسایی قلبی علامت‌دار با بستری اخیر یا NYHA IV؛ بلوک AV درجه ۲ یا ۳ یا سینوس بیمار بدون پیس‌میکر؛ ضربان زیر ۵۰؛ مهارکننده قوی CYP3A و اریترومایسین؛ داروهای افزاینده QT؛ QTc بالای ۵۰۰ یا PR بالای ۲۸۰ ms؛ سمیت کبد یا ریه با آمیودارون قبلی؛ نارسایی شدید کبد؛ حساسیت.',
         'Permanent AF; symptomatic HF with recent decompensation or NYHA IV; 2nd/3rd-degree AV block or sick sinus without pacemaker; HR <50; strong CYP3A inhibitors and erythromycin; QT-prolonging drugs; QTc >500 or PR >280 ms; prior amiodarone liver or lung toxicity; severe hepatic impairment; hypersensitivity.', [R(Mt, '4')])],
     warn=[W('هشدار جعبه‌ای: در نارسایی قلبی اخیر یا NYHA IV و در AF دائمی خطر مرگ، سکته و نارسایی قلب دو برابر.', 'Boxed warning: doubles the risk of death, stroke and HF in recent decompensated/NYHA IV heart failure and in permanent AF.', [R(Mt, 'Boxed Warning')])],
     exs=[ex('af', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

Tk = fda('tikosyn', 'FDA Tikosyn', 'Tikosyn (dofetilide) capsules — Prescribing Information', sid('dofetilide')); d = R(Tk, 'Dosage and Administration')
drug('dofetilide', 'cardiovascular', 'دوفتیلید', 'Dofetilide', T('ضدآریتمی کلاس III', 'Class III antiarrhythmic'), [{'name': 'Tikosyn', 'market': 'US'}], ['tikosyn', 'دوفتیلاید', 'دوفتیلید'],
     [form(f'cap-{m}', 'capsule', 'oral', f'{m} mcg capsule', m, 'mcg', [R(Tk, 'How Supplied')], per='capsule') for m in (125, 250, 500)],
     [NC('af', 'atrial-fibrillation', 'تبدیل و حفظ ریتم سینوسی در AF/فلوتر — دوز بر اساس ClCr: >۶۰ ← ۵۰۰ mcg؛ ۴۰ تا ۶۰ ← ۲۵۰؛ ۲۰ تا <۴۰ ← ۱۲۵ mcg دو بار در روز', 'Conversion/maintenance of sinus rhythm in AF/AFL — by CrCl: >60 → 500 mcg; 40–60 → 250; 20–<40 → 125 mcg twice daily', A18,
         'فقط در مرکز با پایش مداوم ECG دست‌کم ۳ روز. QTc پایه بالای ۴۴۰ نه. ۲ تا ۳ ساعت پس از دوز اول QTc؛ افزایش بیش از ۱۵٪ یا بالای ۵۰۰ ms: کاهش دوز طبق برچسب. ClCr زیر ۲۰ منع مصرف.', 'Start only in a facility with continuous ECG monitoring for ≥3 days. Not if baseline QTc >440 ms. QTc 2–3 h after the first dose; increase >15% or >500 ms: reduce per label. CrCl <20 contraindicated.', [d])],
     [CI('ci', 'سندرم QT طولانی؛ QTc پایه بالای ۴۴۰ ms (۵۰۰ با اختلال هدایت بطنی)؛ ClCr زیر ۲۰؛ وراپامیل، سایمتیدین، تری‌متوپریم، کتوکونازول، پروکلرپرازین، مژسترول، دولوتگراویر، هیدروکلروتیازید.', 'Long QT syndrome; baseline QTc >440 ms (500 with ventricular conduction abnormalities); CrCl <20; verapamil, cimetidine, trimethoprim, ketoconazole, prochlorperazine, megestrol, dolutegravir, hydrochlorothiazide.', [R(Tk, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: آریتمی بطنی (تورساد) — شروع یا شروع مجدد فقط با پایش ECG و محاسبه ClCr.', 'Boxed warning: ventricular arrhythmia (torsade) — initiate or re-initiate only with ECG monitoring and CrCl calculation.', [R(Tk, 'Boxed Warning'), d])])

Nd = fda('nadolol', 'FDA Nadolol', 'Nadolol tablets 20/40/80 mg — Prescribing Information', sid('nadolol')); d = R(Nd, 'Dosage and Administration')
drug('nadolol', 'cardiovascular', 'نادولول', 'Nadolol', T('بتابلاکر غیرانتخابی', 'Non-selective beta-blocker'), [{'name': 'Corgard', 'market': 'US'}], ['corgard', 'کورگارد', 'نادولول'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(Nd, 'How Supplied')], scored=True) for m in (20, 40, 80)],
     [reg('angina', 'angina', T('آنژین صدری — شروع ۴۰ mg یک بار؛ نگهدارنده ۴۰ تا ۸۰ mg (تا ۲۴۰)', 'Angina — start 40 mg once daily; maintenance 40–80 mg (up to 240)'), A18, 'fixed', {'perDose': 40, 'perDoseMax': 80, 'dosesPerDay': 1}, [d],
          limits={'maxPerDay': 240, 'refs': [d]}, notes=[note('افزایش ۴۰ تا ۸۰ mg هر ۳ تا ۷ روز. قطع ناگهانی خطر تشدید آنژین و MI دارد.', 'Increase by 40–80 mg every 3–7 days. Abrupt cessation may exacerbate angina and MI.', [d, R(Nd, 'Warnings')])]),
      reg('htn', 'hypertension', T('فشار خون — شروع ۴۰ mg یک بار؛ نگهدارنده ۴۰ تا ۸۰ mg (تا ۳۲۰)', 'Hypertension — start 40 mg once daily; maintenance 40–80 mg (up to 320)'), A18, 'fixed', {'perDose': 40, 'perDoseMax': 80, 'dosesPerDay': 1}, [d], limits={'maxPerDay': 320, 'refs': [d]})],
     [CI('ci', 'آسم برونشیال؛ برادی‌کاردی سینوسی و بلوک بالاتر از درجه ۱؛ شوک کاردیوژنیک؛ نارسایی آشکار قلب.', 'Bronchial asthma; sinus bradycardia and greater than first-degree block; cardiogenic shock; overt cardiac failure.', [R(Nd, 'Contraindications')])],
     warn=[W('قطع ناگهانی — تشدید آنژین و گاه MI؛ کاهش تدریجی.', 'Abrupt withdrawal — exacerbated angina and occasionally MI; taper gradually.', [R(Nd, 'Warnings')])],
     renal=[{'egfrBelow': 50, 'severity': 'warn', 'text': T('نارسایی کلیه: افزایش فاصله دوز طبق ClCr (برچسب).', 'Renal failure: extend the dosing interval by CrCl (per label).'), 'refs': [d]}],
     exs=[ex('angina', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1, 'upperPerDose': 80}, ageYears=60, weightKg=75), ex('htn', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1, 'upperPerDose': 80}, ageYears=55, weightKg=80)])

Ed = fda('edecrin', 'FDA Edecrin', 'Edecrin (ethacrynic acid) tablets / Sodium Edecrin IV — Prescribing Information', sid('ethacrynic')); d = R(Ed, 'Dosage and Administration')
drug('ethacrynic-acid', 'cardiovascular', 'اتاکرینیک اسید', 'Ethacrynic acid', T('دیورتیک لوپ (غیرسولفونامیدی)', 'Loop diuretic (non-sulfonamide)'), [{'name': 'Edecrin', 'market': 'US'}], ['edecrin', 'اتاکرینیک اسید'],
     [tab('tab-25', 25, '25 mg tablet (scored)', [R(Ed, 'How Supplied')], scored=True), form('vial-50', 'powder-for-injection', 'iv', 'Sodium Edecrin 50 mg vial', 50, 'mg', [R(Ed, 'How Supplied')], per='vial')],
     [reg('oral', 'edema', T('ادم (نارسایی قلب، سیروز، کلیه) — بزرگسال: شروع ۵۰ mg پس از غذا؛ معمولاً ۵۰ تا ۲۰۰ mg/روز', 'Oedema (HF, cirrhosis, renal) — adult: start 50 mg after a meal; usually 50–200 mg/day'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 1}, [d], allowed=['tab-25'],
          notes=[note('تنظیم با پله ۲۵ تا ۵۰ mg؛ بیمار روزانه وزن شود. روز ۲: ۵۰ mg دو بار؛ روز ۳: ۱۰۰ mg صبح و ۵۰ تا ۱۰۰ mg عصر در صورت نیاز. جایگزین مناسب در حساسیت به سولفونامید.', 'Adjust in 25–50 mg steps; weigh daily. Day 2: 50 mg twice; day 3: 100 mg morning and 50–100 mg evening if needed. Option in sulfonamide allergy.', [d])]),
      once('iv', 'acute-pulmonary-edema', 'وریدی (ادم حاد ریه یا ناتوانی در خوراکی) — ۰٫۵ تا ۱ mg/kg (معمولاً ۵۰ mg)؛ هر دوز حداکثر ۱۰۰ mg', 'IV (acute pulmonary oedema or no oral route) — 0.5–1 mg/kg (usually 50 mg); single dose max 100 mg', A18, 0.5, 1, [d], allowed=['vial-50'],
           limits={'maxPerDose': 100, 'refs': [d]}, notes=[note('معمولاً یک دوز کافی است؛ دوز دوم در محل جدید (فلبیت).', 'Usually one dose; a second dose at a new site (thrombophlebitis).', [d])]),
      reg('child', 'edema', T('کودک (غیر شیرخوار) — شروع ۲۵ mg خوراکی، افزایش ۲۵ mg', 'Children (not infants) — start 25 mg orally, increase in 25 mg steps'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [d], allowed=['tab-25'])],
     [CI('ci', 'آنوری؛ شیرخواران؛ اسهال شدید آبکی قبلی با دارو؛ حساسیت.', 'Anuria; infants; prior severe watery diarrhoea with the drug; hypersensitivity.', [R(Ed, 'Contraindications')])],
     warn=[W('دیورز شدید و کم‌آبی، اختلال الکترولیت (هیپوکالمی)؛ سمیت گوش به‌ویژه وریدی یا با آمینوگلیکوزید.', 'Profound diuresis and dehydration, electrolyte loss (hypokalaemia); ototoxicity especially IV or with aminoglycosides.', [R(Ed, 'Warnings')])],
     exs=[ex('oral', 'tab-25', {'perDose': 50, 'tabletsPerDoseRounded': 2, 'upperPerDose': 100}, ageYears=65, weightKg=75), ex('iv', 'vial-50', {'perDose': 35, 'upperPerDose': 70}, ageYears=65, weightKg=70),
          ex('child', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=8, weightKg=25)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['nicardipine-iv', 'nitroprusside', 'milrinone', 'isoproterenol', 'idarucizumab', 'andexanet', 'dantrolene'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s12a ok')
