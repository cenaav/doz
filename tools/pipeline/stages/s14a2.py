"""Stage 14a (part 2) — blood products, electrolytes and antidotes: albumin 25%, potassium phosphates, factor VIII (Advate), 4F-PCC (Kcentra), fibrinogen (RiaSTAP), IVIG (Gammagard Liquid),
physostigmine, dimercaprol, edetate calcium disodium, succimer, penicillamine, botulism antitoxin (BAT), terlipressin."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None, dur=ONE: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=dur, notes=notes, allowed=allowed, limits=limits)
PLASMA_W = lambda src, sec: W('فرآورده مشتق از پلاسمای انسانی — خطر نظری انتقال عوامل عفونی.', 'Human plasma-derived — theoretical risk of transmitting infectious agents.', [R(src, sec)])

add_disease('hypophosphatemia', 'کمبود فسفات خون (هیپوفسفاتمی)', 'Hypophosphataemia', ['hypophosphatemia', 'فسفر پایین', 'کمبود فسفات'], ['E83.39'], 'nephrology')
add_disease('cirrhosis-ascites', 'آسیت سیروزی (پاراسنتز حجیم)', 'Cirrhotic ascites (large-volume paracentesis)', ['ascites', 'آسیت', 'پاراسنتز'], ['R18.8'], 'gastroenterology')
add_disease('fibrinogen-deficiency', 'کمبود مادرزادی فیبرینوژن', 'Congenital fibrinogen deficiency', ['afibrinogenemia', 'هیپوفیبرینوژنمی', 'کمبود فیبرینوژن'], ['D68.2'], 'hematology')
add_disease('primary-immunodeficiency', 'نقص ایمنی اولیه (هومورال)', 'Primary humoral immunodeficiency', ['PI', 'PID', 'نقص ایمنی مادرزادی', 'هیپوگاماگلوبولینمی'], ['D80.9'], 'allergy')
add_disease('cidp', 'پلی‌نوروپاتی دمیلینه‌کننده التهابی مزمن (CIDP)', 'Chronic inflammatory demyelinating polyneuropathy (CIDP)', ['CIDP', 'پلی نوروپاتی دمیلینه'], ['G61.81'], 'neurology')
add_disease('anticholinergic-toxicity', 'مسمومیت آنتی‌کولینرژیک', 'Anticholinergic toxicity', ['anticholinergic syndrome', 'مسمومیت آتروپینی', 'آنتی کولینرژیک'], ['T44.3X1A'], 'toxicology')
add_disease('heavy-metal-poisoning', 'مسمومیت با فلزات سنگین (سرب، آرسنیک، جیوه، طلا)', 'Heavy-metal poisoning (lead, arsenic, mercury, gold)', ['lead poisoning', 'مسمومیت سرب', 'آرسنیک', 'جیوه'], ['T56.0X1A'], 'toxicology')
add_disease('wilson-disease', 'بیماری ویلسون', 'Wilson disease', ['wilson', 'ویلسون', 'تجمع مس'], ['E83.01'], 'gastroenterology')
add_disease('cystinuria', 'سیستینوری (سنگ سیستین)', 'Cystinuria (cystine stones)', ['cystinuria', 'سنگ سیستین', 'سیستینوری'], ['E72.01'], 'nephrology')
add_disease('botulism', 'بوتولیسم', 'Botulism', ['botulism', 'بوتولیسم', 'مسمومیت غذایی بوتولینوم'], ['A05.1'], 'toxicology')
add_disease('hepatorenal-syndrome', 'سندرم هپاتورنال', 'Hepatorenal syndrome', ['HRS', 'هپاتورنال', 'نارسایی کلیه در سیروز'], ['K76.7'], 'gastroenterology')

Ab = fda('albuminex-25', 'FDA Albuminex 25%', 'Albuminex (albumin human) 25% solution — Prescribing Information', sid('albumin'))
drug('albumin', 'blood', 'آلبومین انسانی ۲۵٪', 'Albumin (human) 25%', T('کلوئید پلاسمایی', 'Plasma colloid'), [{'name': 'Albuminex', 'market': 'US'}], ['albumin', 'آلبومین', 'human albumin'],
     [form('vial-25', 'injection', 'iv', '25% (25 g/100 mL; 12.5 g/50 mL)', 0.25, 'g', [R(Ab, '3')], vol=1)],
     [reg('hypovol', 'shock', T('هیپوولمی بزرگسال — شروع ۲۵ g؛ در صورت عدم ثبات طی ۱۵ تا ۳۰ دقیقه دوز دیگر', 'Hypovolaemia, adults — initial 25 g; repeat if not stable within 15–30 min'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Ab, '2.1')], unit='g', dur=ONE,
          notes=[note('نارسایی حاد کبد: ۱۲ تا ۲۵ g. سرعت معمول ۱ تا ۲ mL/دقیقه. هرگز با آب مقطر رقیق نشود (همولیز).', 'Acute liver failure: 12–25 g. Usual rate 1–2 mL/min. Never dilute with sterile water (haemolysis).', [R(Ab, '2.1'), R(Ab, '2.3')])]),
      NC('para', 'cirrhosis-ascites', 'پیشگیری از کاهش حجم مرکزی پس از پاراسنتز آسیت سیروزی — ۸ g به‌ازای هر ۱۰۰۰ mL مایع خارج‌شده', 'Prevention of central volume depletion after paracentesis — 8 g per 1000 mL of ascitic fluid removed', A18,
         'دوز به حجم مایع خارج‌شده بستگی دارد (نه وزن): مثلاً ۵ لیتر → ۴۰ g. هیپوآلبومینمی و سوختگی: ۵۰ تا ۷۵ g.', 'Dose depends on volume removed, not weight: e.g. 5 L → 40 g. Hypoalbuminaemia and burns: 50–75 g.', [R(Ab, '2.1')])],
     [CI('ci', 'حساسیت به آلبومین؛ کم‌خونی شدید یا نارسایی قلب با حجم داخل‌عروقی طبیعی یا بالا.', 'Hypersensitivity to albumin; severe anaemia or cardiac failure with normal or increased intravascular volume.', [R(Ab, '4')])],
     warn=[W('هیپرولمی و ادم ریه (سرعت متناسب با همودینامیک)؛ حساسیت.', 'Hypervolaemia and pulmonary oedema (match rate to haemodynamics); hypersensitivity.', [R(Ab, '5')]), PLASMA_W(Ab, '5.6')],
     exs=[ex('hypovol', 'vial-25', {'perDose': 25, 'mlPerDose': 100}, ageYears=50, weightKg=70)])

Kp = fda('potassium-phosphates', 'FDA Potassium phosphates', 'Potassium phosphates injection 3 mmol P/mL — Prescribing Information', sid('potassium-phosphate'))
drug('potassium-phosphate', 'blood', 'پتاسیم فسفات (تزریقی)', 'Potassium phosphates (injection)', T('مکمل الکترولیت', 'Electrolyte replenisher'), [{'name': 'Potassium Phosphates', 'market': 'US'}], ['potassium phosphate', 'پتاسیم فسفات', 'فسفات تزریقی', 'KPhos'],
     [form('vial-3', 'injection', 'iv', 'Phosphorus 3 mmol/mL (potassium 4.4 mEq/mL), 5/15 mL vials', 1, 'application', [R(Kp, '3')], per='vial')],
     [NC('hypo', 'hypophosphatemia', 'اصلاح هیپوفسفاتمی در مایعات وریدی — فقط اگر پتاسیم سرم زیر ۴ mEq/L', 'Correction of hypophosphataemia in IV fluids — only if serum potassium is below 4 mEq/L', {},
         'دوز فردی بر اساس فسفر سرم، وزن و منابع دیگر؛ هر mL حاوی ۳ mmol فسفر و ۴٫۴ mEq پتاسیم. فقط پس از رقیق‌سازی در حجم بیشتر؛ سرعت و غلظت حداکثر طبق بخش ۲. فسفر، پتاسیم، کلسیم و منیزیم پایش شود.',
         'Dose individualised by serum phosphorus, weight and other sources; each mL has 3 mmol phosphorus and 4.4 mEq potassium. Only after dilution in a larger volume; maximum rate and concentration per section 2. Monitor phosphorus, potassium, calcium and magnesium.', [R(Kp, '2.1'), R(Kp, '2.2')])],
     [CI('ci', 'هیپرکالمی؛ هیپرفسفاتمی؛ نارسایی شدید کلیه (eGFR زیر ۳۰) یا ESRD؛ هیپرکلسمی یا هیپوکلسمی قابل‌توجه.', 'Hyperkalaemia; hyperphosphataemia; severe renal impairment (eGFR <30) or ESRD; hypercalcaemia or significant hypocalcaemia.', [R(Kp, '4')])],
     warn=[W('عوارض قلبی جدی با تزریق رقیق‌نشده یا سریع؛ آمبولی ریه از رسوب (کلسیم-فسفات)؛ هیپرکالمی؛ هیپوکلسمی؛ آسیب ورید.', 'Serious cardiac reactions with undiluted or rapid infusion; pulmonary embolism from precipitates (calcium phosphate); hyperkalaemia; hypocalcaemia; vein damage.', [R(Kp, '5')])])

Ad = fda('advate', 'FDA Advate', 'Advate (antihemophilic factor, recombinant) — Prescribing Information', sid('factor-viii'))
drug('factor-viii', 'blood', 'فاکتور ۸ نوترکیب', 'Antihemophilic factor VIII (recombinant)', T('فاکتور انعقادی', 'Coagulation factor'), [{'name': 'Advate', 'market': 'US'}], ['advate', 'factor 8', 'فاکتور هشت', 'فاکتور VIII', 'آدویت'],
     [form('vial-1000', 'powder-for-injection', 'iv', '1000 IU vial (also 250–4000 IU)', 1000, 'unit', [R(Ad, '3')], per='vial')],
     [reg('proph', 'hemophilia-a', T('پیشگیری روتین هموفیلی A — ۲۰ تا ۴۰ IU/kg یک روز در میان (۳ تا ۴ بار در هفته)', 'Routine prophylaxis in haemophilia A — 20–40 IU/kg every other day (3–4 times weekly)'), {}, 'weightBased', {'perKgPerDose': 20, 'perKgPerDoseMax': 40, 'intervalHours': 48}, [R(Ad, '2.1')], unit='unit',
          notes=[note('درمان خونریزی یا جراحی: دوز (IU) = وزن (kg) × افزایش مطلوب فاکتور ۸ (٪) × ۰٫۵؛ دفعات طبق نوع خونریزی. یا هر ۳ روز با هدف حداقل ۱٪.', 'Bleeding or surgery: dose (IU) = weight (kg) × desired FVIII rise (%) × 0.5; frequency by bleed type. Or every third day targeting trough ≥1%.', [R(Ad, '2.1')])])],
     [CI('ci', 'حساسیت تهدیدکننده حیات به پروتئین موش یا همستر یا اجزای فرآورده.', 'Life-threatening hypersensitivity to mouse or hamster protein or product constituents.', [R(Ad, '4')])],
     warn=[W('واکنش حساسیتی؛ آنتی‌بادی مهارکننده (inhibitor) — اگر پاسخ مورد انتظار نبود بررسی شود.', 'Hypersensitivity; neutralising antibodies (inhibitors) — test if the expected response is not achieved.', [R(Ad, '5')])],
     exs=[ex('proph', 'vial-1000', {'perDose': 400, 'upperPerDose': 800}, ageYears=10, weightKg=20)])

Kc = fda('kcentra', 'FDA Kcentra', 'Kcentra (prothrombin complex concentrate, human) — Prescribing Information', sid('pcc'))
PCC = lambda id, fa, en, kg, mx: reg(id, 'anticoagulant-reversal', T(fa, en), A18, 'weightBased', {'perKgPerDose': kg, 'intervalHours': 24}, [R(Kc, '2.1, Table 1')], unit='unit', dur=ONE, limits={'maxPerDose': mx, 'refs': [R(Kc, '2.1, Table 1')]})
drug('kcentra', 'blood', 'کنسانتره کمپلکس پروترومبین ۴ فاکتوری (PCC)', 'Prothrombin complex concentrate, 4-factor (Kcentra)', T('فاکتورهای انعقادی II، VII، IX، X', 'Coagulation factors II, VII, IX, X'), [{'name': 'Kcentra', 'market': 'US'}], ['kcentra', 'pcc', 'beriplex', 'برپلکس', 'کمپلکس پروترومبین'],
     [form('vial-1000', 'powder-for-injection', 'iv', '1000 unit vial (factor IX units; actual potency on carton)', 1000, 'unit', [R(Kc, '3')], per='vial')],
     [PCC('inr2', 'برگشت اثر وارفارین در خونریزی حاد یا جراحی فوری — INR ۲ تا <۴: ۲۵ واحد/kg (حداکثر ۲۵۰۰)', 'Reversal of warfarin for acute major bleeding or urgent surgery — INR 2–<4: 25 units/kg (max 2500)', 25, 2500),
      PCC('inr4', 'برگشت اثر وارفارین — INR ۴ تا ۶: ۳۵ واحد/kg (حداکثر ۳۵۰۰)', 'Warfarin reversal — INR 4–6: 35 units/kg (max 3500)', 35, 3500),
      PCC('inr6', 'برگشت اثر وارفارین — INR بالای ۶: ۵۰ واحد/kg (حداکثر ۵۰۰۰)', 'Warfarin reversal — INR >6: 50 units/kg (max 5000)', 50, 5000)],
     [CI('ci', 'آنافیلاکسی یا واکنش شدید به اجزا (هپارین، فاکتورها، پروتئین C و S، آنتی‌ترومبین، آلبومین)؛ DIC؛ HIT شناخته‌شده (حاوی هپارین).', 'Anaphylaxis or severe reaction to any component (heparin, factors, proteins C and S, antithrombin, albumin); DIC; known HIT (contains heparin).', [R(Kc, '4')])],
     warn=[W('هشدار جعبه‌ای: ترومبوآمبولی شریانی و وریدی (کشنده و غیرکشنده). همراه ویتامین K داده شود؛ تکرار دوز توصیه نمی‌شود؛ وزن بالای ۱۰۰ kg = ۱۰۰ kg.', 'Boxed warning: arterial and venous thromboembolism (fatal and non-fatal). Give with vitamin K; repeat dosing not recommended; weight above 100 kg counts as 100 kg.', [R(Kc, 'Boxed Warning'), R(Kc, '2.1')]), PLASMA_W(Kc, '5.3')],
     exs=[ex('inr2', 'vial-1000', {'perDose': 1750}, ageYears=70, weightKg=70), ex('inr4', 'vial-1000', {'perDose': 2450}, ageYears=70, weightKg=70), ex('inr6', 'vial-1000', {'perDose': 3500}, ageYears=70, weightKg=70),
          ex('inr6', 'vial-1000', {'perDose': 5000}, ageYears=60, weightKg=120)])

Rs = fda('riastap', 'FDA RiaSTAP', 'RiaSTAP (fibrinogen concentrate, human) — Prescribing Information', sid('fibrinogen'))
drug('fibrinogen', 'blood', 'کنسانتره فیبرینوژن', 'Fibrinogen concentrate (human)', T('فاکتور انعقادی', 'Coagulation factor'), [{'name': 'RiaSTAP', 'market': 'US'}], ['riastap', 'haemocomplettan', 'فیبرینوژن', 'هموکمپلتان'],
     [form('vial-1g', 'powder-for-injection', 'iv', 'About 1 g vial (actual potency on label)', 1000, 'mg', [R(Rs, '3')], per='vial')],
     [once('unknown', 'fibrinogen-deficiency', 'خونریزی حاد در کمبود مادرزادی فیبرینوژن (سطح نامعلوم) — ۷۰ mg/kg وریدی آهسته', 'Acute bleeding in congenital fibrinogen deficiency (level unknown) — 70 mg/kg slow IV', {}, 70, None, [R(Rs, '2.1')],
           notes=[note('سطح معلوم: دوز (mg/kg) = (سطح هدف − سطح فعلی mg/dL) ÷ ۱٫۷. هدف ۱۰۰ mg/dL تا هموستاز. سرعت حداکثر ۵ mL/دقیقه.', 'Known level: dose (mg/kg) = (target − measured, mg/dL) ÷ 1.7. Target 100 mg/dL until haemostasis. Rate max 5 mL/min.', [R(Rs, '2'), R(Rs, '2.3')])])],
     [CI('hyper', 'آنافیلاکسی یا واکنش شدید به فرآورده‌های پلاسمای انسانی.', 'Anaphylactic or severe reactions to human plasma-derived products.', [R(Rs, '4')])],
     warn=[W('واکنش حساسیتی؛ ترومبوز.', 'Hypersensitivity; thrombosis.', [R(Rs, '5')]), PLASMA_W(Rs, '5.3')],
     exs=[ex('unknown', 'vial-1g', {'perDose': 1400}, ageYears=20, weightKg=20)])

Gg = fda('gammagard', 'FDA Gammagard Liquid', 'Gammagard Liquid (immune globulin infusion, human) 10% — Prescribing Information', sid('ivig'))
drug('ivig', 'blood', 'ایمونوگلوبولین وریدی (IVIG)', 'Immune globulin intravenous (IVIG) 10%', T('ایمونوگلوبولین انسانی', 'Human immune globulin'), [{'name': 'Gammagard Liquid', 'market': 'US'}], ['ivig', 'immune globulin', 'ایمونوگلوبولین', 'آی وی آی جی', 'gammagard'],
     [form('sol-10', 'injection', 'iv', '10% (100 mg/mL)', 100, 'mg', [R(Gg, '3')], vol=1)],
     [once('pi', 'primary-immunodeficiency', 'نقص ایمنی اولیه — ۳۰۰ تا ۶۰۰ mg/kg وریدی هر ۳ تا ۴ هفته', 'Primary immunodeficiency — 300–600 mg/kg IV every 3–4 weeks', {'minAge': age(2, 'year')}, 300, 600, [R(Gg, '2.1, Table 1')],
           notes=[note('شروع ۰٫۵ mL/kg/ساعت ۳۰ دقیقه، سپس هر ۳۰ دقیقه افزایش تا ۵ mL/kg/ساعت. تنظیم با سطح IgG.', 'Start 0.5 mL/kg/h for 30 min, then increase every 30 min up to 5 mL/kg/h. Adjust to IgG levels.', [R(Gg, '2.1, Table 1')])]),
      once('cidp', 'cidp', 'CIDP بزرگسال — القا ۲ g/kg تقسیم طی ۲ تا ۵ روز؛ نگهدارنده ۱ g/kg هر ۳ هفته', 'CIDP, adults — induction 2 g/kg divided over 2–5 days; maintenance 1 g/kg every 3 weeks', A18, 2000, None, [R(Gg, '2.3, Table 5')],
           notes=[note('عدد ماشین‌حساب کل دوز القا است (تقسیم طی ۲ تا ۵ روز). نوروپاتی حرکتی چندکانونی: ۰٫۵ تا ۲٫۴ g/kg/ماه.', 'The calculator gives the total induction dose (divide over 2–5 days). Multifocal motor neuropathy: 0.5–2.4 g/kg/month.', [R(Gg, '2.3'), R(Gg, '2.2')])])],
     [CI('ci', 'آنافیلاکسی یا حساسیت شدید به ایمونوگلوبولین انسانی؛ کمبود IgA با آنتی‌بادی ضد IgA و سابقه حساسیت.', 'Anaphylaxis or severe hypersensitivity to human immune globulin; IgA deficiency with anti-IgA antibodies and history of hypersensitivity.', [R(Gg, '4')])],
     warn=[W('هشدار جعبه‌ای: ترومبوز؛ اختلال و نارسایی حاد کلیه — کمترین غلظت و سرعت در بیماران پرخطر، هیدراتاسیون کافی.', 'Boxed warning: thrombosis; renal dysfunction and acute renal failure — use minimum concentration and rate in at-risk patients, ensure hydration.', [R(Gg, 'Boxed Warning')]),
           W('مننژیت آسپتیک؛ همولیز؛ TRALI؛ افزایش ویسکوزیته.', 'Aseptic meningitis; haemolysis; TRALI; hyperviscosity.', [R(Gg, '5')])],
     exs=[ex('pi', 'sol-10', {'perDose': 21000, 'mlPerDose': 210, 'upperPerDose': 42000}, ageYears=30, weightKg=70), ex('cidp', 'sol-10', {'perDose': 140000, 'mlPerDose': 1400}, ageYears=50, weightKg=70)])

Ph = fda('anticholium', 'FDA Anticholium', 'Anticholium (physostigmine salicylate) injection — imported product labeling', sid('physostigmine'))
drug('physostigmine', 'nervous-system', 'فیزوستیگمین', 'Physostigmine', T('مهارکننده کولین‌استراز (پادزهر)', 'Cholinesterase inhibitor (antidote)'), [{'name': 'Anticholium', 'market': 'US'}], ['anticholium', 'آنتی کولیوم', 'فیزوستیگمین'],
     [unitform('amp', 'injection', 'iv', '5 mL ampoule (IM or slow IV)', [R(Ph, 'How Supplied')], per='vial')],
     [NC('adult', 'anticholinergic-toxicity', 'برگشت اثر مرکزی مسمومیت آنتی‌کولینرژیک — بزرگسال ۰٫۵ تا ۱ mg عضلانی یا وریدی آهسته', 'Reversal of central anticholinergic toxicity — adult 0.5–1 mg IM or slow IV', A18,
         'وریدی حداکثر ۱ mg/دقیقه؛ در صورت نیاز هر ۱۰ تا ۳۰ دقیقه تکرار. غلظت آمپول این فرآورده وارداتی در برچسب موجود ذکر نشده؛ حجم از روی بسته محاسبه شود.', 'IV no faster than 1 mg/min; repeat every 10–30 min if needed. Ampoule concentration of this imported product is not stated in the available labeling; compute volume from the package.', [R(Ph, 'Dosage and Administration')]),
      NC('child', 'anticholinergic-toxicity', 'کودک — ۰٫۰۲ mg/kg عضلانی یا وریدی آهسته (حداکثر ۰٫۵ mg/دقیقه)؛ تکرار هر ۵ تا ۱۰ دقیقه تا حداکثر ۲ mg', 'Children — 0.02 mg/kg IM or slow IV (max 0.5 mg/min); repeat every 5–10 min up to 2 mg total', {'maxAge': age(18, 'year')},
         'تکرار فقط اگر اثرات سمی ادامه دارد و علائم کولینرژیک نیست. اقدامات حمایتی همیشه.', 'Repeat only while toxic effects persist without cholinergic signs. Always with supportive care.', [R(Ph, 'Dosage and Administration')])],
     [CI('ci', 'حساسیت؛ آسم؛ گانگرن؛ بیماری کرونر؛ انسداد مکانیکی روده یا ادرار؛ دیستروفی میوتونیک؛ آسیب مغزی بسته؛ پس از شل‌کننده‌های دپلاریزان (سوکسینیل‌کولین).', 'Hypersensitivity; asthma; gangrene; coronary heart disease; mechanical bowel or urinary obstruction; myotonic dystrophy; closed head injury; after depolarising relaxants (succinylcholine).', [R(Ph, 'Contraindications')])])

Bl = fda('bal-in-oil', 'FDA BAL in Oil', 'BAL in Oil (dimercaprol injection) 100 mg/mL — Prescribing Information', sid('dimercaprol')); d = R(Bl, 'Dosage and Administration')
drug('dimercaprol', 'various', 'دیمرکاپرول (BAL)', 'Dimercaprol (BAL)', T('شلات‌کننده فلزات سنگین', 'Heavy-metal chelator'), [{'name': 'BAL in Oil', 'market': 'US'}], ['bal', 'بال', 'دیمرکاپرول', 'british anti-lewisite'],
     [form('amp-100', 'injection', 'im', '100 mg/mL in oil, 3 mL ampoule (deep IM only)', 100, 'mg', [R(Bl, 'How Supplied')], vol=1)],
     [once('as-mild', 'heavy-metal-poisoning', 'مسمومیت خفیف آرسنیک یا طلا — ۲٫۵ mg/kg عضلانی عمقی ۴ بار در روز، ۲ روز', 'Mild arsenic or gold poisoning — 2.5 mg/kg deep IM four times daily for 2 days', {}, 2.5, None, [d],
           notes=[note('سپس روز سوم دو بار و بعد روزانه تا ۱۰ روز. شدید: ۳ mg/kg هر ۴ ساعت ۲ روز. جیوه: ۵ mg/kg سپس ۲٫۵ mg/kg یک یا دو بار در روز ۱۰ روز. فقط عضلانی عمقی.', 'Then twice on day 3 and daily for 10 days. Severe: 3 mg/kg every 4 h for 2 days. Mercury: 5 mg/kg then 2.5 mg/kg once or twice daily for 10 days. Deep IM only.', [d])], dur=None),
      once('lead', 'heavy-metal-poisoning', 'انسفالوپاتی حاد سرب — ۴ mg/kg عضلانی، سپس هر ۴ ساعت همراه EDTA در محل جدا', 'Acute lead encephalopathy — 4 mg/kg IM, then every 4 h with edetate calcium disodium at a separate site', {}, 4, None, [d], dur=None)],
     [CI('ci', 'اغلب موارد نارسایی کبد (جز زردی پس از آرسنیک)؛ در نارسایی حاد کلیه قطع یا احتیاط شدید.', 'Most cases of hepatic insufficiency (except post-arsenical jaundice); stop or use extreme caution if acute renal failure develops.', [R(Bl, 'Contraindications')])],
     warn=[W('درد محل تزریق؛ تب در حدود ۳۰٪ کودکان؛ کاهش گذرای نوتروفیل.', 'Injection-site pain; fever in about 30% of children; transient neutrophil reduction.', [R(Bl, 'Warnings')])],
     exs=[ex('as-mild', 'amp-100', {'perDose': 175, 'mlPerDose': 1.75}, ageYears=40, weightKg=70), ex('lead', 'amp-100', {'perDose': 80, 'mlPerDose': 0.8}, ageYears=4, weightKg=20)])

Ed = fda('edetate-calcium', 'FDA Edetate Ca disodium', 'Edetate calcium disodium injection 200 mg/mL — Prescribing Information', sid('edta'))
drug('edetate-calcium-disodium', 'various', 'ادتات کلسیم دی‌سدیم (CaNa2EDTA)', 'Edetate calcium disodium (CaNa2EDTA)', T('شلات‌کننده سرب', 'Lead chelator'), [{'name': 'Calcium Disodium Versenate', 'market': 'US'}], ['edta', 'versenate', 'ورسنات', 'ادتات کلسیم'],
     [form('vial-200', 'injection', 'iv', '200 mg/mL, 5 mL vial (1 g)', 200, 'mg', [R(Ed, 'How Supplied')], vol=1)],
     [reg('lead', 'heavy-metal-poisoning', T('مسمومیت سرب بدون علامت (سرب خون ۲۰ تا ۷۰ mcg/dL) — ۱۰۰۰ mg/m²/روز وریدی یا عضلانی', 'Asymptomatic lead poisoning (blood lead 20–70 mcg/dL) — 1000 mg/m²/day IV or IM'), {}, 'bsa', {'perM2PerDay': 1000, 'dividedDoses': 1}, [R(Ed, 'Dosage and Administration')],
          notes=[note('ابتدا منبع سرب حذف شود. انسفالوپاتی سربی و ادم مغزی: عضلانی ترجیح دارد (افزایش کشنده فشار داخل جمجمه با انفوزیون وریدی).', 'Remove the lead source first. Lead encephalopathy with cerebral oedema: IM preferred (fatal ICP rise with IV infusion).', [R(Ed, 'Dosage and Administration'), R(Ed, 'Boxed Warning')])])],
     [CI('ci', 'آنوری؛ بیماری فعال کلیه یا هپاتیت.', 'Anuria; active renal disease or hepatitis.', [R(Ed, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: سمیت کشنده؛ در انسفالوپاتی سربی افزایش کشنده فشار داخل جمجمه با انفوزیون وریدی سریع. با ادتات دی‌سدیم (بدون کلسیم) اشتباه نشود.', 'Boxed warning: potentially fatal toxicity; fatal ICP rise with rapid IV infusion in lead encephalopathy. Do not confuse with edetate disodium (calcium-free).', [R(Ed, 'Boxed Warning')])],
     exs=[ex('lead', 'vial-200', {'perDose': 1000, 'mlPerDose': 5}, ageYears=6, weightKg=25, heightCm=144)])

Ch = fda('chemet', 'FDA Chemet', 'Chemet (succimer) capsules 100 mg — Prescribing Information', sid('succimer'))
drug('succimer', 'various', 'سوکسیمر (DMSA)', 'Succimer (DMSA)', T('شلات‌کننده خوراکی سرب', 'Oral lead chelator'), [{'name': 'Chemet', 'market': 'US'}], ['chemet', 'dmsa', 'کمت', 'سوکسیمر'],
     [tab('cap-100', 100, '100 mg capsule (may be sprinkled on food)', [R(Ch, '3')], per='capsule', form_='capsule')],
     [reg('lead', 'heavy-metal-poisoning', T('مسمومیت سرب کودکان — ۱۰ mg/kg هر ۸ ساعت ۵ روز، سپس هر ۱۲ ساعت ۱۴ روز', 'Lead poisoning in children — 10 mg/kg every 8 h for 5 days, then every 12 h for 14 days'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 10, 'intervalHours': 8}, [R(Ch, '2.2')], dur={'min': 5, 'max': 5},
          notes=[note('یا ۳۵۰ mg/m². کل دوره ۱۹ روز. پیش از شروع منبع سرب حذف؛ CBC، ANC >۱۵۰۰ و آنزیم کبد. هیدراتاسیون کافی.', 'Or 350 mg/m². Total course 19 days. Remove the lead source first; CBC, ANC >1500 and transaminases. Keep well hydrated.', [R(Ch, '2.2'), R(Ch, '2.1'), R(Ch, '2.3')])])],
     [CI('hyper', 'سابقه حساسیت به سوکسیمر.', 'History of hypersensitivity to succimer.', [R(Ch, '4')])],
     warn=[W('واکنش پوستی و حساسیت؛ نوتروپنی؛ سمیت کبد؛ سمیت جنینی.', 'Skin and hypersensitivity reactions; neutropenia; hepatotoxicity; embryo-fetal toxicity.', [R(Ch, '5')])],
     exs=[ex('lead', 'cap-100', {'perDose': 200, 'tabletsPerDoseRounded': 2}, ageYears=4, weightKg=20)])

Cu = fda('cuprimine', 'FDA Cuprimine', 'Cuprimine (penicillamine) capsules 250 mg — Prescribing Information', sid('penicillamine')); d = R(Cu, 'Dosage and Administration')
drug('penicillamine', 'musculoskeletal', 'پنی‌سیلامین', 'Penicillamine', T('شلات‌کننده (مس، سیستین)', 'Chelating agent (copper, cystine)'), [{'name': 'Cuprimine', 'market': 'US'}], ['cuprimine', 'depen', 'کوپریمین', 'پنی سیلامین'],
     [tab('cap-250', 250, '250 mg capsule', [R(Cu, 'Description')], per='capsule', form_='capsule')],
     [NC('wilson', 'wilson-disease', 'بیماری ویلسون — ۰٫۷۵ تا ۱٫۵ g/روز تقسیمی، تنظیم با مس ادرار ۲۴ ساعته', 'Wilson disease — 0.75–1.5 g/day divided, titrated to 24-h urinary copper', {},
         'دوز با دفع مس ادرار و مس آزاد سرم تنظیم می‌شود. ناشتا (۱ ساعت قبل یا ۲ ساعت بعد غذا) و جدا از سایر داروها و شیر. ممکن است مکمل پیریدوکسین لازم باشد.', 'Titrated to urinary copper excretion and free serum copper. On an empty stomach (1 h before or 2 h after food), apart from other drugs and milk. Pyridoxine supplement may be needed.', [d]),
      reg('cyst', 'cystinuria', T('سیستینوری بزرگسال — ۲ g/روز در ۴ دوز (۱ تا ۴ g)', 'Cystinuria, adults — 2 g/day in 4 doses (1–4 g)'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 4}, [d],
          notes=[note('کودک: ۳۰ mg/kg/روز در ۴ دوز. همراه درمان معمول (مایعات فراوان).', 'Children: 30 mg/kg/day in 4 doses. With conventional therapy (high fluid intake).', [d])]),
      reg('cyst-child', 'cystinuria', T('سیستینوری کودکان — ۳۰ mg/kg/روز در ۴ دوز', 'Cystinuria, children — 30 mg/kg/day in 4 doses'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 30, 'dividedDoses': 4}, [d])],
     [CI('ci', 'بارداری (جز ویلسون یا برخی بیماران سیستینوری)؛ شیردهی؛ سابقه آنمی آپلاستیک یا آگرانولوسیتوز با پنی‌سیلامین؛ آرتریت روماتوئید با سابقه یا شواهد نارسایی کلیه.', 'Pregnancy (except Wilson disease or some cystinuria); breastfeeding; prior penicillamine-related aplastic anaemia or agranulocytosis; rheumatoid arthritis with history or evidence of renal insufficiency.', [R(Cu, 'Contraindications')])],
     warn=[W('مرگ از آنمی آپلاستیک، آگرانولوسیتوز، ترومبوسیتوپنی، گودپاسچر و میاستنی — آزمایش ادرار و CBC دو بار در هفته در ابتدا.', 'Fatalities from aplastic anaemia, agranulocytosis, thrombocytopenia, Goodpasture syndrome and myasthenia gravis — urinalysis and CBC twice weekly initially.', [R(Cu, 'Warnings')])],
     exs=[ex('cyst', 'cap-250', {'perDose': 500, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70), ex('cyst-child', 'cap-250', {'perDose': 270, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=36)])

Bt = fda('bat-antitoxin', 'FDA BAT', 'BAT (botulism antitoxin heptavalent, equine) — Prescribing Information', sid('botulism-antitoxin'))
drug('botulism-antitoxin', 'anti-infectives', 'آنتی‌توکسین بوتولیسم هفت‌ظرفیتی (BAT)', 'Botulism antitoxin heptavalent (BAT)', T('آنتی‌توکسین اسبی', 'Equine antitoxin'), [{'name': 'BAT', 'market': 'US'}], ['bat', 'botulism antitoxin', 'ضد سم بوتولیسم', 'آنتی توکسین بوتولیسم'],
     [form('vial', 'injection', 'iv', 'Single-use vial (A–G antitoxin; dilute 1:10)', 1, 'application', [R(Bt, '3')], per='vial')],
     [reg('adult', 'botulism', T('بوتولیسم علامت‌دار (۱۷ سال به بالا) — یک ویال انفوزیون وریدی آهسته پس از رقیق‌سازی ۱:۱۰', 'Symptomatic botulism (≥17 y) — one vial by slow IV infusion after 1:10 dilution'), {'minAge': age(17, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Bt, '2.1, Table 1')], unit='application', dur=ONE,
          notes=[note('شروع ۰٫۵ mL/دقیقه ۳۰ دقیقه، سپس هر ۳۰ دقیقه دو برابر تا ۲ mL/دقیقه. کودک ۱ تا <۱۷ سال: ۲۰ تا ۱۰۰٪ دوز بزرگسال بر اساس وزن (جدول ۲). علائم حیاتی در طول انفوزیون پایش.', 'Start 0.5 mL/min for 30 min, then double every 30 min to 2 mL/min. Children 1–<17 y: 20–100% of adult dose by weight (Table 2). Monitor vitals throughout.', [R(Bt, '2.1, Table 1'), R(Bt, '2.1')])])],
     warn=[W('واکنش حساسیتی و آنافیلاکسی (پروتئین اسبی)؛ بیماری سرم تأخیری؛ واکنش انفوزیون؛ تداخل با برخی گلوکومترها (مالتوز).', 'Hypersensitivity and anaphylaxis (equine protein); delayed serum sickness; infusion reactions; interference with some glucose meters (maltose).', [R(Bt, '5')])],
     exs=[ex('adult', 'vial', {'perDose': 1}, ageYears=40, weightKg=70)])

Tv = fda('terlivaz', 'FDA Terlivaz', 'Terlivaz (terlipressin) for injection 0.85 mg — Prescribing Information', sid('terlipressin'))
drug('terlipressin', 'systemic-hormones', 'ترلیپرسین', 'Terlipressin', T('آنالوگ وازوپرسین', 'Vasopressin analogue'), [{'name': 'Terlivaz', 'market': 'US'}], ['terlivaz', 'glypressin', 'گلیپرسین', 'ترلیپرسین'],
     [form('vial-0-85', 'powder-for-injection', 'iv', '0.85 mg vial', 0.85, 'mg', [R(Tv, '3')], per='vial')],
     [reg('hrs', 'hepatorenal-syndrome', T('سندرم هپاتورنال با کاهش سریع عملکرد کلیه — ۰٫۸۵ mg بولوس وریدی آهسته (۲ دقیقه) هر ۶ ساعت، روز ۱ تا ۳', 'Hepatorenal syndrome with rapid reduction in kidney function — 0.85 mg slow IV bolus (2 min) every 6 h, days 1–3'), A18, 'fixed', {'perDose': 0.85, 'dosesPerDay': 4}, [R(Tv, '2.2')],
          notes=[note('روز ۴: اگر کراتینین ۳۰٪ یا بیشتر کاهش یافته ادامه؛ کمتر: طبق نمودار برچسب افزایش تا ۱٫۷ mg. پیش از شروع SpO2 و درجه ACLF؛ پالس‌اکسی‌متری مداوم.', 'Day 4: continue if creatinine fell ≥30%; less: may increase per label chart (to 1.7 mg). Check SpO2 and ACLF grade first; continuous pulse oximetry.', [R(Tv, '2.2'), R(Tv, '2.1'), R(Tv, '2')])])],
     [CI('ci', 'هیپوکسی یا بدتر شدن علائم تنفسی؛ ایسکمی کرونر، محیطی یا مزانتریک فعال.', 'Hypoxia or worsening respiratory symptoms; ongoing coronary, peripheral or mesenteric ischaemia.', [R(Tv, '4')])],
     warn=[W('هشدار جعبه‌ای: نارسایی تنفسی جدی یا کشنده (بیشتر با حجم اضافه یا ACLF درجه ۳) — SpO2 زیر ۹۰٪ شروع نشود یا قطع شود.', 'Boxed warning: serious or fatal respiratory failure (higher with volume overload or ACLF grade 3) — do not start or stop if SpO2 <90%.', [R(Tv, 'Boxed Warning')]),
           W('ایسکمی؛ عدم واجد شرایط شدن برای پیوند کبد؛ سمیت جنینی.', 'Ischaemic events; ineligibility for liver transplant; embryo-fetal toxicity.', [R(Tv, '5')])],
     exs=[ex('hrs', 'vial-0-85', {'perDose': 0.85, 'dosesPerDay': 4}, ageYears=55, weightKg=75)])
print('s14a2 ok')
