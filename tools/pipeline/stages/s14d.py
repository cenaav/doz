"""Stage 14d — oncology part 2: kinase/PARP/CDK inhibitors (dasatinib, nilotinib, ibrutinib, osimertinib, erlotinib, gefitinib, sorafenib, sunitinib, pazopanib,
olaparib, palbociclib), thalidomide, antibodies (atezolizumab, durvalumab, ipilimumab, cetuximab, panitumumab, pertuzumab, daratumumab, blinatumomab),
flutamide, megestrol acetate suspension, pegfilgrastim."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
fx = lambda id, dis, fa, en, pop, mg, n, refs, dur=None, notes=None, allowed=None, mx=None: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': mg, **({'perDoseMax': mx} if mx else {}), 'dosesPerDay': n}, refs, dur=dur, notes=notes, allowed=allowed)
bsa = lambda id, dis, fa, en, pop, m2, refs, dur=ONE, notes=None: reg(id, dis, T(fa, en), pop, 'bsa', {'perM2PerDay': m2, 'dividedDoses': 1}, refs, dur=dur, notes=notes)
kg = lambda id, dis, fa, en, pop, k, refs, notes=None: reg(id, dis, T(fa, en), pop, 'weightBased', {'perKgPerDose': k, 'intervalHours': 24}, refs, dur=ONE, notes=notes)
sol = lambda id, mg, label, src, sec='3': form(id, 'injection', 'iv', label, mg, 'mg', [R(src, sec)], vol=1)
tabs = lambda src, sizes, sec='3', per='tablet', form_='tablet': [tab(f'{form_[:3]}-{str(s).replace(".", "-")}', s, f'{s} mg {form_}', [R(src, sec)], per=per, form_=form_) for s in sizes]
caps = lambda src, sizes, sec='3': tabs(src, sizes, sec, per='capsule', form_='capsule')
X = lambda r, f, mg, ml=None, **k: ex(r, f, {'perDose': mg, **({'mlPerDose': ml} if ml is not None else {})}, ageYears=k.get('age', 55), weightKg=k.get('w', 80), heightCm=k.get('h', 180))
T1 = lambda r, f, mg, n, **k: ex(r, f, {'perDose': mg, 'tabletsPerDoseRounded': n}, ageYears=k.get('age', 55), weightKg=k.get('w', 70))
ONCN = lambda src, sec: note('فقط زیر نظر متخصص انکولوژی؛ ادامه تا پیشرفت بیماری یا سمیت غیرقابل‌قبول. تنظیم دوز برای عوارض و تداخل‌ها طبق برچسب.', 'Only under an oncologist; continue until progression or unacceptable toxicity. Dose adjustments for toxicity and interactions per label.', [R(src, sec)])
ICI_W = lambda src: W('واکنش‌های ایمنی شدید و کشنده (پنومونیت، کولیت، هپاتیت، اندوکرینوپاتی، نفریت، پوستی)؛ واکنش انفوزیون؛ عوارض پیوند آلوژن مغز استخوان؛ سمیت جنینی.', 'Severe and fatal immune-mediated reactions (pneumonitis, colitis, hepatitis, endocrinopathies, nephritis, skin); infusion reactions; complications of allogeneic HSCT; embryo-fetal toxicity.', [R(src, '5')])

add_disease('renal-cell-carcinoma', 'کارسینوم سلول کلیوی', 'Renal cell carcinoma', ['RCC', 'سرطان کلیه', 'کارسینوم کلیه'], ['C64.9'], 'oncology')
add_disease('hepatocellular-carcinoma', 'کارسینوم هپاتوسلولار (سرطان کبد)', 'Hepatocellular carcinoma', ['HCC', 'سرطان کبد', 'هپاتوما'], ['C22.0'], 'oncology')

Sp = fda('sprycel', 'FDA Sprycel', 'Sprycel (dasatinib) tablets — Prescribing Information', sid('dasatinib'))
drug('dasatinib', 'antineoplastic-immunomodulating', 'داساتینیب', 'Dasatinib', T('مهارکننده تیروزین کیناز BCR-ABL', 'BCR-ABL tyrosine kinase inhibitor'), [{'name': 'Sprycel', 'market': 'US'}], ['sprycel', 'اسپرایسل', 'داساتینیب'],
     tabs(Sp, (20, 50, 70, 100, 140)),
     [fx('cp', 'chronic-myeloid-leukemia', 'CML فاز مزمن بزرگسال — ۱۰۰ mg یک بار در روز', 'Chronic-phase CML, adults — 100 mg once daily', A18, 100, 1, [R(Sp, '2.1')], notes=[ONCN(Sp, '2.1')]),
      fx('adv', 'chronic-myeloid-leukemia', 'CML فاز تسریع‌شده یا بلاست، یا ALL فیلادلفیا مثبت بزرگسال — ۱۴۰ mg یک بار در روز', 'Accelerated or blast-phase CML, or Ph+ ALL, adults — 140 mg once daily', A18, 140, 1, [R(Sp, '2.1')], notes=[ONCN(Sp, '2.1')]),
      reg('child', 'chronic-myeloid-leukemia', T('CML فاز مزمن یا ALL Ph+ کودکان — یک بار در روز بر اساس وزن: ۱۰ تا <۲۰ kg: ۴۰ mg؛ ۲۰ تا <۳۰: ۶۰؛ ۳۰ تا <۴۵: ۷۰؛ ۴۵ به بالا: ۱۰۰ mg', 'Chronic-phase CML or Ph+ ALL, children — once daily by weight: 10–<20 kg: 40 mg; 20–<30: 60; 30–<45: 70; ≥45: 100 mg'), {'maxAge': age(18, 'year'), 'minWeightKg': 10}, 'weightBand',
          {'weightBands': [{'minWeightKg': 10, 'maxWeightKg': 19.99, 'perDose': 40, 'dosesPerDay': 1}, {'minWeightKg': 20, 'maxWeightKg': 29.99, 'perDose': 60, 'dosesPerDay': 1}, {'minWeightKg': 30, 'maxWeightKg': 44.99, 'perDose': 70, 'dosesPerDay': 1}, {'minWeightKg': 45, 'maxWeightKg': 150, 'perDose': 100, 'dosesPerDay': 1}]},
          [R(Sp, '2.2, Table 1')], notes=[note('هر ۳ ماه با وزن جدید محاسبه شود. زیر ۱۰ kg قرص توصیه نمی‌شود. قرص خرد یا جویده نشود.', 'Recalculate every 3 months by weight. Tablets not recommended under 10 kg. Do not crush or chew.', [R(Sp, '2.2')])])],
     [],
     warn=[W('سرکوب مغز استخوان؛ خونریزی؛ احتباس مایع (افیوژن پلور)؛ سمیت قلبی؛ فشار خون ریوی؛ طولانی شدن QT؛ واکنش پوستی شدید؛ لیز تومور؛ سمیت جنینی؛ اثر بر رشد کودکان؛ سمیت کبدی.', 'Myelosuppression; bleeding; fluid retention (pleural effusion); cardiac toxicity; pulmonary arterial hypertension; QT prolongation; severe skin reactions; tumour lysis; embryo-fetal toxicity; effects on growth in children; hepatotoxicity.', [R(Sp, '5')])],
     exs=[T1('cp', 'tab-100', 100, 1), T1('adv', 'tab-140', 140, 1), T1('child', 'tab-20', 40, 2, age=6, w=15), T1('child', 'tab-70', 70, 1, age=12, w=35)])

Ts = fda('tasigna', 'FDA Tasigna', 'Tasigna (nilotinib) capsules — Prescribing Information', sid('nilotinib'))
drug('nilotinib', 'antineoplastic-immunomodulating', 'نیلوتینیب', 'Nilotinib', T('مهارکننده تیروزین کیناز BCR-ABL', 'BCR-ABL tyrosine kinase inhibitor'), [{'name': 'Tasigna', 'market': 'US'}], ['tasigna', 'تاسیگنا', 'نیلوتینیب'],
     caps(Ts, (50, 150, 200)),
     [fx('new', 'chronic-myeloid-leukemia', 'CML فاز مزمن Ph+ تازه بزرگسال — ۳۰۰ mg دو بار در روز (ناشتا)', 'Newly diagnosed Ph+ chronic-phase CML, adults — 300 mg twice daily (fasting)', A18, 300, 2, [R(Ts, '2.1')],
         notes=[ONCN(Ts, '2.1'), note('هر ۱۲ ساعت؛ ۲ ساعت قبل و ۱ ساعت بعد چیزی خورده نشود. کودک: ۲۳۰ mg/m² دو بار در روز گرد به نزدیک‌ترین ۵۰ mg (حداکثر ۴۰۰ mg در هر دوز).', 'Every 12 h; no food for 2 h before and 1 h after. Children: 230 mg/m² twice daily rounded to nearest 50 mg (max 400 mg per dose).', [R(Ts, '2.1')])]),
      fx('res', 'chronic-myeloid-leukemia', 'CML فاز مزمن یا تسریع‌شده مقاوم یا عدم تحمل — ۴۰۰ mg دو بار در روز', 'Resistant or intolerant chronic- or accelerated-phase CML — 400 mg twice daily', A18, 400, 2, [R(Ts, '2.1')], notes=[ONCN(Ts, '2.1')])],
     [CI('ci', 'هیپوکالمی، هیپومنیزیمی یا سندرم QT طولانی.', 'Hypokalaemia, hypomagnesaemia or long QT syndrome.', [R(Ts, '4')])],
     warn=[W('هشدار جعبه‌ای: طولانی شدن QT و مرگ ناگهانی — ECG پایه، ۷ روز بعد و دوره‌ای؛ اصلاح پتاسیم و منیزیم؛ پرهیز از غذا و مهارکننده‌های قوی CYP3A4.', 'Boxed warning: QT prolongation and sudden deaths — ECG at baseline, day 7 and periodically; correct potassium and magnesium; avoid food and strong CYP3A4 inhibitors.', [R(Ts, 'Boxed Warning')]),
           W('سرکوب مغز استخوان؛ انسداد عروقی قلبی و شریانی؛ پانکراتیت؛ سمیت کبدی؛ خونریزی؛ احتباس مایع.', 'Myelosuppression; cardiac and arterial vascular occlusive events; pancreatitis; hepatotoxicity; haemorrhage; fluid retention.', [R(Ts, '5')])],
     exs=[T1('new', 'cap-150', 300, 2), T1('res', 'cap-200', 400, 2)])

Ib = fda('imbruvica', 'FDA Imbruvica', 'Imbruvica (ibrutinib) capsules, tablets and oral suspension — Prescribing Information', sid('ibrutinib'))
drug('ibrutinib', 'antineoplastic-immunomodulating', 'ایبروتینیب', 'Ibrutinib', T('مهارکننده BTK', 'BTK inhibitor'), [{'name': 'Imbruvica', 'market': 'US'}], ['imbruvica', 'ایمبرویکا', 'ایبروتینیب'],
     caps(Ib, (70, 140)) + tabs(Ib, (140, 280, 420)),
     [fx('cll', 'chronic-lymphocytic-leukemia', 'CLL/SLL و ماکروگلوبولینمی والدنشتروم — ۴۲۰ mg یک بار در روز', 'CLL/SLL and Waldenström macroglobulinaemia — 420 mg once daily', A18, 420, 1, [R(Ib, '2.1')],
         notes=[ONCN(Ib, '2.1'), note('GVHD مزمن: ۱۲ سال به بالا ۴۲۰ mg؛ ۱ تا <۱۲ سال ۲۴۰ mg/m² (حداکثر ۴۲۰). قرص یا کپسول کامل با آب بلعیده شود.', 'Chronic GVHD: ≥12 years 420 mg; 1–<12 years 240 mg/m² (max 420). Swallow tablets or capsules whole with water.', [R(Ib, '2.1')])])],
     [],
     warn=[W('خونریزی؛ عفونت؛ آریتمی، نارسایی قلب و مرگ ناگهانی؛ فشار خون؛ سیتوپنی؛ بدخیمی دوم؛ سمیت کبدی؛ سمیت جنینی.', 'Haemorrhage; infections; arrhythmias, cardiac failure and sudden death; hypertension; cytopenias; second primary malignancies; hepatotoxicity; embryo-fetal toxicity.', [R(Ib, '5')])],
     exs=[T1('cll', 'cap-140', 420, 3, age=65), T1('cll', 'tab-420', 420, 1, age=65)])

Tg = fda('tagrisso', 'FDA Tagrisso', 'Tagrisso (osimertinib) tablets — Prescribing Information', sid('osimertinib'))
drug('osimertinib', 'antineoplastic-immunomodulating', 'اوسیمرتینیب', 'Osimertinib', T('مهارکننده EGFR نسل سوم', 'Third-generation EGFR inhibitor'), [{'name': 'Tagrisso', 'market': 'US'}], ['tagrisso', 'تاگریسو', 'اوسیمرتینیب'],
     tabs(Tg, (40, 80)),
     [fx('nsclc', 'lung-cancer', 'NSCLC با جهش EGFR (حذف اگزون ۱۹ یا L858R) — ۸۰ mg یک بار در روز', 'EGFR-mutated NSCLC (exon 19 deletion or L858R) — 80 mg once daily', A18, 80, 1, [R(Tg, '2.3')],
         notes=[ONCN(Tg, '2.3'), note('درمان کمکی پس از جراحی: حداکثر ۳ سال. انتخاب بیمار با تست مورد تأیید FDA.', 'Adjuvant after resection: up to 3 years. Select patients with an FDA-approved test.', [R(Tg, '2.3'), R(Tg, '2.2')])])],
     [],
     warn=[W('بیماری بینابینی ریه؛ طولانی شدن QT؛ کاردیومیوپاتی؛ کراتیت؛ SJS؛ واسکولیت پوستی؛ آنمی آپلاستیک؛ میوزیت؛ سمیت جنینی.', 'Interstitial lung disease; QT prolongation; cardiomyopathy; keratitis; SJS; cutaneous vasculitis; aplastic anaemia; myositis; embryo-fetal toxicity.', [R(Tg, '5')])],
     exs=[T1('nsclc', 'tab-80', 80, 1)])

Er = fda('erlotinib', 'FDA Erlotinib', 'Erlotinib tablets (Teva) — Prescribing Information', sid('erlotinib'))
drug('erlotinib', 'antineoplastic-immunomodulating', 'ارلوتینیب', 'Erlotinib', T('مهارکننده EGFR', 'EGFR inhibitor'), [{'name': 'Tarceva', 'market': 'US'}], ['tarceva', 'تارسوا', 'ارلوتینیب'],
     tabs(Er, (25, 100, 150)),
     [fx('nsclc', 'lung-cancer', 'NSCLC متاستاتیک با جهش EGFR — ۱۵۰ mg ناشتا یک بار در روز', 'Metastatic EGFR-mutated NSCLC — 150 mg on an empty stomach once daily', A18, 150, 1, [R(Er, '2.2')], notes=[ONCN(Er, '2.2')]),
      fx('pancreas', 'pancreatic-cancer', 'سرطان پانکراس (با جمسیتابین) — ۱۰۰ mg ناشتا یک بار در روز', 'Pancreatic cancer (with gemcitabine) — 100 mg on an empty stomach once daily', A18, 100, 1, [R(Er, '2.3')], notes=[ONCN(Er, '2.3')])],
     [],
     warn=[W('بیماری بینابینی ریه؛ نارسایی کلیه؛ سمیت کبدی؛ سوراخ شدن گوارش؛ واکنش پوستی تاولی؛ سکته مغزی؛ کم‌خونی همولیتیک میکروآنژیوپاتیک؛ اختلال چشمی؛ خونریزی با وارفارین؛ سمیت جنینی.', 'Interstitial lung disease; renal failure; hepatotoxicity; GI perforation; bullous skin disorders; stroke; microangiopathic haemolytic anaemia; ocular disorders; bleeding with warfarin; embryo-fetal toxicity.', [R(Er, '5')])],
     exs=[T1('nsclc', 'tab-150', 150, 1), T1('pancreas', 'tab-100', 100, 1)])

Ir = fda('iressa', 'FDA Iressa', 'Iressa (gefitinib) tablets 250 mg — Prescribing Information', sid('gefitinib'))
drug('gefitinib', 'antineoplastic-immunomodulating', 'جفیتینیب', 'Gefitinib', T('مهارکننده EGFR', 'EGFR inhibitor'), [{'name': 'Iressa', 'market': 'US'}], ['iressa', 'ایرسا', 'جفیتینیب', 'ژفیتینیب'],
     tabs(Ir, (250,)),
     [fx('nsclc', 'lung-cancer', 'NSCLC متاستاتیک با حذف اگزون ۱۹ یا L858R (خط اول) — ۲۵۰ mg یک بار در روز', 'First-line metastatic NSCLC with exon 19 deletion or L858R — 250 mg once daily', A18, 250, 1, [R(Ir, '2.2')], notes=[ONCN(Ir, '2.2')])],
     [],
     warn=[W('بیماری بینابینی ریه؛ سمیت کبدی؛ سوراخ شدن گوارش؛ اسهال شدید؛ کراتیت؛ واکنش پوستی تاولی؛ سمیت جنینی.', 'Interstitial lung disease; hepatotoxicity; GI perforation; severe diarrhoea; keratitis; bullous skin disorders; embryo-fetal toxicity.', [R(Ir, '5')])],
     exs=[T1('nsclc', 'tab-250', 250, 1)])

Nx = fda('nexavar', 'FDA Nexavar', 'Nexavar (sorafenib) tablets 200 mg — Prescribing Information', sid('sorafenib'))
drug('sorafenib', 'antineoplastic-immunomodulating', 'سورافنیب', 'Sorafenib', T('مهارکننده چندکینازی', 'Multikinase inhibitor'), [{'name': 'Nexavar', 'market': 'US'}], ['nexavar', 'نکساوار', 'سورافنیب'],
     tabs(Nx, (200,)),
     [fx('hcc', 'hepatocellular-carcinoma', 'کارسینوم هپاتوسلولار غیرقابل‌جراحی، RCC پیشرفته و سرطان تمایزیافته تیروئید مقاوم به ید — ۴۰۰ mg دو بار در روز بدون غذا', 'Unresectable HCC, advanced RCC and RAI-refractory differentiated thyroid cancer — 400 mg twice daily without food', A18, 400, 2, [R(Nx, '2.1')], notes=[ONCN(Nx, '2.1')])],
     [CI('ci', 'حساسیت شدید به سورافنیب؛ همراه کربوپلاتین و پاکلی‌تاکسل در سرطان سلول سنگفرشی ریه.', 'Severe hypersensitivity to sorafenib; with carboplatin and paclitaxel in squamous cell lung cancer.', [R(Nx, '4')])],
     warn=[W('ایسکمی قلب؛ خونریزی؛ فشار خون؛ واکنش پوستی (دست و پا)؛ سوراخ شدن گوارش؛ اختلال ترمیم زخم؛ طولانی شدن QT؛ آسیب کبدی؛ سمیت جنینی.', 'Cardiac ischaemia; haemorrhage; hypertension; skin toxicity (hand-foot); GI perforation; impaired wound healing; QT prolongation; liver injury; embryo-fetal toxicity.', [R(Nx, '5')])],
     exs=[T1('hcc', 'tab-200', 400, 2)])

St = fda('sutent', 'FDA Sutent', 'Sutent (sunitinib malate) capsules — Prescribing Information', sid('sunitinib'))
drug('sunitinib', 'antineoplastic-immunomodulating', 'سونیتینیب', 'Sunitinib', T('مهارکننده چندکینازی', 'Multikinase inhibitor'), [{'name': 'Sutent', 'market': 'US'}], ['sutent', 'سوتنت', 'سونیتینیب'],
     caps(St, (12.5, 25, 37.5, 50)),
     [fx('rcc', 'renal-cell-carcinoma', 'RCC پیشرفته و GIST — ۵۰ mg یک بار در روز، ۴ هفته مصرف و ۲ هفته استراحت', 'Advanced RCC and GIST — 50 mg once daily, 4 weeks on and 2 weeks off', A18, 50, 1, [R(St, '2.1')],
         notes=[ONCN(St, '2.1'), note('درمان کمکی RCC: همین برنامه، حداکثر ۹ دوره. pNET: ۳۷٫۵ mg مداوم.', 'Adjuvant RCC: same schedule for up to 9 cycles. pNET: 37.5 mg continuously.', [R(St, '2.2'), R(St, '2')])])],
     [],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی شدید و گاه کشنده.', 'Boxed warning: severe, sometimes fatal hepatotoxicity.', [R(St, 'Boxed Warning')]),
           W('عوارض قلبی‌عروقی؛ QT طولانی؛ فشار خون؛ خونریزی؛ لیز تومور؛ TMA؛ پروتئینوری؛ واکنش پوستی؛ اختلال تیروئید؛ هیپوگلیسمی؛ استئونکروز فک.', 'Cardiovascular events; QT prolongation; hypertension; haemorrhage; tumour lysis; TMA; proteinuria; skin reactions; thyroid dysfunction; hypoglycaemia; osteonecrosis of the jaw.', [R(St, '5')])],
     exs=[T1('rcc', 'cap-50', 50, 1)])

Vt = fda('votrient', 'FDA Votrient', 'Votrient (pazopanib) tablets 200 mg — Prescribing Information', sid('pazopanib'))
drug('pazopanib', 'antineoplastic-immunomodulating', 'پازوپانیب', 'Pazopanib', T('مهارکننده چندکینازی', 'Multikinase inhibitor'), [{'name': 'Votrient', 'market': 'US'}], ['votrient', 'ووترینت', 'پازوپانیب'],
     tabs(Vt, (200,)),
     [fx('rcc', 'renal-cell-carcinoma', 'RCC پیشرفته و سارکوم بافت نرم پیشرفته — ۸۰۰ mg یک بار در روز بدون غذا', 'Advanced RCC and advanced soft-tissue sarcoma — 800 mg once daily without food', A18, 800, 1, [R(Vt, '2.1')],
         notes=[ONCN(Vt, '2.1'), note('نارسایی متوسط کبد: ۲۰۰ mg یک بار در روز.', 'Moderate hepatic impairment: 200 mg once daily.', [R(Vt, '2.2')])])],
     [],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی شدید و کشنده — پایش عملکرد کبد.', 'Boxed warning: severe and fatal hepatotoxicity — monitor liver function.', [R(Vt, 'Boxed Warning')]),
           W('QT طولانی؛ اختلال عملکرد قلب؛ خونریزی؛ ترومبوز شریانی و وریدی؛ TMA؛ سوراخ شدن گوارش؛ پنومونیت؛ PRES؛ فشار خون.', 'QT prolongation; cardiac dysfunction; haemorrhage; arterial and venous thrombosis; TMA; GI perforation; pneumonitis; PRES; hypertension.', [R(Vt, '5')])],
     exs=[T1('rcc', 'tab-200', 800, 4)])

Ly = fda('lynparza', 'FDA Lynparza', 'Lynparza (olaparib) tablets — Prescribing Information', sid('olaparib'))
drug('olaparib', 'antineoplastic-immunomodulating', 'اولاپاریب', 'Olaparib', T('مهارکننده PARP', 'PARP inhibitor'), [{'name': 'Lynparza', 'market': 'US'}], ['lynparza', 'لینپارزا', 'اولاپاریب'],
     tabs(Ly, (100, 150)),
     [fx('ovary', 'ovarian-cancer', 'سرطان تخمدان، پستان، پانکراس و پروستات با جهش BRCA/HRR — ۳۰۰ mg دو بار در روز', 'BRCA/HRR-mutated ovarian, breast, pancreatic and prostate cancer — 300 mg twice daily', A18, 300, 2, [R(Ly, '2.2')],
         notes=[ONCN(Ly, '2.2'), note('قرص کامل بلعیده شود. پروستات: همراه آنالوگ GnRH یا پس از اورکیدکتومی. نارسایی متوسط کلیه: کاهش دوز.', 'Swallow whole. Prostate: with a GnRH analogue or after orchiectomy. Moderate renal impairment: reduce dose.', [R(Ly, '2.2'), R(Ly, '2')])])],
     [],
     warn=[W('MDS/AML؛ پنومونیت؛ ترومبوآمبولی وریدی؛ سمیت کبدی؛ سمیت جنینی.', 'MDS/AML; pneumonitis; venous thromboembolism; hepatotoxicity; embryo-fetal toxicity.', [R(Ly, '5')])],
     exs=[T1('ovary', 'tab-150', 300, 2, age=60, w=60)])

Ib2 = fda('ibrance', 'FDA Ibrance', 'Ibrance (palbociclib) tablets — Prescribing Information', sid('palbociclib'))
drug('palbociclib', 'antineoplastic-immunomodulating', 'پالبوسیکلیب', 'Palbociclib', T('مهارکننده CDK4/6', 'CDK4/6 inhibitor'), [{'name': 'Ibrance', 'market': 'US'}], ['ibrance', 'ایبرنس', 'پالبوسیکلیب'],
     tabs(Ib2, (75, 100, 125)),
     [fx('breast', 'breast-cancer', 'سرطان پستان پیشرفته HR+/HER2- (با مهارکننده آروماتاز یا فولوسترانت) — ۱۲۵ mg روزانه ۲۱ روز، سپس ۷ روز استراحت', 'HR+/HER2- advanced breast cancer (with an aromatase inhibitor or fulvestrant) — 125 mg daily for 21 days, then 7 days off', A18, 125, 1, [R(Ib2, '2.1')], notes=[ONCN(Ib2, '2.1')])],
     [],
     warn=[W('نوتروپنی؛ بیماری بینابینی ریه یا پنومونیت؛ سمیت جنینی.', 'Neutropenia; interstitial lung disease or pneumonitis; embryo-fetal toxicity.', [R(Ib2, '5')])],
     exs=[T1('breast', 'tab-125', 125, 1, w=60)])

Th = fda('thalomid', 'FDA Thalomid', 'Thalomid (thalidomide) capsules — Prescribing Information', sid('thalidomide'))
drug('thalidomide', 'antineoplastic-immunomodulating', 'تالیدومید', 'Thalidomide', T('تعدیل‌کننده ایمنی', 'Immunomodulatory agent'), [{'name': 'Thalomid', 'market': 'US'}], ['thalomid', 'تالومید', 'تالیدومید'],
     caps(Th, (50, 100, 150, 200)),
     [fx('mm', 'multiple-myeloma', 'مولتیپل میلوما تازه (با دگزامتازون) — ۲۰۰ mg یک بار در روز (شب)', 'Newly diagnosed multiple myeloma (with dexamethasone) — 200 mg once daily (bedtime)', A18, 200, 1, [R(Th, '2.2')],
         notes=[ONCN(Th, '2.2'), note('اریتم ندوزوم لپروزوم پوستی: ۱۰۰ تا ۳۰۰ mg/روز (شدید تا ۴۰۰). فقط از طریق برنامه REMS؛ تست بارداری پیش و حین درمان.', 'Cutaneous erythema nodosum leprosum: 100–300 mg/day (severe up to 400). Only through REMS; pregnancy testing before and during treatment.', [R(Th, '2.3'), R(Th, '2.1')])])],
     [CI('preg', 'بارداری.', 'Pregnancy.', [R(Th, '4.1')]), CI('hyper', 'حساسیت به تالیدومید یا اجزا.', 'Hypersensitivity to thalidomide or its components.', [R(Th, '4.2')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی شدید (نقص مادرزادی، مرگ جنین) — حتی یک دوز؛ ترومبوآمبولی وریدی و شریانی (پروفیلاکسی در میلوما).', 'Boxed warning: severe embryo-fetal toxicity (birth defects, fetal death) — even a single dose; venous and arterial thromboembolism (prophylaxis in myeloma).', [R(Th, 'Boxed Warning')]),
           W('خواب‌آلودگی؛ نوروپاتی محیطی؛ سرگیجه و افت فشار وضعیتی؛ نوتروپنی؛ برادیکاردی؛ واکنش پوستی شدید؛ تشنج.', 'Somnolence; peripheral neuropathy; dizziness and orthostatic hypotension; neutropenia; bradycardia; severe skin reactions; seizures.', [R(Th, '5')])],
     exs=[T1('mm', 'cap-200', 200, 1, age=65)])

Tc = fda('tecentriq', 'FDA Tecentriq', 'Tecentriq (atezolizumab) injection — Prescribing Information', sid('atezolizumab'))
drug('atezolizumab', 'antineoplastic-immunomodulating', 'آتزولیزوماب', 'Atezolizumab', T('مهارکننده PD-L1', 'PD-L1 blocking antibody'), [{'name': 'Tecentriq', 'market': 'US'}], ['tecentriq', 'تسنتریک', 'آتزولیزوماب'],
     [sol('inj-60', 60, '60 mg/mL (840 mg/14 mL, 1200 mg/20 mL)', Tc)],
     [fx('q3w', 'lung-cancer', 'NSCLC، SCLC و سایر اندیکاسیون‌ها — ۱۲۰۰ mg وریدی هر ۳ هفته (یا ۸۴۰ mg هر ۲ هفته یا ۱۶۸۰ mg هر ۴ هفته)', 'NSCLC, SCLC and other indications — 1200 mg IV every 3 weeks (or 840 mg every 2 weeks or 1680 mg every 4 weeks)', A18, 1200, 1, [R(Tc, '2.2, Table 1')], dur=ONE,
         notes=[ONCN(Tc, '2.2'), note('انفوزیون اول ۶۰ دقیقه، بعدی‌ها ۳۰ دقیقه اگر تحمل شد. کمکی NSCLC: حداکثر ۱ سال.', 'First infusion over 60 min, then 30 min if tolerated. Adjuvant NSCLC: up to 1 year.', [R(Tc, '2.2')])])],
     [],
     warn=[ICI_W(Tc)],
     exs=[ex('q3w', 'inj-60', {'perDose': 1200, 'mlPerDose': 20}, ageYears=60, weightKg=70)])

Im = fda('imfinzi', 'FDA Imfinzi', 'Imfinzi (durvalumab) injection — Prescribing Information', sid('durvalumab'))
drug('durvalumab', 'antineoplastic-immunomodulating', 'دوروالوماب', 'Durvalumab', T('مهارکننده PD-L1', 'PD-L1 blocking antibody'), [{'name': 'Imfinzi', 'market': 'US'}], ['imfinzi', 'ایمفینزی', 'دوروالوماب'],
     [sol('inj-50', 50, '50 mg/mL (120 mg/2.4 mL, 500 mg/10 mL)', Im)],
     [fx('fixed', 'lung-cancer', 'NSCLC، SCLC، سرطان مجاری صفراوی، کبد و سایر — وزن ۳۰ kg به بالا: ۱۵۰۰ mg وریدی هر ۳ یا ۴ هفته طبق رژیم', 'NSCLC, SCLC, biliary tract, liver and other cancers — weight ≥30 kg: 1500 mg IV every 3 or 4 weeks by regimen', {'minAge': age(18, 'year'), 'minWeightKg': 30}, 1500, 1, [R(Im, '2.2, Table 1')], dur=ONE, notes=[ONCN(Im, '2.2')]),
      kg('light', 'lung-cancer', 'وزن زیر ۳۰ kg — ۲۰ mg/kg وریدی هر ۳ یا ۴ هفته', 'Weight under 30 kg — 20 mg/kg IV every 3 or 4 weeks', {'minAge': age(18, 'year'), 'maxWeightKg': 29.99}, 20, [R(Im, '2.2, Table 1')], notes=[ONCN(Im, '2.2')])],
     [],
     warn=[ICI_W(Im)],
     exs=[ex('fixed', 'inj-50', {'perDose': 1500, 'mlPerDose': 30}, ageYears=60, weightKg=70), ex('light', 'inj-50', {'perDose': 560, 'mlPerDose': 11.2}, ageYears=70, weightKg=28)])

Yv = fda('yervoy', 'FDA Yervoy', 'Yervoy (ipilimumab) injection 5 mg/mL — Prescribing Information', sid('ipilimumab'))
drug('ipilimumab', 'antineoplastic-immunomodulating', 'ایپیلیموماب', 'Ipilimumab', T('مهارکننده CTLA-4', 'CTLA-4 blocking antibody'), [{'name': 'Yervoy', 'market': 'US'}], ['yervoy', 'یروی', 'ایپیلیموماب'],
     [sol('inj-5', 5, '5 mg/mL (50 mg/10 mL, 200 mg/40 mL)', Yv)],
     [kg('mel', 'melanoma', 'ملانوم غیرقابل‌جراحی یا متاستاتیک (۱۲ سال به بالا) — ۳ mg/kg وریدی هر ۳ هفته، حداکثر ۴ دوز', 'Unresectable or metastatic melanoma (≥12 years) — 3 mg/kg IV every 3 weeks, max 4 doses', {'minAge': age(12, 'year')}, 3, [R(Yv, '2.2')],
         notes=[ONCN(Yv, '2.2'), note('ترکیب با نیوولوماب و سایر اندیکاسیون‌ها (کلیه، کولورکتال، کبد، ریه، مزوتلیوما): دوز و فاصله متفاوت طبق بخش ۲.', 'Combinations with nivolumab and other indications (renal, colorectal, liver, lung, mesothelioma): different dose and interval per section 2.', [R(Yv, '2')])])],
     [],
     warn=[ICI_W(Yv)],
     exs=[ex('mel', 'inj-5', {'perDose': 210, 'mlPerDose': 42}, ageYears=50, weightKg=70)])

Eb = fda('erbitux', 'FDA Erbitux', 'Erbitux (cetuximab) injection 2 mg/mL — Prescribing Information', sid('cetuximab'))
drug('cetuximab', 'antineoplastic-immunomodulating', 'ستوکسیماب', 'Cetuximab', T('آنتی‌بادی ضد EGFR', 'EGFR antagonist antibody'), [{'name': 'Erbitux', 'market': 'US'}], ['erbitux', 'اربیتوکس', 'ستوکسیماب'],
     [sol('inj-2', 2, '2 mg/mL (100 mg/50 mL, 200 mg/100 mL)', Eb)],
     [bsa('load', 'colorectal-cancer', 'سرطان کولورکتال RAS وحشی و سر و گردن — دوز اول ۴۰۰ mg/m² وریدی ۱۲۰ دقیقه', 'RAS wild-type colorectal and head-and-neck cancer — initial dose 400 mg/m² IV over 120 min', A18, 400, [R(Eb, '2.2'), R(Eb, '2.3')], notes=[ONCN(Eb, '2.3')]),
      bsa('weekly', 'colorectal-cancer', 'ادامه هفتگی — ۲۵۰ mg/m² وریدی ۶۰ دقیقه هر هفته (یا ۵۰۰ mg/m² هر ۲ هفته)', 'Weekly continuation — 250 mg/m² IV over 60 min every week (or 500 mg/m² every 2 weeks)', A18, 250, [R(Eb, '2.2'), R(Eb, '2.3')], notes=[ONCN(Eb, '2.3')])],
     [],
     warn=[W('هشدار جعبه‌ای: واکنش انفوزیون جدی و کشنده؛ ایست قلبی‌ریوی یا مرگ ناگهانی (پایش الکترولیت‌ها).', 'Boxed warning: serious and fatal infusion reactions; cardiopulmonary arrest or sudden death (monitor electrolytes).', [R(Eb, 'Boxed Warning')]),
           W('سمیت ریوی؛ سمیت پوستی؛ هیپومنیزیمی؛ پیشرفت تومور و مرگ بیشتر در RAS جهش‌یافته؛ سمیت جنینی.', 'Pulmonary toxicity; dermatologic toxicity; hypomagnesaemia; increased progression and mortality in RAS-mutant disease; embryo-fetal toxicity.', [R(Eb, '5')])],
     exs=[X('load', 'inj-2', 800, 400), X('weekly', 'inj-2', 500, 250)])

Vx = fda('vectibix', 'FDA Vectibix', 'Vectibix (panitumumab) injection 20 mg/mL — Prescribing Information', sid('panitumumab'))
drug('panitumumab', 'antineoplastic-immunomodulating', 'پانیتوموماب', 'Panitumumab', T('آنتی‌بادی ضد EGFR', 'EGFR antagonist antibody'), [{'name': 'Vectibix', 'market': 'US'}], ['vectibix', 'وکتیبیکس', 'پانیتوموماب'],
     [sol('inj-20', 20, '20 mg/mL (100 mg/5 mL, 400 mg/20 mL)', Vx)],
     [kg('crc', 'colorectal-cancer', 'سرطان کولورکتال متاستاتیک RAS وحشی — ۶ mg/kg وریدی هر ۱۴ روز', 'RAS wild-type metastatic colorectal cancer — 6 mg/kg IV every 14 days', A18, 6, [R(Vx, '2')],
         notes=[ONCN(Vx, '2'), note('انفوزیون ۶۰ دقیقه (تا ۱۰۰۰ mg) یا ۹۰ دقیقه (بیشتر). جهش KRAS G12C: همراه سوتوراسیب.', 'Infuse over 60 min (≤1000 mg) or 90 min (>1000 mg). KRAS G12C: with sotorasib.', [R(Vx, '2')])])],
     [],
     warn=[W('هشدار جعبه‌ای: سمیت پوستی (۹۰٪، شدید ۱۵٪).', 'Boxed warning: dermatologic toxicity (90%, severe in 15%).', [R(Vx, 'Boxed Warning')]),
           W('کاهش الکترولیت؛ واکنش انفوزیون؛ نارسایی حاد کلیه؛ بیماری بینابینی ریه؛ حساسیت به نور؛ سمیت چشمی؛ سمیت جنینی.', 'Electrolyte depletion; infusion reactions; acute renal failure; interstitial lung disease; photosensitivity; ocular toxicity; embryo-fetal toxicity.', [R(Vx, '5')])],
     exs=[ex('crc', 'inj-20', {'perDose': 420, 'mlPerDose': 21}, ageYears=60, weightKg=70)])

Pj = fda('perjeta', 'FDA Perjeta', 'Perjeta (pertuzumab) injection 420 mg/14 mL — Prescribing Information', sid('pertuzumab'))
drug('pertuzumab', 'antineoplastic-immunomodulating', 'پرتوزوماب', 'Pertuzumab', T('آنتی‌بادی ضد HER2', 'HER2-directed antibody'), [{'name': 'Perjeta', 'market': 'US'}], ['perjeta', 'پرجتا', 'پرتوزوماب'],
     [sol('inj-30', 30, '30 mg/mL, 420 mg/14 mL vial', Pj)],
     [fx('load', 'breast-cancer', 'سرطان پستان HER2 مثبت (با تراستوزوماب) — دوز اول ۸۴۰ mg وریدی ۶۰ دقیقه', 'HER2-positive breast cancer (with trastuzumab) — initial dose 840 mg IV over 60 min', A18, 840, 1, [R(Pj, '2.3')], dur=ONE, notes=[ONCN(Pj, '2.3')]),
      fx('maint', 'breast-cancer', 'ادامه — ۴۲۰ mg وریدی هر ۳ هفته', 'Continuation — 420 mg IV every 3 weeks', A18, 420, 1, [R(Pj, '2.3')], dur=ONE,
         notes=[note('تراستوزوماب همراه: ۸ mg/kg سپس ۶ mg/kg هر ۳ هفته. فقط انفوزیون وریدی، نه پوش یا بولوس. LVEF پیش و حین درمان.', 'Trastuzumab with it: 8 mg/kg then 6 mg/kg every 3 weeks. IV infusion only, not push or bolus. LVEF before and during.', [R(Pj, '2.3'), R(Pj, '2.1')])])],
     [CI('hyper', 'حساسیت به پرتوزوماب یا اجزا.', 'Hypersensitivity to pertuzumab or excipients.', [R(Pj, '4')])],
     warn=[W('هشدار جعبه‌ای: اختلال عملکرد بطن چپ و نارسایی قلب؛ سمیت جنینی (مرگ جنین و نقص مادرزادی).', 'Boxed warning: left ventricular dysfunction and heart failure; embryo-fetal toxicity (fetal death and birth defects).', [R(Pj, 'Boxed Warning')])],
     exs=[ex('load', 'inj-30', {'perDose': 840, 'mlPerDose': 28}, ageYears=50, weightKg=65), ex('maint', 'inj-30', {'perDose': 420, 'mlPerDose': 14}, ageYears=50, weightKg=65)])

Dz = fda('darzalex', 'FDA Darzalex', 'Darzalex (daratumumab) injection for IV use — Prescribing Information', sid('daratumumab'))
drug('daratumumab', 'antineoplastic-immunomodulating', 'داراتوموماب', 'Daratumumab', T('آنتی‌بادی ضد CD38', 'CD38-directed antibody'), [{'name': 'Darzalex', 'market': 'US'}], ['darzalex', 'دارزالکس', 'داراتوموماب'],
     [sol('inj-20', 20, '20 mg/mL (100 mg/5 mL, 400 mg/20 mL) — IV', Dz)],
     [kg('mm', 'multiple-myeloma', 'مولتیپل میلوما — ۱۶ mg/kg وزن واقعی، انفوزیون وریدی؛ برنامه طبق رژیم ترکیبی', 'Multiple myeloma — 16 mg/kg actual body weight IV infusion; schedule by combination regimen', A18, 16, [R(Dz, '2.2')],
         notes=[ONCN(Dz, '2.2'), note('پیش‌دارو: کورتیکواستروئید، ضدتب و آنتی‌هیستامین؛ داروهای پس از انفوزیون. پیش از شروع گروه خون و غربالگری آنتی‌بادی (تداخل با کراس‌مچ).', 'Premedicate with corticosteroid, antipyretic and antihistamine; post-infusion medicines. Type and screen before starting (cross-match interference).', [R(Dz, '2.3'), R(Dz, '5.2')])])],
     [CI('hyper', 'سابقه حساسیت شدید (آنافیلاکسی) به داراتوموماب یا اجزا.', 'History of severe hypersensitivity (anaphylaxis) to daratumumab or components.', [R(Dz, '4')])],
     warn=[W('واکنش انفوزیون؛ تداخل با آزمایش سرولوژی و تعیین پاسخ؛ عفونت؛ نوتروپنی؛ ترومبوسیتوپنی؛ سمیت جنینی.', 'Infusion reactions; interference with serological testing and response assessment; infections; neutropenia; thrombocytopenia; embryo-fetal toxicity.', [R(Dz, '5')])],
     exs=[ex('mm', 'inj-20', {'perDose': 1120, 'mlPerDose': 56}, ageYears=65, weightKg=70)])

Bc = fda('blincyto', 'FDA Blincyto', 'Blincyto (blinatumomab) for injection 35 mcg — Prescribing Information', sid('blinatumomab'))
drug('blinatumomab', 'antineoplastic-immunomodulating', 'بلیناتوموماب', 'Blinatumomab', T('درگیرکننده دوگانه سلول T (CD19/CD3)', 'Bispecific CD19/CD3 T-cell engager'), [{'name': 'Blincyto', 'market': 'US'}], ['blincyto', 'بلینسایتو', 'بلیناتوموماب'],
     [form('vial-35', 'powder-for-injection', 'iv', '35 mcg vial', 35, 'mcg', [R(Bc, '3')], per='vial')],
     [NC('all', 'acute-lymphoblastic-leukemia', 'ALL پیش‌ساز B (MRD مثبت، عودکننده یا تثبیت) — انفوزیون وریدی مداوم ۲۸ روزه، سپس ۱۴ روز استراحت', 'B-cell precursor ALL (MRD-positive, relapsed/refractory or consolidation) — continuous IV infusion for 28 days, then 14 days off', {},
         'دوز روزانه (mcg/روز) ثابت برای ۴۵ kg و بالاتر و بر حسب mcg/m²/روز برای زیر ۴۵ kg، و بسته به نوع درمان و دوره متفاوت است (جداول ۱ تا ۳). فقط در مرکز مجهز؛ بستری در روزهای اول دوره اول.',
         'Daily dose (mcg/day) is fixed for ≥45 kg and mcg/m²/day for <45 kg, and varies by setting and cycle (Tables 1–3). Only in an equipped centre; hospitalise for the first days of the first cycle.', [R(Bc, '2.1'), R(Bc, '2.2'), R(Bc, '2.3')])],
     [CI('hyper', 'حساسیت به بلیناتوموماب یا اجزا.', 'Hypersensitivity to blinatumomab or components.', [R(Bc, '4')])],
     warn=[W('هشدار جعبه‌ای: سندرم آزادسازی سیتوکین تهدیدکننده حیات؛ سمیت عصبی شامل ICANS.', 'Boxed warning: life-threatening cytokine release syndrome; neurological toxicities including ICANS.', [R(Bc, 'Boxed Warning')]),
           W('عفونت؛ لیز تومور؛ نوتروپنی؛ افزایش آنزیم کبد؛ پانکراتیت؛ لکوانسفالوپاتی؛ خطای آماده‌سازی؛ بنزیل الکل در نوزاد.', 'Infections; tumour lysis; neutropenia; elevated liver enzymes; pancreatitis; leukoencephalopathy; preparation errors; benzyl alcohol toxicity in neonates.', [R(Bc, '5')])])

Eu = fda('eulexin', 'FDA Eulexin', 'Eulexin (flutamide) capsules 125 mg — Prescribing Information', sid('flutamide'))
drug('flutamide', 'antineoplastic-immunomodulating', 'فلوتامید', 'Flutamide', T('ضدآندروژن غیراستروئیدی', 'Non-steroidal antiandrogen'), [{'name': 'Eulexin', 'market': 'US'}], ['eulexin', 'اولکسین', 'فلوتامید'],
     [tab('cap-125', 125, '125 mg capsule', [R(Eu, 'Description')], per='capsule', form_='capsule')],
     [fx('prostate', 'prostate-cancer', 'سرطان پروستات مرحله B2-C و D2 (با آگونیست LHRH) — ۲۵۰ mg (۲ کپسول) سه بار در روز هر ۸ ساعت', 'Stage B2-C and D2 prostate cancer (with LHRH agonist) — 250 mg (2 capsules) three times daily every 8 h', A18, 250, 3, [R(Eu, 'Dosage and Administration')])],
     [CI('ci', 'حساسیت به فلوتامید؛ نارسایی شدید کبد (آنزیم‌های کبد پیش از شروع).', 'Hypersensitivity to flutamide; severe hepatic impairment (check liver enzymes before starting).', [R(Eu, 'Contraindications')])],
     warn=[W('آسیب کبدی — بستری و به‌ندرت مرگ از نارسایی کبد؛ آنزیم کبد پایه، ماهانه ۴ ماه و سپس دوره‌ای.', 'Hepatic injury — hospitalisation and rarely death from liver failure; baseline liver enzymes, monthly for 4 months, then periodically.', [R(Eu, 'Warnings')])],
     exs=[T1('prostate', 'cap-125', 250, 2, age=70)])

Mg = fda('megestrol-susp', 'FDA Megestrol susp', 'Megestrol acetate oral suspension 40 mg/mL — Prescribing Information', sid('megestrol'))
drug('megestrol', 'antineoplastic-immunomodulating', 'مژسترول استات', 'Megestrol acetate', T('پروژستین', 'Progestin'), [{'name': 'Megace', 'market': 'US'}], ['megace', 'مگیس', 'مژسترول', 'megestrol acetate'],
     [liquid('susp-40', 40, 1, '40 mg/mL oral suspension', [R(Mg, 'How Supplied')])],
     [fx('aids', 'aids-anorexia', 'بی‌اشتهایی، کاشکسی یا کاهش وزن قابل‌توجه در ایدز — ۸۰۰ mg (۲۰ mL) یک بار در روز', 'Anorexia, cachexia or significant weight loss in AIDS — 800 mg (20 mL) once daily', A18, 800, 1, [R(Mg, 'Dosage and Administration')],
         notes=[note('دوزهای ۴۰۰ و ۸۰۰ mg/روز در کارآزمایی‌ها مؤثر بودند. پیش از مصرف خوب تکان داده شود.', 'Daily doses of 400 and 800 mg were effective in trials. Shake well before use.', [R(Mg, 'Dosage and Administration')])])],
     [CI('ci', 'حساسیت به مژسترول؛ بارداری قطعی یا مشکوک.', 'Hypersensitivity to megestrol acetate; known or suspected pregnancy.', [R(Mg, 'Contraindications')])],
     warn=[W('آسیب جنینی؛ سرکوب آدرنال و کوشینگ با مصرف طولانی یا قطع؛ ترومبوآمبولی.', 'Fetal harm; adrenal suppression and Cushingoid effects with chronic use or withdrawal; thromboembolism.', [R(Mg, 'Warnings')])],
     exs=[ex('aids', 'susp-40', {'perDose': 800, 'mlPerDose': 20}, ageYears=40, weightKg=55)])

Nl = fda('neulasta', 'FDA Neulasta', 'Neulasta (pegfilgrastim) injection — Prescribing Information', sid('pegfilgrastim'))
PEGN = note('یک بار در هر دوره شیمی‌درمانی؛ نه در فاصله ۱۴ روز قبل تا ۲۴ ساعت بعد از شیمی‌درمانی.', 'Once per chemotherapy cycle; not between 14 days before and 24 hours after chemotherapy.', [R(Nl, '2.1')])
drug('pegfilgrastim', 'antineoplastic-immunomodulating', 'پگ‌فیلگراستیم', 'Pegfilgrastim', T('فاکتور محرک کلونی گرانولوسیت طولانی‌اثر', 'Long-acting granulocyte colony-stimulating factor'), [{'name': 'Neulasta', 'market': 'US'}], ['neulasta', 'pegagen', 'پگاژن', 'نولاستا', 'پگ فیلگراستیم'],
     [form('pfs-6', 'injection', 'sc', '6 mg/0.6 mL prefilled syringe (10 mg/mL)', 10, 'mg', [R(Nl, '3')], vol=1)],
     [fx('adult', 'febrile-neutropenia', 'کاهش نوتروپنی تب‌دار در شیمی‌درمانی سرکوب‌کننده مغز استخوان — بزرگسال و کودک ۴۵ kg به بالا: ۶ mg زیرجلدی', 'Reduce febrile neutropenia with myelosuppressive chemotherapy — adults and children ≥45 kg: 6 mg SC', {'minWeightKg': 45}, 6, 1, [R(Nl, '2.1')], dur=ONE,
         notes=[PEGN, note('سندرم حاد پرتوی (زیرگروه خونی): دو دوز ۶ mg به فاصله یک هفته.', 'Haematopoietic acute radiation syndrome: two 6 mg doses one week apart.', [R(Nl, '2.2')])]),
      reg('child', 'febrile-neutropenia', T('کودک ۱۰ تا <۴۵ kg — ۱۰ تا ۲۰ kg: ۱٫۵ mg؛ ۲۱ تا ۳۰: ۲٫۵ mg؛ ۳۱ تا ۴۴: ۴ mg زیرجلدی', 'Children 10 to <45 kg — 10–20 kg: 1.5 mg; 21–30: 2.5 mg; 31–44: 4 mg SC'), {'maxAge': age(18, 'year'), 'minWeightKg': 10, 'maxWeightKg': 44.99}, 'weightBand',
          {'weightBands': [{'minWeightKg': 10, 'maxWeightKg': 20.99, 'perDose': 1.5, 'dosesPerDay': 1}, {'minWeightKg': 21, 'maxWeightKg': 30.99, 'perDose': 2.5, 'dosesPerDay': 1}, {'minWeightKg': 31, 'maxWeightKg': 44.99, 'perDose': 4, 'dosesPerDay': 1}]}, [R(Nl, '2.1, Table 1')], dur=ONE, notes=[PEGN]),
      reg('infant', 'febrile-neutropenia', T('کودک زیر ۱۰ kg — ۰٫۱ mg/kg (۰٫۰۱ mL/kg) زیرجلدی', 'Children under 10 kg — 0.1 mg/kg (0.01 mL/kg) SC'), {'maxAge': age(18, 'year'), 'maxWeightKg': 9.99}, 'weightBased', {'perKgPerDose': 0.1, 'intervalHours': 24}, [R(Nl, '2.1, Table 1')], dur=ONE, notes=[PEGN])],
     [CI('hyper', 'سابقه حساسیت جدی به پگ‌فیلگراستیم یا فیلگراستیم.', 'History of serious hypersensitivity to pegfilgrastim or filgrastim.', [R(Nl, '4')])],
     warn=[W('پارگی طحال؛ ARDS؛ حساسیت جدی؛ بحران داسی‌شکل؛ گلومرولونفریت؛ لکوسیتوز؛ سندرم نشت مویرگی؛ MDS/AML.', 'Splenic rupture; ARDS; serious hypersensitivity; sickle-cell crises; glomerulonephritis; leukocytosis; capillary leak syndrome; MDS/AML.', [R(Nl, '5')])],
     exs=[ex('adult', 'pfs-6', {'perDose': 6, 'mlPerDose': 0.6}, ageYears=50, weightKg=70), ex('child', 'pfs-6', {'perDose': 1.5, 'mlPerDose': 0.15}, ageYears=4, weightKg=15),
          ex('child', 'pfs-6', {'perDose': 4, 'mlPerDose': 0.4}, ageYears=10, weightKg=35), ex('infant', 'pfs-6', {'perDose': 0.8, 'mlPerDose': 0.08}, ageYears=0.5, weightKg=8)])
print('s14d ok')
