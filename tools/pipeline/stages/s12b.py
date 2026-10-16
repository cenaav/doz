"""Stage 12b — hospital antibiotics, antifungals, antivirals (CMV, influenza, HBV/HCV) and HIV antiretrovirals."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
vial = lambda id, mg, label, src, sec='3': form(id, 'powder-for-injection', 'iv', label, mg, 'mg', [R(src, sec)], per='vial')
CDI = lambda src, sec='5': W('واکنش آلرژیک جدی؛ اسهال مرتبط با کلستریدیوئیدس دیفیسیل.', 'Serious hypersensitivity; Clostridioides difficile-associated diarrhoea.', [R(src, sec)])
ART = lambda src, sec: note('همیشه همراه سایر داروهای ضدرتروویروس (مگر فرآورده کامل).', 'Always with other antiretrovirals (unless a complete regimen).', [R(src, sec)])
HBV = lambda src: W('هشدار جعبه‌ای: تشدید شدید هپاتیت B پس از قطع در عفونت همزمان HBV — پایش کبد چند ماه.', 'Boxed warning: severe acute exacerbation of hepatitis B after discontinuation in HBV co-infection — monitor the liver for several months.', [R(src, 'Boxed Warning')])

add_disease('cmv-infection', 'عفونت سیتومگالوویروس (CMV) — رتینیت و پیشگیری در پیوند', 'Cytomegalovirus (CMV) — retinitis and transplant prophylaxis', ['CMV', 'سیتومگالوویروس', 'رتینیت CMV'], ['B25.9'], 'infectious')
add_disease('toxoplasmosis', 'توکسوپلاسموز', 'Toxoplasmosis', ['toxoplasmosis', 'توکسوپلاسما', 'توکسوپلاسموز'], ['B58.9'], 'infectious')
add_disease('leprosy', 'جذام', 'Leprosy (Hansen disease)', ['leprosy', 'hansen', 'جذام', 'خوره'], ['A30.9'], 'infectious')
add_disease('dermatitis-herpetiformis', 'درماتیت هرپتی‌فرم', 'Dermatitis herpetiformis', ['dermatitis herpetiformis', 'درماتیت هرپتیفورم', 'دوهرینگ'], ['L13.0'], 'dermatology')

# ===================== antibacterials =====================
Cf = fda('cefoxitin', 'FDA Cefoxitin', 'Cefoxitin for injection (WG Critical Care) — Prescribing Information', sid('cefoxitin')); d = R(Cf, 'Dosage and Administration — Table 1')
drug('cefoxitin', 'anti-infectives', 'سفوکسیتین', 'Cefoxitin', T('سفامایسین (سفالوسپورین نسل دوم)', 'Cephamycin (second-generation cephalosporin)'), [{'name': 'Mefoxin', 'market': 'US'}], ['mefoxin', 'سفوکسیتین'],
     [vial('vial-1g', 1000, '1 g vial', Cf, 'How Supplied'), vial('vial-2g', 2000, '2 g vial', Cf, 'How Supplied')],
     [reg('std', 'intra-abdominal-infection', T('عفونت بدون عارضه (پنومونی، UTI، پوست) — بزرگسال ۱ g هر ۶ تا ۸ ساعت', 'Uncomplicated infections (pneumonia, UTI, skin) — adult 1 g every 6–8 h'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 4}, [d],
          notes=[note('متوسط تا شدید: ۱ g هر ۴ ساعت یا ۲ g هر ۶ تا ۸ ساعت (۶ تا ۸ g/روز)؛ گانگرن گازی: تا ۱۲ g/روز. روی کلامیدیا اثر ندارد.', 'Moderate–severe: 1 g every 4 h or 2 g every 6–8 h (6–8 g/day); gas gangrene: up to 12 g/day. No activity against chlamydia.', [d])]),
      reg('child', 'intra-abdominal-infection', T('کودک ۳ ماه به بالا — ۳۰ تا ۴۰ mg/kg هر ۶ تا ۸ ساعت', 'Children ≥3 months — 30–40 mg/kg every 6–8 h'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 30, 'perKgPerDoseMax': 40, 'intervalHours': 6}, [R(Cf, 'Dosage and Administration')]),
      reg('cs', 'surgical-prophylaxis', T('پیشگیری سزارین — ۲ g وریدی هنگام بستن بند ناف', 'Caesarean prophylaxis — 2 g IV when the cord is clamped'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 1}, [R(Cf, 'Dosage and Administration')], dur=ONE,
          notes=[note('یا سه دوز ۲ g: هنگام بستن بند ناف و ۴ و ۸ ساعت بعد.', 'Or three 2 g doses: at cord clamping and 4 and 8 h later.', [R(Cf, 'Dosage and Administration')])])],
     [CI('hyper', 'حساسیت به سفوکسیتین و سفالوسپورین‌ها.', 'Hypersensitivity to cefoxitin and cephalosporins.', [R(Cf, 'Contraindications')])], warn=[CDI(Cf, 'Warnings')],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۳۰ تا ۵۰: ۱ تا ۲ g هر ۸ تا ۱۲ ساعت؛ کمتر طبق جدول ۲ برچسب.', 'CrCl 30–50: 1–2 g every 8–12 h; lower per label Table 2.'), 'refs': [R(Cf, 'Dosage and Administration — Table 2')]}],
     exs=[ex('std', 'vial-1g', {'perDose': 1000, 'dosesPerDay': 4}, ageYears=50, weightKg=70), ex('child', 'vial-1g', {'perDose': 600, 'upperPerDose': 800}, ageYears=6, weightKg=20), ex('cs', 'vial-2g', {'perDose': 2000}, ageYears=30, weightKg=75)])

Az = fda('azactam', 'FDA Azactam', 'Azactam (aztreonam) for injection — Prescribing Information', sid('aztreonam')); d = R(Az, 'Dosage and Administration')
drug('aztreonam', 'anti-infectives', 'آزترئونام', 'Aztreonam', T('مونوباکتام', 'Monobactam'), [{'name': 'Azactam', 'market': 'US'}], ['azactam', 'آزترئونام', 'آزترونام'],
     [vial('vial-1g', 1000, '1 g vial', Az, 'How Supplied'), vial('vial-2g', 2000, '2 g vial', Az, 'How Supplied')],
     [reg('uti', 'urinary-tract-infection', T('UTI — بزرگسال ۵۰۰ mg یا ۱ g هر ۸ تا ۱۲ ساعت', 'UTI — adult 500 mg or 1 g every 8–12 h'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 1000, 'dosesPerDay': 2}, [d]),
      reg('severe', 'sepsis', T('عفونت شدید یا تهدیدکننده حیات (پسودوموناس) — بزرگسال ۲ g هر ۶ تا ۸ ساعت', 'Severe or life-threatening infection (Pseudomonas) — adult 2 g every 6–8 h'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 3}, [d],
          limits={'maxPerDay': 8000, 'refs': [d]}, notes=[note('عفونت سیستمیک متوسط: ۱ یا ۲ g هر ۸ تا ۱۲ ساعت. حداکثر ۸ g/روز. حساسیت متقاطع با سایر بتالاکتام‌ها نادر است.', 'Moderately severe systemic: 1 or 2 g every 8–12 h. Max 8 g/day. Cross-reactivity with other beta-lactams is rare.', [d, R(Az, 'Warnings')])]),
      reg('child', 'sepsis', T('کودک ۹ ماه تا ۱۶ سال — ۳۰ mg/kg هر ۶ تا ۸ ساعت (حداکثر ۱۲۰ mg/kg/روز)', 'Children 9 months–16 y — 30 mg/kg every 6–8 h (max 120 mg/kg/day)'), {'minAge': age(9, 'month'), 'maxAge': age(17, 'year')}, 'weightBased', {'perKgPerDose': 30, 'intervalHours': 8}, [d],
          limits={'maxPerKgPerDay': 120, 'refs': [d]})],
     [CI('hyper', 'حساسیت به آزترئونام.', 'Hypersensitivity to aztreonam.', [R(Az, 'Contraindications')])], warn=[CDI(Az, 'Warnings')],
     exs=[ex('uti', 'vial-1g', {'perDose': 500, 'upperPerDose': 1000}, ageYears=50, weightKg=70), ex('severe', 'vial-2g', {'perDose': 2000, 'dosesPerDay': 3}, ageYears=50, weightKg=70), ex('child', 'vial-1g', {'perDose': 600}, ageYears=6, weightKg=20)])

Tg = fda('tygacil', 'FDA Tygacil', 'Tygacil (tigecycline) 50 mg — Prescribing Information', sid('tigecycline'))
drug('tigecycline', 'anti-infectives', 'تیژسیکلین', 'Tigecycline', T('گلیسیل‌سیکلین', 'Glycylcycline'), [{'name': 'Tygacil', 'market': 'US'}], ['tygacil', 'تایگاسیل', 'تیگسیکلین'],
     [vial('vial-50', 50, '50 mg vial', Tg)],
     [reg('adult', 'intra-abdominal-infection', T('عفونت عارضه‌دار پوست یا داخل شکم، پنومونی اکتسابی — ۱۰۰ mg سپس ۵۰ mg هر ۱۲ ساعت', 'cSSSI, cIAI, CAP — 100 mg, then 50 mg every 12 h'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 2}, [R(Tg, '2.1')], dur={'min': 5, 'max': 14},
          notes=[note('دوز اول ۱۰۰ mg. انفوزیون ۳۰ تا ۶۰ دقیقه. نارسایی شدید کبد: ۱۰۰ سپس ۲۵ mg هر ۱۲ ساعت. فیبرینوژن و انعقاد پایش شود.', 'First dose 100 mg. Infuse over 30–60 min. Severe hepatic impairment: 100 then 25 mg every 12 h. Monitor fibrinogen and coagulation.', [R(Tg, '2.1'), R(Tg, '2.2'), R(Tg, '2')])])],
     [CI('hyper', 'حساسیت به تیژسیکلین.', 'Hypersensitivity to tigecycline.', [R(Tg, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ از هر علت — فقط وقتی جایگزین مناسب نیست. کودکان: فقط اگر جایگزینی نیست.', 'Boxed warning: increased all-cause mortality — reserve for when alternatives are unsuitable. Children: only if no alternative.', [R(Tg, 'Boxed Warning'), R(Tg, '2.3')])],
     exs=[ex('adult', 'vial-50', {'perDose': 50, 'dosesPerDay': 2}, ageYears=50, weightKg=70)])

Dt = fda('cubicin-rf', 'FDA Cubicin RF', 'Cubicin RF (daptomycin) 500 mg — Prescribing Information', sid('daptomycin'))
DAP_AGE = lambda lo, hi: {'minAge': age(lo, 'year'), 'maxAge': age(hi, 'year')}
drug('daptomycin', 'anti-infectives', 'داپتومایسین', 'Daptomycin', T('لیپوپپتید حلقوی', 'Cyclic lipopeptide'), [{'name': 'Cubicin', 'market': 'US'}], ['cubicin', 'کوبیسین', 'داپتومایسین'],
     [vial('vial-500', 500, '500 mg vial', Dt)],
     [reg('sssi', 'skin-soft-tissue-infection', T('عفونت عارضه‌دار پوست — بزرگسال ۴ mg/kg هر ۲۴ ساعت، ۷ تا ۱۴ روز', 'cSSSI — adult 4 mg/kg every 24 h, 7–14 days'), A18, 'weightBased', {'perKgPerDose': 4, 'intervalHours': 24}, [R(Dt, '2.2')], dur={'min': 7, 'max': 14}),
      reg('bac', 'sepsis', T('باکتریمی استاف اورئوس (و اندوکاردیت راست) — بزرگسال ۶ mg/kg هر ۲۴ ساعت، ۲ تا ۶ هفته', 'S. aureus bacteraemia (incl. right-sided endocarditis) — adult 6 mg/kg every 24 h, 2–6 weeks'), A18, 'weightBased', {'perKgPerDose': 6, 'intervalHours': 24}, [R(Dt, '2.4')]),
      reg('sssi-12', 'skin-soft-tissue-infection', T('پوست — کودک ۱۲ تا ۱۷ سال: ۵ mg/kg هر ۲۴ ساعت', 'cSSSI — children 12–17 y: 5 mg/kg every 24 h'), DAP_AGE(12, 18), 'weightBased', {'perKgPerDose': 5, 'intervalHours': 24}, [R(Dt, '2.3, Table 1')], dur={'min': 1, 'max': 14}),
      reg('sssi-7', 'skin-soft-tissue-infection', T('پوست — کودک ۷ تا ۱۱ سال: ۷ mg/kg هر ۲۴ ساعت', 'cSSSI — children 7–11 y: 7 mg/kg every 24 h'), DAP_AGE(7, 12), 'weightBased', {'perKgPerDose': 7, 'intervalHours': 24}, [R(Dt, '2.3, Table 1')], dur={'min': 1, 'max': 14}),
      reg('sssi-2', 'skin-soft-tissue-infection', T('پوست — کودک ۲ تا ۶ سال: ۹ mg/kg هر ۲۴ ساعت', 'cSSSI — children 2–6 y: 9 mg/kg every 24 h'), DAP_AGE(2, 7), 'weightBased', {'perKgPerDose': 9, 'intervalHours': 24}, [R(Dt, '2.3, Table 1')], dur={'min': 1, 'max': 14}),
      reg('sssi-1', 'skin-soft-tissue-infection', T('پوست — کودک ۱ تا <۲ سال: ۱۰ mg/kg هر ۲۴ ساعت', 'cSSSI — children 1–<2 y: 10 mg/kg every 24 h'), DAP_AGE(1, 2), 'weightBased', {'perKgPerDose': 10, 'intervalHours': 24}, [R(Dt, '2.3, Table 1')], dur={'min': 1, 'max': 14}),
      reg('bac-12', 'sepsis', T('باکتریمی — کودک ۱۲ تا ۱۷ سال: ۷ mg/kg هر ۲۴ ساعت', 'Bacteraemia — children 12–17 y: 7 mg/kg every 24 h'), DAP_AGE(12, 18), 'weightBased', {'perKgPerDose': 7, 'intervalHours': 24}, [R(Dt, '2.5, Table 2')]),
      reg('bac-7', 'sepsis', T('باکتریمی — کودک ۷ تا ۱۱ سال: ۹ mg/kg هر ۲۴ ساعت', 'Bacteraemia — children 7–11 y: 9 mg/kg every 24 h'), DAP_AGE(7, 12), 'weightBased', {'perKgPerDose': 9, 'intervalHours': 24}, [R(Dt, '2.5, Table 2')]),
      reg('bac-1', 'sepsis', T('باکتریمی — کودک ۱ تا ۶ سال: ۱۲ mg/kg هر ۲۴ ساعت', 'Bacteraemia — children 1–6 y: 12 mg/kg every 24 h'), DAP_AGE(1, 7), 'weightBased', {'perKgPerDose': 12, 'intervalHours': 24}, [R(Dt, '2.5, Table 2')])],
     [CI('hyper', 'حساسیت به داپتومایسین.', 'Hypersensitivity to daptomycin.', [R(Dt, '4')])],
     warn=[W('میوپاتی و رابدومیولیز (CPK هفتگی)؛ پنومونی ائوزینوفیلیک؛ برای پنومونی مؤثر نیست؛ زیر ۱ سال نه (اثر عضلانی).', 'Myopathy and rhabdomyolysis (weekly CPK); eosinophilic pneumonia; not effective for pneumonia; not under 1 y (muscular effects).', [R(Dt, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('بزرگسال ClCr زیر ۳۰ و دیالیز: همان mg/kg هر ۴۸ ساعت (پس از دیالیز). کودکان تنظیم کلیوی تعیین نشده.', 'Adults CrCl <30 incl. dialysis: same mg/kg every 48 h (after dialysis). No paediatric renal adjustment established.'), 'refs': [R(Dt, '2.6')]}],
     exs=[ex('sssi', 'vial-500', {'perDose': 280}, ageYears=50, weightKg=70), ex('bac', 'vial-500', {'perDose': 420}, ageYears=50, weightKg=70), ex('sssi-12', 'vial-500', {'perDose': 250}, ageYears=14, weightKg=50),
          ex('sssi-7', 'vial-500', {'perDose': 175}, ageYears=8, weightKg=25), ex('sssi-2', 'vial-500', {'perDose': 135}, ageYears=4, weightKg=15), ex('sssi-1', 'vial-500', {'perDose': 100}, ageMonths=18, weightKg=10),
          ex('bac-12', 'vial-500', {'perDose': 350}, ageYears=14, weightKg=50), ex('bac-7', 'vial-500', {'perDose': 225}, ageYears=8, weightKg=25), ex('bac-1', 'vial-500', {'perDose': 180}, ageYears=4, weightKg=15)])

Tz = fda('sivextro', 'FDA Sivextro', 'Sivextro (tedizolid) tablets and injection — Prescribing Information', sid('tedizolid'))
drug('tedizolid', 'anti-infectives', 'تدیزولید', 'Tedizolid', T('اکسازولیدینون', 'Oxazolidinone'), [{'name': 'Sivextro', 'market': 'US'}], ['sivextro', 'سیوکسترو', 'تدیزولید'],
     [tab('tab-200', 200, '200 mg tablet', [R(Tz, '3')]), vial('vial-200', 200, '200 mg vial', Tz)],
     [reg('absssi', 'skin-soft-tissue-infection', T('عفونت حاد باکتریایی پوست — ۲۰۰ mg یک بار در روز، ۶ روز (خوراکی یا وریدی)', 'Acute bacterial skin infection — 200 mg once daily for 6 days (oral or IV)'), {'minAge': age(12, 'year'), 'minWeightKg': 35}, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Tz, '2.2, Table 1')], dur={'min': 6, 'max': 6},
          notes=[note('قرص در کودک زیر ۳۵ kg داده نشود. تغییر وریدی به خوراکی بدون تنظیم دوز.', 'Do not give tablets to children under 35 kg. IV-to-oral switch needs no adjustment.', [R(Tz, '2'), R(Tz, '2.2')])])],
     warn=[W('در نوتروپنی اثر بررسی نشده؛ اسهال C. difficile.', 'Not evaluated in neutropenic patients; C. difficile diarrhoea.', [R(Tz, '5')])],
     exs=[ex('absssi', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Fx = fda('dificid', 'FDA Dificid', 'Dificid (fidaxomicin) tablets and oral suspension — Prescribing Information', sid('fidaxomicin'))
drug('fidaxomicin', 'alimentary-metabolism', 'فیداکسومایسین', 'Fidaxomicin', T('آنتی‌بیوتیک ماکروسیکلیک', 'Macrocyclic antibiotic'), [{'name': 'Dificid', 'market': 'US'}], ['dificid', 'دیفیسید', 'فیداکسومایسین'],
     [tab('tab-200', 200, '200 mg tablet', [R(Fx, '3')]), liquid('susp-40', 40, 1, '40 mg/mL oral suspension', [R(Fx, '3')])],
     [reg('adult', 'c-diff', T('اسهال کلستریدیوئیدس دیفیسیل — بزرگسال ۲۰۰ mg دو بار در روز، ۱۰ روز', 'C. difficile diarrhoea — adult 200 mg twice daily for 10 days'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 2}, [R(Fx, '2.2')], dur={'min': 10, 'max': 10}, allowed=['tab-200']),
      reg('child', 'c-diff', T('کودک ۶ ماه تا <۱۸ سال (سوسپانسیون) — ۸۰ / ۱۲۰ / ۱۶۰ / ۲۰۰ mg دو بار در روز بر اساس وزن، ۱۰ روز', 'Children 6 months–<18 y (suspension) — 80 / 120 / 160 / 200 mg twice daily by weight, 10 days'), {'minAge': age(6, 'month'), 'maxAge': age(18, 'year'), 'minWeightKg': 4}, 'weightBand',
          {'weightBands': [{'minWeightKg': 4, 'maxWeightKg': 6.99, 'perDose': 80, 'dosesPerDay': 2}, {'minWeightKg': 7, 'maxWeightKg': 8.99, 'perDose': 120, 'dosesPerDay': 2}, {'minWeightKg': 9, 'maxWeightKg': 12.49, 'perDose': 160, 'dosesPerDay': 2}, {'minWeightKg': 12.5, 'maxWeightKg': None, 'perDose': 200, 'dosesPerDay': 2}]},
          [R(Fx, '2.3, Table 1')], dur={'min': 10, 'max': 10}, allowed=['susp-40'])],
     [CI('hyper', 'حساسیت به فیداکسومایسین.', 'Hypersensitivity to fidaxomicin.', [R(Fx, '4')])],
     exs=[ex('adult', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70), ex('child', 'susp-40', {'perDose': 160, 'mlPerDose': 4}, ageYears=1, weightKg=10)])

Ds = fda('dapsone', 'FDA Dapsone', 'Dapsone tablets 25/100 mg (Macleods) — Prescribing Information', sid('dapsone')); d = R(Ds, 'Dosage and Administration')
drug('dapsone', 'anti-infectives', 'داپسون', 'Dapsone', T('سولفون (ضدجذام)', 'Sulfone (antileprotic)'), [{'name': 'Dapsone', 'market': 'US'}], ['dapsone', 'داپسون', 'DDS'],
     [tab('tab-25', 25, '25 mg tablet', [R(Ds, 'How Supplied')]), tab('tab-100', 100, '100 mg tablet', [R(Ds, 'How Supplied')])],
     [reg('lep', 'leprosy', T('جذام — ۱۰۰ mg روزانه بدون وقفه همراه سایر داروهای ضدجذام', 'Leprosy — 100 mg daily without interruption, with other antileprosy drugs'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [d]),
      reg('dh', 'dermatitis-herpetiformis', T('درماتیت هرپتی‌فرم — شروع ۵۰ mg روزانه (۵۰ تا ۳۰۰ mg)', 'Dermatitis herpetiformis — start 50 mg daily (50–300 mg)'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [d],
          notes=[note('تیتراسیون تا کنترل؛ در اسرع وقت به کمترین دوز نگهدارنده کاهش. کودک دوز کمتر.', 'Titrate to control; reduce to the minimum maintenance dose as soon as possible. Children: smaller doses.', [d])])],
     [CI('hyper', 'حساسیت به داپسون یا مشتقات آن.', 'Hypersensitivity to dapsone or its derivatives.', [R(Ds, 'Contraindications')])],
     warn=[W('آگرانولوسیتوز، آنمی آپلاستیک و دیسکرازی خونی کشنده — CBC مکرر؛ همولیز (به‌ویژه کمبود G6PD)؛ مت‌هموگلوبینمی.', 'Fatal agranulocytosis, aplastic anaemia and blood dyscrasias — frequent CBC; haemolysis (especially G6PD deficiency); methaemoglobinaemia.', [R(Ds, 'Warnings')])],
     exs=[ex('lep', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=60), ex('dh', 'tab-25', {'perDose': 50, 'tabletsPerDoseRounded': 2}, ageYears=40, weightKg=60)])

Sr = fda('sirturo', 'FDA Sirturo', 'Sirturo (bedaquiline) 20/100 mg tablets — Prescribing Information', sid('bedaquiline'))
drug('bedaquiline', 'anti-infectives', 'بداکیلین', 'Bedaquiline', T('دی‌آریل‌کینولین (ضدسل)', 'Diarylquinoline (antimycobacterial)'), [{'name': 'Sirturo', 'market': 'US'}], ['sirturo', 'سیرتورو', 'بداکیلین'],
     [tab('tab-100', 100, '100 mg tablet', [R(Sr, '3')]), tab('tab-20', 20, '20 mg tablet (functionally scored)', [R(Sr, '3')], scored=True)],
     [NC('mdr', 'tuberculosis', 'سل مقاوم به چند دارو (ریوی) — بزرگسال: ۴۰۰ mg روزانه ۲ هفته، سپس ۲۰۰ mg سه بار در هفته تا هفته ۲۴', 'Pulmonary MDR-TB — adult: 400 mg daily for 2 weeks, then 200 mg three times weekly to week 24', {'minAge': age(2, 'year'), 'minWeightKg': 8},
         'همراه دست‌کم ۳ داروی مؤثر دیگر، با غذا، تحت نظارت مستقیم. سه بار در هفته با دست‌کم ۴۸ ساعت فاصله. کودک ۲ سال و ۸ kg به بالا طبق جدول ۲ برچسب بر اساس وزن. ECG پایه و دوره‌ای.', 'With at least 3 other active drugs, with food, under directly observed therapy. Three-times-weekly doses at least 48 h apart. Children ≥2 y and ≥8 kg per label Table 2 by weight. Baseline and periodic ECG.', [R(Sr, '2.3, Table 1'), R(Sr, '2.4, Table 2'), R(Sr, '2.6')])],
     warn=[W('هشدار جعبه‌ای: طولانی شدن QTc — ECG؛ قطع در آریتمی بطنی مهم یا QTc بالای ۵۰۰ ms.', 'Boxed warning: QTc prolongation — monitor ECGs; stop for significant ventricular arrhythmia or QTc >500 ms.', [R(Sr, 'Boxed Warning')])])

# ===================== antifungals =====================
Px = fda('noxafil', 'FDA Noxafil', 'Noxafil (posaconazole) injection, delayed-release tablets, oral suspension — Prescribing Information', sid('posaconazole'))
drug('posaconazole', 'anti-infectives', 'پوساکونازول', 'Posaconazole', T('ضدقارچ آزولی', 'Azole antifungal'), [{'name': 'Noxafil', 'market': 'US'}], ['noxafil', 'نوکسافیل', 'پوساکونازول'],
     [tab('dr-100', 100, '100 mg delayed-release tablet (NOT interchangeable with suspension)', [R(Px, '3')]), liquid('susp-40', 40, 1, '40 mg/mL oral suspension (NOT interchangeable with tablets)', [R(Px, '3')])],
     [reg('proph', 'invasive-fungal', T('پیشگیری از آسپرژیلوس و کاندیدا (سرکوب ایمنی شدید) — قرص: روز اول ۳۰۰ mg دو بار، سپس ۳۰۰ mg یک بار در روز', 'Aspergillus/Candida prophylaxis (severe immunosuppression) — tablets: 300 mg twice on day 1, then 300 mg once daily'), {'minAge': age(13, 'year'), 'minWeightKg': 40.01}, 'fixed',
          {'perDose': 300, 'dosesPerDay': 1}, [R(Px, '2.2, Table 1')], allowed=['dr-100'], notes=[note('روز اول بارگذاری ۳۰۰ mg دو بار. قرص آهسته‌رهش و سوسپانسیون جایگزین هم نیستند.', 'Day 1 loading 300 mg twice. Delayed-release tablets and suspension are not interchangeable.', [R(Px, '2.2'), R(Px, '2.9')])]),
      reg('asperg', 'invasive-fungal', T('درمان آسپرژیلوز تهاجمی — قرص: روز اول ۳۰۰ mg دو بار، سپس ۳۰۰ mg یک بار (۶ تا ۱۲ هفته)', 'Invasive aspergillosis — tablets: 300 mg twice on day 1, then 300 mg once daily (6–12 weeks)'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Px, '2.2, Table 1')], allowed=['dr-100']),
      reg('proph-susp', 'invasive-fungal', T('پیشگیری — سوسپانسیون: ۲۰۰ mg (۵ mL) سه بار در روز', 'Prophylaxis — suspension: 200 mg (5 mL) three times daily'), {'minAge': age(13, 'year')}, 'fixed', {'perDose': 200, 'dosesPerDay': 3}, [R(Px, '2.2, Table 1')], allowed=['susp-40'])],
     [CI('ci', 'حساسیت به پوساکونازول یا سایر آزول‌ها؛ سیرولیموس؛ پیموزاید و کینیدین (QT)؛ استاتین‌های وابسته به CYP3A4 (سیمواستاتین، لواستاتین، آتورواستاتین)؛ آلکالوئیدهای ارگوت؛ ونتوکلاکس در شروع درمان CLL.',
         'Hypersensitivity to posaconazole or other azoles; sirolimus; pimozide and quinidine (QT); CYP3A4-metabolised statins (simvastatin, lovastatin, atorvastatin); ergot alkaloids; venetoclax at initiation for CLL.', [R(Px, '4')])],
     warn=[W('طولانی شدن QT؛ سمیت کبد؛ تداخل زیاد با داروهای CYP3A4.', 'QT prolongation; hepatotoxicity; many CYP3A4 drug interactions.', [R(Px, '5')])],
     exs=[ex('proph', 'dr-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=50, weightKg=70), ex('asperg', 'dr-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=50, weightKg=70), ex('proph-susp', 'susp-40', {'perDose': 200, 'mlPerDose': 5}, ageYears=50, weightKg=70)])

Mc = fda('micafungin', 'FDA Micafungin premix', 'Micafungin in sodium chloride injection 1 mg/mL (Baxter) — Prescribing Information', sid('micafungin'))
drug('micafungin', 'anti-infectives', 'میکافانژین', 'Micafungin', T('اکینوکاندین', 'Echinocandin'), [{'name': 'Mycamine', 'market': 'US'}], ['mycamine', 'مایکامین', 'میکافانژین'],
     [form('bag-1', 'injection', 'iv', '1 mg/mL premixed (50/100/150 mL)', 1, 'mg', [R(Mc, '3')], vol=1)],
     [reg('cand', 'invasive-fungal', T('کاندیدمی و کاندیدیاز منتشر — بزرگسال ۱۰۰ mg روزانه', 'Candidaemia and disseminated candidiasis — adult 100 mg daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Mc, '2.2, Table 1')]),
      reg('eso', 'esophageal-candidiasis', T('کاندیدیاز مری — بزرگسال ۱۵۰ mg روزانه', 'Oesophageal candidiasis — adult 150 mg daily'), A18, 'fixed', {'perDose': 150, 'dosesPerDay': 1}, [R(Mc, '2.2, Table 1')]),
      reg('proph', 'invasive-fungal', T('پیشگیری کاندیدا در پیوند سلول بنیادی — بزرگسال ۵۰ mg روزانه', 'Candida prophylaxis in HSCT — adult 50 mg daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Mc, '2.2, Table 1')]),
      reg('cand-child', 'invasive-fungal', T('کاندیدمی — کودک ۴ ماه به بالا: ۲ mg/kg روزانه (حداکثر ۱۰۰ mg)', 'Candidaemia — children ≥4 months: 2 mg/kg daily (max 100 mg)'), {'minAge': age(4, 'month'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 2, 'intervalHours': 24}, [R(Mc, '2.3, Table 2')],
          limits={'maxPerDose': 100, 'refs': [R(Mc, '2.3, Table 2')]}, notes=[note('این فرآورده آماده فقط دوز ۵۰، ۱۰۰ یا ۱۵۰ mg می‌دهد؛ دوزهای دیگر فرآورده دیگر میکافانژین لازم دارند.', 'This premix only supplies 50, 100 or 150 mg; other doses need another micafungin formulation.', [R(Mc, '2')])])],
     [CI('hyper', 'حساسیت به میکافانژین یا سایر اکینوکاندین‌ها.', 'Hypersensitivity to micafungin or other echinocandins.', [R(Mc, '4')])],
     exs=[ex('cand', 'bag-1', {'perDose': 100, 'mlPerDose': 100}, ageYears=50, weightKg=70), ex('eso', 'bag-1', {'perDose': 150, 'mlPerDose': 150}, ageYears=50, weightKg=70), ex('proph', 'bag-1', {'perDose': 50, 'mlPerDose': 50}, ageYears=50, weightKg=70),
          ex('cand-child', 'bag-1', {'perDose': 50, 'mlPerDose': 50}, ageYears=7, weightKg=25)])

Er = fda('eraxis', 'FDA Eraxis', 'Eraxis (anidulafungin) 50/100 mg — Prescribing Information', sid('anidulafungin'))
drug('anidulafungin', 'anti-infectives', 'آنیدولافانژین', 'Anidulafungin', T('اکینوکاندین', 'Echinocandin'), [{'name': 'Eraxis', 'market': 'US'}], ['eraxis', 'اراکسیس', 'آنیدولافانژین'],
     [vial('vial-100', 100, '100 mg vial', Er), vial('vial-50', 50, '50 mg vial', Er)],
     [reg('load', 'invasive-fungal', T('کاندیدمی — بزرگسال: روز اول بارگذاری ۲۰۰ mg', 'Candidaemia — adult: day 1 loading 200 mg'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Er, '2')], dur=ONE, allowed=['vial-100']),
      reg('maint', 'invasive-fungal', T('کاندیدمی — بزرگسال: ۱۰۰ mg روزانه از روز ۲، دست‌کم ۱۴ روز پس از آخرین کشت مثبت', 'Candidaemia — adult: 100 mg daily from day 2, ≥14 days after the last positive culture'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Er, '2')], allowed=['vial-100']),
      reg('child', 'invasive-fungal', T('کاندیدمی — کودک ۱ ماه به بالا: روز اول ۳ mg/kg (حداکثر ۲۰۰)، سپس ۱٫۵ mg/kg روزانه (حداکثر ۱۰۰)', 'Candidaemia — children ≥1 month: day 1 3 mg/kg (max 200), then 1.5 mg/kg daily (max 100)'), {'minAge': age(1, 'month'), 'maxAge': age(18, 'year')}, 'weightBased',
          {'perKgPerDose': 1.5, 'intervalHours': 24}, [R(Er, '2')], limits={'maxPerDose': 100, 'refs': [R(Er, '2')]}, allowed=['vial-50'],
          notes=[note('عدد ماشین‌حساب دوز نگهدارنده است؛ روز اول ۳ mg/kg. سرعت انفوزیون حداکثر ۱٫۱ mg/دقیقه.', 'The calculator gives the maintenance dose; day 1 is 3 mg/kg. Infusion rate max 1.1 mg/min.', [R(Er, '2')])]),
      reg('eso', 'esophageal-candidiasis', T('کاندیدیاز مری — بزرگسال: روز اول ۱۰۰ mg سپس ۵۰ mg روزانه', 'Oesophageal candidiasis — adult: 100 mg day 1, then 50 mg daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Er, '2')], allowed=['vial-50'],
          notes=[note('دست‌کم ۱۴ روز و ۷ روز پس از رفع علائم.', 'At least 14 days and 7 days after symptoms resolve.', [R(Er, '2')])])],
     [CI('ci', 'حساسیت به آنیدولافانژین یا اکینوکاندین‌ها؛ عدم تحمل ارثی فروکتوز (معلوم یا مشکوک).', 'Hypersensitivity to anidulafungin or other echinocandins; known or suspected hereditary fructose intolerance.', [R(Er, '4')])],
     exs=[ex('load', 'vial-100', {'perDose': 200}, ageYears=50, weightKg=70), ex('maint', 'vial-100', {'perDose': 100}, ageYears=50, weightKg=70), ex('child', 'vial-50', {'perDose': 30}, ageYears=6, weightKg=20), ex('eso', 'vial-50', {'perDose': 50}, ageYears=50, weightKg=70)])

Fc = fda('flucytosine', 'FDA Flucytosine', 'Flucytosine capsules 250/500 mg — Prescribing Information', sid('flucytosine')); d = R(Fc, 'Dosage and Administration')
drug('flucytosine', 'anti-infectives', 'فلوسیتوزین', 'Flucytosine', T('ضدقارچ (آنتی‌متابولیت)', 'Antifungal (antimetabolite)'), [{'name': 'Ancobon', 'market': 'US'}], ['ancobon', 'فلوسیتوزین', '5-FC'],
     [tab('cap-250', 250, '250 mg capsule', [R(Fc, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-500', 500, '500 mg capsule', [R(Fc, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('std', 'invasive-fungal', T('عفونت جدی کاندیدا یا کریپتوکوک (همراه آمفوتریسین) — ۵۰ تا ۱۵۰ mg/kg/روز هر ۶ ساعت', 'Serious Candida or Cryptococcus infection (with amphotericin B) — 50–150 mg/kg/day every 6 h'), {}, 'weightBased', {'perKgPerDay': 50, 'perKgPerDayMax': 150, 'dividedDoses': 4}, [d],
          notes=[note('کپسول‌ها چندتا چندتا طی ۱۵ دقیقه (کاهش تهوع). نارسایی کلیه: دوز پایین‌تر و پایش سطح خونی. به‌تنهایی مقاومت ایجاد می‌شود.', 'Give capsules a few at a time over 15 min (less nausea). Renal impairment: lower dose and monitor levels. Resistance develops when used alone.', [d, R(Fc, 'Warnings')])])],
     [CI('hyper', 'حساسیت به فلوسیتوزین.', 'Hypersensitivity to flucytosine.', [R(Fc, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: در نارسایی کلیه با احتیاط شدید؛ سرکوب مغز استخوان؛ پایش خون، کلیه و کبد.', 'Boxed warning: extreme caution in renal impairment; bone-marrow suppression; monitor haematology, renal and hepatic function.', [R(Fc, 'Warnings')])],
     exs=[ex('std', 'cap-250', {'perDose': 750, 'tabletsPerDoseRounded': 3, 'upperPerDose': 2250}, ageYears=40, weightKg=60)])

# ===================== antivirals =====================
Rl = fda('relenza', 'FDA Relenza', 'Relenza (zanamivir) inhalation powder — Prescribing Information', sid('zanamivir'))
drug('zanamivir', 'anti-infectives', 'زانامیویر', 'Zanamivir', T('مهارکننده نورآمینیداز استنشاقی', 'Inhaled neuraminidase inhibitor'), [{'name': 'Relenza', 'market': 'US'}], ['relenza', 'رلنزا', 'زانامیویر'],
     [form('diskhaler', 'inhaler', 'inhaled', '5 mg per blister (Diskhaler); dose = 2 inhalations', 5, 'mg', [R(Rl, '3')], per='actuation')],
     [reg('tx', 'influenza', T('درمان آنفلوانزا (۷ سال به بالا) — ۱۰ mg (۲ استنشاق) دو بار در روز، ۵ روز', 'Influenza treatment (≥7 y) — 10 mg (2 inhalations) twice daily for 5 days'), {'minAge': age(7, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 2}, [R(Rl, '2.2')], dur={'min': 5, 'max': 5}),
      reg('proph', 'influenza-prophylaxis', T('پیشگیری خانگی (۵ سال به بالا) — ۱۰ mg یک بار در روز، ۱۰ روز', 'Household prophylaxis (≥5 y) — 10 mg once daily for 10 days'), {'minAge': age(5, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Rl, '2.3')], dur={'min': 10, 'max': 10},
          notes=[note('همه‌گیری جامعه (بزرگسال و نوجوان): ۱۰ mg روزانه ۲۸ روز.', 'Community outbreaks (adults and adolescents): 10 mg daily for 28 days.', [R(Rl, '2.3')])])],
     [CI('ci', 'سابقه آلرژی به اجزای فرآورده از جمله پروتئین شیر.', 'History of allergy to any ingredient, including milk proteins.', [R(Rl, '4')])],
     warn=[W('برونکواسپاسم (گاه کشنده) — در آسم یا COPD توصیه نمی‌شود.', 'Bronchospasm (sometimes fatal) — not recommended in asthma or COPD.', [R(Rl, '5')])],
     exs=[ex('tx', 'diskhaler', {'perDose': 10, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70), ex('proph', 'diskhaler', {'perDose': 10, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70)])

Gc = fda('ganciclovir', 'FDA Ganciclovir', 'Ganciclovir for injection 500 mg (Par) — Prescribing Information', sid('ganciclovir'))
HEM = lambda src: W('هشدار جعبه‌ای: سمیت خونی (نوتروپنی، کم‌خونی، ترومبوسیتوپنی)، کاهش باروری، سمیت جنینی و سرطان‌زایی.', 'Boxed warning: haematological toxicity, impaired fertility, fetal toxicity, mutagenesis and carcinogenesis.', [R(src, 'Boxed Warning')])
drug('ganciclovir', 'anti-infectives', 'گان‌سیکلوویر', 'Ganciclovir', T('ضدویروس CMV', 'Anti-CMV antiviral'), [{'name': 'Cytovene', 'market': 'US'}], ['cytovene', 'سایتوون', 'گانسیکلوویر'],
     [vial('vial-500', 500, '500 mg vial', Gc)],
     [reg('ind', 'cmv-infection', T('رتینیت CMV یا پیشگیری در پیوند — القا ۵ mg/kg هر ۱۲ ساعت', 'CMV retinitis or transplant prevention — induction 5 mg/kg every 12 h'), A18, 'weightBased', {'perKgPerDose': 5, 'intervalHours': 12}, [R(Gc, '2.3'), R(Gc, '2.4')], dur={'min': 7, 'max': 21},
          notes=[note('رتینیت ۱۴ تا ۲۱ روز؛ پیوند ۷ تا ۱۴ روز. انفوزیون ۱ ساعته، نه بولوس.', 'Retinitis 14–21 days; transplant 7–14 days. 1-hour infusion, never bolus.', [R(Gc, '2.3'), R(Gc, '2.1')])]),
      reg('maint', 'cmv-infection', T('نگهدارنده — ۵ mg/kg یک بار در روز (۷ روز در هفته) یا ۶ mg/kg (۵ روز در هفته)', 'Maintenance — 5 mg/kg once daily (7 days a week) or 6 mg/kg (5 days a week)'), A18, 'weightBased', {'perKgPerDose': 5, 'intervalHours': 24}, [R(Gc, '2.3'), R(Gc, '2.4')])],
     [CI('hyper', 'حساسیت به گان‌سیکلوویر یا والگان‌سیکلوویر.', 'Hypersensitivity to ganciclovir or valganciclovir.', [R(Gc, '4')])], warn=[HEM(Gc)],
     renal=[{'egfrBelow': 70, 'severity': 'warn', 'text': T('ClCr زیر ۷۰: کاهش دوز القا و نگهدارنده طبق جدول ۱ برچسب.', 'CrCl <70: reduce induction and maintenance doses per label Table 1.'), 'refs': [R(Gc, '2.5')]}],
     exs=[ex('ind', 'vial-500', {'perDose': 350}, ageYears=50, weightKg=70), ex('maint', 'vial-500', {'perDose': 350}, ageYears=50, weightKg=70)])

Vc = fda('valcyte', 'FDA Valcyte', 'Valcyte (valganciclovir) tablets and oral solution — Prescribing Information', sid('valganciclovir'))
drug('valganciclovir', 'anti-infectives', 'والگان‌سیکلوویر', 'Valganciclovir', T('ضدویروس CMV (خوراکی)', 'Oral anti-CMV antiviral'), [{'name': 'Valcyte', 'market': 'US'}], ['valcyte', 'والسایت', 'والگانسیکلوویر'],
     [tab('tab-450', 450, '450 mg tablet', [R(Vc, '3')])],
     [reg('ind', 'cmv-infection', T('رتینیت CMV — القا ۹۰۰ mg دو بار در روز، ۲۱ روز', 'CMV retinitis — induction 900 mg twice daily for 21 days'), A18, 'fixed', {'perDose': 900, 'dosesPerDay': 2}, [R(Vc, '2.2')], dur={'min': 21, 'max': 21}),
      reg('maint', 'cmv-infection', T('رتینیت نگهدارنده یا پیشگیری در پیوند — ۹۰۰ mg یک بار در روز', 'Retinitis maintenance or transplant prevention — 900 mg once daily'), A18, 'fixed', {'perDose': 900, 'dosesPerDay': 1}, [R(Vc, '2.2')],
          notes=[note('پیشگیری: ظرف ۱۰ روز پس از پیوند تا روز ۱۰۰ (قلب، کلیه-پانکراس) یا ۲۰۰ (کلیه). با غذا. کودک طبق الگوریتم BSA و ClCr برچسب.', 'Prevention: within 10 days of transplant until day 100 (heart, kidney-pancreas) or 200 (kidney). With food. Children per label BSA/CrCl algorithm.', [R(Vc, '2.2'), R(Vc, '2.1'), R(Vc, '2.3')])])],
     [CI('hyper', 'حساسیت به والگان‌سیکلوویر یا گان‌سیکلوویر.', 'Hypersensitivity to valganciclovir or ganciclovir.', [R(Vc, '4')])], warn=[HEM(Vc)],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr زیر ۶۰: کاهش دوز طبق جدول ۲؛ همودیالیز: توصیه دوز ندارد.', 'CrCl <60: reduce per Table 2; haemodialysis: no recommendation.'), 'refs': [R(Vc, '2.5')]}],
     exs=[ex('ind', 'tab-450', {'perDose': 900, 'tabletsPerDoseRounded': 2}, ageYears=45, weightKg=70), ex('maint', 'tab-450', {'perDose': 900, 'tabletsPerDoseRounded': 2}, ageYears=45, weightKg=70)])

Fs = fda('foscavir', 'FDA Foscavir', 'Foscavir (foscarnet) 24 mg/mL — Prescribing Information', sid('foscarnet')); d = R(Fs, 'Dosage and Administration')
drug('foscarnet', 'anti-infectives', 'فوسکارنت', 'Foscarnet', T('ضدویروس (آنالوگ پیروفسفات)', 'Antiviral (pyrophosphate analogue)'), [{'name': 'Foscavir', 'market': 'US'}], ['foscavir', 'فوسکاویر', 'فوسکارنت'],
     [form('bot-24', 'injection', 'iv', '24 mg/mL (250 mL)', 24, 'mg', [R(Fs, 'How Supplied')], vol=1)],
     [NC('cmv', 'cmv-infection', 'رتینیت CMV — القا ۹۰ mg/kg هر ۱۲ ساعت یا ۶۰ mg/kg هر ۸ ساعت (۲ تا ۳ هفته)؛ نگهدارنده ۹۰ تا ۱۲۰ mg/kg/روز', 'CMV retinitis — induction 90 mg/kg every 12 h or 60 mg/kg every 8 h (2–3 weeks); maintenance 90–120 mg/kg/day', A18,
         'برچسب: همه دوزها باید بر اساس عملکرد کلیه فردی شوند (جدول برچسب)؛ فقط با پمپ انفوزیون، هرگز بولوس؛ هیدراتاسیون پیش و حین درمان. HSV مقاوم به آسیکلوویر: ۴۰ mg/kg هر ۸ یا ۱۲ ساعت ۲ تا ۳ هفته.', 'Label: every dose must be individualised to renal function (label table); infusion pump only, never bolus; hydrate before and during. Aciclovir-resistant HSV: 40 mg/kg every 8 or 12 h for 2–3 weeks.', [d])],
     [CI('hyper', 'حساسیت قابل‌توجه به فوسکارنت.', 'Clinically significant hypersensitivity to foscarnet.', [R(Fs, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: نارسایی کلیه (شایع‌ترین عارضه محدودکننده)؛ اختلال مواد معدنی و الکترولیت (کلسیم، منیزیم) و تشنج.', 'Boxed warning: renal impairment (major dose-limiting toxicity); mineral/electrolyte disturbances (calcium, magnesium) and seizures.', [R(Fs, 'Boxed Warning')])])

Vm = fda('vemlidy', 'FDA Vemlidy', 'Vemlidy (tenofovir alafenamide) 25 mg — Prescribing Information', sid('vemlidy'))
drug('tenofovir-alafenamide', 'anti-infectives', 'تنوفوویر آلافنامید', 'Tenofovir alafenamide', T('مهارکننده نوکلئوتیدی (HBV)', 'Nucleotide reverse transcriptase inhibitor (HBV)'), [{'name': 'Vemlidy', 'market': 'US'}], ['vemlidy', 'ومیلیدی', 'TAF', 'تنوفوویر آلافنامید'],
     [tab('tab-25', 25, '25 mg tablet', [R(Vm, '3')])],
     [reg('hbv', 'hepatitis-b', T('هپاتیت B مزمن (کبد جبران‌شده) — بزرگسال و کودک ۶ سال و ≥۲۵ kg: ۲۵ mg یک بار با غذا', 'Chronic hepatitis B (compensated) — adults and children ≥6 y and ≥25 kg: 25 mg once daily with food'), {'minAge': age(6, 'year'), 'minWeightKg': 25}, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Vm, '2.2')],
          notes=[note('پیش از شروع HIV چک شود. ClCr ۱۵ و بالاتر تنظیم ندارد؛ ESRD بدون دیالیز توصیه نمی‌شود؛ روزهای دیالیز پس از دیالیز. Child-Pugh B یا C توصیه نمی‌شود.', 'Test for HIV before starting. No adjustment at CrCl ≥15; ESRD not on dialysis not recommended; on dialysis days give after dialysis. Not recommended in Child-Pugh B or C.', [R(Vm, '2.3'), R(Vm, '2.4'), R(Vm, '2')])])],
     warn=[HBV(Vm)], exs=[ex('hbv', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Rb = fda('ribavirin', 'FDA Ribavirin caps', 'Ribavirin capsules 200 mg (Aurobindo) — Prescribing Information', sid('ribavirin'))
drug('ribavirin', 'anti-infectives', 'ریباویرین', 'Ribavirin', T('آنالوگ نوکلئوزید (ضدویروس)', 'Nucleoside analogue antiviral'), [{'name': 'Rebetol', 'market': 'US'}], ['rebetol', 'ربتول', 'ریباویرین'],
     [tab('cap-200', 200, '200 mg capsule', [R(Rb, '3')], per='capsule', form_='capsule')],
     [NC('hcv', 'hepatitis-c', 'هپاتیت C مزمن (فقط همراه اینترفرون) — ۸۰۰ تا ۱۴۰۰ mg/روز در دو دوز بر اساس وزن', 'Chronic hepatitis C (only with interferon) — 800–1400 mg/day in two doses by weight', A18,
         'دوز از جدول وزنی برچسب (همراه PegIntron یا Intron A)؛ با غذا؛ کپسول باز یا شکسته نشود. به‌تنهایی برای HCV مؤثر نیست. در کم‌خونی یا عوارض طبق جدول ۴ کاهش.', 'Dose from the label weight table (with PegIntron or Intron A); with food; do not open or crush. Not effective alone for HCV. Reduce for anaemia/adverse reactions per Table 4.', [R(Rb, '2.2'), R(Rb, '2.3'), R(Rb, '2.1'), R(Rb, '2.5')])],
     [CI('ci', 'بارداری و همسر مرد زن باردار؛ هموگلوبینوپاتی (تالاسمی ماژور، سیکل‌سل)؛ هپاتیت خودایمنی؛ نارسایی کبد جبران‌نشده؛ ClCr زیر ۵۰؛ دیدانوزین.', 'Pregnancy and male partners of pregnant women; haemoglobinopathies (thalassaemia major, sickle-cell); autoimmune hepatitis; decompensated liver disease; CrCl <50; didanosine.', [R(Rb, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت شدید جنینی (پیشگیری تا ۶ ماه پس از درمان در زن و مرد)؛ کم‌خونی همولیتیک؛ به‌تنهایی بی‌اثر.', 'Boxed warning: severe embryo-fetal toxicity (contraception until 6 months after treatment for women and men); haemolytic anaemia; ineffective alone.', [R(Rb, 'Boxed Warning')])])

# ===================== HIV =====================
Ef = fda('efavirenz', 'FDA Efavirenz', 'Efavirenz tablets 600 mg (Cipla) — Prescribing Information', sid('efavirenz'))
drug('efavirenz', 'anti-infectives', 'افاویرنز', 'Efavirenz', T('NNRTI', 'NNRTI'), [{'name': 'Sustiva', 'market': 'US'}], ['sustiva', 'استوکرین', 'افاویرنز', 'EFV'],
     [tab('tab-600', 600, '600 mg tablet (do not crush)', [R(Ef, '3')])],
     [reg('hiv', 'hiv', T('HIV-1 — بزرگسال و کودک ≥۴۰ kg: ۶۰۰ mg یک بار، ناشتا ترجیحاً هنگام خواب', 'HIV-1 — adults and children ≥40 kg: 600 mg once daily, empty stomach, preferably at bedtime'), {'minWeightKg': 40}, 'fixed', {'perDose': 600, 'dosesPerDay': 1}, [R(Ef, '2.2'), R(Ef, '2.3')],
          notes=[ART(Ef, '2.2'), note('با ریفامپین (≥۵۰ kg): ۸۰۰ mg. با وریکونازول: افاویرنز ۳۰۰ mg و وریکونازول ۴۰۰ mg هر ۱۲ ساعت. نارسایی متوسط/شدید کبد توصیه نمی‌شود.', 'With rifampin (≥50 kg): 800 mg. With voriconazole: efavirenz 300 mg and voriconazole 400 mg every 12 h. Not recommended in moderate/severe hepatic impairment.', [R(Ef, '2'), R(Ef, '2.1')])])],
     [CI('ci', 'حساسیت قبلی (SJS، اریتم مولتی‌فرم، راش سمی)؛ الباسویر/گرازوپرویر همزمان.', 'Prior significant hypersensitivity (SJS, erythema multiforme, toxic rash); concomitant elbasvir/grazoprevir.', [R(Ef, '4')])],
     warn=[W('علائم روانی و عصبی (رؤیا، سرگیجه، افسردگی)؛ آسیب جنینی (پیشگیری از بارداری)؛ طولانی شدن QT؛ سمیت کبد.', 'Psychiatric and nervous-system symptoms (dreams, dizziness, depression); embryo-fetal toxicity (avoid pregnancy); QT prolongation; hepatotoxicity.', [R(Ef, '5')])],
     exs=[ex('hiv', 'tab-600', {'perDose': 600, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Is = fda('isentress', 'FDA Isentress', 'Isentress / Isentress HD (raltegravir) — Prescribing Information', sid('raltegravir'))
drug('raltegravir', 'anti-infectives', 'رالتگراویر', 'Raltegravir', T('مهارکننده اینتگراز (INSTI)', 'Integrase inhibitor (INSTI)'), [{'name': 'Isentress', 'market': 'US'}], ['isentress', 'ایزنترس', 'رالتگراویر', 'RAL'],
     [tab('tab-400', 400, '400 mg film-coated tablet', [R(Is, '3')]), tab('tab-600', 600, '600 mg HD tablet', [R(Is, '3')])],
     [reg('hiv', 'hiv', T('HIV-1 — بزرگسال: ۴۰۰ mg دو بار در روز (یا ۱۲۰۰ mg یک بار در درمان‌نشده)', 'HIV-1 — adult: 400 mg twice daily (or 1200 mg once daily if treatment-naive)'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 2}, [R(Is, '2.2, Table 1')], allowed=['tab-400'],
          notes=[ART(Is, '2.2'), note('با ریفامپین: ۸۰۰ mg دو بار. قرص جویدنی و سوسپانسیون جایگزین قرص روکش‌دار نیستند.', 'With rifampin: 800 mg twice daily. Chewable tablets and suspension are not interchangeable with film-coated tablets.', [R(Is, '2.2, Table 1'), R(Is, '2.1')])]),
      reg('hiv-hd', 'hiv', T('HIV-1 درمان‌نشده یا سرکوب‌شده — ۱۲۰۰ mg (۲ × ۶۰۰ mg) یک بار در روز', 'HIV-1 naive or suppressed — 1200 mg (2 × 600 mg) once daily'), A18, 'fixed', {'perDose': 1200, 'dosesPerDay': 1}, [R(Is, '2.2, Table 1')], allowed=['tab-600'], notes=[ART(Is, '2.2')])],
     warn=[W('واکنش شدید پوستی و حساسیت (SJS، DRESS)؛ رابدومیولیز؛ سندرم بازسازی ایمنی.', 'Severe skin and hypersensitivity reactions (SJS, DRESS); rhabdomyolysis; immune reconstitution syndrome.', [R(Is, '5')])],
     exs=[ex('hiv', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('hiv-hd', 'tab-600', {'perDose': 1200, 'tabletsPerDoseRounded': 2}, ageYears=35, weightKg=70)])

Bk = fda('biktarvy', 'FDA Biktarvy', 'Biktarvy (bictegravir/emtricitabine/tenofovir alafenamide) — Prescribing Information', sid('biktarvy'))
drug('biktarvy', 'anti-infectives', 'بیکتاروی (بیکتگراویر/امتریسیتابین/TAF)', 'Bictegravir/emtricitabine/tenofovir alafenamide', T('رژیم کامل تک‌قرص HIV', 'Complete single-tablet HIV regimen'), [{'name': 'Biktarvy', 'market': 'US'}], ['biktarvy', 'بیکتاروی', 'bictegravir', 'بیکتگراویر'],
     [unitform('tab', 'tablet', 'oral', '50/200/25 mg tablet (30/120/15 mg for 14–<25 kg)', [R(Bk, '3')], unit='application', per='tablet')],
     [NC('hiv', 'hiv', 'HIV-1 (رژیم کامل) — ≥۲۵ kg: یک قرص ۵۰/۲۰۰/۲۵ mg روزانه؛ ۱۴ تا <۲۵ kg: یک قرص ۳۰/۱۲۰/۱۵ mg', 'HIV-1 (complete regimen) — ≥25 kg: one 50/200/25 mg tablet daily; 14–<25 kg: one 30/120/15 mg tablet', {'minWeightKg': 14},
         'یک قرص یک بار در روز با یا بدون غذا؛ ClCr ۳۰ و بالاتر. ClCr ۱۵ تا <۳۰ یا ESRD بدون دیالیز مزمن و نارسایی شدید کبد توصیه نمی‌شود.', 'One tablet once daily with or without food; CrCl ≥30. Not recommended at CrCl 15–<30, ESRD not on chronic haemodialysis, or severe hepatic impairment.', [R(Bk, '2.2'), R(Bk, '2.3'), R(Bk, '2.5'), R(Bk, '2.6')])],
     [CI('ci', 'دوفتیلید یا ریفامپین همزمان.', 'Concomitant dofetilide or rifampin.', [R(Bk, '4')])], warn=[HBV(Bk)])

Pz = fda('prezista', 'FDA Prezista', 'Prezista (darunavir) tablets and oral suspension — Prescribing Information', sid('darunavir'))
drug('darunavir', 'anti-infectives', 'داروناویر', 'Darunavir', T('مهارکننده پروتئاز (با ریتوناویر)', 'Protease inhibitor (boosted with ritonavir)'), [{'name': 'Prezista', 'market': 'US'}], ['prezista', 'پرزیستا', 'داروناویر', 'DRV'],
     [tab('tab-800', 800, '800 mg tablet', [R(Pz, '3')]), tab('tab-600', 600, '600 mg tablet', [R(Pz, '3')])],
     [reg('naive', 'hiv', T('HIV-1 درمان‌نشده یا بدون جهش مقاومت — ۸۰۰ mg + ریتوناویر ۱۰۰ mg یک بار با غذا', 'HIV-1 naive or no darunavir resistance — 800 mg + ritonavir 100 mg once daily with food'), A18, 'fixed', {'perDose': 800, 'dosesPerDay': 1}, [R(Pz, '2.3')], allowed=['tab-800'], notes=[ART(Pz, '2.3')]),
      reg('exp', 'hiv', T('HIV-1 با دست‌کم یک جهش مقاومت، یا بارداری — ۶۰۰ mg + ریتوناویر ۱۰۰ mg دو بار با غذا', 'HIV-1 with ≥1 darunavir resistance substitution, or pregnancy — 600 mg + ritonavir 100 mg twice daily with food'), A18, 'fixed', {'perDose': 600, 'dosesPerDay': 2}, [R(Pz, '2.3'), R(Pz, '2.4')], allowed=['tab-600'], notes=[ART(Pz, '2.3')])],
     [CI('ci', 'داروهای با پاکسازی وابسته به CYP3A و دامنه درمانی باریک (آلفوزوسین، رانولازین، دروندارون، کلشی‌سین در نارسایی کلیه/کبد، لوراسیدون، پیموزاید، میدازولام خوراکی، تریازولام، سیلدنافیل برای PAH، سیمواستاتین، لواستاتین، ارگوت…) و القاگرهای قوی (ریفامپین، گل راعی).',
         'Drugs highly dependent on CYP3A with narrow therapeutic index (alfuzosin, ranolazine, dronedarone, colchicine in renal/hepatic impairment, lurasidone, pimozide, oral midazolam, triazolam, sildenafil for PAH, simvastatin, lovastatin, ergots…) and strong inducers (rifampin, St John’s wort).', [R(Pz, '4')])],
     warn=[W('سمیت کبد؛ واکنش شدید پوستی؛ داروناویر سولفونامید دارد (احتیاط در حساسیت به سولفا).', 'Hepatotoxicity; severe skin reactions; contains a sulfonamide moiety (caution in sulfa allergy).', [R(Pz, '5')])],
     exs=[ex('naive', 'tab-800', {'perDose': 800, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('exp', 'tab-600', {'perDose': 600, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Ry = fda('reyataz', 'FDA Reyataz', 'Reyataz (atazanavir) capsules and oral powder — Prescribing Information', sid('atazanavir'))
drug('atazanavir', 'anti-infectives', 'آتازاناویر', 'Atazanavir', T('مهارکننده پروتئاز', 'Protease inhibitor'), [{'name': 'Reyataz', 'market': 'US'}], ['reyataz', 'ریاتاز', 'آتازاناویر', 'ATV'],
     [tab('cap-300', 300, '300 mg capsule', [R(Ry, '3')], per='capsule', form_='capsule'), tab('cap-200', 200, '200 mg capsule', [R(Ry, '3')], per='capsule', form_='capsule')],
     [reg('boost', 'hiv', T('HIV-1 بزرگسال — ۳۰۰ mg + ریتوناویر ۱۰۰ mg یک بار با غذا', 'HIV-1 adult — 300 mg + ritonavir 100 mg once daily with food'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Ry, '2.3')], allowed=['cap-300'],
          notes=[ART(Ry, '2.3'), note('درمان‌نشده: جایگزین ۴۰۰ mg بدون ریتوناویر. با H2 بلاکر یا PPI فاصله زمانی طبق برچسب. آزمایش کلیه پیش و حین درمان.', 'Treatment-naive alternative: 400 mg unboosted. Separate from H2 blockers/PPIs per label. Renal tests before and during therapy.', [R(Ry, '2.3'), R(Ry, '2.1'), R(Ry, '2')])])],
     [CI('ci', 'حساسیت قبلی (SJS، اریتم مولتی‌فرم)؛ داروهای وابسته به CYP3A یا UGT1A1 با دامنه باریک و القاگرهای قوی (طبق جدول برچسب).', 'Prior hypersensitivity (SJS, erythema multiforme); CYP3A/UGT1A1-dependent narrow-index drugs and strong inducers (per label table).', [R(Ry, '4')])],
     warn=[W('اختلال هدایت قلب (PR)؛ راش؛ هیپربیلی‌روبینمی؛ سنگ کلیه و صفرا؛ نارسایی مزمن کلیه.', 'Cardiac conduction abnormalities (PR); rash; hyperbilirubinaemia; nephrolithiasis and cholelithiasis; chronic kidney disease.', [R(Ry, '5')])],
     exs=[ex('boost', 'cap-300', {'perDose': 300, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Ab = fda('abacavir', 'FDA Abacavir', 'Abacavir tablets 300 mg (Aurobindo) — Prescribing Information', sid('abacavir'))
drug('abacavir', 'anti-infectives', 'آباکاویر', 'Abacavir', T('NRTI', 'NRTI'), [{'name': 'Ziagen', 'market': 'US'}], ['ziagen', 'زیاژن', 'آباکاویر', 'ABC'],
     [tab('tab-300', 300, '300 mg tablet (scored)', [R(Ab, '3')], scored=True)],
     [reg('adult', 'hiv', T('HIV-1 بزرگسال — ۳۰۰ mg دو بار یا ۶۰۰ mg یک بار', 'HIV-1 adult — 300 mg twice daily or 600 mg once daily'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 2}, [R(Ab, '2.2')],
          notes=[ART(Ab, '2.2'), note('پیش از شروع HLA-B*5701 چک شود. نارسایی خفیف کبد: ۲۰۰ mg دو بار (محلول خوراکی).', 'Screen for HLA-B*5701 before starting. Mild hepatic impairment: 200 mg twice daily (oral solution).', [R(Ab, '2.1'), R(Ab, '2.4')])]),
      reg('child', 'hiv', T('کودک ≥۱۴ kg (قرص شیاردار) — یک بار: ۳۰۰ / ۴۵۰ / ۶۰۰ mg بر اساس وزن', 'Children ≥14 kg (scored tablet) — once daily: 300 / 450 / 600 mg by weight'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year'), 'minWeightKg': 14}, 'weightBand',
          {'weightBands': [{'minWeightKg': 14, 'maxWeightKg': 19.99, 'perDose': 300, 'dosesPerDay': 1}, {'minWeightKg': 20, 'maxWeightKg': 24.99, 'perDose': 450, 'dosesPerDay': 1}, {'minWeightKg': 25, 'maxWeightKg': None, 'perDose': 600, 'dosesPerDay': 1}]},
          [R(Ab, '2.3, Table 1')], notes=[ART(Ab, '2.3'), note('یا دو بار در روز طبق همان جدول. ناتوان در بلع قرص: محلول خوراکی.', 'Or twice daily per the same table. Unable to swallow tablets: oral solution.', [R(Ab, '2.3')])])],
     [CI('ci', 'ناقل HLA-B*5701؛ حساسیت قبلی به آباکاویر؛ نارسایی متوسط یا شدید کبد.', 'HLA-B*5701 carriers; prior abacavir hypersensitivity; moderate or severe hepatic impairment.', [R(Ab, '4')])],
     warn=[W('هشدار جعبه‌ای: واکنش حساسیتی جدی و گاه کشنده (بیشتر در HLA-B*5701) — پس از واکنش هرگز دوباره نه.', 'Boxed warning: serious, sometimes fatal hypersensitivity (higher with HLA-B*5701) — never rechallenge after a reaction.', [R(Ab, 'Boxed Warning')])],
     exs=[ex('adult', 'tab-300', {'perDose': 300, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('child', 'tab-300', {'perDose': 450, 'tabletsPerDoseRounded': 1.5}, ageYears=7, weightKg=22)])

Ed = fda('edurant', 'FDA Edurant', 'Edurant / Edurant PED (rilpivirine) — Prescribing Information', sid('rilpivirine'))
drug('rilpivirine', 'anti-infectives', 'ریلپیویرین', 'Rilpivirine', T('NNRTI', 'NNRTI'), [{'name': 'Edurant', 'market': 'US'}], ['edurant', 'ادورانت', 'ریلپیویرین', 'RPV'],
     [tab('tab-25', 25, '25 mg tablet', [R(Ed, '3')])],
     [reg('hiv', 'hiv', T('HIV-1 درمان‌نشده — ≥۲۵ kg: ۲۵ mg یک بار با غذا', 'HIV-1 treatment-naive — ≥25 kg: 25 mg once daily with a meal'), {'minAge': age(2, 'year'), 'minWeightKg': 25}, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Ed, '2.2')],
          notes=[ART(Ed, '2.2'), note('با ریفابوتین: ۵۰ mg روزانه. ۱۴ تا <۲۵ kg: Edurant PED (mg به mg جایگزین نیست).', 'With rifabutin: 50 mg daily. 14–<25 kg: Edurant PED (not interchangeable mg-for-mg).', [R(Ed, '2.7'), R(Ed, '2.1')])])],
     [CI('ci', 'القاگرهای CYP3A یا افزاینده pH معده که سطح را شدیداً کم می‌کنند: کاربامازپین، اکس‌کاربازپین، فنوباربیتال، فنی‌توئین، ریفامپین، ریفاپنتین، PPIها، دگزامتازون چنددوزی، گل راعی.',
         'CYP3A inducers or gastric pH-raising drugs that markedly lower levels: carbamazepine, oxcarbazepine, phenobarbital, phenytoin, rifampin, rifapentine, proton-pump inhibitors, multiple-dose dexamethasone, St John’s wort.', [R(Ed, '4')])],
     warn=[W('واکنش پوستی و حساسیت (DRESS)؛ افسردگی؛ سمیت کبد؛ طولانی شدن QT در دوز بالا.', 'Skin and hypersensitivity reactions (DRESS); depressive disorders; hepatotoxicity; QT prolongation at supratherapeutic doses.', [R(Ed, '5')])],
     exs=[ex('hiv', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Cb = fda('cabenuva', 'FDA Cabenuva', 'Cabenuva (cabotegravir + rilpivirine extended-release injectable) — Prescribing Information', sid('cabenuva'))
drug('cabenuva', 'anti-infectives', 'کابنوا (کابوتگراویر + ریلپیویرین تزریقی)', 'Cabotegravir/rilpivirine long-acting injection', T('رژیم تزریقی طولانی‌اثر HIV', 'Long-acting injectable HIV regimen'), [{'name': 'Cabenuva', 'market': 'US'}], ['cabenuva', 'کابنوا', 'cabotegravir', 'کابوتگراویر'],
     [unitform('kit', 'injection', 'im', 'Kit: cabotegravir 600 mg/3 mL + rilpivirine 900 mg/3 mL (or 400/600 mg)', [R(Cb, '3')])],
     [NC('hiv', 'hiv', 'HIV-1 سرکوب‌شده (≥۱۲ سال، ≥۳۵ kg) — تزریق گلوتئال ماهانه یا هر ۲ ماه توسط کادر درمان', 'Virologically suppressed HIV-1 (≥12 y, ≥35 kg) — gluteal IM injections monthly or every 2 months by a healthcare provider', {'minAge': age(12, 'year'), 'minWeightKg': 35},
         'شروع: کابوتگراویر ۶۰۰ mg + ریلپیویرین ۹۰۰ mg. ماهانه: سپس ۴۰۰/۶۰۰ mg هر ماه. هر ۲ ماه: ۶۰۰/۹۰۰ mg ماه ۱ و ۲، سپس هر ۲ ماه. دو تزریق جداگانه در دو طرف باسن. شروع خوراکی اختیاری.', 'Initiation: cabotegravir 600 mg + rilpivirine 900 mg. Monthly: then 400/600 mg every month. Every 2 months: 600/900 mg at months 1 and 2, then every 2 months. Two separate gluteal injections. Optional oral lead-in.', [R(Cb, '2.4'), R(Cb, '2.5'), R(Cb, '2.3')])],
     [CI('ci', 'حساسیت قبلی به کابوتگراویر یا ریلپیویرین؛ القاگرهای UGT1A1 یا CYP3A (کاربامازپین، اکس‌کاربازپین، فنوباربیتال، فنی‌توئین، ریفابوتین، ریفامپین، ریفاپنتین، دگزامتازون، گل راعی).', 'Prior hypersensitivity to cabotegravir or rilpivirine; UGT1A1/CYP3A inducers (carbamazepine, oxcarbazepine, phenobarbital, phenytoin, rifabutin, rifampin, rifapentine, dexamethasone, St John’s wort).', [R(Cb, '4')])],
     warn=[W('واکنش پس از تزریق (مشابه مسمومیت ریلپیویرین)؛ واکنش حساسیتی؛ سمیت کبد؛ افسردگی؛ اثر طولانی تا ۱۲ ماه پس از قطع.', 'Post-injection reactions (rilpivirine-like toxicity); hypersensitivity; hepatotoxicity; depression; long-acting exposure up to 12 months after stopping.', [R(Cb, '5')])])

Dr = fda('daraprim', 'FDA Daraprim', 'Daraprim (pyrimethamine) 25 mg tablets — Prescribing Information', sid('pyrimethamine')); d = R(Dr, 'Dosage and Administration')
drug('pyrimethamine', 'antiparasitic', 'پیریمتامین', 'Pyrimethamine', T('آنتاگونیست اسید فولیک (ضدانگل)', 'Folic acid antagonist (antiparasitic)'), [{'name': 'Daraprim', 'market': 'US'}], ['daraprim', 'داراپریم', 'پیریمتامین'],
     [tab('tab-25', 25, '25 mg tablet (scored)', [R(Dr, 'How Supplied')], scored=True)],
     [reg('toxo', 'toxoplasmosis', T('توکسوپلاسموز — بزرگسال شروع ۵۰ تا ۷۵ mg روزانه همراه سولفونامید، ۱ تا ۳ هفته', 'Toxoplasmosis — adult start 50–75 mg daily with a sulfonamide, 1–3 weeks'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 75, 'dosesPerDay': 1}, [d], dur={'min': 7, 'max': 21},
          notes=[note('همراه ۱ تا ۴ g سولفونامید (مثلاً سولفادیازین) روزانه و اسید فولینیک (لکوورین) در همه بیماران. سپس حدود نصف دوز ۴ تا ۵ هفته. کودک: ۱ mg/kg روزانه در دو دوز ۲ تا ۴ روز، سپس نصف تا یک ماه.', 'With 1–4 g of a sulfonamide (e.g. sulfadiazine) daily and folinic acid (leucovorin) in all patients. Then about half the dose for 4–5 weeks. Children: 1 mg/kg/day in two doses for 2–4 days, then half for about a month.', [d])])],
     [CI('ci', 'حساسیت به پیریمتامین؛ کم‌خونی مگالوبلاستیک ناشی از کمبود فولات.', 'Hypersensitivity to pyrimethamine; megaloblastic anaemia due to folate deficiency.', [R(Dr, 'Contraindications')])],
     warn=[W('دامنه درمانی باریک؛ علائم کمبود فولات — اسید فولینیک ۵ تا ۱۵ mg روزانه؛ CBC دو بار در هفته.', 'Narrow therapeutic window; folate deficiency — folinic acid 5–15 mg daily; CBC twice weekly.', [R(Dr, 'Warnings')])],
     exs=[ex('toxo', 'tab-25', {'perDose': 50, 'tabletsPerDoseRounded': 2, 'upperPerDose': 75}, ageYears=35, weightKg=70)])
print('s12b ok')
