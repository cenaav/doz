"""Stage 12d (part 2) — primidone, dementia (galantamine, lecanemab), Parkinson (rotigotine, apomorphine, selegiline, benztropine), onabotulinumtoxinA, triptans (zolmitriptan, eletriptan)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
cap = lambda id, mg, src, sec='3': tab(id, mg, f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
TRIP_CI = lambda src: CI('ci', 'بیماری ایسکمیک کرونر یا وازواسپاسم کرونر (پرینزمتال)؛ WPW یا آریتمی مسیر فرعی؛ سابقه سکته، TIA یا میگرن همی‌پلژیک/بازیلار؛ بیماری عروق محیطی؛ بیماری ایسکمیک روده؛ فشار خون کنترل‌نشده؛ تریپتان یا ارگوت دیگر ظرف ۲۴ ساعت؛ حساسیت.',
    'Ischaemic coronary disease or coronary vasospasm (Prinzmetal); WPW or accessory-pathway arrhythmias; history of stroke, TIA or hemiplegic/basilar migraine; peripheral vascular disease; ischaemic bowel disease; uncontrolled hypertension; another triptan or ergot within 24 h; hypersensitivity.', [R(src, '4')])
TRIP_W = lambda src: W('ایسکمی و انفارکتوس قلب؛ آریتمی؛ احساس فشار قفسه سینه، گلو یا فک؛ رویداد عروق مغزی؛ سردرد ناشی از مصرف زیاد دارو؛ سندرم سروتونین؛ افزایش فشار خون.', 'Myocardial ischaemia and infarction; arrhythmias; chest/throat/jaw tightness; cerebrovascular events; medication-overuse headache; serotonin syndrome; increased blood pressure.', [R(src, '5')])
DA_W = lambda src: W('به خواب رفتن ناگهانی حین فعالیت روزانه؛ توهم؛ افت فشار و سنکوپ؛ رفتار تکانشی و وسواسی (قمار، خرید)؛ دیسکینزی؛ تب و گیجی با قطع ناگهانی.', 'Falling asleep during daily activities; hallucinations; hypotension and syncope; impulse-control/compulsive behaviours (gambling, shopping); dyskinesia; hyperpyrexia and confusion on abrupt withdrawal.', [R(src, '5')])

add_disease('drug-induced-parkinsonism', 'عوارض اکستراپیرامیدال و پارکینسونیسم ناشی از دارو', 'Drug-induced extrapyramidal disorders and parkinsonism', ['EPS', 'اکستراپیرامیدال', 'پارکینسونیسم دارویی', 'دیستونی حاد'], ['G21.1'], 'neurology')

Pr = fda('primidone', 'FDA Primidone', 'Primidone tablets USP 50/250 mg — Prescribing Information', sid('primidone')); d = R(Pr, 'Dosage and Administration')
drug('primidone', 'nervous-system', 'پریمیدون', 'Primidone', T('ضدتشنج (دئوکسی‌باربیتورات)', 'Antiseizure (deoxybarbiturate)'), [{'name': 'Mysoline', 'market': 'US'}], ['mysoline', 'مایزولین', 'پریمیدون'],
     [tab('tab-250', 250, '250 mg tablet (scored)', [R(Pr, 'How Supplied')], scored=True), tab('tab-50', 50, '50 mg tablet (scored)', [R(Pr, 'How Supplied')], scored=True)],
     [reg('adult', 'epilepsy', T('صرع (تونیک-کلونیک، سایکوموتور، فوکال) — ۸ سال به بالا: نگهدارنده ۲۵۰ mg سه بار در روز', 'Epilepsy (tonic-clonic, psychomotor, focal) — ≥8 y: maintenance 250 mg three times daily'), {'minAge': age(8, 'year')}, 'fixed', {'perDose': 250, 'dosesPerDay': 3}, [d],
          limits={'maxPerDay': 2000, 'refs': [d]}, notes=[note('شروع ۱۰۰ تا ۱۲۵ mg هنگام خواب و طی ۱۰ روز افزایش (روز ۴: دو بار، روز ۷: سه بار، روز ۱۰: ۲۵۰ mg سه بار). معمولاً ۷۵۰ تا ۱۰۰۰ mg/روز؛ حداکثر ۵۰۰ mg چهار بار. سطح سرمی مؤثر ۵ تا ۱۲ µg/mL.', 'Start 100–125 mg at bedtime and build over 10 days (day 4: twice, day 7: three times, day 10: 250 mg three times). Usually 750–1000 mg/day; max 500 mg four times daily. Effective serum level 5–12 µg/mL.', [d])]),
      reg('child', 'epilepsy', T('کودک زیر ۸ سال — نگهدارنده ۱۲۵ تا ۲۵۰ mg سه بار در روز', 'Children under 8 y — maintenance 125–250 mg three times daily'), {'maxAge': age(8, 'year')}, 'fixed', {'perDose': 125, 'perDoseMax': 250, 'dosesPerDay': 3}, [d],
          notes=[note('یا ۱۰ تا ۲۵ mg/kg/روز تقسیمی. شروع ۵۰ mg هنگام خواب؛ روز ۴: ۵۰ mg دو بار؛ روز ۷: ۱۰۰ mg دو بار؛ روز ۱۰: نگهدارنده.', 'Or 10–25 mg/kg/day divided. Start 50 mg at bedtime; day 4: 50 mg twice; day 7: 100 mg twice; day 10: maintenance.', [d])])],
     [CI('ci', 'پورفیری؛ حساسیت به فنوباربیتال.', 'Porphyria; hypersensitivity to phenobarbital.', [R(Pr, 'Contraindications')])],
     warn=[W('قطع ناگهانی ممکن است استاتوس صرعی ایجاد کند؛ اثر درمانی چند هفته طول می‌کشد.', 'Abrupt withdrawal may precipitate status epilepticus; therapeutic efficacy takes several weeks to assess.', [R(Pr, 'Warnings')])],
     exs=[ex('adult', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1, 'perDay': 750}, ageYears=30, weightKg=70), ex('child', 'tab-250', {'perDose': 125, 'tabletsPerDoseRounded': 0.5, 'upperPerDose': 250}, ageYears=5, weightKg=18)])

Gl = fda('galantamine', 'FDA Galantamine', 'Galantamine tablets USP 4/8/12 mg — Prescribing Information', sid('galantamine'))
drug('galantamine', 'nervous-system', 'گالانتامین', 'Galantamine', T('مهارکننده کولین‌استراز', 'Cholinesterase inhibitor'), [{'name': 'Razadyne', 'market': 'US'}], ['razadyne', 'reminyl', 'رمینیل', 'گالانتامین'],
     [tab('tab-4', 4, '4 mg tablet', [R(Gl, '3')]), tab('tab-8', 8, '8 mg tablet', [R(Gl, '3')]), tab('tab-12', 12, '12 mg tablet', [R(Gl, '3')])],
     [reg('ad', 'alzheimers', T('دمانس خفیف تا متوسط آلزایمر — نگهدارنده ۸ mg دو بار (تا ۱۲ mg دو بار)؛ شروع ۴ mg دو بار', 'Mild to moderate Alzheimer dementia — maintenance 8 mg twice daily (up to 12 mg twice daily); start 4 mg twice daily'), A18, 'fixed', {'perDose': 8, 'perDoseMax': 12, 'dosesPerDay': 2}, [R(Gl, '2.2')],
          notes=[note('شروع ۴ mg دو بار، پس از دست‌کم ۴ هفته ۸ mg دو بار و پس از ۴ هفته دیگر تا ۱۲ mg دو بار. با غذا و مایعات کافی. نارسایی متوسط کبد حداکثر ۱۶ mg/روز؛ شدید توصیه نمی‌شود.', 'Start 4 mg twice daily; after ≥4 weeks 8 mg twice daily; after another 4 weeks up to 12 mg twice daily. With meals and adequate fluids. Moderate hepatic impairment max 16 mg/day; severe not recommended.', [R(Gl, '2.2'), R(Gl, '2.3')])])],
     [CI('hyper', 'حساسیت به گالانتامین.', 'Hypersensitivity to galantamine.', [R(Gl, '4')])],
     warn=[W('واکنش پوستی شدید (SJS)؛ برادیکاردی و بلوک قلبی؛ خونریزی گوارشی؛ انسداد ادراری؛ تشنج؛ تشدید آسم/COPD؛ تشدید شل‌کننده‌های عضلانی سوکسینیل‌کولینی در بیهوشی.', 'Serious skin reactions (SJS); bradycardia and heart block; GI bleeding; urinary outflow obstruction; seizures; asthma/COPD; exaggerates succinylcholine-type relaxation in anaesthesia.', [R(Gl, '5')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr ۹ تا ۵۹: حداکثر ۱۶ mg/روز؛ زیر ۹ توصیه نمی‌شود.', 'CrCl 9–59: max 16 mg/day; below 9 not recommended.'), 'refs': [R(Gl, '2.4')]}],
     exs=[ex('ad', 'tab-4', {'perDose': 8, 'tabletsPerDoseRounded': 2, 'upperPerDose': 12}, ageYears=75, weightKg=65)])

Lq = fda('leqembi', 'FDA Leqembi', 'Leqembi / Leqembi Iqlik (lecanemab-irmb) — Prescribing Information', sid('lecanemab'))
drug('lecanemab', 'nervous-system', 'لکانماب', 'Lecanemab', T('آنتی‌بادی ضدآمیلوئید بتا', 'Anti-amyloid-beta antibody'), [{'name': 'Leqembi', 'market': 'US'}], ['leqembi', 'لکمبی', 'لکانماب'],
     [form('vial-100', 'injection', 'iv', '100 mg/mL vial (500 mg/5 mL, 200 mg/2 mL)', 100, 'mg', [R(Lq, '3')], vol=1)],
     [once('iv', 'alzheimers', 'آلزایمر زودرس (MCI یا دمانس خفیف) با آمیلوئید تأییدشده — ۱۰ mg/kg وریدی هر ۲ هفته طی حدود ۱ ساعت', 'Early Alzheimer disease (MCI or mild dementia) with confirmed amyloid — 10 mg/kg IV every 2 weeks over about 1 hour', A18, 10, None, [R(Lq, '2.2, Table 1')],
           notes=[note('پس از ۱۸ ماه: ادامه یا نگهدارنده ۱۰ mg/kg هر ۴ هفته. زیرجلدی: شروع ۵۰۰ mg هفتگی، نگهدارنده ۳۶۰ mg هفتگی. پیش از شروع ژنوتیپ ApoE ε4 و MRI پایه؛ MRI در ماه ۱، ۲، ۳ و ۶.', 'After 18 months: continue, or maintenance 10 mg/kg every 4 weeks. Subcutaneous: start 500 mg weekly, maintenance 360 mg weekly. Before starting: ApoE ε4 testing and baseline MRI; MRI at months 1, 2, 3 and 6.', [R(Lq, '2.2'), R(Lq, '2.4'), R(Lq, 'Boxed Warning')])])],
     [CI('hyper', 'حساسیت جدی به لکانماب (آنژیوادم، آنافیلاکسی).', 'Serious hypersensitivity to lecanemab (angioedema, anaphylaxis).', [R(Lq, '4')])],
     warn=[W('هشدار جعبه‌ای: ناهنجاری تصویربرداری مرتبط با آمیلوئید (ARIA: ادم و هموسیدرین)، گاه کشنده؛ خونریزی مغزی بیش از ۱ cm؛ در هموزیگوت ApoE ε4 شایع‌تر؛ احتیاط با ضدانعقاد و ترومبولیتیک.', 'Boxed warning: amyloid-related imaging abnormalities (ARIA-E/ARIA-H), sometimes fatal; intracerebral haemorrhage >1 cm; more frequent in ApoE ε4 homozygotes; caution with anticoagulants and thrombolytics.', [R(Lq, 'Boxed Warning')]),
           W('واکنش انفوزیون و حساسیت.', 'Infusion-related and hypersensitivity reactions.', [R(Lq, '5')])],
     exs=[ex('iv', 'vial-100', {'perDose': 700, 'mlPerDose': 7}, ageYears=72, weightKg=70)])

Nu = fda('neupro', 'FDA Neupro', 'Neupro (rotigotine transdermal system) — Prescribing Information', sid('rotigotine'))
pt = lambda mg: form(f'patch-{mg}', 'patch', 'transdermal', f'{mg} mg/24 h patch', mg, 'mg', [R(Nu, '3')], per='application')
drug('rotigotine', 'nervous-system', 'روتیگوتین', 'Rotigotine', T('آگونیست دوپامین (پچ)', 'Dopamine agonist (patch)'), [{'name': 'Neupro', 'market': 'US'}], ['neupro', 'نوپرو', 'روتیگوتین'],
     [pt(2), pt(4), pt(6), pt(8), pt(1), pt(3)],
     [reg('early', 'parkinsons', T('پارکینسون مراحل اولیه — شروع پچ ۲ mg/۲۴ ساعت؛ هفتگی ۲ mg افزایش تا ۶ mg/۲۴ ساعت', 'Early-stage Parkinson disease — start 2 mg/24 h patch; increase by 2 mg weekly to 6 mg/24 h'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 6, 'dosesPerDay': 1}, [R(Nu, '2.1')],
          notes=[note('روزانه یک پچ روی پوست سالم (شکم، ران، باسن، پهلو، شانه، بازو)؛ محل هر روز عوض شود. قطع تدریجی: حداکثر ۲ mg هر روز در میان.', 'One patch daily on intact skin (abdomen, thigh, hip, flank, shoulder, upper arm); rotate the site daily. Taper: max 2 mg every other day.', [R(Nu, '2.3'), R(Nu, '2.4')])]),
      reg('adv', 'parkinsons', T('پارکینسون پیشرفته — شروع ۴ mg/۲۴ ساعت؛ هفتگی ۲ mg افزایش تا ۸ mg/۲۴ ساعت', 'Advanced-stage Parkinson disease — start 4 mg/24 h; increase by 2 mg weekly to 8 mg/24 h'), A18, 'fixed', {'perDose': 4, 'perDoseMax': 8, 'dosesPerDay': 1}, [R(Nu, '2.1')]),
      reg('rls', 'restless-legs', T('سندرم پای بی‌قرار — شروع ۱ mg/۲۴ ساعت؛ هفتگی ۱ mg افزایش تا ۳ mg/۲۴ ساعت', 'Restless legs syndrome — start 1 mg/24 h; increase by 1 mg weekly to 3 mg/24 h'), A18, 'fixed', {'perDose': 1, 'perDoseMax': 3, 'dosesPerDay': 1}, [R(Nu, '2.2')])],
     [CI('hyper', 'حساسیت به روتیگوتین یا اجزای پچ.', 'Hypersensitivity to rotigotine or the patch components.', [R(Nu, '4')])],
     warn=[DA_W(Nu), W('حساسیت به سولفیت؛ افزایش فشار و ضربان؛ تشدید (augmentation) در RLS؛ پیش از MRI یا کاردیوورژن پچ برداشته شود (سوختگی)؛ گرما روی پچ نه.', 'Sulfite sensitivity; increased blood pressure and heart rate; augmentation in RLS; remove before MRI or cardioversion (burns); no heat over the patch.', [R(Nu, '5')])],
     exs=[ex('early', 'patch-2', {'perDose': 2, 'tabletsPerDoseRounded': 1, 'upperPerDose': 6}, ageYears=60, weightKg=75), ex('adv', 'patch-4', {'perDose': 4, 'tabletsPerDoseRounded': 1, 'upperPerDose': 8}, ageYears=65, weightKg=75),
          ex('rls', 'patch-1', {'perDose': 1, 'tabletsPerDoseRounded': 1, 'upperPerDose': 3}, ageYears=50, weightKg=75)])

Ak = fda('apokyn', 'FDA Apokyn', 'Apokyn (apomorphine hydrochloride) injection 10 mg/mL — Prescribing Information', sid('apomorphine'))
drug('apomorphine', 'nervous-system', 'آپومورفین', 'Apomorphine', T('آگونیست دوپامین (تزریقی)', 'Dopamine agonist (injectable)'), [{'name': 'Apokyn', 'market': 'US'}], ['apokyn', 'آپوکین', 'آپومورفین'],
     [form('cart-10', 'injection', 'sc', '10 mg/mL cartridge (30 mg/3 mL) for pen', 10, 'mg', [R(Ak, '3')], vol=1)],
     [reg('off', 'parkinsons', T('دوره‌های «off» پارکینسون پیشرفته — هر دوز ۰٫۲ mL (۲ mg) زیرجلدی؛ تیتراسیون تا حداکثر ۰٫۶ mL (۶ mg)', 'Parkinson "off" episodes — each dose 0.2 mL (2 mg) SC; titrate to max 0.6 mL (6 mg)'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 6, 'dosesPerDay': 1}, [R(Ak, '2.3')], dur=ONE,
          notes=[note('همیشه دوز را به mL بنویسید. اولین دوز زیر نظر پزشک. شروع ۰٫۱ تا ۰٫۲ mL. برای یک دوره off دوز دوم نه؛ فاصله دست‌کم ۲ ساعت. ۳ روز پیش از شروع تری‌متوبنزامید ۳۰۰ mg سه بار. وقفه بیش از یک هفته: از ۰٫۲ mL دوباره. نارسایی خفیف/متوسط کلیه: شروع ۰٫۱ mL.', 'Always express the dose in mL. First dose under medical supervision. Start 0.1–0.2 mL. No second dose for the same off episode; at least 2 h apart. Trimethobenzamide 300 mg three times daily from 3 days before. Interruption >1 week: restart at 0.2 mL. Mild/moderate renal impairment: start 0.1 mL.', [R(Ak, '2.1'), R(Ak, '2.3'), R(Ak, '2.5'), R(Ak, '2.2'), R(Ak, '2.4')])])],
     [CI('ci', 'آنتاگونیست‌های 5HT3 (اندانسترون، گرانیسترون، دولاسترون، پالونوسترون، آلوسترون) — افت فشار شدید و کاهش هوشیاری؛ حساسیت به آپومورفین یا سولفیت.', '5HT3 antagonists (ondansetron, granisetron, dolasetron, palonosetron, alosetron) — profound hypotension and loss of consciousness; hypersensitivity to apomorphine or sulfite.', [R(Ak, '4')])],
     warn=[DA_W(Ak), W('تزریق وریدی نه (ترومبوز)؛ تهوع و استفراغ؛ کم‌خونی همولیتیک؛ رویداد کرونری؛ طولانی شدن QTc؛ پریاپیسم.', 'Never IV (thrombosis); nausea and vomiting; haemolytic anaemia; coronary events; QTc prolongation; priapism.', [R(Ak, '5')])],
     exs=[ex('off', 'cart-10', {'perDose': 2, 'mlPerDose': 0.2, 'upperPerDose': 6}, ageYears=65, weightKg=70)])

Sl = fda('selegiline', 'FDA Selegiline caps', 'Selegiline hydrochloride capsules 5 mg — Prescribing Information', sid('selegiline')); d = R(Sl, 'Dosage and Administration')
drug('selegiline', 'nervous-system', 'سلژیلین', 'Selegiline', T('مهارکننده MAO-B', 'MAO-B inhibitor'), [{'name': 'Eldepryl', 'market': 'US'}], ['eldepryl', 'jumex', 'جومکس', 'سلژیلین', 'سلگیلین'],
     [cap('cap-5', 5, Sl, 'How Supplied')],
     [reg('pd', 'parkinsons', T('پارکینسون با پاسخ رو به کاهش به لوودوپا — ۵ mg هنگام صبحانه و ۵ mg هنگام ناهار', 'Parkinson disease with waning levodopa response — 5 mg at breakfast and 5 mg at lunch'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 2}, [d],
          limits={'maxPerDay': 10, 'refs': [d, R(Sl, 'Warnings')]}, notes=[note('همراه لوودوپا/کاربیدوپا؛ پس از ۲ تا ۳ روز می‌توان لوودوپا را ۱۰ تا ۳۰٪ کم کرد. بیش از ۱۰ mg/روز انتخابی بودن MAO-B از بین می‌رود.', 'With levodopa/carbidopa; after 2–3 days levodopa may be cut by 10–30%. Above 10 mg/day MAO-B selectivity is lost.', [d, R(Sl, 'Warnings')])])],
     [CI('ci', 'حساسیت به سلژیلین؛ مپریدین (و معمولاً سایر اپیوئیدها).', 'Hypersensitivity to selegiline; meperidine (often extended to other opioids).', [R(Sl, 'Contraindications')])],
     warn=[W('بیش از ۱۰ mg/روز نه (مهار غیرانتخابی MAO)؛ واکنش فشار خون با غذای تیرامین‌دار نادر است.', 'Not above 10 mg/day (non-selective MAO inhibition); rare hypertensive reactions with tyramine-rich foods.', [R(Sl, 'Warnings')])],
     exs=[ex('pd', 'cap-5', {'perDose': 5, 'tabletsPerDoseRounded': 1, 'perDay': 10}, ageYears=65, weightKg=70)])

Bz = fda('benztropine', 'FDA Benztropine tabs', 'Benztropine mesylate tablets USP — Prescribing Information', sid('benztropine')); d = R(Bz, 'Dosage and Administration')
drug('benztropine', 'nervous-system', 'بنزتروپین', 'Benztropine', T('آنتی‌کولینرژیک ضدپارکینسون', 'Anticholinergic antiparkinsonian'), [{'name': 'Cogentin', 'market': 'US'}], ['cogentin', 'کوجنتین', 'بنزتروپین'],
     [tab('tab-1', 1, '1 mg tablet (scored)', [R(Bz, 'How Supplied')], scored=True), tab('tab-0-5', 0.5, '0.5 mg tablet (scored)', [R(Bz, 'How Supplied')], scored=True)],
     [reg('eps', 'drug-induced-parkinsonism', T('عوارض اکستراپیرامیدال ناشی از نورولپتیک — ۱ تا ۲ mg دو یا سه بار در روز', 'Neuroleptic-induced extrapyramidal disorders — 1–2 mg two or three times daily'), {'minAge': age(3, 'year')}, 'fixed', {'perDose': 1, 'perDoseMax': 2, 'dosesPerDay': 2}, [d],
          limits={'maxPerDay': 6, 'refs': [d]}, notes=[note('محدوده کلی ۱ تا ۴ mg یک یا دو بار. پس از ۱ تا ۲ هفته قطع برای سنجش نیاز. برای دیسکینزی دیررس نه.', 'Overall range 1–4 mg once or twice daily. Withdraw after 1–2 weeks to reassess. Not for tardive dyskinesia.', [d, R(Bz, 'Indications and Usage')])]),
      NC('pd', 'parkinsons', 'پارکینسونیسم ایدیوپاتیک یا پس از آنسفالیت (کمکی) — ۱ تا ۲ mg/روز (۰٫۵ تا ۶ mg)', 'Idiopathic or postencephalitic parkinsonism (adjunct) — 1–2 mg/day (0.5–6 mg)', {'minAge': age(3, 'year')},
         'ایدیوپاتیک: شروع ۰٫۵ تا ۱ mg هنگام خواب؛ هر ۵ تا ۶ روز ۰٫۵ mg افزایش تا حداکثر ۶ mg. سالمند و افراد لاغر دوز بالا را تحمل نمی‌کنند.', 'Idiopathic: start 0.5–1 mg at bedtime; increase by 0.5 mg every 5–6 days to max 6 mg. Elderly and thin patients tolerate large doses poorly.', [d])],
     [CI('ci', 'حساسیت؛ کودک زیر ۳ سال (اثرات شبه‌آتروپین).', 'Hypersensitivity; children under 3 years (atropine-like effects).', [R(Bz, 'Contraindications')])],
     warn=[W('ایلئوس فلجی، هیپرترمی و گرمازدگی (گاه کشنده) به‌ویژه با فنوتیازین یا هالوپریدول؛ اختلال رانندگی.', 'Paralytic ileus, hyperthermia and heat stroke (sometimes fatal), especially with phenothiazines or haloperidol; impairs driving.', [R(Bz, 'Warnings')])],
     exs=[ex('eps', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1, 'upperPerDose': 2}, ageYears=35, weightKg=70)])

Bt = fda('botox', 'FDA Botox', 'Botox (onabotulinumtoxinA) for injection — Prescribing Information', sid('botox'))
BTX = lambda: note('واحدهای بوتاکس با سایر فرآورده‌های بوتولینوم قابل تبدیل نیستند. در هر ۳ ماه: بزرگسال حداکثر ۴۰۰ واحد؛ کودک کمتر از ۱۰ واحد/kg یا ۳۴۰ واحد.', 'Botox units are not interchangeable with other botulinum products. In any 3 months: adults max 400 Units; children the lesser of 10 Units/kg or 340 Units.', [R(Bt, '2.1'), R(Bt, '2')])
drug('onabotulinumtoxina', 'musculoskeletal', 'بوتاکس (اونابوتولینوم‌توکسین A)', 'OnabotulinumtoxinA (Botox)', T('نوروتوکسین بوتولینوم', 'Botulinum neurotoxin'), [{'name': 'Botox', 'market': 'US'}], ['botox', 'بوتاکس', 'botulinum', 'بوتولینوم', 'سم بوتولینوم'],
     [form('vial-100', 'powder-for-injection', 'im', '100 Units vial', 100, 'unit', [R(Bt, '3')], per='vial'), form('vial-200', 'powder-for-injection', 'im', '200 Units vial', 200, 'unit', [R(Bt, '3')], per='vial')],
     [reg('cm', 'migraine-prophylaxis', T('پیشگیری میگرن مزمن — ۱۵۵ واحد عضلانی (۵ واحد در هر نقطه، ۷ ناحیه سر و گردن)', 'Chronic migraine prophylaxis — 155 Units IM (5 Units per site across 7 head/neck areas)'), A18, 'fixed', {'perDose': 155, 'dosesPerDay': 1}, [R(Bt, '2.5')], unit='unit', dur=ONE, notes=[BTX()]),
      reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال — ۱۰۰ واحد داخل دترسور (۲۰ نقطه × ۵ واحد)', 'Overactive bladder — 100 Units intradetrusor (20 sites × 5 Units)'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Bt, '2.3')], unit='unit', dur=ONE,
          notes=[note('عفونت ادراری نباشد؛ آنتی‌بیوتیک پیشگیری (غیر آمینوگلیکوزید) ۱ تا ۳ روز قبل تا بعد؛ ضدپلاکت ۳ روز قبل قطع.', 'No UTI; prophylactic antibiotics (not aminoglycosides) 1–3 days before to after; stop antiplatelets 3 days before.', [R(Bt, '2.3')])]),
      reg('ndo', 'neurogenic-bladder', T('بیش‌فعالی دترسور نوروژنیک بزرگسال — ۲۰۰ واحد داخل دترسور (۳۰ نقطه)', 'Adult neurogenic detrusor overactivity — 200 Units intradetrusor (30 sites)'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Bt, '2.3')], unit='unit', dur=ONE),
      reg('hh', 'hyperhidrosis', T('تعریق شدید زیربغل — ۵۰ واحد داخل‌جلدی در هر زیربغل', 'Severe axillary hyperhidrosis — 50 Units intradermally per axilla'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Bt, '2.9')], unit='unit', dur=ONE),
      once('sp-ul', 'spasticity', 'اسپاستیسیته اندام فوقانی کودک — ۳ تا ۶ واحد/kg کل (حداکثر ۲۰۰) بین عضلات', 'Paediatric upper-limb spasticity — 3–6 Units/kg total (max 200) divided among muscles', {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 3, 6, [R(Bt, '2.7')], unit='unit', limits={'maxPerDose': 200, 'refs': [R(Bt, '2.7')]}),
      once('sp-ll', 'spasticity', 'اسپاستیسیته اندام تحتانی کودک — ۴ تا ۸ واحد/kg کل (حداکثر ۳۰۰)', 'Paediatric lower-limb spasticity — 4–8 Units/kg total (max 300)', {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 4, 8, [R(Bt, '2.7')], unit='unit', limits={'maxPerDose': 300, 'refs': [R(Bt, '2.7')]}),
      NC('sp-adult', 'spasticity', 'اسپاستیسیته بزرگسال — اندام فوقانی تا ۴۰۰ واحد؛ تحتانی ۳۰۰ تا ۴۰۰ واحد بین عضلات', 'Adult spasticity — upper limb up to 400 Units; lower limb 300–400 Units divided among muscles', A18,
         'دوز هر عضله طبق جداول برچسب و راهنمای EMG/سونوگرافی تعیین می‌شود.', 'Per-muscle doses follow the label tables with EMG/ultrasound guidance.', [R(Bt, '2.6')])],
     [CI('ci', 'حساسیت به هر فرآورده بوتولینوم؛ عفونت در محل تزریق؛ تزریق دترسور در عفونت ادراری یا احتباس ادرار (PVR >۲۰۰ mL) بدون سونداژ متناوب.', 'Hypersensitivity to any botulinum toxin product; infection at the injection site; intradetrusor injection with UTI or urinary retention (PVR >200 mL) without clean intermittent catheterisation.', [R(Bt, '4')])],
     warn=[W('هشدار جعبه‌ای: انتشار دوردست اثر سم (ضعف عمومی، دوبینی، افتادگی پلک، اختلال بلع و تنفس — گاه کشنده)، ساعت‌ها تا هفته‌ها بعد؛ بیشترین خطر در کودکان با اسپاستیسیته.', 'Boxed warning: distant spread of toxin effect (generalised weakness, diplopia, ptosis, swallowing and breathing difficulty — can be fatal), hours to weeks later; highest risk in children treated for spasticity.', [R(Bt, 'Boxed Warning')]),
           W('اختلال بلع و تنفس؛ عفونت ادراری و احتباس ادرار پس از تزریق مثانه؛ زخم قرنیه در بلفارواسپاسم؛ دیسرفلکسی اتونوم.', 'Dysphagia and breathing difficulties; UTI and urinary retention after bladder injection; corneal ulceration in blepharospasm; autonomic dysreflexia.', [R(Bt, '5')])],
     exs=[ex('cm', 'vial-200', {'perDose': 155}, ageYears=40, weightKg=65), ex('oab', 'vial-100', {'perDose': 100}, ageYears=60, weightKg=70), ex('ndo', 'vial-200', {'perDose': 200}, ageYears=45, weightKg=70), ex('hh', 'vial-100', {'perDose': 50}, ageYears=30, weightKg=70),
          ex('sp-ul', 'vial-100', {'perDose': 60, 'upperPerDose': 120}, ageYears=6, weightKg=20), ex('sp-ll', 'vial-100', {'perDose': 80, 'upperPerDose': 160}, ageYears=6, weightKg=20)])

Zm = fda('zolmitriptan', 'FDA Zolmitriptan', 'Zolmitriptan tablets 2.5/5 mg — Prescribing Information', sid('zolmitriptan'))
drug('zolmitriptan', 'nervous-system', 'زولمیتریپتان', 'Zolmitriptan', T('تریپتان (آگونیست 5-HT1B/1D)', 'Triptan (5-HT1B/1D agonist)'), [{'name': 'Zomig', 'market': 'US'}], ['zomig', 'زومیگ', 'زولمیتریپتان'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet (functionally scored)', [R(Zm, '3')], scored=True), tab('tab-5', 5, '5 mg tablet', [R(Zm, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن بزرگسال — ۱٫۲۵ یا ۲٫۵ mg؛ حداکثر تک‌دوز ۵ mg', 'Acute migraine, adults — 1.25 or 2.5 mg; max single dose 5 mg'), A18, 'fixed', {'perDose': 2.5, 'perDoseMax': 5, 'dosesPerDay': 1}, [R(Zm, '2.1')],
          limits={'maxPerDay': 10, 'refs': [R(Zm, '2.1')]}, notes=[note('در صورت عدم بهبود یا بازگشت پس از ۲ ساعت تکرار؛ حداکثر ۱۰ mg در ۲۴ ساعت. نارسایی متوسط/شدید کبد: ۱٫۲۵ mg (شدید حداکثر ۵ mg/روز). با سایمتیدین حداکثر ۲٫۵ mg تک‌دوز و ۵ mg/روز.', 'Repeat after 2 h if not resolved or recurs; max 10 mg in 24 h. Moderate/severe hepatic impairment: 1.25 mg (severe max 5 mg/day). With cimetidine max 2.5 mg single and 5 mg/day.', [R(Zm, '2.1'), R(Zm, '2.3'), R(Zm, '2.4')])])],
     [TRIP_CI(Zm), CI('maoi', 'مهارکننده MAO-A همزمان یا ظرف ۲ هفته.', 'MAO-A inhibitor concomitantly or within 2 weeks.', [R(Zm, '4')])], warn=[TRIP_W(Zm)],
     exs=[ex('acute', 'tab-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 5}, ageYears=35, weightKg=65)])

Rp = fda('relpax', 'FDA Relpax', 'Relpax (eletriptan) tablets — Prescribing Information', sid('eletriptan'))
drug('eletriptan', 'nervous-system', 'الیتریپتان', 'Eletriptan', T('تریپتان (آگونیست 5-HT1B/1D)', 'Triptan (5-HT1B/1D agonist)'), [{'name': 'Relpax', 'market': 'US'}], ['relpax', 'رلپکس', 'الیتریپتان', 'eletriptan'],
     [tab('tab-20', 20, '20 mg tablet', [R(Rp, '3')]), tab('tab-40', 40, '40 mg tablet', [R(Rp, '3')])],
     [reg('acute', 'migraine-acute', T('حمله حاد میگرن بزرگسال — ۲۰ یا ۴۰ mg؛ حداکثر تک‌دوز ۴۰ mg', 'Acute migraine, adults — 20 or 40 mg; max single dose 40 mg'), A18, 'fixed', {'perDose': 20, 'perDoseMax': 40, 'dosesPerDay': 1}, [R(Rp, '2')],
          limits={'maxPerDay': 80, 'refs': [R(Rp, '2')]}, notes=[note('اگر پس از ۲ ساعت بهبود نیافت یا بازگشت، دوز دوم دست‌کم ۲ ساعت بعد؛ حداکثر ۸۰ mg/روز.', 'If not resolved after 2 h or it returns, a second dose at least 2 h later; max 80 mg/day.', [R(Rp, '2')])])],
     [TRIP_CI(Rp), CI('cyp3a4', 'مهارکننده‌های قوی CYP3A4 ظرف ۷۲ ساعت: کتوکونازول، ایتراکونازول، نفازودون، کلاریترومایسین، ریتوناویر، نلفیناویر.', 'Potent CYP3A4 inhibitors within 72 h: ketoconazole, itraconazole, nefazodone, clarithromycin, ritonavir, nelfinavir.', [R(Rp, '4')])],
     warn=[TRIP_W(Rp)], exs=[ex('acute', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1, 'upperPerDose': 40}, ageYears=35, weightKg=65)])
print('s12d2 ok')
