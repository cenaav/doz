"""Stage 14b (part 1) — new forms/indications for existing drugs (methotrexate injection, Revatio sildenafil for PAH,
long-acting injectable paliperidone/haloperidol/fluphenazine/aripiprazole) and beta-lactam/beta-lactamase-inhibitor combinations
(ceftazidime-avibactam, ceftolozane-tazobactam, meropenem-vaborbactam)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs, allowed=None: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs, allowed=allowed)
bsa = lambda id, dis, fa, en, pop, m2, refs, dur=ONE, notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'bsa', {'perM2PerDay': m2, 'dividedDoses': 1}, refs, dur=dur, notes=notes, allowed=allowed, limits=limits)
X = lambda r, f, mg, ml=None, **k: ex(r, f, {'perDose': mg, **({'mlPerDose': ml} if ml is not None else {})}, ageYears=k.get('age', 55), weightKg=k.get('w', 80), heightCm=k.get('h', 180))
ONC = ('فقط زیر نظر پزشک متخصص شیمی‌درمانی و در مرکز مجهز. عدد ماشین‌حساب = mg/m² برچسب × سطح بدن (Mosteller)؛ پروتکل، فاصله دوره‌ها، تنظیم بر اساس CBC و عملکرد کلیه/کبد با تیم انکولوژی.',
       'Only under an oncologist in an equipped centre. Calculator = label mg/m² × BSA (Mosteller); protocol, cycle interval and adjustment for CBC and renal/hepatic function rest with the oncology team.')
onc = lambda src, sec: note(*ONC, [R(src, sec)])
LAI = lambda src, sec: note('فقط تزریق عضلانی توسط کادر درمان. در بیمارانی که قبلاً این دارو را نگرفته‌اند ابتدا تحمل شکل خوراکی سنجیده شود.', 'IM injection by a healthcare professional only. Establish tolerability with the oral form first in patients new to the drug.', [R(src, sec)])

add_disease('osteosarcoma', 'استئوسارکوم', 'Osteosarcoma', ['osteosarcoma', 'سارکوم استخوان', 'استئوسارکوما'], ['C41.9'], 'oncology')
add_disease('head-neck-cancer', 'سرطان سلول سنگفرشی سر و گردن', 'Squamous cell carcinoma of the head and neck', ['SCCHN', 'سرطان سر و گردن', 'head and neck cancer'], ['C76.0'], 'oncology')
add_disease('pulmonary-arterial-hypertension', 'فشار خون شریان ریوی (PAH)', 'Pulmonary arterial hypertension (PAH)', ['PAH', 'فشار ریوی', 'هیپرتانسیون ریوی', 'pulmonary hypertension'], ['I27.0'], 'cardiology')

# --- methotrexate injection (Accord, 25 mg/mL preservative-free) ---
Mi = fda('mtx-injection', 'FDA Methotrexate inj', 'Methotrexate injection 25 mg/mL (Accord) — Prescribing Information', sid('mtx-inj'))
IT = lambda id, fa, en, pop, mg: reg(id, 'acute-lymphoblastic-leukemia', T(fa, en), pop, 'fixed', {'perDose': mg, 'dosesPerDay': 1}, [R(Mi, '2.4')], dur=ONE, allowed=['inj-25'],
    notes=[note('فقط فرآورده بدون نگهدارنده، رقیق‌شده تا ۱ mg/mL در سالین بدون نگهدارنده. درمان: هر ۲ تا ۵ روز تا پاکسازی CSF.', 'Preservative-free product only, diluted to 1 mg/mL in preservative-free saline. Treatment: every 2–5 days until CSF clears.', [R(Mi, '2.4'), R(Mi, '2.1')])])
patch('methotrexate',
      add_forms=[form('inj-25', 'injection', 'iv', '25 mg/mL preservative-free (50 mg/2 mL, 250 mg/10 mL, 1 g/40 mL) — IV, IM, SC or intrathecal', 25, 'mg', [R(Mi, '3')], vol=1)],
      add_regs=[bsa('osteo', 'osteosarcoma', 'استئوسارکوم — ۱۲ g/m² وریدی طی ۴ ساعت (حداکثر ۲۰ g در هر دوز) با نجات لکوورین', 'Osteosarcoma — 12 g/m² IV over 4 h (max 20 g per dose) with leucovorin rescue', {}, 12000, [R(Mi, '2.6')], allowed=['inj-25'],
                    limits={'maxPerDose': 20000, 'refs': [R(Mi, '2.6')]}, notes=[onc(Mi, '2.6'), note('دوز بالا: نجات لکوورین، هیدراتاسیون، قلیایی‌سازی ادرار و پایش سطح متوترکسات الزامی.', 'High dose: leucovorin rescue, hydration, urine alkalinisation and methotrexate level monitoring are mandatory.', [R(Mi, '2.2')])]),
                bsa('scchn', 'head-neck-cancer', 'سرطان سلول سنگفرشی سر و گردن — ۴۰ تا ۶۰ mg/m² وریدی هفته‌ای یک بار', 'Squamous cell head and neck cancer — 40–60 mg/m² IV once weekly', A18, 40, [R(Mi, '2.8')], allowed=['inj-25'], notes=[onc(Mi, '2.8')]),
                bsa('breast', 'breast-cancer', 'سرطان پستان — ۴۰ mg/m² وریدی در رژیم چنددارویی با سیکلوفسفامید و فلوئوروراسیل', 'Breast cancer — 40 mg/m² IV within a cyclophosphamide- and fluorouracil-based regimen', A18, 40, [R(Mi, '2.7')], allowed=['inj-25'], notes=[onc(Mi, '2.7')]),
                IT('it-0', 'لوسمی مننژیال (پیشگیری/درمان) — داخل نخاعی، زیر ۱ سال: ۶ mg', 'Meningeal leukaemia (prophylaxis/treatment) — intrathecal, under 1 year: 6 mg', {'maxAge': age(1, 'year')}, 6),
                IT('it-1', 'لوسمی مننژیال — داخل نخاعی، ۱ تا <۲ سال: ۸ mg', 'Meningeal leukaemia — intrathecal, 1 to <2 years: 8 mg', {'minAge': age(1, 'year'), 'maxAge': age(2, 'year')}, 8),
                IT('it-2', 'لوسمی مننژیال — داخل نخاعی، ۲ تا <۳ سال: ۱۰ mg', 'Meningeal leukaemia — intrathecal, 2 to <3 years: 10 mg', {'minAge': age(2, 'year'), 'maxAge': age(3, 'year')}, 10),
                IT('it-3', 'لوسمی مننژیال — داخل نخاعی، ۳ سال و بالاتر: ۱۲ mg (۹ سال به بالا ۱۲ تا ۱۵ mg)', 'Meningeal leukaemia — intrathecal, 3 years and older: 12 mg (≥9 years 12–15 mg)', {'minAge': age(3, 'year')}, 12),
                NC('all', 'acute-lymphoblastic-leukemia', 'لوسمی لنفوبلاستیک حاد — جزئی از رژیم چنددارویی، ۱۰ تا ۵۰۰۰ mg/m²', 'Acute lymphoblastic leukaemia — part of a multi-drug regimen, 10–5000 mg/m²', {},
                   'دوز و برنامه بر اساس پروتکل، گروه خطر و فاز درمان فردی می‌شود (عضلانی ۲۰ تا ۳۰ mg/m²/هفته). ۵۰۰ mg/m² و بیشتر: نجات لکوورین الزامی.', 'Dose and schedule are individualised by protocol, risk group and phase (IM 20–30 mg/m²/week). 500 mg/m² or more: leucovorin rescue mandatory.', [R(Mi, '2.3'), R(Mi, '2.2')], allowed=['inj-25'])],
      add_exs=[X('osteo', 'inj-25', 12000, 480, age=14, w=25, h=144), X('osteo', 'inj-25', 20000, 800, age=18), X('scchn', 'inj-25', 80, 3.2), X('breast', 'inj-25', 80, 3.2),
               ex('it-0', 'inj-25', {'perDose': 6, 'mlPerDose': 0.24}, ageYears=0.5, weightKg=7), ex('it-1', 'inj-25', {'perDose': 8, 'mlPerDose': 0.32}, ageYears=1.5, weightKg=10),
               ex('it-2', 'inj-25', {'perDose': 10, 'mlPerDose': 0.4}, ageYears=2.5, weightKg=13), ex('it-3', 'inj-25', {'perDose': 12, 'mlPerDose': 0.48}, ageYears=10, weightKg=30)],
      pin_old=True)

# --- sildenafil (Revatio) for PAH ---
Rv = fda('revatio', 'FDA Revatio', 'Revatio (sildenafil) tablets, oral suspension and injection — Prescribing Information', sid('revatio'))
patch('sildenafil',
      add_forms=[tab('tab-20', 20, '20 mg tablet (Revatio)', [R(Rv, '3')]), liquid('susp-10', 10, 1, '10 mg/mL oral suspension (Revatio, after reconstitution)', [R(Rv, '3')])],
      add_regs=[reg('pah', 'pulmonary-arterial-hypertension', T('فشار خون شریان ریوی (WHO گروه ۱) بزرگسال — ۲۰ mg سه بار در روز', 'PAH (WHO group 1), adults — 20 mg three times daily'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 3}, [R(Rv, '2.1')], allowed=['tab-20', 'susp-10'],
                    notes=[note('بر اساس علائم و تحمل تا حداکثر ۸۰ mg سه بار در روز قابل افزایش. تزریقی: ۱۰ mg وریدی بولوس سه بار در روز (معادل ۲۰ mg خوراکی).', 'May be titrated by symptoms and tolerability up to 80 mg three times daily. Injection: 10 mg IV bolus three times daily (equivalent to 20 mg oral).', [R(Rv, '2.1')])]),
                reg('pah-child', 'pulmonary-arterial-hypertension', T('PAH کودکان ۱ تا ۱۷ سال — ۲۰ kg و کمتر: ۱۰ mg؛ بالای ۲۰ kg: ۲۰ mg سه بار در روز', 'PAH, children 1–17 years — ≤20 kg: 10 mg; >20 kg: 20 mg three times daily'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year')}, 'weightBand',
                    {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 20, 'perDose': 10, 'dosesPerDay': 3}, {'minWeightKg': 20.01, 'maxWeightKg': 150, 'perDose': 20, 'dosesPerDay': 3}]}, [R(Rv, '2.2')], allowed=['tab-20', 'susp-10'],
                    notes=[note('بالای ۴۵ kg ممکن است تا ۴۰ mg سه بار در روز افزایش یابد. استفاده طولانی در کودکان با مرگ بیشتر در دوزهای بالاتر همراه بوده است.', 'Above 45 kg may be titrated to 40 mg three times daily. Long-term use in children was associated with higher mortality at higher doses.', [R(Rv, '2.2')])])],
      add_exs=[ex('pah', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('pah-child', 'susp-10', {'perDose': 10, 'mlPerDose': 1}, ageYears=4, weightKg=16),
               ex('pah-child', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=40)],
      pin_old=True)

# The Viagra-era drug-level "not for children" block would also block Revatio's labelled paediatric PAH dosing; ED regimens are adult-only already.
_p = find('sildenafil'); _d = json.load(open(_p)); _d['contraindications'] = [c for c in _d['contraindications'] if c['id'] != 'child']
json.dump(_d, open(_p, 'w'), ensure_ascii=False, indent=2); open(_p, 'a').write('\n')

# --- long-acting injectable antipsychotics ---
Iv = fda('invega-sustenna', 'FDA Invega Sustenna', 'Invega Sustenna (paliperidone palmitate) extended-release injectable suspension — Prescribing Information', sid('invega-sustenna'))
patch('paliperidone',
      add_forms=[form('lai', 'injection', 'im', 'Invega Sustenna 156 mg/mL prefilled syringes (39, 78, 117, 156, 234 mg)', 156, 'mg', [R(Iv, '3')], vol=1)],
      add_regs=[reg('lai-start', 'schizophrenia', T('اسکیزوفرنی و اسکیزوافکتیو (Invega Sustenna) — شروع: روز ۱ ۲۳۴ mg، روز ۸ ۱۵۶ mg در عضله دلتوئید', 'Schizophrenia and schizoaffective disorder (Invega Sustenna) — initiation: day 1 234 mg, day 8 156 mg into the deltoid'), A18, 'fixed', {'perDose': 234, 'dosesPerDay': 1}, [R(Iv, '2.2, Table 1')], dur=ONE, allowed=['lai'],
                    notes=[LAI(Iv, '2.1')]),
                reg('lai-maint', 'schizophrenia', T('نگهدارنده ماهانه Invega Sustenna — اسکیزوفرنی ۱۱۷ mg (۳۹ تا ۲۳۴ mg)؛ اسکیزوافکتیو ۷۸ تا ۲۳۴ mg', 'Invega Sustenna monthly maintenance — schizophrenia 117 mg (39–234 mg); schizoaffective 78–234 mg'), A18, 'fixed', {'perDose': 117, 'dosesPerDay': 1}, [R(Iv, '2.2, Table 1')], dur=ONE, allowed=['lai'],
                    notes=[note('نخستین دوز نگهدارنده ۵ هفته پس از تزریق اول، در دلتوئید یا گلوتئال.', 'First maintenance dose 5 weeks after the first injection, deltoid or gluteal.', [R(Iv, '2.2')])])],
      add_exs=[ex('lai-start', 'lai', {'perDose': 234, 'mlPerDose': 1.5}, ageYears=30, weightKg=70), ex('lai-maint', 'lai', {'perDose': 117, 'mlPerDose': 0.75}, ageYears=30, weightKg=70)],
      pin_old=True)

Hd = fda('haloperidol-decanoate', 'FDA Haloperidol dec', 'Haloperidol decanoate injection 50 and 100 mg/mL — Prescribing Information', sid('haldol-dec'))
patch('haloperidol',
      add_forms=[form('dec-50', 'injection', 'im', 'Haloperidol decanoate 50 mg/mL (deep IM)', 50, 'mg', [R(Hd, '3')], vol=1), form('dec-100', 'injection', 'im', 'Haloperidol decanoate 100 mg/mL (deep IM)', 100, 'mg', [R(Hd, '3')], vol=1)],
      add_regs=[NC('dec', 'schizophrenia', 'اسکیزوفرنی پایدار (دکانوات) بزرگسال — ۱۰ تا ۱۵ برابر دوز روزانه خوراکی، هر ۴ هفته عضلانی عمقی', 'Stabilised schizophrenia (decanoate), adults — 10–15 × the daily oral dose, deep IM every 4 weeks', A18,
                   'دوز از دوز خوراکی قبلی محاسبه می‌شود (نه وزن): مثلاً ۱۰ mg/روز خوراکی → ۱۰۰ تا ۱۵۰ mg. حداکثر دوز اول ۱۰۰ mg؛ باقی ۳ تا ۷ روز بعد. حداکثر ۳ mL در هر محل؛ هرگز وریدی.',
                   'Dose derives from the previous oral dose, not weight: e.g. 10 mg/day oral → 100–150 mg. Maximum first dose 100 mg; give the remainder 3–7 days later. Max 3 mL per site; never IV.', [R(Hd, '2.1, Table 1')], allowed=['dec-50', 'dec-100'])],
      pin_old=True)

Fd = fda('fluphenazine-decanoate', 'FDA Fluphenazine dec', 'Fluphenazine decanoate injection 25 mg/mL — Prescribing Information', sid('fluphenazine-dec'))
patch('fluphenazine',
      add_forms=[form('dec-25', 'injection', 'im', 'Fluphenazine decanoate 25 mg/mL (IM or SC)', 25, 'mg', [R(Fd, 'How Supplied')], vol=1)],
      add_regs=[reg('dec', 'schizophrenia', T('اسکیزوفرنی (دکانوات) — شروع ۱۲٫۵ تا ۲۵ mg عضلانی یا زیرجلدی', 'Schizophrenia (decanoate) — initial 12.5–25 mg IM or SC'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 12.5, 'perDoseMax': 25, 'dosesPerDay': 1}, [R(Fd, 'Dosage and Administration')], dur=ONE, allowed=['dec-25'],
                    notes=[note('دوز و فاصله بعدی بر اساس پاسخ؛ یک تزریق معمولاً تا ۴ هفته یا بیشتر اثر دارد. سرنگ و سوزن خشک (حداقل گیج ۲۱). زیر ۱۲ سال منع مصرف.', 'Subsequent dose and interval by response; one injection usually lasts up to 4 weeks or longer. Dry syringe and needle (at least 21 G). Not for children under 12.', [R(Fd, 'Dosage and Administration'), R(Fd, 'Contraindications')])])],
      add_exs=[ex('dec', 'dec-25', {'perDose': 12.5, 'mlPerDose': 0.5, 'upperPerDose': 25}, ageYears=40, weightKg=70)],
      pin_old=True)

Am = fda('abilify-maintena', 'FDA Abilify Maintena', 'Abilify Maintena (aripiprazole) extended-release injectable suspension — Prescribing Information', sid('abilify-maintena'))
patch('aripiprazole',
      add_forms=[form('am-400', 'powder-for-injection', 'im', 'Abilify Maintena 400 mg vial or prefilled syringe (also 300 mg)', 400, 'mg', [R(Am, '3')], per='vial')],
      add_regs=[reg('maintena', 'schizophrenia', T('اسکیزوفرنی و نگهدارنده دوقطبی I (Abilify Maintena) بزرگسال — ۴۰۰ mg عضلانی ماهانه', 'Schizophrenia and bipolar I maintenance (Abilify Maintena), adults — 400 mg IM monthly'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 1}, [R(Am, '2.2')], dur=ONE, allowed=['am-400'],
                    notes=[LAI(Am, '2.1'), note('حداقل ۲۶ روز فاصله. شروع: یا دو تزریق ۴۰۰ mg در یک روز + ۲۰ mg خوراکی، یا یک تزریق + ادامه خوراکی ۱۴ روز. عارضه: کاهش به ۳۰۰ mg. CYP2D6 ضعیف یا مهارکننده‌ها: جدول ۱ و ۲.', 'At least 26 days apart. Start: either two 400 mg injections on one day plus 20 mg oral, or one injection plus 14 days of oral. Adverse reactions: reduce to 300 mg. CYP2D6 poor metabolisers or inhibitors: Tables 1 and 2.', [R(Am, '2.2'), R(Am, '2.4')])])],
      add_exs=[ex('maintena', 'am-400', {'perDose': 400}, ageYears=30, weightKg=70)],
      pin_old=True)

# --- beta-lactam combinations ---
Av = fda('avycaz', 'FDA Avycaz', 'Avycaz (ceftazidime and avibactam) for injection — Prescribing Information', sid('avycaz'))
AVN = note('دوز به‌صورت مجموع سفتازیدیم + آویباکتام (۴:۱). انفوزیون ۲ ساعته هر ۸ ساعت. cIAI همراه مترونیدازول. مدت: cIAI ۵ تا ۱۴، cUTI و پنومونی ۷ تا ۱۴ روز.', 'Dose as total ceftazidime + avibactam (4:1). 2-hour infusion every 8 h. cIAI with metronidazole. Duration: cIAI 5–14, cUTI and pneumonia 7–14 days.', [R(Av, '2.1'), R(Av, '2.2')])
AVP = lambda id, fa, en, pop, kg: reg(id, 'intra-abdominal-infection', T(fa, en), pop, 'weightBased', {'perKgPerDose': kg, 'intervalHours': 8}, [R(Av, '2.2, Table 2')], dur={'min': 5, 'max': 14}, limits={'maxPerDose': 2500, 'refs': [R(Av, '2.2, Table 2')]}, notes=[AVN])
drug('ceftazidime-avibactam', 'anti-infectives', 'سفتازیدیم-آویباکتام', 'Ceftazidime-avibactam', T('سفالوسپورین + مهارکننده بتالاکتاماز', 'Cephalosporin + beta-lactamase inhibitor'), [{'name': 'Avycaz', 'market': 'US'}], ['avycaz', 'zavicefta', 'آویکاز', 'زاویسفتا', 'سفتازیدیم آویباکتام'],
     [form('vial-2-5', 'powder-for-injection', 'iv', '2.5 g vial (ceftazidime 2 g + avibactam 0.5 g)', 2500, 'mg', [R(Av, '3')], per='vial')],
     [reg('adult', 'intra-abdominal-infection', T('عفونت عارضه‌دار داخل شکم، ادراری (پیلونفریت) و پنومونی بیمارستانی/ونتیلاتور — بزرگسال ۲٫۵ g هر ۸ ساعت', 'Complicated intra-abdominal and urinary infections (pyelonephritis), HABP/VABP — adult 2.5 g every 8 h'), A18, 'fixed', {'perDose': 2500, 'dosesPerDay': 3}, [R(Av, '2.1, Table 1')], dur={'min': 5, 'max': 14}, notes=[AVN]),
      AVP('child', 'کودک ۶ ماه تا <۱۸ سال — ۶۲٫۵ mg/kg هر ۸ ساعت (حداکثر ۲٫۵ g)', 'Children 6 months to <18 years — 62.5 mg/kg every 8 h (max 2.5 g)', {'minAge': age(6, 'month'), 'maxAge': age(18, 'year')}, 62.5),
      AVP('infant', 'شیرخوار ۳ تا <۶ ماه — ۵۰ mg/kg هر ۸ ساعت', 'Infants 3 to <6 months — 50 mg/kg every 8 h', {'minAge': age(3, 'month'), 'maxAge': age(6, 'month')}, 50),
      AVP('young', 'شیرخوار بالای ۲۸ روز تا <۳ ماه — ۳۷٫۵ mg/kg هر ۸ ساعت', 'Infants >28 days to <3 months — 37.5 mg/kg every 8 h', {'minAge': age(29, 'day'), 'maxAge': age(3, 'month')}, 37.5)],
     [CI('hyper', 'حساسیت جدی به سفتازیدیم، آویباکتام، فرآورده‌های حاوی آویباکتام یا سایر سفالوسپورین‌ها.', 'Serious hypersensitivity to ceftazidime, avibactam, avibactam-containing products or other cephalosporins.', [R(Av, '4')])],
     warn=[W('کاهش پاسخ بالینی در cIAI با ClCr ۳۰ تا ۵۰؛ حساسیت (واکنش متقاطع با پنی‌سیلین)؛ اسهال C. difficile؛ سمیت عصبی (تشنج، انسفالوپاتی) در نارسایی کلیه بدون تنظیم دوز.', 'Decreased clinical response in cIAI with CrCl 30–50; hypersensitivity (penicillin cross-reactivity); C. difficile diarrhoea; neurotoxicity (seizures, encephalopathy) with unadjusted renal impairment.', [R(Av, '5')])],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۵۰ و کمتر: ۳۱ تا ۵۰ → ۱٫۲۵ g هر ۸ ساعت؛ ۱۶ تا ۳۰ → ۰٫۹۴ g هر ۱۲ ساعت؛ کمتر طبق جدول ۳. کودک زیر ۲ سال با نارسایی کلیه: داده کافی نیست.', 'CrCl ≤50: 31–50 → 1.25 g every 8 h; 16–30 → 0.94 g every 12 h; lower per Table 3. Children under 2 with renal impairment: insufficient data.'), 'refs': [R(Av, '2.3')]}],
     exs=[ex('adult', 'vial-2-5', {'perDose': 2500, 'dosesPerDay': 3}, ageYears=50, weightKg=70), ex('child', 'vial-2-5', {'perDose': 625}, ageYears=2, weightKg=10),
          ex('child', 'vial-2-5', {'perDose': 2500}, ageYears=14, weightKg=50), ex('infant', 'vial-2-5', {'perDose': 300}, ageYears=0.4, weightKg=6), ex('young', 'vial-2-5', {'perDose': 150}, ageYears=0.15, weightKg=4)])

Zb = fda('zerbaxa', 'FDA Zerbaxa', 'Zerbaxa (ceftolozane and tazobactam) for injection — Prescribing Information', sid('zerbaxa'))
ZBN = note('دوز به‌صورت مجموع سفتولوزان + تازوباکتام (۲:۱). انفوزیون ۱ ساعته هر ۸ ساعت. cIAI همراه مترونیدازول.', 'Dose as total ceftolozane + tazobactam (2:1). 1-hour infusion every 8 h. cIAI with metronidazole.', [R(Zb, '2.1')])
drug('ceftolozane-tazobactam', 'anti-infectives', 'سفتولوزان-تازوباکتام', 'Ceftolozane-tazobactam', T('سفالوسپورین + مهارکننده بتالاکتاماز', 'Cephalosporin + beta-lactamase inhibitor'), [{'name': 'Zerbaxa', 'market': 'US'}], ['zerbaxa', 'زرباکسا', 'سفتولوزان تازوباکتام'],
     [form('vial-1-5', 'powder-for-injection', 'iv', '1.5 g vial (ceftolozane 1 g + tazobactam 0.5 g)', 1500, 'mg', [R(Zb, '3')], per='vial')],
     [reg('ciai', 'intra-abdominal-infection', T('عفونت عارضه‌دار داخل شکم (۴ تا ۱۴ روز) و ادراری/پیلونفریت (۷ روز) — بزرگسال ۱٫۵ g هر ۸ ساعت', 'Complicated intra-abdominal (4–14 days) and urinary/pyelonephritis (7 days) — adult 1.5 g every 8 h'), A18, 'fixed', {'perDose': 1500, 'dosesPerDay': 3}, [R(Zb, '2.1, Table 1')], dur={'min': 4, 'max': 14}, notes=[ZBN]),
      reg('hap', 'hospital-acquired-pneumonia', T('پنومونی بیمارستانی و ونتیلاتور — بزرگسال ۳ g هر ۸ ساعت، ۸ تا ۱۴ روز', 'HABP/VABP — adult 3 g every 8 h for 8–14 days'), A18, 'fixed', {'perDose': 3000, 'dosesPerDay': 3}, [R(Zb, '2.1, Table 1')], dur={'min': 8, 'max': 14}, notes=[ZBN]),
      reg('child', 'intra-abdominal-infection', T('کودکان (از ۳۲ هفته سن بارداری) cIAI و cUTI — ۳۰ mg/kg هر ۸ ساعت (حداکثر ۱٫۵ g)', 'Children (from 32 weeks gestational age), cIAI and cUTI — 30 mg/kg every 8 h (max 1.5 g)'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 30, 'intervalHours': 8}, [R(Zb, '2.2, Table 2')], dur={'min': 5, 'max': 14},
          limits={'maxPerDose': 1500, 'refs': [R(Zb, '2.2, Table 2')]}, notes=[note('پنومونی بیمارستانی کودکان: دوز بالاتر و انفوزیون ۲ ساعته طبق جدول ۲.', 'Paediatric HABP/VABP: higher dose and 2-hour infusion per Table 2.', [R(Zb, '2.2, Table 2')])])],
     [CI('hyper', 'حساسیت جدی به سفتولوزان، تازوباکتام، پیپراسیلین-تازوباکتام یا سایر بتالاکتام‌ها.', 'Serious hypersensitivity to ceftolozane, tazobactam, piperacillin-tazobactam or other beta-lactams.', [R(Zb, '4')])],
     warn=[W('کاهش اثر در ClCr پایه ۳۰ تا ۵۰؛ حساسیت؛ اسهال C. difficile؛ مقاومت دارویی.', 'Decreased efficacy with baseline CrCl 30–50; hypersensitivity; C. difficile diarrhoea; drug-resistant bacteria.', [R(Zb, '5')])],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۵۰ و کمتر: cIAI/cUTI ۳۰ تا ۵۰ → ۷۵۰ mg، ۱۵ تا ۲۹ → ۳۷۵ mg هر ۸ ساعت؛ پنومونی ۳۰ تا ۵۰ → ۱٫۵ g، ۱۵ تا ۲۹ → ۷۵۰ mg؛ ESRD طبق جدول ۳.', 'CrCl ≤50: cIAI/cUTI 30–50 → 750 mg, 15–29 → 375 mg every 8 h; pneumonia 30–50 → 1.5 g, 15–29 → 750 mg; ESRD per Table 3.'), 'refs': [R(Zb, '2.3, Table 3')]}],
     exs=[ex('ciai', 'vial-1-5', {'perDose': 1500, 'dosesPerDay': 3}, ageYears=50, weightKg=70), ex('hap', 'vial-1-5', {'perDose': 3000, 'dosesPerDay': 3}, ageYears=60, weightKg=70),
          ex('child', 'vial-1-5', {'perDose': 600}, ageYears=5, weightKg=20), ex('child', 'vial-1-5', {'perDose': 1500}, ageYears=15, weightKg=60)])

Vb = fda('vabomere', 'FDA Vabomere', 'Vabomere (meropenem and vaborbactam) for injection — Prescribing Information', sid('vabomere'))
drug('meropenem-vaborbactam', 'anti-infectives', 'مروپنم-واباربکتام', 'Meropenem-vaborbactam', T('کارباپنم + مهارکننده بتالاکتاماز', 'Carbapenem + beta-lactamase inhibitor'), [{'name': 'Vabomere', 'market': 'US'}], ['vabomere', 'vaborem', 'وابومر', 'مروپنم واباربکتام'],
     [form('vial-2', 'powder-for-injection', 'iv', '2 g vial (meropenem 1 g + vaborbactam 1 g)', 2000, 'mg', [R(Vb, '3')], per='vial')],
     [reg('cuti', 'urinary-tract-infection', T('عفونت ادراری عارضه‌دار و پیلونفریت (۱۸ سال به بالا) — ۴ g هر ۸ ساعت، انفوزیون ۳ ساعته، تا ۱۴ روز', 'Complicated UTI including pyelonephritis (≥18 years) — 4 g every 8 h as a 3-hour infusion, up to 14 days'), A18, 'fixed', {'perDose': 4000, 'dosesPerDay': 3}, [R(Vb, '2.1')], dur={'min': 1, 'max': 14},
          notes=[note('دوز به‌صورت مجموع مروپنم + واباربکتام (۲ ویال). فقط با سالین ۰٫۹٪ سازگار است.', 'Dose as total meropenem + vaborbactam (2 vials). Compatible only with 0.9% sodium chloride.', [R(Vb, '2.1'), R(Vb, '2.4')])])],
     [CI('hyper', 'حساسیت به مروپنم، واباربکتام یا هم‌گروه‌ها؛ آنافیلاکسی با بتالاکتام‌ها.', 'Hypersensitivity to meropenem, vaborbactam or same-class drugs; anaphylaxis with beta-lactams.', [R(Vb, '4')])],
     warn=[W('حساسیت؛ تشنج؛ کاهش سطح والپروئیک‌اسید و تشنج ناگهانی؛ ترومبوسیتوپنی؛ اسهال C. difficile؛ رابدومیولیز.', 'Hypersensitivity; seizures; reduced valproic acid levels with breakthrough seizures; thrombocytopenia; C. difficile diarrhoea; rhabdomyolysis.', [R(Vb, '5')])],
     renal=[{'egfrBelow': 50, 'severity': 'warn', 'text': T('eGFR زیر ۵۰: ۳۰ تا ۴۹ → ۲ g هر ۸ ساعت؛ ۱۵ تا ۲۹ → ۲ g هر ۱۲ ساعت؛ زیر ۱۵ → ۱ g هر ۱۲ ساعت؛ همودیالیز: پس از دیالیز.', 'eGFR <50: 30–49 → 2 g every 8 h; 15–29 → 2 g every 12 h; <15 → 1 g every 12 h; haemodialysis: after dialysis.'), 'refs': [R(Vb, '2.2, Table 1')]}],
     exs=[ex('cuti', 'vial-2', {'perDose': 4000, 'dosesPerDay': 3}, ageYears=60, weightKg=70)])
print('s14b1 ok')
