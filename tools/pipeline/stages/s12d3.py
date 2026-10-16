"""Stage 12d (part 3) — migraine (naratriptan, frovatriptan, lasmiditan, atogepant, fremanezumab, eptinezumab) and antidepressants (vilazodone, levomilnacipran, milnacipran, nefazodone)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
cap = lambda id, mg, src, label=None, sec='3': tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
TRIP_CI = lambda src: CI('ci', 'بیماری ایسکمیک کرونر یا وازواسپاسم کرونر (پرینزمتال)؛ WPW یا آریتمی مسیر فرعی؛ سابقه سکته، TIA یا میگرن همی‌پلژیک/بازیلار؛ بیماری عروق محیطی؛ بیماری ایسکمیک روده؛ فشار خون کنترل‌نشده؛ تریپتان یا ارگوت دیگر ظرف ۲۴ ساعت؛ حساسیت.',
    'Ischaemic coronary disease or coronary vasospasm (Prinzmetal); WPW or accessory-pathway arrhythmias; history of stroke, TIA or hemiplegic/basilar migraine; peripheral vascular disease; ischaemic bowel disease; uncontrolled hypertension; another triptan or ergot within 24 h; hypersensitivity.', [R(src, '4')])
TRIP_W = lambda src: W('ایسکمی و انفارکتوس قلب؛ آریتمی؛ احساس فشار قفسه سینه، گلو یا فک؛ رویداد عروق مغزی؛ سردرد ناشی از مصرف زیاد دارو؛ سندرم سروتونین؛ افزایش فشار خون.', 'Myocardial ischaemia and infarction; arrhythmias; chest/throat/jaw tightness; cerebrovascular events; medication-overuse headache; serotonin syndrome; increased blood pressure.', [R(src, '5')])
CGRP_W = lambda src: W('واکنش حساسیتی؛ یبوست با عوارض جدی؛ فشار خون بالا؛ پدیده رینود.', 'Hypersensitivity; constipation with serious complications; hypertension; Raynaud phenomenon.', [R(src, '5')])
SUI = lambda src, sec='Boxed Warning': W('هشدار جعبه‌ای: افزایش افکار و رفتار خودکشی در کودکان و جوانان — پایش بدتر شدن بالینی.', 'Boxed warning: increased suicidal thoughts and behaviours in children and young adults — monitor for clinical worsening.', [R(src, sec)])
MAOI = lambda src, days, sec='4': CI('maoi', f'مهارکننده MAO همزمان، ظرف ۱۴ روز پس از قطع آن، یا ظرف {days} روز پس از قطع این دارو؛ لینزولید یا متیلن بلو وریدی (سندرم سروتونین).', f'MAOIs concomitantly, within 14 days of stopping them, or within {days} days of stopping this drug; linezolid or IV methylene blue (serotonin syndrome).', [R(src, sec)])

Nr = fda('naratriptan', 'FDA Naratriptan', 'Naratriptan tablets 1/2.5 mg — Prescribing Information', sid('naratriptan'))
drug('naratriptan', 'nervous-system', 'ناراتریپتان', 'Naratriptan', T('تریپتان (آگونیست 5-HT1B/1D)', 'Triptan (5-HT1B/1D agonist)'), [{'name': 'Amerge', 'market': 'US'}], ['amerge', 'naramig', 'ناراتریپتان'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet', [R(Nr, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Nr, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن بزرگسال — ۱ یا ۲٫۵ mg', 'Acute migraine, adults — 1 or 2.5 mg'), A18, 'fixed', {'perDose': 1, 'perDoseMax': 2.5, 'dosesPerDay': 1}, [R(Nr, '2.1')],
          limits={'maxPerDay': 5, 'refs': [R(Nr, '2.1')]}, notes=[note('اگر بازگشت یا پاسخ نسبی: یک بار پس از ۴ ساعت تکرار؛ حداکثر ۵ mg در ۲۴ ساعت. نارسایی خفیف/متوسط کلیه یا کبد: شروع ۱ mg، حداکثر ۲٫۵ mg/روز.', 'If it returns or partial response: repeat once after 4 h; max 5 mg in 24 h. Mild/moderate renal or hepatic impairment: start 1 mg, max 2.5 mg/day.', [R(Nr, '2.1'), R(Nr, '2.2'), R(Nr, '2.3')])])],
     [TRIP_CI(Nr), CI('organ', 'نارسایی شدید کلیه (ClCr زیر ۱۵) یا کبد (Child-Pugh C).', 'Severe renal impairment (CrCl <15) or severe hepatic impairment (Child-Pugh C).', [R(Nr, '2.2'), R(Nr, '2.3')])], warn=[TRIP_W(Nr)],
     renal=[{'egfrBelow': 15, 'severity': 'block', 'text': T('ClCr زیر ۱۵: منع مصرف.', 'CrCl <15: contraindicated.'), 'refs': [R(Nr, '2.2')]}],
     exs=[ex('acute', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65)])

Fr = fda('frovatriptan', 'FDA Frovatriptan', 'Frovatriptan succinate tablets 2.5 mg — Prescribing Information', sid('frovatriptan'))
drug('frovatriptan', 'nervous-system', 'فرواتریپتان', 'Frovatriptan', T('تریپتان (آگونیست 5-HT1B/1D)', 'Triptan (5-HT1B/1D agonist)'), [{'name': 'Frova', 'market': 'US'}], ['frova', 'فروا', 'فرواتریپتان'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet', [R(Fr, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن بزرگسال — ۲٫۵ mg با مایعات', 'Acute migraine, adults — 2.5 mg with fluids'), A18, 'fixed', {'perDose': 2.5, 'dosesPerDay': 1}, [R(Fr, '2')],
          limits={'maxPerDay': 7.5, 'refs': [R(Fr, '2')]}, notes=[note('اگر پس از بهبود اولیه بازگشت: دوز دوم با دست‌کم ۲ ساعت فاصله؛ حداکثر ۳ قرص (۷٫۵ mg) در ۲۴ ساعت.', 'If it recurs after initial relief: second dose at least 2 h later; max 3 tablets (7.5 mg) in 24 h.', [R(Fr, '2')])])],
     [TRIP_CI(Fr)], warn=[TRIP_W(Fr)], exs=[ex('acute', 'tab-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65)])

Ry = fda('reyvow', 'FDA Reyvow', 'Reyvow (lasmiditan) tablets — Prescribing Information', sid('lasmiditan'))
drug('lasmiditan', 'nervous-system', 'لاسمیدیتان', 'Lasmiditan', T('آگونیست 5-HT1F (دیتان)', '5-HT1F agonist (ditan)'), [{'name': 'Reyvow', 'market': 'US'}], ['reyvow', 'ری‌وو', 'لاسمیدیتان'],
     [tab('tab-50', 50, '50 mg tablet', [R(Ry, '3')]), tab('tab-100', 100, '100 mg tablet', [R(Ry, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن بزرگسال — ۵۰، ۱۰۰ یا ۲۰۰ mg در صورت نیاز', 'Acute migraine, adults — 50, 100 or 200 mg as needed'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 200, 'dosesPerDay': 1}, [R(Ry, '2')],
          notes=[note('حداکثر یک دوز در ۲۴ ساعت؛ تا ۸ ساعت پس از مصرف رانندگی نکند. دوز دوم برای همان حمله مؤثر نیست.', 'No more than one dose in 24 h; do not drive for 8 h after. A second dose for the same attack is not effective.', [R(Ry, '2')])])],
     warn=[W('اختلال رانندگی؛ تضعیف CNS (سرگیجه، خواب‌آلودگی)؛ سندرم سروتونین؛ سردرد ناشی از مصرف زیاد دارو.', 'Driving impairment; CNS depression (dizziness, sedation); serotonin syndrome; medication-overuse headache.', [R(Ry, '5')])],
     exs=[ex('acute', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'upperPerDose': 200}, ageYears=35, weightKg=65)])

Qu = fda('qulipta', 'FDA Qulipta', 'Qulipta (atogepant) tablets — Prescribing Information', sid('atogepant'))
drug('atogepant', 'nervous-system', 'آتوجپانت', 'Atogepant', T('آنتاگونیست گیرنده CGRP (جپانت)', 'CGRP receptor antagonist (gepant)'), [{'name': 'Qulipta', 'market': 'US'}], ['qulipta', 'کولیپتا', 'آتوجپانت'],
     [tab('tab-60', 60, '60 mg tablet', [R(Qu, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Qu, '3')]), tab('tab-30', 30, '30 mg tablet', [R(Qu, '3')])],
     [reg('epi', 'migraine-prophylaxis', T('پیشگیری میگرن اپیزودیک بزرگسال — ۱۰، ۳۰ یا ۶۰ mg یک بار در روز', 'Episodic migraine prevention, adults — 10, 30 or 60 mg once daily'), A18, 'fixed', {'perDose': 10, 'perDoseMax': 60, 'dosesPerDay': 1}, [R(Qu, '2.1')],
          notes=[note('مهارکننده قوی CYP3A4: ۱۰ mg؛ القاگر قوی CYP3A4: ۶۰ mg (در میگرن مزمن توصیه نمی‌شود). سایر تداخل‌ها طبق جدول ۱.', 'Strong CYP3A4 inhibitors: 10 mg; strong CYP3A4 inducers: 60 mg (not recommended in chronic migraine). Other interactions per Table 1.', [R(Qu, '2.2, Table 1')])]),
      reg('chronic', 'migraine-prophylaxis', T('پیشگیری میگرن مزمن بزرگسال — ۶۰ mg یک بار در روز', 'Chronic migraine prevention, adults — 60 mg once daily'), A18, 'fixed', {'perDose': 60, 'dosesPerDay': 1}, [R(Qu, '2.1')], allowed=['tab-60'])],
     [CI('hyper', 'سابقه حساسیت به آتوجپانت (آنافیلاکسی، تنگی نفس).', 'History of hypersensitivity to atogepant (anaphylaxis, dyspnoea).', [R(Qu, '4')])],
     warn=[W('واکنش حساسیتی.', 'Hypersensitivity reactions.', [R(Qu, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰ یا ESRD: اپیزودیک ۱۰ mg؛ مزمن توصیه نمی‌شود.', 'CrCl <30 or ESRD: episodic 10 mg; chronic not recommended.'), 'refs': [R(Qu, '2.2')]}],
     exs=[ex('epi', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65), ex('chronic', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65)])

Aj = fda('ajovy', 'FDA Ajovy', 'Ajovy (fremanezumab-vfrm) injection — Prescribing Information', sid('fremanezumab'))
drug('fremanezumab', 'nervous-system', 'فرمانزوماب', 'Fremanezumab', T('آنتی‌بادی ضد CGRP', 'Anti-CGRP monoclonal antibody'), [{'name': 'Ajovy', 'market': 'US'}], ['ajovy', 'آجووی', 'فرمانزوماب'],
     [form('pfs-225', 'injection', 'sc', '225 mg/1.5 mL prefilled syringe or autoinjector', 225, 'mg', [R(Aj, '3')], vol=1.5)],
     [reg('m', 'migraine-prophylaxis', T('پیشگیری میگرن — ۲۲۵ mg زیرجلدی ماهانه (بزرگسال؛ کودک ۶ تا ۱۷ سال ≥۴۵ kg برای اپیزودیک)', 'Migraine prevention — 225 mg SC monthly (adults; children 6–17 y ≥45 kg for episodic)'), {'minAge': age(6, 'year'), 'minWeightKg': 45}, 'fixed', {'perDose': 225, 'dosesPerDay': 1}, [R(Aj, '2.1')], dur=ONE),
      reg('q', 'migraine-prophylaxis', T('پیشگیری میگرن بزرگسال — ۶۷۵ mg هر ۳ ماه (سه تزریق پشت سر هم ۲۲۵ mg)', 'Migraine prevention, adults — 675 mg every 3 months (three consecutive 225 mg injections)'), A18, 'fixed', {'perDose': 675, 'dosesPerDay': 1}, [R(Aj, '2.1')], dur=ONE)],
     [CI('hyper', 'حساسیت جدی به فرمانزوماب (آنافیلاکسی، آنژیوادم).', 'Serious hypersensitivity to fremanezumab (anaphylaxis, angioedema).', [R(Aj, '4')])], warn=[CGRP_W(Aj)],
     exs=[ex('m', 'pfs-225', {'perDose': 225, 'mlPerDose': 1.5}, ageYears=35, weightKg=65), ex('q', 'pfs-225', {'perDose': 675, 'mlPerDose': 4.5}, ageYears=35, weightKg=65)])

Vy = fda('vyepti', 'FDA Vyepti', 'Vyepti (eptinezumab-jjmr) injection — Prescribing Information', sid('eptinezumab'))
drug('eptinezumab', 'nervous-system', 'اپتینزوماب', 'Eptinezumab', T('آنتی‌بادی ضد CGRP (وریدی)', 'Anti-CGRP monoclonal antibody (IV)'), [{'name': 'Vyepti', 'market': 'US'}], ['vyepti', 'وایپتی', 'اپتینزوماب'],
     [form('vial-100', 'injection', 'iv', '100 mg/mL vial', 100, 'mg', [R(Vy, '3')], vol=1)],
     [reg('iv', 'migraine-prophylaxis', T('پیشگیری میگرن بزرگسال — ۱۰۰ mg انفوزیون وریدی ۳۰ دقیقه هر ۳ ماه (برخی ۳۰۰ mg)', 'Migraine prevention, adults — 100 mg IV infusion over 30 min every 3 months (some 300 mg)'), A18, 'fixed', {'perDose': 100, 'perDoseMax': 300, 'dosesPerDay': 1}, [R(Vy, '2.1')], dur=ONE,
          notes=[note('فقط در ۱۰۰ mL سرم نرمال سالین رقیق شود.', 'Dilute only in 100 mL 0.9% sodium chloride.', [R(Vy, '2.2')])])],
     [CI('hyper', 'حساسیت جدی به اپتینزوماب.', 'Serious hypersensitivity to eptinezumab.', [R(Vy, '4')])], warn=[CGRP_W(Vy)],
     exs=[ex('iv', 'vial-100', {'perDose': 100, 'mlPerDose': 1, 'upperPerDose': 300}, ageYears=35, weightKg=65)])

Vi = fda('viibryd', 'FDA Viibryd', 'Viibryd (vilazodone) tablets — Prescribing Information', sid('vilazodone'))
drug('vilazodone', 'nervous-system', 'ویلازودون', 'Vilazodone', T('ضدافسردگی (SSRI + آگونیست نسبی 5-HT1A)', 'Antidepressant (SSRI + 5-HT1A partial agonist)'), [{'name': 'Viibryd', 'market': 'US'}], ['viibryd', 'ویبرید', 'ویلازودون'],
     [tab('tab-20', 20, '20 mg tablet', [R(Vi, '3')]), tab('tab-40', 40, '40 mg tablet', [R(Vi, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Vi, '3')])],
     [reg('mdd', 'mdd', T('افسردگی اساسی بزرگسال — هدف ۲۰ تا ۴۰ mg یک بار با غذا', 'Major depressive disorder, adults — target 20–40 mg once daily with food'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [R(Vi, '2.1')],
          notes=[note('شروع ۱۰ mg ۷ روز، سپس ۲۰ mg؛ پس از دست‌کم ۷ روز تا ۴۰ mg. پیش از شروع اختلال دوقطبی بررسی شود. قطع تدریجی.', 'Start 10 mg for 7 days, then 20 mg; after ≥7 days up to 40 mg. Screen for bipolar disorder first. Taper when stopping.', [R(Vi, '2.1'), R(Vi, '2.2')])])],
     [MAOI(Vi, 14)], warn=[SUI(Vi), W('سندرم سروتونین؛ تشنج؛ اختلال عملکرد جنسی.', 'Serotonin syndrome; seizures; sexual dysfunction.', [R(Vi, '5')])],
     exs=[ex('mdd', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1, 'upperPerDose': 40}, ageYears=40, weightKg=70)])

Fz = fda('fetzima', 'FDA Fetzima', 'Fetzima (levomilnacipran) extended-release capsules — Prescribing Information', sid('levomilnacipran'))
drug('levomilnacipran', 'nervous-system', 'لِوومیلناسیپران', 'Levomilnacipran', T('SNRI', 'SNRI'), [{'name': 'Fetzima', 'market': 'US'}], ['fetzima', 'فتزیما', 'لووميلناسیپران', 'لوومیلناسیپران'],
     [cap('er-40', 40, Fz, '40 mg ER capsule (swallow whole)'), cap('er-20', 20, Fz, '20 mg ER capsule (swallow whole)'), cap('er-80', 80, Fz, '80 mg ER capsule (swallow whole)'), cap('er-120', 120, Fz, '120 mg ER capsule (swallow whole)')],
     [reg('mdd', 'mdd', T('افسردگی اساسی بزرگسال — ۴۰ تا ۱۲۰ mg یک بار در روز', 'Major depressive disorder, adults — 40–120 mg once daily'), A18, 'fixed', {'perDose': 40, 'perDoseMax': 120, 'dosesPerDay': 1}, [R(Fz, '2.1')],
          notes=[note('شروع ۲۰ mg دو روز، سپس ۴۰ mg؛ گام ۴۰ mg با فاصله ۲ روز یا بیشتر. کپسول باز یا جویده نشود. با مهارکننده قوی CYP3A4 حداکثر ۸۰ mg. قطع تدریجی.', 'Start 20 mg for 2 days, then 40 mg; 40 mg steps at ≥2-day intervals. Do not open or chew. With strong CYP3A4 inhibitors max 80 mg. Taper when stopping.', [R(Fz, '2.1'), R(Fz, '2.6'), R(Fz, '2.4')])])],
     [CI('ci', 'حساسیت به لووميلناسیپران یا میلناسیپران؛ مهارکننده MAO همزمان، ظرف ۷ روز پس از قطع این دارو یا ۱۴ روز پس از قطع MAOI؛ لینزولید یا متیلن بلو وریدی.', 'Hypersensitivity to levomilnacipran or milnacipran; MAOIs concomitantly, within 7 days of stopping this drug or 14 days of stopping the MAOI; linezolid or IV methylene blue.', [R(Fz, '4')])],
     warn=[SUI(Fz), W('سندرم سروتونین؛ افزایش فشار خون و ضربان؛ خونریزی؛ گلوکوم زاویه بسته؛ احتباس ادرار؛ هیپوناترمی.', 'Serotonin syndrome; raised blood pressure and heart rate; bleeding; angle-closure glaucoma; urinary retention; hyponatraemia.', [R(Fz, '5')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr ۳۰ تا ۵۹: حداکثر ۸۰ mg؛ ۱۵ تا ۲۹: حداکثر ۴۰ mg. ESRD توصیه نمی‌شود.', 'CrCl 30–59: max 80 mg; 15–29: max 40 mg. ESRD not recommended.'), 'refs': [R(Fz, '2.3')]}],
     exs=[ex('mdd', 'er-40', {'perDose': 40, 'tabletsPerDoseRounded': 1, 'upperPerDose': 120}, ageYears=40, weightKg=70)])

Sv = fda('savella', 'FDA Savella', 'Savella (milnacipran) tablets — Prescribing Information', sid('milnacipran'))
drug('milnacipran', 'nervous-system', 'میلناسیپران', 'Milnacipran', T('SNRI', 'SNRI'), [{'name': 'Savella', 'market': 'US'}], ['savella', 'ساولا', 'ixel', 'میلناسیپران'],
     [tab('tab-50', 50, '50 mg tablet', [R(Sv, '3')]), tab('tab-25', 25, '25 mg tablet', [R(Sv, '3')]), tab('tab-100', 100, '100 mg tablet', [R(Sv, '3')]), tab('tab-12-5', 12.5, '12.5 mg tablet', [R(Sv, '3')])],
     [reg('fm', 'fibromyalgia', T('فیبرومیالژی بزرگسال — ۵۰ mg دو بار در روز (تا ۱۰۰ mg دو بار)', 'Fibromyalgia, adults — 50 mg twice daily (up to 100 mg twice daily)'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 2}, [R(Sv, '2.1')],
          notes=[note('تیتراسیون: روز ۱: ۱۲٫۵ mg؛ روز ۲–۳: ۱۲٫۵ mg دو بار؛ روز ۴–۷: ۲۵ mg دو بار؛ سپس ۵۰ mg دو بار. با غذا بهتر تحمل می‌شود. قطع تدریجی.', 'Titration: day 1: 12.5 mg; days 2–3: 12.5 mg twice; days 4–7: 25 mg twice; then 50 mg twice daily. Better tolerated with food. Taper when stopping.', [R(Sv, '2.1'), R(Sv, '2.4')])])],
     [MAOI(Sv, 5, '4.1')],
     warn=[W('هشدار جعبه‌ای: خطر خودکشی با ضدافسردگی‌ها در کودکان و جوانان؛ برای افسردگی در آمریکا تأیید نشده.', 'Boxed warning: suicidality with antidepressants in children and young adults; not approved for depression in the US.', [R(Sv, 'Boxed Warning')]),
           W('سندرم سروتونین؛ افزایش فشار و ضربان؛ تشنج؛ سمیت کبد؛ هیپوناترمی؛ خونریزی؛ فعال شدن مانیا.', 'Serotonin syndrome; raised blood pressure and heart rate; seizures; hepatotoxicity; hyponatraemia; bleeding; activation of mania.', [R(Sv, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr ۵ تا ۲۹: نگهدارنده ۵۰٪ کم (۲۵ mg دو بار)؛ ESRD توصیه نمی‌شود.', 'CrCl 5–29: reduce maintenance by 50% (25 mg twice daily); ESRD not recommended.'), 'refs': [R(Sv, '2.2')]}],
     exs=[ex('fm', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'upperPerDose': 100}, ageYears=45, weightKg=70)])

Nz = fda('nefazodone', 'FDA Nefazodone', 'Nefazodone hydrochloride tablets USP (Teva) — Prescribing Information', sid('nefazodone')); d = R(Nz, 'Dosage and Administration')
drug('nefazodone', 'nervous-system', 'نفازودون', 'Nefazodone', T('ضدافسردگی فنیل‌پیپرازین', 'Phenylpiperazine antidepressant'), [{'name': 'Nefazodone', 'market': 'US'}], ['serzone', 'نفازودون'],
     [tab('tab-100', 100, '100 mg tablet (scored)', [R(Nz, 'How Supplied')], scored=True), tab('tab-50', 50, '50 mg tablet', [R(Nz, 'How Supplied')])],
     [reg('mdd', 'mdd', T('افسردگی اساسی بزرگسال — شروع ۱۰۰ mg دو بار در روز؛ محدوده مؤثر ۳۰۰ تا ۶۰۰ mg/روز', 'Major depressive disorder, adults — start 100 mg twice daily; effective range 300–600 mg/day'), A18, 'fixed', {'perDose': 100, 'perDoseMax': 300, 'dosesPerDay': 2}, [d],
          notes=[note('افزایش ۱۰۰ تا ۲۰۰ mg/روز با فاصله دست‌کم ۱ هفته. سالمند یا ناتوان: شروع ۵۰ mg دو بار. خطر نارسایی کبد در انتخاب دارو لحاظ شود.', 'Increase by 100–200 mg/day at intervals of at least 1 week. Elderly or debilitated: start 50 mg twice daily. Weigh hepatic failure risk when choosing.', [d])])],
     [CI('ci', 'ترفنادین، آستمیزول، سیزاپراید، پیموزاید یا کاربامازپین همزمان؛ سابقه قطع نفازودون به‌دلیل آسیب کبدی؛ حساسیت به نفازودون یا ضدافسردگی‌های فنیل‌پیپرازین. تریازولام در بیشتر بیماران پرهیز شود.', 'Concomitant terfenadine, astemizole, cisapride, pimozide or carbamazepine; prior withdrawal from nefazodone for liver injury; hypersensitivity to nefazodone or phenylpiperazine antidepressants. Avoid triazolam in most patients.', [R(Nz, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: نارسایی کبد تهدیدکننده حیات (حدود ۱ مورد مرگ یا پیوند در ۲۵۰ تا ۳۰۰ هزار بیمار-سال)؛ خودکشی در کودکان و جوانان.', 'Boxed warning: life-threatening hepatic failure (about 1 death or transplant per 250,000–300,000 patient-years); suicidality in children and young adults.', [R(Nz, 'Boxed Warning')])],
     exs=[ex('mdd', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1, 'upperPerDose': 300}, ageYears=40, weightKg=70)])
print('s12d3 ok')
