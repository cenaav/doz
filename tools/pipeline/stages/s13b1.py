"""Stage 13b (part 1) — cytotoxic chemotherapy: cisplatin, carboplatin, oxaliplatin, paclitaxel, docetaxel, doxorubicin, cyclophosphamide, fluorouracil, gemcitabine, vincristine, etoposide, cytarabine.
mg/m² regimens use type 'bsa' (Mosteller); examples use 180 cm / 80 kg (BSA exactly 2.0 m²) or 144 cm / 25 kg (1.0 m²)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's13_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
bsa = lambda id, dis, fa, en, pop, m2, refs, dur=ONE, notes=None, allowed=None: reg(id, dis, T(fa, en), pop, 'bsa', {'perM2PerDay': m2, 'dividedDoses': 1}, refs, dur=dur, notes=notes, allowed=allowed)
sol = lambda id, mg, label, src, sec='3': form(id, 'injection', 'iv', label, mg, 'mg', [R(src, sec)], vol=1)
pw = lambda id, mg, label, src, sec='3': form(id, 'powder-for-injection', 'iv', label, mg, 'mg', [R(src, sec)], per='vial')
X = lambda r, f, mg, ml=None, **k: ex(r, f, {'perDose': mg, **({'mlPerDose': ml} if ml is not None else {})}, ageYears=k.get('age', 55), weightKg=k.get('w', 80), heightCm=k.get('h', 180))
ONC = note('فقط زیر نظر پزشک متخصص شیمی‌درمانی و در مرکز مجهز. عدد ماشین‌حساب = mg/m² برچسب × سطح بدن (Mosteller)؛ پروتکل، فاصله دوره‌ها، تنظیم بر اساس CBC و عملکرد کلیه/کبد با تیم انکولوژی.',
           'Only under an oncologist in an equipped centre. Calculator = label mg/m² × BSA (Mosteller); protocol, cycle interval and adjustment for CBC and renal/hepatic function rest with the oncology team.', [])
def onc(src, sec): return note(ONC['text']['fa'], ONC['text']['en'], [R(src, sec)])

add_disease('ovarian-cancer', 'سرطان تخمدان', 'Ovarian cancer', ['ovarian cancer', 'سرطان تخمدان', 'کارسینوم تخمدان'], ['C56'], 'oncology')
add_disease('testicular-cancer', 'سرطان بیضه', 'Testicular cancer', ['testicular cancer', 'سرطان بیضه', 'تومور ژرم سل'], ['C62.9'], 'oncology')
add_disease('bladder-cancer', 'سرطان مثانه', 'Bladder cancer', ['bladder cancer', 'سرطان مثانه', 'کارسینوم ترانزیشنال'], ['C67.9'], 'oncology')
add_disease('lung-cancer', 'سرطان ریه (سلول کوچک و غیرسلول کوچک)', 'Lung cancer (small-cell and non-small-cell)', ['NSCLC', 'SCLC', 'سرطان ریه'], ['C34.90'], 'oncology')
add_disease('gastric-cancer', 'سرطان معده', 'Gastric cancer', ['gastric cancer', 'سرطان معده', 'آدنوکارسینوم معده'], ['C16.9'], 'oncology')
add_disease('pancreatic-cancer', 'سرطان پانکراس', 'Pancreatic cancer', ['pancreatic cancer', 'سرطان لوزالمعده', 'سرطان پانکراس'], ['C25.9'], 'oncology')
add_disease('acute-myeloid-leukemia', 'لوسمی میلوئید حاد (AML)', 'Acute myeloid leukaemia (AML)', ['AML', 'ANLL', 'لوسمی میلوئیدی حاد'], ['C92.0'], 'oncology')

Cp = fda('cisplatin', 'FDA Cisplatin', 'Cisplatin for injection 50 mg (WG Critical Care) — Prescribing Information', sid('cisplatin'))
drug('cisplatin', 'antineoplastic-immunomodulating', 'سیس‌پلاتین', 'Cisplatin', T('ترکیب پلاتین', 'Platinum compound'), [{'name': 'Cisplatin', 'market': 'US'}], ['platinol', 'سیسپلاتین', 'cisplatin'],
     [pw('vial-50', 50, '50 mg vial', Cp)],
     [bsa('testis', 'testicular-cancer', 'سرطان پیشرفته بیضه — ۲۰ mg/m² وریدی روزانه ۵ روز در هر دوره', 'Advanced testicular cancer — 20 mg/m² IV daily for 5 days per cycle', A18, 20, [R(Cp, '2.2')], dur={'min': 5, 'max': 5}, notes=[onc(Cp, '2.2')]),
      bsa('ovary', 'ovarian-cancer', 'سرطان پیشرفته تخمدان — ۷۵ تا ۱۰۰ mg/m² روز ۱ هر ۳ تا ۴ هفته', 'Advanced ovarian cancer — 75–100 mg/m² on day 1 every 3–4 weeks', A18, 75, [R(Cp, '2.3')],
          notes=[note('عدد ماشین‌حساب حد پایین (۷۵ mg/m²) است.', 'Calculator gives the lower bound (75 mg/m²).', [R(Cp, '2.3')])]),
      bsa('bladder', 'bladder-cancer', 'سرطان پیشرفته مثانه — ۵۰ تا ۷۰ mg/m² هر ۳ تا ۴ هفته (درمان‌شده قبلی: ۵۰ mg/m² هر ۴ هفته)', 'Advanced bladder cancer — 50–70 mg/m² every 3–4 weeks (heavily pretreated: 50 mg/m² every 4 weeks)', A18, 50, [R(Cp, '2.4')])],
     [CI('hyper', 'حساسیت شدید به سیس‌پلاتین.', 'Severe hypersensitivity to cisplatin.', [R(Cp, '4')])],
     warn=[W('هشدار جعبه‌ای: نفروتوکسیسیتی شدید (هیدراتاسیون کافی و پایش کلیه و الکترولیت)، نوروپاتی محیطی، تهوع و استفراغ شدید (ضدتهوع پیش و پس)، سرکوب مغز استخوان.', 'Boxed warning: severe nephrotoxicity (adequate hydration; monitor renal function and electrolytes), peripheral neuropathy, severe nausea/vomiting (antiemetics before and after), myelosuppression.', [R(Cp, 'Boxed Warning'), R(Cp, '2.1')]),
           W('سمیت شنوایی؛ سمیت چشمی؛ حساسیت؛ بدخیمی ثانویه؛ سمیت جنینی. با وسایل آلومینیومی تماس نیابد.', 'Ototoxicity; ocular toxicity; hypersensitivity; secondary malignancy; embryo-fetal toxicity. Avoid aluminium equipment.', [R(Cp, '5'), R(Cp, '2')])],
     exs=[X('testis', 'vial-50', 40), X('ovary', 'vial-50', 150), X('bladder', 'vial-50', 100)])

Cb = fda('carboplatin', 'FDA Carboplatin', 'Carboplatin injection 10 mg/mL (Natco) — Prescribing Information', sid('carboplatin')); d = R(Cb, 'Dosage and Administration')
drug('carboplatin', 'antineoplastic-immunomodulating', 'کربوپلاتین', 'Carboplatin', T('ترکیب پلاتین', 'Platinum compound'), [{'name': 'Paraplatin', 'market': 'US'}], ['paraplatin', 'کربوپلاتین', 'carboplatin'],
     [sol('vial-10', 10, '10 mg/mL (50/150/450/600 mg)', Cb, 'How Supplied')],
     [bsa('mono', 'ovarian-cancer', 'سرطان عودکننده تخمدان (تک‌دارو) — ۳۶۰ mg/m² روز ۱ هر ۴ هفته', 'Recurrent ovarian cancer (single agent) — 360 mg/m² on day 1 every 4 weeks', A18, 360, [d],
          notes=[note('جایگزین: دوز بر اساس فرمول (Calvert: AUC × [GFR + ۲۵]). تا نوتروفیل ≥۲۰۰۰ و پلاکت ≥۱۰۰ هزار تکرار نشود.', 'Alternative: formula dosing (Calvert: AUC × [GFR + 25]). Do not repeat until neutrophils ≥2,000 and platelets ≥100,000.', [d]), onc(Cb, 'Dosage and Administration')]),
      bsa('combo', 'ovarian-cancer', 'سرطان پیشرفته تخمدان (با سیکلوفسفامید) — ۳۰۰ mg/m² روز ۱ هر ۴ هفته، ۶ دوره', 'Advanced ovarian cancer (with cyclophosphamide) — 300 mg/m² on day 1 every 4 weeks for 6 cycles', A18, 300, [d])],
     [CI('ci', 'سابقه آلرژی شدید به سیس‌پلاتین یا سایر ترکیبات پلاتین؛ سرکوب شدید مغز استخوان یا خونریزی قابل‌توجه.', 'History of severe allergy to cisplatin or other platinum compounds; severe bone-marrow depression or significant bleeding.', [R(Cb, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: سرکوب مغز استخوان (عفونت، خونریزی)، استفراغ، واکنش شبه‌آنافیلاکسی ظرف چند دقیقه.', 'Boxed warning: bone-marrow suppression (infection, bleeding), vomiting, anaphylactic-like reactions within minutes.', [R(Cb, 'Warnings')])],
     exs=[X('mono', 'vial-10', 720, 72), X('combo', 'vial-10', 600, 60)])

Ox = fda('oxaliplatin', 'FDA Oxaliplatin', 'Oxaliplatin injection 5 mg/mL (Gland) — Prescribing Information', sid('oxaliplatin'))
drug('oxaliplatin', 'antineoplastic-immunomodulating', 'اگزالی‌پلاتین', 'Oxaliplatin', T('ترکیب پلاتین', 'Platinum compound'), [{'name': 'Eloxatin', 'market': 'US'}], ['eloxatin', 'الوکساتین', 'اگزالیپلاتین', 'FOLFOX'],
     [sol('vial-5', 5, '5 mg/mL (50/100/200 mg)', Ox)],
     [bsa('crc', 'colorectal-cancer', 'سرطان کولورکتال (FOLFOX: کمکی یا پیشرفته) — ۸۵ mg/m² طی ۱۲۰ دقیقه روز ۱ هر ۲ هفته', 'Colorectal cancer (FOLFOX: adjuvant or advanced) — 85 mg/m² over 120 min on day 1 every 2 weeks', A18, 85, [R(Ox, '2.1')],
          notes=[note('همزمان با لکوورین ۲۰۰ mg/m² (کیسه جدا)، سپس فلوئورویوراسیل. کمکی تا ۱۲ دوره. در واکنش حاد انفوزیون تا ۶ ساعت طولانی شود.', 'Concurrently with leucovorin 200 mg/m² (separate bag), then fluorouracil. Adjuvant up to 12 cycles. Prolong to 6 h for acute infusion reactions.', [R(Ox, '2.1'), R(Ox, '2.2')]), onc(Ox, '2.1')])],
     [CI('hyper', 'سابقه حساسیت به اگزالی‌پلاتین یا سایر داروهای پلاتین.', 'History of hypersensitivity to oxaliplatin or other platinum drugs.', [R(Ox, '4')])],
     warn=[W('هشدار جعبه‌ای: واکنش حساسیتی و آنافیلاکسی کشنده در هر دوره — قطع دائم.', 'Boxed warning: serious and fatal hypersensitivity/anaphylaxis in any cycle — stop permanently.', [R(Ox, 'Boxed Warning')]),
           W('نوروپاتی حسی (تشدید با سرما)؛ سرکوب شدید مغز استخوان؛ PRES؛ سمیت ریوی و کبدی؛ QT؛ رابدومیولیز؛ خونریزی؛ سمیت جنینی.', 'Sensory neuropathy (cold-induced); severe myelosuppression; PRES; pulmonary and hepatic toxicity; QT; rhabdomyolysis; haemorrhage; embryo-fetal toxicity.', [R(Ox, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰: ۶۵ mg/m².', 'CrCl <30: 65 mg/m².'), 'refs': [R(Ox, '2.3')]}],
     exs=[X('crc', 'vial-5', 170, 34)])

Px = fda('paclitaxel', 'FDA Paclitaxel', 'Paclitaxel injection 6 mg/mL (Teva) — Prescribing Information', sid('paclitaxel')); d = R(Px, 'Dosage and Administration')
drug('paclitaxel', 'antineoplastic-immunomodulating', 'پاکلی‌تاکسل', 'Paclitaxel', T('تاکسان', 'Taxane'), [{'name': 'Taxol', 'market': 'US'}], ['taxol', 'تاکسول', 'پاکلیتاکسل'],
     [sol('vial-6', 6, '6 mg/mL (30/100/150/300 mg)', Px, 'How Supplied')],
     [bsa('ovary', 'ovarian-cancer', 'سرطان تخمدان درمان‌نشده — ۱۷۵ mg/m² طی ۳ ساعت (سپس سیس‌پلاتین ۷۵) هر ۳ هفته', 'Untreated ovarian cancer — 175 mg/m² over 3 h (then cisplatin 75) every 3 weeks', A18, 175, [d],
          notes=[note('یا ۱۳۵ mg/m² طی ۲۴ ساعت. پیش‌دارو: دگزامتازون ۲۰ mg خوراکی ۱۲ و ۶ ساعت قبل، دیفن‌هیدرامین ۵۰ mg و سایمتیدین ۳۰۰ mg وریدی ۳۰ تا ۶۰ دقیقه قبل. ست بدون PVC.', 'Or 135 mg/m² over 24 h. Premedicate: dexamethasone 20 mg PO 12 and 6 h before, diphenhydramine 50 mg and cimetidine 300 mg IV 30–60 min before. Non-PVC sets.', [d]), onc(Px, 'Dosage and Administration')]),
      bsa('breast', 'breast-cancer', 'سرطان پستان (کمکی با گره مثبت) — ۱۷۵ mg/m² طی ۳ ساعت هر ۳ هفته، ۴ دوره پس از AC', 'Breast cancer (node-positive adjuvant) — 175 mg/m² over 3 h every 3 weeks for 4 courses after AC', A18, 175, [d])],
     [CI('ci', 'سابقه حساسیت به پاکلی‌تاکسل یا داروهای با روغن کرچک پلی‌اکسیل ۳۵؛ نوتروفیل پایه زیر ۱۵۰۰ (تومور جامد) یا زیر ۱۰۰۰ (کاپوسی).', 'History of hypersensitivity to paclitaxel or polyoxyl 35 castor oil drugs; baseline neutrophils <1,500 (solid tumours) or <1,000 (Kaposi sarcoma).', [R(Px, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: آنافیلاکسی و حساسیت شدید (حتی با پیش‌دارو، گاه کشنده)؛ سرکوب مغز استخوان — با نوتروفیل زیر ۱۵۰۰ نه.', 'Boxed warning: anaphylaxis and severe hypersensitivity (fatal despite premedication); myelosuppression — not with neutrophils <1,500.', [R(Px, 'Warnings')])],
     exs=[X('ovary', 'vial-6', 350, 58.33), X('breast', 'vial-6', 350, 58.33)])

Dc = fda('docetaxel', 'FDA Docetaxel', 'Docetaxel injection 20 mg/mL (Mylan) — Prescribing Information', sid('docetaxel'))
drug('docetaxel', 'antineoplastic-immunomodulating', 'دوستاکسل', 'Docetaxel', T('تاکسان', 'Taxane'), [{'name': 'Taxotere', 'market': 'US'}], ['taxotere', 'تاکسوتر', 'دوستاکسل', 'docetaxel'],
     [sol('vial-20', 20, '20 mg/mL (160 mg/8 mL)', Dc)],
     [bsa('breast', 'breast-cancer', 'سرطان پستان پیشرفته پس از شکست شیمی‌درمانی — ۶۰ تا ۱۰۰ mg/m² طی ۱ ساعت هر ۳ هفته', 'Advanced breast cancer after prior chemotherapy — 60–100 mg/m² over 1 h every 3 weeks', A18, 60, [R(Dc, '2.1')],
          notes=[note('حد پایین در ماشین‌حساب. کمکی (TAC): ۷۵ mg/m² یک ساعت پس از دوکسوروبیسین ۵۰ و سیکلوفسفامید ۵۰۰. پیش‌دارو دگزامتازون ۸ mg دو بار ۳ روز از روز قبل.', 'Calculator gives the lower bound. Adjuvant (TAC): 75 mg/m² 1 h after doxorubicin 50 and cyclophosphamide 500. Premedicate dexamethasone 8 mg twice daily for 3 days starting the day before.', [R(Dc, '2.1'), R(Dc, '2.6')]), onc(Dc, '2')]),
      bsa('nsclc', 'lung-cancer', 'NSCLC پس از شکست پلاتین — ۷۵ mg/m² طی ۱ ساعت هر ۳ هفته', 'NSCLC after platinum failure — 75 mg/m² over 1 h every 3 weeks', A18, 75, [R(Dc, '2.2')]),
      bsa('prostate', 'prostate-cancer', 'سرطان پروستات مقاوم به اخته — ۷۵ mg/m² هر ۳ هفته همراه پردنیزون ۵ mg دو بار', 'Castration-resistant prostate cancer — 75 mg/m² every 3 weeks with prednisone 5 mg twice daily', A18, 75, [R(Dc, '2.3')]),
      bsa('gastric', 'gastric-cancer', 'آدنوکارسینوم معده — ۷۵ mg/m² روز ۱ (با سیس‌پلاتین و فلوئورویوراسیل) هر ۳ هفته', 'Gastric adenocarcinoma — 75 mg/m² on day 1 (with cisplatin and fluorouracil) every 3 weeks', A18, 75, [R(Dc, '2.4')])],
     [CI('ci', 'نوتروفیل زیر ۱۵۰۰؛ سابقه حساسیت شدید به دوستاکسل یا پلی‌سوربات ۸۰.', 'Neutrophils <1,500; history of severe hypersensitivity to docetaxel or polysorbate 80.', [R(Dc, '4')])],
     warn=[W('هشدار جعبه‌ای: مرگ مرتبط با درمان (بیشتر با اختلال کبد، دوز بالا، NSCLC پس از پلاتین با ۱۰۰ mg/m²)؛ بیلی‌روبین بالای حد طبیعی یا AST/ALT >۱٫۵× با ALP >۲٫۵× نه؛ نوتروپنی؛ حساسیت شدید؛ احتباس مایع.', 'Boxed warning: treatment-related deaths (more with hepatic impairment, higher doses, NSCLC after platinum at 100 mg/m²); avoid if bilirubin >ULN or AST/ALT >1.5× ULN with ALP >2.5× ULN; neutropenia; severe hypersensitivity; fluid retention.', [R(Dc, 'Boxed Warning')])],
     exs=[X('breast', 'vial-20', 120, 6), X('nsclc', 'vial-20', 150, 7.5), X('prostate', 'vial-20', 150, 7.5), X('gastric', 'vial-20', 150, 7.5)])

Dx = fda('doxorubicin', 'FDA Doxorubicin', 'Doxorubicin HCl injection 2 mg/mL (Pfizer) — Prescribing Information', sid('doxorubicin'))
drug('doxorubicin', 'antineoplastic-immunomodulating', 'دوکسوروبیسین', 'Doxorubicin', T('آنتراسایکلین', 'Anthracycline'), [{'name': 'Adriamycin', 'market': 'US'}], ['adriamycin', 'آدریامایسین', 'دوکسوروبیسین'],
     [sol('vial-2', 2, '2 mg/mL (10/20/50/150/200 mg)', Dx)],
     [bsa('breast', 'breast-cancer', 'سرطان پستان کمکی (AC) — ۶۰ mg/m² بولوس وریدی روز ۱ هر ۲۱ روز، ۴ دوره', 'Adjuvant breast cancer (AC) — 60 mg/m² IV bolus on day 1 every 21 days for 4 cycles', A18, 60, [R(Dx, '2.1')], notes=[onc(Dx, '2')]),
      bsa('mono', 'breast-cancer', 'سایر سرطان‌ها (تک‌دارو) — ۶۰ تا ۷۵ mg/m² هر ۲۱ روز', 'Other cancers (single agent) — 60–75 mg/m² every 21 days', A18, 60, [R(Dx, '2.2')],
          notes=[note('ترکیبی: ۴۰ تا ۷۵ mg/m² هر ۲۱ تا ۲۸ روز. دوز تجمعی بالای ۵۵۰ mg/m² خطر کاردیومیوپاتی دارد. بیلی‌روبین ۱٫۲ تا ۳: ۵۰٪؛ ۳٫۱ تا ۵: ۲۵٪ دوز.', 'Combination: 40–75 mg/m² every 21–28 days. Cumulative >550 mg/m² carries cardiomyopathy risk. Bilirubin 1.2–3: 50%; 3.1–5: 25% of dose.', [R(Dx, '2.2'), R(Dx, '2.4, Table 1')])])],
     [CI('ci', 'نارسایی شدید میوکارد؛ MI در ۴ تا ۶ هفته اخیر؛ سرکوب شدید و پایدار مغز استخوان؛ نارسایی شدید کبد (Child-Pugh C یا بیلی‌روبین >۵)؛ حساسیت شدید.', 'Severe myocardial insufficiency; MI within 4–6 weeks; severe persistent myelosuppression; severe hepatic impairment (Child-Pugh C or bilirubin >5); severe hypersensitivity.', [R(Dx, '4')])],
     warn=[W('هشدار جعبه‌ای: کاردیومیوپاتی وابسته به دوز تجمعی (LVEF پیش و حین درمان)؛ بدخیمی ثانویه (AML/MDS)؛ نشت و نکروز بافتی؛ سرکوب شدید مغز استخوان.', 'Boxed warning: cumulative-dose cardiomyopathy (LVEF before and during); secondary malignancy (AML/MDS); extravasation and tissue necrosis; severe myelosuppression.', [R(Dx, 'Boxed Warning')])],
     exs=[X('breast', 'vial-2', 120, 60), X('mono', 'vial-2', 120, 60)])

Cy = fda('cyclophosphamide-inj', 'FDA Cyclophosphamide inj', 'Cyclophosphamide injection 200 mg/mL (Nexus) — Prescribing Information', sid('cyclophosphamide'))
drug('cyclophosphamide', 'antineoplastic-immunomodulating', 'سیکلوفسفامید', 'Cyclophosphamide', T('عامل آلکیله‌کننده', 'Alkylating agent'), [{'name': 'Cyclophosphamide', 'market': 'US'}], ['cytoxan', 'endoxan', 'اندوکسان', 'سیکلوفسفامید'],
     [sol('vial-200', 200, '200 mg/mL (500 mg/2.5 mL, 1 g/5 mL)', Cy)],
     [reg('repeat', 'b-cell-lymphoma', T('بدخیمی‌ها (بزرگسال و کودک) — ۱۰ تا ۱۵ mg/kg وریدی هر ۷ تا ۱۰ روز', 'Malignant diseases (adults and children) — 10–15 mg/kg IV every 7–10 days'), {}, 'weightBased', {'perKgPerDose': 10, 'perKgPerDoseMax': 15, 'intervalHours': 24}, [R(Cy, '2')], dur=ONE,
          notes=[note('دوره اول بدون نقص خونی: ۴۰ تا ۵۰ mg/kg تقسیم طی ۲ تا ۵ روز؛ یا ۳ تا ۵ mg/kg دو بار در هفته. مایعات فراوان و صبح تجویز (سمیت مثانه).', 'Initial course without haematological deficit: 40–50 mg/kg divided over 2–5 days; or 3–5 mg/kg twice weekly. Ample fluids and morning dosing (bladder toxicity).', [R(Cy, '2'), R(Cy, '2.1')]),
                 note('فقط زیر نظر متخصص شیمی‌درمانی؛ پروتکل و تنظیم با تیم انکولوژی.', 'Only under an oncologist; protocol and adjustment rest with the oncology team.', [R(Cy, '2')])])],
     [CI('ci', 'حساسیت شدید به سیکلوفسفامید یا متابولیت‌ها؛ انسداد خروجی ادرار.', 'Severe hypersensitivity to cyclophosphamide or its metabolites; urinary outflow obstruction.', [R(Cy, '4')])],
     warn=[W('سرکوب مغز استخوان و ایمنی؛ سمیت ادراری (سیستیت هموراژیک) و کلیه؛ سمیت قلب و ریه؛ بدخیمی ثانویه؛ بیماری انسدادی ورید کبد؛ ناباروری؛ سمیت جنینی؛ هیپوناترمی.', 'Myelosuppression and immunosuppression; urinary (haemorrhagic cystitis) and renal toxicity; cardiac and pulmonary toxicity; secondary malignancy; hepatic veno-occlusive disease; infertility; embryo-fetal toxicity; hyponatraemia.', [R(Cy, '5')])],
     exs=[ex('repeat', 'vial-200', {'perDose': 800, 'mlPerDose': 4, 'upperPerDose': 1200}, ageYears=50, weightKg=80)])

Fu = fda('fluorouracil', 'FDA Fluorouracil', 'Fluorouracil injection 50 mg/mL pharmacy bulk (Alembic) — Prescribing Information', sid('fluorouracil'))
drug('fluorouracil', 'antineoplastic-immunomodulating', 'فلوئورویوراسیل', 'Fluorouracil', T('آنتی‌متابولیت پیریمیدین', 'Pyrimidine antimetabolite'), [{'name': 'Adrucil', 'market': 'US'}], ['5-FU', 'adrucil', 'فلورواوراسیل', 'فلوئورواوراسیل'],
     [sol('vial-50', 50, '50 mg/mL (2.5 g/50 mL pharmacy bulk)', Fu)],
     [bsa('crc', 'colorectal-cancer', 'سرطان کولورکتال (رژیم انفوزیونی با لکوورین) — بولوس ۴۰۰ mg/m² روز ۱، سپس ۲۴۰۰ تا ۳۰۰۰ mg/m² انفوزیون ۴۶ ساعته هر ۲ هفته', 'Colorectal cancer (infusional with leucovorin) — 400 mg/m² bolus day 1, then 2400–3000 mg/m² over 46 h every 2 weeks', A18, 400, [R(Fu, '2.3')],
          notes=[note('عدد ماشین‌حساب بولوس است. رژیم بولوس: ۵۰۰ mg/m² روزهای ۱، ۸، ۱۵، ۲۲، ۲۹، ۳۶ در دوره ۸ هفته‌ای. پیش از شروع ژنوتیپ DPYD.', 'The calculator gives the bolus. Bolus regimen: 500 mg/m² on days 1, 8, 15, 22, 29, 36 of 8-week cycles. Test DPYD before starting.', [R(Fu, '2.3'), R(Fu, '2.1')]), onc(Fu, '2.2')]),
      bsa('breast', 'breast-cancer', 'سرطان پستان (رژیم بر پایه سیکلوفسفامید) — ۵۰۰ یا ۶۰۰ mg/m² روزهای ۱ و ۸ هر ۲۸ روز، ۶ دوره', 'Breast cancer (cyclophosphamide-based) — 500 or 600 mg/m² on days 1 and 8 every 28 days for 6 cycles', A18, 500, [R(Fu, '2.4')]),
      bsa('pancreas', 'pancreatic-cancer', 'سرطان پانکراس — بولوس ۴۰۰ mg/m² روز ۱، سپس ۲۴۰۰ mg/m² طی ۴۶ ساعت هر ۲ هفته', 'Pancreatic cancer — 400 mg/m² bolus day 1, then 2400 mg/m² over 46 h every 2 weeks', A18, 400, [R(Fu, '2.6')])],
     warn=[W('هشدار جعبه‌ای: واکنش جدی یا مرگ در کمبود کامل DPD — پیش از شروع ژنوتیپ DPYD.', 'Boxed warning: serious reactions or death with complete DPD deficiency — test DPYD variants first.', [R(Fu, 'Boxed Warning')]),
           W('سمیت قلبی؛ انسفالوپاتی هیپرآمونمیک؛ سمیت عصبی؛ اسهال؛ سندرم دست-پا؛ سرکوب مغز استخوان؛ موکوزیت؛ افزایش INR با وارفارین.', 'Cardiotoxicity; hyperammonaemic encephalopathy; neurotoxicity; diarrhoea; hand-foot syndrome; myelosuppression; mucositis; raised INR with warfarin.', [R(Fu, '5')])],
     exs=[X('crc', 'vial-50', 800, 16), X('breast', 'vial-50', 1000, 20), X('pancreas', 'vial-50', 800, 16)])

Gm = fda('gemcitabine', 'FDA Gemcitabine', 'Gemcitabine for injection 200 mg/1 g (Sagent) — Prescribing Information', sid('gemcitabine'))
drug('gemcitabine', 'antineoplastic-immunomodulating', 'جمسیتابین', 'Gemcitabine', T('آنتی‌متابولیت نوکلئوزید', 'Nucleoside antimetabolite'), [{'name': 'Gemzar', 'market': 'US'}], ['gemzar', 'جمزار', 'جمسیتابین', 'gemcitabine'],
     [pw('vial-1g', 1000, '1 g vial', Gm), pw('vial-200', 200, '200 mg vial', Gm)],
     [bsa('pancreas', 'pancreatic-cancer', 'سرطان پانکراس — ۱۰۰۰ mg/m² طی ۳۰ دقیقه هفتگی ۷ هفته، یک هفته استراحت، سپس ۳ هفته از هر ۴', 'Pancreatic cancer — 1000 mg/m² over 30 min weekly for 7 weeks, 1 week rest, then 3 of every 4 weeks', A18, 1000, [R(Gm, '2.4')], notes=[onc(Gm, '2')]),
      bsa('nsclc', 'lung-cancer', 'NSCLC — ۱۰۰۰ mg/m² روزهای ۱، ۸ و ۱۵ هر ۲۸ روز (یا ۱۲۵۰ mg/m² روز ۱ و ۸ هر ۲۱ روز)', 'NSCLC — 1000 mg/m² on days 1, 8 and 15 every 28 days (or 1250 mg/m² days 1 and 8 every 21 days)', A18, 1000, [R(Gm, '2.3')]),
      bsa('ovary', 'ovarian-cancer', 'سرطان تخمدان — ۱۰۰۰ mg/m² روز ۱ و ۸ هر ۲۱ روز', 'Ovarian cancer — 1000 mg/m² on days 1 and 8 every 21 days', A18, 1000, [R(Gm, '2.1')]),
      bsa('breast', 'breast-cancer', 'سرطان پستان — ۱۲۵۰ mg/m² روز ۱ و ۸ هر ۲۱ روز', 'Breast cancer — 1250 mg/m² on days 1 and 8 every 21 days', A18, 1250, [R(Gm, '2.2')])],
     [CI('hyper', 'حساسیت به جمسیتابین.', 'Hypersensitivity to gemcitabine.', [R(Gm, '4')])],
     warn=[W('سمیت وابسته به برنامه (انفوزیون طولانی‌تر از ۶۰ دقیقه یا بیش از هفتگی سمیت بیشتر)؛ سرکوب مغز استخوان؛ واکنش پوستی شدید؛ سمیت ریوی؛ HUS؛ سمیت کبد؛ نشت مویرگی؛ PRES.', 'Schedule-dependent toxicity (infusion >60 min or more than weekly is more toxic); myelosuppression; severe skin reactions; pulmonary toxicity; HUS; hepatotoxicity; capillary leak; PRES.', [R(Gm, '5')])],
     exs=[X('pancreas', 'vial-1g', 2000), X('nsclc', 'vial-1g', 2000), X('ovary', 'vial-1g', 2000), X('breast', 'vial-1g', 2500)])

Vc = fda('vincristine', 'FDA Vincristine', 'Vincristine sulfate injection 1 mg/mL (Hospira) — Prescribing Information', sid('vincristine')); d = R(Vc, 'Dosage and Administration')
drug('vincristine', 'antineoplastic-immunomodulating', 'وینکریستین', 'Vincristine', T('آلکالوئید وینکا', 'Vinca alkaloid'), [{'name': 'Oncovin', 'market': 'US'}], ['oncovin', 'انکووین', 'وینکریستین'],
     [sol('vial-1', 1, '1 mg/mL (1 mg, 2 mg vials)', Vc, 'How Supplied')],
     [bsa('adult', 'acute-lymphoblastic-leukemia', 'بزرگسال (لوسمی حاد و سایر بدخیمی‌ها) — ۱٫۴ mg/m² وریدی هفتگی', 'Adults (acute leukaemia and other malignancies) — 1.4 mg/m² IV weekly', A18, 1.4, [d],
          notes=[note('فقط وریدی — تزریق داخل نخاعی کشنده است. بیلی‌روبین مستقیم بالای ۳: ۵۰٪ دوز. محاسبه دوز با دقت زیاد (بیش‌مصرفی کشنده).', 'IV only — intrathecal injection is fatal. Direct bilirubin >3 mg/dL: 50% dose. Calculate with extreme care (overdose can be fatal).', [d, R(Vc, 'Warnings')]), onc(Vc, 'Dosage and Administration')]),
      bsa('child', 'acute-lymphoblastic-leukemia', 'کودک — ۱٫۵ تا ۲ mg/m² وریدی هفتگی (≤۱۰ kg: ۰٫۰۵ mg/kg)', 'Children — 1.5–2 mg/m² IV weekly (≤10 kg: 0.05 mg/kg)', {'maxAge': age(18, 'year'), 'minWeightKg': 10.01}, 1.5, [d]),
      reg('infant', 'acute-lymphoblastic-leukemia', T('کودک ۱۰ kg یا کمتر — شروع ۰٫۰۵ mg/kg هفتگی', 'Children ≤10 kg — start 0.05 mg/kg weekly'), {'maxAge': age(18, 'year'), 'maxWeightKg': 10}, 'weightBased', {'perKgPerDose': 0.05, 'intervalHours': 24}, [d], dur=ONE)],
     [CI('ci', 'فرم دمیلینه‌کننده سندرم شارکو-ماری-توث.', 'Demyelinating form of Charcot–Marie–Tooth syndrome.', [R(Vc, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: فقط وریدی — داخل نخاعی کشنده؛ نشت به بافت تحریک شدید. نوروتوکسیسیتی وابسته به دوز.', 'Boxed warning: IV only — fatal if given intrathecally; extravasation causes severe irritation. Dose-related neurotoxicity.', [R(Vc, 'Warnings')])],
     exs=[X('adult', 'vial-1', 2.8, 2.8), ex('child', 'vial-1', {'perDose': 1.5, 'mlPerDose': 1.5}, ageYears=12, weightKg=25, heightCm=144), ex('infant', 'vial-1', {'perDose': 0.4, 'mlPerDose': 0.4}, ageMonths=10, weightKg=8)])

Ep = fda('etoposide', 'FDA Etoposide', 'Etoposide injection 20 mg/mL (Fresenius) — Prescribing Information', sid('etoposide')); d = R(Ep, 'Dosage and Administration')
drug('etoposide', 'antineoplastic-immunomodulating', 'اتوپوزید', 'Etoposide', T('مهارکننده توپوایزومراز II', 'Topoisomerase II inhibitor'), [{'name': 'Toposar', 'market': 'US'}], ['vepesid', 'toposar', 'وپسید', 'اتوپوزاید', 'اتوپوزید'],
     [sol('vial-20', 20, '20 mg/mL (100 mg/5 mL, 500 mg, 1 g)', Ep, 'How Supplied')],
     [bsa('testis', 'testicular-cancer', 'سرطان بیضه (ترکیبی) — ۵۰ تا ۱۰۰ mg/m²/روز روزهای ۱ تا ۵', 'Testicular cancer (combination) — 50–100 mg/m²/day on days 1–5', A18, 50, [d], dur={'min': 5, 'max': 5},
          notes=[note('یا ۱۰۰ mg/m²/روز روزهای ۱، ۳ و ۵. دوره‌ها هر ۳ تا ۴ هفته پس از بهبود سمیت. نارسایی کلیه طبق احتیاطات.', 'Or 100 mg/m²/day on days 1, 3 and 5. Repeat courses every 3–4 weeks after recovery. Renal impairment per Precautions.', [d]), onc(Ep, 'Dosage and Administration')]),
      bsa('sclc', 'lung-cancer', 'سرطان ریه سلول کوچک (ترکیبی) — ۳۵ mg/m²/روز ۴ روز تا ۵۰ mg/m²/روز ۵ روز', 'Small-cell lung cancer (combination) — 35 mg/m²/day for 4 days to 50 mg/m²/day for 5 days', A18, 35, [d], dur={'min': 4, 'max': 5})],
     [CI('hyper', 'سابقه حساسیت به اتوپوزید یا اجزای فرآورده.', 'Previous hypersensitivity to etoposide or any component.', [R(Ep, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: سرکوب شدید مغز استخوان با عفونت یا خونریزی.', 'Boxed warning: severe myelosuppression with infection or bleeding.', [R(Ep, 'Warnings')])],
     exs=[X('testis', 'vial-20', 100, 5), X('sclc', 'vial-20', 70, 3.5)])

Ca = fda('cytarabine', 'FDA Cytarabine', 'Cytarabine injection 20 mg/mL (Hospira) — Prescribing Information', sid('cytarabine'))
drug('cytarabine', 'antineoplastic-immunomodulating', 'سیتارابین', 'Cytarabine', T('آنتی‌متابولیت پیریمیدین', 'Pyrimidine antimetabolite'), [{'name': 'Cytarabine', 'market': 'US'}], ['ara-c', 'cytosar', 'سیتوزار', 'سیتارابین'],
     [sol('vial-20', 20, '20 mg/mL (500 mg/25 mL)', Ca, 'How Supplied')],
     [NC('aml', 'acute-myeloid-leukemia', 'القای بهبودی لوسمی حاد غیرلنفوسیتی (AML)، ALL و فاز بلاستی CML — طبق پروتکل', 'Remission induction in acute non-lymphocytic leukaemia (AML), ALL and CML blast phase — per protocol', {},
         'برنامه و روش تجویز (انفوزیون مداوم، بولوس یا زیرجلدی) به پروتکل بستگی دارد؛ دوز قطعی از پروتکل درمانی انکولوژی گرفته شود. شمارش روزانه لکوسیت و پلاکت حین القا. فرم بدون نگهدارنده برای تزریق داخل نخاعی.',
         'Schedule and route (continuous infusion, bolus or SC) depend on the protocol; take the exact dose from the oncology protocol. Daily leukocyte and platelet counts during induction. Only preservative-free product intrathecally.', [R(Ca, 'Dosage and Administration'), R(Ca, 'Warnings')])],
     [CI('hyper', 'حساسیت به سیتارابین.', 'Hypersensitivity to cytarabine.', [R(Ca, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: فقط زیر نظر پزشک مجرب؛ سرکوب قوی مغز استخوان — شمارش روزانه در القا.', 'Boxed warning: only by experienced physicians; potent bone-marrow suppression — daily counts during induction.', [R(Ca, 'Boxed Warning'), R(Ca, 'Warnings')])])
print('s13b1 ok')
