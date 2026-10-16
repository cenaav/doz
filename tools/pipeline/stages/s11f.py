"""Stage 11f — newer antiepileptics, Parkinson adjuncts, sleep/wake, CGRP migraine, newer antipsychotics, antifungal/antiviral, labour induction, insulins, romosozumab, agomelatine."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's11_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
DEM = lambda src: W('هشدار جعبه‌ای: افزایش مرگ در سالمندان با سایکوز دمانس؛ افکار خودکشی در کودکان و جوانان.', 'Boxed warning: increased mortality in elderly patients with dementia-related psychosis; suicidal thoughts in children and young adults.', [R(src, 'Boxed Warning')])

add_disease('narcolepsy', 'نارکولپسی و خواب‌آلودگی شدید روزانه', 'Narcolepsy and excessive daytime sleepiness', ['narcolepsy', 'نارکولپسی', 'حمله خواب', 'cataplexy', 'خواب آلودگی روزانه'], ['G47.419'], 'neurology')
add_disease('infantile-spasms', 'اسپاسم شیرخواران (سندرم وست)', 'Infantile spasms (West syndrome)', ['infantile spasms', 'west syndrome', 'سندرم وست', 'اسپاسم نوزادی'], ['G40.822'], 'neurology')
add_disease('esophageal-candidiasis', 'کاندیدیاز مری', 'Oesophageal candidiasis', ['esophageal candidiasis', 'برفک مری', 'قارچ مری'], ['B37.81'], 'infectious')
def ml(aid, title, review):
    m, dd, y = review.split('/')
    return add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                   edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
d = json.load(open(os.path.join(ROOT, 'diseases.json')))
for x in d:
    if x['id'] == 'narcolepsy':
        x['symptoms'] = {'items': [T('شروع معمولاً ۱۵ تا ۳۰ سالگی', 'Usually starts at 15–30 y'), T('خواب‌آلودگی شدید روزانه و حمله‌های خواب غیرقابل کنترل (چند ثانیه تا چند دقیقه)', 'Extreme daytime sleepiness and uncontrollable sleep attacks (seconds to minutes)'),
                                       T('کاتاپلکسی: از دست رفتن ناگهانی کنترل عضلات با هیجان (خنده یا خشم) با هوشیاری حفظ‌شده', 'Cataplexy: sudden loss of muscle control triggered by emotions (laughter, anger) with awareness preserved'),
                                       T('حمله‌ها حین غذا خوردن، صحبت یا رانندگی خطرناک است', 'Attacks during eating, talking or driving can be dangerous')],
                             'refs': [{'source': ml('000802', 'Narcolepsy', '7/17/2025'), 'section': 'Symptoms', 'note': {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}}]}
json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')

# ===================== epilepsy =====================
Fy = fda('fycompa', 'FDA Fycompa', 'Fycompa (perampanel) tablets and oral suspension — Prescribing Information', sid('fycompa'))
drug('perampanel', 'nervous-system', 'پرامپانل', 'Perampanel', T('آنتاگونیست گیرنده AMPA (ضدصرع)', 'AMPA receptor antagonist (antiepileptic)'), [{'name': 'Fycompa', 'market': 'US'}], ['fycompa', 'فایکومپا', 'پرامپانل'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Fy, '3')]) for m in (2, 4, 6, 8, 10, 12)],
     [reg('pos', 'epilepsy', T('تشنج پارشیل (۴ سال به بالا) — ۲ mg هنگام خواب، هر هفته ۲ mg بیشتر؛ نگهدارنده ۸ تا ۱۲ mg', 'Partial-onset seizures (≥4 y) — 2 mg at bedtime, +2 mg weekly; maintenance 8–12 mg'), {'minAge': age(4, 'year')}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 2, 'increment': 2, 'incrementEveryDays': 7, 'targetMin': 8, 'targetMax': 12, 'max': 12}}, [R(Fy, '2.1')],
          notes=[note('با القاگر متوسط/قوی CYP3A4 (کاربامازپین، فنی‌توئین، اکس‌کاربازپین) شروع ۴ mg. تشنج تونیک-کلونیک ژنرالیزه (۱۲ سال به بالا): نگهدارنده ۸ mg.', 'With moderate/strong CYP3A4 inducers (carbamazepine, phenytoin, oxcarbazepine) start at 4 mg. Primary generalised tonic-clonic (≥12 y): maintenance 8 mg.', [R(Fy, '2'), R(Fy, '2.2')])])],
     warn=[W('هشدار جعبه‌ای: واکنش‌های روانی و رفتاری جدی (پرخاشگری، خصومت، افکار قتل).', 'Boxed warning: serious psychiatric and behavioural reactions (aggression, hostility, homicidal ideation).', [R(Fy, 'Boxed Warning')])],
     exs=[ex('pos', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Xc = fda('xcopri', 'FDA Xcopri', 'Xcopri (cenobamate) tablets — Prescribing Information', sid('xcopri'))
drug('cenobamate', 'nervous-system', 'سنوبامات', 'Cenobamate', T('ضدصرع', 'Antiepileptic'), [{'name': 'Xcopri', 'market': 'US'}], ['xcopri', 'سنوبامات'],
     [tab(f'tab-{m}'.replace('.', '-'), m, f'{m} mg tablet', [R(Xc, '3')]) for m in (12.5, 25, 50, 100, 150, 200)],
     [NC('pos', 'epilepsy', 'تشنج پارشیل بزرگسال — تیتراسیون ۱۱ هفته‌ای تا ۲۰۰ mg یک بار در روز', 'Adult partial-onset seizures — 11-week titration to 200 mg once daily', A18,
         'هفته ۱ و ۲: ۱۲٫۵ mg؛ ۳ و ۴: ۲۵؛ ۵ و ۶: ۵۰؛ ۷ و ۸: ۱۰۰؛ ۹ و ۱۰: ۱۵۰؛ از هفته ۱۱: ۲۰۰ mg یک بار در روز. در صورت نیاز هر ۲ هفته ۵۰ mg بیشتر تا ۴۰۰ mg. سریع‌تر تیتره نشود (DRESS). نارسایی خفیف/متوسط کبد: حداکثر ۲۰۰ mg.',
         'Weeks 1–2: 12.5 mg; 3–4: 25; 5–6: 50; 7–8: 100; 9–10: 150; from week 11: 200 mg once daily. If needed +50 mg every 2 weeks to 400 mg. Do not titrate faster (DRESS). Mild/moderate hepatic impairment: max 200 mg.', [R(Xc, '2.2, Table 1'), R(Xc, '2.3')])],
     [CI('ci', 'حساسیت به سنوبامات؛ سندرم QT کوتاه خانوادگی.', 'Hypersensitivity to cenobamate; familial short QT syndrome.', [R(Xc, '4')])],
     warn=[W('DRESS با تیتراسیون سریع؛ کوتاه شدن QT؛ افکار خودکشی؛ خواب‌آلودگی.', 'DRESS with rapid titration; QT shortening; suicidal ideation; somnolence.', [R(Xc, '5')])])

Rf = fda('rufinamide', 'FDA Rufinamide susp.', 'Rufinamide oral suspension 40 mg/mL — Prescribing Information', sid('banzel'))
drug('rufinamide', 'nervous-system', 'روفینامید', 'Rufinamide', T('ضدصرع (تریازول)', 'Antiepileptic (triazole)'), [{'name': 'Banzel', 'market': 'US'}], ['banzel', 'inovelon', 'روفینامید'],
     [liquid('susp-40', 40, 1, '40 mg/mL oral suspension', [R(Rf, '3')])],
     [reg('child', 'lennox-gastaut', T('لنوکس-گاستو کودک (۱ تا <۱۷ سال) — شروع ۱۰ mg/kg/روز در دو دوز', 'Lennox-Gastaut, children 1–<17 y — start 10 mg/kg/day in two doses'), {'minAge': age(1, 'year'), 'maxAge': age(17, 'year')}, 'weightBased', {'perKgPerDay': 10, 'dividedDoses': 2}, [R(Rf, '2.1')],
          limits={'maxPerKgPerDay': 45, 'maxPerDay': 3200, 'refs': [R(Rf, '2.1')]}, notes=[note('افزایش ۱۰ mg/kg یک روز در میان تا حداکثر ۴۵ mg/kg/روز (نه بیش از ۳۲۰۰ mg). با غذا. با والپروات دوز شروع کمتر.', 'Increase by 10 mg/kg every other day up to 45 mg/kg/day (not over 3200 mg). With food. Start lower with valproate.', [R(Rf, '2.1'), R(Rf, '2.5')])]),
      reg('adult', 'lennox-gastaut', T('لنوکس-گاستو بزرگسال — شروع ۴۰۰ تا ۸۰۰ mg/روز در دو دوز (حداکثر ۳۲۰۰ mg)', 'Lennox-Gastaut, adult — start 400–800 mg/day in two doses (max 3200 mg)'), {'minAge': age(17, 'year')}, 'fixed', {'perDose': 200, 'perDoseMax': 400, 'dosesPerDay': 2}, [R(Rf, '2.1')],
          limits={'maxPerDay': 3200, 'refs': [R(Rf, '2.1')]}, notes=[note('افزایش ۴۰۰ تا ۸۰۰ mg یک روز در میان تا ۳۲۰۰ mg/روز.', 'Increase by 400–800 mg every other day to 3200 mg/day.', [R(Rf, '2.1')])])],
     [CI('qt', 'سندرم QT کوتاه خانوادگی.', 'Familial short QT syndrome.', [R(Rf, '4')])],
     exs=[ex('child', 'susp-40', {'perDose': 100, 'mlPerDose': 2.5}, ageYears=8, weightKg=20), ex('adult', 'susp-40', {'perDose': 200, 'mlPerDose': 5, 'upperPerDose': 400}, ageYears=25, weightKg=65)])

Vg = fda('vigabatrin', 'FDA Vigabatrin', 'Vigabatrin for oral solution 500 mg packet — Prescribing Information', sid('sabril'))
VIS = W('هشدار جعبه‌ای: کاهش دائمی میدان بینایی (دید تونلی) — معاینه بینایی پایه و هر ۳ ماه؛ فقط از طریق برنامه REMS.', 'Boxed warning: permanent bilateral visual field loss (tunnel vision) — baseline and 3-monthly vision assessment; available only through REMS.', [R(Vg, 'Boxed Warning')])
drug('vigabatrin', 'nervous-system', 'ویگاباترین', 'Vigabatrin', T('مهارکننده GABA ترانس‌آمیناز', 'GABA transaminase inhibitor'), [{'name': 'Sabril', 'market': 'US'}], ['sabril', 'سابریل', 'ویگاباترین'],
     [liquid('sol-50', 50, 1, '500 mg packet dissolved in 10 mL water = 50 mg/mL', [R(Vg, '3'), R(Vg, '2.3')], form_='solution')],
     [reg('is', 'infantile-spasms', T('اسپاسم شیرخواران (۱ ماه تا ۲ سال) — شروع ۵۰ mg/kg/روز در دو دوز، تا ۱۵۰ mg/kg/روز', 'Infantile spasms (1 month–2 y) — start 50 mg/kg/day in two doses, up to 150 mg/kg/day'), {'minAge': age(1, 'month'), 'maxAge': age(2, 'year')}, 'weightBased',
          {'perKgPerDay': 50, 'perKgPerDayMax': 150, 'dividedDoses': 2}, [R(Vg, '2.3')], limits={'maxPerKgPerDay': 150, 'refs': [R(Vg, '2.3')]},
          notes=[note('افزایش ۲۵ تا ۵۰ mg/kg/روز هر ۳ روز.', 'Increase by 25–50 mg/kg/day every 3 days.', [R(Vg, '2.3')])]),
      reg('cps', 'epilepsy', T('تشنج پارشیل مقاوم بزرگسال (۱۷ سال به بالا) — ۵۰۰ mg دو بار، هر هفته ۵۰۰ mg/روز بیشتر تا ۱۵۰۰ mg دو بار', 'Refractory complex partial seizures, adult (≥17 y) — 500 mg twice daily, +500 mg/day weekly to 1500 mg twice daily'), {'minAge': age(17, 'year')}, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 1000, 'increment': 500, 'incrementEveryDays': 7, 'max': 3000}}, [R(Vg, '2.2')],
          notes=[note('۶۰۰۰ mg/روز سود بیشتری ندارد. نارسایی کلیه: ClCr ۵۰ تا ۸۰ ← ۲۵٪ کمتر؛ ۳۰ تا ۵۰ ← ۵۰٪ کمتر.', '6000 mg/day adds no benefit. Renal impairment: CrCl 50–80 → 25% less; 30–50 → 50% less.', [R(Vg, '2.2'), R(Vg, '2.4')])])],
     warn=[VIS], exs=[ex('is', 'sol-50', {'perDose': 150, 'mlPerDose': 3, 'upperPerDose': 450}, ageMonths=6, weightKg=6), ex('cps', 'sol-50', {'perDose': 500, 'mlPerDose': 10}, ageYears=30, weightKg=70)])

# ===================== Parkinson =====================
Ec = fda('entacapone', 'FDA Entacapone', 'Entacapone tablets 200 mg (Macleods) — Prescribing Information', sid('comtan')); d = R(Ec, 'Dosage and Administration')
drug('entacapone', 'nervous-system', 'انتاکاپون', 'Entacapone', T('مهارکننده COMT', 'COMT inhibitor'), [{'name': 'Comtan', 'market': 'US'}], ['comtan', 'کامتان', 'انتاکاپون'],
     [tab('tab-200', 200, '200 mg tablet', [R(Ec, 'How Supplied')])],
     [reg('pd', 'parkinsons', T('پارکینسون با پدیده wearing-off — ۲۰۰ mg همراه هر دوز لوودوپا/کاربیدوپا (حداکثر ۸ بار در روز)', 'Parkinson’s with wearing-off — 200 mg with each levodopa/carbidopa dose (max 8 times daily)'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 4}, [d],
          limits={'maxPerDay': 1600, 'refs': [d]}, notes=[note('همیشه همراه لوودوپا/کاربیدوپا؛ به‌تنهایی اثر ضدپارکینسون ندارد. ماشین‌حساب ۴ دوز را نشان می‌دهد؛ تعداد دوز = تعداد دوز لوودوپا. ممکن است کاهش دوز لوودوپا لازم شود.', 'Always with levodopa/carbidopa; no antiparkinsonian effect alone. The calculator shows 4 doses; number of doses = number of levodopa doses. Levodopa dose may need reduction.', [d])])],
     [CI('hyper', 'حساسیت به انتاکاپون.', 'Hypersensitivity to entacapone.', [R(Ec, 'Contraindications')])],
     inter=[IA('maoi', 'MAOI غیرانتخابی (فنلزین، ترانیل‌سیپرومین): همزمان نه.', 'Non-selective MAOIs (phenelzine, tranylcypromine): should not be combined.', [R(Ec, 'Warnings')])],
     exs=[ex('pd', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

Og = fda('ongentys', 'FDA Ongentys', 'Ongentys (opicapone) capsules — Prescribing Information', sid('ongentys'))
drug('opicapone', 'nervous-system', 'اوپیکاپون', 'Opicapone', T('مهارکننده COMT', 'COMT inhibitor'), [{'name': 'Ongentys', 'market': 'US'}], ['ongentys', 'اونجنتیس', 'اوپیکاپون'],
     [tab('cap-25', 25, '25 mg capsule', [R(Og, '3')], per='capsule', form_='capsule'), tab('cap-50', 50, '50 mg capsule', [R(Og, '3')], per='capsule', form_='capsule')],
     [reg('pd', 'parkinsons', T('پارکینسون (کمکی لوودوپا، دوره off) — ۵۰ mg یک بار هنگام خواب', 'Parkinson’s (adjunct to levodopa for "off" episodes) — 50 mg once at bedtime'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Og, '2.1')],
          notes=[note('یک ساعت قبل و دست‌کم یک ساعت بعد غذا نخورد. نارسایی متوسط کبد: ۲۵ mg؛ شدید: پرهیز.', 'No food 1 h before and at least 1 h after. Moderate hepatic impairment: 25 mg; severe: avoid.', [R(Og, '2.1'), R(Og, '2.2')])])],
     [CI('ci', 'MAOI غیرانتخابی همزمان؛ فئوکروموسیتوم، پاراگانگلیوم یا تومورهای ترشح‌کننده کاتکول‌آمین.', 'Concomitant non-selective MAOIs; phaeochromocytoma, paraganglioma or other catecholamine-secreting tumours.', [R(Og, '4')])],
     exs=[ex('pd', 'cap-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

Xd = fda('xadago', 'FDA Xadago', 'Xadago (safinamide) tablets — Prescribing Information', sid('xadago'))
drug('safinamide', 'nervous-system', 'سافینامید', 'Safinamide', T('مهارکننده MAO-B', 'MAO-B inhibitor'), [{'name': 'Xadago', 'market': 'US'}], ['xadago', 'زاداگو', 'سافینامید'],
     [tab('tab-50', 50, '50 mg tablet', [R(Xd, '3')]), tab('tab-100', 100, '100 mg tablet', [R(Xd, '3')])],
     [reg('pd', 'parkinsons', T('پارکینسون (کمکی لوودوپا) — ۵۰ mg روزانه، پس از ۲ هفته تا ۱۰۰ mg', 'Parkinson’s (adjunct to levodopa) — 50 mg daily, up to 100 mg after 2 weeks'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 1}, [R(Xd, '2.1')],
          notes=[note('نارسایی متوسط کبد: حداکثر ۵۰ mg؛ شدید: منع مصرف.', 'Moderate hepatic impairment: max 50 mg; severe: contraindicated.', [R(Xd, '2.2')])])],
     [CI('ci', 'سایر MAOI یا مهارکننده قوی MAO (از جمله لاینزولید)؛ اپیوئیدها (مپریدین، متادون، ترامادول)، SNRI، ضدافسردگی سه‌حلقه‌ای و چهارحلقه‌ای، سیکلوبنزاپرین، متیل‌فنیدیت و آمفتامین، گل راعی؛ دکسترومتورفان؛ نارسایی شدید کبد.',
         'Other MAOIs or potent MAO inhibitors (including linezolid); opioids (meperidine, methadone, tramadol), SNRIs, tri-/tetracyclic antidepressants, cyclobenzaprine, methylphenidate and amphetamines, St John’s wort; dextromethorphan; severe hepatic impairment.', [R(Xd, '4')])],
     exs=[ex('pd', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'upperPerDose': 100}, ageYears=65, weightKg=70)])

# ===================== sleep / wake =====================
Md = fda('modafinil', 'FDA Modafinil', 'Modafinil tablets 100/200 mg — Prescribing Information', sid('modafinil'))
drug('modafinil', 'nervous-system', 'مودافینیل', 'Modafinil', T('محرک بیداری', 'Wakefulness-promoting agent'), [{'name': 'Provigil', 'market': 'US'}], ['provigil', 'پروویژیل', 'مودافینیل'],
     [tab('tab-100', 100, '100 mg tablet', [R(Md, '3')]), tab('tab-200', 200, '200 mg tablet (scored)', [R(Md, '3')], scored=True)],
     [reg('narco', 'narcolepsy', T('نارکولپسی یا آپنه انسدادی خواب — ۲۰۰ mg یک بار صبح', 'Narcolepsy or obstructive sleep apnoea — 200 mg once in the morning'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Md, '2.1')],
          notes=[note('تا ۴۰۰ mg تحمل شده ولی سود بیشتری ثابت نشده. نارسایی شدید کبد: نصف دوز. سالمند: دوز کمتر.', 'Up to 400 mg tolerated but no consistent extra benefit. Severe hepatic impairment: half dose. Elderly: consider lower dose.', [R(Md, '2.1'), R(Md, '2')])]),
      reg('swd', 'narcolepsy', T('اختلال کار شیفتی — ۲۰۰ mg حدود ۱ ساعت قبل از شروع شیفت', 'Shift work disorder — 200 mg about 1 h before the shift'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Md, '2.2')])],
     [CI('hyper', 'حساسیت به مودافینیل یا آرمودافینیل.', 'Hypersensitivity to modafinil or armodafinil.', [R(Md, '4')])],
     warn=[W('بثورات جدی پوستی (SJS) — قطع با اولین بثورات؛ آنژیوادم و آنافیلاکسی؛ حساسیت چندارگانی؛ خواب‌آلودگی پایدار؛ علائم روانی.', 'Serious rash (SJS) — stop at the first rash; angioedema and anaphylaxis; multi-organ hypersensitivity; persistent sleepiness; psychiatric symptoms.', [R(Md, '5')])],
     exs=[ex('narco', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('swd', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Xy = fda('xyrem', 'FDA Xyrem', 'Xyrem (sodium oxybate) oral solution 0.5 g/mL — Prescribing Information', sid('xyrem'))
drug('sodium-oxybate', 'nervous-system', 'سدیم اکسی‌بات', 'Sodium oxybate', T('مضعف CNS (GHB)', 'CNS depressant (GHB)'), [{'name': 'Xyrem', 'market': 'US'}], ['xyrem', 'زایرم', 'GHB', 'اکسی بات'],
     [form('sol', 'solution', 'oral', '0.5 g/mL oral solution', 0.5, 'g', [R(Xy, '3')], vol=1)],
     [NC('narco', 'narcolepsy', 'نارکولپسی (کاتاپلکسی یا خواب‌آلودگی) — بزرگسال ۴٫۵ g شبانه در دو دوز، تا ۶ تا ۹ g', 'Narcolepsy (cataplexy or sleepiness) — adult 4.5 g per night in two doses, up to 6–9 g', A18,
         'شبانه در دو نوبت: نیمی هنگام رفتن به رختخواب و نیمی ۲٫۵ تا ۴ ساعت بعد. افزایش هفتگی ۱٫۵ g/شب تا ۶ تا ۹ g. کودک ۷ سال به بالا: بر اساس جدول وزن برچسب. شروع دیوالپروکس: ۲۰٪ کاهش.', 'At night in two doses: half at bedtime, half 2.5–4 h later. Increase by 1.5 g/night weekly to 6–9 g. Children ≥7 y: per label weight table. Starting divalproex: reduce by 20%.', [R(Xy, '2.1'), R(Xy, '2.2'), R(Xy, '2.5')])],
     [CI('ci', 'همراه داروهای خواب‌آور یا الکل؛ کمبود سوکسینیک سمی‌آلدئید دهیدروژناز.', 'With sedative hypnotics or alcohol; succinic semialdehyde dehydrogenase deficiency.', [R(Xy, '4')])],
     warn=[W('هشدار جعبه‌ای: دپرسیون CNS و تنفس؛ سوءمصرف (GHB)؛ فقط از طریق برنامه REMS.', 'Boxed warning: CNS and respiratory depression; abuse and misuse (GHB); available only through REMS.', [R(Xy, 'Boxed Warning')])])

Wk = fda('wakix', 'FDA Wakix', 'Wakix (pitolisant) tablets — Prescribing Information', sid('wakix'))
drug('pitolisant', 'nervous-system', 'پیتولیسانت', 'Pitolisant', T('آنتاگونیست/آگونیست معکوس H3', 'H3 antagonist/inverse agonist'), [{'name': 'Wakix', 'market': 'US'}], ['wakix', 'واکیکس', 'پیتولیسانت'],
     [tab('tab-17', 17.8, '17.8 mg tablet', [R(Wk, '3')]), tab('tab-4', 4.45, '4.45 mg tablet', [R(Wk, '3')])],
     [reg('narco', 'narcolepsy', T('خواب‌آلودگی روزانه یا کاتاپلکسی در نارکولپسی — بزرگسال ۱۷٫۸ تا ۳۵٫۶ mg صبح', 'Daytime sleepiness or cataplexy in narcolepsy — adult 17.8–35.6 mg in the morning'), A18, 'fixed', {'perDose': 17.8, 'perDoseMax': 35.6, 'dosesPerDay': 1}, [R(Wk, '2.2')],
          notes=[note('هفته ۱: ۸٫۹ mg؛ هفته ۲: ۱۷٫۸؛ هفته ۳: تا ۳۵٫۶ mg. eGFR زیر ۶۰، نارسایی متوسط کبد یا متابولیزر ضعیف CYP2D6: حداکثر ۱۷٫۸ mg.', 'Week 1: 8.9 mg; week 2: 17.8; week 3: up to 35.6 mg. eGFR <60, moderate hepatic impairment or CYP2D6 poor metabolisers: max 17.8 mg.', [R(Wk, '2.2'), R(Wk, '2.4'), R(Wk, '2.5'), R(Wk, '2.7')])])],
     [CI('ci', 'حساسیت به پیتولیسانت؛ نارسایی شدید کبد.', 'Hypersensitivity to pitolisant; severe hepatic impairment.', [R(Wk, '4')])],
     warn=[W('طولانی شدن QT — با سایر داروهای افزاینده QT پرهیز.', 'QT prolongation — avoid with other QT-prolonging drugs.', [R(Wk, '5')])],
     exs=[ex('narco', 'tab-17', {'perDose': 17.8, 'tabletsPerDoseRounded': 1, 'upperPerDose': 35.6}, ageYears=30, weightKg=70)])

Bs = fda('belsomra', 'FDA Belsomra', 'Belsomra (suvorexant) tablets — Prescribing Information', sid('belsomra'))
drug('suvorexant', 'nervous-system', 'سووورکسانت', 'Suvorexant', T('آنتاگونیست گیرنده اورکسین', 'Orexin receptor antagonist'), [{'name': 'Belsomra', 'market': 'US'}], ['belsomra', 'بلسومرا', 'سووورکسانت'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Bs, '3')]) for m in (5, 10, 15, 20)],
     [reg('ins', 'insomnia', T('بی‌خوابی (شروع یا تداوم خواب) — ۱۰ mg ۳۰ دقیقه قبل از خواب (حداکثر ۲۰ mg)', 'Insomnia (onset or maintenance) — 10 mg within 30 min of bedtime (max 20 mg)'), A18, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [R(Bs, '2.1')],
          notes=[note('حداکثر یک بار در شب با دست‌کم ۷ ساعت تا بیداری. با مهارکننده متوسط CYP3A ← ۵ mg؛ با مهارکننده قوی توصیه نمی‌شود.', 'No more than once per night with at least 7 h before waking. Moderate CYP3A inhibitors → 5 mg; strong inhibitors not recommended.', [R(Bs, '2.1'), R(Bs, '2.4')])])],
     [CI('narco', 'نارکولپسی.', 'Narcolepsy.', [R(Bs, '4')])],
     warn=[W('خواب‌آلودگی روز بعد (رانندگی)؛ رفتارهای پیچیده خواب؛ فلج خواب و توهم.', 'Next-day impairment (driving); complex sleep behaviours; sleep paralysis and hallucinations.', [R(Bs, '5')])],
     exs=[ex('ins', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'upperPerDose': 20}, ageYears=50, weightKg=70)])

# ===================== migraine =====================
Am = fda('aimovig', 'FDA Aimovig', 'Aimovig (erenumab) — Prescribing Information', sid('aimovig'))
drug('erenumab', 'nervous-system', 'ارنومب', 'Erenumab', T('آنتی‌بادی ضد گیرنده CGRP', 'Anti-CGRP receptor antibody'), [{'name': 'Aimovig', 'market': 'US'}], ['aimovig', 'آیموویگ', 'ارنوماب'],
     [form('pen-70', 'injection', 'sc', '70 mg/mL or 140 mg/mL autoinjector', 70, 'mg', [R(Am, '3')], vol=1)],
     [reg('mig', 'migraine-prophylaxis', T('پیشگیری از میگرن بزرگسال — ۷۰ mg ماهی یک بار (برخی ۱۴۰ mg)', 'Adult migraine prevention — 70 mg once MONTHLY (some 140 mg)'), A18, 'fixed', {'perDose': 70, 'perDoseMax': 140, 'dosesPerDay': 1}, [R(Am, '2.1')], dur=ONE,
          notes=[note('یک دوز در ماه (نه روزانه) زیرجلدی.', 'One SC dose per MONTH (not daily).', [R(Am, '2.1')])])],
     [CI('hyper', 'حساسیت جدی به ارنومب (آنافیلاکسی، آنژیوادم).', 'Serious hypersensitivity to erenumab (anaphylaxis, angioedema).', [R(Am, '4')])],
     warn=[W('یبوست شدید؛ افزایش یا بدتر شدن فشار خون.', 'Severe constipation; new or worsening hypertension.', [R(Am, '5')])],
     exs=[ex('mig', 'pen-70', {'perDose': 70, 'mlPerDose': 1, 'upperPerDose': 140}, ageYears=35, weightKg=65)])
Eg = fda('emgality', 'FDA Emgality', 'Emgality (galcanezumab) — Prescribing Information', sid('emgality'))
drug('galcanezumab', 'nervous-system', 'گالکانزومب', 'Galcanezumab', T('آنتی‌بادی ضد CGRP', 'Anti-CGRP antibody'), [{'name': 'Emgality', 'market': 'US'}], ['emgality', 'امگالیتی', 'گالکانزوماب'],
     [form('pen-120', 'injection', 'sc', '120 mg/mL pen or syringe (100 mg/mL for cluster)', 120, 'mg', [R(Eg, '3')], vol=1)],
     [NC('mig', 'migraine-prophylaxis', 'پیشگیری از میگرن — بارگذاری ۲۴۰ mg، سپس ۱۲۰ mg ماهانه', 'Migraine prevention — 240 mg load, then 120 mg monthly', A18, 'دوز اول ۲۴۰ mg (دو تزریق ۱۲۰)، سپس ۱۲۰ mg ماهی یک بار زیرجلدی.', 'First dose 240 mg (two 120 mg injections), then 120 mg SC once monthly.', [R(Eg, '2.1')]),
      NC('cluster', 'migraine-acute', 'سردرد خوشه‌ای دوره‌ای — ۳۰۰ mg در شروع دوره، سپس ماهانه تا پایان دوره', 'Episodic cluster headache — 300 mg at onset of the cluster period, then monthly until it ends', A18,
         '۳۰۰ mg (سه تزریق ۱۰۰ mg) در شروع دوره خوشه‌ای و سپس ماهانه تا پایان دوره.', '300 mg (three 100 mg injections) at the start of the cluster period, then monthly until the period ends.', [R(Eg, '2.2')])],
     [CI('hyper', 'حساسیت جدی به گالکانزومب.', 'Serious hypersensitivity to galcanezumab.', [R(Eg, '4')])])
Ub = fda('ubrelvy', 'FDA Ubrelvy', 'Ubrelvy (ubrogepant) tablets — Prescribing Information', sid('ubrelvy'))
drug('ubrogepant', 'nervous-system', 'اوبروجپانت', 'Ubrogepant', T('آنتاگونیست گیرنده CGRP (ژپانت)', 'CGRP receptor antagonist (gepant)'), [{'name': 'Ubrelvy', 'market': 'US'}], ['ubrelvy', 'اوبرلوی', 'اوبروجپانت'],
     [tab('tab-50', 50, '50 mg tablet', [R(Ub, '3')]), tab('tab-100', 100, '100 mg tablet', [R(Ub, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن — ۵۰ یا ۱۰۰ mg؛ دوز دوم دست‌کم ۲ ساعت بعد (حداکثر ۲۰۰ mg/۲۴ ساعت)', 'Acute migraine — 50 or 100 mg; a second dose ≥2 h later (max 200 mg/24 h)'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 1}, [R(Ub, '2.1')],
          limits={'maxPerDay': 200, 'refs': [R(Ub, '2.1')]}, notes=[note('درمان بیش از ۸ میگرن در ۳۰ روز بررسی نشده. نارسایی شدید کبد یا کلیه: ۵۰ mg.', 'Treating more than 8 migraines in 30 days not studied. Severe hepatic or renal impairment: 50 mg.', [R(Ub, '2.1'), R(Ub, '2.2')])])],
     [CI('ci', 'مهارکننده قوی CYP3A4 همزمان؛ سابقه حساسیت جدی به اوبروجپانت.', 'Concomitant strong CYP3A4 inhibitors; history of serious hypersensitivity to ubrogepant.', [R(Ub, '4')])],
     exs=[ex('acute', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'upperPerDose': 100}, ageYears=35, weightKg=65)])

# ===================== psychiatry =====================
Vr = fda('vraylar', 'FDA Vraylar', 'Vraylar (cariprazine) capsules — Prescribing Information', sid('vraylar'))
drug('cariprazine', 'nervous-system', 'کاریپرازین', 'Cariprazine', T('آنتی‌سایکوتیک آتیپیک', 'Atypical antipsychotic'), [{'name': 'Vraylar', 'market': 'US'}], ['vraylar', 'reagila', 'ورایلار', 'کاریپرازین'],
     [tab(f'cap-{m}'.replace('.', '-'), m, f'{m} mg capsule', [R(Vr, '3')], per='capsule', form_='capsule') for m in (1.5, 3, 4.5, 6)],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — شروع ۱٫۵ mg، محدوده ۱٫۵ تا ۶ mg یک بار در روز', 'Adult schizophrenia — start 1.5 mg, range 1.5–6 mg once daily'), A18, 'fixed', {'perDose': 1.5, 'perDoseMax': 6, 'dosesPerDay': 1}, [R(Vr, '2.2')],
          notes=[note('روز ۲ می‌تواند ۳ mg شود. به دلیل نیمه‌عمر طولانی، اثر تغییر دوز تا چند هفته دیده می‌شود.', 'May increase to 3 mg on day 2. Long half-life: dose changes take weeks to show.', [R(Vr, '2.2'), R(Vr, '2.1')])]),
      reg('mania', 'bipolar-mania', T('مانیا یا دوره مختلط دوقطبی I — ۱٫۵ mg، روز ۲ ← ۳ mg؛ محدوده ۳ تا ۶ mg', 'Bipolar I manic/mixed — 1.5 mg, day 2 → 3 mg; range 3–6 mg'), A18, 'fixed', {'perDose': 3, 'perDoseMax': 6, 'dosesPerDay': 1}, [R(Vr, '2.3')]),
      reg('bpd', 'bipolar-depression', T('افسردگی دوقطبی I — ۱٫۵ mg، روز ۱۵ تا ۳ mg', 'Bipolar I depression — 1.5 mg, up to 3 mg on day 15'), A18, 'fixed', {'perDose': 1.5, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Vr, '2.4')]),
      reg('mdd', 'mdd', T('افسردگی اساسی (کمکی ضدافسردگی) — ۱٫۵ mg، روز ۱۵ تا ۳ mg', 'MDD (adjunct to antidepressant) — 1.5 mg, up to 3 mg on day 15'), A18, 'fixed', {'perDose': 1.5, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Vr, '2.5')])],
     [CI('hyper', 'سابقه حساسیت به کاریپرازین.', 'History of hypersensitivity to cariprazine.', [R(Vr, '4')])], warn=[DEM(Vr)],
     exs=[ex('scz', 'cap-1-5', {'perDose': 1.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 6}, ageYears=30, weightKg=75), ex('mania', 'cap-3', {'perDose': 3, 'tabletsPerDoseRounded': 1, 'upperPerDose': 6}, ageYears=30, weightKg=75),
          ex('bpd', 'cap-1-5', {'perDose': 1.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 3}, ageYears=30, weightKg=75), ex('mdd', 'cap-1-5', {'perDose': 1.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 3}, ageYears=40, weightKg=75)])

Rx = fda('rexulti', 'FDA Rexulti', 'Rexulti (brexpiprazole) tablets — Prescribing Information', sid('rexulti'))
drug('brexpiprazole', 'nervous-system', 'برکس‌پیپرازول', 'Brexpiprazole', T('آنتی‌سایکوتیک آتیپیک', 'Atypical antipsychotic'), [{'name': 'Rexulti', 'market': 'US'}], ['rexulti', 'رکسولتی', 'برکسپیپرازول'],
     [tab(f'tab-{m}'.replace('.', '-'), m, f'{m} mg tablet', [R(Rx, '3')]) for m in (0.5, 1, 2, 3, 4)],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی بزرگسال — ۱ mg روز ۱ تا ۴، ۲ mg روز ۵ تا ۷، سپس تا ۴ mg', 'Adult schizophrenia — 1 mg days 1–4, 2 mg days 5–7, then up to 4 mg'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 4, 'dosesPerDay': 1}, [R(Rx, '2.3')]),
      reg('mdd', 'mdd', T('افسردگی اساسی (کمکی) — شروع ۰٫۵ یا ۱ mg، هدف ۲ mg (حداکثر ۳)', 'MDD (adjunct) — start 0.5 or 1 mg, target 2 mg (max 3)'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Rx, '2.2')],
          notes=[note('افزایش هفتگی بر اساس پاسخ.', 'Increase at weekly intervals by response.', [R(Rx, '2.2')])]),
      reg('agit', 'alzheimers', T('بی‌قراری ناشی از دمانس آلزایمر — ۰٫۵ mg روز ۱ تا ۷، ۱ mg روز ۸ تا ۱۴، از روز ۱۵ ← ۲ mg (حداکثر ۳)', 'Agitation with Alzheimer’s dementia — 0.5 mg days 1–7, 1 mg days 8–14, 2 mg from day 15 (max 3)'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Rx, '2.4')])],
     [CI('hyper', 'حساسیت به برکس‌پیپرازول.', 'Hypersensitivity to brexpiprazole.', [R(Rx, '4')])], warn=[DEM(Rx)],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr زیر ۶۰: حداکثر ۲ mg (MDD، بی‌قراری) یا ۳ mg (اسکیزوفرنی).', 'CrCl <60: max 2 mg (MDD, agitation) or 3 mg (schizophrenia).'), 'refs': [R(Rx, '2.6')]}],
     exs=[ex('scz', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1, 'upperPerDose': 4}, ageYears=30, weightKg=75), ex('mdd', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70),
          ex('agit', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=80, weightKg=60)])

Sp = fda('spravato', 'FDA Spravato', 'Spravato (esketamine) nasal spray — Prescribing Information', sid('spravato'))
drug('esketamine', 'nervous-system', 'اس‌کتامین (اسپری بینی)', 'Esketamine (nasal)', T('آنتاگونیست NMDA', 'NMDA antagonist'), [{'name': 'Spravato', 'market': 'US'}], ['spravato', 'اسپراواتو', 'اسکتامین'],
     [form('device', 'nasal-spray', 'nasal', '28 mg per device (two sprays)', 28, 'mg', [R(Sp, '3')], per='spray')],
     [NC('trd', 'mdd', 'افسردگی مقاوم به درمان — ۵۶ یا ۸۴ mg دو بار در هفته (القا)، سپس کمتر', 'Treatment-resistant depression — 56 or 84 mg twice weekly (induction), then less often', A18,
         'فقط در مرکز درمانی تحت نظر و پایش دست‌کم ۲ ساعت پس از هر نوبت؛ فشار خون قبل و بعد. برنامه هفته‌ها طبق جدول ۱ برچسب. افکار خودکشی حاد: ۸۴ mg دو بار در هفته ۴ هفته همراه ضدافسردگی.', 'Only in a certified healthcare setting with ≥2 h observation after each session; check BP before and after. Weekly schedule per label Table 1. Acute suicidal ideation: 84 mg twice weekly for 4 weeks with an antidepressant.', [R(Sp, '2.2'), R(Sp, '2.3'), R(Sp, '2.5')])],
     [CI('ci', 'بیماری آنوریسمی عروق یا AVM؛ سابقه خونریزی داخل مغز؛ حساسیت به اس‌کتامین یا کتامین.', 'Aneurysmal vascular disease or AVM; history of intracerebral haemorrhage; hypersensitivity to esketamine or ketamine.', [R(Sp, '4')])],
     warn=[W('هشدار جعبه‌ای: آرام‌بخشی، تجزیه (دیسوسیاسیون)، دپرسیون تنفسی، سوءمصرف، افکار خودکشی؛ فقط از طریق REMS.', 'Boxed warning: sedation, dissociation, respiratory depression, abuse and misuse, suicidal thoughts; REMS only.', [R(Sp, 'Boxed Warning')])])

Vd = uk('emc-valdoxan', 'eMC Valdoxan', 'Valdoxan (agomelatine) 25 mg film-coated tablets — SmPC', 'Servier Laboratories', '15 April 2026', 6564)
drug('agomelatine', 'nervous-system', 'آگوملاتین', 'Agomelatine', T('آگونیست ملاتونین و آنتاگونیست 5-HT2C', 'Melatonergic agonist and 5-HT2C antagonist'), [{'name': 'Valdoxan', 'market': 'UK'}], ['valdoxan', 'والدوکسان', 'آگوملاتین'],
     [tab('tab-25', 25, '25 mg film-coated tablet', [R(Vd, '6.5')], markets=('UK',))],
     [reg('mdd', 'mdd', T('افسردگی اساسی بزرگسال — ۲۵ mg هنگام خواب؛ پس از ۲ هفته بدون بهبود تا ۵۰ mg', 'Adult major depression — 25 mg at bedtime; 50 mg if no improvement after 2 weeks'), A18, 'fixed', {'perDose': 25, 'perDoseMax': 50, 'dosesPerDay': 1}, [R(Vd, '4.2')],
          notes=[note('آزمایش کبد پیش از شروع و حدود ۳، ۶، ۱۲ و ۲۴ هفته؛ ترانس‌آمیناز بالای ۳ برابر: شروع نشود و قطع شود. افزایش به ۵۰ mg با پایش دقیق کبد.', 'Liver tests before starting and at about 3, 6, 12 and 24 weeks; do not start (and stop) if transaminases exceed 3× ULN. Increase to 50 mg only with strict liver monitoring.', [R(Vd, '4.2')])])],
     [CI('ci', 'نارسایی کبد (سیروز یا بیماری فعال کبد) یا ترانس‌آمیناز بالای ۳ برابر؛ مهارکننده قوی CYP1A2 (فلووکسامین، سیپروفلوکساسین)؛ حساسیت.', 'Hepatic impairment (cirrhosis or active liver disease) or transaminases >3× ULN; potent CYP1A2 inhibitors (fluvoxamine, ciprofloxacin); hypersensitivity.', [R(Vd, '4.3')])],
     warn=[W('آسیب کبدی (گاه نارسایی کبد)؛ پایش آزمایش کبد.', 'Liver injury (occasionally hepatic failure); monitor liver tests.', [R(Vd, '4.4')])],
     exs=[ex('mdd', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1, 'upperPerDose': 50}, ageYears=40, weightKg=70)])

# ===================== anti-infective / obstetric / metabolic =====================
Cs = fda('cancidas', 'FDA Cancidas', 'Cancidas (caspofungin) for injection 50/70 mg — Prescribing Information', sid('caspo'))
drug('caspofungin', 'anti-infectives', 'کاسپوفانژین', 'Caspofungin', T('اکینوکاندین (ضدقارچ)', 'Echinocandin antifungal'), [{'name': 'Cancidas', 'market': 'US'}], ['cancidas', 'کانسیداس', 'کاسپوفانژین'],
     [form('vial-50', 'powder-for-injection', 'iv', '50 mg vial', 50, 'mg', [R(Cs, '3')], per='vial'), form('vial-70', 'powder-for-injection', 'iv', '70 mg vial', 70, 'mg', [R(Cs, '3')], per='vial')],
     [reg('load', 'invasive-fungal', T('کاندیدمی، تب نوتروپنیک، آسپرژیلوز مقاوم — بزرگسال: روز ۱ دوز بارگذاری ۷۰ mg', 'Candidaemia, febrile neutropenia, refractory aspergillosis — adult: day 1 loading 70 mg'), A18, 'fixed', {'perDose': 70, 'dosesPerDay': 1}, [R(Cs, '2.2')], dur=ONE, allowed=['vial-70']),
      reg('maint', 'invasive-fungal', T('نگهدارنده بزرگسال — ۵۰ mg یک بار در روز از روز ۲', 'Adult maintenance — 50 mg once daily from day 2'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Cs, '2.2')], allowed=['vial-50'],
          notes=[note('کاندیدمی: دست‌کم ۱۴ روز پس از آخرین کشت مثبت. نارسایی متوسط کبد: ۳۵ mg روزانه. انفوزیون ۱ ساعت؛ با دکستروز رقیق نشود.', 'Candidaemia: at least 14 days after the last positive culture. Moderate hepatic impairment: 35 mg daily. 1-hour infusion; no dextrose diluents.', [R(Cs, '2.2'), R(Cs, '2.4'), R(Cs, '2.7')])]),
      reg('eso', 'esophageal-candidiasis', T('کاندیدیاز مری — بزرگسال ۵۰ mg روزانه تا ۷ تا ۱۴ روز پس از بهبود', 'Oesophageal candidiasis — adult 50 mg daily until 7–14 days after symptoms resolve'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Cs, '2.2')], allowed=['vial-50'],
          notes=[note('بارگذاری ۷۰ mg در این اندیکاسیون بررسی نشده.', 'A 70 mg load has not been studied for this indication.', [R(Cs, '2.2')])]),
      reg('child', 'invasive-fungal', T('کودک ۳ ماه تا ۱۷ سال — روز ۱: ۷۰ mg/m²، سپس ۵۰ mg/m² روزانه (حداکثر ۷۰ mg)', 'Children 3 months–17 y — day 1: 70 mg/m², then 50 mg/m² daily (max 70 mg)'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year')}, 'bsa', {'perM2PerDay': 50, 'dividedDoses': 1}, [R(Cs, '2.3')],
          limits={'maxPerDose': 70, 'refs': [R(Cs, '2.3')]}, notes=[note('عدد ماشین‌حساب دوز نگهدارنده ۵۰ mg/m² است؛ روز اول ۷۰ mg/m² (حداکثر ۷۰ mg). BSA با فرمول Mosteller.', 'The calculator gives the 50 mg/m² maintenance dose; day 1 is 70 mg/m² (max 70 mg). BSA by Mosteller.', [R(Cs, '2.3')])])],
     [CI('hyper', 'حساسیت (مثلاً آنافیلاکسی) به اجزای فرآورده.', 'Hypersensitivity (e.g. anaphylaxis) to any component.', [R(Cs, '4')])],
     inter=[IA('cyclosporine', 'سیکلوسپورین: افزایش ALT — فقط اگر سود بیشتر باشد.', 'Cyclosporine: raised ALT — use only if benefit outweighs risk.', [R(Cs, '5.3')])],
     exs=[ex('load', 'vial-70', {'perDose': 70}, ageYears=50, weightKg=70), ex('maint', 'vial-50', {'perDose': 50}, ageYears=50, weightKg=70), ex('eso', 'vial-50', {'perDose': 50}, ageYears=40, weightKg=60),
          ex('child', 'vial-50', {'perDose': 50}, ageYears=10, weightKg=36, heightCm=100)])

Vk = fda('veklury', 'FDA Veklury', 'Veklury (remdesivir) for injection 100 mg — Prescribing Information', sid('veklury'))
VKN = note('بستری بدون ونتیلاتور: ۵ روز (در صورت عدم بهبود تا ۱۰)؛ ونتیلاتور یا ECMO: ۱۰ روز. آزمایش کبد و PT پیش از شروع. نارسایی کلیه تنظیم ندارد.', 'Hospitalised without ventilation: 5 days (up to 10 if no improvement); ventilation/ECMO: 10 days. Liver tests and PT before starting. No renal adjustment.', [R(Vk, '2.3'), R(Vk, '2.2'), R(Vk, '2.4')])
drug('remdesivir', 'anti-infectives', 'رمدسیویر', 'Remdesivir', T('مهارکننده RNA پلیمراز ویروسی', 'Viral RNA polymerase inhibitor'), [{'name': 'Veklury', 'market': 'US'}], ['veklury', 'وکلوری', 'رمدسیویر', 'remdeiran'],
     [form('vial-100', 'powder-for-injection', 'iv', '100 mg vial', 100, 'mg', [R(Vk, '3')], per='vial')],
     [reg('load', 'covid-19', T('کووید-۱۹ — بزرگسال و کودک ≥۴۰ kg: روز ۱ دوز بارگذاری ۲۰۰ mg', 'COVID-19 — adults and children ≥40 kg: day 1 loading 200 mg'), {'minWeightKg': 40}, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Vk, '2.3')], dur=ONE, notes=[VKN]),
      reg('maint', 'covid-19', T('نگهدارنده — ≥۴۰ kg: ۱۰۰ mg یک بار در روز از روز ۲', 'Maintenance — ≥40 kg: 100 mg once daily from day 2'), {'minWeightKg': 40}, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Vk, '2.3')], dur={'min': 4, 'max': 9}, notes=[VKN]),
      reg('child-load', 'covid-19', T('کودک ≥۲۸ روز و ۳ تا <۴۰ kg — روز ۱: ۵ mg/kg', 'Child ≥28 days and 3–<40 kg — day 1: 5 mg/kg'), {'minAge': age(28, 'day'), 'minWeightKg': 3, 'maxWeightKg': 39.99}, 'weightBased', {'perKgPerDose': 5, 'intervalHours': 24}, [R(Vk, '2.3, Table 1')], dur=ONE, notes=[VKN]),
      reg('child-maint', 'covid-19', T('کودک ≥۲۸ روز و ۳ تا <۴۰ kg — از روز ۲: ۲٫۵ mg/kg یک بار در روز', 'Child ≥28 days and 3–<40 kg — from day 2: 2.5 mg/kg once daily'), {'minAge': age(28, 'day'), 'minWeightKg': 3, 'maxWeightKg': 39.99}, 'weightBased', {'perKgPerDose': 2.5, 'intervalHours': 24}, [R(Vk, '2.3, Table 1')], notes=[VKN,
          note('نوزاد زیر ۲۸ روز (≥۱٫۵ kg): ۲٫۵ mg/kg روز ۱، سپس ۱٫۲۵ mg/kg.', 'Neonates <28 days (≥1.5 kg): 2.5 mg/kg day 1, then 1.25 mg/kg.', [R(Vk, '2.3, Table 1')])])],
     [CI('hyper', 'سابقه حساسیت قابل‌توجه به رمدسیویر.', 'History of clinically significant hypersensitivity to remdesivir.', [R(Vk, '4')])],
     warn=[W('واکنش انفوزیون و حساسیت؛ افزایش ترانس‌آمیناز.', 'Infusion-related and hypersensitivity reactions; transaminase elevations.', [R(Vk, '5')])],
     exs=[ex('load', 'vial-100', {'perDose': 200}, ageYears=50, weightKg=75), ex('maint', 'vial-100', {'perDose': 100}, ageYears=50, weightKg=75), ex('child-load', 'vial-100', {'perDose': 100}, ageYears=6, weightKg=20), ex('child-maint', 'vial-100', {'perDose': 50}, ageYears=6, weightKg=20)])

Pd = fda('prepidil', 'FDA Prepidil', 'Prepidil (dinoprostone 0.5 mg) endocervical gel — Prescribing Information', sid('cervidil')); d = R(Pd, 'Dosage and Administration')
drug('dinoprostone', 'genitourinary-sex-hormones', 'دینوپروستون (ژل داخل سرویکس)', 'Dinoprostone (endocervical gel)', T('پروستاگلاندین E2', 'Prostaglandin E2'), [{'name': 'Prepidil', 'market': 'US'}], ['prepidil', 'cervidil', 'prostin', 'دینوپروستون', 'پروستین'],
     [form('gel', 'gel', 'vaginal', '0.5 mg dinoprostone in 3 g (2.5 mL) gel syringe with endocervical catheter', 0.5, 'mg', [R(Pd, 'How Supplied')], per='application')],
     [reg('ripen', 'labor-induction', T('آماده‌سازی دهانه رحم در زمان ترم — ۰٫۵ mg داخل سرویکس؛ تکرار ۰٫۵ mg هر ۶ ساعت (حداکثر ۱٫۵ mg/۲۴ ساعت)', 'Cervical ripening at term — 0.5 mg endocervical; repeat 0.5 mg every 6 h (max 1.5 mg/24 h)'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [d],
          limits={'maxPerDay': 1.5, 'refs': [d]}, notes=[note('فقط در بیمارستان با امکانات مراقبت ویژه و جراحی. بیمار ۱۵ تا ۳۰ دقیقه درازکش بماند. شروع اکسی‌توسین ۶ تا ۱۲ ساعت پس از پاسخ.', 'Hospital only, with intensive care and surgery available. Keep supine for 15–30 min. Start oxytocin 6–12 h after response.', [d, R(Pd, 'Warnings')])])],
     [CI('ci', 'هر جا داروی اکسی‌توسیک منع دارد یا انقباض طولانی رحم نامناسب است (سزارین یا جراحی بزرگ رحم قبلی، عدم تناسب سر و لگن، دیسترس جنین بدون زایمان قریب‌الوقوع)؛ جفت سرراهی یا خونریزی واژینال بی‌علت؛ وقتی زایمان طبیعی مناسب نیست؛ حساسیت به پروستاگلاندین.', 'Where oxytocics are contraindicated or prolonged contractions are inappropriate (previous Caesarean or major uterine surgery, cephalopelvic disproportion, fetal distress without imminent delivery); placenta praevia or unexplained vaginal bleeding; when vaginal delivery is not indicated; prostaglandin hypersensitivity.', [R(Pd, 'Contraindications')])],
     warn=[W('فقط در بیمارستان؛ دقیقاً با دوز توصیه‌شده. خطر انعقاد درون‌عروقی منتشر در زنان ۳۰ سال به بالا، عوارض بارداری و بارداری بالای ۴۰ هفته.', 'Hospital use only; strict adherence to dosing. Increased risk of DIC in women ≥30 y, with pregnancy complications or gestation >40 weeks.', [R(Pd, 'Warnings')])],
     exs=[ex('ripen', 'gel', {'perDose': 0.5}, ageYears=28, weightKg=70)])

Lv = fda('levemir', 'FDA Levemir', 'Levemir (insulin detemir) — Prescribing Information (repackager listing)', sid('levemir'))
drug('insulin-detemir', 'alimentary-metabolism', 'انسولین دتمیر', 'Insulin detemir', T('انسولین پایه طولانی‌اثر', 'Long-acting basal insulin'), [{'name': 'Levemir', 'market': 'US'}], ['levemir', 'لومیر', 'دتمیر'],
     [liquid('u100', 100, 1, '100 units/mL FlexPen or vial', [R(Lv, '3')], form_='injection', route='sc', unit='unit')],
     [reg('t2', 'type-2-diabetes', T('دیابت نوع ۲ — ۱۰ واحد (یا ۰٫۱ تا ۰٫۲ واحد/kg) یک بار عصر', 'Type 2 diabetes — 10 units (or 0.1–0.2 units/kg) once daily in the evening'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Lv, '2.3')], unit='unit',
          notes=[note('یک بار با شام یا هنگام خواب، یا تقسیم دو بار در روز. تنظیم بر اساس قند.', 'Once with the evening meal or at bedtime, or split twice daily. Titrate by glucose.', [R(Lv, '2.2'), R(Lv, '2.3')])]),
      NC('t1', 'type-1-diabetes', 'دیابت نوع ۱ — یک‌سوم تا نیمی از کل انسولین روزانه', 'Type 1 diabetes — one-third to one-half of total daily insulin', {}, 'کل انسولین روزانه به‌طور کلی ۰٫۲ تا ۰٫۴ واحد/kg؛ یک‌سوم تا نیمی دتمیر و بقیه انسولین کوتاه‌اثر با غذا.', 'Total daily insulin generally 0.2–0.4 units/kg; one-third to one-half as detemir, the rest as short-acting with meals.', [R(Lv, '2.3')])],
     [CI('ci', 'هنگام هیپوگلیسمی؛ حساسیت به انسولین دتمیر.', 'During hypoglycaemia; hypersensitivity to insulin detemir.', [R(Lv, '4')])],
     warn=[W('هیپوگلیسمی؛ هیپوکالمی؛ قلم مشترک ممنوع.', 'Hypoglycaemia; hypokalaemia; never share pens.', [R(Lv, '5')])],
     exs=[ex('t2', 'u100', {'perDose': 10, 'mlPerDose': 0.1}, ageYears=55, weightKg=90)])

Ap = fda('apidra', 'FDA Apidra', 'Apidra (insulin glulisine) — Prescribing Information', sid('apidra'))
drug('insulin-glulisine', 'alimentary-metabolism', 'انسولین گلولیزین', 'Insulin glulisine', T('انسولین سریع‌الاثر', 'Rapid-acting insulin'), [{'name': 'Apidra', 'market': 'US'}], ['apidra', 'آپیدرا', 'گلولیزین'],
     [liquid('u100', 100, 1, '100 units/mL vial or SoloStar pen', [R(Ap, '3')], form_='injection', route='sc', unit='unit')],
     [NC('dm', 'type-1-diabetes', 'دیابت — دوز فردی همراه غذا', 'Diabetes — individualised mealtime dose', {}, 'برچسب: دوز بر اساس نیاز متابولیک، پایش قند و هدف درمان فردی شود؛ زیرجلدی ظرف ۱۵ دقیقه قبل یا ۲۰ دقیقه پس از شروع غذا؛ معمولاً همراه انسولین پایه.', 'Label: individualise by metabolic needs, glucose monitoring and goals; SC within 15 min before or within 20 min after starting a meal; usually with a basal insulin.', [R(Ap, '2.3'), R(Ap, '2')])],
     [CI('ci', 'هنگام هیپوگلیسمی؛ حساسیت به انسولین گلولیزین.', 'During hypoglycaemia; hypersensitivity to insulin glulisine.', [R(Ap, '4')])],
     warn=[W('هیپوگلیسمی؛ هیپوکالمی؛ قلم مشترک ممنوع.', 'Hypoglycaemia; hypokalaemia; never share pens.', [R(Ap, '5')])])

Ev = fda('evenity', 'FDA Evenity', 'Evenity (romosozumab) 105 mg/1.17 mL — Prescribing Information', sid('evenity'))
drug('romosozumab', 'musculoskeletal', 'رموزوزومب', 'Romosozumab', T('مهارکننده اسکلروستین', 'Sclerostin inhibitor'), [{'name': 'Evenity', 'market': 'US'}], ['evenity', 'اونیتی', 'رموزوزوماب'],
     [form('syr-105', 'injection', 'sc', '105 mg/1.17 mL syringe (dose = 2 syringes)', 105, 'mg', [R(Ev, '3')], vol=1.17)],
     [reg('op', 'osteoporosis', T('پوکی استخوان پرخطر پس از یائسگی — ۲۱۰ mg ماهی یک بار، ۱۲ دوز', 'High-risk postmenopausal osteoporosis — 210 mg once MONTHLY, 12 doses'), A18, 'fixed', {'perDose': 210, 'dosesPerDay': 1}, [R(Ev, '2.2')], dur=ONE,
          notes=[note('یک دوز در ماه (نه روزانه) = دو سرنگ ۱۰۵ mg پشت سر هم توسط کادر درمان؛ ۱۲ ماه. کلسیم و ویتامین D کافی.', 'One dose per MONTH (not daily) = two 105 mg syringes one after the other by a healthcare provider; 12 months. Adequate calcium and vitamin D.', [R(Ev, '2.1'), R(Ev, '2.2')])])],
     [CI('ci', 'هیپوکلسمی (پیش از شروع اصلاح شود)؛ حساسیت سیستمیک به رموزوزومب.', 'Hypocalcaemia (correct before starting); systemic hypersensitivity to romosozumab.', [R(Ev, '4')])],
     warn=[W('هشدار جعبه‌ای: احتمال افزایش MI، سکته و مرگ قلبی — در MI یا سکته طی سال گذشته شروع نشود.', 'Boxed warning: possible increase in MI, stroke and cardiovascular death — do not start within a year of MI or stroke.', [R(Ev, 'Boxed Warning')])],
     exs=[ex('op', 'syr-105', {'perDose': 210, 'mlPerDose': 2.34}, ageYears=70, weightKg=60)])
print('s11f ok')
