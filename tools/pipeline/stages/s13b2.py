"""Stage 13b (part 2) — targeted, immune, hormonal and supportive oncology: bortezomib, lenalidomide, trastuzumab, bevacizumab, pembrolizumab, nivolumab, exemestane, abiraterone, enzalutamide, leucovorin, mesna, dexrazoxane, rasburicase."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's13_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
bsa = lambda id, dis, fa, en, pop, m2, refs, dur=ONE, notes=None: reg(id, dis, T(fa, en), pop, 'bsa', {'perM2PerDay': m2, 'dividedDoses': 1}, refs, dur=dur, notes=notes)
fx = lambda id, dis, fa, en, pop, mg, refs, notes=None, allowed=None, n=1, dur=ONE: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': mg, 'dosesPerDay': n}, refs, dur=dur, notes=notes, allowed=allowed)
sol = lambda id, mg, label, src, sec='3': form(id, 'injection', 'iv', label, mg, 'mg', [R(src, sec)], vol=1)
pw = lambda id, mg, label, src, sec='3', route='iv': form(id, 'powder-for-injection', route, label, mg, 'mg', [R(src, sec)], per='vial')
cap = lambda id, mg, src, label=None: tab(id, mg, label or f'{mg} mg capsule', [R(src, '3')], per='capsule', form_='capsule')
ONC = lambda src, sec: note('فقط زیر نظر پزشک متخصص انکولوژی؛ پروتکل، فاصله دوره‌ها و تنظیم با تیم درمان.', 'Only under an oncologist; protocol, cycle interval and adjustment rest with the treating team.', [R(src, sec)])
IO_W = lambda src: W('واکنش‌های ایمنی شدید و کشنده (پنومونیت، کولیت، هپاتیت، اندوکرینوپاتی، نفریت، پوستی)؛ واکنش انفوزیون؛ عوارض پیوند آلوژن؛ سمیت جنینی.', 'Severe and fatal immune-mediated reactions (pneumonitis, colitis, hepatitis, endocrinopathies, nephritis, skin); infusion reactions; allogeneic HSCT complications; embryo-fetal toxicity.', [R(src, '5')])
ARSI = note('همراه آنالوگ GnRH یا پس از اورکیکتومی دوطرفه.', 'With a GnRH analogue or after bilateral orchiectomy.', [])

add_disease('multiple-myeloma', 'مولتیپل میلوما', 'Multiple myeloma', ['myeloma', 'میلوم', 'مولتیپل مایلوما'], ['C90.00'], 'oncology')
add_disease('tumor-lysis-syndrome', 'هیپراوریسمی سندرم لیز تومور', 'Tumour lysis syndrome hyperuricaemia', ['TLS', 'لیز تومور', 'سندرم لیز تومور'], ['E88.3'], 'oncology')
add_disease('methotrexate-toxicity', 'نجات (rescue) پس از متوترکسات با دوز بالا و مسمومیت ضدفولات', 'Rescue after high-dose methotrexate and antifolate overdose', ['leucovorin rescue', 'مسمومیت متوترکسات', 'رسکیو'], ['T45.1X1A'], 'toxicology')
add_disease('hemorrhagic-cystitis-prevention', 'پیشگیری از سیستیت هموراژیک ناشی از ایفوسفامید', 'Prevention of ifosfamide-induced haemorrhagic cystitis', ['hemorrhagic cystitis', 'سیستیت خونریزی‌دهنده', 'ایفوسفامید'], ['N30.40'], 'oncology')
add_disease('myelodysplastic-syndrome', 'سندرم میلودیسپلاستیک (MDS)', 'Myelodysplastic syndrome (MDS)', ['MDS', 'میلودیسپلازی', 'پیش‌لوسمی'], ['D46.9'], 'hematology')
add_disease('melanoma', 'ملانوم', 'Melanoma', ['melanoma', 'ملانوما', 'سرطان پوست ملانوم'], ['C43.9'], 'oncology')

Vl = fda('velcade', 'FDA Velcade', 'Velcade (bortezomib) for injection 3.5 mg — Prescribing Information', sid('bortezomib'))
drug('bortezomib', 'antineoplastic-immunomodulating', 'بورتزومیب', 'Bortezomib', T('مهارکننده پروتئازوم', 'Proteasome inhibitor'), [{'name': 'Velcade', 'market': 'US'}], ['velcade', 'ولکید', 'بورتزومیب'],
     [pw('vial-3-5', 3.5, '3.5 mg vial (IV 1 mg/mL or SC 2.5 mg/mL after reconstitution)', Vl)],
     [bsa('mm', 'multiple-myeloma', 'مولتیپل میلوما — ۱٫۳ mg/m² وریدی یا زیرجلدی در هر دوز (برنامه دوره‌ای)', 'Multiple myeloma — 1.3 mg/m² IV or SC per dose (cyclical schedule)', A18, 1.3, [R(Vl, '2.1'), R(Vl, '2.2'), R(Vl, '2.6')],
          notes=[note('عودکننده: دو بار در هفته روزهای ۱، ۴، ۸، ۱۱ سپس ۱۰ روز استراحت. درمان‌نشده: با ملفالان و پردنیزون طبق جدول ۱. دست‌کم ۷۲ ساعت بین دوزها. غلظت وریدی و زیرجلدی متفاوت است — حجم را با دقت حساب کنید. نارسایی متوسط/شدید کبد: ۰٫۷ mg/m².', 'Relapsed: twice weekly on days 1, 4, 8, 11 then 10-day rest. Untreated: with melphalan and prednisone per Table 1. At least 72 h between doses. IV and SC concentrations differ — calculate the volume carefully. Moderate/severe hepatic impairment: 0.7 mg/m².', [R(Vl, '2.6'), R(Vl, '2.2'), R(Vl, '2.1'), R(Vl, '2.8')]), ONC(Vl, '2')])],
     [CI('ci', 'حساسیت به بورتزومیب، بور یا مانیتول؛ تزریق داخل نخاعی (کشنده).', 'Hypersensitivity to bortezomib, boron or mannitol; intrathecal administration (fatal).', [R(Vl, '4')])],
     warn=[W('نوروپاتی محیطی؛ افت فشار؛ سمیت قلبی و ریوی؛ PRES؛ سمیت گوارشی؛ ترومبوسیتوپنی و نوتروپنی؛ لیز تومور؛ سمیت کبد؛ TMA؛ سمیت جنینی.', 'Peripheral neuropathy; hypotension; cardiac and pulmonary toxicity; PRES; GI toxicity; thrombocytopenia and neutropenia; tumour lysis; hepatotoxicity; TMA; embryo-fetal toxicity.', [R(Vl, '5')])],
     exs=[ex('mm', 'vial-3-5', {'perDose': 2.6}, ageYears=60, weightKg=80, heightCm=180)])

Rv = fda('revlimid', 'FDA Revlimid', 'Revlimid (lenalidomide) capsules — Prescribing Information', sid('lenalidomide'))
drug('lenalidomide', 'antineoplastic-immunomodulating', 'لنالیدومید', 'Lenalidomide', T('داروی تعدیل‌کننده ایمنی (مشتق تالیدومید)', 'Immunomodulatory drug (thalidomide analogue)'), [{'name': 'Revlimid', 'market': 'US'}], ['revlimid', 'رولیمید', 'لنالیدوماید'],
     [cap('cap-25', 25, Rv), cap('cap-10', 10, Rv), cap('cap-5', 5, Rv), cap('cap-15', 15, Rv), cap('cap-20', 20, Rv)],
     [fx('mm', 'multiple-myeloma', 'مولتیپل میلوما (ترکیبی) — ۲۵ mg یک بار روزهای ۱ تا ۲۱ هر دوره ۲۸ روزه', 'Multiple myeloma (combination) — 25 mg once daily on days 1–21 of 28-day cycles', A18, 25, [R(Rv, '2.1')], allowed=['cap-25'], dur=None,
         notes=[note('نگهدارنده پس از پیوند: ۱۰ mg روزانه مداوم. کپسول باز یا جویده نشود. فقط از طریق برنامه REMS.', 'Maintenance after auto-HSCT: 10 mg daily continuously. Do not open or chew. Only through the REMS programme.', [R(Rv, '2.1'), R(Rv, '2.7'), R(Rv, '5.2')]), ONC(Rv, '2')]),
      fx('mds', 'myelodysplastic-syndrome', 'سندرم میلودیسپلاستیک (del 5q) — ۱۰ mg یک بار در روز', 'Myelodysplastic syndrome (del 5q) — 10 mg once daily', A18, 10, [R(Rv, '2.2')], allowed=['cap-10'], dur=None)],
     [CI('ci', 'بارداری؛ حساسیت شدید به لنالیدومید (آنژیوادم، SJS، TEN).', 'Pregnancy; severe hypersensitivity to lenalidomide (angioedema, SJS, TEN).', [R(Rv, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی (دو تست بارداری منفی و دو روش پیشگیری)، سمیت خونی (نوتروپنی، ترومبوسیتوپنی)، ترومبوآمبولی وریدی و شریانی.', 'Boxed warning: embryo-fetal toxicity (two negative pregnancy tests and two contraceptive methods), haematologic toxicity (neutropenia, thrombocytopenia), venous and arterial thromboembolism.', [R(Rv, 'Boxed Warning')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr ۳۰ تا ۶۰: ۱۰ mg (نگهدارنده/MDS: ۵ mg)؛ زیر ۳۰: طبق جدول ۳.', 'CrCl 30–60: 10 mg (maintenance/MDS: 5 mg); below 30: per Table 3.'), 'refs': [R(Rv, '2.6, Table 3')]}],
     exs=[ex('mm', 'cap-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=75), ex('mds', 'cap-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=70, weightKg=70)])

Hc = fda('herceptin', 'FDA Herceptin', 'Herceptin (trastuzumab) for injection 150 mg — Prescribing Information', sid('trastuzumab'))
drug('trastuzumab', 'antineoplastic-immunomodulating', 'تراستوزوماب', 'Trastuzumab', T('آنتی‌بادی ضد HER2', 'Anti-HER2 antibody'), [{'name': 'Herceptin', 'market': 'US'}], ['herceptin', 'هرسپتین', 'تراستوزوماب', 'aryotrust', 'آریوتراست'],
     [pw('vial-150', 150, '150 mg vial', Hc)],
     [once('load3w', 'breast-cancer', 'سرطان پستان HER2 مثبت (کمکی) یا معده — دوز اول ۸ mg/kg طی ۹۰ دقیقه', 'HER2-positive breast (adjuvant) or gastric cancer — first dose 8 mg/kg over 90 min', A18, 8, None, [R(Hc, '2.3')],
           notes=[note('سپس ۶ mg/kg هر ۳ هفته (کمکی تا ۵۲ هفته). پیش از شروع و منظم LVEF. با تراستوزوماب امتانسین یا دروکستکان جایگزین نشود. وریدی، بولوس نه.', 'Then 6 mg/kg every 3 weeks (adjuvant up to 52 weeks). LVEF before and regularly. Not interchangeable with ado-trastuzumab emtansine or fam-trastuzumab deruxtecan. IV infusion, never bolus.', [R(Hc, '2.3'), R(Hc, '2.1')]), ONC(Hc, '2')]),
      once('m3w', 'breast-cancer', 'نگهدارنده — ۶ mg/kg هر ۳ هفته', 'Maintenance — 6 mg/kg every 3 weeks', A18, 6, None, [R(Hc, '2.3')]),
      once('load1w', 'breast-cancer', 'رژیم هفتگی (کمکی یا متاستاتیک) — دوز اول ۴ mg/kg، سپس ۲ mg/kg هفتگی', 'Weekly regimen (adjuvant or metastatic) — first dose 4 mg/kg, then 2 mg/kg weekly', A18, 4, None, [R(Hc, '2.3')]),
      once('m1w', 'breast-cancer', 'نگهدارنده هفتگی — ۲ mg/kg', 'Weekly maintenance — 2 mg/kg', A18, 2, None, [R(Hc, '2.3')])],
     warn=[W('هشدار جعبه‌ای: کاردیومیوپاتی (بیشتر با آنتراسایکلین)؛ واکنش انفوزیون و سمیت ریوی؛ سمیت جنینی (الیگوهیدرآمنیوس).', 'Boxed warning: cardiomyopathy (higher with anthracyclines); infusion reactions and pulmonary toxicity; embryo-fetal toxicity (oligohydramnios).', [R(Hc, 'Boxed Warning')])],
     exs=[ex('load3w', 'vial-150', {'perDose': 560}, ageYears=50, weightKg=70), ex('m3w', 'vial-150', {'perDose': 420}, ageYears=50, weightKg=70), ex('load1w', 'vial-150', {'perDose': 280}, ageYears=50, weightKg=70), ex('m1w', 'vial-150', {'perDose': 140}, ageYears=50, weightKg=70)])

Av = fda('avastin', 'FDA Avastin', 'Avastin (bevacizumab) injection — Prescribing Information', sid('bevacizumab'))
drug('bevacizumab', 'antineoplastic-immunomodulating', 'بواسیزوماب', 'Bevacizumab', T('آنتی‌بادی ضد VEGF', 'Anti-VEGF antibody'), [{'name': 'Avastin', 'market': 'US'}], ['avastin', 'آواستین', 'بواسیزوماب', 'stivant', 'استیوانت'],
     [sol('vial-25', 25, '25 mg/mL (100 mg/4 mL, 400 mg/16 mL)', Av)],
     [once('crc5', 'colorectal-cancer', 'سرطان کولورکتال متاستاتیک — ۵ mg/kg هر ۲ هفته (با IFL یا رژیم خط دوم)', 'Metastatic colorectal cancer — 5 mg/kg every 2 weeks (with IFL or second-line regimen)', A18, 5, None, [R(Av, '2.2')],
           notes=[note('با FOLFOX4: ۱۰ mg/kg هر ۲ هفته؛ یا ۷٫۵ mg/kg هر ۳ هفته در خط دوم. ۲۸ روز قبل و بعد از جراحی بزرگ نه.', 'With FOLFOX4: 10 mg/kg every 2 weeks; or 7.5 mg/kg every 3 weeks second-line. Not within 28 days before or after major surgery.', [R(Av, '2.2'), R(Av, '2.1')]), ONC(Av, '2')]),
      once('nsclc', 'lung-cancer', 'NSCLC غیرسنگفرشی خط اول — ۱۵ mg/kg هر ۳ هفته با کربوپلاتین و پاکلی‌تاکسل', 'First-line non-squamous NSCLC — 15 mg/kg every 3 weeks with carboplatin and paclitaxel', A18, 15, None, [R(Av, '2.3')],
           notes=[note('گلیوبلاستوم عودکننده و کارسینوم کلیه: ۱۰ mg/kg هر ۲ هفته؛ سرطان سرویکس: ۱۵ mg/kg هر ۳ هفته.', 'Recurrent glioblastoma and renal cell carcinoma: 10 mg/kg every 2 weeks; cervical cancer: 15 mg/kg every 3 weeks.', [R(Av, '2.4'), R(Av, '2.5'), R(Av, '2.6')])])],
     warn=[W('سوراخ‌شدگی گوارش و فیستول؛ اختلال ترمیم زخم؛ خونریزی؛ ترومبوآمبولی شریانی و وریدی؛ فشار خون؛ PRES؛ پروتئینوری؛ واکنش انفوزیون؛ نارسایی تخمدان؛ نارسایی قلب.', 'GI perforation and fistula; wound-healing complications; haemorrhage; arterial and venous thromboembolism; hypertension; PRES; proteinuria; infusion reactions; ovarian failure; heart failure.', [R(Av, '5')])],
     exs=[ex('crc5', 'vial-25', {'perDose': 350, 'mlPerDose': 14}, ageYears=60, weightKg=70), ex('nsclc', 'vial-25', {'perDose': 1050, 'mlPerDose': 42}, ageYears=60, weightKg=70)])

Kt = fda('keytruda', 'FDA Keytruda', 'Keytruda (pembrolizumab) injection — Prescribing Information', sid('pembrolizumab'))
drug('pembrolizumab', 'antineoplastic-immunomodulating', 'پمبرولیزوماب', 'Pembrolizumab', T('مهارکننده PD-1', 'PD-1 blocking antibody'), [{'name': 'Keytruda', 'market': 'US'}], ['keytruda', 'کیترودا', 'پمبرولیزوماب'],
     [sol('vial-25', 25, '25 mg/mL (100 mg/4 mL)', Kt)],
     [fx('adult', 'lung-cancer', 'بزرگسال (ملانوم، NSCLC، سر و گردن، اوروتلیال و سایر اندیکاسیون‌ها) — ۲۰۰ mg هر ۳ هفته یا ۴۰۰ mg هر ۶ هفته', 'Adults (melanoma, NSCLC, head & neck, urothelial and other indications) — 200 mg every 3 weeks or 400 mg every 6 weeks', A18, 200, [R(Kt, '2.2, Table 1')],
         notes=[note('انفوزیون ۳۰ دقیقه. اندیکاسیون و انتخاب بیمار (PD-L1، MSI) طبق جدول ۱ و ۲٫۱. کاهش دوز ندارد؛ در عوارض ایمنی قطع موقت یا دائم.', '30-min infusion. Indication and patient selection (PD-L1, MSI) per Table 1 and 2.1. No dose reductions; withhold or discontinue for immune-mediated reactions.', [R(Kt, '2.2'), R(Kt, '2.1'), R(Kt, '2.3')]), ONC(Kt, '2')]),
      once('child', 'melanoma', 'کودک (ملانوم، cHL، PMBCL) — ۲ mg/kg هر ۳ هفته (حداکثر ۲۰۰ mg)', 'Children (melanoma, cHL, PMBCL) — 2 mg/kg every 3 weeks (max 200 mg)', {'maxAge': age(18, 'year')}, 2, None, [R(Kt, '2.2')], limits={'maxPerDose': 200, 'refs': [R(Kt, '2.2')]})],
     warn=[IO_W(Kt)],
     exs=[ex('adult', 'vial-25', {'perDose': 200, 'mlPerDose': 8}, ageYears=60, weightKg=70), ex('child', 'vial-25', {'perDose': 60, 'mlPerDose': 2.4}, ageYears=10, weightKg=30)])

Op = fda('opdivo', 'FDA Opdivo', 'Opdivo (nivolumab) injection — Prescribing Information', sid('nivolumab'))
drug('nivolumab', 'antineoplastic-immunomodulating', 'نیولوماب', 'Nivolumab', T('مهارکننده PD-1', 'PD-1 blocking antibody'), [{'name': 'Opdivo', 'market': 'US'}], ['opdivo', 'اپدیوو', 'نیولوماب'],
     [sol('vial-10', 10, '10 mg/mL (40/100/120/240 mg)', Op)],
     [fx('adult', 'lung-cancer', 'تک‌دارو (NSCLC، ملانوم، کلیه، هوچکین و سایر) — ۲۴۰ mg هر ۲ هفته یا ۴۸۰ mg هر ۴ هفته (≥۴۰ kg)', 'Single agent (NSCLC, melanoma, RCC, Hodgkin and others) — 240 mg every 2 weeks or 480 mg every 4 weeks (≥40 kg)', {'minWeightKg': 40}, 240, [R(Op, '2.2, Table 1')],
         notes=[note('انفوزیون ۳۰ دقیقه. ترکیب با ایپیلیموماب یا شیمی‌درمانی دوز متفاوت (جدول برچسب). کاهش دوز ندارد.', '30-min infusion. Combinations with ipilimumab or chemotherapy use different doses (label tables). No dose reductions.', [R(Op, '2.2'), R(Op, '2.3')]), ONC(Op, '2')]),
      once('child', 'melanoma', 'ملانوم کودک زیر ۴۰ kg — ۳ mg/kg هر ۲ هفته (یا ۶ mg/kg هر ۴ هفته)', 'Melanoma, children <40 kg — 3 mg/kg every 2 weeks (or 6 mg/kg every 4 weeks)', {'maxAge': age(18, 'year'), 'maxWeightKg': 39.99}, 3, None, [R(Op, '2.2')])],
     warn=[IO_W(Op)],
     exs=[ex('adult', 'vial-10', {'perDose': 240, 'mlPerDose': 24}, ageYears=60, weightKg=70), ex('child', 'vial-10', {'perDose': 90, 'mlPerDose': 9}, ageYears=12, weightKg=30)])

Ar = fda('aromasin', 'FDA Aromasin', 'Aromasin (exemestane) tablets 25 mg — Prescribing Information', sid('exemestane'))
drug('exemestane', 'antineoplastic-immunomodulating', 'اگزمستان', 'Exemestane', T('مهارکننده آروماتاز استروئیدی', 'Steroidal aromatase inactivator'), [{'name': 'Aromasin', 'market': 'US'}], ['aromasin', 'آروماسین', 'اگزمستان'],
     [tab('tab-25', 25, '25 mg tablet', [R(Ar, '3')])],
     [fx('bc', 'breast-cancer', 'سرطان پستان ER مثبت در یائسگی (کمکی پس از تاموکسیفن یا پیشرفته) — ۲۵ mg یک بار پس از غذا', 'ER-positive breast cancer after menopause (adjuvant after tamoxifen or advanced) — 25 mg once daily after a meal', A18, 25, [R(Ar, '2.1')], dur=None,
         notes=[note('با القاگر قوی CYP3A4 (ریفامپین، فنی‌توئین): ۵۰ mg.', 'With strong CYP3A4 inducers (rifampin, phenytoin): 50 mg.', [R(Ar, '2.2')])])],
     [CI('hyper', 'حساسیت به اگزمستان.', 'Hypersensitivity to exemestane.', [R(Ar, '4')])],
     warn=[W('کاهش تراکم استخوان؛ ویتامین D پایش؛ همراه استروژن نه؛ در پیش از یائسگی نه؛ سمیت جنینی.', 'Reduced bone mineral density; check vitamin D; not with oestrogens; not for premenopausal women; embryo-fetal toxicity.', [R(Ar, '5')])],
     exs=[ex('bc', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Zy = fda('zytiga', 'FDA Zytiga', 'Zytiga (abiraterone acetate) tablets — Prescribing Information', sid('abiraterone'))
drug('abiraterone', 'antineoplastic-immunomodulating', 'آبیراترون', 'Abiraterone acetate', T('مهارکننده CYP17', 'CYP17 inhibitor'), [{'name': 'Zytiga', 'market': 'US'}], ['zytiga', 'زایتیگا', 'آبیراترون'],
     [tab('tab-500', 500, '500 mg film-coated tablet', [R(Zy, '3')]), tab('tab-250', 250, '250 mg tablet', [R(Zy, '3')])],
     [fx('crpc', 'prostate-cancer', 'سرطان پروستات متاستاتیک مقاوم به اخته — ۱۰۰۰ mg یک بار ناشتا با پردنیزون ۵ mg دو بار', 'Metastatic castration-resistant prostate cancer — 1000 mg once daily on an empty stomach with prednisone 5 mg twice daily', A18, 1000, [R(Zy, '2.1')], dur=None,
         notes=[note('حساس به اخته پرخطر: پردنیزون ۵ mg یک بار. ۲ ساعت قبل و ۱ ساعت بعد غذا نخورد. با القاگر قوی CYP3A4 دو بار در روز.', 'High-risk castration-sensitive: prednisone 5 mg once daily. No food 2 h before and 1 h after. With strong CYP3A4 inducers twice daily.', [R(Zy, '2.2'), R(Zy, '2'), R(Zy, '2.5')]), note(ARSI['text']['fa'], ARSI['text']['en'], [R(Zy, '2')])])],
     warn=[W('هیپوکالمی، احتباس مایع و عوارض قلبی (اضافه مینرالوکورتیکوئید)؛ نارسایی آدرنال؛ سمیت کبد (آزمایش قبل و حین)؛ شکستگی و مرگ بیشتر با رادیوم-۲۲۳؛ هیپوگلیسمی.', 'Hypokalaemia, fluid retention and cardiovascular events (mineralocorticoid excess); adrenal insufficiency; hepatotoxicity (tests before and during); more fractures and deaths with radium-223; hypoglycaemia.', [R(Zy, '5')])],
     exs=[ex('crpc', 'tab-500', {'perDose': 1000, 'tabletsPerDoseRounded': 2}, ageYears=70, weightKg=80)])

Xt = fda('xtandi', 'FDA Xtandi', 'Xtandi (enzalutamide) capsules and tablets — Prescribing Information', sid('enzalutamide'))
drug('enzalutamide', 'antineoplastic-immunomodulating', 'انزالوتامید', 'Enzalutamide', T('مهارکننده گیرنده آندروژن', 'Androgen receptor inhibitor'), [{'name': 'Xtandi', 'market': 'US'}], ['xtandi', 'اکستاندی', 'انزالوتامید'],
     [cap('cap-40', 40, Xt), tab('tab-80', 80, '80 mg tablet', [R(Xt, '3')])],
     [fx('pc', 'prostate-cancer', 'سرطان پروستات (مقاوم به اخته یا متاستاتیک حساس) — ۱۶۰ mg یک بار', 'Prostate cancer (castration-resistant or metastatic castration-sensitive) — 160 mg once daily', A18, 160, [R(Xt, '2.1')], dur=None,
         notes=[note('کامل بلعیده شود. عارضه درجه ۳: یک هفته قطع، سپس همان یا ۱۲۰/۸۰ mg. مهارکننده قوی CYP2C8: ۸۰ mg.', 'Swallow whole. Grade ≥3 reaction: hold one week, then same or 120/80 mg. Strong CYP2C8 inhibitors: 80 mg.', [R(Xt, '2.1'), R(Xt, '2.2'), R(Xt, '2.3')]), note(ARSI['text']['fa'], ARSI['text']['en'], [R(Xt, '2.1')])])],
     warn=[W('تشنج؛ PRES؛ حساسیت؛ بیماری ایسکمیک قلب؛ زمین خوردن و شکستگی؛ سمیت جنینی؛ اختلال بلع.', 'Seizure; PRES; hypersensitivity; ischaemic heart disease; falls and fractures; embryo-fetal toxicity; dysphagia/choking.', [R(Xt, '5')])],
     exs=[ex('pc', 'cap-40', {'perDose': 160, 'tabletsPerDoseRounded': 4}, ageYears=70, weightKg=80), ex('pc', 'tab-80', {'perDose': 160, 'tabletsPerDoseRounded': 2}, ageYears=70, weightKg=80)])

Lv = fda('leucovorin', 'FDA Leucovorin inj', 'Leucovorin calcium for injection 50/100/200/350 mg (Sagent) — Prescribing Information', sid('leucovorin')); d = R(Lv, 'Dosage and Administration')
drug('leucovorin', 'various', 'لکوورین (فولینیک اسید)', 'Leucovorin (folinic acid)', T('آنالوگ فولات (نجات‌دهنده)', 'Folate analogue (rescue agent)'), [{'name': 'Leucovorin', 'market': 'US'}], ['folinic acid', 'calcium folinate', 'فولینیک اسید', 'لکوورین', 'کلسیم فولینات'],
     [pw('vial-100', 100, '100 mg vial', Lv, 'How Supplied'), pw('vial-350', 350, '350 mg vial', Lv, 'How Supplied')],
     [fx('mtx', 'methotrexate-toxicity', 'نجات پس از متوترکسات با دوز بالا — ۱۵ mg (حدود ۱۰ mg/m²) هر ۶ ساعت، ۱۰ دوز از ۲۴ ساعت پس از شروع متوترکسات', 'Rescue after high-dose methotrexate — 15 mg (about 10 mg/m²) every 6 h for 10 doses from 24 h after methotrexate start', {}, 15, [d], n=4, dur=None,
         notes=[note('تنظیم بر اساس کراتینین و سطح متوترکسات (جدول برچسب). هرگز داخل نخاعی. وریدی حداکثر ۱۶۰ mg/دقیقه (کلسیم).', 'Adjust by creatinine and methotrexate levels (label table). Never intrathecal. IV no faster than 160 mg/min (calcium).', [d, R(Lv, 'Warnings')])]),
      bsa('crc', 'colorectal-cancer', 'سرطان کولورکتال پیشرفته — ۲۰۰ mg/m² وریدی آهسته، سپس فلوئورویوراسیل ۳۷۰ mg/m²، روزانه ۵ روز', 'Advanced colorectal cancer — 200 mg/m² slow IV, then fluorouracil 370 mg/m², daily for 5 days', A18, 200, [d], dur={'min': 5, 'max': 5},
          notes=[note('یا ۲۰ mg/m² سپس فلوئورویوراسیل ۴۲۵ mg/m². در یک انفوزیون با فلوئورویوراسیل مخلوط نشود.', 'Or 20 mg/m² then fluorouracil 425 mg/m². Do not mix with fluorouracil in one infusion.', [d]), ONC(Lv, 'Dosage and Administration')])],
     [CI('ci', 'کم‌خونی پرنیشیوز و سایر کم‌خونی‌های مگالوبلاستیک ناشی از کمبود B12.', 'Pernicious anaemia and other megaloblastic anaemias from vitamin B12 deficiency.', [R(Lv, 'Contraindications')])],
     warn=[W('داخل نخاعی کشنده است؛ هرچه زودتر پس از مسمومیت ضدفولات؛ با فلوئورویوراسیل سمیت بیشتر (به‌ویژه سالمند).', 'Fatal if given intrathecally; give as soon as possible after antifolate overdose; enhances fluorouracil toxicity (especially elderly).', [R(Lv, 'Warnings')])],
     exs=[ex('mtx', 'vial-100', {'perDose': 15}, ageYears=30, weightKg=70), ex('crc', 'vial-350', {'perDose': 400}, ageYears=55, weightKg=80, heightCm=180)])

Ms = fda('mesna', 'FDA Mesna', 'Mesna injection 100 mg/mL / Mesnex tablets (Baxter) — Prescribing Information', sid('mesna'))
drug('mesna', 'various', 'مسنا', 'Mesna', T('محافظ مثانه (ضد اکرولئین)', 'Uroprotective agent'), [{'name': 'Mesnex', 'market': 'US'}], ['mesnex', 'uromitexan', 'مسنا', 'اورومیتکسان'],
     [sol('vial-100', 100, '100 mg/mL (1 g multidose vial)', Ms), tab('tab-400', 400, '400 mg tablet (scored)', [R(Ms, '3')], scored=True)],
     [NC('ifos', 'hemorrhagic-cystitis-prevention', 'پیشگیری از سیستیت هموراژیک ناشی از ایفوسفامید — وریدی ۲۰٪ دوز ایفوسفامید در ساعت ۰، ۴ و ۸', 'Prevention of ifosfamide-induced haemorrhagic cystitis — IV 20% of the ifosfamide dose at 0, 4 and 8 h', A18,
         'دوز نسبتی از دوز ایفوسفامید است (نه وزن): وریدی ۲۰٪ (w/w) در زمان ایفوسفامید و ۴ و ۸ ساعت بعد (جمع ۶۰٪)؛ یا وریدی ۲۰٪ در ساعت ۰ و قرص ۴۰٪ در ساعت ۲ و ۶ (جمع ۱۰۰٪). هر روز ایفوسفامید تکرار. مثال برچسب: ایفوسفامید ۱٫۲ g/m² → مسنا ۲۴۰ mg/m² × ۳.',
         'Dose is a ratio of the ifosfamide dose (not weight): IV 20% (w/w) at ifosfamide time and 4 and 8 h later (total 60%); or IV 20% at 0 h plus tablets 40% at 2 and 6 h (total 100%). Repeat each ifosfamide day. Label example: ifosfamide 1.2 g/m² → mesna 240 mg/m² × 3.', [R(Ms, '2.1'), R(Ms, '2.2')])],
     [CI('hyper', 'حساسیت به مسنا یا اجزا از جمله بنزیل الکل.', 'Hypersensitivity to mesna or excipients including benzyl alcohol.', [R(Ms, '4')])],
     warn=[W('واکنش حساسیتی؛ واکنش پوستی؛ سمیت بنزیل الکل (نوزاد)؛ کتون مثبت کاذب ادرار. هیدراتاسیون کافی و پایش هماچوری.', 'Hypersensitivity; dermatologic toxicity; benzyl alcohol toxicity (neonates); false-positive urine ketones. Maintain hydration and monitor for haematuria.', [R(Ms, '5'), R(Ms, '2.3')])])

Dz = fda('dexrazoxane', 'FDA Dexrazoxane', 'Dexrazoxane for injection 250 mg (Eugia) — Prescribing Information', sid('dexrazoxane'))
drug('dexrazoxane', 'various', 'دکس‌رازوکسان', 'Dexrazoxane', T('محافظ قلب در برابر آنتراسایکلین', 'Anthracycline cardioprotectant'), [{'name': 'Zinecard', 'market': 'US'}], ['zinecard', 'totect', 'زینکارد', 'دکسرازوکسان'],
     [pw('vial-250', 250, '250 mg vial', Dz)],
     [NC('cardio', 'breast-cancer', 'کاهش کاردیومیوپاتی دوکسوروبیسین — نسبت ۱۰ به ۱ با دوز دوکسوروبیسین (مثلاً ۵۰۰ mg/m² برای ۵۰ mg/m²)', 'Reduce doxorubicin cardiomyopathy — 10:1 ratio to the doxorubicin dose (e.g. 500 mg/m² for 50 mg/m²)', A18,
         'دوز = ۱۰ برابر دوز دوکسوروبیسین (mg/m²)؛ تزریق آهسته یا انفوزیون سریع؛ دوکسوروبیسین ظرف ۳۰ دقیقه پس از پایان آن (هرگز قبل). ClCr زیر ۴۰: نسبت ۵ به ۱.',
         'Dose = 10 × the doxorubicin dose (mg/m²); slow push or rapid drip; give doxorubicin within 30 min after it ends (never before). CrCl <40: 5:1 ratio.', [R(Dz, '2.1'), R(Dz, '2.2')])],
     [CI('ci', 'همراه رژیم‌های غیرآنتراسایکلینی نه.', 'Do not use with non-anthracycline regimens.', [R(Dz, '4')])],
     warn=[W('تشدید سرکوب مغز استخوان؛ سمیت قلبی همچنان ممکن؛ بدخیمی ثانویه؛ سمیت جنینی.', 'Added myelosuppression; cardiac toxicity still possible; secondary malignancy; embryo-fetal toxicity.', [R(Dz, '5')])])

El = fda('elitek', 'FDA Elitek', 'Elitek (rasburicase) for injection 1.5/7.5 mg — Prescribing Information', sid('rasburicase'))
drug('rasburicase', 'various', 'راسبوریکاز', 'Rasburicase', T('اوریکاز نوترکیب', 'Recombinant urate oxidase'), [{'name': 'Elitek', 'market': 'US'}], ['elitek', 'fasturtec', 'الیتک', 'راسبوریکاز'],
     [pw('vial-7-5', 7.5, '7.5 mg vial', El), pw('vial-1-5', 1.5, '1.5 mg vial', El)],
     [reg('tls', 'tumor-lysis-syndrome', T('کنترل اسید اوریک در شیمی‌درمانی لوسمی، لنفوم و تومور جامد — ۰٫۲ mg/kg انفوزیون ۳۰ دقیقه روزانه، تا ۵ روز', 'Uric acid control in chemotherapy for leukaemia, lymphoma and solid tumours — 0.2 mg/kg 30-min infusion daily for up to 5 days'), {}, 'weightBased', {'perKgPerDose': 0.2, 'intervalHours': 24}, [R(El, '2.1')], dur={'min': 1, 'max': 5},
          notes=[note('بیش از ۵ روز یا بیش از یک دوره توصیه نمی‌شود. بولوس نه؛ رقیق تا ۵۰ mL. پیش از شروع تست G6PD.', 'Not beyond 5 days or more than one course. Never bolus; dilute to 50 mL. Screen G6PD first.', [R(El, '2.1'), R(El, '2.3'), R(El, 'Boxed Warning')])])],
     [CI('ci', 'سابقه آنافیلاکسی یا حساسیت شدید، همولیز یا مت‌هموگلوبینمی با راسبوریکاز؛ کمبود G6PD.', 'History of anaphylaxis or severe hypersensitivity, haemolysis or methaemoglobinaemia with rasburicase; G6PD deficiency.', [R(El, '4')])],
     warn=[W('هشدار جعبه‌ای: آنافیلاکسی، همولیز (G6PD)، مت‌هموگلوبینمی و تداخل با اندازه‌گیری اسید اوریک (نمونه روی یخ).', 'Boxed warning: anaphylaxis, haemolysis (G6PD), methaemoglobinaemia and interference with uric acid measurement (sample on ice).', [R(El, 'Boxed Warning')])],
     exs=[ex('tls', 'vial-7-5', {'perDose': 14}, ageYears=40, weightKg=70), ex('tls', 'vial-1-5', {'perDose': 4}, ageYears=6, weightKg=20)])
print('s13b2 ok')
