"""Stage 2 — anti-infectives: injectables, TB, new oral forms and STI/other indications."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = {**json.load(open(os.path.join(C, 's1_setids.json'))), **json.load(open(os.path.join(C, 's2_setids.json')))}
sid = lambda k: S[k][0]

add_disease('chlamydia', 'عفونت کلامیدیا (اورتریت/سرویسیت)', 'Chlamydia (urethritis / cervicitis)', ['chlamydia', 'کلامیدیا', 'NGU', 'اورتریت غیرگنوکوکی'], ['A56.00'], 'infectious')
add_disease('epididymitis', 'اپیدیدیمو-ارکیت', 'Epididymo-orchitis', ['epididymitis', 'orchitis', 'اپیدیدیمیت', 'ورم بیضه'], ['N45.3'], 'urology')
add_disease('pid', 'بیماری التهابی لگن (PID)', 'Pelvic inflammatory disease', ['PID', 'عفونت لگن', 'بیماری التهابی لگن'], ['N73.9'], 'gynecology')
add_disease('prostatitis', 'پروستاتیت باکتریایی مزمن', 'Chronic bacterial prostatitis', ['prostatitis', 'پروستاتیت', 'عفونت پروستات'], ['N41.1'], 'urology')
add_disease('scarlet-fever', 'مخملک و اریزیپل (استرپتوکوک گروه A)', 'Scarlet fever and erysipelas (group A streptococcus)', ['scarlet fever', 'erysipelas', 'مخملک', 'باد سرخ'], ['A38.9', 'A46'], 'infectious')
add_disease('c-diff', 'اسهال کلستریدیوم دیفیسیل', 'Clostridioides difficile diarrhoea', ['c diff', 'C. difficile', 'کلستریدیوم', 'کولیت سودوممبران'], ['A04.72'], 'infectious')
add_disease('sepsis', 'سپسیس / عفونت شدید بیمارستانی (ارجاع)', 'Sepsis / serious hospital infection (refer)', ['sepsis', 'septicemia', 'سپسیس', 'عفونت خون'], ['A41.9'], 'infectious')
add_disease('minor-wound', 'زخم، خراش و سوختگی جزئی (پیشگیری از عفونت)', 'Minor cuts, scrapes and burns (infection prevention)', ['wound', 'زخم', 'خراش', 'پماد آنتی بیوتیک'], ['T14.8XXA'], 'dermatology')
add_disease('bacterial-diarrhea', 'اسهال باکتریایی', 'Bacterial diarrhoea', ['bacterial diarrhea', 'اسهال عفونی', 'آنتریت'], ['A04.9'], 'gastroenterology')
REF = lambda fa, en: T(f'داروی بیمارستانی؛ دوز بر اساس نوع و شدت عفونت، کارکرد کلیه و سطح سرمی تعیین می‌شود. {fa}', f'Hospital drug; dose depends on infection type and severity, renal function and serum levels. {en}')
pv = lambda id, label, mg, src, sec, route='iv', unit='mg': form(id, 'powder-for-injection', route, label, mg, unit, [R(src, sec)], per='vial')
CEPH = lambda src, sec: CI('hyper', 'حساسیت به سفالوسپورین‌ها؛ در حساسیت به پنی‌سیلین با احتیاط.', 'Cephalosporin hypersensitivity; caution with penicillin allergy.', [R(src, sec)])

# cefotaxime
Cf = fda('cefotaxime', 'FDA Claforan', 'Claforan (cefotaxime) for injection — Prescribing Information', sid('cefotaxime')); d = R(Cf, 'Dosage and Administration')
drug('cefotaxime', 'anti-infectives', 'سفوتاکسیم (تزریقی)', 'Cefotaxime (injection)', T('سفالوسپورین نسل سوم', 'Third-generation cephalosporin'), [{'name': 'Claforan', 'market': 'US'}], ['claforan', 'کلافوران', 'سفوتاکسیم', 'آمپول سفوتاکسیم'],
     [pv('vial-1g', '1 g vial (IM/IV after reconstitution)', 1000, Cf, 'How Supplied')],
     [reg('child', 'sepsis', T('کودک ۱ ماه تا ۱۲ سال زیر ۵۰ kg — ۵۰ تا ۱۸۰ mg/kg/روز در ۴ تا ۶ دوز', 'Child 1 month–12 y, <50 kg — 50–180 mg/kg/day in 4–6 doses'), {'minAge': age(29, 'day'), 'maxAge': age(13, 'year'), 'maxWeightKg': 49.99}, 'notCalculated',
          {'reason': T('برچسب: ۵۰ تا ۱۸۰ mg/kg/روز عضلانی یا وریدی در ۴ تا ۶ دوز؛ دوز بالاتر برای عفونت شدید از جمله مننژیت. ۵۰ kg و بیشتر: دوز بزرگسال؛ حداکثر ۱۲ گرم در روز. حجم رقیق‌سازی طبق برچسب.', 'Label: 50–180 mg/kg/day IM or IV in 4–6 doses; higher doses for severe infection including meningitis. ≥50 kg: adult dose; max 12 g/day. Dilution per label.')}, [d]),
      reg('adult', 'sepsis', T('بزرگسال — ۱ گرم هر ۱۲ ساعت تا ۲ گرم هر ۴ ساعت بسته به شدت', 'Adult — 1 g every 12 h up to 2 g every 4 h by severity'), A18, 'notCalculated',
          {'reason': T('عفونت ساده: ۱ g هر ۱۲ ساعت؛ متوسط تا شدید: ۱ تا ۲ g هر ۸ ساعت؛ سپتی‌سمی: ۲ g هر ۶ تا ۸ ساعت؛ تهدیدکننده حیات: ۲ g هر ۴ ساعت؛ حداکثر ۱۲ g در روز. گنوره ساده: ۰٫۵ g عضلانی یک دوز.', 'Uncomplicated: 1 g every 12 h; moderate–severe: 1–2 g every 8 h; septicaemia: 2 g every 6–8 h; life-threatening: 2 g every 4 h; max 12 g/day. Uncomplicated gonorrhoea: 0.5 g IM once.')}, [d])],
     [CEPH(Cf, 'Contraindications')])

Cz = fda('ceftazidime', 'FDA Ceftazidime', 'Ceftazidime for injection (WG Critical Care) — Prescribing Information', sid('ceftazidime')); d = R(Cz, 'Dosage and Administration, Table 3')
drug('ceftazidime', 'anti-infectives', 'سفتازیدیم (تزریقی)', 'Ceftazidime (injection)', T('سفالوسپورین نسل سوم ضدسودوموناس', 'Antipseudomonal third-generation cephalosporin'), [{'name': 'Fortaz', 'market': 'US'}], ['fortaz', 'tazicef', 'فورتاز', 'سفتازیدیم'],
     [pv('vial-1g', '1 g (reconstitute per label)', 1000, Cz, 'How Supplied')],
     [reg('child', 'sepsis', T('کودک ۱ ماه تا ۱۲ سال — ۳۰ تا ۵۰ mg/kg هر ۸ ساعت (حداکثر ۶ g در روز)', 'Child 1 month–12 y — 30–50 mg/kg every 8 h (max 6 g/day)'), {'minAge': age(1, 'month'), 'maxAge': age(13, 'year')}, 'weightBased',
          {'perKgPerDose': 30, 'perKgPerDoseMax': 50, 'intervalHours': 8}, [d], limits={'maxPerDay': 6000, 'refs': [d]},
          notes=[note('دوز بالاتر برای نقص ایمنی، فیبروز کیستیک یا مننژیت. در GFR زیر ۵۰ کاهش دوز.', 'Higher dose for immunocompromise, cystic fibrosis or meningitis. Reduce if GFR <50.', [d, R(Cz, 'Dosage and Administration — Impaired Renal Function')])]),
      reg('adult', 'sepsis', T('بزرگسال — معمولاً ۱ g هر ۸ تا ۱۲ ساعت', 'Adult — usually 1 g every 8–12 h'), A18, 'notCalculated',
          {'reason': T('معمول ۱ g وریدی یا عضلانی هر ۸ تا ۱۲ ساعت؛ UTI ساده ۲۵۰ mg هر ۱۲ ساعت؛ مننژیت و عفونت‌های تهدیدکننده ۲ g هر ۸ ساعت. در نارسایی کلیه طبق جدول برچسب.', 'Usual 1 g IV/IM every 8–12 h; uncomplicated UTI 250 mg every 12 h; meningitis and life-threatening infections 2 g every 8 h. Renal impairment per label table.')}, [d])],
     [CEPH(Cz, 'Contraindications')], exs=[ex('child', 'vial-1g', {'status': 'ok', 'perDose': 600, 'upperPerDose': 1000}, ageYears=6, weightKg=20)])

Ak = fda('amikacin', 'FDA Amikacin inj.', 'Amikacin sulfate injection 250 mg/mL (Sagent) — Prescribing Information', sid('amikacin')); d = R(Ak, 'Dosage and Administration')
drug('amikacin', 'anti-infectives', 'آمیکاسین (تزریقی)', 'Amikacin (injection)', T('آمینوگلیکوزید', 'Aminoglycoside'), [{'name': 'Amikin', 'market': 'US'}], ['amikin', 'آمیکاسین', 'آمپول آمیکاسین'],
     [liquid('vial-250', 250, 1, '250 mg/mL (500 mg/2 mL; 1 g/4 mL) vial', [R(Ak, 'How Supplied')], form_='injection', route='im')],
     [reg('std', 'sepsis', T('بزرگسال، کودک و شیرخوار بزرگ‌تر با کلیه سالم — ۱۵ mg/kg/روز در ۲ تا ۳ دوز', 'Adults, children and older infants with normal renal function — 15 mg/kg/day in 2–3 doses'), {'minAge': age(1, 'month')}, 'weightBased', {'perKgPerDay': 15, 'dividedDoses': 2}, [d],
          limits={'maxPerDay': 1500, 'refs': [d]}, dur={'min': 7, 'max': 10}, notes=[note('یعنی ۷٫۵ mg/kg هر ۱۲ ساعت یا ۵ mg/kg هر ۸ ساعت؛ حداکثر ۱٫۵ g در روز. سطح سرمی، کلیه، شنوایی و تعادل پایش شود.', 'i.e. 7.5 mg/kg every 12 h or 5 mg/kg every 8 h; max 1.5 g/day. Monitor serum levels, renal, auditory and vestibular function.', [d])]),
      reg('neo', 'sepsis', T('نوزاد — بارگذاری ۱۰ mg/kg سپس ۷٫۵ mg/kg هر ۱۲ ساعت', 'Newborn — load 10 mg/kg then 7.5 mg/kg every 12 h'), {'maxAge': age(1, 'month')}, 'weightBased', {'perKgPerDose': 7.5, 'intervalHours': 12}, [d],
          notes=[note('دوز اول ۱۰ mg/kg. در نارس و نوزاد به‌علت نارسی کلیه با احتیاط.', 'First dose 10 mg/kg. Caution in premature and newborn infants (renal immaturity).', [d, R(Ak, 'Pediatric Use')])])],
     [CI('hyper', 'حساسیت به آمیکاسین یا سایر آمینوگلیکوزیدها.', 'Hypersensitivity to amikacin or other aminoglycosides.', [R(Ak, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: سمیت گوش، کلیه و عصبی‌عضلانی؛ آسیب جنین در بارداری.', 'Boxed warning: oto-, nephro- and neuromuscular toxicity; fetal harm in pregnancy.', [R(Ak, 'Boxed Warning'), R(Ak, 'Warnings')])],
     exs=[ex('std', 'vial-250', {'perDose': 525, 'mlPerDose': 2.1}, ageYears=40, weightKg=70), ex('neo', 'vial-250', {'perDose': 26.25, 'mlPerDose': 0.11}, ageDays=10, weightKg=3.5)])

Vi = fda('vancoinj', 'FDA Vancomycin inj.', 'Vancomycin hydrochloride for injection (Glenmark) — Prescribing Information', sid('vancoinj'))
Vo = fda('vancooral', 'FDA Vancomycin caps', 'Vancomycin hydrochloride capsules (Cameron) — Prescribing Information', sid('vancooral'))
drug('vancomycin', 'anti-infectives', 'ونکومایسین', 'Vancomycin', T('گلیکوپپتید', 'Glycopeptide antibiotic'), [{'name': 'Vancocin', 'market': 'US'}], ['vancocin', 'ونکوسین', 'ونکومایسین', 'وانکومایسین'],
     [pv('vial-1g', '1 g vial for IV infusion (reconstitute per label)', 1000, Vi, 'How Supplied'), tab('cap-125', 125, '125 mg capsule (oral)', [R(Vo, '3')], per='capsule', form_='capsule'), tab('cap-250', 250, '250 mg capsule (oral)', [R(Vo, '3')], per='capsule', form_='capsule')],
     [reg('cdiff-adult', 'c-diff', T('اسهال C. difficile — بزرگسال: ۱۲۵ mg خوراکی چهار بار در روز، ۱۰ روز', 'C. difficile diarrhoea — adult: 125 mg orally four times daily, 10 days'), A18, 'fixed', {'perDose': 125, 'dosesPerDay': 4}, [R(Vo, '2.1')], allowed=['cap-125', 'cap-250'], dur={'min': 10, 'max': 10}),
      reg('cdiff-child', 'c-diff', T('اسهال C. difficile — کودک: ۴۰ mg/kg/روز خوراکی در ۳ تا ۴ دوز، ۷ تا ۱۰ روز', 'C. difficile diarrhoea — child: 40 mg/kg/day orally in 3–4 doses, 7–10 days'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 40, 'dividedDoses': 4}, [R(Vo, '2.2')], allowed=['cap-125', 'cap-250'], limits={'maxPerDay': 2000, 'refs': [R(Vo, '2.2')]}, dur={'min': 7, 'max': 10}),
      reg('iv-child', 'sepsis', T('وریدی — کودک: ۱۰ mg/kg هر ۶ ساعت (انفوزیون حداقل ۶۰ دقیقه)', 'IV — child: 10 mg/kg every 6 h (infuse over ≥60 min)'), {'minAge': age(1, 'month'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 10, 'intervalHours': 6}, [R(Vi, 'Dosage and Administration — Pediatric patients')], allowed=['vial-1g'],
          notes=[note('سطح سرمی پایش شود. نوزاد: ۱۵ mg/kg سپس ۱۰ mg/kg هر ۱۲ ساعت (هفته اول) و هر ۸ ساعت تا ۱ ماهگی.', 'Monitor serum levels. Neonates: 15 mg/kg then 10 mg/kg every 12 h (first week) and every 8 h up to 1 month.', [R(Vi, 'Dosage and Administration — Neonates')])]),
      reg('iv-adult', 'sepsis', T('وریدی — بزرگسال: ۵۰۰ mg هر ۶ ساعت یا ۱ g هر ۱۲ ساعت', 'IV — adult: 500 mg every 6 h or 1 g every 12 h'), A18, 'notCalculated',
          {'reason': T('برچسب: ۲ g در روز (۵۰۰ mg هر ۶ ساعت یا ۱ g هر ۱۲ ساعت)، هر دوز حداکثر ۱۰ mg/min یا حداقل ۶۰ دقیقه؛ در نارسایی کلیه و سالمندان کاهش دوز و پایش سطح.', 'Label: 2 g/day (500 mg every 6 h or 1 g every 12 h), each dose ≤10 mg/min or over ≥60 min; reduce in renal impairment and the elderly, monitor levels.')}, [R(Vi, 'Dosage and Administration — Adults')])],
     [CI('hyper', 'حساسیت به ونکومایسین.', 'Hypersensitivity to vancomycin.', [R(Vi, 'Contraindications')])],
     warn=[W('تزریق سریع: افت فشار و شوک؛ واکنش‌های تزریق (گرگرفتگی، قرمزی، کهیر، خارش)؛ آسیب حاد کلیه با مواجهه بالا.', 'Rapid infusion: hypotension and shock; infusion reactions (flushing, erythema, urticaria, pruritus); acute kidney injury with high exposure.', [R(Vi, 'Warnings')])],
     exs=[ex('cdiff-adult', 'cap-125', {'perDose': 125, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('cdiff-child', 'cap-125', {'perDose': 250, 'tabletsPerDoseRounded': 2}, ageYears=10, weightKg=25),
          ex('iv-child', 'vial-1g', {'perDose': 200}, ageYears=6, weightKg=20)])

Pg = fda('pfizerpen', 'FDA Penicillin G K inj.', 'Penicillin G potassium for injection (WG Critical Care) — Prescribing Information', sid('pfizerpen')); d = R(Pg, 'Dosage and Administration')
drug('penicillin-g-crystalline', 'anti-infectives', 'پنی‌سیلین G کریستال (تزریقی)', 'Penicillin G (crystalline, injection)', T('پنی‌سیلین طبیعی', 'Natural penicillin'), [{'name': 'Pfizerpen', 'market': 'US'}], ['penicillin g', 'crystalline penicillin', 'پنی سیلین کریستال', 'پنی سیلین جی', 'پنی سیلین ۵ میلیون'],
     [form('vial-5mu', 'powder-for-injection', 'iv', '5,000,000 units vial', 5000000, 'unit', [R(Pg, 'How Supplied')], per='vial')],
     [reg('mening-child', 'bacterial-meningitis', T('مننژیت پنوموکوک/مننگوکوک — کودک: ۲۵۰٬۰۰۰ واحد/kg/روز در دوزهای هر ۴ ساعت', 'Pneumococcal/meningococcal meningitis — child: 250,000 units/kg/day every 4 h'), {'minAge': age(1, 'month'), 'maxAge': age(18, 'year')}, 'weightBased',
          {'perKgPerDay': 250000, 'dividedDoses': 6}, [R(Pg, 'Dosage and Administration — Pediatric Patients')], unit='unit', limits={'maxPerDay': 20000000, 'refs': [R(Pg, 'Dosage and Administration — Pediatric Patients')]}, dur={'min': 7, 'max': 14},
          notes=[note('حداکثر ۱۲ تا ۲۰ میلیون واحد در روز. این فرآورده برای دوزهای کمتر از ۱ میلیون واحد در هر نوبت نیست.', 'Max 12–20 million units/day. This product is not for patients needing less than 1 million units per dose.', [R(Pg, 'Dosage and Administration — Pediatric Patients')])]),
      reg('adult', 'sepsis', T('بزرگسال — عفونت‌های جدی استرپتوکوکی: ۱۲ تا ۲۴ میلیون واحد در روز', 'Adult — serious streptococcal infections: 12–24 million units/day'), A18, 'notCalculated',
          {'reason': T('عفونت جدی استرپتوکوک (سپتی‌سمی، پنومونی، اندوکاردیت، مننژیت): ۱۲ تا ۲۴ میلیون واحد/روز در دوزهای هر ۴ تا ۶ ساعت؛ مننژیت ۱۵ تا ۲۰ میلیون واحد/روز به مدت ۲ هفته. در نارسایی کلیه کاهش.', 'Serious streptococcal infections (septicaemia, pneumonia, endocarditis, meningitis): 12–24 million units/day every 4–6 h; meningitis 15–20 million units/day for 2 weeks. Reduce in renal impairment.')}, [d])],
     [CI('pen', 'سابقه واکنش آنافیلاکسی به هر پنی‌سیلین.', 'History of anaphylactic reaction to any penicillin.', [R(Pg, 'Contraindications')])],
     exs=[ex('mening-child', 'vial-5mu', {'perDose': 833333.33}, ageYears=4, weightKg=20)])

Bc = fda('penprocaine', 'FDA Bicillin C-R', 'Bicillin C-R (penicillin G benzathine + procaine) — Prescribing Information', sid('penprocaine')); d = R(Bc, 'Dosage and Administration — Streptococcal Infections')
LB = 0.4536
drug('penicillin-benzathine-procaine', 'anti-infectives', 'پنی‌سیلین بنزاتین + پروکائین', 'Penicillin G benzathine + procaine', T('پنی‌سیلین طولانی‌اثر عضلانی', 'Long-acting IM penicillin'), [{'name': 'Bicillin C-R', 'market': 'US'}], ['bicillin c-r', 'بیسیلین', 'پنی سیلین ترکیبی'],
     [liquid('syr-1-2mu', 600000, 1, '1,200,000 units / 2 mL syringe (deep IM only)', [R(Bc, 'How Supplied')], form_='injection', route='im', unit='unit')],
     [reg('strep', 'scarlet-fever', T('عفونت استرپتوکوک گروه A (حلق، پوست، مخملک، اریزیپل) — یک نوبت بر اساس وزن', 'Group A strep (throat, skin, scarlet fever, erysipelas) — single dose by weight'), {}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': round(30 * LB, 2) - 0.01, 'perDose': 600000, 'dosesPerDay': 1}, {'minWeightKg': round(30 * LB, 2), 'maxWeightKg': round(60 * LB, 2), 'perDose': 900000, 'dosesPerDay': 1}, {'minWeightKg': round(60 * LB, 2) + 0.01, 'maxWeightKg': None, 'perDose': 2400000, 'dosesPerDay': 1}]},
          [d], unit='unit', dur={'min': 1, 'max': 1}, notes=[note('برچسب بر حسب پوند: زیر ۳۰ پوند ← ۶۰۰٬۰۰۰؛ ۳۰ تا ۶۰ پوند ← ۹۰۰٬۰۰۰ تا ۱٬۲۰۰٬۰۰۰؛ بالای ۶۰ پوند ← ۲٬۴۰۰٬۰۰۰ واحد (به kg تبدیل شده). فقط عضلانی عمیق.', 'Label in pounds: <30 lb → 600,000; 30–60 lb → 900,000–1,200,000; >60 lb → 2,400,000 units (converted to kg). Deep IM only.', [d])])],
     [CI('hyper', 'حساسیت به پنی‌سیلین یا پروکائین.', 'Hypersensitivity to penicillin or procaine.', [R(Bc, 'Contraindications')])],
     warn=[W('هشدار: هرگز وریدی تزریق نشود — ایست قلبی‌تنفسی و مرگ گزارش شده.', 'Warning: never inject intravenously — cardiorespiratory arrest and death reported.', [R(Bc, 'Warnings')])],
     exs=[ex('strep', 'syr-1-2mu', {'perDose': 600000, 'mlPerDose': 1}, ageYears=1, weightKg=10), ex('strep', 'syr-1-2mu', {'perDose': 2400000, 'mlPerDose': 4}, ageYears=20, weightKg=60)])

Un = fda('unasyn', 'FDA Ampicillin-sulbactam', 'Ampicillin and sulbactam for injection (Sagent) — Prescribing Information', sid('unasyn')); d = R(Un, 'Dosage and Administration')
drug('ampicillin-sulbactam', 'anti-infectives', 'آمپی‌سیلین + سولباکتام (تزریقی)', 'Ampicillin + sulbactam (injection)', T('پنی‌سیلین + مهارکننده بتالاکتاماز', 'Penicillin + beta-lactamase inhibitor'), [{'name': 'Unasyn', 'market': 'US'}], ['unasyn', 'یوناسین', 'آمپی سیلین سولباکتام'],
     [pv('vial-1-5', '1.5 g vial (ampicillin 1 g + sulbactam 0.5 g)', 1500, Un, 'How Supplied'), pv('vial-3', '3 g vial (ampicillin 2 g + sulbactam 1 g)', 3000, Un, 'How Supplied')],
     [reg('adult', 'skin-soft-tissue-infection', T('بزرگسال — ۱٫۵ تا ۳ g (مجموع) هر ۶ ساعت', 'Adult — 1.5–3 g (combined) every 6 h'), A18, 'fixed', {'perDose': 1500, 'perDoseMax': 3000, 'dosesPerDay': 4}, [d], limits={'maxPerDay': 12000, 'refs': [d]},
          notes=[note('سولباکتام حداکثر ۴ g در روز (= ۱۲ g مجموع).', 'Sulbactam max 4 g/day (= 12 g combined).', [d])]),
      reg('child', 'skin-soft-tissue-infection', T('کودک ۱ سال به بالا — ۳۰۰ mg/kg/روز (مجموع) وریدی در ۴ دوز', 'Child ≥1 y — 300 mg/kg/day (combined) IV in 4 doses'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year'), 'maxWeightKg': 39.99}, 'weightBased', {'perKgPerDay': 300, 'dividedDoses': 4}, [d],
          notes=[note('۴۰ kg و بیشتر: دوز بزرگسال. عضلانی در کودکان ثابت نشده.', '≥40 kg: adult dose. IM not established in children.', [d])])],
     [CI('ci', 'حساسیت شدید به بتالاکتام‌ها؛ سابقه یرقان کلستاتیک با این دارو.', 'Serious beta-lactam hypersensitivity; prior cholestatic jaundice with this drug.', [R(Un, 'Contraindications')])],
     exs=[ex('adult', 'vial-3', {'perDose': 1500, 'upperPerDose': 3000}, ageYears=40, weightKg=70), ex('child', 'vial-1-5', {'perDose': 1500}, ageYears=6, weightKg=20)])

Eb = fda('ethambutol', 'FDA Ethambutol', 'Ethambutol hydrochloride tablets (STI Pharma) — Prescribing Information', sid('ethambutol')); d = R(Eb, 'Dosage and Administration')
drug('ethambutol', 'anti-infectives', 'اتامبوتول', 'Ethambutol', T('ضدسل', 'Antituberculous'), [{'name': 'Myambutol', 'market': 'US'}], ['myambutol', 'اتامبوتول'],
     [tab('tab-100', 100, '100 mg tablet', [R(Eb, 'How Supplied')]), tab('tab-400', 400, '400 mg tablet (scored)', [R(Eb, 'How Supplied')], scored=True)],
     [reg('initial', 'tuberculosis', T('سل — درمان اولیه: ۱۵ mg/kg یک بار در روز (۱۳ سال به بالا)', 'TB — initial treatment: 15 mg/kg once daily (≥13 y)'), {'minAge': age(13, 'year')}, 'weightBased', {'perKgPerDay': 15, 'dividedDoses': 1}, [d], notes=[note('هرگز تنها مصرف نشود.', 'Never used alone.', [d])]),
      reg('retreat', 'tuberculosis', T('سل — درمان مجدد: ۲۵ mg/kg یک بار در روز به مدت ۶۰ روز، سپس ۱۵ mg/kg', 'TB — retreatment: 25 mg/kg once daily for 60 days, then 15 mg/kg'), {'minAge': age(13, 'year')}, 'weightBased', {'perKgPerDay': 25, 'dividedDoses': 1}, [d], notes=[note('در دوز ۲۵ mg/kg معاینه ماهانه چشم.', 'Monthly eye examination while on 25 mg/kg.', [d])])],
     [CI('ci', 'حساسیت؛ نوریت اپتیک؛ ناتوانی در گزارش تغییرات بینایی (کودک خردسال، بیمار بیهوش).', 'Hypersensitivity; optic neuritis; inability to report visual changes (young children, unconscious patients).', [R(Eb, 'Contraindications')]), CI('lt13', 'زیر ۱۳ سال توصیه نمی‌شود.', 'Not recommended under 13 years.', [R(Eb, 'Pediatric Use')], rule={'maxAge': age(13, 'year')})],
     warn=[W('کاهش دید ناشی از نوریت اپتیک (گاهی دائمی)؛ سمیت کبدی.', 'Reduced vision from optic neuritis (sometimes permanent); liver toxicity.', [R(Eb, 'Warnings')])],
     exs=[ex('initial', 'tab-400', {'perDose': 1200, 'tabletsPerDoseRounded': 3}, ageYears=40, weightKg=80), ex('retreat', 'tab-400', {'perDose': 2000, 'tabletsPerDoseRounded': 5}, ageYears=40, weightKg=80)])

Pz = fda('pyrazinamide', 'FDA Pyrazinamide', 'Pyrazinamide tablets 500 mg (ANI) — Prescribing Information', sid('pyrazinamide')); d = R(Pz, 'Dosage and Administration')
drug('pyrazinamide', 'anti-infectives', 'پیرازینامید', 'Pyrazinamide', T('ضدسل', 'Antituberculous'), [{'name': 'Pyrazinamide', 'market': 'US'}], ['pza', 'پیرازینامید'],
     [tab('tab-500', 500, '500 mg tablet (scored)', [R(Pz, 'How Supplied')], scored=True)],
     [reg('tb', 'tuberculosis', T('سل — ۱۵ تا ۳۰ mg/kg یک بار در روز (۲ ماه اول)', 'TB — 15–30 mg/kg once daily (first 2 months)'), {}, 'weightBased', {'perKgPerDay': 15, 'perKgPerDayMax': 30, 'dividedDoses': 1}, [d], limits={'maxPerDay': 3000, 'refs': [d]},
          notes=[note('همیشه با سایر داروهای سل؛ CDC حداکثر ۲ g در رژیم روزانه.', 'Always with other TB drugs; CDC daily maximum 2 g.', [d])])],
     [CI('ci', 'آسیب شدید کبد؛ نقرس حاد؛ حساسیت.', 'Severe hepatic damage; acute gout; hypersensitivity.', [R(Pz, 'Contraindications')])],
     mon=[note('اسید اوریک و آزمایش کبد پایه و دوره‌ای.', 'Baseline and periodic uric acid and liver tests.', [R(Pz, 'Warnings')])],
     exs=[ex('tb', 'tab-500', {'perDose': 750, 'tabletsPerDoseRounded': 1.5, 'upperPerDose': 1500}, ageYears=40, weightKg=50)])

Az = fda('azithroiv', 'FDA Azithromycin inj.', 'Azithromycin for injection 500 mg (Sun) — Prescribing Information', sid('azithroiv'))
patch('azithromycin', add_forms=[pv('vial-500', '500 mg vial for IV infusion', 500, Az, '3')],
      add_regs=[reg('pid-iv', 'pid', T('بیماری التهابی لگن — بزرگسال: ۵۰۰ mg وریدی روزانه ۱ تا ۲ روز، سپس ۲۵۰ mg خوراکی تا ۷ روز', 'PID — adult: 500 mg IV daily for 1–2 days, then 250 mg orally to complete 7 days'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 1}, [R(Az, '2.2')], allowed=['vial-500'], dur={'min': 1, 'max': 2}),
                reg('cap-iv', 'community-acquired-pneumonia', T('پنومونی اکتسابی — بزرگسال: ۵۰۰ mg وریدی روزانه حداقل ۲ روز، سپس خوراکی تا ۷ تا ۱۰ روز', 'CAP — adult: 500 mg IV daily ≥2 days, then oral to 7–10 days'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 1}, [R(Az, '2.1')], allowed=['vial-500'], dur={'min': 2, 'max': 2},
                    notes=[note('انفوزیون ۱ mg/mL در ۳ ساعت یا ۲ mg/mL در ۱ ساعت؛ هرگز بولوس یا عضلانی.', 'Infuse 1 mg/mL over 3 h or 2 mg/mL over 1 h; never bolus or IM.', [R(Az, '2.3')])])],
      add_exs=[ex('pid-iv', 'vial-500', {'perDose': 500}, ageYears=25, weightKg=60), ex('cap-iv', 'vial-500', {'perDose': 500}, ageYears=50, weightKg=70)], pin_old=True)

Ds = fda('doxysusp', 'FDA Doxycycline susp.', 'Doxycycline for oral suspension 25 mg/5 mL (Lupin) — Prescribing Information', sid('doxysusp')); d = R(Ds, 'Dosage and Administration')
patch('doxycycline', add_forms=[liquid('susp-25', 25, 5, '25 mg / 5 mL oral suspension', [R(Ds, 'How Supplied')])],
      add_regs=[reg('chlamydia', 'chlamydia', T('کلامیدیا (اورتریت، سرویسیت، رکتال) — بزرگسال: ۱۰۰ mg دو بار در روز، ۷ روز', 'Chlamydia (urethral, endocervical, rectal) — adult: 100 mg twice daily, 7 days'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [d], dur={'min': 7, 'max': 7}),
                reg('epididymitis', 'epididymitis', T('اپیدیدیمو-ارکیت کلامیدیایی — ۱۰۰ mg دو بار در روز، حداقل ۱۰ روز', 'Chlamydial epididymo-orchitis — 100 mg twice daily, at least 10 days'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [d], dur={'min': 10, 'max': 10}),
                reg('malaria-adult', 'malaria', T('پیشگیری مالاریا — بزرگسال: ۱۰۰ mg روزانه', 'Malaria prophylaxis — adult: 100 mg daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [d], notes=[note('از ۱ تا ۲ روز پیش از سفر تا ۴ هفته پس از ترک منطقه.', 'From 1–2 days before travel until 4 weeks after leaving.', [d])]),
                reg('malaria-child', 'malaria', T('پیشگیری مالاریا — کودک بالای ۸ سال: ۲ mg/kg روزانه (تا دوز بزرگسال)', 'Malaria prophylaxis — child >8 y: 2 mg/kg daily (up to adult dose)'), {'minAge': age(8, 'year'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 2, 'dividedDoses': 1}, [d], limits={'maxPerDose': 100, 'refs': [d]}),
                reg('child-lt45', 'susceptible-bacterial-infection', T('عفونت‌های حساس — کودک بالای ۸ سال زیر ۴۵ kg: روز اول ۴٫۴ mg/kg در ۲ دوز، سپس ۲٫۲ mg/kg روزانه', 'Susceptible infections — child >8 y, <45 kg: 4.4 mg/kg in 2 doses on day 1, then 2.2 mg/kg daily'), {'minAge': age(8, 'year'), 'maxAge': age(18, 'year'), 'maxWeightKg': 44.99}, 'weightBased', {'perKgPerDay': 2.2, 'dividedDoses': 1}, [d],
                    notes=[note('روز اول ۴٫۴ mg/kg در دو دوز. ۸ سال و کمتر فقط در عفونت‌های شدید (مثل سیاه‌زخم، تب منقوط): ۲٫۲ mg/kg هر ۱۲ ساعت.', 'Day 1: 4.4 mg/kg in two doses. ≤8 years only for severe infections (e.g. anthrax, Rocky Mountain spotted fever): 2.2 mg/kg every 12 h.', [d, R(Ds, 'Pediatric Use')])])],
      add_exs=[ex('chlamydia', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=25, weightKg=60), ex('epididymitis', 'tab-100', {'perDose': 100}, ageYears=30, weightKg=75),
               ex('malaria-adult', 'tab-100', {'perDose': 100}, ageYears=30, weightKg=70), ex('malaria-child', 'susp-25', {'perDose': 60, 'mlPerDose': 12}, ageYears=10, weightKg=30), ex('child-lt45', 'susp-25', {'perDose': 66, 'mlPerDose': 13.2}, ageYears=10, weightKg=30)])

Ci = fda('clindainj', 'FDA Cleocin Phosphate', 'Cleocin Phosphate (clindamycin injection 150 mg/mL) — Prescribing Information', sid('clindainj'))
Cc = fda('clindacap', 'FDA Clindamycin caps', 'Clindamycin hydrochloride capsules (Aurobindo) — Prescribing Information', sid('clindacap')); dc = R(Cc, 'Dosage and Administration')
patch('clindamycin', add_forms=[tab('cap-150', 150, '150 mg capsule', [R(Cc, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-300', 300, '300 mg capsule', [R(Cc, 'How Supplied')], per='capsule', form_='capsule'),
                               liquid('inj-150', 150, 1, '150 mg/mL injection (IM undiluted; IV diluted)', [R(Ci, 'How Supplied')], form_='injection', route='iv')],
      add_regs=[reg('cap-adult', 'serious-anaerobic-infection', T('کپسول — بزرگسال: ۱۵۰ تا ۳۰۰ mg هر ۶ ساعت (شدیدتر ۳۰۰ تا ۴۵۰ mg)', 'Capsules — adult: 150–300 mg every 6 h (more severe 300–450 mg)'), A18, 'fixed', {'perDose': 150, 'perDoseMax': 300, 'dosesPerDay': 4}, [dc], allowed=['cap-150', 'cap-300']),
                reg('cap-child', 'serious-anaerobic-infection', T('کپسول — کودکی که کپسول می‌بلعد: ۸ تا ۱۶ mg/kg/روز در ۳ تا ۴ دوز', 'Capsules — child able to swallow capsules: 8–16 mg/kg/day in 3–4 doses'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 8, 'perKgPerDayMax': 16, 'dividedDoses': 4}, [dc], allowed=['cap-150', 'cap-300'],
                    notes=[note('عفونت شدیدتر ۱۶ تا ۲۰ mg/kg/روز. بر اساس وزن کل بدن حتی در چاقی.', 'More severe 16–20 mg/kg/day. Dose by total body weight, even in obesity.', [dc])]),
                reg('iv-child', 'serious-anaerobic-infection', T('تزریقی — کودک ۱ ماه تا ۱۶ سال: ۲۰ تا ۴۰ mg/kg/روز در ۳ تا ۴ دوز', 'Injection — child 1 month–16 y: 20–40 mg/kg/day in 3–4 doses'), {'minAge': age(1, 'month'), 'maxAge': age(17, 'year')}, 'weightBased', {'perKgPerDay': 20, 'perKgPerDayMax': 40, 'dividedDoses': 4}, [R(Ci, 'Dosage and Administration')], allowed=['inj-150'],
                    notes=[note('دوز بالاتر در عفونت شدیدتر. حاوی بنزیل الکل (خطر در نوزاد). تزریق عضلانی تک‌دوز بیش از ۶۰۰ mg توصیه نمی‌شود.', 'Higher doses for more severe infection. Contains benzyl alcohol (neonatal risk). Single IM injections >600 mg not recommended.', [R(Ci, 'Dosage and Administration'), R(Ci, 'Warnings — Neonates')])])],
      add_exs=[ex('cap-adult', 'cap-150', {'perDose': 150, 'tabletsPerDoseRounded': 1, 'upperPerDose': 300}, ageYears=40, weightKg=70), ex('cap-child', 'cap-150', {'perDose': 150, 'tabletsPerDoseRounded': 1, 'upperPerDose': 300}, ageYears=16, weightKg=75), ex('iv-child', 'inj-150', {'perDose': 100, 'mlPerDose': 0.67, 'upperPerDose': 200}, ageYears=5, weightKg=20)], pin_old=True)

Mi = fda('metroiv', 'FDA Metronidazole inj.', 'Metronidazole injection 500 mg/100 mL (WG Critical Care) — Prescribing Information', sid('metroiv')); d = R(Mi, 'Dosage and Administration')
patch('metronidazole', add_forms=[liquid('iv-5', 5, 1, '500 mg / 100 mL (5 mg/mL) IV infusion', [R(Mi, 'How Supplied')], form_='injection', route='iv')],
      add_regs=[reg('iv-load', 'serious-anaerobic-infection', T('عفونت بی‌هوازی شدید — بارگذاری ۱۵ mg/kg وریدی طی ۱ ساعت', 'Serious anaerobic infection — loading 15 mg/kg IV over 1 h'), A18, 'weightBased', {'perKgPerDay': 15, 'dividedDoses': 1}, [d], allowed=['iv-5'], notes=[note('حدود ۱ g برای ۷۰ kg؛ ۶ ساعت بعد نگهدارنده.', 'About 1 g for 70 kg; maintenance starts 6 h later.', [d])]),
                reg('iv-maint', 'serious-anaerobic-infection', T('نگهدارنده — ۷٫۵ mg/kg وریدی هر ۶ ساعت', 'Maintenance — 7.5 mg/kg IV every 6 h'), A18, 'weightBased', {'perKgPerDose': 7.5, 'intervalHours': 6}, [d], allowed=['iv-5'], limits={'maxPerDay': 4000, 'refs': [d]})],
      add_exs=[ex('iv-load', 'iv-5', {'perDose': 1050, 'mlPerDose': 210}, ageYears=40, weightKg=70), ex('iv-maint', 'iv-5', {'perDose': 525, 'mlPerDose': 105}, ageYears=40, weightKg=70)], pin_old=True)

Ai = fda('ampinj', 'FDA Ampicillin inj.', 'Ampicillin for injection (Sagent) — Prescribing Information', sid('ampinj')); d = R(Ai, 'Dosage and Administration')
patch('ampicillin', add_forms=[pv('vial-1g', '1 g vial (IM/IV after reconstitution)', 1000, Ai, 'How Supplied')],
      add_regs=[reg('mening', 'bacterial-meningitis', T('مننژیت / سپتی‌سمی — بزرگسال و کودک: ۱۵۰ تا ۲۰۰ mg/kg/روز در دوزهای هر ۳ تا ۴ ساعت', 'Meningitis / septicaemia — adults and children: 150–200 mg/kg/day every 3–4 h'), {'minAge': age(29, 'day')}, 'weightBased', {'perKgPerDay': 150, 'perKgPerDayMax': 200, 'dividedDoses': 6}, [d], allowed=['vial-1g'],
                    notes=[note('نوزاد ۲۸ روزه و کمتر: بر اساس سن بارداری و پس از تولد (جدول ۱ برچسب). با آمینوگلیکوزید اثر بیشتر.', 'Neonates ≤28 days: by gestational and postnatal age (label Table 1). Aminoglycoside may enhance effect.', [d])])],
      add_exs=[ex('mening', 'vial-1g', {'perDose': 500, 'upperPerDose': 666.67}, ageYears=4, weightKg=20)], pin_old=True)

Ex = fda('cephalexincap', 'FDA Cephalexin caps', 'Cephalexin capsules (Aurobindo) — Prescribing Information', sid('cephalexincap'))
patch('cephalexin', add_forms=[tab('cap-250', 250, '250 mg capsule', [R(Ex, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-500', 500, '500 mg capsule', [R(Ex, 'How Supplied')], per='capsule', form_='capsule')])
Er = fda('erythrotab', 'FDA Erythromycin tabs', 'Erythromycin tablets 250/500 mg (Torrent) — Prescribing Information', sid('erythrotab'))
patch('erythromycin', add_forms=[tab('tab-250', 250, '250 mg tablet (base)', [R(Er, 'How Supplied')]), tab('tab-500', 500, '500 mg tablet (base)', [R(Er, 'How Supplied')])],
      add_regs=[reg('tab-adult', 'respiratory-tract-infection', T('قرص — بزرگسال: ۲۵۰ mg چهار بار در روز یا ۵۰۰ mg هر ۱۲ ساعت', 'Tablets — adult: 250 mg four times daily or 500 mg every 12 h'), A18, 'fixed', {'perDose': 250, 'dosesPerDay': 4}, [R(Er, 'Dosage and Administration — Adults')], allowed=['tab-250', 'tab-500'], limits={'maxPerDay': 4000, 'refs': [R(Er, 'Dosage and Administration — Adults')]},
                    notes=[note('تا ۴ g در روز بسته به شدت؛ بالای ۱ g در روز دو بار در روز توصیه نمی‌شود.', 'Up to 4 g/day by severity; twice-daily dosing not recommended above 1 g/day.', [R(Er, 'Dosage and Administration — Adults')])])],
      add_exs=[ex('tab-adult', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)], pin_old=True)
Cp = fda('ciprosusp', 'FDA Cipro (tab+susp)', 'Cipro (ciprofloxacin) tablets and oral suspension (Bayer) — Prescribing Information', sid('ciprosusp'))
patch('ciprofloxacin', add_regs=[reg('prostatitis', 'prostatitis', T('پروستاتیت باکتریایی مزمن — ۵۰۰ mg هر ۱۲ ساعت، ۲۸ روز', 'Chronic bacterial prostatitis — 500 mg every 12 h, 28 days'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 2}, [R(Cp, 'Dosage and Administration — Adult Dosage Guidelines')], dur={'min': 28, 'max': 28}, allowed=['tab-250', 'tab-500', 'tab-750', 'susp-250', 'susp-500'])],
      add_exs=[ex('prostatitis', 'tab-500', {'perDose': 500, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=80)])

Np = fda('neosporin', 'FDA Neosporin', 'Neosporin Original (bacitracin/neomycin/polymyxin B) ointment — Drug Facts', sid('neosporin')); d = R(Np, 'Directions')
drug('neomycin-polymyxin-bacitracin', 'dermatology', 'پماد سه‌آنتی‌بیوتیک (نئومایسین + پلی‌میکسین + باسیتراسین)', 'Triple antibiotic ointment (neomycin + polymyxin B + bacitracin)', T('آنتی‌بیوتیک موضعی', 'Topical antibiotic'), [{'name': 'Neosporin', 'market': 'US'}],
     ['neosporin', 'نئوسپورین', 'پماد آنتی بیوتیک', 'triple antibiotic'],
     [unitform('oint', 'ointment', 'topical', 'Per g: bacitracin 400 U, neomycin 3.5 mg, polymyxin B 5,000 U', [R(Np, 'Active ingredients')])],
     [reg('wound', 'minor-wound', T('زخم و خراش و سوختگی جزئی — مقدار کم ۱ تا ۳ بار در روز', 'Minor cuts, scrapes, burns — small amount 1–3 times daily'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 3}, [d], unit='application', dur={'min': 1, 'max': 7})],
     [CI('ci', 'حساسیت به اجزا؛ در چشم یا سطح وسیع بدن مصرف نشود. زخم عمیق، گازگرفتگی حیوان یا سوختگی جدی: با پزشک.', 'Allergy to ingredients; not in the eyes or over large areas. Deep or puncture wounds, animal bites, serious burns: ask a doctor.', [R(Np, 'Warnings')])],
     exs=[ex('wound', 'oint', {'perDose': 1}, ageYears=10, weightKg=30)])

Fz = dy('ir-darooyab-furazolidone', 'Darooyab Furazolidone', 'فورازولیدون — موارد مصرف، منع مصرف، تداخلات و اشکال دارویی', 'G-1122/Furazolidone')
drug('furazolidone', 'anti-infectives', 'فورازولیدون', 'Furazolidone', T('نیتروفوران روده‌ای', 'Intestinal nitrofuran'), [{'name': 'Furazolidone', 'market': 'IR'}], ['furoxone', 'فورازولیدون', 'فوروکسون'],
     [tab('tab-100', 100, '100 mg tablet', [R(Fz, 'اشکال دارویی')], markets=('IR',)), liquid('susp', 50, 15, '50 mg / 15 mL suspension', [R(Fz, 'اشکال دارویی')], markets=('IR',))],
     [reg('diarrhea', 'bacterial-diarrhea', T('اسهال و آنتریت باکتریایی', 'Bacterial diarrhoea and enteritis'), {'minAge': age(1, 'month')}, 'notCalculated',
          {'reason': T('رفرنس مطمئن نیست: برچسب آمریکا/انگلیس برای فورازولیدون در دسترس نیست و اطلاعات از سایت ایرانی دارویاب است. دوز محاسبه نمی‌شود.', 'Reference not reliable: no current US/UK label; information is from the Iranian site Darooyab. No dose is calculated.')}, [R(Fz, 'موارد مصرف')])],
     [CI('lt1m', 'نوزاد زیر یک ماه — ممنوع.', 'Infants under 1 month — contraindicated.', [R(Fz, 'محدودیت سنی')], rule={'maxAge': age(1, 'month')}),
      CI('lact', 'در شیردهی توصیه نمی‌شود (خطر کم‌خونی همولیتیک شیرخوار).', 'Not recommended while breastfeeding (risk of haemolytic anaemia in the infant).', [R(Fz, 'شیردهی')], sev='warn')],
     inter=[IA('maoi', 'مهار MAO: با غذاهای حاوی تیرامین و داروهای مقلد سمپاتیک یا سروتونرژیک بحران فشار خون؛ الکل تا ۴ روز پس از قطع ممنوع.', 'MAO inhibition: hypertensive crisis with tyramine foods and sympathomimetic or serotonergic drugs; no alcohol until 4 days after stopping.', [R(Fz, 'تداخلات')])])
print('s2 ok')
