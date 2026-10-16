"""Stage 12d (part 4) — MAOIs (phenelzine, tranylcypromine), hypnotics (eszopiclone, zaleplon, ramelteon, lemborexant, daridorexant) and ADHD (viloxazine, dexmethylphenidate)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
cap = lambda id, mg, src, label=None, sec='3': tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
CSB = lambda src, sec='Boxed Warning': W('هشدار جعبه‌ای: رفتارهای پیچیده خواب (راه رفتن یا رانندگی در خواب) گاه با آسیب جدی یا مرگ — در صورت بروز فوراً قطع شود.', 'Boxed warning: complex sleep behaviours (sleep-walking, sleep-driving) sometimes causing serious injury or death — stop immediately if they occur.', [R(src, sec)])
DORA_W = lambda src: W('تضعیف CNS و اختلال عملکرد روز بعد؛ فلج خواب و توهم هیپناگوژیک؛ رفتارهای پیچیده خواب؛ اختلال تنفسی؛ تشدید افسردگی و افکار خودکشی.', 'CNS depression and next-day impairment; sleep paralysis and hypnagogic hallucinations; complex sleep behaviours; compromised respiratory function; worsening depression and suicidal ideation.', [R(src, '5')])

Nd = fda('nardil', 'FDA Nardil', 'Nardil (phenelzine sulfate) tablets 15 mg — Prescribing Information', sid('phenelzine')); d = R(Nd, 'Dosage and Administration')
drug('phenelzine', 'nervous-system', 'فنلزین', 'Phenelzine', T('مهارکننده MAO (غیرانتخابی)', 'MAO inhibitor (non-selective)'), [{'name': 'Nardil', 'market': 'US'}], ['nardil', 'ناردیل', 'فنلزین'],
     [tab('tab-15', 15, '15 mg tablet', [R(Nd, 'How Supplied')])],
     [reg('dep', 'mdd', T('افسردگی (آتیپیک، غیرآندوژن یا نوروتیک) بزرگسال — شروع ۱۵ mg سه بار در روز', 'Depression (atypical, non-endogenous or neurotic), adults — start 15 mg three times daily'), A18, 'fixed', {'perDose': 15, 'dosesPerDay': 3}, [d],
          limits={'maxPerDay': 90, 'refs': [d]}, notes=[note('به‌سرعت تا دست‌کم ۶۰ mg/روز؛ گاه تا ۹۰ mg/روز. پاسخ ممکن است ۴ هفته با ۶۰ mg طول بکشد. نگهدارنده تا ۱۵ mg روزانه یا یک روز در میان، با کاهش آهسته.', 'Increase fairly rapidly to at least 60 mg/day; up to 90 mg/day if needed. Response may take 4 weeks at 60 mg. Maintenance as low as 15 mg daily or every other day, reduced slowly.', [d])])],
     [CI('ci', 'حساسیت؛ فئوکروموسیتوم؛ نارسایی احتقانی قلب؛ نارسایی شدید یا بیماری کلیه؛ سابقه بیماری کبد یا آزمایش کبد غیرطبیعی؛ داروهای سمپاتومیمتیک (آمفتامین، کوکائین، متیل‌فنیدیت، دوپامین، اپی‌نفرین…) و غذای پرتیرامین (بحران فشار خون).',
         'Hypersensitivity; pheochromocytoma; congestive heart failure; severe renal impairment or renal disease; history of liver disease or abnormal liver tests; sympathomimetic drugs (amphetamines, cocaine, methylphenidate, dopamine, epinephrine…) and high-tyramine foods (hypertensive crisis).', [R(Nd, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: خودکشی با ضدافسردگی‌ها در کودکان، نوجوانان و جوانان.', 'Boxed warning: suicidality with antidepressants in children, adolescents and young adults.', [R(Nd, 'Warnings')])],
     exs=[ex('dep', 'tab-15', {'perDose': 15, 'tabletsPerDoseRounded': 1, 'perDay': 45}, ageYears=40, weightKg=70)])

Pn = fda('tranylcypromine', 'FDA Tranylcypromine', 'Tranylcypromine sulfate tablets 10 mg — Prescribing Information', sid('tranylcypromine'))
drug('tranylcypromine', 'nervous-system', 'ترانیل‌سیپرومین', 'Tranylcypromine', T('مهارکننده MAO (غیرانتخابی)', 'MAO inhibitor (non-selective)'), [{'name': 'Parnate', 'market': 'US'}], ['parnate', 'پارنیت', 'ترانیلسیپرومین'],
     [tab('tab-10', 10, '10 mg tablet', [R(Pn, '3')])],
     [reg('mdd', 'mdd', T('افسردگی اساسی بدون پاسخ کافی به سایر ضدافسردگی‌ها، بزرگسال — ۳۰ mg/روز در دوزهای تقسیمی', 'Major depressive disorder without adequate response to other antidepressants, adults — 30 mg/day in divided doses'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 3}, [R(Pn, '2.1')],
          limits={'maxPerDay': 60, 'refs': [R(Pn, '2.1')]}, notes=[note('اگر پاسخ ناکافی: هر ۱ تا ۳ هفته ۱۰ mg/روز افزایش تا حداکثر ۳۰ mg دو بار. پیش از شروع فشار خون و سابقه مانیا. قطع تدریجی (دلیریوم با قطع ناگهانی). فاصله زمانی با سایر ضدافسردگی‌ها طبق ۲٫۲.', 'If inadequate: +10 mg/day every 1–3 weeks to max 30 mg twice daily. Check BP and history of mania first. Taper (delirium on abrupt stop). Washout with other antidepressants per 2.2.', [R(Pn, '2.1'), R(Pn, '2.4'), R(Pn, '2.3'), R(Pn, '2.2')])])],
     [CI('ci', 'سایر MAOIها، SSRI، SNRI، ضدافسردگی سه‌حلقه‌ای، سمپاتومیمتیک‌ها و بسیاری داروهای دیگر (جدول ۱ برچسب)؛ فئوکروموسیتوم یا پاراگانگلیوم ترشح‌کننده کاتکول‌آمین.', 'Other MAOIs, SSRIs, SNRIs, tricyclics, sympathomimetics and many other drugs (label Table 1); pheochromocytoma or catecholamine-releasing paraganglioma.', [R(Pn, '4')])],
     warn=[W('هشدار جعبه‌ای: خودکشی در کودکان و جوانان؛ بحران فشار خون با مصرف زیاد تیرامین (پنیر کهنه، گوشت فرآوری‌شده…).', 'Boxed warning: suicidality in children and young adults; hypertensive crisis with significant tyramine intake (aged cheese, cured meats…).', [R(Pn, 'Boxed Warning')]),
           W('سندرم سروتونین؛ مانیا؛ افت فشار؛ سمیت کبد؛ تشنج؛ هیپوگلیسمی در دیابت.', 'Serotonin syndrome; mania; hypotension; hepatotoxicity; seizures; hypoglycaemia in diabetics.', [R(Pn, '5')])],
     exs=[ex('mdd', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'perDay': 30}, ageYears=40, weightKg=70)])

Lu = fda('lunesta', 'FDA Lunesta', 'Lunesta (eszopiclone) tablets — Prescribing Information', sid('eszopiclone'))
drug('eszopiclone', 'nervous-system', 'اس‌زوپیکلون', 'Eszopiclone', T('خواب‌آور غیربنزودیازپینی (Z-drug)', 'Non-benzodiazepine hypnotic (Z-drug)'), [{'name': 'Lunesta', 'market': 'US'}], ['lunesta', 'لونستا', 'اسزوپیکلون'],
     [tab('tab-1', 1, '1 mg tablet', [R(Lu, '3')]), tab('tab-2', 2, '2 mg tablet', [R(Lu, '3')]), tab('tab-3', 3, '3 mg tablet', [R(Lu, '3')])],
     [reg('ins', 'insomnia', T('بی‌خوابی بزرگسال — ۱ mg درست پیش از خواب (تا ۳ mg)', 'Insomnia, adults — 1 mg immediately before bedtime (up to 3 mg)'), A18, 'fixed', {'perDose': 1, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Lu, '2.1')],
          notes=[note('دست‌کم ۷ تا ۸ ساعت تا بیداری. سالمند/ناتوان، نارسایی شدید کبد یا مهارکننده قوی CYP3A4: حداکثر ۲ mg. نه با یا بلافاصله پس از غذای پرچرب.', 'At least 7–8 h before planned awakening. Elderly/debilitated, severe hepatic impairment or strong CYP3A4 inhibitors: max 2 mg. Not with or right after a heavy meal.', [R(Lu, '2'), R(Lu, '2.2'), R(Lu, '2.3'), R(Lu, '2.5')])])],
     [CI('ci', 'سابقه رفتار پیچیده خواب با اس‌زوپیکلون؛ حساسیت (آنافیلاکسی، آنژیوادم).', 'Prior complex sleep behaviours with eszopiclone; hypersensitivity (anaphylaxis, angioedema).', [R(Lu, '4')])],
     warn=[CSB(Lu), W('تضعیف CNS و اختلال رانندگی روز بعد (به‌ویژه ۲ یا ۳ mg)؛ رفتار غیرطبیعی؛ علائم قطع.', 'CNS depression and next-day driving impairment (especially 2 or 3 mg); abnormal behaviour; withdrawal effects.', [R(Lu, '5')])],
     exs=[ex('ins', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1, 'upperPerDose': 3}, ageYears=40, weightKg=70)])

Zl = fda('zaleplon', 'FDA Zaleplon', 'Zaleplon capsules USP 5/10 mg — Prescribing Information', sid('zaleplon')); d = R(Zl, 'Dosage and Administration')
drug('zaleplon', 'nervous-system', 'زالپلون', 'Zaleplon', T('خواب‌آور غیربنزودیازپینی (Z-drug)', 'Non-benzodiazepine hypnotic (Z-drug)'), [{'name': 'Sonata', 'market': 'US'}], ['sonata', 'سوناتا', 'زالپلون'],
     [cap('cap-10', 10, Zl, sec='How Supplied'), cap('cap-5', 5, Zl, sec='How Supplied')],
     [reg('ins', 'insomnia', T('بی‌خوابی (کوتاه‌مدت) بزرگسال — ۱۰ mg درست پیش از خواب', 'Insomnia (short-term), adults — 10 mg immediately before bedtime'), {'minAge': age(18, 'year'), 'maxAge': age(65, 'year')}, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [d],
          notes=[note('یا پس از رفتن به رختخواب و ناتوانی در خوابیدن. وزن کم: ۵ mg ممکن است کافی باشد. بیش از ۲۰ mg توصیه نمی‌شود.', 'Or after going to bed with difficulty falling asleep. Low weight: 5 mg may suffice. Not above 20 mg.', [d])]),
      reg('eld', 'insomnia', T('سالمند یا ناتوان — ۵ mg', 'Elderly or debilitated — 5 mg'), {'minAge': age(65, 'year')}, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(Zl, 'Precautions')])],
     [CI('ci', 'سابقه رفتار پیچیده خواب با زالپلون؛ حساسیت.', 'Prior complex sleep behaviours with zaleplon; hypersensitivity.', [R(Zl, 'Contraindications')])], warn=[CSB(Zl)],
     exs=[ex('ins', 'cap-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'upperPerDose': 20}, ageYears=40, weightKg=70), ex('eld', 'cap-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=72, weightKg=65)])

Rz = fda('rozerem', 'FDA Rozerem', 'Rozerem (ramelteon) tablets 8 mg — Prescribing Information', sid('ramelteon'))
drug('ramelteon', 'nervous-system', 'راملتئون', 'Ramelteon', T('آگونیست گیرنده ملاتونین', 'Melatonin receptor agonist'), [{'name': 'Rozerem', 'market': 'US'}], ['rozerem', 'روزرم', 'راملتئون'],
     [tab('tab-8', 8, '8 mg tablet', [R(Rz, '3')])],
     [reg('ins', 'insomnia', T('بی‌خوابی (دشواری به خواب رفتن) بزرگسال — ۸ mg ظرف ۳۰ دقیقه پیش از خواب', 'Insomnia (sleep onset), adults — 8 mg within 30 min of going to bed'), A18, 'fixed', {'perDose': 8, 'dosesPerDay': 1}, [R(Rz, '2.1')],
          limits={'maxPerDay': 8, 'refs': [R(Rz, '2.1')]}, notes=[note('نه با غذای پرچرب. نارسایی شدید کبد توصیه نمی‌شود. با مهارکننده‌های CYP1A2 احتیاط.', 'Not with a high-fat meal. Not recommended in severe hepatic impairment. Caution with CYP1A2 inhibitors.', [R(Rz, '2.1'), R(Rz, '2.2'), R(Rz, '2.3')])])],
     [CI('ci', 'سابقه آنژیوادم با راملتئون؛ فلووکسامین همزمان.', 'History of angioedema with ramelteon; concomitant fluvoxamine.', [R(Rz, '4')])],
     warn=[W('آنافیلاکسی و آنژیوادم؛ تفکر و رفتار غیرطبیعی؛ اثرات تولیدمثلی (پرولاکتین، تستوسترون).', 'Anaphylaxis and angioedema; abnormal thinking and behaviour; reproductive effects (prolactin, testosterone).', [R(Rz, '5')])],
     exs=[ex('ins', 'tab-8', {'perDose': 8, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Dv = fda('dayvigo', 'FDA Dayvigo', 'Dayvigo (lemborexant) tablets — Prescribing Information', sid('lemborexant'))
drug('lemborexant', 'nervous-system', 'لمبورکسانت', 'Lemborexant', T('آنتاگونیست گیرنده اورکسین (DORA)', 'Dual orexin receptor antagonist'), [{'name': 'Dayvigo', 'market': 'US'}], ['dayvigo', 'دیویگو', 'لمبورکسانت'],
     [tab('tab-5', 5, '5 mg tablet', [R(Dv, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Dv, '3')])],
     [reg('ins', 'insomnia', T('بی‌خوابی بزرگسال — ۵ mg درست پیش از خواب (تا ۱۰ mg)', 'Insomnia, adults — 5 mg immediately before bedtime (up to 10 mg)'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 1}, [R(Dv, '2.1')],
          notes=[note('حداکثر یک بار در شب، دست‌کم ۷ ساعت تا بیداری. مهارکننده متوسط/قوی CYP3A یا القاگر: پرهیز؛ مهارکننده ضعیف: حداکثر ۵ mg. نارسایی متوسط کبد حداکثر ۵ mg؛ شدید توصیه نمی‌شود.', 'No more than once a night, ≥7 h before awakening. Moderate/strong CYP3A inhibitors or inducers: avoid; weak inhibitors: max 5 mg. Moderate hepatic impairment max 5 mg; severe not recommended.', [R(Dv, '2.1'), R(Dv, '2.2'), R(Dv, '2.3')])])],
     [CI('narc', 'نارکولپسی.', 'Narcolepsy.', [R(Dv, '4')])], warn=[DORA_W(Dv)],
     exs=[ex('ins', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 10}, ageYears=40, weightKg=70)])

Qv = fda('quviviq', 'FDA Quviviq', 'Quviviq (daridorexant) tablets — Prescribing Information', sid('daridorexant'))
drug('daridorexant', 'nervous-system', 'داریدورکسانت', 'Daridorexant', T('آنتاگونیست گیرنده اورکسین (DORA)', 'Dual orexin receptor antagonist'), [{'name': 'Quviviq', 'market': 'US'}], ['quviviq', 'کوویویک', 'داریدورکسانت'],
     [tab('tab-25', 25, '25 mg tablet', [R(Qv, '3')]), tab('tab-50', 50, '50 mg tablet', [R(Qv, '3')])],
     [reg('ins', 'insomnia', T('بی‌خوابی بزرگسال — ۲۵ تا ۵۰ mg ظرف ۳۰ دقیقه پیش از خواب', 'Insomnia, adults — 25–50 mg within 30 min before bedtime'), A18, 'fixed', {'perDose': 25, 'perDoseMax': 50, 'dosesPerDay': 1}, [R(Qv, '2.1')],
          notes=[note('حداکثر یک بار در شب، دست‌کم ۷ ساعت تا بیداری. نارسایی متوسط کبد حداکثر ۲۵ mg؛ شدید توصیه نمی‌شود.', 'No more than once a night, ≥7 h before awakening. Moderate hepatic impairment max 25 mg; severe not recommended.', [R(Qv, '2.1'), R(Qv, '2.3')])])],
     [CI('ci', 'نارکولپسی؛ حساسیت به داریدورکسانت (آنژیوادم).', 'Narcolepsy; hypersensitivity to daridorexant (angioedema).', [R(Qv, '4')])], warn=[DORA_W(Qv)],
     exs=[ex('ins', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1, 'upperPerDose': 50}, ageYears=40, weightKg=70)])

Qb = fda('qelbree', 'FDA Qelbree', 'Qelbree (viloxazine extended-release capsules) — Prescribing Information', sid('viloxazine'))
drug('viloxazine', 'nervous-system', 'ویلوکسازین', 'Viloxazine', T('مهارکننده انتخابی بازجذب نوراپی‌نفرین (غیرمحرک)', 'Selective norepinephrine reuptake inhibitor (non-stimulant)'), [{'name': 'Qelbree', 'market': 'US'}], ['qelbree', 'کلبری', 'ویلوکسازین'],
     [cap('er-100', 100, Qb, '100 mg ER capsule'), cap('er-200', 200, Qb, '200 mg ER capsule'), cap('er-150', 150, Qb, '150 mg ER capsule')],
     [reg('c6', 'adhd', T('ADHD کودک ۶ تا ۱۱ سال — شروع ۱۰۰ mg یک بار؛ هفتگی ۱۰۰ mg تا حداکثر ۴۰۰ mg', 'ADHD, children 6–11 y — start 100 mg once daily; +100 mg weekly to max 400 mg'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 100, 'perDoseMax': 400, 'dosesPerDay': 1}, [R(Qb, '2.2')]),
      reg('c12', 'adhd', T('ADHD نوجوان ۱۲ تا ۱۷ سال — شروع ۲۰۰ mg؛ پس از ۱ هفته تا ۴۰۰ mg', 'ADHD, adolescents 12–17 y — start 200 mg; after 1 week up to 400 mg'), {'minAge': age(12, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 200, 'perDoseMax': 400, 'dosesPerDay': 1}, [R(Qb, '2.2')]),
      reg('adult', 'adhd', T('ADHD بزرگسال — شروع ۲۰۰ mg؛ هفتگی ۲۰۰ mg تا حداکثر ۶۰۰ mg', 'ADHD, adults — start 200 mg; +200 mg weekly to max 600 mg'), A18, 'fixed', {'perDose': 200, 'perDoseMax': 600, 'dosesPerDay': 1}, [R(Qb, '2.2')],
          notes=[note('کپسول کامل بلعیده شود یا محتویات روی پوره سیب/پودینگ؛ نجوید. پیش از شروع ضربان و فشار و سابقه خودکشی/دوقطبی.', 'Swallow whole or sprinkle on applesauce/pudding; do not chew. Check HR/BP and history of suicide/bipolar first.', [R(Qb, '2.3'), R(Qb, '2.1')])])],
     [CI('ci', 'MAOI همزمان یا ظرف ۱۴ روز (بحران فشار خون)؛ سوبستراهای حساس یا با دامنه باریک CYP1A2 (مثل تیزانیدین، تئوفیلین).', 'MAOIs concomitantly or within 14 days (hypertensive crisis); sensitive or narrow-range CYP1A2 substrates (e.g. tizanidine, theophylline).', [R(Qb, '4')])],
     warn=[W('هشدار جعبه‌ای: افکار و رفتار خودکشی بیشتر از دارونما.', 'Boxed warning: higher rates of suicidal thoughts and behaviour than placebo.', [R(Qb, 'Boxed Warning')]), W('افزایش فشار و ضربان؛ مانیا؛ خواب‌آلودگی.', 'Increased blood pressure and heart rate; mania; somnolence.', [R(Qb, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('eGFR زیر ۳۰: شروع ۱۰۰ mg، حداکثر ۲۰۰ mg.', 'eGFR <30: start 100 mg, max 200 mg.'), 'refs': [R(Qb, '2.4')]}],
     exs=[ex('c6', 'er-100', {'perDose': 100, 'tabletsPerDoseRounded': 1, 'upperPerDose': 400}, ageYears=8, weightKg=25), ex('c12', 'er-200', {'perDose': 200, 'tabletsPerDoseRounded': 1, 'upperPerDose': 400}, ageYears=14, weightKg=50),
          ex('adult', 'er-200', {'perDose': 200, 'tabletsPerDoseRounded': 1, 'upperPerDose': 600}, ageYears=30, weightKg=70)])

Fo = fda('focalin', 'FDA Focalin', 'Focalin (dexmethylphenidate hydrochloride) tablets — Prescribing Information', sid('dexmethylphenidate'))
drug('dexmethylphenidate', 'nervous-system', 'دکس‌متیل‌فنیدیت', 'Dexmethylphenidate', T('محرک CNS', 'CNS stimulant'), [{'name': 'Focalin', 'market': 'US'}], ['focalin', 'فوکالین', 'دکسمتیلفنیدیت'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet', [R(Fo, '3')]), tab('tab-5', 5, '5 mg tablet', [R(Fo, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Fo, '3')])],
     [reg('adhd', 'adhd', T('ADHD (۶ سال به بالا) تازه‌شروع — ۲٫۵ mg دو بار در روز با ۴ ساعت فاصله؛ تا ۱۰ mg دو بار', 'ADHD (≥6 y), new to methylphenidate — 2.5 mg twice daily 4 h apart; up to 10 mg twice daily'), {'minAge': age(6, 'year')}, 'fixed', {'perDose': 2.5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(Fo, '2.2')],
          limits={'maxPerDay': 20, 'refs': [R(Fo, '2.2')]}, notes=[note('هفتگی ۲٫۵ تا ۵ mg افزایش. اگر متیل‌فنیدیت مصرف می‌کند: نصف دوز روزانه متیل‌فنیدیت. پیش از شروع بیماری قلبی و تیک بررسی. اگر طی یک ماه بهبود نیافت قطع.', 'Increase by 2.5–5 mg weekly. If already on methylphenidate: half the daily methylphenidate dose. Screen for cardiac disease and tics first. Stop if no improvement within a month.', [R(Fo, '2.2'), R(Fo, '2.1'), R(Fo, '2.4')])])],
     [CI('ci', 'حساسیت به متیل‌فنیدیت؛ MAOI همزمان یا ظرف ۱۴ روز (بحران فشار خون).', 'Hypersensitivity to methylphenidate; MAOIs concomitantly or within 14 days (hypertensive crisis).', [R(Fo, '4')])],
     warn=[W('هشدار جعبه‌ای: پتانسیل بالای سوءمصرف، اعتیاد، بیش‌مصرفی و مرگ.', 'Boxed warning: high potential for abuse, misuse and addiction, overdose and death.', [R(Fo, 'Boxed Warning')]),
           W('خطر در بیماری قلبی جدی؛ افزایش فشار و ضربان؛ عوارض روانی؛ پریاپیسم؛ رینود؛ مهار رشد در کودک؛ گلوکوم؛ تیک.', 'Risk in serious cardiac disease; raised BP and HR; psychiatric reactions; priapism; Raynaud; growth suppression in children; glaucoma; tics.', [R(Fo, '5')])],
     exs=[ex('adhd', 'tab-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1, 'perDay': 5}, ageYears=8, weightKg=25)])
print('s12d4 ok')

add_disease('tuberous-sclerosis', 'توبروس اسکلروزیس (TSC)', 'Tuberous sclerosis complex', ['TSC', 'توبروس اسکلروز', 'اسکلروز توبروس'], ['Q85.1'], 'neurology')
Ep = fda('epidiolex', 'FDA Epidiolex', 'Epidiolex (cannabidiol) oral solution 100 mg/mL — Prescribing Information', sid('cannabidiol'))
drug('cannabidiol', 'nervous-system', 'کانابیدیول', 'Cannabidiol', T('کانابینوئید ضدتشنج', 'Cannabinoid antiseizure drug'), [{'name': 'Epidiolex', 'market': 'US'}], ['epidiolex', 'اپیدیولکس', 'CBD', 'کانابیدیول'],
     [liquid('sol-100', 100, 1, '100 mg/mL oral solution', [R(Ep, '3')], form_='solution')],
     [reg('lgs', 'lennox-gastaut', T('لنوکس-گاستو یا دراوه (۱ سال به بالا) — شروع ۲٫۵ mg/kg دو بار؛ پس از یک هفته ۵ mg/kg دو بار (تا ۱۰ mg/kg دو بار)', 'Lennox-Gastaut or Dravet (≥1 y) — start 2.5 mg/kg twice daily; after one week 5 mg/kg twice daily (up to 10 mg/kg twice daily)'), {'minAge': age(1, 'year')}, 'weightBased', {'perKgPerDose': 2.5, 'perKgPerDoseMax': 10, 'intervalHours': 12}, [R(Ep, '2.2')],
          notes=[note('نگهدارنده توصیه‌شده ۵ mg/kg دو بار؛ افزایش هفتگی ۲٫۵ mg/kg دو بار تا ۱۰ mg/kg دو بار. پیش از شروع ALT، AST و بیلی‌روبین. نارسایی متوسط/شدید کبد طبق جدول ۱.', 'Recommended maintenance 5 mg/kg twice daily; weekly steps of 2.5 mg/kg twice daily up to 10 mg/kg twice daily. ALT, AST and bilirubin before starting. Moderate/severe hepatic impairment per Table 1.', [R(Ep, '2.2'), R(Ep, '2.1'), R(Ep, '2.6')])]),
      reg('dravet', 'dravet-syndrome', T('سندرم دراوه (۱ سال به بالا) — شروع ۲٫۵ mg/kg دو بار؛ نگهدارنده ۵ mg/kg دو بار (تا ۱۰)', 'Dravet syndrome (≥1 y) — start 2.5 mg/kg twice daily; maintenance 5 mg/kg twice daily (up to 10)'), {'minAge': age(1, 'year')}, 'weightBased', {'perKgPerDose': 2.5, 'perKgPerDoseMax': 10, 'intervalHours': 12}, [R(Ep, '2.2')]),
      reg('tsc', 'tuberous-sclerosis', T('تشنج توبروس اسکلروزیس (۱ سال به بالا) — شروع ۲٫۵ mg/kg دو بار؛ هفتگی تا ۱۲٫۵ mg/kg دو بار', 'Tuberous sclerosis seizures (≥1 y) — start 2.5 mg/kg twice daily; weekly up to 12.5 mg/kg twice daily'), {'minAge': age(1, 'year')}, 'weightBased', {'perKgPerDose': 2.5, 'perKgPerDoseMax': 12.5, 'intervalHours': 12}, [R(Ep, '2.3')])],
     [CI('hyper', 'حساسیت به کانابیدیول یا اجزای فرآورده.', 'Hypersensitivity to cannabidiol or any ingredient.', [R(Ep, '4')])],
     warn=[W('آسیب کبدی (به‌ویژه با والپروات) — آنزیم کبد پایش؛ خواب‌آلودگی؛ افکار خودکشی؛ قطع تدریجی.', 'Hepatocellular injury (especially with valproate) — monitor liver enzymes; somnolence and sedation; suicidal thoughts; withdraw gradually.', [R(Ep, '5')])],
     exs=[ex('lgs', 'sol-100', {'perDose': 50, 'mlPerDose': 0.5, 'upperPerDose': 200}, ageYears=6, weightKg=20), ex('dravet', 'sol-100', {'perDose': 50, 'mlPerDose': 0.5, 'upperPerDose': 200}, ageYears=6, weightKg=20),
          ex('tsc', 'sol-100', {'perDose': 50, 'mlPerDose': 0.5, 'upperPerDose': 250}, ageYears=6, weightKg=20)])
print('cannabidiol ok')
