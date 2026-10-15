"""Stage 5 — pregnancy, women and neonates."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's5_setids.json')))
sid = lambda k: S[k][0]

add_disease('labor-induction', 'القای زایمان / تقویت انقباضات (بیمارستانی)', 'Labour induction / augmentation (hospital)', ['induction of labor', 'القای زایمان', 'اکسی توسین', 'سنتوسینون'], [], 'obstetrics')
add_disease('rh-prophylaxis', 'پیشگیری از ایمن‌سازی Rh (مادر Rh منفی)', 'Rh(D) isoimmunisation prophylaxis (Rh-negative mother)', ['RhoGAM', 'رگام', 'آنتی دی', 'Rh منفی'], ['Z29.13'], 'obstetrics')
add_disease('postpartum-depression', 'افسردگی پس از زایمان', 'Postpartum depression', ['PPD', 'postpartum depression', 'افسردگی بعد از زایمان'], ['F53.0'], 'psychiatry')
add_disease('lactation-suppression', 'قطع یا جلوگیری از شیردهی', 'Lactation inhibition / suppression', ['stop breast milk', 'قطع شیر', 'خشک کردن شیر'], ['O92.5'], 'obstetrics')
add_disease('apnea-of-prematurity', 'آپنه نوزاد نارس', 'Apnoea of prematurity', ['apnea of prematurity', 'آپنه نارسی', 'کافئین نوزاد'], ['P28.40'], 'pediatrics')
add_disease('neonatal-rds', 'سندرم دیسترس تنفسی نوزاد (کمبود سورفکتانت)', 'Neonatal respiratory distress syndrome', ['RDS', 'HMD', 'سورفکتانت', 'دیسترس تنفسی نوزاد'], ['P22.0'], 'pediatrics')
add_disease('pda', 'مجرای شریانی باز (PDA) در نوزاد نارس', 'Patent ductus arteriosus (preterm)', ['PDA', 'مجرای شریانی باز', 'داکتوس'], ['Q25.0'], 'pediatrics')
add_disease('neonatal-seizures', 'تشنج نوزادی', 'Neonatal seizures', ['neonatal seizures', 'تشنج نوزاد'], ['P90'], 'pediatrics')
add_disease('rsv-prophylaxis', 'پیشگیری از RSV در شیرخوار', 'RSV prophylaxis in infants', ['RSV', 'برونشیولیت', 'nirsevimab', 'آر اس وی'], ['Z29.11'], 'pediatrics')
ONE = {'min': 1, 'max': 1}
inj = lambda id, label, amt, ml, src, sec, route='iv', unit='mg': liquid(id, amt, ml, label, [R(src, sec)], form_='injection', route=route, unit=unit)

# --- obstetric ---
Ox = fda('pitocin', 'FDA Pitocin', 'Pitocin (oxytocin injection) — Prescribing Information', sid('pitocin')); d = R(Ox, 'Dosage and Administration')
drug('oxytocin', 'systemic-hormones', 'اکسی‌توسین', 'Oxytocin', T('هورمون منقبض‌کننده رحم', 'Uterotonic hormone'), [{'name': 'Pitocin', 'market': 'US'}], ['pitocin', 'syntocinon', 'سنتوسینون', 'اکسی توسین'],
     [inj('vial-10', '10 units/mL injection', 10, 1, Ox, 'How Supplied', route='im', unit='unit')],
     [reg('pph-im', 'postpartum-hemorrhage', T('خونریزی پس از زایمان — ۱۰ واحد عضلانی پس از خروج جفت', 'Postpartum haemorrhage — 10 units IM after delivery of the placenta'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Ox, 'Dosage and Administration — B. Control of Postpartum Uterine Bleeding')], unit='unit', dur=ONE,
          notes=[note('وریدی: ۱۰ تا ۴۰ واحد به سرم در جریان (حداکثر ۴۰ واحد در ۱۰۰۰ mL) و تنظیم سرعت برای حفظ انقباض رحم.', 'IV: add 10–40 units to the running infusion (max 40 units per 1,000 mL) and adjust the rate to sustain uterine contraction.', [R(Ox, 'Dosage and Administration — B. Control of Postpartum Uterine Bleeding')])]),
      reg('induction', 'labor-induction', T('القا یا تقویت زایمان — فقط انفوزیون وریدی با پمپ', 'Induction or augmentation of labour — IV infusion by pump only'), A18, 'notCalculated',
          {'reason': T('برچسب: ۱ ویال ۱۰ واحدی در ۱۰۰۰ mL سالین یا رینگر لاکتات (۱۰ میلی‌واحد/mL). شروع ۰٫۵ تا ۱ میلی‌واحد/دقیقه (۳ تا ۶ mL/ساعت)، هر ۳۰ تا ۶۰ دقیقه ۱ تا ۲ میلی‌واحد/دقیقه افزایش تا الگوی انقباض مطلوب. فقط در بیمارستان با پایش؛ برای القای انتخابی بدون اندیکاسیون نیست.',
                       'Label: one 10-unit vial in 1,000 mL saline or Ringer’s lactate (10 mU/mL). Start 0.5–1 mU/min (3–6 mL/h), increase by 1–2 mU/min every 30–60 min until the desired contraction pattern. Hospital with monitoring only; not for elective induction without indication.')}, [d])],
     [CI('ante', 'پیش از زایمان: عدم تناسب سر و لگن، وضعیت نامناسب جنین، دیسترس جنین بدون زایمان قریب‌الوقوع، رحم پرکار، منع زایمان طبیعی (جفت سرراهی کامل، وازا پرویا، هرپس فعال تناسلی، پرولاپس بند ناف)، حساسیت.',
         'Antepartum: cephalopelvic disproportion, unfavourable fetal position, fetal distress with delivery not imminent, hyperactive uterus, contraindication to vaginal delivery (complete placenta praevia, vasa praevia, active genital herpes, cord prolapse), hypersensitivity.', [R(Ox, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: برای القای انتخابی زایمان (بدون اندیکاسیون پزشکی) اندیکاسیون ندارد.', 'Boxed warning: not indicated for elective induction of labour.', [R(Ox, 'Boxed Warning')])],
     exs=[ex('pph-im', 'vial-10', {'perDose': 10, 'mlPerDose': 1}, ageYears=28, weightKg=70)])

Cb = fda('carboprost', 'FDA Carboprost', 'Carboprost tromethamine injection 250 mcg/mL — Prescribing Information', sid('hemabate')); d = R(Cb, 'Dosage and Administration — 2. Refractory Postpartum Uterine Bleeding')
drug('carboprost', 'genitourinary-sex-hormones', 'کاربوپروست', 'Carboprost', T('پروستاگلاندین منقبض‌کننده رحم', 'Uterotonic prostaglandin'), [{'name': 'Hemabate', 'market': 'US'}], ['hemabate', 'همابیت', 'کاربوپروست'],
     [inj('amp-250', '250 mcg/mL (1 mL) ampoule', 250, 1, Cb, 'How Supplied', route='im', unit='mcg')],
     [reg('pph', 'postpartum-hemorrhage', T('خونریزی مقاوم پس از زایمان — ۲۵۰ mcg عضلانی عمیق', 'Refractory postpartum haemorrhage — 250 mcg deep IM'), A18, 'fixed', {'perDose': 250, 'dosesPerDay': 1}, [d], unit='mcg', dur=ONE,
          notes=[note('بیشتر موارد با یک تزریق جواب می‌دهند؛ در صورت نیاز تکرار با فاصله ۱۵ تا ۹۰ دقیقه. مجموع حداکثر ۲ mg (۸ دوز).', 'Most respond to a single injection; repeat at 15–90 min intervals if needed. Total max 2 mg (8 doses).', [d])])],
     [CI('ci', 'حساسیت به کاربوپروست؛ PID حاد؛ بیماری فعال قلبی، ریوی، کلیوی یا کبدی.', 'Hypersensitivity to carboprost; acute PID; active cardiac, pulmonary, renal or hepatic disease.', [R(Cb, 'Contraindications')])],
     warn=[W('فقط با دوز دقیق و در بیمارستان با امکان مراقبت ویژه و جراحی فوری.', 'Strictly at recommended doses, in a hospital with immediate intensive care and surgery.', [R(Cb, 'Warnings')])],
     exs=[ex('pph', 'amp-250', {'perDose': 250, 'mlPerDose': 1}, ageYears=28, weightKg=70)])

Rh = fda('rhogam', 'FDA RhoGAM', 'RhoGAM Ultra-Filtered PLUS (Rho(D) immune globulin) — Prescribing Information', sid('rhogam')); d = R(Rh, '2.1')
drug('rho-d-immune-globulin', 'anti-infectives', 'ایمونوگلوبولین Rh (آنتی‌D، رگام)', 'Rho(D) immune globulin (anti-D)', T('ایمونوگلوبولین اختصاصی', 'Specific immune globulin'), [{'name': 'RhoGAM', 'market': 'US'}], ['rhogam', 'رگام', 'آنتی دی', 'anti-D', 'روگام'],
     [form('syr-300', 'injection', 'im', '300 mcg (1500 IU) prefilled syringe', 300, 'mcg', [R(Rh, '3')], per='vial')],
     [reg('std', 'rh-prophylaxis', T('مادر Rh منفی — ۳۰۰ mcg عضلانی (هفته ۲۶ تا ۲۸، پس از زایمان، سقط یا عارضه)', 'Rh-negative mother — 300 mcg IM (26–28 weeks, postpartum, abortion or complication)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [d], unit='mcg', dur=ONE,
          notes=[note('بارداری: هفته ۲۶ تا ۲۸. پس از زایمان (اگر نوزاد Rh مثبت): ظرف ۷۲ ساعت. سقط، حاملگی خارج رحمی، روش تهاجمی یا ترومای بعد از ۱۳ هفته: ظرف ۷۲ ساعت. خونریزی جنینی-مادری بیش از ۱۵ mL گلبول قرمز: ۲۰ mcg به ازای هر mL گلبول قرمز Rh مثبت، گرد به سرنگ کامل بعدی.',
                      'Pregnancy: 26–28 weeks. Postpartum (if newborn Rh-positive): within 72 h. Abortion, ectopic, invasive procedure or trauma after 13 weeks: within 72 h. Fetal-maternal haemorrhage >15 mL red cells: 20 mcg per mL of Rh-positive red cells, rounded up to the next whole syringe.', [d])])],
     [CI('ci', 'افراد Rh مثبت؛ سابقه آنافیلاکسی یا واکنش سیستمیک شدید به ایمونوگلوبولین انسانی.', 'Rh-positive individuals; history of anaphylaxis or severe systemic reaction to human immune globulin.', [R(Rh, '4')])],
     exs=[ex('std', 'syr-300', {'perDose': 300}, ageYears=28, weightKg=70)])

Zr = fda('zurzuvae', 'FDA Zurzuvae', 'Zurzuvae (zuranolone) capsules — Prescribing Information', sid('zurzuvae')); d = R(Zr, '2.1')
drug('zuranolone', 'nervous-system', 'زورانولون', 'Zuranolone', T('تعدیل‌کننده گیرنده GABA-A (ضدافسردگی پس از زایمان)', 'GABA-A receptor modulator (postpartum depression)'), [{'name': 'Zurzuvae', 'market': 'US'}], ['zurzuvae', 'زورانولون'],
     [tab(f'cap-{m}', m, f'{m} mg capsule', [R(Zr, '3')], per='capsule', form_='capsule') for m in (20, 25, 30)],
     [reg('ppd', 'postpartum-depression', T('افسردگی پس از زایمان — ۵۰ mg شب‌ها با غذای چرب، ۱۴ روز', 'Postpartum depression — 50 mg every evening with fatty food, 14 days'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [d], dur={'min': 14, 'max': 14},
          notes=[note('اگر عوارض سرکوب CNS: ۴۰ mg. نارسایی شدید کبد (Child-Pugh C) یا eGFR زیر ۶۰: ۳۰ mg. بیش از ۱۴ روز بررسی نشده.', 'If CNS depressant effects: 40 mg. Severe hepatic impairment (Child-Pugh C) or eGFR <60: 30 mg. Not studied beyond 14 days.', [d, R(Zr, '2.3'), R(Zr, '2.4')])])],
     warn=[W('هشدار جعبه‌ای: اختلال رانندگی — تا ۱۲ ساعت پس از هر دوز در طول ۱۴ روز رانندگی یا کار خطرناک نکند.', 'Boxed warning: impaired driving — no driving or hazardous activity until at least 12 h after each dose during the 14 days.', [R(Zr, 'Boxed Warning')])],
     exs=[ex('ppd', 'cap-25', {'perDose': 50, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=65)])

Mi = fda('methergine-inj', 'FDA Methergine inj.', 'Methylergonovine maleate injection 0.2 mg/mL (American Regent) — Prescribing Information', sid('methergineinj')); d = R(Mi, 'Dosage and Administration')
patch('methylergonovine', add_forms=[inj('inj-0-2', '0.2 mg/mL (1 mL) ampoule', 0.2, 1, Mi, 'How Supplied', route='im')],
      add_regs=[reg('pph-inj', 'postpartum-hemorrhage', T('خونریزی پس از زایمان — ۰٫۲ mg عضلانی (یا وریدی آهسته)، تکرار هر ۲ تا ۴ ساعت', 'Postpartum haemorrhage — 0.2 mg IM (or slow IV), repeat every 2–4 h'), A18, 'fixed', {'perDose': 0.2, 'dosesPerDay': 1}, [d], allowed=['inj-0-2'],
                    notes=[note('عضلانی پس از خروج شانه قدامی، پس از جفت یا در دوره نفاس؛ در صورت نیاز هر ۲ تا ۴ ساعت. وریدی آهسته در حداقل ۶۰ ثانیه.', 'IM after delivery of the anterior shoulder, after the placenta or in the puerperium; repeat every 2–4 h as required. IV slowly over at least 60 s.', [d])])],
      add_exs=[ex('pph-inj', 'inj-0-2', {'perDose': 0.2, 'mlPerDose': 1}, ageYears=28, weightKg=70)], pin_old=True)
p = find('methylergonovine'); dd = json.load(open(p))
if not any(c['id'] == 'inj-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('inj-ci', 'تزریقی: فشار خون بالا، توکسمی (پره‌اکلامپسی)، بارداری، حساسیت.', 'Injection: hypertension, toxaemia (pre-eclampsia), pregnancy, hypersensitivity.', [R(Mi, 'Contraindications')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Dx = uk('uk-dostinex', 'UK Dostinex SmPC', 'Dostinex (cabergoline) tablets — SmPC', 'Pfizer Limited', '09/2024', 1691)
patch('cabergoline',
      add_regs=[reg('lact-inhibit', 'lactation-suppression', T('جلوگیری از شیردهی — ۱ mg (۲ قرص ۰٫۵) یک‌جا در روز اول پس از زایمان', 'Inhibition of lactation — 1 mg (two 0.5 mg tablets) once on the first day postpartum'), A18, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Dx, '4.2')], dur=ONE),
                reg('lact-suppress', 'lactation-suppression', T('قطع شیردهی برقرارشده — ۰٫۲۵ mg هر ۱۲ ساعت، ۲ روز', 'Suppression of established lactation — 0.25 mg every 12 h for 2 days'), A18, 'fixed', {'perDose': 0.25, 'dosesPerDay': 2}, [R(Dx, '4.2')], dur={'min': 2, 'max': 2},
                    notes=[note('این رژیم نسبت به دوز یک‌جا بهتر تحمل می‌شود (افت فشار کمتر). همراه غذا.', 'Better tolerated than the single dose (less hypotension). With food.', [R(Dx, '4.2')])])],
      add_exs=[ex('lact-inhibit', 'tab-0-5', {'perDose': 1, 'tabletsPerDoseRounded': 2}, ageYears=28, weightKg=70), ex('lact-suppress', 'tab-0-5', {'perDose': 0.25, 'tabletsPerDoseRounded': 0.5}, ageYears=28, weightKg=70)])
p = find('cabergoline'); dd = json.load(open(p))
if not any(c['id'] == 'uk-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('uk-ci', 'حساسیت به ارگوت‌ها؛ سابقه فیبروز ریه، پریکارد یا رتروپریتوئن؛ نارسایی کبد؛ توکسمی بارداری؛ مصرف همزمان آنتی‌سایکوتیک؛ سابقه سایکوز پس از زایمان.', 'Ergot hypersensitivity; history of pulmonary, pericardial or retroperitoneal fibrosis; hepatic insufficiency; toxaemia of pregnancy; concomitant antipsychotics; history of puerperal psychosis.', [R(Dx, '4.3')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

# --- women ---
Pm = fda('prometrium', 'FDA Prometrium', 'Prometrium (progesterone) capsules — Prescribing Information', sid('prometrium')); d = R(Pm, 'Dosage and Administration')
drug('progesterone-oral', 'genitourinary-sex-hormones', 'پروژسترون خوراکی (میکرونیزه)', 'Progesterone (oral, micronised)', T('پروژستین', 'Progestogen'), [{'name': 'Prometrium', 'market': 'US'}], ['prometrium', 'utrogestan', 'پروژسترون', 'اوتروژستان'],
     [tab('cap-100', 100, '100 mg capsule', [R(Pm, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-200', 200, '200 mg capsule', [R(Pm, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('hrt', 'menopause-symptoms', T('همراه استروژن در یائسگی با رحم — ۲۰۰ mg شب‌ها، ۱۲ روز از هر ۲۸ روز', 'With oestrogen in postmenopausal women with a uterus — 200 mg at bedtime, 12 days per 28-day cycle'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [d], dur={'min': 12, 'max': 12}),
      reg('amen', 'secondary-amenorrhea', T('آمنوره ثانویه — ۴۰۰ mg شب‌ها، ۱۰ روز', 'Secondary amenorrhoea — 400 mg at bedtime, 10 days'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 1}, [d], dur={'min': 10, 'max': 10})],
     [CI('ci', 'حساسیت (حاوی روغن بادام‌زمینی)؛ خونریزی نامشخص تناسلی؛ سرطان پستان؛ DVT/PE یا ترومبوز شریانی فعال یا سابقه آن؛ بیماری کبد.', 'Hypersensitivity (contains peanut oil); undiagnosed genital bleeding; breast cancer; active or past DVT/PE or arterial thrombosis; liver disease.', [R(Pm, 'Contraindications')])],
     warn=[W('اختلالات قلبی‌عروقی: در PE، DVT، سکته یا MI فوراً قطع؛ ۴ تا ۶ هفته پیش از جراحی پرخطر قطع شود.', 'Cardiovascular disorders: stop immediately if PE, DVT, stroke or MI; stop 4–6 weeks before high-risk surgery.', [R(Pm, 'Warnings')])],
     exs=[ex('hrt', 'cap-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=70), ex('amen', 'cap-200', {'perDose': 400, 'tabletsPerDoseRounded': 2}, ageYears=25, weightKg=60)])

Vz = fda('veozah', 'FDA Veozah', 'Veozah (fezolinetant) tablets — Prescribing Information', sid('veozah')); d = R(Vz, '2.1')
drug('fezolinetant', 'genitourinary-sex-hormones', 'فزولینتانت', 'Fezolinetant', T('آنتاگونیست گیرنده نوروکینین ۳ (گرگرفتگی یائسگی)', 'Neurokinin-3 receptor antagonist (menopausal hot flushes)'), [{'name': 'Veozah', 'market': 'US'}], ['veozah', 'فزولینتانت', 'گرگرفتگی'],
     [tab('tab-45', 45, '45 mg tablet', [R(Vz, '3')])],
     [reg('vms', 'menopause-symptoms', T('گرگرفتگی متوسط تا شدید یائسگی — ۴۵ mg یک بار در روز', 'Moderate–severe menopausal hot flushes — 45 mg once daily'), A18, 'fixed', {'perDose': 45, 'dosesPerDay': 1}, [d],
          notes=[note('پیش از شروع آزمایش کبد؛ اگر ALT یا AST ≥ ۲ برابر حد بالا یا بیلی‌روبین ≥ ۲ برابر، شروع نشود. پایش ماهانه در ۳ ماه اول و سپس ماه ۶ و ۹. قرص کامل بلعیده شود.', 'Liver tests before starting; do not start if ALT or AST ≥2× ULN or bilirubin ≥2× ULN. Monitor monthly for 3 months, then at 6 and 9 months. Swallow whole.', [d, R(Vz, 'Boxed Warning')])])],
     [CI('ci', 'سیروز؛ نارسایی شدید کلیه یا ESRD؛ مصرف همزمان مهارکننده‌های CYP1A2.', 'Cirrhosis; severe renal impairment or ESRD; concomitant CYP1A2 inhibitors.', [R(Vz, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی؛ با علائم آسیب کبد فوراً قطع شود.', 'Boxed warning: hepatotoxicity; stop immediately with signs of liver injury.', [R(Vz, 'Boxed Warning')])],
     inter=[IA('cyp1a2', 'مهارکننده‌های CYP1A2 (مثل فلووکسامین، سیپروفلوکساسین) — ممنوع.', 'CYP1A2 inhibitors (e.g. fluvoxamine, ciprofloxacin) — contraindicated.', [R(Vz, '4')])],
     exs=[ex('vms', 'tab-45', {'perDose': 45, 'tabletsPerDoseRounded': 1}, ageYears=52, weightKg=70)])

Cl = fda('clindesse', 'FDA Clindesse', 'Clindesse (clindamycin phosphate) vaginal cream 2% — Prescribing Information', sid('cleocinvag'))
drug('clindamycin-vaginal', 'genitourinary-sex-hormones', 'کلیندامایسین کرم واژینال', 'Clindamycin vaginal cream', T('آنتی‌بیوتیک واژینال', 'Vaginal antibiotic'), [{'name': 'Clindesse', 'market': 'US'}], ['clindesse', 'cleocin vaginal', 'کرم کلیندامایسین واژینال'],
     [unitform('app-5', 'vaginal-cream', 'vaginal', '2% cream, 5 g single-dose applicator (100 mg)', [R(Cl, '3')], unit='application', per='application')],
     [reg('bv', 'bacterial-vaginosis', T('واژینوز باکتریایی (غیرباردار) — یک اپلیکاتور یک‌بار', 'Bacterial vaginosis (non-pregnant) — one applicator once'), {}, 'notCalculated',
          {'reason': T('کل محتوای یک اپلیکاتور (۵ گرم) یک بار داخل واژن در هر ساعت از روز.', 'The entire contents of one 5 g applicator once intravaginally at any time of day.')}, [R(Cl, '2'), R(Cl, '1')])],
     [CI('ci', 'حساسیت به کلیندامایسین یا لینکوزامیدها؛ سابقه انتریت ناحیه‌ای، کولیت اولسراتیو یا اسهال C. difficile.', 'Hypersensitivity to clindamycin or lincosamides; history of regional enteritis, ulcerative colitis or C. difficile diarrhoea.', [R(Cl, '4')])])

Tc = fda('terconazole', 'FDA Terconazole cream', 'Terconazole vaginal cream 0.4% (Fougera) — Prescribing Information', sid('terconazole')); d = R(Tc, 'Dosage and Administration')
drug('terconazole', 'genitourinary-sex-hormones', 'ترکونازول کرم واژینال', 'Terconazole vaginal cream', T('ضدقارچ واژینال (تری‌آزول)', 'Vaginal antifungal (triazole)'), [{'name': 'Terazol', 'market': 'US'}], ['terazol', 'ترکونازول'],
     [unitform('cream-04', 'vaginal-cream', 'vaginal', '0.4% cream, 5 g applicator (20 mg)', [R(Tc, 'How Supplied')])],
     [reg('vvc', 'vaginal-candidiasis', T('کاندیدیاز واژن — یک اپلیکاتور شب‌ها، ۷ روز', 'Vaginal candidiasis — one applicator at bedtime, 7 days'), {}, 'notCalculated',
          {'reason': T('یک اپلیکاتور کامل (۵ گرم، ۲۰ mg) داخل واژن شب‌ها ۷ شب متوالی؛ قاعدگی اثر را کم نمی‌کند.', 'One full applicator (5 g, 20 mg) intravaginally at bedtime for 7 consecutive days; menstruation does not affect it.')}, [d])],
     [CI('ci', 'حساسیت به ترکونازول.', 'Hypersensitivity to terconazole.', [R(Tc, 'Contraindications')])])

Dn = uk('uk-dienogest', 'UK Dienogest SmPC', 'Dienogest 2 mg tablets — SmPC', 'Exeltis UK Ltd', '05/08/2024', 101366)
drug('dienogest', 'genitourinary-sex-hormones', 'دینوژست', 'Dienogest', T('پروژستین', 'Progestogen'), [{'name': 'Visanne', 'market': 'UK'}], ['visanne', 'ویزان', 'دینوژست'],
     [tab('tab-2', 2, '2 mg tablet', [R(Dn, '4.2')], markets=('UK',))],
     [reg('endo', 'endometriosis', T('آندومتریوز — ۲ mg یک بار در روز بدون وقفه', 'Endometriosis — 2 mg once daily without a break'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Dn, '4.2')],
          notes=[note('هر روز در ساعت ثابت، بدون توجه به خونریزی؛ بسته بعدی بی‌وقفه. پیشگیری هورمونی قطع و در صورت نیاز روش سدی.', 'Same time each day regardless of bleeding; start the next pack without a break. Stop hormonal contraception; use a barrier method if needed.', [R(Dn, '4.2')])])],
     [CI('ci', 'ترومبوآمبولی وریدی فعال؛ بیماری شریانی یا قلبی‌عروقی؛ دیابت با درگیری عروق؛ بیماری یا تومور کبد؛ بدخیمی وابسته به هورمون؛ خونریزی نامشخص واژن؛ حساسیت.', 'Active VTE; arterial or cardiovascular disease; diabetes with vascular involvement; liver disease or tumour; sex-hormone-dependent malignancy; undiagnosed vaginal bleeding; hypersensitivity.', [R(Dn, '4.3')])],
     exs=[ex('endo', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=60)])

Ol = fda('orilissa', 'FDA Orilissa', 'Orilissa (elagolix) tablets — Prescribing Information', sid('orilissa')); d = R(Ol, '2.1, Table 1')
drug('elagolix', 'genitourinary-sex-hormones', 'الاگولیکس', 'Elagolix', T('آنتاگونیست GnRH خوراکی', 'Oral GnRH antagonist'), [{'name': 'Orilissa', 'market': 'US'}], ['orilissa', 'اوریلیسا', 'الاگولیکس'],
     [tab('tab-150', 150, '150 mg tablet', [R(Ol, '3')]), tab('tab-200', 200, '200 mg tablet', [R(Ol, '3')])],
     [reg('std', 'endometriosis', T('درد آندومتریوز — ۱۵۰ mg یک بار در روز (حداکثر ۲۴ ماه)', 'Endometriosis pain — 150 mg once daily (max 24 months)'), A18, 'fixed', {'perDose': 150, 'dosesPerDay': 1}, [d], allowed=['tab-150'],
          notes=[note('پیش از شروع بارداری رد شود یا ظرف ۷ روز از شروع قاعدگی شروع شود. نارسایی متوسط کبد: فقط ۱۵۰ mg و حداکثر ۶ ماه.', 'Exclude pregnancy or start within 7 days of menses. Moderate hepatic impairment: 150 mg only, max 6 months.', [R(Ol, '2.1'), R(Ol, '2.2')])]),
      reg('dysp', 'endometriosis', T('درد آندومتریوز با دیسپارونی — ۲۰۰ mg دو بار در روز (حداکثر ۶ ماه)', 'Endometriosis pain with dyspareunia — 200 mg twice daily (max 6 months)'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 2}, [d], allowed=['tab-200'])],
     [CI('ci', 'بارداری؛ استئوپوروز؛ نارسایی شدید کبد؛ مهارکننده‌های قوی OATP1B1؛ حساسیت.', 'Pregnancy; osteoporosis; severe hepatic impairment; strong OATP1B1 inhibitors; hypersensitivity.', [R(Ol, '4')])],
     warn=[W('کاهش تراکم استخوان وابسته به دوز و مدت؛ مدت مصرف محدود شود.', 'Dose- and duration-dependent bone loss; limit duration of use.', [R(Ol, '2.1')])],
     exs=[ex('std', 'tab-150', {'perDose': 150, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=60), ex('dysp', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=60)])

# --- neonates ---
Ko = fda('caffeine-oral', 'FDA Caffeine cit. oral', 'Caffeine citrate oral solution 20 mg/mL (Armas) — Prescribing Information', sid('cafcitoral')); d = R(Ko, 'Dosage and Administration')
Ki = fda('caffeine-inj', 'FDA Caffeine cit. inj.', 'Caffeine citrate injection 20 mg/mL (Eugia) — Prescribing Information', sid('cafcit'))
NEO = {'maxAge': age(1, 'year')}
CAF = note('دوز بر حسب کافئین سیترات است (کافئین پایه نصف آن). پیش از شروع در نوزادی که تئوفیلین گرفته یا مادرش کافئین مصرف کرده، سطح سرمی کافئین. پایش دوره‌ای سطح برای جلوگیری از سمیت.', 'Doses are caffeine citrate (caffeine base is half). Check baseline caffeine level if the infant had theophylline or the mother consumed caffeine. Monitor levels periodically to avoid toxicity.', [d])
CAFIR = note('آمپول ایران «کافئین (به‌صورت سیترات) ۳۰ mg/۳ mL» بر حسب کافئین پایه است = ۶۰ mg کافئین سیترات در ۳ mL؛ یعنی همان غلظت ۲۰ mg/mL سیترات. دوزهای این صفحه بر حسب سیترات است.', 'The Iranian ampoule “caffeine (as citrate) 30 mg/3 mL” is labelled as caffeine base = 60 mg caffeine citrate per 3 mL, i.e. the same 20 mg/mL citrate. Doses here are citrate.', [R('darooyab-generic', 'G-1457/Caffeine'), d])
drug('caffeine-citrate', 'nervous-system', 'کافئین سیترات (نوزاد)', 'Caffeine citrate (neonatal)', T('محرک تنفسی (متیل‌گزانتین)', 'Respiratory stimulant (methylxanthine)'), [{'name': 'Cafcit', 'market': 'US'}], ['cafcit', 'کافئین سیترات', 'کافئین نوزاد'],
     [liquid('oral-20', 20, 1, '20 mg/mL oral solution (60 mg/3 mL vial)', [R(Ko, 'How Supplied')], form_='solution'), inj('inj-20', '20 mg/mL injection (60 mg/3 mL vial)', 20, 1, Ki, 'How Supplied')],
     [reg('load', 'apnea-of-prematurity', T('آپنه نارسی — بارگذاری ۲۰ mg/kg وریدی در ۳۰ دقیقه', 'Apnoea of prematurity — loading 20 mg/kg IV over 30 min'), NEO, 'weightBased', {'perKgPerDay': 20, 'dividedDoses': 1}, [d], allowed=['inj-20'], dur=ONE, notes=[CAF, CAFIR]),
      reg('maint', 'apnea-of-prematurity', T('آپنه نارسی — نگهدارنده ۵ mg/kg هر ۲۴ ساعت (وریدی یا خوراکی)', 'Apnoea of prematurity — maintenance 5 mg/kg every 24 h (IV or oral)'), NEO, 'weightBased', {'perKgPerDay': 5, 'dividedDoses': 1}, [d],
          notes=[note('۲۴ ساعت پس از دوز بارگذاری شروع شود. وریدی در ۱۰ دقیقه با پمپ سرنگی.', 'Start 24 h after the loading dose. IV over 10 min by syringe pump.', [d]), CAF, CAFIR])],
     [CI('hyper', 'حساسیت به اجزای فرآورده.', 'Hypersensitivity to any component.', [R(Ko, 'Contraindications')])],
     exs=[ex('load', 'inj-20', {'perDose': 30, 'mlPerDose': 1.5}, ageDays=3, weightKg=1.5), ex('maint', 'oral-20', {'perDose': 7.5, 'mlPerDose': 0.38}, ageDays=5, weightKg=1.5)])

Cu = fda('curosurf', 'FDA Curosurf', 'Curosurf (poractant alfa) intratracheal suspension — Prescribing Information', sid('curosurf')); d = R(Cu, '2.2')
drug('poractant-alfa', 'respiratory', 'پوراکتانت آلفا (سورفکتانت)', 'Poractant alfa (surfactant)', T('سورفکتانت ریوی', 'Pulmonary surfactant'), [{'name': 'Curosurf', 'market': 'US'}], ['curosurf', 'کوروسرف', 'سورفکتانت'],
     [form('vial-80', 'suspension', 'inhaled', '80 mg/mL (120 mg/1.5 mL; 240 mg/3 mL) intratracheal suspension', 80, 'mg', [R(Cu, '3')], vol=1)],
     [reg('initial', 'neonatal-rds', T('RDS نوزاد نارس — دوز اول ۲٫۵ mL/kg (۲۰۰ mg/kg) داخل تراشه', 'Preterm RDS — initial 2.5 mL/kg (200 mg/kg) intratracheal'), NEO, 'weightBased', {'perKgPerDay': 200, 'dividedDoses': 1}, [d], dur=ONE,
          notes=[note('بر اساس وزن تولد. فقط داخل تراشه توسط پزشک باتجربه در اینتوباسیون و مراقبت نوزاد نارس.', 'Based on birth weight. Intratracheal only, by clinicians experienced in intubation and preterm care.', [d, R(Cu, '2.1')])]),
      reg('repeat', 'neonatal-rds', T('RDS — تکرار ۱٫۲۵ mL/kg (۱۰۰ mg/kg) با فاصله حدود ۱۲ ساعت، حداکثر ۲ بار', 'RDS — repeat 1.25 mL/kg (100 mg/kg) about 12 h apart, up to 2 times'), NEO, 'weightBased', {'perKgPerDay': 100, 'dividedDoses': 1}, [d],
          notes=[note('مجموع دوز اول و تکرارها حداکثر ۵ mL/kg.', 'Total of initial and repeat doses max 5 mL/kg.', [d])])],
     exs=[ex('initial', 'vial-80', {'perDose': 300, 'mlPerDose': 3.75}, ageDays=1, weightKg=1.5), ex('repeat', 'vial-80', {'perDose': 150, 'mlPerDose': 1.88}, ageDays=1, weightKg=1.5)])

Np = fda('neoprofen', 'FDA NeoProfen', 'NeoProfen (ibuprofen lysine) injection — Prescribing Information', sid('neoprofen')); d = R(Np, '2.1')
PDAN = note('دوزها بر اساس وزن تولد. اگر هنگام دوز دوم یا سوم آنوری یا الیگوری (زیر ۰٫۶ mL/kg/ساعت) بود، تا طبیعی شدن کلیه داده نشود. رقیق و در ۱۵ دقیقه انفوزیون.', 'Doses by birth weight. Withhold the 2nd/3rd dose if anuria or oliguria (<0.6 mL/kg/h) until renal function normalises. Dilute and infuse over 15 min.', [d, R(Np, '2.2')])
drug('ibuprofen-lysine', 'cardiovascular', 'ایبوپروفن لیزین وریدی (نوزاد)', 'Ibuprofen lysine IV (neonatal)', T('NSAID برای بستن PDA', 'NSAID for PDA closure'), [{'name': 'NeoProfen', 'market': 'US'}], ['neoprofen', 'نئوپروفن', 'ایبوپروفن وریدی نوزاد'],
     [inj('vial-10', '10 mg/mL (20 mg/2 mL) vial', 10, 1, Np, '3')],
     [reg('first', 'pda', T('PDA نوزاد نارس — دوز اول ۱۰ mg/kg وریدی', 'Preterm PDA — first dose 10 mg/kg IV'), NEO, 'weightBased', {'perKgPerDay': 10, 'dividedDoses': 1}, [d], dur=ONE, notes=[PDAN]),
      reg('next', 'pda', T('PDA — دوز دوم و سوم ۵ mg/kg پس از ۲۴ و ۴۸ ساعت', 'PDA — 2nd and 3rd doses 5 mg/kg after 24 and 48 h'), NEO, 'weightBased', {'perKgPerDay': 5, 'dividedDoses': 1}, [d], dur={'min': 2, 'max': 2}, notes=[PDAN])],
     [CI('ci', 'عفونت درمان‌نشده؛ بیماری قلبی وابسته به PDA؛ خونریزی فعال (داخل جمجمه یا گوارش)؛ ترومبوسیتوپنی؛ اختلال انعقادی؛ NEC؛ اختلال قابل‌توجه کلیه.', 'Untreated infection; ductal-dependent congenital heart disease; active bleeding (intracranial or GI); thrombocytopenia; coagulation defects; NEC; significant renal impairment.', [R(Np, '4')])],
     exs=[ex('first', 'vial-10', {'perDose': 15, 'mlPerDose': 1.5}, ageDays=3, weightKg=1.5), ex('next', 'vial-10', {'perDose': 7.5, 'mlPerDose': 0.75}, ageDays=4, weightKg=1.5)])

Sz = fda('sezaby', 'FDA Sezaby', 'Sezaby (phenobarbital sodium) for injection — Prescribing Information', sid('sezaby')); d = R(Sz, '2.1, Table 1')
PBIR = note('در ایران آمپول ۱۰۰ و ۲۰۰ mg/mL (دارویاب) هم هست؛ حجم بالا برای پودر ۱۰ mg/mL است — با آمپول ایرانی حجم را از روی mg و غلظت همان آمپول حساب کنید.', 'Iran also has 100 and 200 mg/mL ampoules (Darooyab); the volume shown is for the 10 mg/mL reconstituted powder — with an Iranian ampoule compute the volume from the mg dose and that ampoule’s strength.', [R('darooyab-generic', 'G-677/Phenobarbital')])
drug('phenobarbital-neonatal', 'nervous-system', 'فنوباربیتال وریدی (نوزاد)', 'Phenobarbital IV (neonatal seizures)', T('ضدتشنج باربیتورات', 'Barbiturate anticonvulsant'), [{'name': 'Sezaby', 'market': 'US'}], ['sezaby', 'فنوباربیتال', 'لومینال'],
     [form('vial-100', 'powder-for-injection', 'iv', '100 mg vial (10 mg/mL after reconstitution with 10 mL)', 10, 'mg', [R(Sz, '3'), R(Sz, '2.2')], vol=1)],
     [reg('load', 'neonatal-seizures', T('تشنج نوزادی — بارگذاری ۲۰ mg/kg وریدی در ۱۵ دقیقه', 'Neonatal seizures — loading 20 mg/kg IV over 15 min'), {'maxAge': age(28, 'day')}, 'weightBased', {'perKgPerDay': 20, 'dividedDoses': 1}, [d], dur=ONE,
          notes=[note('اگر ۱۵ دقیقه پس از پایان بارگذاری تشنج ادامه یافت: دوز دوم (نارس ۱۰ یا ۲۰ mg/kg؛ ترم ۲۰ mg/kg). مجموع بارگذاری حداکثر ۴۰ mg/kg. در ورید بزرگ محیطی.', 'If seizures persist 15 min after the loading dose: a second dose (preterm 10 or 20 mg/kg; term 20 mg/kg). Total loading max 40 mg/kg. Into a large peripheral vein.', [d]), PBIR]),
      reg('maint', 'neonatal-seizures', T('تشنج نوزادی — نگهدارنده ۴٫۵ mg/kg/روز (۱٫۵ mg/kg هر ۸ ساعت)', 'Neonatal seizures — maintenance 4.5 mg/kg/day (1.5 mg/kg every 8 h)'), {'maxAge': age(28, 'day')}, 'weightBased', {'perKgPerDose': 1.5, 'intervalHours': 8}, [d], dur={'min': 1, 'max': 5},
          notes=[note('۸ تا ۱۲ ساعت پس از بارگذاری اول شروع. جایگزین: ۲٫۲۵ mg/kg هر ۱۲ ساعت. حداکثر ۵ روز.', 'Start 8–12 h after the first loading dose. Alternative: 2.25 mg/kg every 12 h. Max 5 days.', [d]), PBIR])],
     [CI('ci', 'پورفیری حاد؛ حساسیت به فنوباربیتال یا باربیتورات‌ها.', 'Acute porphyria; hypersensitivity to phenobarbital or barbiturates.', [R(Sz, '4')])],
     exs=[ex('load', 'vial-100', {'perDose': 60, 'mlPerDose': 6}, ageDays=2, weightKg=3), ex('maint', 'vial-100', {'perDose': 4.5, 'mlPerDose': 0.45}, ageDays=3, weightKg=3)])

Bf = fda('beyfortus', 'FDA Beyfortus', 'Beyfortus (nirsevimab-alip) injection — Prescribing Information', sid('beyfortus')); d = R(Bf, '2.1, Table 1')
drug('nirsevimab', 'anti-infectives', 'نیرسویماب', 'Nirsevimab', T('آنتی‌بادی مونوکلونال ضد RSV', 'Anti-RSV monoclonal antibody'), [{'name': 'Beyfortus', 'market': 'US'}], ['beyfortus', 'بیفورتوس', 'نیرسویماب'],
     [inj('syr-50', '50 mg/0.5 mL prefilled syringe', 100, 1, Bf, '3', route='im'), inj('syr-100', '100 mg/mL prefilled syringe', 100, 1, Bf, '3', route='im')],
     [reg('first', 'rsv-prophylaxis', T('فصل اول RSV — زیر ۵ kg: ۵۰ mg؛ ۵ kg و بیشتر: ۱۰۰ mg عضلانی یک‌بار', 'First RSV season — <5 kg: 50 mg; ≥5 kg: 100 mg IM once'), {'maxAge': age(1, 'year')}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 4.99, 'perDose': 50, 'dosesPerDay': 1}, {'minWeightKg': 5, 'maxWeightKg': None, 'perDose': 100, 'dosesPerDay': 1}]}, [d], dur=ONE,
          notes=[note('متولدین فصل RSV: از بدو تولد. متولدین خارج فصل: یک بار پیش از شروع فصل. فصل دوم برای کودک پرخطر تا ۲۴ ماه: ۲۰۰ mg بدون توجه به وزن. با واکسن‌های کودکی همزمان (سرنگ و محل جدا).', 'Born during the RSV season: from birth. Born outside the season: once before the season starts. Second season for high-risk children up to 24 months: 200 mg regardless of weight. Can be given with childhood vaccines (separate syringe and site).', [d, R(Bf, '2.2')])])],
     [CI('hyper', 'سابقه حساسیت جدی (از جمله آنافیلاکسی) به نیرسویماب.', 'History of serious hypersensitivity (including anaphylaxis) to nirsevimab.', [R(Bf, '4')])],
     exs=[ex('first', 'syr-50', {'perDose': 50, 'mlPerDose': 0.5}, ageMonths=1, weightKg=4), ex('first', 'syr-100', {'perDose': 100, 'mlPerDose': 1}, ageMonths=5, weightKg=7)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
WOMEN = ['folic-acid', 'ferrous-sulfate', 'doxylamine-pyridoxine', 'methyldopa', 'labetalol', 'nifedipine', 'magnesium-sulfate', 'oxytocin', 'methylergonovine', 'carboprost', 'rho-d-immune-globulin', 'tdap-vaccine',
         'zuranolone', 'cabergoline', 'progesterone-vaginal', 'progesterone-oral', 'dydrogesterone', 'clomiphene', 'letrozole', 'metronidazole-vaginal', 'clindamycin-vaginal', 'miconazole-vaginal', 'terconazole', 'clotrimazole',
         'fluconazole', 'tranexamic-acid', 'mefenamic-acid', 'norethindrone', 'medroxyprogesterone', 'dienogest', 'elagolix', 'estradiol-oral', 'estradiol-vaginal', 'conjugated-estrogens', 'fezolinetant']
if not any(x['id'] == 'women-pregnancy' for x in c):
    c.append({'id': 'women-pregnancy', 'icon': '🤰', 'order': max(x['order'] for x in c) + 1, 'name': {'fa': 'بارداری و زنان', 'en': 'Pregnancy & women’s health'},
              'description': {'fa': 'بارداری، زایمان و پس از زایمان، عفونت‌های واژن، قاعدگی، آندومتریوز و یائسگی.', 'en': 'Pregnancy, delivery and postpartum, vaginal infections, menstruation, endometriosis and menopause.'}, 'drugs': []})
for col in c:
    if col['id'] == 'women-pregnancy':
        col['drugs'] += [x for x in WOMEN if x not in col['drugs'] and find(x)]
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['oxytocin', 'carboprost'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s5 ok')
