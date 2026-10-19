"""Stage 14c — cytotoxic chemotherapy part 2: ifosfamide, irinotecan, bleomycin, vinblastine, vinorelbine, daunorubicin, epirubicin, melphalan (Evomela),
chlorambucil, busulfan (oral), bendamustine (Bendeka), azacitidine, fludarabine, pemetrexed, temozolomide.
mg/m² regimens use type 'bsa' (Mosteller); examples use 180 cm / 80 kg (2.0 m²) unless noted."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
bsa = lambda id, dis, fa, en, pop, m2, refs, dur=ONE, notes=None, allowed=None, unit='mg': reg(id, dis, T(fa, en), pop, 'bsa', {'perM2PerDay': m2, 'dividedDoses': 1}, refs, unit=unit, dur=dur, notes=notes, allowed=allowed)
sol = lambda id, mg, label, src, sec='3', unit='mg': form(id, 'injection', 'iv', label, mg, unit, [R(src, sec)], vol=1)
pw = lambda id, mg, label, src, sec='3', unit='mg': form(id, 'powder-for-injection', 'iv', label, mg, unit, [R(src, sec)], per='vial')
X = lambda r, f, mg, ml=None, **k: ex(r, f, {'perDose': mg, **({'mlPerDose': ml} if ml is not None else {})}, ageYears=k.get('age', 55), weightKg=k.get('w', 80), heightCm=k.get('h', 180))
ONC = ('فقط زیر نظر پزشک متخصص شیمی‌درمانی و در مرکز مجهز. عدد ماشین‌حساب = mg/m² برچسب × سطح بدن (Mosteller)؛ پروتکل، فاصله دوره‌ها، تنظیم بر اساس CBC و عملکرد کلیه/کبد با تیم انکولوژی.',
       'Only under an oncologist in an equipped centre. Calculator = label mg/m² × BSA (Mosteller); protocol, cycle interval and adjustment for CBC and renal/hepatic function rest with the oncology team.')
onc = lambda src, sec: note(*ONC, [R(src, sec)])
D = lambda n: {'min': n, 'max': n}

add_disease('hodgkin-lymphoma', 'لنفوم هوچکین', 'Hodgkin lymphoma', ['hodgkin', 'هوچکین', 'لنفوم هاجکین'], ['C81.90'], 'oncology')
add_disease('chronic-lymphocytic-leukemia', 'لوسمی لنفوسیتی مزمن (CLL)', 'Chronic lymphocytic leukaemia (CLL)', ['CLL', 'لوسمی لنفوسیتیک مزمن', 'سی ال ال'], ['C91.10'], 'oncology')
add_disease('chronic-myeloid-leukemia', 'لوسمی میلوئید مزمن (CML)', 'Chronic myeloid leukaemia (CML)', ['CML', 'لوسمی میلوئیدی مزمن', 'فیلادلفیا مثبت'], ['C92.10'], 'oncology')
add_disease('malignant-glioma', 'گلیوبلاستوم و آستروسیتوم آناپلاستیک', 'Glioblastoma and anaplastic astrocytoma', ['glioblastoma', 'GBM', 'گلیوبلاستوما', 'تومور مغزی'], ['C71.9'], 'oncology')
add_disease('mesothelioma', 'مزوتلیومای بدخیم پلور', 'Malignant pleural mesothelioma', ['mesothelioma', 'مزوتلیوما', 'سرطان پرده جنب'], ['C45.0'], 'oncology')

If = fda('ifosfamide', 'FDA Ifosfamide', 'Ifosfamide for injection 1 g and 3 g — Prescribing Information', sid('ifosfamide'))
drug('ifosfamide', 'antineoplastic-immunomodulating', 'ایفوسفامید', 'Ifosfamide', T('عامل آلکیله‌کننده', 'Alkylating agent'), [{'name': 'Ifex', 'market': 'US'}], ['ifex', 'holoxan', 'هولوکسان', 'ایفوسفامید'],
     [pw('vial-1g', 1000, '1 g vial (also 3 g)', If)],
     [bsa('testis', 'testicular-cancer', 'سرطان بیضه ژرم‌سل (خط سوم، ترکیبی) — ۱٫۲ g/m²/روز وریدی آهسته ۵ روز متوالی، هر ۳ هفته', 'Germ-cell testicular cancer (third line, combination) — 1.2 g/m²/day slow IV for 5 consecutive days, every 3 weeks', A18, 1200, [R(If, '2.2')], dur=D(5),
          notes=[onc(If, '2.2'), note('همیشه همراه مسنا و هیدراتاسیون حداقل ۲ لیتر در روز (پیشگیری از سیستیت هموراژیک). انفوزیون حداقل ۳۰ دقیقه.', 'Always with mesna and at least 2 L/day hydration (haemorrhagic cystitis prevention). Infuse over at least 30 min.', [R(If, '2.1')])])],
     [CI('ci', 'حساسیت به ایفوسفامید؛ انسداد مجرای خروجی ادرار.', 'Hypersensitivity to ifosfamide; urinary outflow obstruction.', [R(If, '4')])],
     warn=[W('هشدار جعبه‌ای: سرکوب مغز استخوان، انسفالوپاتی (گاه کشنده)، نفروتوکسیسیتی و سیستیت هموراژیک.', 'Boxed warning: myelosuppression, encephalopathy (sometimes fatal), nephrotoxicity and haemorrhagic cystitis.', [R(If, 'Boxed Warning')]),
           W('سمیت قلب و ریه؛ بدخیمی ثانویه؛ بیماری انسدادی وریدهای کبد؛ سمیت جنینی؛ ناباروری.', 'Cardiac and pulmonary toxicity; secondary malignancy; hepatic veno-occlusive disease; embryo-fetal toxicity; infertility.', [R(If, '5')])],
     exs=[X('testis', 'vial-1g', 2400)])

Ir = fda('irinotecan', 'FDA Irinotecan', 'Irinotecan hydrochloride injection 20 mg/mL — Prescribing Information', sid('irinotecan'))
drug('irinotecan', 'antineoplastic-immunomodulating', 'ایرینوتکان', 'Irinotecan', T('مهارکننده توپوایزومراز I', 'Topoisomerase I inhibitor'), [{'name': 'Camptosar', 'market': 'US'}], ['camptosar', 'campto', 'کمپتو', 'ایرینوتکان'],
     [sol('inj-20', 20, '20 mg/mL (40 mg/2 mL, 100 mg/5 mL)', Ir)],
     [bsa('weekly', 'colorectal-cancer', 'سرطان کولورکتال (ترکیبی رژیم ۱، با LV/5-FU) — ۱۲۵ mg/m² وریدی ۹۰ دقیقه، روز ۱، ۸، ۱۵، ۲۲ هر ۶ هفته', 'Colorectal cancer (combination regimen 1, with LV/5-FU) — 125 mg/m² IV over 90 min on days 1, 8, 15, 22 every 6 weeks', A18, 125, [R(Ir, '2.1, Table 1')],
          notes=[onc(Ir, '2.1'), note('تک‌دارویی هفتگی هم ۱۲۵ mg/m² (روز ۱، ۸، ۱۵، ۲۲ هر ۶ هفته). UGT1A1*28 هموزیگوت: کاهش یک سطح دوز.', 'Single-agent weekly is also 125 mg/m² (days 1, 8, 15, 22 every 6 weeks). UGT1A1*28 homozygous: reduce by one dose level.', [R(Ir, '2.2, Table 3'), R(Ir, '2.3')])]),
      bsa('q2w', 'colorectal-cancer', 'سرطان کولورکتال (ترکیبی رژیم ۲، با LV/5-FU) — ۱۸۰ mg/m² روز ۱، ۱۵، ۲۹ هر ۶ هفته', 'Colorectal cancer (combination regimen 2, with LV/5-FU) — 180 mg/m² on days 1, 15, 29 every 6 weeks', A18, 180, [R(Ir, '2.1, Table 1')], notes=[onc(Ir, '2.1')]),
      bsa('q3w', 'colorectal-cancer', 'سرطان کولورکتال تک‌دارویی (رژیم ۲) — ۳۵۰ mg/m² وریدی هر ۳ هفته', 'Colorectal cancer single agent (regimen 2) — 350 mg/m² IV every 3 weeks', A18, 350, [R(Ir, '2.2, Table 3')], notes=[onc(Ir, '2.2')])],
     [CI('hyper', 'حساسیت به ایرینوتکان یا اجزا.', 'Hypersensitivity to irinotecan or excipients.', [R(Ir, '4')])],
     warn=[W('هشدار جعبه‌ای: اسهال زودرس (کولینرژیک — آتروپین) و دیررس تهدیدکننده حیات (لوپرامید فوری)؛ سرکوب شدید مغز استخوان.', 'Boxed warning: early (cholinergic — atropine) and late life-threatening diarrhoea (prompt loperamide); severe myelosuppression.', [R(Ir, 'Boxed Warning')]),
           W('نوتروپنی بیشتر با کاهش فعالیت UGT1A1؛ حساسیت؛ نارسایی کلیه؛ سمیت ریوی؛ سمیت جنینی.', 'Higher neutropenia risk with reduced UGT1A1 activity; hypersensitivity; renal failure; pulmonary toxicity; embryo-fetal toxicity.', [R(Ir, '5')])],
     exs=[X('weekly', 'inj-20', 250, 12.5), X('q2w', 'inj-20', 360, 18), X('q3w', 'inj-20', 700, 35)])

Bl = fda('bleomycin', 'FDA Bleomycin', 'Bleomycin for injection 15 and 30 units — Prescribing Information', sid('bleomycin')); d = R(Bl, 'Dosage and Administration')
drug('bleomycin', 'antineoplastic-immunomodulating', 'بلئومایسین', 'Bleomycin', T('آنتی‌بیوتیک ضدتومور', 'Antitumour antibiotic'), [{'name': 'Blenoxane', 'market': 'US'}], ['blenoxane', 'بلنوکسان', 'بلئومایسین', 'bleo'],
     [pw('vial-30', 30, '30 units vial (also 15 units)', Bl, 'How Supplied', unit='unit')],
     [bsa('tumour', 'testicular-cancer', 'سرطان بیضه، لنفوم هوچکین و غیرهوچکین، سلول سنگفرشی — ۱۰ تا ۲۰ واحد/m² (۰٫۲۵ تا ۰٫۵ واحد/kg) هفته‌ای ۱ یا ۲ بار', 'Testicular carcinoma, Hodgkin and non-Hodgkin lymphoma, squamous cell carcinoma — 10–20 units/m² (0.25–0.5 units/kg) once or twice weekly', A18, 10, [d], unit='unit',
          notes=[onc(Bl, 'Dosage and Administration'), note('عدد ماشین‌حساب حد پایین است. لنفوم: ۲ دوز اول ۲ واحد یا کمتر (واکنش آنافیلاکتوئید). سمیت ریه با دوز کل بالای ۴۰۰ واحد به‌شدت بیشتر می‌شود.', 'Calculator gives the lower bound. Lymphoma: first 2 doses 2 units or less (anaphylactoid reaction). Pulmonary toxicity rises sharply above 400 units total.', [d])])],
     [CI('hyper', 'سابقه واکنش حساسیتی یا ایدیوسنکراتیک به بلئومایسین.', 'Prior hypersensitive or idiosyncratic reaction to bleomycin.', [R(Bl, 'Contraindications')])],
     warn=[W('سمیت ریوی (پنومونیت تا فیبروز، حدود ۱۰٪)؛ واکنش ایدیوسنکراتیک شبیه آنافیلاکسی در لنفوم؛ احتیاط در نارسایی کلیه یا ریه.', 'Pulmonary toxicity (pneumonitis to fibrosis, about 10%); idiosyncratic anaphylaxis-like reactions in lymphoma; caution in renal or pulmonary impairment.', [R(Bl, 'Warnings')])],
     exs=[X('tumour', 'vial-30', 20)])

Vb = fda('vinblastine', 'FDA Vinblastine', 'Vinblastine sulfate injection 1 mg/mL — Prescribing Information', sid('vinblastine')); d = R(Vb, 'Dosage and Administration')
drug('vinblastine', 'antineoplastic-immunomodulating', 'وین‌بلاستین', 'Vinblastine', T('آلکالوئید وینکا', 'Vinca alkaloid'), [{'name': 'Velban', 'market': 'US'}], ['velban', 'ولبان', 'وینبلاستین'],
     [sol('inj-1', 1, '1 mg/mL, 10 mL vial', Vb, 'How Supplied')],
     [bsa('start', 'hodgkin-lymphoma', 'لنفوم هوچکین، سرطان بیضه و سایر بدخیمی‌های پاسخ‌ده (تسکینی) — دوز اول ۳٫۷ mg/m² وریدی، سپس افزایش هفتگی', 'Hodgkin lymphoma, testicular cancer and other responsive malignancies (palliative) — first dose 3.7 mg/m² IV, then weekly increments', A18, 3.7, [d],
          notes=[onc(Vb, 'Dosage and Administration'), note('افزایش هفتگی بر اساس WBC: ۵٫۵، ۷٫۴، ۹٫۲۵، ۱۱٫۱ mg/m²؛ حداکثر ۱۸٫۵ mg/m². فقط وریدی — تزریق داخل نخاعی کشنده است.', 'Weekly increments by WBC: 5.5, 7.4, 9.25, 11.1 mg/m²; max 18.5 mg/m². IV only — intrathecal injection is fatal.', [d])])],
     [CI('ci', 'گرانولوسیتوپنی قابل‌توجه (مگر ناشی از خود بیماری)؛ عفونت باکتریال کنترل‌نشده.', 'Significant granulocytopenia (unless due to the disease treated); uncontrolled bacterial infection.', [R(Vb, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: فقط وریدی — تزریق از راه دیگر کشنده است. نشت از رگ باعث آسیب شدید بافت می‌شود.', 'Boxed warning: IV only — fatal if given by other routes. Extravasation causes severe tissue injury.', [R(Vb, 'Boxed Warning'), R(Vb, 'Warnings')])],
     exs=[X('start', 'inj-1', 7.4, 7.4)])

Vn = fda('vinorelbine', 'FDA Vinorelbine', 'Vinorelbine injection 10 mg/mL — Prescribing Information', sid('vinorelbine'))
drug('vinorelbine', 'antineoplastic-immunomodulating', 'وینورلبین', 'Vinorelbine', T('آلکالوئید وینکا', 'Vinca alkaloid'), [{'name': 'Navelbine', 'market': 'US'}], ['navelbine', 'ناولبین', 'وینورلبین'],
     [sol('inj-10', 10, '10 mg/mL (10 mg/1 mL, 50 mg/5 mL)', Vn)],
     [bsa('nsclc', 'lung-cancer', 'سرطان ریه غیرسلول کوچک — ۳۰ mg/m² وریدی هفته‌ای یک بار (تک‌دارویی یا با سیس‌پلاتین ۲۵ تا ۳۰)', 'Non-small-cell lung cancer — 30 mg/m² IV once weekly (single agent, or 25–30 with cisplatin)', A18, 30, [R(Vn, '2.1')],
          notes=[onc(Vn, '2.1'), note('با کاهش نوتروفیل یا افزایش بیلی‌روبین طبق جداول ۲.۲ کم یا قطع شود. فقط وریدی.', 'Reduce or withhold for low neutrophils or raised bilirubin per 2.2 tables. IV only.', [R(Vn, '2.2')])])],
     [],
     warn=[W('هشدار جعبه‌ای: سرکوب شدید مغز استخوان (عفونت، شوک سپتیک، مرگ).', 'Boxed warning: severe myelosuppression (infection, septic shock, death).', [R(Vn, 'Boxed Warning')]),
           W('سمیت کبدی؛ یبوست شدید و انسداد روده؛ نشت از رگ؛ نوروپاتی؛ سمیت ریوی؛ سمیت جنینی.', 'Hepatotoxicity; severe constipation and bowel obstruction; extravasation; neuropathy; pulmonary toxicity; embryo-fetal toxicity.', [R(Vn, '5')])],
     exs=[X('nsclc', 'inj-10', 60, 6)])

Dn = fda('daunorubicin', 'FDA Daunorubicin', 'Daunorubicin hydrochloride injection 5 mg/mL — Prescribing Information', sid('daunorubicin')); d = R(Dn, 'Dosage and Administration')
drug('daunorubicin', 'antineoplastic-immunomodulating', 'داونوروبیسین', 'Daunorubicin', T('آنتراسایکلین', 'Anthracycline'), [{'name': 'Cerubidine', 'market': 'US'}], ['cerubidine', 'daunomycin', 'داونومایسین', 'داونوروبیسین'],
     [sol('inj-5', 5, '5 mg/mL (20 mg/4 mL, 50 mg/10 mL)', Dn, 'How Supplied')],
     [bsa('aml', 'acute-myeloid-leukemia', 'القای AML بزرگسال زیر ۶۰ سال — ۴۵ mg/m²/روز وریدی روز ۱ تا ۳ (دوره‌های بعد روز ۱ و ۲) با سیتارابین', 'AML induction, adults under 60 — 45 mg/m²/day IV on days 1–3 (later courses days 1–2) with cytarabine', {'minAge': age(18, 'year'), 'maxAge': age(60, 'year')}, 45, [d], dur=D(3), notes=[onc(Dn, 'Dosage and Administration')]),
      bsa('aml-60', 'acute-myeloid-leukemia', 'القای AML ۶۰ سال و بالاتر — ۳۰ mg/m²/روز روز ۱ تا ۳ با سیتارابین', 'AML induction, 60 years and over — 30 mg/m²/day on days 1–3 with cytarabine', {'minAge': age(60, 'year')}, 30, [d], dur=D(3), notes=[onc(Dn, 'Dosage and Administration')])],
     [CI('hyper', 'حساسیت به داونوروبیسین.', 'Hypersensitivity to daunorubicin.', [R(Dn, 'Contraindications')])],
     warn=[W('سمیت قلبی با دوز تجمعی بالای ۴۰۰ تا ۵۵۰ mg/m² در بزرگسال (۳۰۰ mg/m² در کودک بالای ۲ سال، ۱۰ mg/kg زیر ۲ سال)؛ سرکوب شدید مغز استخوان؛ فقط توسط پزشک باتجربه در لوسمی.', 'Cardiotoxicity above cumulative 400–550 mg/m² in adults (300 mg/m² in children over 2, 10 mg/kg under 2); severe myelosuppression; only by physicians experienced in leukaemia therapy.', [R(Dn, 'Warnings')])],
     exs=[X('aml', 'inj-5', 90, 18), X('aml-60', 'inj-5', 60, 12, age=65)])

El = fda('ellence', 'FDA Ellence', 'Ellence (epirubicin hydrochloride) injection 2 mg/mL — Prescribing Information', sid('epirubicin'))
drug('epirubicin', 'antineoplastic-immunomodulating', 'اپی‌روبیسین', 'Epirubicin', T('آنتراسایکلین', 'Anthracycline'), [{'name': 'Ellence', 'market': 'US'}], ['ellence', 'pharmorubicin', 'اپیروبیسین'],
     [sol('inj-2', 2, '2 mg/mL (50 mg/25 mL, 200 mg/100 mL)', El)],
     [bsa('breast', 'breast-cancer', 'سرطان پستان کمکی (گره مثبت) — ۱۰۰ تا ۱۲۰ mg/m² وریدی هر ۳ تا ۴ هفته (روز ۱ یا تقسیم روز ۱ و ۸)', 'Adjuvant node-positive breast cancer — 100–120 mg/m² IV every 3–4 weeks (day 1, or split days 1 and 8)', A18, 100, [R(El, '2.2')],
          notes=[onc(El, '2.2'), note('عدد ماشین‌حساب حد پایین است. CEF-120: ۶۰ mg/m² روز ۱ و ۸؛ FEC-100: ۱۰۰ mg/m² روز ۱.', 'Calculator gives the lower bound. CEF-120: 60 mg/m² days 1 and 8; FEC-100: 100 mg/m² day 1.', [R(El, '2.2')])])],
     [CI('ci', 'نارسایی شدید میوکارد؛ انفارکتوس اخیر یا آریتمی شدید؛ دریافت قبلی حداکثر دوز تجمعی آنتراسایکلین؛ سرکوب پایدار شدید مغز استخوان؛ نارسایی شدید کبد (Child-Pugh C یا بیلی‌روبین بالای ۵)؛ حساسیت شدید به آنتراسایکلین‌ها.',
         'Severe myocardial insufficiency; recent MI or severe arrhythmias; prior maximum cumulative anthracycline dose; severe persistent myelosuppression; severe hepatic impairment (Child-Pugh C or bilirubin >5 mg/dL); severe hypersensitivity to anthracyclines.', [R(El, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت قلبی وابسته به دوز تجمعی (۰٫۹٪ در ۵۵۰ mg/m² تا ۳٫۳٪ در ۹۰۰)؛ بدخیمی ثانویه (AML)؛ نکروز بافت با نشت؛ سرکوب شدید مغز استخوان.', 'Boxed warning: cumulative-dose cardiotoxicity (0.9% at 550 mg/m² to 3.3% at 900); secondary malignancies (AML); tissue necrosis with extravasation; severe myelosuppression.', [R(El, 'Boxed Warning')])],
     exs=[X('breast', 'inj-2', 200, 100)])

Ev = fda('evomela', 'FDA Evomela', 'Evomela (melphalan) for injection 50 mg — Prescribing Information', sid('melphalan'))
drug('melphalan', 'antineoplastic-immunomodulating', 'ملفالان', 'Melphalan', T('عامل آلکیله‌کننده', 'Alkylating agent'), [{'name': 'Evomela', 'market': 'US'}, {'name': 'Alkeran', 'market': 'US'}], ['evomela', 'alkeran', 'آلکران', 'ملفالان'],
     [pw('vial-50', 50, '50 mg vial', Ev)],
     [bsa('asct', 'multiple-myeloma', 'آماده‌سازی پیش از پیوند اتولوگ در مولتیپل میلوما — ۱۰۰ mg/m²/روز وریدی ۳۰ دقیقه، روز ‎-۳ و ‎-۲', 'Conditioning before autologous stem-cell transplant in multiple myeloma — 100 mg/m²/day IV over 30 min on days −3 and −2', A18, 100, [R(Ev, '2.1')], dur=D(2),
          notes=[onc(Ev, '2.1'), note('وزن بالای ۱۳۰٪ وزن ایده‌آل: سطح بدن با وزن ایده‌آل تعدیل‌شده.', 'Weight above 130% of ideal: compute BSA from adjusted ideal body weight.', [R(Ev, '2.1')])])],
     [CI('hyper', 'سابقه واکنش آلرژیک جدی به ملفالان.', 'History of serious allergic reaction to melphalan.', [R(Ev, '4')])],
     warn=[W('هشدار جعبه‌ای: سرکوب شدید مغز استخوان؛ حساسیت (آنافیلاکسی ~۲٪)؛ لوسمی ثانویه.', 'Boxed warning: severe bone-marrow suppression; hypersensitivity (anaphylaxis ~2%); secondary leukaemia.', [R(Ev, 'Boxed Warning')]),
           W('سمیت گوارشی؛ سمیت کبدی؛ سمیت جنینی؛ ناباروری.', 'GI toxicity; hepatotoxicity; embryo-fetal toxicity; infertility.', [R(Ev, '5')])],
     exs=[X('asct', 'vial-50', 200)])

Lk = fda('leukeran', 'FDA Leukeran', 'Leukeran (chlorambucil) tablets 2 mg — Prescribing Information', sid('chlorambucil')); d = R(Lk, 'Dosage and Administration')
drug('chlorambucil', 'antineoplastic-immunomodulating', 'کلرامبوسیل', 'Chlorambucil', T('عامل آلکیله‌کننده خوراکی', 'Oral alkylating agent'), [{'name': 'Leukeran', 'market': 'US'}], ['leukeran', 'لوکران', 'کلرامبوسیل'],
     [tab('tab-2', 2, '2 mg tablet', [R(Lk, 'How Supplied')])],
     [reg('cll', 'chronic-lymphocytic-leukemia', T('CLL و لنفوم‌های بدخیم (تسکینی) — ۰٫۱ تا ۰٫۲ mg/kg خوراکی روزانه ۳ تا ۶ هفته', 'CLL and malignant lymphomas (palliative) — 0.1–0.2 mg/kg orally daily for 3–6 weeks'), A18, 'weightBased', {'perKgPerDay': 0.1, 'perKgPerDayMax': 0.2, 'dividedDoses': 1}, [d], dur={'min': 21, 'max': 42},
          notes=[note('معمولاً ۴ تا ۱۰ mg در روز؛ کل دوز یکجا. با پاسخ و شمارش خون تنظیم و در صورت افت کاهش یابد.', 'Usually 4–10 mg/day; whole dose at once. Adjust to response and counts; reduce if counts fall.', [d])])],
     [CI('ci', 'مقاومت قبلی بیماری به کلرامبوسیل؛ حساسیت به کلرامبوسیل (حساسیت متقاطع پوستی با سایر آلکیله‌کننده‌ها).', 'Prior disease resistance to chlorambucil; hypersensitivity (possible cross skin hypersensitivity with other alkylators).', [R(Lk, 'Contraindications')])],
     warn=[W('سرطان‌زا — فقط برای CLL یا لنفوم. تشنج، ناباروری، لوسمی و بدخیمی ثانویه؛ سرکوب مغز استخوان.', 'Carcinogenic — only for CLL or lymphoma. Seizures, infertility, leukaemia and secondary malignancy; bone-marrow suppression.', [R(Lk, 'Warnings')])],
     exs=[ex('cll', 'tab-2', {'perDose': 8, 'tabletsPerDoseRounded': 4, 'upperPerDose': 16}, ageYears=65, weightKg=80)])

My = fda('myleran', 'FDA Myleran', 'Myleran (busulfan) tablets 2 mg — Prescribing Information', sid('busulfan')); d = R(My, 'Dosage and Administration')
drug('busulfan', 'antineoplastic-immunomodulating', 'بوسولفان', 'Busulfan', T('عامل آلکیله‌کننده', 'Alkylating agent'), [{'name': 'Myleran', 'market': 'US'}], ['myleran', 'busulfex', 'مایلران', 'بوسولفان'],
     [tab('tab-2', 2, '2 mg tablet', [R(My, 'How Supplied')])],
     [reg('cml', 'chronic-myeloid-leukemia', T('CML (تسکینی) — القای بهبود: ۴ تا ۸ mg خوراکی روزانه (حدود ۶۰ mcg/kg یا ۱٫۸ mg/m²)', 'CML (palliative) — remission induction: 4–8 mg orally daily (about 60 mcg/kg or 1.8 mg/m²)'), {}, 'fixed', {'perDose': 4, 'perDoseMax': 8, 'dosesPerDay': 1}, [d],
          notes=[note('سرعت افت WBC به دوز وابسته است؛ دوز بالای ۴ mg/روز فقط با پاسخ کافی نیاز. کودک: همان دوز وزنی. شمارش خون هفتگی.', 'WBC fall is dose-related; above 4 mg/day only if response is insufficient. Children: same weight-based dose. Weekly counts.', [d])])],
     [CI('ci', 'CML بدون تشخیص قطعی؛ سابقه حساسیت به بوسولفان.', 'CML diagnosis not firmly established; prior hypersensitivity to busulfan.', [R(My, 'Contraindications')])],
     warn=[W('نارسایی مغز استخوان و پان‌سیتوپنی طولانی؛ فیبروز ریه؛ بدخیمی ثانویه.', 'Bone-marrow failure and prolonged pancytopenia; pulmonary fibrosis; secondary malignancy.', [R(My, 'Warnings')])],
     exs=[ex('cml', 'tab-2', {'perDose': 4, 'tabletsPerDoseRounded': 2, 'upperPerDose': 8}, ageYears=50, weightKg=70)])

Bd = fda('bendeka', 'FDA Bendeka', 'Bendeka (bendamustine hydrochloride) injection 25 mg/mL — Prescribing Information', sid('bendamustine'))
drug('bendamustine', 'antineoplastic-immunomodulating', 'بنداموستین', 'Bendamustine', T('عامل آلکیله‌کننده', 'Alkylating agent'), [{'name': 'Bendeka', 'market': 'US'}, {'name': 'Treanda', 'market': 'US'}], ['bendeka', 'treanda', 'ribomustin', 'ریبوموستین', 'بنداموستین'],
     [sol('inj-25', 25, '25 mg/mL, 100 mg/4 mL multiple-dose vial', Bd)],
     [bsa('cll', 'chronic-lymphocytic-leukemia', 'CLL — ۱۰۰ mg/m² وریدی ۱۰ دقیقه، روز ۱ و ۲ هر ۲۸ روز، تا ۶ دوره', 'CLL — 100 mg/m² IV over 10 min on days 1 and 2 every 28 days, up to 6 cycles', A18, 100, [R(Bd, '2.1')], dur=D(2), notes=[onc(Bd, '2.1')]),
      bsa('nhl', 'b-cell-lymphoma', 'لنفوم غیرهوچکین سلول B ایندولنت پیشرفته پس از ریتوکسیماب — ۱۲۰ mg/m² روز ۱ و ۲ هر ۲۱ روز، تا ۸ دوره', 'Indolent B-cell NHL progressing after rituximab — 120 mg/m² on days 1 and 2 every 21 days, up to 8 cycles', A18, 120, [R(Bd, '2.2')], dur=D(2), notes=[onc(Bd, '2.2')])],
     [CI('hyper', 'حساسیت به بنداموستین، پلی‌اتیلن گلیکول ۴۰۰، پروپیلن گلیکول یا مونوتیوگلیسرول.', 'Hypersensitivity to bendamustine, polyethylene glycol 400, propylene glycol or monothioglycerol.', [R(Bd, '4')])],
     warn=[W('سرکوب مغز استخوان؛ عفونت (شامل PML)؛ آنافیلاکسی و واکنش انفوزیون؛ سندرم لیز تومور؛ واکنش پوستی شدید؛ سمیت کبدی؛ بدخیمی دیگر؛ آسیب نشت؛ سمیت جنینی.', 'Myelosuppression; infections (including PML); anaphylaxis and infusion reactions; tumour lysis syndrome; severe skin reactions; hepatotoxicity; other malignancies; extravasation injury; embryo-fetal toxicity.', [R(Bd, '5')])],
     exs=[X('cll', 'inj-25', 200, 8), X('nhl', 'inj-25', 240, 9.6)])

Vz = fda('vidaza', 'FDA Vidaza', 'Vidaza (azacitidine) for injection 100 mg — Prescribing Information', sid('azacitidine'))
drug('azacitidine', 'antineoplastic-immunomodulating', 'آزاسیتیدین', 'Azacitidine', T('عامل هیپومتیله‌کننده', 'Hypomethylating agent'), [{'name': 'Vidaza', 'market': 'US'}], ['vidaza', 'ویدازا', 'آزاسیتیدین'],
     [form('vial-100', 'powder-for-injection', 'sc', '100 mg vial (25 mg/mL after reconstitution for SC)', 100, 'mg', [R(Vz, '3')], per='vial')],
     [bsa('mds', 'myelodysplastic-syndrome', 'سندرم میلودیسپلاستیک بزرگسال — ۷۵ mg/m² زیرجلدی یا وریدی روزانه ۷ روز، هر ۴ هفته', 'Myelodysplastic syndromes, adults — 75 mg/m² SC or IV daily for 7 days every 4 weeks', A18, 75, [R(Vz, '2.2'), R(Vz, '2.3')], dur=D(7),
          notes=[onc(Vz, '2.2'), note('پس از ۲ دوره بدون پاسخ و بدون سمیت (جز تهوع) تا ۱۰۰ mg/m². حداقل ۴ تا ۶ دوره. با آزاسیتیدین خوراکی جایگزین نشود.', 'May increase to 100 mg/m² after 2 cycles without benefit or toxicity (other than nausea). At least 4–6 cycles. Not interchangeable with oral azacitidine.', [R(Vz, '2.3'), R(Vz, '2.1')])])],
     [CI('liver', 'تومورهای بدخیم پیشرفته کبد.', 'Advanced malignant hepatic tumours.', [R(Vz, '4.1')]), CI('hyper', 'حساسیت به آزاسیتیدین یا مانیتول.', 'Hypersensitivity to azacitidine or mannitol.', [R(Vz, '4.2')])],
     warn=[W('کم‌خونی، نوتروپنی و ترومبوسیتوپنی؛ سمیت کبدی در نارسایی شدید کبد؛ سمیت کلیه؛ سندرم لیز تومور؛ سمیت جنینی.', 'Anaemia, neutropenia and thrombocytopenia; hepatotoxicity with severe hepatic impairment; renal toxicity; tumour lysis syndrome; embryo-fetal toxicity.', [R(Vz, '5')])],
     exs=[X('mds', 'vial-100', 150, age=70)])

Fl = fda('fludarabine', 'FDA Fludarabine', 'Fludarabine phosphate injection 25 mg/mL — Prescribing Information', sid('fludarabine'))
drug('fludarabine', 'antineoplastic-immunomodulating', 'فلودارابین', 'Fludarabine', T('آنتی‌متابولیت پورینی', 'Purine antimetabolite'), [{'name': 'Fludara', 'market': 'US'}], ['fludara', 'فلودارا', 'فلودارابین'],
     [sol('inj-25', 25, '25 mg/mL, 50 mg/2 mL vial', Fl)],
     [bsa('cll', 'chronic-lymphocytic-leukemia', 'CLL سلول B (همراه سیکلوفسفامید و ریتوکسیماب) — ۲۵ mg/m² وریدی ۳۰ دقیقه، روز ۱ تا ۳ هر ۲۸ روز، ۶ دوره', 'B-cell CLL (with cyclophosphamide and rituximab) — 25 mg/m² IV over 30 min on days 1–3 every 28 days, 6 cycles', A18, 25, [R(Fl, '2.1')], dur=D(3), notes=[onc(Fl, '2.1')])],
     [],
     warn=[W('سمیت عصبی وابسته به دوز (کما، تشنج)؛ سرکوب مغز استخوان؛ سیتوپنی خودایمنی؛ GVHD ناشی از تزریق خون (فقط خون اشعه‌دیده)؛ سندرم لیز تومور؛ سمیت ریوی با پنتوستاتین؛ واکسن زنده ممنوع؛ سمیت جنینی.', 'Dose-dependent neurotoxicity (coma, seizures); myelosuppression; autoimmune cytopenias; transfusion-associated GVHD (irradiated blood only); tumour lysis syndrome; pulmonary toxicity with pentostatin; no live vaccines; embryo-fetal toxicity.', [R(Fl, '5')])],
     renal=[{'egfrBelow': 80, 'severity': 'warn', 'text': T('ClCr ۵۰ تا ۷۹: ۲۰ mg/m²؛ ۳۰ تا ۴۹: ۱۵ mg/m²؛ زیر ۳۰: طبق جدول ۱.', 'CrCl 50–79: 20 mg/m²; 30–49: 15 mg/m²; under 30: per Table 1.'), 'refs': [R(Fl, '2.2, Table 1')]}],
     exs=[X('cll', 'inj-25', 50, 2, age=65)])

Al = fda('alimta', 'FDA Alimta', 'Alimta (pemetrexed) for injection — Prescribing Information', sid('pemetrexed'))
PEM = note('پیش‌درمان: اسید فولیک ۴۰۰ تا ۱۰۰۰ mcg روزانه از ۷ روز قبل، ویتامین B12 عضلانی هر ۹ هفته، دگزامتازون ۴ mg دو بار در روز قبل، روز و بعد از تزریق.', 'Premedication: folic acid 400–1000 mcg daily from 7 days before, vitamin B12 IM every 9 weeks, dexamethasone 4 mg twice daily the day before, of and after.', [R(Al, '2.4')])
drug('pemetrexed', 'antineoplastic-immunomodulating', 'پمترکسد', 'Pemetrexed', T('آنتی‌متابولیت آنتی‌فولات', 'Antifolate antimetabolite'), [{'name': 'Alimta', 'market': 'US'}], ['alimta', 'آلیمتا', 'پمترکسد'],
     [pw('vial-500', 500, '500 mg vial (also 100 mg)', Al)],
     [bsa('nsclc', 'lung-cancer', 'سرطان ریه غیرسلول کوچک غیرسنگفرشی — ۵۰۰ mg/m² وریدی ۱۰ دقیقه، روز ۱ هر ۲۱ روز', 'Non-squamous NSCLC — 500 mg/m² IV over 10 min on day 1 every 21 days', A18, 500, [R(Al, '2.1')], notes=[onc(Al, '2.1'), PEM]),
      bsa('meso', 'mesothelioma', 'مزوتلیومای پلور (با سیس‌پلاتین) — ۵۰۰ mg/m² روز ۱ هر ۲۱ روز', 'Pleural mesothelioma (with cisplatin) — 500 mg/m² on day 1 every 21 days', A18, 500, [R(Al, '2.2')], notes=[onc(Al, '2.2'), PEM])],
     [CI('hyper', 'سابقه واکنش حساسیتی شدید به پمترکسد.', 'History of severe hypersensitivity to pemetrexed.', [R(Al, '4')])],
     warn=[W('سرکوب مغز استخوان (کمتر با فولات و B12)؛ نارسایی کلیه؛ واکنش پوستی تاولی؛ پنومونیت بینابینی؛ تداخل با ایبوپروفن؛ سمیت جنینی.', 'Myelosuppression (reduced with folate and B12); renal failure; bullous skin toxicity; interstitial pneumonitis; ibuprofen interaction; embryo-fetal toxicity.', [R(Al, '5')])],
     renal=[{'egfrBelow': 45, 'severity': 'block', 'text': T('ClCr زیر ۴۵: دوز توصیه‌شده‌ای نیست — تجویز نشود.', 'CrCl below 45: no recommended dose — do not give.'), 'refs': [R(Al, '2.3')]}],
     exs=[X('nsclc', 'vial-500', 1000), X('meso', 'vial-500', 1000)])

Tm = fda('temodar', 'FDA Temodar', 'Temodar (temozolomide) capsules and injection — Prescribing Information', sid('temozolomide'))
drug('temozolomide', 'antineoplastic-immunomodulating', 'تموزولوماید', 'Temozolomide', T('عامل آلکیله‌کننده خوراکی', 'Oral alkylating agent'), [{'name': 'Temodar', 'market': 'US'}], ['temodar', 'temodal', 'تمودال', 'تموزولوماید'],
     [tab(f'cap-{s}', s, f'{s} mg capsule', [R(Tm, '3')], per='capsule', form_='capsule') for s in (5, 20, 100, 140, 180, 250)],
     [bsa('gbm-rt', 'malignant-glioma', 'گلیوبلاستوم تازه — همزمان با رادیوتراپی ۷۵ mg/m² روزانه ۴۲ تا ۴۹ روز', 'Newly diagnosed glioblastoma — with radiotherapy 75 mg/m² daily for 42–49 days', A18, 75, [R(Tm, '2.2')], dur={'min': 42, 'max': 49},
          notes=[onc(Tm, '2.2'), note('پیشگیری پنوموسیستیس در فاز همزمان. شروع فقط با ANC ۱۵۰۰ و پلاکت ۱۰۰ هزار به بالا.', 'Pneumocystis prophylaxis during the concomitant phase. Start only with ANC ≥1.5 × 10⁹/L and platelets ≥100 × 10⁹/L.', [R(Tm, '2.2'), R(Tm, '2.1')])]),
      bsa('gbm-maint', 'malignant-glioma', 'گلیوبلاستوم — نگهدارنده ۱۵۰ mg/m² روز ۱ تا ۵ هر ۲۸ روز، ۶ دوره (از دوره ۲ تا ۲۰۰ mg/m²)', 'Glioblastoma — maintenance 150 mg/m² on days 1–5 every 28 days for 6 cycles (from cycle 2 up to 200 mg/m²)', A18, 150, [R(Tm, '2.2')], dur=D(5), notes=[onc(Tm, '2.2')])],
     [CI('hyper', 'سابقه حساسیت جدی به تموزولوماید یا داکاربازین.', 'History of serious hypersensitivity to temozolomide or dacarbazine.', [R(Tm, '4')])],
     warn=[W('سرکوب مغز استخوان؛ سمیت کبدی؛ پنومونی پنوموسیستیس؛ بدخیمی ثانویه؛ سمیت جنینی؛ کپسول باز نشود.', 'Myelosuppression; hepatotoxicity; Pneumocystis pneumonia; secondary malignancies; embryo-fetal toxicity; do not open capsules.', [R(Tm, '5')])],
     exs=[ex('gbm-rt', 'cap-20', {'perDose': 120, 'tabletsPerDoseRounded': 6}, ageYears=55, weightKg=57.6, heightCm=160), ex('gbm-maint', 'cap-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=55, weightKg=80, heightCm=180)])
print('s14c ok')
