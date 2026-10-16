"""Stage 11d — oral oncology and G-CSF; newer anticoagulants/thrombolytics; PCSK9/lipid and heart-failure/CKD drugs."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's11_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
ONCO = lambda src, sec: note('فقط زیر نظر متخصص انکولوژی؛ دوز بر اساس پاسخ و عوارض تنظیم می‌شود.', 'Only under an oncologist; dose is adjusted by response and toxicity.', [R(src, sec)])

add_disease('prostate-cancer', 'سرطان پروستات', 'Prostate cancer', ['prostate cancer', 'سرطان پروستات', 'کانسر پروستات'], ['C61'], 'oncology')
add_disease('cml', 'لوسمی میلوئید مزمن (CML) و GIST', 'Chronic myeloid leukaemia (CML) and GIST', ['CML', 'GIST', 'لوسمی میلوئید', 'سرطان خون مزمن'], ['C92.10', 'C49.A0'], 'oncology')
add_disease('colorectal-cancer', 'سرطان کولورکتال (روده بزرگ)', 'Colorectal cancer', ['colon cancer', 'سرطان روده', 'سرطان کولون'], ['C18.9'], 'oncology')
add_disease('hit', 'ترومبوسیتوپنی ناشی از هپارین (HIT)', 'Heparin-induced thrombocytopenia (HIT)', ['HIT', 'heparin induced thrombocytopenia', 'افت پلاکت هپارین'], ['D75.82'], 'hematology')
def ml(aid, title, review):
    m, dd, y = review.split('/')
    return add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                   edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
NOTE = {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}
def symptoms(did, items, *srcs):
    d = json.load(open(os.path.join(ROOT, 'diseases.json')))
    for x in d:
        if x['id'] == did: x['symptoms'] = {'items': [T(fa, en) for fa, en in items], 'refs': [{'source': s, 'section': 'Symptoms', 'note': NOTE} for s in srcs]}
    json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')
symptoms('prostate-cancer', [('در مراحل اولیه اغلب بی‌علامت؛ PSA ممکن است زودتر بالا برود', 'Often no symptoms early; PSA may rise first'), ('شروع دیر یا جریان ضعیف ادرار، زور زدن، تخلیه ناقص', 'Delayed or slow urinary stream, straining, incomplete emptying'),
                             ('چکه کردن یا نشت ادرار پس از دفع', 'Dribbling or leakage after urinating'), ('خون در ادرار یا منی', 'Blood in urine or semen'), ('در انتشار: درد استخوان کمر و لگن', 'With spread: bone pain in the lower back and pelvis')], ml('000380', 'Prostate cancer', '7/1/2025'))
symptoms('cml', [('مرحله مزمن: اغلب بی‌علامت و با آزمایش خون پیدا می‌شود', 'Chronic phase: often no symptoms, found on blood tests'), ('مرحله تسریع‌شده: تب بدون عفونت، درد استخوان، بزرگی طحال', 'Accelerated phase: fever without infection, bone pain, enlarged spleen'),
                 ('بحران بلاستی: کبودی، خونریزی، عفونت، تعریق شبانه، خستگی، ضعف', 'Blast crisis: bruising, bleeding, infection, night sweats, fatigue, weakness'), ('فشار زیر دنده‌های چپ از بزرگی طحال؛ نقاط ریز قرمز پوست (پتشی)', 'Pressure under the left ribs from a large spleen; pinpoint red skin spots (petechiae)')],
         ml('000570', 'Chronic myelogenous leukemia (CML)', '1/29/2026'))
symptoms('colorectal-cancer', [('اغلب بی‌علامت', 'Often no symptoms'), ('درد و حساسیت پایین شکم', 'Lower abdominal pain and tenderness'), ('خون در مدفوع', 'Blood in the stool'), ('تغییر اجابت مزاج: اسهال یا یبوست', 'Change in bowel habits: diarrhoea or constipation'),
                               ('مدفوع باریک', 'Narrow stools'), ('کاهش وزن بی‌دلیل', 'Unexplained weight loss')], ml('000262', 'Colorectal cancer', '4/1/2025'))

# ===================== oncology =====================
Tm = fda('tamoxifen', 'FDA Tamoxifen', 'Tamoxifen citrate tablets 10/20 mg (Mylan) — Prescribing Information', sid('tamoxifen')); d = R(Tm, 'Dosage and Administration')
drug('tamoxifen', 'antineoplastic-immunomodulating', 'تاموکسیفن', 'Tamoxifen', T('تعدیل‌کننده انتخابی گیرنده استروژن (SERM)', 'Selective estrogen receptor modulator (SERM)'), [{'name': 'Nolvadex', 'market': 'US'}], ['nolvadex', 'تاموکسیفن', 'نولوادکس'],
     [tab('tab-10', 10, '10 mg tablet', [R(Tm, 'How Supplied')]), tab('tab-20', 20, '20 mg tablet', [R(Tm, 'How Supplied')])],
     [reg('bc', 'breast-cancer', T('سرطان پستان — ۲۰ تا ۴۰ mg در روز (بالای ۲۰ mg در دو دوز)', 'Breast cancer — 20–40 mg/day (above 20 mg in two doses)'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [d],
          notes=[ONCO(Tm, 'Dosage and Administration'), note('دوز بالای ۲۰ mg/روز صبح و عصر. درمان کمکی معمولاً ۵ سال.', 'Doses above 20 mg/day split morning and evening. Adjuvant therapy usually 5 years.', [d])]),
      reg('dcis', 'breast-cancer', T('DCIS و کاهش خطر در زن پرخطر — ۲۰ mg روزانه ۵ سال', 'DCIS and risk reduction in high-risk women — 20 mg daily for 5 years'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [d])],
     [CI('ci', 'حساسیت به تاموکسیفن. DCIS و کاهش خطر: نیاز به ضدانعقاد کومارینی یا سابقه DVT یا آمبولی ریه.', 'Hypersensitivity to tamoxifen. DCIS and risk reduction: need for coumarin anticoagulants or history of DVT or pulmonary embolism.', [R(Tm, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای (DCIS و کاهش خطر): بدخیمی رحم، سکته مغزی و آمبولی ریه — گاه کشنده.', 'Boxed warning (DCIS and risk reduction): uterine malignancies, stroke and pulmonary embolism — sometimes fatal.', [R(Tm, 'Boxed Warning')])],
     inter=[IA('warfarin', 'وارفارین: افزایش شدید اثر ضدانعقادی.', 'Warfarin: marked increase in anticoagulant effect.', [R(Tm, 'Contraindications')])],
     exs=[ex('bc', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=65), ex('dcis', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=65)])

An = fda('anastrozole', 'FDA Anastrozole', 'Anastrozole tablets 1 mg — Prescribing Information', sid('anastrozole'))
drug('anastrozole', 'antineoplastic-immunomodulating', 'آناستروزول', 'Anastrozole', T('مهارکننده آروماتاز', 'Aromatase inhibitor'), [{'name': 'Arimidex', 'market': 'US'}], ['arimidex', 'آریمیدکس', 'آناستروزول'],
     [tab('tab-1', 1, '1 mg tablet', [R(An, '3')])],
     [reg('bc', 'breast-cancer', T('سرطان پستان گیرنده هورمونی مثبت پس از یائسگی — ۱ mg یک بار در روز', 'HR-positive breast cancer after menopause — 1 mg once daily'), A18, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(An, '2.1')],
          notes=[note('پیشرفته: تا پیشرفت بیماری. کمکی: در کارآزمایی ATAC پنج سال.', 'Advanced: until progression. Adjuvant: five years in the ATAC trial.', [R(An, '2.1')])])],
     [CI('hyper', 'حساسیت به آناستروزول یا اجزای قرص.', 'Hypersensitivity to anastrozole or any excipient.', [R(An, '4')])],
     warn=[W('کاهش تراکم استخوان؛ افزایش کلسترول؛ در بیماری ایسکمیک قلب حوادث قلبی بیشتر.', 'Reduced bone mineral density; raised cholesterol; more ischaemic events in pre-existing ischaemic heart disease.', [R(An, '5')])],
     exs=[ex('bc', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=65)])

Bl = fda('bicalutamide', 'FDA Bicalutamide', 'Bicalutamide tablets 50 mg — Prescribing Information', sid('bicalutamide'))
drug('bicalutamide', 'antineoplastic-immunomodulating', 'بیکالوتامید', 'Bicalutamide', T('آنتی‌آندروژن', 'Antiandrogen'), [{'name': 'Casodex', 'market': 'US'}], ['casodex', 'کازودکس', 'بیکالوتامید'],
     [tab('tab-50', 50, '50 mg tablet', [R(Bl, 'How Supplied')])],
     [reg('pc', 'prostate-cancer', T('سرطان پروستات متاستاتیک (همراه آنالوگ LHRH) — ۵۰ mg یک بار در روز', 'Metastatic prostate cancer (with an LHRH analogue) — 50 mg once daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Bl, 'Dosage and Administration')],
          notes=[note('هم‌زمان با شروع آنالوگ LHRH و هر روز در ساعت ثابت.', 'Start at the same time as the LHRH analogue; take at the same time each day.', [R(Bl, 'Dosage and Administration')])])],
     [CI('ci', 'حساسیت به بیکالوتامید (آنژیوادم، کهیر)؛ زنان (اندیکاسیون ندارد)؛ بارداری (آسیب جنین).', 'Hypersensitivity to bicalutamide (angioedema, urticaria); women (no indication); pregnancy (fetal harm).', [R(Bl, 'Contraindications')])],
     warn=[W('آسیب کبدی (آزمایش کبد دوره‌ای)؛ ژنیکوماستی؛ افزایش اثر وارفارین.', 'Hepatitis (periodic liver tests); gynaecomastia; increased warfarin effect.', [R(Bl, 'Warnings')])],
     exs=[ex('pc', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=70, weightKg=75)])

Im = fda('imatinib', 'FDA Imatinib', 'Imatinib mesylate tablets 100/400 mg — Prescribing Information', sid('imatinib'))
IMN = note('با غذا و یک لیوان پر آب. ۴۰۰ و ۶۰۰ mg یک بار؛ ۸۰۰ mg به‌صورت ۴۰۰ mg دو بار. با القاگر قوی CYP3A4 دست‌کم ۵۰٪ افزایش.', 'With a meal and a large glass of water. 400 and 600 mg once daily; 800 mg as 400 mg twice daily. With strong CYP3A4 inducers increase by at least 50%.', [R(Im, '2.1'), R(Im, '2.12')])
drug('imatinib', 'antineoplastic-immunomodulating', 'ایماتینیب', 'Imatinib', T('مهارکننده تیروزین کیناز BCR-ABL', 'BCR-ABL tyrosine kinase inhibitor'), [{'name': 'Gleevec', 'market': 'US'}], ['gleevec', 'glivec', 'گلیوک', 'ایماتینیب'],
     [tab('tab-100', 100, '100 mg tablet (scored)', [R(Im, '3')], scored=True), tab('tab-400', 400, '400 mg tablet (scored)', [R(Im, '3')], scored=True)],
     [reg('cml-cp', 'cml', T('CML فاز مزمن — بزرگسال ۴۰۰ mg یک بار در روز', 'CML chronic phase — adult 400 mg once daily'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 1}, [R(Im, '2.2')], notes=[ONCO(Im, '2'), IMN]),
      reg('cml-ap', 'cml', T('CML فاز تسریع یا بلاستی — بزرگسال ۶۰۰ mg یک بار در روز', 'CML accelerated phase or blast crisis — adult 600 mg once daily'), A18, 'fixed', {'perDose': 600, 'dosesPerDay': 1}, [R(Im, '2.2')], notes=[ONCO(Im, '2'), IMN]),
      reg('cml-child', 'cml', T('CML کودک (۱ سال به بالا) — ۳۴۰ mg/m²/روز (حداکثر ۶۰۰ mg)', 'Pediatric CML (≥1 y) — 340 mg/m²/day (max 600 mg)'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year')}, 'bsa', {'perM2PerDay': 340, 'dividedDoses': 1}, [R(Im, '2.3')],
          limits={'maxPerDay': 600, 'refs': [R(Im, '2.3')]}, notes=[ONCO(Im, '2'), note('یک بار یا تقسیم در دو نوبت صبح و عصر.', 'Once daily or split into morning and evening doses.', [R(Im, '2.3')])]),
      reg('gist', 'cml', T('GIST متاستاتیک یا کمکی — بزرگسال ۴۰۰ mg یک بار در روز', 'Metastatic or adjuvant GIST — adult 400 mg once daily'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 1}, [R(Im, '2.10'), R(Im, '2.11')],
          notes=[ONCO(Im, '2'), IMN, note('کمکی: ۳ سال. پیشرفت در GIST متاستاتیک: تا ۸۰۰ mg (۴۰۰ دو بار).', 'Adjuvant: 3 years. Progression in metastatic GIST: up to 800 mg (400 twice daily).', [R(Im, '2.10'), R(Im, '2.11')])])],
     warn=[W('احتباس مایع و ادم؛ سرکوب مغز استخوان (CBC هفتگی ماه اول)؛ سمیت کبد؛ نارسایی قلب؛ آسیب جنینی.', 'Fluid retention and oedema; myelosuppression (weekly CBC in month 1); hepatotoxicity; heart failure; embryo-fetal toxicity.', [R(Im, '5')])],
     exs=[ex('cml-cp', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('cml-ap', 'tab-100', {'perDose': 600, 'tabletsPerDoseRounded': 6}, ageYears=50, weightKg=70),
          ex('cml-child', 'tab-100', {'perDose': 340, 'tabletsPerDoseRounded': 3.5}, ageYears=10, weightKg=36, heightCm=100), ex('gist', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=75)])

Cp = fda('capecitabine', 'FDA Capecitabine', 'Capecitabine tablets 150/500 mg — Prescribing Information', sid('capecitabine'))
CPN = note('دو بار در روز با فاصله حدود ۱۲ ساعت، تا ۳۰ دقیقه پس از غذا؛ روز ۱ تا ۱۴ هر دوره ۲۱ روزه. دوز به نزدیک‌ترین ۱۵۰ mg گرد شود. ClCr ۳۰ تا ۵۰: ۲۵٪ کمتر؛ زیر ۳۰ تعیین نشده.', 'Twice daily about 12 h apart within 30 min after a meal; days 1–14 of each 21-day cycle. Round to the nearest 150 mg. CrCl 30–50: reduce by 25%; <30 not established.', [R(Cp, '2.7'), R(Cp, '2.6')])
drug('capecitabine', 'antineoplastic-immunomodulating', 'کپسیتابین', 'Capecitabine', T('آنتی‌متابولیت (پیش‌داروی فلوئورواوراسیل)', 'Antimetabolite (fluorouracil prodrug)'), [{'name': 'Xeloda', 'market': 'US'}], ['xeloda', 'زلودا', 'کپسیتابین', 'کاپسیتابین'],
     [tab('tab-150', 150, '150 mg tablet', [R(Cp, '3')]), tab('tab-500', 500, '500 mg tablet', [R(Cp, '3')])],
     [reg('colon', 'colorectal-cancer', T('سرطان کولون (کمکی، تک‌دارو) — ۱۲۵۰ mg/m² دو بار در روز، روز ۱ تا ۱۴ هر ۲۱ روز (حداکثر ۸ دوره)', 'Adjuvant colon cancer (single agent) — 1250 mg/m² twice daily, days 1–14 every 21 days (max 8 cycles)'), A18, 'bsa',
          {'perM2PerDay': 2500, 'dividedDoses': 2}, [R(Cp, '2.1')], dur={'min': 14, 'max': 14}, notes=[ONCO(Cp, '2'), CPN, note('همراه اگزالی‌پلاتین: ۱۰۰۰ mg/m² دو بار در روز.', 'With oxaliplatin: 1000 mg/m² twice daily.', [R(Cp, '2.2')])]),
      reg('breast', 'breast-cancer', T('سرطان پستان پیشرفته (تک‌دارو) — ۱۰۰۰ تا ۱۲۵۰ mg/m² دو بار در روز، روز ۱ تا ۱۴ هر ۲۱ روز', 'Advanced breast cancer (single agent) — 1000–1250 mg/m² twice daily, days 1–14 every 21 days'), A18, 'bsa',
          {'perM2PerDay': 2000, 'dividedDoses': 2}, [R(Cp, '2.2')], dur={'min': 14, 'max': 14}, notes=[ONCO(Cp, '2'), CPN])],
     [CI('ci', 'سابقه حساسیت شدید به فلوئورواوراسیل یا کپسیتابین.', 'History of severe hypersensitivity to fluorouracil or capecitabine.', [R(Cp, '4')])],
     warn=[W('هشدار جعبه‌ای: خونریزی و افزایش INR با وارفارین (پایش مکرر INR). کمبود DPD: سمیت شدید یا کشنده. اسهال، سندرم دست و پا.', 'Boxed warning: bleeding and raised INR with warfarin (monitor INR frequently). DPD deficiency: severe or fatal toxicity. Diarrhoea, hand-foot syndrome.', [R(Cp, 'Boxed Warning'), R(Cp, '5')])],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۳۰ تا ۵۰: ۲۵٪ کاهش دوز؛ زیر ۳۰ دوز تعیین نشده.', 'CrCl 30–50: reduce dose by 25%; <30 dose not established.'), 'refs': [R(Cp, '2.6')]}],
     exs=[ex('colon', 'tab-150', {'perDose': 2250, 'tabletsPerDoseRounded': 15}, ageYears=55, weightKg=72, heightCm=162), ex('breast', 'tab-500', {'perDose': 1500, 'tabletsPerDoseRounded': 3}, ageYears=55, weightKg=56.25, heightCm=144)])

Nu = fda('neupogen', 'FDA Neupogen', 'Neupogen (filgrastim) injection — Prescribing Information', sid('neupogen'))
drug('filgrastim', 'antineoplastic-immunomodulating', 'فیلگراستیم (G-CSF)', 'Filgrastim (G-CSF)', T('فاکتور محرک کلونی گرانولوسیت', 'Granulocyte colony-stimulating factor'), [{'name': 'Neupogen', 'market': 'US'}], ['neupogen', 'نوپوژن', 'G-CSF', 'فیلگراستیم', 'pd-grastim'],
     [form('vial-300', 'injection', 'sc', '300 mcg/mL vial (also 480 mcg/1.6 mL; syringes 300 mcg/0.5 mL, 480 mcg/0.8 mL)', 300, 'mcg', [R(Nu, '3')], vol=1)],
     [reg('chemo', 'febrile-neutropenia', T('شیمی‌درمانی سرکوب‌کننده مغز استخوان — شروع ۵ mcg/kg/روز', 'Myelosuppressive chemotherapy — start 5 mcg/kg/day'), {}, 'weightBased', {'perKgPerDay': 5, 'dividedDoses': 1}, [R(Nu, '2.1')], unit='mcg',
          notes=[note('دست‌کم ۲۴ ساعت پس از شیمی‌درمانی شروع شود؛ تا ANC بالای ۱۰٬۰۰۰ پس از نادیر (حداکثر ۲ هفته). در هر دوره قابل افزایش ۵ mcg/kg. CBC دو بار در هفته.', 'Start at least 24 h after chemotherapy; continue until ANC >10,000 after the nadir (up to 2 weeks). May increase by 5 mcg/kg each cycle. CBC twice weekly.', [R(Nu, '2.1')])]),
      reg('bmt', 'febrile-neutropenia', T('پس از پیوند مغز استخوان — ۱۰ mcg/kg/روز وریدی', 'After bone marrow transplant — 10 mcg/kg/day IV'), {}, 'weightBased', {'perKgPerDay': 10, 'dividedDoses': 1}, [R(Nu, '2.2')], unit='mcg'),
      reg('rad', 'poisoning', T('مواجهه با تشعشع سرکوب‌کننده مغز استخوان (بیش از ۲ Gy) — ۱۰ mcg/kg یک بار در روز', 'Myelosuppressive radiation exposure (>2 Gy) — 10 mcg/kg once daily'), {}, 'weightBased', {'perKgPerDay': 10, 'dividedDoses': 1}, [R(Nu, '2.5')], unit='mcg')],
     [CI('hyper', 'سابقه واکنش آلرژیک جدی به فاکتورهای محرک کلونی گرانولوسیت (فیلگراستیم، پگ‌فیلگراستیم).', 'History of serious allergic reactions to G-CSFs such as filgrastim or pegfilgrastim.', [R(Nu, '4')])],
     warn=[W('پارگی طحال (درد شانه یا بالای شکم چپ)؛ ARDS؛ بحران سلول داسی؛ گلومرولونفریت؛ سندرم نشت مویرگی.', 'Splenic rupture (left upper abdominal or shoulder pain); ARDS; sickle cell crisis; glomerulonephritis; capillary leak syndrome.', [R(Nu, '5')])],
     exs=[ex('chemo', 'vial-300', {'perDose': 350, 'mlPerDose': 1.17}, ageYears=50, weightKg=70), ex('bmt', 'vial-300', {'perDose': 700, 'mlPerDose': 2.33}, ageYears=40, weightKg=70), ex('rad', 'vial-300', {'perDose': 700, 'mlPerDose': 2.33}, ageYears=40, weightKg=70)])

# ===================== anticoagulants / thrombolytics =====================
Sv = fda('savaysa', 'FDA Savaysa', 'Savaysa (edoxaban) tablets — Prescribing Information', sid('savaysa'))
drug('edoxaban', 'blood', 'ادوکسابان', 'Edoxaban', T('مهارکننده مستقیم فاکتور Xa', 'Direct factor Xa inhibitor'), [{'name': 'Savaysa / Lixiana', 'market': 'US'}], ['savaysa', 'lixiana', 'ادوکسابان'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Sv, '3')]) for m in (15, 30, 60)],
     [reg('af', 'atrial-fibrillation', T('AF غیردریچه‌ای — ClCr ۵۰ تا ۹۵: ۶۰ mg یک بار در روز', 'Non-valvular AF — CrCl 50–95: 60 mg once daily'), A18, 'fixed', {'perDose': 60, 'dosesPerDay': 1}, [R(Sv, '2.1')],
          notes=[note('ClCr بالای ۹۵ استفاده نشود (اثر کمتر). ClCr ۱۵ تا ۵۰: ۳۰ mg یک بار در روز.', 'Do not use with CrCl >95 (reduced efficacy). CrCl 15–50: 30 mg once daily.', [R(Sv, '2.1')])]),
      reg('vte', 'venous-thromboembolism', T('درمان DVT و PE — ۶۰ mg یک بار در روز پس از ۵ تا ۱۰ روز ضدانعقاد تزریقی', 'DVT and PE treatment — 60 mg once daily after 5–10 days of parenteral anticoagulation'), {'minAge': age(18, 'year'), 'minWeightKg': 60.01}, 'fixed', {'perDose': 60, 'dosesPerDay': 1}, [R(Sv, '2.2')],
          notes=[note('۳۰ mg یک بار: ClCr ۱۵ تا ۵۰، وزن ۶۰ kg یا کمتر، یا مهارکننده P-gp خاص.', '30 mg once daily: CrCl 15–50, weight ≤60 kg, or certain P-gp inhibitors.', [R(Sv, '2.2')])]),
      reg('vte-low', 'venous-thromboembolism', T('درمان DVT و PE — وزن ۶۰ kg یا کمتر: ۳۰ mg یک بار در روز', 'DVT and PE treatment — weight ≤60 kg: 30 mg once daily'), {'minAge': age(18, 'year'), 'maxWeightKg': 60}, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Sv, '2.2')])],
     [CI('bleed', 'خونریزی پاتولوژیک فعال.', 'Active pathological bleeding.', [R(Sv, '4')])],
     warn=[W('هشدار جعبه‌ای: در AF با ClCr بالای ۹۵ اثر کمتر (سکته بیشتر)؛ قطع زودهنگام خطر ترومبوز را بالا می‌برد؛ هماتوم نخاعی/اپیدورال با بی‌حسی نخاعی.', 'Boxed warning: reduced efficacy in AF with CrCl >95 (more strokes); premature discontinuation raises ischaemic risk; spinal/epidural haematoma with neuraxial procedures.', [R(Sv, 'Boxed Warning')])],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۱۵ تا ۵۰: ۳۰ mg یک بار در روز؛ زیر ۱۵ توصیه نمی‌شود.', 'CrCl 15–50: 30 mg once daily; <15 not recommended.'), 'refs': [R(Sv, '2.1'), R(Sv, '2.2')]}],
     exs=[ex('af', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=70, weightKg=80), ex('vte', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=80), ex('vte-low', 'tab-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=55)])

Fd = fda('fondaparinux', 'FDA Fondaparinux', 'Fondaparinux sodium injection (Mylan) — Prescribing Information', sid('fonda'))
drug('fondaparinux', 'blood', 'فونداپارینوکس', 'Fondaparinux', T('مهارکننده غیرمستقیم فاکتور Xa', 'Indirect factor Xa inhibitor'), [{'name': 'Arixtra', 'market': 'US'}], ['arixtra', 'آریکسترا', 'فونداپارینوکس'],
     [form('syr-25', 'injection', 'sc', '2.5 mg/0.5 mL prefilled syringe', 2.5, 'mg', [R(Fd, '3')], vol=0.5), form('syr-75', 'injection', 'sc', '7.5 mg/0.6 mL prefilled syringe (also 5 mg/0.4 mL, 10 mg/0.8 mL)', 7.5, 'mg', [R(Fd, '3')], vol=0.6)],
     [reg('proph', 'dvt-prophylaxis', T('پیشگیری از DVT پس از جراحی شکستگی لگن، تعویض مفصل یا جراحی شکم — ۲٫۵ mg یک بار در روز', 'DVT prophylaxis after hip fracture, hip/knee replacement or abdominal surgery — 2.5 mg once daily'), {'minAge': age(18, 'year'), 'minWeightKg': 50}, 'fixed',
          {'perDose': 2.5, 'dosesPerDay': 1}, [R(Fd, '2.2'), R(Fd, '2.3')], dur={'min': 5, 'max': 9}, allowed=['syr-25'],
          notes=[note('اولین دوز ۶ تا ۸ ساعت پس از جراحی پس از هموستاز (زودتر خونریزی بیشتر). شکستگی لگن: تا ۲۴ روز اضافه.', 'First dose 6–8 h after surgery once haemostasis is established (earlier increases bleeding). Hip fracture: up to 24 additional days.', [R(Fd, '2.2')])]),
      reg('tx', 'venous-thromboembolism', T('درمان DVT و PE — زیر ۵۰ kg: ۵؛ ۵۰ تا ۱۰۰: ۷٫۵؛ بالای ۱۰۰ kg: ۱۰ mg یک بار در روز', 'DVT and PE treatment — <50 kg: 5; 50–100: 7.5; >100 kg: 10 mg once daily'), A18, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 49.99, 'perDose': 5, 'dosesPerDay': 1}, {'minWeightKg': 49.99, 'maxWeightKg': 100, 'perDose': 7.5, 'dosesPerDay': 1}, {'minWeightKg': 100, 'maxWeightKg': None, 'perDose': 10, 'dosesPerDay': 1}]},
          [R(Fd, '2.4')], notes=[note('وارفارین هرچه زودتر (معمولاً ظرف ۷۲ ساعت) شروع شود؛ دست‌کم ۵ روز و تا INR ۲ تا ۳ دو روز پشت سر هم.', 'Start warfarin as soon as possible (usually within 72 h); at least 5 days and until INR 2–3 on two consecutive days.', [R(Fd, '2.4')])])],
     [CI('ci', 'ClCr زیر ۳۰؛ خونریزی فعال شدید؛ اندوکاردیت باکتریایی؛ ترومبوسیتوپنی با آنتی‌بادی ضدپلاکت وابسته به فونداپارینوکس؛ وزن زیر ۵۰ kg در پیشگیری؛ حساسیت.', 'CrCl <30; active major bleeding; bacterial endocarditis; thrombocytopenia with a positive anti-platelet antibody test in the presence of fondaparinux; body weight <50 kg for prophylaxis; hypersensitivity.', [R(Fd, '4')])],
     warn=[W('هشدار جعبه‌ای: هماتوم نخاعی یا اپیدورال با بی‌حسی نخاعی یا پونکسیون (فلج طولانی یا دائمی).', 'Boxed warning: spinal or epidural haematoma with neuraxial anaesthesia or puncture (long-term or permanent paralysis).', [R(Fd, 'Boxed Warning')])],
     exs=[ex('proph', 'syr-25', {'perDose': 2.5, 'mlPerDose': 0.5}, ageYears=70, weightKg=70), ex('tx', 'syr-75', {'perDose': 7.5, 'mlPerDose': 0.6}, ageYears=55, weightKg=80)])

Ag = fda('argatroban', 'FDA Argatroban', 'Argatroban in 0.9% NaCl 1 mg/mL — Prescribing Information', sid('argatroban'))
drug('argatroban', 'blood', 'آرگاتروبان', 'Argatroban', T('مهارکننده مستقیم ترومبین', 'Direct thrombin inhibitor'), [{'name': 'Argatroban', 'market': 'US'}], ['argatroban', 'آرگاتروبان'],
     [form('vial-1-mcg', 'injection', 'iv', '125 mg/125 mL ready-to-use (1 mg/mL = 1000 mcg/mL)', 1000, 'mcg', [R(Ag, '3')], vol=1)],
     [reg('hit', 'hit', T('HIT (با یا بدون ترومبوز) — شروع ۲ mcg/kg/دقیقه (حداکثر ۱۰)', 'HIT (with or without thrombosis) — start 2 mcg/kg/min (max 10)'), A18, 'infusion', {'perKgPerMin': 2}, [R(Ag, '2.2')], unit='mcg',
          notes=[note('هپارین قطع و aPTT پایه گرفته شود. تنظیم تا aPTT ۱٫۵ تا ۳ برابر پایه (نه بیش از ۱۰۰ ثانیه)؛ حداکثر ۱۰ mcg/kg/دقیقه. نارسایی متوسط/شدید کبد: دوز کمتر.', 'Stop heparin and get a baseline aPTT. Adjust to aPTT 1.5–3× baseline (not >100 s); max 10 mcg/kg/min. Moderate/severe hepatic impairment: lower dose.', [R(Ag, '2.2'), R(Ag, '2.4')])]),
      reg('pci', 'acute-coronary-syndrome', T('PCI در HIT — انفوزیون ۲۵ mcg/kg/دقیقه (به‌اضافه بولوس ۳۵۰ mcg/kg)', 'PCI in HIT — infusion 25 mcg/kg/min (plus a 350 mcg/kg bolus)'), A18, 'infusion', {'perKgPerMin': 25}, [R(Ag, '2.3')], unit='mcg',
          notes=[note('بولوس ۳۵۰ mcg/kg در ۳ تا ۵ دقیقه؛ ACT ۵ تا ۱۰ دقیقه بعد؛ ادامه PCI اگر ACT بالای ۳۰۰ ثانیه.', 'Bolus 350 mcg/kg over 3–5 min; check ACT 5–10 min later; proceed if ACT >300 s.', [R(Ag, '2.3')])])],
     [CI('ci', 'خونریزی شدید؛ سابقه حساسیت به آرگاتروبان.', 'Major bleeding; history of hypersensitivity to argatroban.', [R(Ag, '4')])],
     exs=[ex('hit', 'vial-1-mcg', {'perMin': 140, 'mlPerHour': 8.4}, ageYears=60, weightKg=70), ex('pci', 'vial-1-mcg', {'perMin': 1750, 'mlPerHour': 105}, ageYears=60, weightKg=70)])

Bv = fda('bivalirudin', 'FDA Bivalirudin', 'Bivalirudin for injection 250 mg — Prescribing Information', sid('bival'))
drug('bivalirudin', 'blood', 'بیوالیرودین', 'Bivalirudin', T('مهارکننده مستقیم ترومبین', 'Direct thrombin inhibitor'), [{'name': 'Angiomax', 'market': 'US'}], ['angiomax', 'آنژیومکس', 'بیوالیرودین'],
     [form('vial-250', 'powder-for-injection', 'iv', '250 mg vial', 250, 'mg', [R(Bv, '3')], per='vial')],
     [reg('pci', 'acute-coronary-syndrome', T('PCI — بولوس ۰٫۷۵ mg/kg، سپس انفوزیون ۱٫۷۵ mg/kg/ساعت در طول پروسیجر', 'PCI — 0.75 mg/kg bolus, then 1.75 mg/kg/h infusion for the procedure'), A18, 'weightBased', {'perKgPerDose': 0.75, 'intervalHours': 24}, [R(Bv, '2.1')], dur=ONE,
          notes=[note('عدد ماشین‌حساب دوز بولوس است. ACT ۵ دقیقه بعد؛ در صورت نیاز ۰٫۳ mg/kg بولوس اضافه. فقط با آسپرین مطالعه شده. انفوزیون تا ۴ ساعت پس از PCI قابل ادامه.', 'The calculator gives the BOLUS. Check ACT after 5 min; extra 0.3 mg/kg bolus if needed. Studied only with aspirin. Infusion may continue up to 4 h after PCI.', [R(Bv, '2.1')])])],
     [CI('ci', 'خونریزی فعال شدید؛ حساسیت به بیوالیرودین.', 'Active major bleeding; hypersensitivity to bivalirudin.', [R(Bv, '4')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰: انفوزیون ۱ mg/kg/ساعت؛ همودیالیز: ۰٫۲۵ mg/kg/ساعت. بولوس تغییر نمی‌کند.', 'CrCl <30: infusion 1 mg/kg/h; haemodialysis: 0.25 mg/kg/h. No change to the bolus.'), 'refs': [R(Bv, '2')]}],
     exs=[ex('pci', 'vial-250', {'perDose': 52.5}, ageYears=60, weightKg=70)])

Tk = fda('tnkase', 'FDA TNKase', 'TNKase (tenecteplase) 25 mg / 50 mg — Prescribing Information', sid('tnk'))
drug('tenecteplase', 'blood', 'تنکتپلاز', 'Tenecteplase', T('فعال‌کننده پلاسمینوژن بافتی (ترومبولیتیک)', 'Tissue plasminogen activator (thrombolytic)'), [{'name': 'TNKase', 'market': 'US'}], ['tnkase', 'metalyse', 'تنکتپلاز', 'متالیز'],
     [form('vial-5', 'powder-for-injection', 'iv', '25 mg or 50 mg vial; 5 mg/mL after reconstitution', 5, 'mg', [R(Tk, '3'), R(Tk, '2.3')], vol=1)],
     [reg('ais', 'acute-ischemic-stroke', T('سکته ایسکمیک حاد (ظرف ۳ ساعت) — بولوس واحد بر اساس وزن، حداکثر ۲۵ mg', 'Acute ischaemic stroke (within 3 h) — single weight-based bolus, max 25 mg'), A18, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 59.99, 'perDose': 15, 'dosesPerDay': 1}, {'minWeightKg': 59.99, 'maxWeightKg': 69.99, 'perDose': 17.5, 'dosesPerDay': 1}, {'minWeightKg': 69.99, 'maxWeightKg': 79.99, 'perDose': 20, 'dosesPerDay': 1},
                           {'minWeightKg': 79.99, 'maxWeightKg': 89.99, 'perDose': 22.5, 'dosesPerDay': 1}, {'minWeightKg': 89.99, 'maxWeightKg': None, 'perDose': 25, 'dosesPerDay': 1}]},
          [R(Tk, '2.1, Table 1')], dur=ONE, notes=[note('بولوس وریدی در ۵ ثانیه. فشار خون حین و پس از تزریق کنترل شود.', 'IV bolus over 5 seconds. Monitor and control blood pressure during and after.', [R(Tk, '2.1')])]),
      reg('stemi', 'acute-coronary-syndrome', T('STEMI حاد — بولوس واحد بر اساس وزن، حداکثر ۵۰ mg', 'Acute STEMI — single weight-based bolus, max 50 mg'), A18, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 59.99, 'perDose': 30, 'dosesPerDay': 1}, {'minWeightKg': 59.99, 'maxWeightKg': 69.99, 'perDose': 35, 'dosesPerDay': 1}, {'minWeightKg': 69.99, 'maxWeightKg': 79.99, 'perDose': 40, 'dosesPerDay': 1},
                           {'minWeightKg': 79.99, 'maxWeightKg': 89.99, 'perDose': 45, 'dosesPerDay': 1}, {'minWeightKg': 89.99, 'maxWeightKg': None, 'perDose': 50, 'dosesPerDay': 1}]},
          [R(Tk, '2.2, Table 2')], dur=ONE, notes=[note('بولوس وریدی در ۵ ثانیه هرچه زودتر پس از شروع علائم. با دکستروز رسوب می‌کند — قبل و بعد با سالین شستشو.', 'IV bolus over 5 s as soon as possible after symptom onset. Precipitates with dextrose — flush with saline before and after.', [R(Tk, '2.2'), R(Tk, '2.5')])])],
     [CI('ci', 'خونریزی داخلی فعال؛ جراحی یا ترومای داخل جمجمه یا نخاع در ۲ ماه اخیر؛ اختلال خونریزی‌دهنده؛ فشار خون شدید کنترل‌نشده؛ ضایعه داخل جمجمه (تومور، AVM، آنوریسم). سکته: خونریزی فعال داخل جمجمه. STEMI: سابقه خونریزی مغزی.', 'Active internal bleeding; intracranial or intraspinal surgery or trauma within 2 months; bleeding diathesis; severe uncontrolled hypertension; intracranial lesion (neoplasm, AVM, aneurysm). Stroke: active intracranial haemorrhage. STEMI: history of intracranial haemorrhage.', [R(Tk, '4')])],
     warn=[W('خونریزی (از جمله داخل مغز)؛ آمبولی کلسترول؛ آریتمی ریپرفیوژن.', 'Bleeding (including intracranial); cholesterol embolisation; reperfusion arrhythmias.', [R(Tk, '5')])],
     exs=[ex('ais', 'vial-5', {'perDose': 20, 'mlPerDose': 4}, ageYears=65, weightKg=75), ex('stemi', 'vial-5', {'perDose': 40, 'mlPerDose': 8}, ageYears=65, weightKg=75)])

# ===================== lipids / heart failure / CKD =====================
PCSK = lambda src: [CI('hyper', 'سابقه واکنش حساسیتی جدی به دارو (از جمله آنژیوادم).', 'History of serious hypersensitivity to the drug (including angioedema).', [R(src, '4')])]
Rp = fda('repatha', 'FDA Repatha', 'Repatha (evolocumab) — Prescribing Information', sid('repatha'))
drug('evolocumab', 'cardiovascular', 'اوولوکومب', 'Evolocumab', T('مهارکننده PCSK9', 'PCSK9 inhibitor'), [{'name': 'Repatha', 'market': 'US'}], ['repatha', 'رپاتا', 'اوولوکوماب'],
     [form('pen-140', 'injection', 'sc', '140 mg/mL pen, autoinjector or syringe', 140, 'mg', [R(Rp, '3')], vol=1)],
     [NC('ldl', 'hyperlipidemia', 'هیپرکلسترولمی یا خطر بالای قلبی — ۱۴۰ mg هر ۲ هفته یا ۴۲۰ mg ماهانه', 'Hypercholesterolaemia or high CV risk — 140 mg every 2 weeks or 420 mg monthly', {'minAge': age(10, 'year')},
         'زیرجلدی ۱۴۰ mg هر ۲ هفته یا ۴۲۰ mg یک بار در ماه (نه روزانه). HeFH از ۱۰ سالگی هم همین دوز. هنگام تعویض رژیم، اولین دوز جدید در تاریخ بعدی رژیم قبلی.', '140 mg SC every 2 weeks or 420 mg once monthly (not daily). HeFH from 10 y: same dosage. When switching, give the first new dose on the next scheduled date.', [R(Rp, '2.1')])],
     PCSK(Rp))
Pl = fda('praluent', 'FDA Praluent', 'Praluent (alirocumab) — Prescribing Information', sid('praluent'))
drug('alirocumab', 'cardiovascular', 'آلیروکومب', 'Alirocumab', T('مهارکننده PCSK9', 'PCSK9 inhibitor'), [{'name': 'Praluent', 'market': 'US'}], ['praluent', 'پرالوئنت', 'آلیروکوماب'],
     [form('pen-75', 'injection', 'sc', '75 mg/mL or 150 mg/mL pen', 75, 'mg', [R(Pl, '3')], vol=1)],
     [NC('ldl', 'hyperlipidemia', 'هیپرکلسترولمی بزرگسال — ۷۵ mg هر ۲ هفته یا ۳۰۰ mg هر ۴ هفته', 'Adult hypercholesterolaemia — 75 mg every 2 weeks or 300 mg every 4 weeks', A18,
         'زیرجلدی (نه روزانه). پاسخ ناکافی: تا ۱۵۰ mg هر ۲ هفته. کودک ۸ سال به بالا با HeFH: زیر ۵۰ kg ← ۱۵۰ mg هر ۴ هفته؛ ≥۵۰ kg ← ۳۰۰ mg هر ۴ هفته.', 'SC (not daily). Inadequate response: up to 150 mg every 2 weeks. Children ≥8 y with HeFH: <50 kg → 150 mg every 4 weeks; ≥50 kg → 300 mg every 4 weeks.', [R(Pl, '2.1'), R(Pl, '2.2')])],
     PCSK(Pl))
Lq = fda('leqvio', 'FDA Leqvio', 'Leqvio (inclisiran) 284 mg/1.5 mL — Prescribing Information', sid('leqvio'))
drug('inclisiran', 'cardiovascular', 'اینکلیسیران', 'Inclisiran', T('siRNA مهارکننده PCSK9', 'PCSK9-directed siRNA'), [{'name': 'Leqvio', 'market': 'US'}], ['leqvio', 'لکویو', 'اینکلیسیران'],
     [form('syr-284', 'injection', 'sc', '284 mg/1.5 mL prefilled syringe', 284, 'mg', [R(Lq, '3')], vol=1.5)],
     [NC('ldl', 'hyperlipidemia', 'کاهش LDL (۱۲ سال به بالا) — ۲۸۴ mg، دوباره در ماه ۳، سپس هر ۶ ماه', 'LDL lowering (≥12 y) — 284 mg, again at 3 months, then every 6 months', {'minAge': age(12, 'year')},
         'تزریق زیرجلدی توسط کادر درمان: شروع، ماه ۳، سپس هر ۶ ماه. دوز فراموش‌شده کمتر از ۳ ماه: تزریق و ادامه برنامه؛ بیش از ۳ ماه: شروع برنامه جدید.', 'SC by a healthcare professional: initially, at 3 months, then every 6 months. Missed by <3 months: give and keep the schedule; >3 months: restart the schedule.', [R(Lq, '2.1')])],
     [CI('hyper', 'سابقه حساسیت جدی به اینکلیسیران (آنافیلاکسی، آنژیوادم).', 'Prior serious hypersensitivity to inclisiran (anaphylaxis, angioedema).', [R(Lq, '4')])])
Nx = fda('nexletol', 'FDA Nexletol', 'Nexletol (bempedoic acid) 180 mg — Prescribing Information', sid('nexletol'))
drug('bempedoic-acid', 'cardiovascular', 'بمپدوئیک اسید', 'Bempedoic acid', T('مهارکننده ACL (کاهش LDL)', 'ACL inhibitor (LDL-lowering)'), [{'name': 'Nexletol', 'market': 'US'}], ['nexletol', 'نکسلتول', 'بمپدوئیک'],
     [tab('tab-180', 180, '180 mg tablet', [R(Nx, '3')])],
     [reg('ldl', 'hyperlipidemia', T('هیپرکلسترولمی یا پیشگیری قلبی — ۱۸۰ mg یک بار در روز', 'Hypercholesterolaemia or CV risk reduction — 180 mg once daily'), A18, 'fixed', {'perDose': 180, 'dosesPerDay': 1}, [R(Nx, '2.1')],
          notes=[note('چربی خون ۸ تا ۱۲ هفته پس از شروع.', 'Check lipids 8–12 weeks after starting.', [R(Nx, '2.1')])])],
     [CI('hyper', 'سابقه حساسیت جدی به بمپدوئیک اسید.', 'History of serious hypersensitivity to bempedoic acid.', [R(Nx, '4')])],
     warn=[W('افزایش اسید اوریک و نقرس؛ پارگی تاندون؛ با سیمواستاتین بالای ۲۰ mg یا پراواستاتین بالای ۴۰ mg نه.', 'Hyperuricaemia and gout; tendon rupture; avoid simvastatin >20 mg or pravastatin >40 mg.', [R(Nx, '5')])],
     exs=[ex('ldl', 'tab-180', {'perDose': 180, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80)])
Vs = fda('vascepa', 'FDA Vascepa', 'Vascepa (icosapent ethyl) capsules — Prescribing Information', sid('vascepa'))
drug('icosapent-ethyl', 'cardiovascular', 'ایکوزاپنت اتیل (امگا-۳ خالص EPA)', 'Icosapent ethyl', T('اتیل استر EPA', 'EPA ethyl ester'), [{'name': 'Vascepa', 'market': 'US'}], ['vascepa', 'واسپا', 'EPA', 'ایکوزاپنت'],
     [form('cap-1g', 'capsule', 'oral', '1 g capsule (also 0.5 g)', 1, 'g', [R(Vs, '3')], per='capsule')],
     [reg('tg', 'hypertriglyceridemia', T('تری‌گلیسرید بالا یا پیشگیری قلبی — ۲ g دو بار در روز با غذا (۴ g/روز)', 'High triglycerides or CV risk reduction — 2 g twice daily with food (4 g/day)'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 2}, [R(Vs, '2.2')], unit='g',
          notes=[note('کپسول کامل بلعیده شود. رژیم غذایی و فعالیت ادامه یابد.', 'Swallow whole. Continue diet and exercise.', [R(Vs, '2.2'), R(Vs, '2.1')])])],
     [CI('hyper', 'حساسیت به ایکوزاپنت اتیل.', 'Hypersensitivity to icosapent ethyl.', [R(Vs, '4')])],
     warn=[W('فیبریلاسیون دهلیزی؛ خونریزی (به‌ویژه با ضدانعقاد)؛ احتیاط در حساسیت به ماهی.', 'Atrial fibrillation/flutter; bleeding (especially with anticoagulants); caution with fish allergy.', [R(Vs, '5')])],
     exs=[ex('tg', 'cap-1g', {'perDose': 2, 'tabletsPerDoseRounded': 2}, ageYears=60, weightKg=85)])
Kr = fda('kerendia', 'FDA Kerendia', 'Kerendia (finerenone) tablets — Prescribing Information', sid('kerendia'))
drug('finerenone', 'cardiovascular', 'فینرنون', 'Finerenone', T('آنتاگونیست غیراستروئیدی گیرنده مینرالوکورتیکوئید', 'Non-steroidal mineralocorticoid receptor antagonist'), [{'name': 'Kerendia', 'market': 'US'}], ['kerendia', 'کرندیا', 'فینرنون'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Kr, '3')]) for m in (10, 20, 40)],
     [reg('ckd', 'diabetic-nephropathy', T('بیماری مزمن کلیه با دیابت — eGFR ≥۶۰: ۲۰ mg؛ ۲۵ تا <۶۰: ۱۰ mg یک بار در روز (هدف ۲۰ mg)', 'CKD with diabetes — eGFR ≥60: 20 mg; 25–<60: 10 mg once daily (target 20 mg)'), A18, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [R(Kr, '2.2, Table 1'), R(Kr, '2.3')],
          notes=[note('پتاسیم پیش از شروع: بالای ۵ شروع نشود. افزایش به ۲۰ mg پس از ۴ هفته طبق پتاسیم و eGFR. eGFR زیر ۲۵ شروع توصیه نمی‌شود.', 'Check potassium before starting: do not start if >5.0. Increase to 20 mg after 4 weeks per potassium and eGFR. eGFR <25: initiation not recommended.', [R(Kr, '2.1'), R(Kr, '2.3')])]),
      reg('hf', 'heart-failure', T('نارسایی قلبی با LVEF ≥۴۰٪ — شروع ۱۰ یا ۲۰ mg، هدف ۲۰ یا ۴۰ mg', 'Heart failure with LVEF ≥40% — start 10 or 20 mg, target 20 or 40 mg'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [R(Kr, '2.3')],
          notes=[note('شروع بر اساس eGFR طبق جدول ۱؛ افزایش پس از ۴ هفته طبق پتاسیم و eGFR.', 'Start per eGFR (Table 1); increase after 4 weeks per potassium and eGFR.', [R(Kr, '2.2'), R(Kr, '2.3')])])],
     [CI('ci', 'حساسیت به دارو؛ مهارکننده قوی CYP3A4 همزمان؛ نارسایی آدرنال.', 'Hypersensitivity; concomitant strong CYP3A4 inhibitors; adrenal insufficiency.', [R(Kr, '4')])],
     warn=[W('هیپرکالمی — پتاسیم پیش از شروع و دوره‌ای.', 'Hyperkalaemia — check potassium before starting and periodically.', [R(Kr, '5')])],
     exs=[ex('ckd', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'upperPerDose': 20}, ageYears=60, weightKg=80), ex('hf', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1, 'upperPerDose': 40}, ageYears=70, weightKg=80)])
Vq = fda('verquvo', 'FDA Verquvo', 'Verquvo (vericiguat) tablets — Prescribing Information', sid('verquvo'))
drug('vericiguat', 'cardiovascular', 'وریسیگوات', 'Vericiguat', T('محرک گوانیلات سیکلاز محلول', 'Soluble guanylate cyclase stimulator'), [{'name': 'Verquvo', 'market': 'US'}], ['verquvo', 'ورکوو', 'وریسیگوات'],
     [tab(f'tab-{m}'.replace('.', '-'), m, f'{m} mg tablet', [R(Vq, '3')]) for m in (2.5, 5, 10)],
     [reg('hfref', 'heart-failure', T('نارسایی قلبی با EF زیر ۴۵٪ پس از بدتر شدن — شروع ۵ mg، هر ۲ هفته دو برابر تا ۱۰ mg', 'HFrEF (EF <45%) after worsening — start 5 mg, double every 2 weeks to 10 mg'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 5, 'incrementEveryDays': 14, 'max': 10}}, [R(Vq, '2.1')],
          notes=[note('با غذا. در خطر افت فشار علامت‌دار: شروع ۲٫۵ mg. زن در سن باروری: تست بارداری پیش از شروع.', 'With food. At risk of symptomatic hypotension: start 2.5 mg. Females of reproductive potential: pregnancy test before starting.', [R(Vq, '2.1'), R(Vq, '2.2')])])],
     [CI('ci', 'مصرف همزمان سایر محرک‌های گوانیلات سیکلاز محلول (ریوسیگوات)؛ بارداری.', 'Concomitant other soluble guanylate cyclase stimulators (e.g. riociguat); pregnancy.', [R(Vq, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی — رد بارداری پیش از شروع و پیشگیری مؤثر تا ۱ ماه پس از قطع.', 'Boxed warning: embryo-fetal toxicity — exclude pregnancy before starting and use effective contraception until 1 month after stopping.', [R(Vq, 'Boxed Warning')])],
     inter=[IA('pde5', 'مهارکننده‌های PDE5: توصیه نمی‌شود (افت فشار).', 'PDE5 inhibitors: not recommended (hypotension).', [R(Vq, '7')])],
     exs=[ex('hfref', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=70, weightKg=75)])
print('s11d ok')
