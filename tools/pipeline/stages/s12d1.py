"""Stage 12d (part 1) — antipsychotics (asenapine, iloperidone, lumateperone, fluphenazine, loxapine, pimozide) and antiseizure drugs (eslicarbazepine, felbamate, stiripentol, fenfluramine)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
APS = lambda src, sec='Boxed Warning': W('هشدار جعبه‌ای: افزایش مرگ در سالمندان مبتلا به سایکوز ناشی از دمانس — برای این کاربرد تأیید نشده.', 'Boxed warning: increased mortality in elderly patients with dementia-related psychosis — not approved for this use.', [R(src, sec)])
AED = lambda src, sec: W('افکار و رفتار خودکشی؛ قطع ناگهانی نه (خطر تشنج و استاتوس).', 'Suicidal thoughts and behaviour; do not stop abruptly (seizures, status epilepticus).', [R(src, sec)])

add_disease('dravet-syndrome', 'سندرم دراوه', 'Dravet syndrome', ['dravet', 'دراوه', 'دراوت', 'صرع میوکلونیک شدید شیرخوارگی'], ['G40.83'], 'neurology')

# ===================== antipsychotics =====================
Sa = fda('saphris', 'FDA Saphris', 'Saphris (asenapine) sublingual tablets — Prescribing Information', sid('asenapine'))
sl = lambda id, mg: form(id, 'sublingual-tablet', 'sublingual', f'{mg} mg sublingual tablet', mg, 'mg', [R(Sa, '3')], per='tablet')
drug('asenapine', 'nervous-system', 'آسناپین', 'Asenapine', T('ضدروان‌پریشی آتیپیک', 'Atypical antipsychotic'), [{'name': 'Saphris', 'market': 'US'}], ['saphris', 'سافریس', 'آسناپین'],
     [sl('sl-5', 5), sl('sl-10', 10), sl('sl-2-5', 2.5)],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — ۵ mg زیرزبانی دو بار در روز (حداکثر ۱۰ mg دو بار)', 'Schizophrenia, adults — 5 mg sublingually twice daily (max 10 mg twice daily)'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(Sa, '2.2')],
          notes=[note('زیر زبان حل شود؛ نجوید و نبلعید؛ ۱۰ دقیقه بعد چیزی نخورد و ننوشد. افزایش به ۱۰ mg پس از یک هفته؛ سود بیشتری نشان نداده.', 'Dissolve under the tongue; do not chew or swallow; no food or drink for 10 min. Increase to 10 mg after one week if tolerated; no added benefit shown.', [R(Sa, '2.2'), R(Sa, '2.1')])]),
      reg('bp', 'bipolar-mania', T('مانیا یا دوره مختلط دوقطبی I بزرگسال (تک‌درمانی) — ۵ تا ۱۰ mg دو بار در روز', 'Bipolar I mania or mixed episodes, adults (monotherapy) — 5–10 mg twice daily'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(Sa, '2.3')]),
      reg('bp-child', 'bipolar-mania', T('مانیای دوقطبی کودک ۱۰ تا ۱۷ سال — شروع ۲٫۵ mg دو بار؛ تا ۱۰ mg دو بار', 'Bipolar mania, children 10–17 y — start 2.5 mg twice daily; up to 10 mg twice daily'), {'minAge': age(10, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 2.5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(Sa, '2.3')],
          notes=[note('پس از ۳ روز به ۵ mg و پس از ۳ روز دیگر به ۱۰ mg دو بار.', 'After 3 days to 5 mg, and after 3 more days to 10 mg twice daily.', [R(Sa, '2.3')])])],
     [CI('ci', 'نارسایی شدید کبد (Child-Pugh C)؛ سابقه حساسیت به آسناپین (آنافیلاکسی، آنژیوادم).', 'Severe hepatic impairment (Child-Pugh C); history of hypersensitivity to asenapine (anaphylaxis, angioedema).', [R(Sa, '4')])],
     warn=[APS(Sa), W('سندرم نورولپتیک بدخیم؛ دیسکینزی دیررس؛ تغییرات متابولیک؛ هیپرپرولاکتینمی؛ تشنج؛ دیسفاژی؛ زمین خوردن.', 'Neuroleptic malignant syndrome; tardive dyskinesia; metabolic changes; hyperprolactinaemia; seizures; dysphagia; falls.', [R(Sa, '5')])],
     exs=[ex('scz', 'sl-5', {'perDose': 5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 10}, ageYears=30, weightKg=70), ex('bp', 'sl-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70),
          ex('bp-child', 'sl-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=40)])

Fn = fda('fanapt', 'FDA Fanapt', 'Fanapt (iloperidone) tablets — Prescribing Information', sid('iloperidone'))
drug('iloperidone', 'nervous-system', 'ایلوپریدون', 'Iloperidone', T('ضدروان‌پریشی آتیپیک', 'Atypical antipsychotic'), [{'name': 'Fanapt', 'market': 'US'}], ['fanapt', 'فاناپت', 'ایلوپریدون'],
     [tab('tab-6', 6, '6 mg tablet', [R(Fn, '3')]), tab('tab-12', 12, '12 mg tablet', [R(Fn, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Fn, '3')])],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — هدف ۶ تا ۱۲ mg دو بار در روز پس از تیتراسیون از ۱ mg دو بار', 'Schizophrenia, adults — target 6–12 mg twice daily after titrating from 1 mg twice daily'), A18, 'fixed', {'perDose': 6, 'perDoseMax': 12, 'dosesPerDay': 2}, [R(Fn, '2.1, Table 1')],
          notes=[note('تیتراسیون روزانه طبق جدول ۱ (۱، ۲، ۴، ۶ mg دو بار…) برای پرهیز از افت فشار وضعیتی. وقفه بیش از ۳ روز: تیتراسیون از اول. متابولیزه‌کننده ضعیف CYP2D6 یا مهارکننده قوی CYP2D6/3A4: نصف دوز.', 'Daily titration per Table 1 (1, 2, 4, 6 mg twice daily…) to avoid orthostatic hypotension. Off >3 days: re-titrate. CYP2D6 poor metabolisers or strong CYP2D6/3A4 inhibitors: half the dose.', [R(Fn, '2.1'), R(Fn, '2.5'), R(Fn, '2.2'), R(Fn, '2.4')])]),
      reg('bp', 'bipolar-mania', T('مانیا یا دوره مختلط دوقطبی I بزرگسال — هدف ۱۲ mg دو بار پس از تیتراسیون', 'Bipolar I mania or mixed episodes, adults — target 12 mg twice daily after titration'), A18, 'fixed', {'perDose': 12, 'dosesPerDay': 2}, [R(Fn, '2.1, Table 1')])],
     [CI('hyper', 'حساسیت شناخته‌شده به ایلوپریدون.', 'Known hypersensitivity to iloperidone.', [R(Fn, '4')])],
     warn=[APS(Fn), W('طولانی شدن QT؛ افت فشار وضعیتی و سنکوپ؛ NMS؛ دیسکینزی دیررس؛ تغییرات متابولیک؛ لکوپنی؛ پریاپیسم. نارسایی شدید کبد توصیه نمی‌شود.', 'QT prolongation; orthostatic hypotension and syncope; NMS; tardive dyskinesia; metabolic changes; leukopenia; priapism. Not recommended in severe hepatic impairment.', [R(Fn, '5'), R(Fn, '2.3')])],
     exs=[ex('scz', 'tab-6', {'perDose': 6, 'tabletsPerDoseRounded': 1, 'upperPerDose': 12}, ageYears=30, weightKg=70), ex('bp', 'tab-12', {'perDose': 12, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Cp = fda('caplyta', 'FDA Caplyta', 'Caplyta (lumateperone) capsules — Prescribing Information', sid('lumateperone'))
cap = lambda id, mg, src, sec='3', label=None: tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
drug('lumateperone', 'nervous-system', 'لوماتپرون', 'Lumateperone', T('ضدروان‌پریشی آتیپیک', 'Atypical antipsychotic'), [{'name': 'Caplyta', 'market': 'US'}], ['caplyta', 'کاپلیتا', 'لوماتپرون'],
     [cap('cap-42', 42, Cp), cap('cap-21', 21, Cp), tab('cap-10-5', 10.5, '10.5 mg capsule', [R(Cp, '3')], per='capsule', form_='capsule')],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — ۴۲ mg یک بار در روز (بدون تیتراسیون)', 'Schizophrenia, adults — 42 mg once daily (no titration)'), A18, 'fixed', {'perDose': 42, 'dosesPerDay': 1}, [R(Cp, '2.1')], allowed=['cap-42'],
          notes=[note('نارسایی متوسط/شدید کبد یا مهارکننده متوسط CYP3A4: ۲۱ mg؛ مهارکننده قوی CYP3A4: ۱۰٫۵ mg.', 'Moderate/severe hepatic impairment or moderate CYP3A4 inhibitors: 21 mg; strong CYP3A4 inhibitors: 10.5 mg.', [R(Cp, '2.3'), R(Cp, '2.2')])]),
      reg('bpd', 'bipolar-depression', T('افسردگی دوقطبی بزرگسال — ۴۲ mg یک بار در روز', 'Bipolar depression, adults — 42 mg once daily'), A18, 'fixed', {'perDose': 42, 'dosesPerDay': 1}, [R(Cp, '2.1')], allowed=['cap-42'])],
     [CI('hyper', 'سابقه حساسیت به لوماتپرون.', 'History of hypersensitivity to lumateperone.', [R(Cp, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ در سالمندان با سایکوز دمانس؛ افکار خودکشی در کودکان و جوانان (ضدافسردگی).', 'Boxed warning: increased mortality in elderly patients with dementia-related psychosis; suicidal thoughts in children and young adults (antidepressant).', [R(Cp, 'Boxed Warning')]),
           W('NMS؛ دیسکینزی دیررس؛ تغییرات متابولیک؛ لکوپنی؛ افت فشار وضعیتی؛ تشنج.', 'NMS; tardive dyskinesia; metabolic changes; leukopenia; orthostatic hypotension; seizures.', [R(Cp, '5')])],
     exs=[ex('scz', 'cap-42', {'perDose': 42, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('bpd', 'cap-42', {'perDose': 42, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Fp = fda('fluphenazine', 'FDA Fluphenazine', 'Fluphenazine hydrochloride tablets USP — Prescribing Information', sid('fluphenazine')); d = R(Fp, 'Dosage and Administration')
drug('fluphenazine', 'nervous-system', 'فلوفنازین', 'Fluphenazine', T('فنوتیازین (ضدروان‌پریشی تیپیک)', 'Phenothiazine (typical antipsychotic)'), [{'name': 'Fluphenazine', 'market': 'US'}], ['prolixin', 'فلوفنازین', 'modecate'],
     [tab('tab-1', 1, '1 mg tablet', [R(Fp, 'How Supplied')]), tab('tab-2-5', 2.5, '2.5 mg tablet', [R(Fp, 'How Supplied')]), tab('tab-5', 5, '5 mg tablet', [R(Fp, 'How Supplied')]), tab('tab-10', 10, '10 mg tablet', [R(Fp, 'How Supplied')])],
     [NC('psy', 'psychotic-disorders', 'اختلالات سایکوتیک بزرگسال — شروع ۲٫۵ تا ۱۰ mg/روز تقسیم هر ۶ تا ۸ ساعت', 'Psychotic disorders, adults — start 2.5–10 mg/day divided every 6–8 h', A18,
         'دوز روزانه کل فردی است؛ پاسخ معمولاً زیر ۲۰ mg/روز؛ تا ۴۰ mg/روز در موارد شدید. نگهدارنده ۱ تا ۵ mg یک بار در روز. سالمند: شروع ۱ تا ۲٫۵ mg/روز.', 'Total daily dose is individualised; response usually under 20 mg/day; up to 40 mg/day if severe. Maintenance 1–5 mg once daily. Elderly: start 1–2.5 mg/day.', [d])],
     [CI('ci', 'آسیب ساب‌کورتیکال مغز؛ دوز بالای خواب‌آورها؛ کما یا افسردگی شدید CNS؛ دیسکرازی خونی؛ آسیب کبدی؛ حساسیت به فلوفنازین (حساسیت متقاطع فنوتیازین).', 'Subcortical brain damage; large doses of hypnotics; coma or severe CNS depression; blood dyscrasia; liver damage; hypersensitivity to fluphenazine (phenothiazine cross-sensitivity).', [R(Fp, 'Contraindications')])],
     warn=[APS(Fp, 'Warnings'), W('دیسکینزی دیررس؛ سندرم نورولپتیک بدخیم.', 'Tardive dyskinesia; neuroleptic malignant syndrome.', [R(Fp, 'Warnings')])])

Lx = fda('loxapine', 'FDA Loxapine', 'Loxapine capsules USP (Watson/Actavis) — Prescribing Information', sid('loxapine')); d = R(Lx, 'Dosage and Administration')
drug('loxapine', 'nervous-system', 'لوکساپین', 'Loxapine', T('دی‌بنزوکسازپین (ضدروان‌پریشی تیپیک)', 'Dibenzoxazepine (typical antipsychotic)'), [{'name': 'Loxitane', 'market': 'US'}], ['loxitane', 'لوکساپین'],
     [cap('cap-10', 10, Lx, 'How Supplied'), cap('cap-25', 25, Lx, 'How Supplied'), cap('cap-5', 5, Lx, 'How Supplied'), cap('cap-50', 50, Lx, 'How Supplied')],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — شروع ۱۰ mg دو بار در روز', 'Schizophrenia, adults — start 10 mg twice daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 2}, [d],
          limits={'maxPerDay': 250, 'refs': [d]}, notes=[note('افزایش طی ۷ تا ۱۰ روز؛ محدوده معمول ۶۰ تا ۱۰۰ mg/روز در ۲ تا ۴ دوز؛ بیش از ۲۵۰ mg/روز نه. نگهدارنده اغلب ۲۰ تا ۶۰ mg/روز.', 'Increase over 7–10 days; usual range 60–100 mg/day in 2–4 doses; not above 250 mg/day. Maintenance often 20–60 mg/day.', [d])])],
     [CI('ci', 'کما یا افسردگی شدید ناشی از دارو (الکل، باربیتورات، مخدر)؛ حساسیت به دی‌بنزوکسازپین‌ها.', 'Coma or severe drug-induced depressed states (alcohol, barbiturates, opioids); hypersensitivity to dibenzoxazepines.', [R(Lx, 'Contraindications')])],
     warn=[APS(Lx, 'Warnings')], exs=[ex('scz', 'cap-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'perDay': 20}, ageYears=35, weightKg=70)])

Pi = fda('pimozide', 'FDA Pimozide', 'Pimozide tablets USP 1/2 mg (Par) — Prescribing Information', sid('pimozide')); d = R(Pi, 'Dosage and Administration')
drug('pimozide', 'nervous-system', 'پیموزاید', 'Pimozide', T('دی‌فنیل‌بوتیل‌پیپریدین (ضدروان‌پریشی)', 'Diphenylbutylpiperidine antipsychotic'), [{'name': 'Orap', 'market': 'US'}], ['orap', 'اوراپ', 'پیموزید'],
     [tab('tab-1', 1, '1 mg tablet (scored)', [R(Pi, 'How Supplied')], scored=True), tab('tab-2', 2, '2 mg tablet (scored)', [R(Pi, 'How Supplied')], scored=True)],
     [NC('tour', 'tourette', 'سندرم توره (تیک حرکتی و صوتی شدید) — شروع ۱ تا ۲ mg/روز در دوزهای تقسیمی؛ افزایش یک روز در میان', 'Tourette disorder (severe motor and phonic tics) — start 1–2 mg/day in divided doses; increase every other day', {},
         'بیشتر بیماران زیر ۰٫۲ mg/kg/روز یا ۱۰ mg/روز (هر کدام کمتر)؛ بیشتر توصیه نمی‌شود. بالای ۴ mg/روز ژنوتیپ CYP2D6؛ متابولیزه‌کننده ضعیف حداکثر ۴ mg/روز و افزایش زودتر از ۱۴ روز نه. ECG پایه و دوره‌ای.',
         'Most patients stay below 0.2 mg/kg/day or 10 mg/day (whichever is less); higher not recommended. Above 4 mg/day do CYP2D6 genotyping; poor metabolisers max 4 mg/day and no increase before 14 days. Baseline and periodic ECG.', [d])],
     [CI('ci', 'تیک ساده یا غیر از توره؛ داروهای ایجادکننده تیک (متیل‌فنیدیت، آمفتامین) تا قطع آن‌ها؛ QT طولانی مادرزادی، سابقه آریتمی، داروهای طولانی‌کننده QT، هیپوکالمی یا هیپومنیزیمی؛ افسردگی شدید CNS یا کما؛ حساسیت؛ ماکرولیدها و سایر مهارکننده‌های CYP3A4 (آزول‌ها، مهارکننده‌های پروتئاز).',
         'Simple tics or tics other than Tourette; tic-causing drugs (methylphenidate, amphetamines) until withdrawn; congenital long QT, history of arrhythmia, QT-prolonging drugs, hypokalaemia or hypomagnesaemia; severe CNS depression or coma; hypersensitivity; macrolides and other CYP3A4 inhibitors (azoles, protease inhibitors).', [R(Pi, 'Contraindications')])],
     warn=[W('طولانی شدن QT و مرگ ناگهانی؛ دیسکینزی دیررس؛ NMS.', 'QT prolongation and sudden death; tardive dyskinesia; NMS.', [R(Pi, 'Contraindications'), R(Pi, 'Warnings')])])

# ===================== antiseizure =====================
Ap = fda('aptiom', 'FDA Aptiom', 'Aptiom (eslicarbazepine acetate) tablets — Prescribing Information', sid('eslicarbazepine'))
drug('eslicarbazepine', 'nervous-system', 'اسلی‌کاربازپین', 'Eslicarbazepine acetate', T('ضدتشنج (مسدودکننده کانال سدیم)', 'Antiseizure (sodium-channel blocker)'), [{'name': 'Aptiom', 'market': 'US'}], ['aptiom', 'آپتیوم', 'zebinix', 'اسلیکاربازپین'],
     [tab('tab-800', 800, '800 mg tablet (scored)', [R(Ap, '3')], scored=True), tab('tab-400', 400, '400 mg tablet', [R(Ap, '3')]), tab('tab-200', 200, '200 mg tablet (scored)', [R(Ap, '3')], scored=True), tab('tab-600', 600, '600 mg tablet (scored)', [R(Ap, '3')], scored=True)],
     [reg('adult', 'epilepsy', T('تشنج فوکال بزرگسال — نگهدارنده ۸۰۰ تا ۱۶۰۰ mg یک بار در روز (شروع ۴۰۰ mg)', 'Focal seizures, adults — maintenance 800–1600 mg once daily (start 400 mg)'), A18, 'fixed', {'perDose': 800, 'perDoseMax': 1600, 'dosesPerDay': 1}, [R(Ap, '2.2')],
          notes=[note('شروع ۴۰۰ mg (یا ۸۰۰ mg در صورت نیاز)؛ هفتگی ۴۰۰ تا ۶۰۰ mg افزایش. همراه اکس‌کاربازپین نه.', 'Start 400 mg (or 800 mg if needed); increase weekly by 400–600 mg. Not with oxcarbazepine.', [R(Ap, '2.2'), R(Ap, '2.3')])]),
      reg('child', 'epilepsy', T('تشنج فوکال کودک ۴ تا ۱۷ سال — نگهدارنده یک بار در روز بر اساس وزن (حد پایین محدوده)', 'Focal seizures, children 4–17 y — once-daily maintenance by weight (lower end of range)'), {'minAge': age(4, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 11}, 'weightBand',
          {'weightBands': [{'minWeightKg': 11, 'maxWeightKg': 21.99, 'perDose': 400, 'dosesPerDay': 1}, {'minWeightKg': 22, 'maxWeightKg': 31.99, 'perDose': 500, 'dosesPerDay': 1}, {'minWeightKg': 32, 'maxWeightKg': 38, 'perDose': 600, 'dosesPerDay': 1}, {'minWeightKg': 38.01, 'maxWeightKg': None, 'perDose': 800, 'dosesPerDay': 1}]},
          [R(Ap, '2.2, Table 1')], notes=[note('حد بالای نگهدارنده: ۱۱–۲۱ kg: ۶۰۰؛ ۲۲–۳۱: ۸۰۰؛ ۳۲–۳۸: ۹۰۰؛ >۳۸: ۱۲۰۰ mg. شروع و گام افزایش هفتگی: ۲۰۰ / ۳۰۰ / ۳۰۰ / ۴۰۰ mg.', 'Upper maintenance: 11–21 kg: 600; 22–31: 800; 32–38: 900; >38: 1200 mg. Start and weekly step: 200 / 300 / 300 / 400 mg.', [R(Ap, '2.2, Table 1')])])],
     [CI('hyper', 'حساسیت به اسلی‌کاربازپین یا اکس‌کاربازپین.', 'Hypersensitivity to eslicarbazepine acetate or oxcarbazepine.', [R(Ap, '4')])],
     warn=[AED(Ap, '5.1'), W('واکنش پوستی شدید و DRESS؛ آنافیلاکسی؛ هیپوناترمی؛ سرگیجه و اختلال تعادل؛ آسیب کبدی. نارسایی شدید کبد توصیه نمی‌شود.', 'Serious skin reactions and DRESS; anaphylaxis; hyponatraemia; dizziness and gait disturbance; liver injury. Not recommended in severe hepatic impairment.', [R(Ap, '5'), R(Ap, '2.5')])],
     renal=[{'egfrBelow': 50, 'severity': 'warn', 'text': T('ClCr زیر ۵۰: دوز شروع، تیتراسیون و نگهدارنده ۵۰٪ کم شود.', 'CrCl <50: reduce initial, titration and maintenance doses by 50%.'), 'refs': [R(Ap, '2.4')]}],
     exs=[ex('adult', 'tab-800', {'perDose': 800, 'tabletsPerDoseRounded': 1, 'upperPerDose': 1600}, ageYears=35, weightKg=70), ex('child', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=5, weightKg=18),
          ex('child', 'tab-200', {'perDose': 500, 'tabletsPerDoseRounded': 2.5}, ageYears=8, weightKg=25)])

Fb = fda('felbatol', 'FDA Felbatol', 'Felbatol (felbamate) tablets and oral suspension — Prescribing Information', sid('felbamate')); d = R(Fb, 'Dosage and Administration')
drug('felbamate', 'nervous-system', 'فلبامات', 'Felbamate', T('ضدتشنج (دی‌کاربامات)', 'Antiseizure (dicarbamate)'), [{'name': 'Felbatol', 'market': 'US'}], ['felbatol', 'فلباتول', 'فلبامات'],
     [tab('tab-400', 400, '400 mg tablet (scored)', [R(Fb, 'How Supplied')], scored=True), tab('tab-600', 600, '600 mg tablet (scored)', [R(Fb, 'How Supplied')], scored=True), liquid('susp-600', 600, 5, '600 mg/5 mL oral suspension', [R(Fb, 'How Supplied')])],
     [reg('adult', 'epilepsy', T('صرع شدید مقاوم بزرگسال و ۱۴ سال به بالا — شروع ۱۲۰۰ mg/روز در ۳ دوز؛ تا ۳۶۰۰ mg/روز', 'Severe refractory epilepsy, adults and ≥14 y — start 1200 mg/day in 3 doses; up to 3600 mg/day'), {'minAge': age(14, 'year')}, 'fixed', {'perDose': 400, 'perDoseMax': 1200, 'dosesPerDay': 3}, [d],
          notes=[note('یا در ۴ دوز. افزودنی: داروهای ضدصرع دیگر ۲۰٪ (تا ۳۳٪) کم شوند؛ هفتگی ۱۲۰۰ mg/روز افزایش. فقط وقتی صرع آن‌قدر شدید است که خطر آنمی آپلاستیک پذیرفتنی باشد.', 'Or in 4 doses. Adjunct: reduce other AEDs by 20% (up to 33%); increase by 1200 mg/day weekly. Only when epilepsy is severe enough that aplastic anaemia risk is acceptable.', [d, R(Fb, 'Boxed Warning')])]),
      reg('lgs', 'lennox-gastaut', T('لنوکس-گاستو کودک ۲ تا ۱۴ سال (افزودنی) — شروع ۱۵ mg/kg/روز در ۳ دوز؛ هفتگی تا ۴۵ mg/kg/روز', 'Lennox-Gastaut, children 2–14 y (adjunct) — start 15 mg/kg/day in 3 doses; weekly up to 45 mg/kg/day'), {'minAge': age(2, 'year'), 'maxAge': age(14, 'year')}, 'weightBased', {'perKgPerDay': 15, 'perKgPerDayMax': 45, 'dividedDoses': 3}, [d],
          notes=[note('یا در ۴ دوز. داروهای ضدصرع همزمان ۲۰٪ کم شوند.', 'Or in 4 doses. Reduce concomitant AEDs by 20%.', [d])])],
     [CI('ci', 'حساسیت به فلبامات یا سایر کاربامات‌ها؛ سابقه دیسکرازی خونی یا اختلال کبدی.', 'Hypersensitivity to felbamate or other carbamates; history of blood dyscrasia or hepatic dysfunction.', [R(Fb, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: آنمی آپلاستیک (بیش از ۱۰۰ برابر) و نارسایی کبد — فقط در صرع بسیار شدید، با مشاوره خون و رضایت آگاهانه.', 'Boxed warning: aplastic anaemia (>100-fold) and hepatic failure — only in very severe epilepsy, with haematology consultation and informed consent.', [R(Fb, 'Boxed Warning')]), AED(Fb, 'Warnings')],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('اختلال کلیه: دوز شروع و نگهدارنده نصف شود.', 'Renal impairment: halve the starting and maintenance doses.'), 'refs': [R(Fb, 'Dosage and Administration')]}],
     exs=[ex('adult', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1, 'upperPerDose': 1200}, ageYears=30, weightKg=70), ex('lgs', 'susp-600', {'perDose': 100, 'mlPerDose': 0.83, 'upperPerDose': 300}, ageYears=6, weightKg=20)])

Dc = fda('diacomit', 'FDA Diacomit', 'Diacomit (stiripentol) capsules and powder for oral suspension — Prescribing Information', sid('stiripentol'))
drug('stiripentol', 'nervous-system', 'استیری‌پنتول', 'Stiripentol', T('ضدتشنج', 'Antiseizure'), [{'name': 'Diacomit', 'market': 'US'}], ['diacomit', 'دیاکومیت', 'استیریپنتول'],
     [form('sach-250', 'sachet', 'oral', '250 mg powder for oral suspension (packet)', 250, 'mg', [R(Dc, '3')], per='sachet'), form('sach-500', 'sachet', 'oral', '500 mg powder for oral suspension (packet)', 500, 'mg', [R(Dc, '3')], per='sachet'), cap('cap-250', 250, Dc), cap('cap-500', 500, Dc)],
     [reg('dravet', 'dravet-syndrome', T('سندرم دراوه (همراه کلوبازام) — ۶ ماه و ≥۷ kg: ۵۰ mg/kg/روز در ۲ دوز', 'Dravet syndrome (with clobazam) — ≥6 months and ≥7 kg: 50 mg/kg/day in 2 doses'), {'minAge': age(6, 'month'), 'minWeightKg': 7}, 'weightBased', {'perKgPerDay': 50, 'dividedDoses': 2}, [R(Dc, '2.2, Table 1')],
          limits={'maxPerDay': 3000, 'refs': [R(Dc, '2.2')]}, notes=[note('۱ سال و ≥۱۰ kg: می‌تواند ۳ دوز (۱۶٫۶۷ mg/kg) باشد. به نزدیک‌ترین دوز ممکن گرد شود (معمولاً ۵۰ تا ۱۵۰ mg از ۵۰ mg/kg/روز). با غذا؛ کپسول باز نشود. CBC پیش از شروع.', '≥1 y and ≥10 kg: may use 3 doses (16.67 mg/kg). Round to the nearest achievable dose (usually within 50–150 mg of 50 mg/kg/day). With a meal; do not open capsules. CBC before starting.', [R(Dc, '2.2'), R(Dc, '2.3'), R(Dc, '2.1')])])],
     warn=[W('خواب‌آلودگی؛ کاهش اشتها و وزن؛ نوتروپنی و ترومبوسیتوپنی؛ فنیل‌کتونوری (پودر)؛ افکار خودکشی؛ قطع تدریجی.', 'Somnolence; decreased appetite and weight; neutropenia and thrombocytopenia; phenylketonuria (powder); suicidal thoughts; withdraw gradually.', [R(Dc, '5')])],
     exs=[ex('dravet', 'sach-250', {'perDose': 500, 'tabletsPerDoseRounded': 2}, ageYears=5, weightKg=20)])

Ft = fda('fintepla', 'FDA Fintepla', 'Fintepla (fenfluramine) oral solution 2.2 mg/mL — Prescribing Information', sid('fenfluramine'))
drug('fenfluramine', 'nervous-system', 'فن‌فلورامین', 'Fenfluramine', T('ضدتشنج (عامل سروتونرژیک)', 'Antiseizure (serotonergic agent)'), [{'name': 'Fintepla', 'market': 'US'}], ['fintepla', 'فینتپلا', 'فنفلورامین'],
     [liquid('sol-2-2', 2.2, 1, '2.2 mg/mL oral solution', [R(Ft, '3')], form_='solution')],
     [reg('std', 'dravet-syndrome', T('دراوه و لنوکس-گاستو (۲ سال به بالا) — شروع ۰٫۱ mg/kg دو بار؛ هفتگی تا ۰٫۳۵ mg/kg دو بار (حداکثر ۲۶ mg/روز)', 'Dravet and Lennox-Gastaut (≥2 y) — start 0.1 mg/kg twice daily; weekly up to 0.35 mg/kg twice daily (max 26 mg/day)'), {'minAge': age(2, 'year')}, 'weightBased', {'perKgPerDose': 0.1, 'perKgPerDoseMax': 0.35, 'intervalHours': 12}, [R(Ft, '2.2')],
          limits={'maxPerDay': 26, 'refs': [R(Ft, '2.2')]}, notes=[note('با استیری‌پنتول + کلوبازام: حداکثر ۰٫۲ mg/kg دو بار (۱۷ mg/روز). مهارکننده قوی CYP1A2/2D6: حداکثر ۲۰ mg/روز (۱۷ با استیری‌پنتول). نارسایی کبد طبق جدول ۲. اکوکاردیوگرافی پیش، هر ۶ ماه و پس از درمان.', 'With stiripentol + clobazam: max 0.2 mg/kg twice daily (17 mg/day). Strong CYP1A2/2D6 inhibitors: max 20 mg/day (17 with stiripentol). Hepatic impairment per Table 2. Echocardiogram before, every 6 months and after.', [R(Ft, '2.2'), R(Ft, '2.3'), R(Ft, '2.5'), R(Ft, '2.6')])]),
      reg('lgs', 'lennox-gastaut', T('لنوکس-گاستو (۲ سال به بالا) — شروع ۰٫۱ mg/kg دو بار؛ نگهدارنده ۰٫۳۵ mg/kg دو بار (حداکثر ۲۶ mg/روز)', 'Lennox-Gastaut (≥2 y) — start 0.1 mg/kg twice daily; maintenance 0.35 mg/kg twice daily (max 26 mg/day)'), {'minAge': age(2, 'year')}, 'weightBased', {'perKgPerDose': 0.1, 'perKgPerDoseMax': 0.35, 'intervalHours': 12}, [R(Ft, '2.2')],
          limits={'maxPerDay': 26, 'refs': [R(Ft, '2.2')]})],
     [CI('ci', 'حساسیت به فن‌فلورامین؛ مهارکننده MAO همزمان یا ظرف ۱۴ روز (سندرم سروتونین).', 'Hypersensitivity to fenfluramine; MAOIs concomitantly or within 14 days (serotonin syndrome).', [R(Ft, '4')])],
     warn=[W('هشدار جعبه‌ای: بیماری دریچه قلب و فشار خون شریانی ریوی — اکو اجباری؛ فقط از طریق برنامه REMS.', 'Boxed warning: valvular heart disease and pulmonary arterial hypertension — echocardiograms required; available only through a REMS.', [R(Ft, 'Boxed Warning')]),
           W('کاهش اشتها و وزن؛ خواب‌آلودگی؛ افکار خودکشی؛ سندرم سروتونین؛ افزایش فشار خون؛ گلوکوم.', 'Decreased appetite and weight; somnolence; suicidal thoughts; serotonin syndrome; increased blood pressure; glaucoma.', [R(Ft, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('eGFR ۱۵ تا ۲۹: حداکثر ۲۰ mg/روز (۱۷ با استیری‌پنتول + کلوبازام).', 'eGFR 15–29: max 20 mg/day (17 with stiripentol + clobazam).'), 'refs': [R(Ft, '2.4')]}],
     exs=[ex('std', 'sol-2-2', {'perDose': 2, 'mlPerDose': 0.91, 'upperPerDose': 7}, ageYears=6, weightKg=20), ex('lgs', 'sol-2-2', {'perDose': 2, 'mlPerDose': 0.91, 'upperPerDose': 7}, ageYears=6, weightKg=20)])
print('s12d1 ok')
