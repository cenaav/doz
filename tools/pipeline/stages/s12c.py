"""Stage 12c — hormones (GH, GnRH), diabetes (SGLT2, GLP-1, amylin), hypoglycaemia, Cushing, CKD-MBD and haematology (ESA, B12, TPO agonists, emicizumab)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed)
vial = lambda id, amt, label, src, unit='mg', route='sc', sec='3': form(id, 'powder-for-injection', route, label, amt, unit, [R(src, sec)], per='vial')
sol = lambda id, amt, vol, label, src, unit='mg', route='sc', sec='3': form(id, 'injection', route, label, amt, unit, [R(src, sec)], vol=vol)

add_disease('growth-hormone-deficiency', 'کمبود هورمون رشد و اختلالات رشد (ترنر، پرادر-ویلی، SGA، کوتاهی قد ایدیوپاتیک)', 'Growth hormone deficiency and growth disorders (Turner, Prader-Willi, SGA, idiopathic short stature)', ['GHD', 'کوتاهی قد', 'هورمون رشد', 'short stature'], ['E23.0'], 'endocrinology')
add_disease('cushing-disease', 'بیماری کوشینگ', 'Cushing disease', ['cushing', 'کوشینگ', 'هیپرکورتیزولیسم'], ['E24.0'], 'endocrinology')
add_disease('chemotherapy-induced-anemia', 'کم‌خونی ناشی از شیمی‌درمانی', 'Chemotherapy-induced anaemia', ['کم خونی شیمی درمانی', 'chemotherapy anemia'], ['D64.81'], 'oncology')
add_disease('immune-thrombocytopenia', 'ترومبوسیتوپنی ایمنی (ITP)', 'Immune thrombocytopenia (ITP)', ['ITP', 'پلاکت پایین', 'ترومبوسیتوپنی', 'پورپورای ترومبوسیتوپنیک'], ['D69.3'], 'hematology')
add_disease('aplastic-anemia', 'کم‌خونی آپلاستیک شدید', 'Severe aplastic anaemia', ['aplastic anemia', 'آپلاستیک', 'نارسایی مغز استخوان'], ['D61.9'], 'hematology')
add_disease('hemophilia-a', 'هموفیلی A', 'Haemophilia A', ['hemophilia', 'هموفیلی', 'کمبود فاکتور ۸'], ['D66'], 'hematology')
add_disease('acute-radiation-syndrome', 'سندرم حاد پرتوگیری (خون‌سازی)', 'Acute radiation syndrome (haematopoietic)', ['ARS', 'پرتوگیری', 'تشعشع هسته‌ای'], ['T66'], 'emergency')

# ===================== hormones =====================
Gt = fda('genotropin', 'FDA Genotropin', 'Genotropin (somatropin) for injection — Prescribing Information', sid('somatropin'))
drug('somatropin', 'systemic-hormones', 'سوماتروپین (هورمون رشد)', 'Somatropin', T('هورمون رشد نوترکیب', 'Recombinant growth hormone'), [{'name': 'Genotropin', 'market': 'US'}], ['genotropin', 'ژنوتروپین', 'growth hormone', 'هورمون رشد', 'GH'],
     [vial('cart-5', 5, '5 mg two-chamber cartridge', Gt), vial('cart-12', 12, '12 mg two-chamber cartridge', Gt)],
     [NC('peds', 'growth-hormone-deficiency', 'کودکان — دوز هفتگی mg/kg، تقسیم به ۶ یا ۷ تزریق زیرجلدی', 'Children — weekly mg/kg dose divided into 6 or 7 subcutaneous injections', {'maxAge': age(18, 'year')},
         'کمبود GH: ۰٫۱۶ تا ۰٫۲۴ mg/kg/هفته؛ پرادر-ویلی: ۰٫۲۴؛ SGA: تا ۰٫۴۸؛ ترنر: ۰٫۳۳؛ کوتاهی قد ایدیوپاتیک: تا ۰٫۴۷ mg/kg/هفته. دوز هفتگی بر ۶ یا ۷ تقسیم می‌شود؛ هرگز وریدی نه. زیر نظر متخصص غدد کودکان.',
         'GHD: 0.16–0.24 mg/kg/week; Prader-Willi: 0.24; SGA: up to 0.48; Turner: 0.33; idiopathic short stature: up to 0.47 mg/kg/week. Weekly dose split into 6 or 7 injections; never IV. Under a paediatric endocrinologist.', [R(Gt, '2'), R(Gt, '2.1')]),
      NC('adult', 'growth-hormone-deficiency', 'کمبود GH بزرگسال — حدود ۰٫۲ mg/روز (۰٫۱۵ تا ۰٫۳۰) یا حداکثر ۰٫۰۴ mg/kg/هفته در شروع', 'Adult GHD — about 0.2 mg/day (0.15–0.30) or not more than 0.04 mg/kg/week to start', A18,
         'بدون وزن: شروع ۰٫۲ mg/روز و هر ۱ تا ۲ ماه ۰٫۱ تا ۰٫۲ mg/روز افزایش. با وزن: شروع حداکثر ۰٫۰۴ و تا ۰٫۰۸ mg/kg/هفته طی ۴ تا ۸ هفته. تنظیم با پاسخ و IGF-I.',
         'Non-weight-based: start 0.2 mg/day, increase by 0.1–0.2 mg/day every 1–2 months. Weight-based: start ≤0.04, up to ≤0.08 mg/kg/week at 4–8-week intervals. Adjust to response and IGF-I.', [R(Gt, '2.2')])],
     [CI('ci', 'بیماری حاد بحرانی؛ کودک پرادر-ویلی با چاقی شدید یا اختلال تنفسی شدید (مرگ ناگهانی)؛ بدخیمی فعال؛ حساسیت؛ رتینوپاتی دیابتی پرولیفراتیو فعال یا غیرپرولیفراتیو شدید؛ کودک با اپی‌فیز بسته.',
         'Acute critical illness; children with Prader-Willi who are severely obese or have severe respiratory impairment (sudden death); active malignancy; hypersensitivity; active proliferative or severe non-proliferative diabetic retinopathy; children with closed epiphyses.', [R(Gt, '4')])],
     warn=[W('نئوپلاسم؛ اختلال تحمل گلوکز و دیابت؛ فشار داخل جمجمه؛ احتباس مایع؛ کم‌کاری آدرنال و تیروئید؛ لغزش اپی‌فیز سر فمور و پیشرفت اسکولیوز در کودک؛ پانکراتیت.', 'Neoplasms; impaired glucose tolerance and diabetes; intracranial hypertension; fluid retention; hypoadrenalism and hypothyroidism; slipped capital femoral epiphysis and scoliosis progression in children; pancreatitis.', [R(Gt, '5')])])

Lp = fda('lupron-depot', 'FDA Lupron Depot', 'Lupron Depot 7.5/22.5/30/45 mg (leuprolide acetate, prostate cancer) — Prescribing Information', sid('leuprolide'))
LPN = lambda: note('فقط توسط کادر درمان؛ دوزهای کسری یا ترکیب فرآورده‌های دپو مجاز نیست (رهش متفاوت).', 'Healthcare provider only; no fractional doses or combinations of depot products (different release).', [R(Lp, '2.1')])
drug('leuprolide', 'antineoplastic-immunomodulating', 'لوپرولید', 'Leuprolide', T('آگونیست GnRH', 'GnRH agonist'), [{'name': 'Lupron Depot', 'market': 'US'}], ['lupron', 'لوپرون', 'لوپرولین', 'leuprorelin', 'لوپرورلین', 'eligard'],
     [vial('dep-7-5', 7.5, '7.5 mg depot kit (1-month)', Lp, route='im'), vial('dep-22-5', 22.5, '22.5 mg depot kit (3-month)', Lp, route='im'), vial('dep-30', 30, '30 mg depot kit (4-month)', Lp, route='im'), vial('dep-45', 45, '45 mg depot kit (6-month)', Lp, route='im')],
     [reg('m1', 'prostate-cancer', T('سرطان پیشرفته پروستات — ۷٫۵ mg عضلانی هر ۴ هفته', 'Advanced prostate cancer — 7.5 mg IM every 4 weeks'), A18, 'fixed', {'perDose': 7.5, 'dosesPerDay': 1}, [R(Lp, '2.1')], dur=ONE, allowed=['dep-7-5'], notes=[LPN()]),
      reg('m3', 'prostate-cancer', T('سرطان پیشرفته پروستات — ۲۲٫۵ mg عضلانی هر ۱۲ هفته', 'Advanced prostate cancer — 22.5 mg IM every 12 weeks'), A18, 'fixed', {'perDose': 22.5, 'dosesPerDay': 1}, [R(Lp, '2.2')], dur=ONE, allowed=['dep-22-5']),
      reg('m4', 'prostate-cancer', T('سرطان پیشرفته پروستات — ۳۰ mg عضلانی هر ۱۶ هفته', 'Advanced prostate cancer — 30 mg IM every 16 weeks'), A18, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Lp, '2.3')], dur=ONE, allowed=['dep-30']),
      reg('m6', 'prostate-cancer', T('سرطان پیشرفته پروستات — ۴۵ mg عضلانی هر ۲۴ هفته', 'Advanced prostate cancer — 45 mg IM every 24 weeks'), A18, 'fixed', {'perDose': 45, 'dosesPerDay': 1}, [R(Lp, '2.4')], dur=ONE, allowed=['dep-45'])],
     [CI('hyper', 'حساسیت به GnRH، آگونیست‌های GnRH یا اجزای فرآورده.', 'Hypersensitivity to GnRH, GnRH agonists or any excipient.', [R(Lp, '4')])],
     warn=[W('افزایش گذرای تستوسترون و شعله‌ور شدن تومور (درد استخوان، فشار نخاع، انسداد ادراری) در هفته‌های اول؛ سندرم متابولیک و دیابت؛ بیماری قلبی‌عروقی؛ طولانی شدن QT؛ تشنج.', 'Transient testosterone surge and tumour flare (bone pain, spinal cord compression, urinary obstruction) in the first weeks; metabolic syndrome and diabetes; cardiovascular disease; QT prolongation; convulsions.', [R(Lp, '5')])],
     exs=[ex('m1', 'dep-7-5', {'perDose': 7.5}, ageYears=70, weightKg=75), ex('m3', 'dep-22-5', {'perDose': 22.5}, ageYears=70, weightKg=75), ex('m4', 'dep-30', {'perDose': 30}, ageYears=70, weightKg=75), ex('m6', 'dep-45', {'perDose': 45}, ageYears=70, weightKg=75)])

Zx = fda('zoladex', 'FDA Zoladex 3.6', 'Zoladex (goserelin implant) 3.6 mg — Prescribing Information', sid('goserelin'))
drug('goserelin', 'antineoplastic-immunomodulating', 'گوسرلین', 'Goserelin', T('آگونیست GnRH (ایمپلنت)', 'GnRH agonist (implant)'), [{'name': 'Zoladex', 'market': 'US'}], ['zoladex', 'زولادکس', 'گوسرلین'],
     [form('impl-3-6', 'injection', 'sc', '3.6 mg implant in prefilled syringe', 3.6, 'mg', [R(Zx, '3')], per='application')],
     [reg('pca', 'prostate-cancer', T('سرطان پروستات — ۳٫۶ mg زیرجلد شکم هر ۲۸ روز', 'Prostate cancer — 3.6 mg SC into the abdominal wall every 28 days'), A18, 'fixed', {'perDose': 3.6, 'dosesPerDay': 1}, [R(Zx, '2'), R(Zx, '2.2')], dur=ONE,
          notes=[note('همراه رادیوتراپی و فلوتامید (T2b-T4): ۸ هفته پیش از رادیوتراپی شروع شود.', 'With radiotherapy and flutamide (T2b–T4): start 8 weeks before radiotherapy.', [R(Zx, '2.1')])]),
      reg('bca', 'breast-cancer', T('سرطان پیشرفته پستان — ۳٫۶ mg زیرجلد هر ۲۸ روز', 'Advanced breast cancer — 3.6 mg SC every 28 days'), A18, 'fixed', {'perDose': 3.6, 'dosesPerDay': 1}, [R(Zx, '2'), R(Zx, '2.5')], dur=ONE),
      reg('endo', 'endometriosis', T('اندومتریوز — ۳٫۶ mg زیرجلد هر ۲۸ روز، ۶ ماه', 'Endometriosis — 3.6 mg SC every 28 days for 6 months'), A18, 'fixed', {'perDose': 3.6, 'dosesPerDay': 1}, [R(Zx, '2'), R(Zx, '2.3')], dur=ONE,
          notes=[note('بیش از ۶ ماه و درمان مجدد توصیه نمی‌شود (داده ایمنی نیست). نازک کردن آندومتر پیش از ابلیشن: ۱ یا ۲ دوز با ۴ هفته فاصله.', 'Not beyond 6 months and no retreatment (no safety data). Endometrial thinning before ablation: 1 or 2 depots 4 weeks apart.', [R(Zx, '2.3'), R(Zx, '2.4')])])],
     [CI('ci', 'حساسیت؛ بارداری مگر برای درمان سرطان پیشرفته پستان.', 'Hypersensitivity; pregnancy unless used for advanced breast cancer.', [R(Zx, '4')])],
     warn=[W('پیش از شروع بارداری رد شود و پیشگیری غیرهورمونی؛ شعله‌ور شدن تومور؛ هیپرگلیسمی؛ بیماری قلبی‌عروقی؛ هیپرکلسمی؛ QT؛ آسیب محل تزریق (عروق اپی‌گاستریک)؛ افسردگی.', 'Exclude pregnancy and use non-hormonal contraception; tumour flare; hyperglycaemia; cardiovascular disease; hypercalcaemia; QT; injection-site injury (epigastric vessels); depression.', [R(Zx, '5')])],
     exs=[ex('pca', 'impl-3-6', {'perDose': 3.6}, ageYears=70, weightKg=75), ex('bca', 'impl-3-6', {'perDose': 3.6}, ageYears=50, weightKg=65), ex('endo', 'impl-3-6', {'perDose': 3.6}, ageYears=30, weightKg=60)])

Fm = fda('firmagon', 'FDA Firmagon', 'Firmagon (degarelix) for injection — Prescribing Information', sid('degarelix'))
drug('degarelix', 'antineoplastic-immunomodulating', 'دگارلیکس', 'Degarelix', T('آنتاگونیست GnRH', 'GnRH antagonist'), [{'name': 'Firmagon', 'market': 'US'}], ['firmagon', 'فیرماگون', 'دگارلیکس'],
     [vial('vial-120', 120, '120 mg vial (starting dose = 2 vials)', Fm), vial('vial-80', 80, '80 mg vial (maintenance)', Fm)],
     [reg('start', 'prostate-cancer', T('سرطان پیشرفته پروستات — شروع ۲۴۰ mg (دو تزریق ۱۲۰ mg زیرجلد شکم)', 'Advanced prostate cancer — start 240 mg (two 120 mg SC abdominal injections)'), A18, 'fixed', {'perDose': 240, 'dosesPerDay': 1}, [R(Fm, '2.1')], dur=ONE, allowed=['vial-120']),
      reg('maint', 'prostate-cancer', T('نگهدارنده — ۸۰ mg زیرجلد هر ۲۸ روز (اولین ۲۸ روز پس از شروع)', 'Maintenance — 80 mg SC every 28 days (first 28 days after the starting dose)'), A18, 'fixed', {'perDose': 80, 'dosesPerDay': 1}, [R(Fm, '2.1')], dur=ONE, allowed=['vial-80'])],
     [CI('hyper', 'سابقه حساسیت شدید به دگارلیکس.', 'History of severe hypersensitivity to degarelix.', [R(Fm, '4')])],
     warn=[W('واکنش حساسیتی؛ طولانی شدن QT؛ سمیت جنینی.', 'Hypersensitivity reactions; QT prolongation; embryo-fetal toxicity.', [R(Fm, '5')])],
     exs=[ex('start', 'vial-120', {'perDose': 240}, ageYears=70, weightKg=75), ex('maint', 'vial-80', {'perDose': 80}, ageYears=70, weightKg=75)])

Sg = fda('signifor', 'FDA Signifor', 'Signifor (pasireotide) injection — Prescribing Information', sid('pasireotide'))
drug('pasireotide', 'systemic-hormones', 'پاسیرئوتید', 'Pasireotide', T('آنالوگ سوماتوستاتین', 'Somatostatin analogue'), [{'name': 'Signifor', 'market': 'US'}], ['signifor', 'سیگنیفور', 'پاسیرئوتید'],
     [sol('amp-0-3', 0.3, 1, '0.3 mg/mL ampule', Sg), sol('amp-0-6', 0.6, 1, '0.6 mg/mL ampule', Sg), sol('amp-0-9', 0.9, 1, '0.9 mg/mL ampule', Sg)],
     [reg('cush', 'cushing-disease', T('بیماری کوشینگ (جراحی ناممکن یا ناموفق) — ۰٫۶ یا ۰٫۹ mg زیرجلد دو بار در روز', 'Cushing disease (surgery not an option or failed) — 0.6 or 0.9 mg SC twice daily'), A18, 'fixed', {'perDose': 0.6, 'perDoseMax': 0.9, 'dosesPerDay': 2}, [R(Sg, '2.1')],
          notes=[note('محدوده ۰٫۳ تا ۰٫۹ mg دو بار؛ تیتراسیون با کورتیزول ادرار. پیش از شروع: قند ناشتا، HbA1c، کبد، ECG، سونوگرافی کیسه صفرا، پتاسیم و منیزیم. Child-Pugh B: شروع ۰٫۳، حداکثر ۰٫۶ mg دو بار؛ Child-Pugh C پرهیز.', 'Range 0.3–0.9 mg twice daily; titrate by urinary free cortisol. Before starting: FPG, HbA1c, liver tests, ECG, gallbladder ultrasound, potassium and magnesium. Child-Pugh B: start 0.3, max 0.6 mg twice daily; avoid in Child-Pugh C.', [R(Sg, '2.1'), R(Sg, '2.2'), R(Sg, '2.3')])])],
     warn=[W('کمبود کورتیزول؛ هیپرگلیسمی و دیابت (شایع)؛ برادیکاردی و QT؛ افزایش آنزیم کبد؛ سنگ صفرا؛ کمبود سایر هورمون‌های هیپوفیز.', 'Hypocortisolism; hyperglycaemia and diabetes (common); bradycardia and QT prolongation; liver test elevations; cholelithiasis; deficiency of other pituitary hormones.', [R(Sg, '5')])],
     exs=[ex('cush', 'amp-0-6', {'perDose': 0.6, 'mlPerDose': 1}, ageYears=40, weightKg=70)])

Zp = fda('zemplar-iv', 'FDA Zemplar injection', 'Zemplar (paricalcitol) injection — Prescribing Information', sid('paricalcitol'))
drug('paricalcitol', 'systemic-hormones', 'پاری‌کلسیتول', 'Paricalcitol', T('آنالوگ ویتامین D فعال', 'Active vitamin D analogue'), [{'name': 'Zemplar', 'market': 'US'}], ['zemplar', 'زمپلار', 'پاریکلسیتول'],
     [sol('vial-5', 5, 1, '5 mcg/mL vial', Zp, unit='mcg', route='iv'), sol('vial-2', 2, 1, '2 mcg/mL vial', Zp, unit='mcg', route='iv')],
     [once('hd', 'secondary-hyperparathyroidism-ckd', 'هیپرپاراتیروئیدی ثانویه در CKD مرحله ۵ (دیالیز) — بولوس وریدی ۰٫۰۴ تا ۰٫۱ mcg/kg حداکثر یک روز در میان حین دیالیز', 'Secondary hyperparathyroidism in CKD stage 5 (dialysis) — IV bolus 0.04–0.1 mcg/kg no more often than every other day during dialysis', A18, 0.04, 0.1, [R(Zp, '2.2')], unit='mcg',
           notes=[note('پیش از شروع کلسیم بالاتر از حد طبیعی نباشد. کلسیم دو بار در هفته و PTH هر ۲ تا ۴ هفته؛ تیتراسیون با جدول ۱. حداکثر ۰٫۲۴ mcg/kg.', 'Calcium must not be above normal before starting. Calcium twice weekly and PTH every 2–4 weeks; titrate per Table 1. Max 0.24 mcg/kg.', [R(Zp, '2.1'), R(Zp, '2.2')])])],
     [CI('ci', 'هیپرکلسمی؛ مسمومیت با ویتامین D؛ حساسیت به پاری‌کلسیتول.', 'Hypercalcaemia; vitamin D toxicity; hypersensitivity to paricalcitol.', [R(Zp, '4')])],
     warn=[W('هیپرکلسمی؛ تشدید مسمومیت دیژیتال با هیپرکلسمی؛ بیماری استخوان آدینامیک با سرکوب بیش از حد PTH.', 'Hypercalcaemia; digitalis toxicity potentiated by hypercalcaemia; adynamic bone disease with PTH over-suppression.', [R(Zp, '5')])],
     exs=[ex('hd', 'vial-5', {'perDose': 2.8, 'mlPerDose': 0.56, 'upperPerDose': 7}, ageYears=55, weightKg=70)])

# ===================== diabetes / glucose =====================
Iv = fda('invokana', 'FDA Invokana', 'Invokana (canagliflozin) tablets — Prescribing Information', sid('canagliflozin'))
SGLT = lambda src: W('کتواسیدوز (حتی با قند نه‌چندان بالا)؛ قطع عضو تحتانی؛ کاهش حجم؛ عفونت ادراری-تناسلی و گانگرن فورنیه؛ هیپوگلیسمی با انسولین یا سولفونیل‌اوره.', 'Ketoacidosis (even with modest glucose); lower-limb amputation; volume depletion; genitourinary infections incl. urosepsis; hypoglycaemia with insulin or sulfonylureas.', [R(src, '5')])
drug('canagliflozin', 'alimentary-metabolism', 'کاناگلیفلوزین', 'Canagliflozin', T('مهارکننده SGLT2', 'SGLT2 inhibitor'), [{'name': 'Invokana', 'market': 'US'}], ['invokana', 'اینووکانا', 'کاناگلیفلوزین'],
     [tab('tab-100', 100, '100 mg tablet', [R(Iv, '3')]), tab('tab-300', 300, '300 mg tablet', [R(Iv, '3')])],
     [reg('t2dm', 'type-2-diabetes', T('دیابت نوع ۲ (بزرگسال و کودک ۱۰ سال به بالا) — ۱۰۰ mg یک بار پیش از اولین وعده؛ تا ۳۰۰ mg اگر eGFR ۶۰ به بالا', 'Type 2 diabetes (adults and children ≥10 y) — 100 mg once daily before the first meal; up to 300 mg if eGFR ≥60'), {'minAge': age(10, 'year')}, 'fixed', {'perDose': 100, 'perDoseMax': 300, 'dosesPerDay': 1}, [R(Iv, '2.2')],
          notes=[note('پیش از شروع کمبود حجم اصلاح شود. دست‌کم ۳ روز پیش از جراحی قطع. با القاگر UGT (ریفامپین، فنی‌توئین…) افزایش به ۲۰۰ mg.', 'Correct volume depletion first. Withhold ≥3 days before surgery. With UGT inducers (rifampin, phenytoin…) increase to 200 mg.', [R(Iv, '2.1'), R(Iv, '2.5'), R(Iv, '2.4')])]),
      reg('ckd', 'diabetic-nephropathy', T('کاهش خطر قلبی‌عروقی و نفروپاتی دیابتی با آلبومینوری — ۱۰۰ mg یک بار', 'Cardiovascular risk and diabetic nephropathy with albuminuria — 100 mg once daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Iv, '2.2'), R(Iv, '2.3')])],
     [CI('hyper', 'واکنش حساسیتی جدی به کاناگلیفلوزین (آنافیلاکسی، آنژیوادم).', 'Serious hypersensitivity to canagliflozin (anaphylaxis, angioedema).', [R(Iv, '4')])],
     warn=[SGLT(Iv), W('شکستگی استخوان.', 'Bone fracture.', [R(Iv, '5.7')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('eGFR ۳۰ تا <۶۰: حداکثر ۱۰۰ mg. زیر ۳۰: شروع توصیه نمی‌شود (با آلبومینوری >۳۰۰ mg/روز ادامه ۱۰۰ mg مجاز).', 'eGFR 30–<60: max 100 mg. Below 30: initiation not recommended (may continue 100 mg if albuminuria >300 mg/day).'), 'refs': [R(Iv, '2.3')]}],
     exs=[ex('t2dm', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1, 'upperPerDose': 300}, ageYears=55, weightKg=80), ex('ckd', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80)])

St = fda('steglatro', 'FDA Steglatro', 'Steglatro (ertugliflozin) tablets — Prescribing Information', sid('ertugliflozin'))
drug('ertugliflozin', 'alimentary-metabolism', 'ارتوگلیفلوزین', 'Ertugliflozin', T('مهارکننده SGLT2', 'SGLT2 inhibitor'), [{'name': 'Steglatro', 'market': 'US'}], ['steglatro', 'استگلاترو', 'ارتوگلیفلوزین'],
     [tab('tab-5', 5, '5 mg tablet', [R(St, '3')]), tab('tab-15', 15, '15 mg tablet', [R(St, '3')])],
     [reg('t2dm', 'type-2-diabetes', T('دیابت نوع ۲ بزرگسال — ۵ mg صبح؛ تا ۱۵ mg یک بار', 'Type 2 diabetes, adults — 5 mg in the morning; up to 15 mg once daily'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 15, 'dosesPerDay': 1}, [R(St, '2.2')],
          notes=[note('پیش از شروع کمبود حجم اصلاح شود. دست‌کم ۴ روز پیش از جراحی قطع.', 'Correct volume depletion first. Withhold ≥4 days before surgery.', [R(St, '2.1'), R(St, '2.3')])])],
     [CI('hyper', 'حساسیت به ارتوگلیفلوزین.', 'Hypersensitivity to ertugliflozin.', [R(St, '4')])], warn=[SGLT(St)],
     renal=[{'egfrBelow': 45, 'severity': 'block', 'text': T('eGFR زیر ۴۵: توصیه نمی‌شود.', 'eGFR <45: not recommended.'), 'refs': [R(St, '2.2')]}],
     exs=[ex('t2dm', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 15}, ageYears=55, weightKg=80)])

By = fda('byetta', 'FDA Byetta', 'Byetta (exenatide) injection — Prescribing Information', sid('exenatide'))
drug('exenatide', 'alimentary-metabolism', 'اگزناتاید', 'Exenatide', T('آگونیست گیرنده GLP-1', 'GLP-1 receptor agonist'), [{'name': 'Byetta', 'market': 'US'}], ['byetta', 'بایتا', 'اگزناتید', 'اکسناتاید'],
     [sol('pen-250', 250, 1, '250 mcg/mL prefilled pen (5 or 10 mcg per dose)', By, unit='mcg')],
     [reg('t2dm', 'type-2-diabetes', T('دیابت نوع ۲ — ۵ mcg زیرجلدی دو بار در روز ظرف ۶۰ دقیقه پیش از صبحانه و شام؛ پس از ۱ ماه تا ۱۰ mcg', 'Type 2 diabetes — 5 mcg SC twice daily within 60 min before morning and evening meals; 10 mcg after 1 month'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(By, '2.1')], unit='mcg',
          notes=[note('پس از غذا تزریق نشود. قلم بین بیماران مشترک نشود.', 'Do not inject after a meal. Never share a pen between patients.', [R(By, '2.1'), R(By, '5.2')])])],
     [CI('ci', 'حساسیت شدید قبلی به اگزناتاید؛ سابقه ترومبوسیتوپنی ایمنی ناشی از فرآورده‌های اگزناتاید.', 'Prior severe hypersensitivity to exenatide; history of drug-induced immune-mediated thrombocytopenia from exenatide products.', [R(By, '4')])],
     warn=[W('پانکراتیت حاد؛ هیپوگلیسمی با سولفونیل‌اوره یا انسولین؛ آسیب حاد کلیه با کاهش حجم؛ عوارض شدید گوارشی؛ ترومبوسیتوپنی؛ بیماری کیسه صفرا؛ آسپیراسیون ریوی حین بیهوشی.', 'Acute pancreatitis; hypoglycaemia with sulfonylureas or insulin; acute kidney injury from volume depletion; severe GI reactions; thrombocytopenia; gallbladder disease; pulmonary aspiration during anaesthesia.', [R(By, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'block', 'text': T('ClCr زیر ۳۰ یا ESRD: توصیه نمی‌شود.', 'CrCl <30 or ESRD: not recommended.'), 'refs': [R(By, '8.6')]}],
     exs=[ex('t2dm', 'pen-250', {'perDose': 5, 'mlPerDose': 0.02, 'upperPerDose': 10}, ageYears=55, weightKg=90)])

Sy = fda('symlin', 'FDA Symlin', 'Symlin (pramlintide) injection — Prescribing Information', sid('pramlintide'))
PRM = lambda: note('هنگام شروع، انسولین وعده ۵۰٪ کم شود. فقط پیش از وعده اصلی (≥۲۵۰ kcal یا ≥۳۰ g کربوهیدرات)، شکم یا ران، جدا از انسولین. دست‌کم ۳ روز بین افزایش‌ها.', 'On initiation reduce mealtime insulin by 50%. Only before major meals (≥250 kcal or ≥30 g carbohydrate), abdomen or thigh, separate from insulin. At least 3 days between titration steps.', [R(Sy, '2.1'), R(Sy, '2.4')])
drug('pramlintide', 'alimentary-metabolism', 'پراملینتاید', 'Pramlintide', T('آنالوگ آمیلین', 'Amylin analogue'), [{'name': 'Symlin', 'market': 'US'}], ['symlin', 'سیملین', 'پراملینتید'],
     [sol('pen-1000', 1000, 1, '1000 mcg/mL SymlinPen (dial the mcg dose on the pen; do not measure by mL)', Sy, unit='mcg')],
     [reg('t2', 'type-2-diabetes', T('دیابت نوع ۲ با انسولین وعده — ۶۰ mcg پیش از هر وعده اصلی؛ تا ۱۲۰ mcg', 'Type 2 diabetes on mealtime insulin — 60 mcg before each major meal; up to 120 mcg'), A18, 'fixed', {'perDose': 60, 'perDoseMax': 120, 'dosesPerDay': 1}, [R(Sy, '2.2')], unit='mcg', dur=ONE, notes=[PRM()]),
      reg('t1', 'type-1-diabetes', T('دیابت نوع ۱ — ۱۵ mcg پیش از هر وعده اصلی؛ با گام ۱۵ تا ۳۰ (حداکثر ۶۰) mcg', 'Type 1 diabetes — 15 mcg before each major meal; steps of 15 to 30 (max 60) mcg'), A18, 'fixed', {'perDose': 15, 'perDoseMax': 60, 'dosesPerDay': 1}, [R(Sy, '2.3')], unit='mcg', dur=ONE, notes=[PRM()])],
     [CI('ci', 'حساسیت جدی؛ عدم درک هیپوگلیسمی؛ گاستروپارزی تأییدشده.', 'Serious hypersensitivity; hypoglycaemia unawareness; confirmed gastroparesis.', [R(Sy, '4')])],
     warn=[W('هشدار جعبه‌ای: هیپوگلیسمی شدید با انسولین، به‌ویژه دیابت نوع ۱، ظرف ۳ ساعت پس از تزریق. هرگز با انسولین مخلوط نشود.', 'Boxed warning: severe hypoglycaemia with insulin, especially type 1, within 3 h of injection. Never mix with insulin.', [R(Sy, 'Boxed Warning'), R(Sy, '5.4')])],
     exs=[ex('t2', 'pen-1000', {'perDose': 60, 'mlPerDose': 0.06, 'upperPerDose': 120}, ageYears=55, weightKg=90), ex('t1', 'pen-1000', {'perDose': 15, 'upperPerDose': 60}, ageYears=30, weightKg=70)])

Pg = fda('proglycem', 'FDA Proglycem', 'Proglycem (diazoxide) oral suspension 50 mg/mL — Prescribing Information', sid('diazoxide')); d = R(Pg, 'Dosage and Administration')
drug('diazoxide', 'various', 'دیازوکساید', 'Diazoxide', T('مهارکننده ترشح انسولین', 'Insulin-secretion inhibitor'), [{'name': 'Proglycem', 'market': 'US'}], ['proglycem', 'پروگلایسم', 'دیازوکسید'],
     [liquid('susp-50', 50, 1, '50 mg/mL oral suspension', [R(Pg, 'How Supplied')])],
     [reg('std', 'hypoglycemia', T('هیپوگلیسمی ناشی از هیپرانسولینیسم (بزرگسال و کودک) — شروع ۳ mg/kg/روز در ۳ دوز هر ۸ ساعت؛ حداکثر ۸', 'Hyperinsulinaemic hypoglycaemia (adults and children) — start 3 mg/kg/day in 3 doses every 8 h; max 8'), {'minAge': age(1, 'year')}, 'weightBased', {'perKgPerDay': 3, 'perKgPerDayMax': 8, 'dividedDoses': 3}, [d],
          notes=[note('یا در ۲ دوز هر ۱۲ ساعت. اگر پس از ۲ تا ۳ هفته مؤثر نبود قطع شود.', 'Or in 2 doses every 12 h. Stop if ineffective after 2–3 weeks.', [d])]),
      reg('infant', 'hypoglycemia', T('شیرخوار و نوزاد — شروع ۸ mg/kg/روز در ۳ دوز هر ۸ ساعت؛ حداکثر ۱۵', 'Infants and newborns — start 8 mg/kg/day in 3 doses every 8 h; max 15'), {'maxAge': age(1, 'year')}, 'weightBased', {'perKgPerDay': 8, 'perKgPerDayMax': 15, 'dividedDoses': 3}, [d],
          notes=[note('دقت دوز در شیرخوار بسیار مهم است. فشار ریوی (PH) در نوزاد گزارش شده.', 'Dose accuracy is critical in infants. Pulmonary hypertension has been reported in newborns.', [d, R(Pg, 'Warnings')])])],
     [CI('ci', 'هیپوگلیسمی عملکردی؛ حساسیت به دیازوکساید یا تیازیدها.', 'Functional hypoglycaemia; hypersensitivity to diazoxide or other thiazides.', [R(Pg, 'Contraindications')])],
     warn=[W('احتباس مایع و نارسایی قلب؛ کتواسیدوز و کمای هیپراسمولار؛ با تیازید افزایش قند و اسید اوریک.', 'Fluid retention and heart failure; ketoacidosis and hyperosmolar coma; thiazides potentiate hyperglycaemia and hyperuricaemia.', [R(Pg, 'Warnings')])],
     exs=[ex('std', 'susp-50', {'perDose': 20, 'mlPerDose': 0.4, 'upperPerDose': 53.33}, ageYears=6, weightKg=20), ex('infant', 'susp-50', {'perDose': 16, 'mlPerDose': 0.32, 'upperPerDose': 30}, ageMonths=4, weightKg=6)])

# ===================== haematology =====================
Ar = fda('aranesp', 'FDA Aranesp', 'Aranesp (darbepoetin alfa) injection — Prescribing Information', sid('darbepoetin'))
drug('darbepoetin', 'blood', 'داربپوئتین آلفا', 'Darbepoetin alfa', T('محرک خون‌سازی (ESA) طولانی‌اثر', 'Long-acting erythropoiesis-stimulating agent'), [{'name': 'Aranesp', 'market': 'US'}], ['aranesp', 'آرانسپ', 'داربپوئتین'],
     [sol('syr-40', 40, 0.4, '40 mcg/0.4 mL prefilled syringe', Ar, unit='mcg'), sol('syr-100', 100, 0.5, '100 mcg/0.5 mL prefilled syringe', Ar, unit='mcg'), sol('syr-500', 500, 1, '500 mcg/1 mL prefilled syringe', Ar, unit='mcg')],
     [once('dial', 'anemia-ckd', 'کم‌خونی CKD روی دیالیز — شروع ۰٫۴۵ mcg/kg هفتگی (یا ۰٫۷۵ هر ۲ هفته)، وریدی ترجیحاً', 'CKD anaemia on dialysis — start 0.45 mcg/kg weekly (or 0.75 every 2 weeks), IV preferred', A18, 0.45, None, [R(Ar, '2.2')], unit='mcg',
           notes=[note('هموگلوبین را بالای ۱۱ g/dL هدف نگیرید؛ کمترین دوز برای کاهش تزریق خون. پیش از شروع آهن (فریتین <۱۰۰ یا اشباع <۲۰٪ مکمل).', 'Do not target haemoglobin >11 g/dL; lowest dose to reduce transfusions. Check iron first (supplement if ferritin <100 or saturation <20%).', [R(Ar, '2.2'), R(Ar, '2.1')])]),
      once('nondial', 'anemia-ckd', 'کم‌خونی CKD بدون دیالیز — شروع ۰٫۴۵ mcg/kg هر ۴ هفته', 'CKD anaemia not on dialysis — start 0.45 mcg/kg every 4 weeks', A18, 0.45, None, [R(Ar, '2.2')], unit='mcg'),
      once('child', 'anemia-ckd', 'کودک با CKD — شروع ۰٫۴۵ mcg/kg هفتگی (بدون دیالیز: یا ۰٫۷۵ هر ۲ هفته)', 'Children with CKD — start 0.45 mcg/kg weekly (not on dialysis: or 0.75 every 2 weeks)', {'maxAge': age(18, 'year')}, 0.45, None, [R(Ar, '2')], unit='mcg'),
      once('chemo', 'chemotherapy-induced-anemia', 'کم‌خونی ناشی از شیمی‌درمانی (Hb <۱۰) — ۲٫۲۵ mcg/kg زیرجلدی هفتگی', 'Chemotherapy-induced anaemia (Hb <10) — 2.25 mcg/kg SC weekly', A18, 2.25, None, [R(Ar, '2.3')], unit='mcg',
           notes=[note('یا ۵۰۰ mcg هر ۳ هفته. فقط اگر دست‌کم ۲ ماه شیمی‌درمانی باقی است؛ تا پایان دوره.', 'Or 500 mcg every 3 weeks. Only with ≥2 more months of planned chemotherapy; until the course ends.', [R(Ar, '2.3')])])],
     [CI('ci', 'فشار خون کنترل‌نشده؛ آپلازی خالص گلبول قرمز پس از ESA؛ واکنش آلرژیک جدی.', 'Uncontrolled hypertension; pure red cell aplasia after ESA therapy; serious allergic reactions.', [R(Ar, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ، MI، سکته، ترومبوز و رشد تومور؛ در سرطان فقط کم‌خونی ناشی از شیمی‌درمانی میلوساپرسیو، نه درمان علاج‌بخش. فشار خون؛ تشنج.', 'Boxed warning: increased death, MI, stroke, thrombosis and tumour progression; in cancer only for myelosuppressive-chemotherapy anaemia, not curative intent. Hypertension; seizures.', [R(Ar, 'Boxed Warning'), R(Ar, '5')])],
     exs=[ex('dial', 'syr-40', {'perDose': 31.5, 'mlPerDose': 0.32}, ageYears=60, weightKg=70), ex('nondial', 'syr-40', {'perDose': 31.5, 'mlPerDose': 0.32}, ageYears=60, weightKg=70),
          ex('child', 'syr-40', {'perDose': 9, 'mlPerDose': 0.09}, ageYears=6, weightKg=20), ex('chemo', 'syr-500', {'perDose': 157.5, 'mlPerDose': 0.32}, ageYears=55, weightKg=70)])

Cy = fda('cyanocobalamin', 'FDA Cyanocobalamin inj', 'Cyanocobalamin injection 1000 mcg/mL (American Regent/BluePoint) — Prescribing Information', sid('cyanocobalamin')); d = R(Cy, 'Dosage and Administration')
drug('cyanocobalamin', 'blood', 'سیانوکوبالامین (ویتامین B12)', 'Cyanocobalamin (vitamin B12)', T('ویتامین B12', 'Vitamin B12'), [{'name': 'Cyanocobalamin', 'market': 'US'}], ['vitamin b12', 'ویتامین ب۱۲', 'ب 12', 'B12', 'سیانوکوبالامین'],
     [sol('amp-1000', 1000, 1, '1000 mcg/mL injection', Cy, unit='mcg', route='im', sec='How Supplied')],
     [reg('pa', 'b12-deficiency', T('کم‌خونی پرنیشیوز — ۱۰۰ mcg عضلانی یا زیرجلدی عمقی روزانه ۶ تا ۷ روز', 'Pernicious anaemia — 100 mcg IM or deep SC daily for 6–7 days'), {}, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [d], unit='mcg', dur={'min': 6, 'max': 7},
          notes=[note('اگر پاسخ رتیکولوسیت: همان دوز یک روز در میان ۷ دوز، سپس هر ۳ تا ۴ روز ۲ تا ۳ هفته، سپس ۱۰۰ mcg ماهانه مادام‌العمر. وریدی نه (دفع ادراری). در صورت نیاز اسید فولیک.', 'If reticulocyte response: same dose on alternate days for 7 doses, then every 3–4 days for 2–3 weeks, then 100 mcg monthly for life. Not IV (lost in urine). Folic acid if needed.', [d])])],
     [CI('ci', 'حساسیت به کبالت یا ویتامین B12.', 'Sensitivity to cobalt and/or vitamin B12.', [R(Cy, 'Contraindications')])],
     warn=[W('بیماری لبر (آتروفی سریع عصب بینایی)؛ هیپوکالمی و مرگ ناگهانی در درمان شدید کم‌خونی مگالوبلاستیک؛ آنافیلاکسی (تست داخل‌جلدی در مشکوک)؛ بنزیل الکل در نوزاد نارس.', "Leber's disease (rapid optic atrophy); hypokalaemia and sudden death with intensive treatment of severe megaloblastic anaemia; anaphylaxis (intradermal test if suspected); benzyl alcohol in premature infants.", [R(Cy, 'Warnings')])],
     exs=[ex('pa', 'amp-1000', {'perDose': 100, 'mlPerDose': 0.1}, ageYears=60, weightKg=70)])

Pm = fda('promacta', 'FDA Promacta', 'Promacta (eltrombopag) tablets and oral suspension — Prescribing Information', sid('eltrombopag'))
ELT = lambda: note('ناشتا یا با غذای کم‌کلسیم؛ ۲ ساعت قبل یا ۴ ساعت بعد از آنتی‌اسید، لبنیات و مکمل‌های آهن/کلسیم/روی.', 'Fasting or with a low-calcium meal; 2 h before or 4 h after antacids, dairy and iron/calcium/zinc supplements.', [R(Pm, '2.4')])
drug('eltrombopag', 'blood', 'التروم‌بوپاگ', 'Eltrombopag', T('آگونیست گیرنده ترومبوپویتین', 'Thrombopoietin receptor agonist'), [{'name': 'Promacta', 'market': 'US'}], ['promacta', 'پروماکتا', 'revolade', 'رevolade', 'التromبوپاگ', 'التروم بوپاگ'],
     [tab('tab-12-5', 12.5, '12.5 mg tablet', [R(Pm, '3')]), tab('tab-25', 25, '25 mg tablet', [R(Pm, '3')]), tab('tab-50', 50, '50 mg tablet', [R(Pm, '3')]), tab('tab-75', 75, '75 mg tablet', [R(Pm, '3')])],
     [reg('itp', 'immune-thrombocytopenia', T('ITP مزمن (بزرگسال و کودک ۶ سال به بالا) — شروع ۵۰ mg یک بار', 'Chronic ITP (adults and children ≥6 y) — start 50 mg once daily'), {'minAge': age(6, 'year')}, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Pm, '2.1')],
          limits={'maxPerDay': 75, 'refs': [R(Pm, '2.1')]}, notes=[note('تبار آسیای شرقی یا نارسایی کبد: شروع ۲۵ mg. هدف پلاکت ≥۵۰ هزار، نه طبیعی کردن.', 'East-/Southeast-Asian ancestry or hepatic impairment: start 25 mg. Target platelets ≥50×10⁹/L, not normalisation.', [R(Pm, '2.1')]), ELT()]),
      reg('itp-young', 'immune-thrombocytopenia', T('ITP — کودک ۱ تا ۵ سال: شروع ۲۵ mg یک بار', 'ITP — children 1–5 y: start 25 mg once daily'), {'minAge': age(1, 'year'), 'maxAge': age(6, 'year')}, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Pm, '2')], limits={'maxPerDay': 75, 'refs': [R(Pm, '2')]}),
      reg('hcv', 'hepatitis-c', T('ترومبوسیتوپنی هپاتیت C (برای شروع اینترفرون) — شروع ۲۵ mg یک بار', 'Hepatitis C thrombocytopenia (to start interferon) — start 25 mg once daily'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Pm, '2.2')], limits={'maxPerDay': 100, 'refs': [R(Pm, '2')]}),
      reg('saa12', 'aplastic-anemia', T('آنمی آپلاستیک شدید خط اول (۱۲ سال به بالا) — ۱۵۰ mg یک بار، ۶ ماه همراه درمان سرکوب ایمنی', 'First-line severe aplastic anaemia (≥12 y) — 150 mg once daily for 6 months with immunosuppressive therapy'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 150, 'dosesPerDay': 1}, [R(Pm, '2.3, Table 3')],
          notes=[note('از دوز اولیه بالاتر نرود. تبار آسیای شرقی دوز کمتر طبق جدول.', 'Do not exceed the initial dose. East-/Southeast-Asian ancestry: reduced dose per table.', [R(Pm, '2.3')])]),
      reg('saa6', 'aplastic-anemia', T('آنمی آپلاستیک شدید — کودک ۶ تا ۱۱ سال: ۷۵ mg یک بار، ۶ ماه', 'Severe aplastic anaemia — children 6–11 y: 75 mg once daily for 6 months'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 75, 'dosesPerDay': 1}, [R(Pm, '2.3, Table 3')]),
      reg('saa2', 'aplastic-anemia', T('آنمی آپلاستیک شدید — کودک ۲ تا ۵ سال: ۲٫۵ mg/kg یک بار، ۶ ماه', 'Severe aplastic anaemia — children 2–5 y: 2.5 mg/kg once daily for 6 months'), {'minAge': age(2, 'year'), 'maxAge': age(6, 'year')}, 'weightBased', {'perKgPerDose': 2.5, 'intervalHours': 24}, [R(Pm, '2.3, Table 3')])],
     warn=[W('هشدار جعبه‌ای: جبران‌ناپذیری کبد در هپاتیت C با اینترفرون/ریباویرین؛ سمیت کبدی — آزمایش کبد پایش شود.', 'Boxed warning: hepatic decompensation in hepatitis C with interferon/ribavirin; hepatotoxicity — monitor liver tests.', [R(Pm, 'Boxed Warning')]),
           W('ترومبوز؛ آب مروارید؛ خطر پیشرفت MDS.', 'Thrombotic events; cataracts; risk of MDS progression.', [R(Pm, '5')])],
     exs=[ex('itp', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('itp-young', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=3, weightKg=14),
          ex('hcv', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('saa12', 'tab-75', {'perDose': 150, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70),
          ex('saa6', 'tab-75', {'perDose': 75, 'tabletsPerDoseRounded': 1}, ageYears=8, weightKg=25), ex('saa2', 'tab-12-5', {'perDose': 37.5, 'tabletsPerDoseRounded': 3}, ageYears=4, weightKg=15)])

Np = fda('nplate', 'FDA Nplate', 'Nplate (romiplostim) for injection — Prescribing Information', sid('romiplostim'))
drug('romiplostim', 'blood', 'رومی‌پلوستیم', 'Romiplostim', T('آگونیست گیرنده ترومبوپویتین', 'Thrombopoietin receptor agonist'), [{'name': 'Nplate', 'market': 'US'}], ['nplate', 'ان‌پلیت', 'رومیپلوستیم'],
     [vial('vial-250', 250, '250 mcg vial', Np, unit='mcg'), vial('vial-125', 125, '125 mcg vial', Np, unit='mcg'), vial('vial-500', 500, '500 mcg vial', Np, unit='mcg')],
     [once('itp', 'immune-thrombocytopenia', 'ITP بزرگسال — شروع ۱ mcg/kg زیرجلدی هفتگی', 'Adult ITP — start 1 mcg/kg SC once weekly', A18, 1, None, [R(Np, '2.1')], unit='mcg',
           notes=[note('هفتگی ۱ mcg/kg افزایش تا پلاکت ≥۵۰ هزار؛ حداکثر ۱۰ mcg/kg/هفته؛ وزن واقعی شروع. سرنگ با درجه ۰٫۰۱ mL. اگر پس از ۴ هفته با حداکثر دوز پاسخ نبود قطع.', 'Increase weekly by 1 mcg/kg until platelets ≥50×10⁹/L; max 10 mcg/kg/week; use actual body weight at initiation. Syringe with 0.01 mL graduations. Stop if no response after 4 weeks at max dose.', [R(Np, '2.1'), R(Np, '2.3')])]),
      once('ars', 'acute-radiation-syndrome', 'پرتوگیری حاد با دوز سرکوب‌کننده مغز استخوان — ۱۰ mcg/kg زیرجلدی یک بار، هرچه زودتر', 'Acute exposure to myelosuppressive radiation — 10 mcg/kg SC once, as soon as possible', {}, 10, None, [R(Np, '2.2')], unit='mcg')],
     warn=[W('پیشرفت سندرم میلودیسپلاستیک به AML؛ ترومبوز؛ از دست رفتن پاسخ.', 'Progression of myelodysplastic syndromes to AML; thrombotic events; loss of response.', [R(Np, '5')])],
     exs=[ex('itp', 'vial-250', {'perDose': 70}, ageYears=40, weightKg=70), ex('ars', 'vial-500', {'perDose': 700}, ageYears=40, weightKg=70)])

Hm = fda('hemlibra', 'FDA Hemlibra', 'Hemlibra (emicizumab-kxwh) injection — Prescribing Information', sid('emicizumab'))
HEM = [R(Hm, '2.1')]
drug('emicizumab', 'blood', 'امیسیزوماب', 'Emicizumab', T('آنتی‌بادی دوویژه (جایگزین عملکرد فاکتور VIII)', 'Bispecific antibody (factor VIII mimetic)'), [{'name': 'Hemlibra', 'market': 'US'}], ['hemlibra', 'هملیبرا', 'امیسیزوماب'],
     [sol('vial-30', 30, 1, '30 mg/mL vial', Hm), sol('vial-150', 150, 1, '150 mg/mL vial (60 mg/0.4, 105 mg/0.7, 150 mg/1, 300 mg/2 mL)', Hm)],
     [once('load', 'hemophilia-a', 'پیشگیری هموفیلی A (همه سنین از نوزادی) — بارگذاری ۳ mg/kg زیرجلدی هفتگی ۴ هفته اول', 'Haemophilia A prophylaxis (all ages from newborn) — loading 3 mg/kg SC weekly for the first 4 weeks', {}, 3, None, HEM,
           notes=[note('مصرف پیشگیرانه داروهای بای‌پس از روز قبل قطع؛ فاکتور VIII پیشگیرانه در هفته اول قابل ادامه.', 'Stop prophylactic bypassing agents the day before starting; prophylactic factor VIII may continue in week 1.', HEM)]),
      once('w1', 'hemophilia-a', 'نگهدارنده — ۱٫۵ mg/kg هفتگی', 'Maintenance — 1.5 mg/kg once weekly', {}, 1.5, None, HEM),
      once('w2', 'hemophilia-a', 'نگهدارنده — ۳ mg/kg هر ۲ هفته', 'Maintenance — 3 mg/kg every 2 weeks', {}, 3, None, HEM),
      once('w4', 'hemophilia-a', 'نگهدارنده — ۶ mg/kg هر ۴ هفته', 'Maintenance — 6 mg/kg every 4 weeks', {}, 6, None, HEM)],
     warn=[W('هشدار جعبه‌ای: میکروآنژیوپاتی ترومبوتیک و ترومبوز با aPCC (بیش از ۱۰۰ U/kg/۲۴ ساعت به مدت ۲۴ ساعت یا بیشتر). تداخل با آزمایش‌های انعقادی (aPTT).', 'Boxed warning: thrombotic microangiopathy and thromboembolism with aPCC (>100 U/kg/24 h for ≥24 h). Interferes with coagulation tests (aPTT).', [R(Hm, 'Boxed Warning'), R(Hm, '5.4')])],
     exs=[ex('load', 'vial-150', {'perDose': 60, 'mlPerDose': 0.4}, ageYears=6, weightKg=20), ex('w1', 'vial-30', {'perDose': 30, 'mlPerDose': 1}, ageYears=6, weightKg=20),
          ex('w2', 'vial-150', {'perDose': 60, 'mlPerDose': 0.4}, ageYears=6, weightKg=20), ex('w4', 'vial-150', {'perDose': 120, 'mlPerDose': 0.8}, ageYears=6, weightKg=20)])
print('s12c ok')
