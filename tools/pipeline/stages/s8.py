"""Stage 8 — psychiatry, addiction, neurology and eye; links for diseases that had no drug."""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's8_setids.json')))
sid = lambda k: S[k][0]

add_disease('opioid-use-disorder', 'اختلال مصرف اپیوئید (اعتیاد به مواد افیونی)', 'Opioid use disorder', ['opioid dependence', 'اعتیاد', 'ترک تریاک', 'متادون درمانی', 'OUD'], ['F11.20'], 'psychiatry')
add_disease('alcohol-use-disorder', 'وابستگی به الکل', 'Alcohol dependence', ['alcoholism', 'الکلیسم', 'ترک الکل'], ['F10.20'], 'psychiatry')
add_disease('lennox-gastaut', 'سندرم لنوکس-گاستو', 'Lennox-Gastaut syndrome', ['LGS', 'لنوکس گاستو'], ['G40.812'], 'neurology')
add_disease('absence-epilepsy', 'صرع ابسانس (پتی‌مال)', 'Absence epilepsy (petit mal)', ['absence seizure', 'petit mal', 'پتی مال', 'غیبت'], ['G40.A09'], 'neurology')
add_disease('myasthenia-gravis', 'میاستنی گراویس', 'Myasthenia gravis', ['myasthenia', 'میاستنی'], ['G70.00'], 'neurology')
add_disease('altitude-sickness', 'بیماری کوهستان (ارتفاع)', 'Acute mountain sickness', ['altitude sickness', 'AMS', 'ارتفاع زدگی', 'کوه گرفتگی'], ['T70.29XA'], 'emergency')
ONE = {'min': 1, 'max': 1}
drops = lambda id, label, src, sec='3', form_='eye-drops': unitform(id, form_, 'ophthalmic', label, [R(src, sec)], unit='drop', per='drop')

# --- diseases that had no linked drug: regimens from labels already in the database ---
SRC = {s['id']: s for s in json.load(open(os.path.join(ROOT, 'sources.json')))}
Mt, Cz, Hq, Cf, Bz = 'fda-metronidazole-tab', 'fda-carbamazepine', 'fda-hcq', 'fda-cefazolin', 'fda-benzocaine'
mt_oral = [f['id'] for f in json.load(open(find('metronidazole')))['formulations'] if f['route'] == 'oral']
patch('metronidazole', add_regs=[
    reg('liver-abscess-adult', 'amebic-liver-abscess', T('آبسه کبدی آمیبی — بزرگسال: ۵۰۰ یا ۷۵۰ mg سه بار در روز، ۵ تا ۱۰ روز', 'Amoebic liver abscess — adult: 500 or 750 mg three times daily, 5–10 days'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 750, 'dosesPerDay': 3}, [R(Mt, 'Dosage and Administration — Amebiasis')], allowed=mt_oral, dur={'min': 5, 'max': 10},
        notes=[note('درمان دارویی جای آسپیراسیون یا درناژ چرک را نمی‌گیرد.', 'Drug therapy does not replace aspiration or drainage of pus.', [R(Mt, 'Indications and Usage — Amebiasis')])]),
    reg('liver-abscess-child', 'amebic-liver-abscess', T('آبسه کبدی آمیبی — کودک: ۳۵ تا ۵۰ mg/kg/روز در ۳ دوز، ۱۰ روز', 'Amoebic liver abscess — child: 35–50 mg/kg/day in 3 doses, 10 days'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 35, 'perKgPerDayMax': 50, 'dividedDoses': 3}, [R(Mt, 'Dosage and Administration — Amebiasis')], allowed=mt_oral, dur={'min': 10, 'max': 10})],
    add_exs=[ex('liver-abscess-adult', 'tab-250', {'perDose': 500, 'upperPerDose': 750}, ageYears=40, weightKg=70), ex('liver-abscess-child', 'tab-250', {'perDose': 501.67, 'upperPerDose': 716.67}, ageYears=13, weightKg=43)])
patch('carbamazepine', add_regs=[
    reg('tn', 'trigeminal-neuralgia', T('نورالژی سه‌قلو — روز اول ۱۰۰ mg دو بار، افزایش تا رفع درد (حداکثر ۱۲۰۰ mg در روز)', 'Trigeminal neuralgia — day 1: 100 mg twice daily, increase until pain-free (max 1,200 mg/day)'), A18, 'titration',
        {'dividedDoses': 2, 'titration': {'start': 200, 'increment': 200, 'incrementEveryDays': 1, 'targetMin': 400, 'targetMax': 800, 'max': 1200}}, [R(Cz, 'Dosage and Administration — Trigeminal Neuralgia')],
        notes=[note('افزایش روزانه حداکثر ۲۰۰ mg (۱۰۰ mg هر ۱۲ ساعت) و فقط در حد نیاز برای رفع درد. نگهدارنده بیشتر بیماران ۴۰۰ تا ۸۰۰ mg در روز. هر ۳ ماه تلاش برای کمترین دوز یا قطع. مسکن ساده نیست.', 'Increase by up to 200 mg/day (100 mg every 12 h) only as needed for pain freedom. Most maintain on 400–800 mg/day. Try to reduce to the minimum or stop every 3 months. Not a simple analgesic.', [R(Cz, 'Dosage and Administration — Trigeminal Neuralgia'), R(Cz, 'Indications and Usage')])])],
    add_exs=[ex('tn', 'susp-100-5', {'perDose': 100, 'mlPerDose': 5}, ageYears=60, weightKg=70)])
patch('hydroxychloroquine', add_regs=[
    reg('sle', 'lupus', T('لوپوس اریتماتوی سیستمیک یا دیسکوئید — بزرگسال: ۲۰۰ تا ۴۰۰ mg در روز', 'Systemic or chronic discoid lupus — adult: 200–400 mg/day'), A18, 'fixed', {'perDose': 200, 'perDoseMax': 400, 'dosesPerDay': 1}, [R(Hq, '2.4'), R(Hq, '2.5')],
        notes=[note('۲۰۰ mg یک بار، یا ۴۰۰ mg یک بار یا در ۲ دوز.', '200 mg once daily, or 400 mg once daily or in two divided doses.', [R(Hq, '2.4')])])],
    add_exs=[ex('sle', 'tab-200', {'perDose': 200, 'upperPerDose': 400}, ageYears=35, weightKg=60)] if any(f['id'] == 'tab-200' for f in json.load(open(find('hydroxychloroquine')))['formulations']) else [])
patch('cefazolin', add_regs=[
    reg('bone', 'bone-infection', T('عفونت استخوان و مفصل (استافیلوکوک طلایی) — بزرگسال: عفونت متوسط تا شدید ۵۰۰ mg تا ۱ g هر ۶ تا ۸ ساعت', 'Bone and joint infection (S. aureus) — adult: moderate–severe 500 mg–1 g every 6–8 h'), A18, 'notCalculated',
        {'reason': T('برچسب: عفونت متوسط تا شدید ۵۰۰ mg تا ۱ g وریدی هر ۶ تا ۸ ساعت؛ عفونت شدید تهدیدکننده ۱ تا ۱٫۵ g هر ۶ ساعت. مدت درمان و نیاز به جراحی با متخصص.', 'Label: moderate–severe infections 500 mg–1 g IV every 6–8 h; severe life-threatening 1–1.5 g every 6 h. Duration and need for surgery per specialist.')},
        [R(Cf, 'Dosage and Administration — Usual Adult Dosage'), R(Cf, 'Indications and Usage — Bone and Joint Infections')])])
bz = json.load(open(find('benzocaine-oral')))
use = next(r for r in bz['regimens'] if r['id'] == 'use')
canker = dict(json.loads(json.dumps(use)), id='canker', disease='mouth-pain', label=T('زخم آفتی (آفت دهان) — تا ۴ بار در روز (۲ سال به بالا)', 'Canker sores — up to 4 times daily (≥2 y)'))
canker['refs'] = [R(Bz, 'Directions'), R(Bz, 'Uses')]
patch('benzocaine-oral', add_regs=[canker], add_exs=[dict(e, regimen='canker') for e in bz['examples'] if e['regimen'] == 'use'][:1])
dz = json.load(open(os.path.join(ROOT, 'diseases.json')))
json.dump([x for x in dz if x['id'] != 'cardiac-arrest'], open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')

# --- addiction ---
OPI_W = lambda src: W('هشدار جعبه‌ای/مهم: دپرسیون تنفسی کشنده (به‌ویژه با بنزودیازپین و الکل)، مصرف تصادفی در کودک کشنده است؛ نالوکسان در دسترس باشد.', 'Boxed/major warning: life-threatening respiratory depression (especially with benzodiazepines and alcohol); accidental ingestion by a child can be fatal; keep naloxone available.', [R(src, 'Boxed Warning'), R(src, '5')])
Bn = fda('bup-nal', 'FDA Buprenorphine-nalox.', 'Buprenorphine and naloxone sublingual tablets (Hikma) — Prescribing Information', sid('suboxone'))
drug('buprenorphine-naloxone', 'nervous-system', 'بوپرنورفین + نالوکسان (زیرزبانی)', 'Buprenorphine + naloxone (sublingual)', T('آگونیست نسبی اپیوئید برای درمان اعتیاد', 'Partial opioid agonist for OUD'), [{'name': 'Suboxone', 'market': 'US'}], ['suboxone', 'سابوکسون', 'بوپرنورفین', 'بوپره نورفین', 'ب ن'],
     [form(f'sl-{b}', 'sublingual-tablet', 'sublingual', f'Buprenorphine {b} mg / naloxone {n} mg sublingual tablet', b, 'mg', [R(Bn, '3')], per='tablet',
           components={'buprenorphine': {'name': T('بوپرنورفین', 'Buprenorphine'), 'amount': b, 'unit': 'mg'}, 'naloxone': {'name': T('نالوکسان', 'Naloxone'), 'amount': n, 'unit': 'mg'}}) for b, n in ((2, 0.5), (8, 2))],
     [reg('maint', 'opioid-use-disorder', T('نگهدارنده اختلال مصرف اپیوئید — هدف ۱۶ mg بوپرنورفین یک بار در روز (بازه ۴ تا ۲۴ mg)', 'OUD maintenance — target 16 mg buprenorphine once daily (range 4–24 mg)'), A18, 'fixed', {'perDose': 16, 'dosesPerDay': 1}, [R(Bn, '2.3')], doseComponent='buprenorphine',
          notes=[note('دوز به‌صورت جزء بوپرنورفین. پس از القا با بوپرنورفین زیرزبانی؛ تنظیم با گام‌های ۲ یا ۴ mg؛ بازه معمول ۴ تا ۲۴ mg در روز. زیر زبان تا حل کامل؛ نجود و نبلعد. آغاز با مصرف تحت نظر.', 'Shown as the buprenorphine component. After induction with sublingual buprenorphine; adjust in 2 or 4 mg steps; usual range 4–24 mg/day. Under the tongue until dissolved; do not chew or swallow. Start with supervised dosing.', [R(Bn, '2.3'), R(Bn, '2.1'), R(Bn, '2.4'), R(Bn, '2.5')])])],
     [CI('hyper', 'حساسیت به بوپرنورفین یا نالوکسان.', 'Hypersensitivity to buprenorphine or naloxone.', [R(Bn, '4')])],
     warn=[W('دپرسیون تنفسی (به‌ویژه همراه بنزودیازپین یا سایر مضعف‌های CNS)؛ مصرف تصادفی در کودک؛ نالوکسان در دسترس باشد.', 'Respiratory depression (especially with benzodiazepines or other CNS depressants); accidental pediatric exposure; keep naloxone available.', [R(Bn, '2.2'), R(Bn, '5')])],
     exs=[ex('maint', 'sl-8', {'perDose': 16, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70)])

Md = fda('methadone', 'FDA Methadone 40 mg', 'Methadone hydrochloride tablets for oral suspension 40 mg (VistaPharm) — Prescribing Information', sid('methadone'))
drug('methadone', 'nervous-system', 'متادون', 'Methadone', T('آگونیست اپیوئید (درمان نگهدارنده اعتیاد)', 'Opioid agonist (OUD maintenance)'), [{'name': 'Diskets', 'market': 'US'}], ['diskets', 'dolophine', 'متادون', 'شربت متادون'],
     [form('disp-40', 'tablet', 'oral', '40 mg dispersible tablet (quadrisected; disperse in ~120 mL liquid)', 40, 'mg', [R(Md, '3')], per='tablet')],
     [reg('induction', 'opioid-use-disorder', T('القای درمان اعتیاد — ۲۰ تا ۳۰ mg دوز اول (حداکثر ۳۰ mg)', 'OUD induction — first dose 20–30 mg (max 30 mg)'), A18, 'notCalculated',
          {'reason': T('فقط در مراکز مجاز درمان اعتیاد. دوز اول ۲۰ تا ۳۰ mg تحت نظر، وقتی بیمار علائم ترک دارد و خواب‌آلود نیست؛ دوز اول بیش از ۳۰ mg نشود. اگر پس از ۲ تا ۴ ساعت علائم ترک ماند، ۵ تا ۱۰ mg دیگر. تنظیم‌های بعدی طبق برچسب. قرص در آب یا آب‌میوه حل شود؛ هرگز تزریق نشود.',
                       'Only in certified opioid treatment programmes. First dose 20–30 mg supervised, when the patient shows withdrawal and is not sedated; the first dose must not exceed 30 mg. If withdrawal persists after 2–4 h, give 5–10 mg more. Further titration per label. Disperse in water or juice; never inject.')}, [R(Md, '2.5'), R(Md, '2.1'), R(Md, '2.4')])],
     [CI('ci', 'دپرسیون تنفسی قابل‌توجه؛ آسم حاد یا شدید بدون پایش؛ انسداد گوارشی یا ایلئوس؛ حساسیت.', 'Significant respiratory depression; acute or severe asthma without monitoring; GI obstruction or ileus; hypersensitivity.', [R(Md, '4')])],
     warn=[W('هشدار جعبه‌ای: دپرسیون تنفسی کشنده (اوج اثر دیرتر و طولانی‌تر از اثر ضددرد)، طولانی شدن QT، مصرف تصادفی در کودک و تداخل با بنزودیازپین‌ها.', 'Boxed warning: life-threatening respiratory depression (peak later and longer than the analgesic effect), QT prolongation, accidental pediatric ingestion and benzodiazepine interactions.', [R(Md, 'Boxed Warning'), R(Md, '2.2')])])

Nx = fda('naltrexone', 'FDA Naltrexone', 'Naltrexone hydrochloride tablets 50 mg (SpecGx) — Prescribing Information', sid('naltrexone')); d = R(Nx, 'Dosage and Administration')
drug('naltrexone', 'nervous-system', 'نالترکسون', 'Naltrexone', T('آنتاگونیست اپیوئید', 'Opioid antagonist'), [{'name': 'Revia', 'market': 'US'}], ['revia', 'رویا', 'نالترکسون'],
     [tab('tab-50', 50, '50 mg tablet (scored)', [R(Nx, 'How Supplied')], scored=True)],
     [reg('alcohol', 'alcohol-use-disorder', T('وابستگی به الکل — ۵۰ mg یک بار در روز', 'Alcohol dependence — 50 mg once daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Nx, 'Dosage and Administration — Alcoholism')],
          notes=[note('در کارآزمایی‌ها تا ۱۲ هفته؛ فقط بخشی از برنامه درمان جامع.', 'Studied for up to 12 weeks; only part of a comprehensive programme.', [R(Nx, 'Dosage and Administration — Alcoholism')])]),
      reg('opioid', 'opioid-use-disorder', T('پیشگیری از عود اپیوئید (پس از سم‌زدایی) — شروع ۲۵ mg، سپس ۵۰ mg روزانه', 'Opioid relapse prevention (after detox) — start 25 mg, then 50 mg daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Nx, 'Dosage and Administration — Treatment of Opioid Dependence')],
          notes=[note('دوز اول ۲۵ mg؛ اگر علائم ترک نبود، ۵۰ mg روزانه. بیمار باید ۷ تا ۱۰ روز بدون اپیوئید باشد (تست ادرار منفی یا تست نالوکسان).', 'First dose 25 mg; if no withdrawal, 50 mg daily. Patient must be opioid-free for 7–10 days (negative urine screen or naloxone challenge).', [R(Nx, 'Dosage and Administration — Treatment of Opioid Dependence'), R(Nx, 'Contraindications')])])],
     [CI('ci', 'مصرف مسکن اپیوئیدی؛ وابستگی فعلی به اپیوئید (از جمله متادون یا بوپرنورفین)؛ ترک حاد اپیوئید؛ تست نالوکسان ناموفق یا ادرار مثبت؛ حساسیت.', 'Receiving opioid analgesics; current opioid dependence (including methadone or buprenorphine); acute opioid withdrawal; failed naloxone challenge or positive urine screen; hypersensitivity.', [R(Nx, 'Contraindications')])],
     exs=[ex('alcohol', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=80), ex('opioid', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Ac = fda('acamprosate', 'FDA Acamprosate DR', 'Acamprosate calcium delayed-release tablets 333 mg (Somerset) — Prescribing Information', sid('acamprosate'))
drug('acamprosate', 'nervous-system', 'آکامپروسات', 'Acamprosate', T('داروی حفظ پرهیز از الکل', 'Alcohol abstinence maintenance'), [{'name': 'Campral', 'market': 'US'}], ['campral', 'کمپرال', 'آکامپروسات'],
     [tab('tab-333', 333, '333 mg delayed-release tablet', [R(Ac, '3')])],
     [reg('std', 'alcohol-use-disorder', T('حفظ پرهیز از الکل — ۶۶۶ mg (۲ قرص) سه بار در روز', 'Maintaining alcohol abstinence — 666 mg (2 tablets) three times daily'), A18, 'fixed', {'perDose': 666, 'dosesPerDay': 3}, [R(Ac, '2')],
          notes=[note('هرچه زودتر پس از دوره ترک و پس از رسیدن به پرهیز شروع؛ در صورت عود ادامه. ترجیحاً با وعده‌ها.', 'Start as soon as possible after withdrawal once abstinent; continue through relapse. Preferably with meals.', [R(Ac, '2')])])],
     [CI('ci', 'حساسیت؛ نارسایی شدید کلیه.', 'Hypersensitivity; severe renal impairment.', [R(Ac, '4')])],
     exs=[ex('std', 'tab-333', {'perDose': 666, 'tabletsPerDoseRounded': 2}, ageYears=45, weightKg=75)])

Ds = fda('disulfiram', 'FDA Disulfiram', 'Disulfiram tablets 250 mg (Alvogen) — Prescribing Information', sid('disulfiram')); d = R(Ds, 'Dosage and Administration')
drug('disulfiram', 'nervous-system', 'دی‌سولفیرام', 'Disulfiram', T('بازدارنده مصرف الکل', 'Alcohol deterrent'), [{'name': 'Antabuse', 'market': 'US'}], ['antabuse', 'آنتابوس', 'دی سولفیرام'],
     [tab('tab-250', 250, '250 mg tablet', [R(Ds, 'How Supplied')])],
     [reg('initial', 'alcohol-use-disorder', T('وابستگی به الکل — مرحله اول: حداکثر ۵۰۰ mg یک بار در روز، ۱ تا ۲ هفته', 'Alcohol dependence — first phase: max 500 mg once daily for 1–2 weeks'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 1}, [d], dur={'min': 7, 'max': 14},
          notes=[note('فقط پس از دست‌کم ۱۲ ساعت پرهیز از الکل و با آگاهی کامل بیمار.', 'Only after at least 12 h of abstinence and with the patient’s full knowledge.', [d, R(Ds, 'Boxed Warning')])]),
      reg('maint', 'alcohol-use-disorder', T('نگهدارنده — معمولاً ۲۵۰ mg روزانه (۱۲۵ تا ۵۰۰ mg)', 'Maintenance — usually 250 mg daily (125–500 mg)'), A18, 'fixed', {'perDose': 250, 'dosesPerDay': 1}, [d], limits={'maxPerDay': 500, 'refs': [d]})],
     [CI('ci', 'مصرف اخیر مترونیدازول، پارالدئید، الکل یا فرآورده‌های الکل‌دار؛ بیماری شدید میوکارد یا انسداد کرونر؛ سایکوز؛ حساسیت به تیورام‌ها.', 'Recent metronidazole, paraldehyde, alcohol or alcohol-containing preparations; severe myocardial disease or coronary occlusion; psychosis; thiuram hypersensitivity.', [R(Ds, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: هرگز در حالت مستی یا بدون آگاهی بیمار داده نشود. هپاتیت و نارسایی کبد (گاهی کشنده)؛ نوریت اپتیک و نوروپاتی.', 'Boxed warning: never give to an intoxicated patient or without their knowledge. Hepatitis and hepatic failure (sometimes fatal); optic neuritis and neuropathy.', [R(Ds, 'Boxed Warning'), R(Ds, 'Warnings')])],
     inter=[IA('metronidazole', 'مترونیدازول و فرآورده‌های الکل‌دار (شربت سرفه، تونیک) — ممنوع.', 'Metronidazole and alcohol-containing preparations (cough syrups, tonics) — contraindicated.', [R(Ds, 'Contraindications')])],
     exs=[ex('initial', 'tab-250', {'perDose': 500, 'tabletsPerDoseRounded': 2}, ageYears=45, weightKg=75), ex('maint', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=75)])

# --- psychiatry ---
Vy = fda('vyvanse', 'FDA Vyvanse', 'Vyvanse (lisdexamfetamine) — Prescribing Information', sid('vyvanse'))
drug('lisdexamfetamine', 'nervous-system', 'لیزدگزامفتامین', 'Lisdexamfetamine', T('محرک CNS (آمفتامین)', 'CNS stimulant (amphetamine)'), [{'name': 'Vyvanse', 'market': 'US'}], ['vyvanse', 'elvanse', 'ویوانس', 'لیزدگزامفتامین'],
     [tab(f'cap-{m}', m, f'{m} mg capsule', [R(Vy, '3')], per='capsule', form_='capsule') for m in (10, 20, 30, 40, 50, 60, 70)],
     [reg('adhd', 'adhd', T('ADHD — ۶ سال به بالا: شروع ۳۰ mg صبح‌ها (تا ۷۰ mg)', 'ADHD — ≥6 y: start 30 mg every morning (up to 70 mg)'), {'minAge': age(6, 'year')}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 30, 'increment': 10, 'incrementEveryDays': 7, 'max': 70}}, [R(Vy, '2.3')],
          notes=[note('افزایش ۱۰ یا ۲۰ mg تقریباً هفتگی. صبح؛ دوز بعدازظهر نه (بی‌خوابی). نارسایی شدید کلیه: حداکثر ۵۰ mg؛ ESRD: ۳۰ mg.', 'Increase by 10 or 20 mg about weekly. Morning; avoid afternoon doses (insomnia). Severe renal impairment: max 50 mg; ESRD: 30 mg.', [R(Vy, '2.3'), R(Vy, '2.2'), R(Vy, '2.5')])])],
     [CI('ci', 'حساسیت به آمفتامین‌ها؛ MAOI همزمان یا ظرف ۱۴ روز (از جمله لینزولید یا متیلن بلو وریدی).', 'Hypersensitivity to amphetamines; MAOIs now or within 14 days (including linezolid or IV methylene blue).', [R(Vy, '4')])],
     warn=[W('هشدار جعبه‌ای: سوءمصرف، مصرف نادرست و اعتیاد؛ پیش از تجویز خطر بررسی و در طول درمان پایش شود.', 'Boxed warning: abuse, misuse and addiction; assess risk before prescribing and monitor during treatment.', [R(Vy, 'Boxed Warning')])],
     exs=[ex('adhd', 'cap-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=10, weightKg=30)])

Gf = fda('guanfacine-er', 'FDA Guanfacine ER', 'Guanfacine extended-release tablets (Upsher-Smith) — Prescribing Information', sid('intuniv'))
drug('guanfacine-er', 'nervous-system', 'گوانفاسین آهسته‌رهش', 'Guanfacine extended-release', T('آگونیست α2A (غیرمحرک ADHD)', 'α2A agonist (non-stimulant ADHD)'), [{'name': 'Intuniv', 'market': 'US'}], ['intuniv', 'اینتونیو', 'گوانفاسین'],
     [tab(f'tab-{m}', m, f'{m} mg extended-release tablet', [R(Gf, '3')]) for m in (1, 2, 3, 4)],
     [reg('adhd', 'adhd', T('ADHD کودک و نوجوان ۶ تا ۱۷ سال — شروع ۱ mg روزانه، هدف ۰٫۰۵ تا ۰٫۱۲ mg/kg', 'ADHD age 6–17 — start 1 mg daily, target 0.05–0.12 mg/kg'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year')}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 1, 'increment': 1, 'incrementEveryDays': 7, 'max': 7}}, [R(Gf, '2.2')],
          notes=[note('افزایش حداکثر ۱ mg در هفته؛ هدف ۰٫۰۵ تا ۰٫۱۲ mg/kg/روز (۱ تا ۷ mg). قرص کامل بلعیده شود؛ با غذای پرچرب نه. ناگهانی قطع نشود. با گوانفاسین سریع‌رهش میلی‌گرم به میلی‌گرم جایگزین نشود.', 'Increase by no more than 1 mg/week; target 0.05–0.12 mg/kg/day (1–7 mg). Swallow whole; not with high-fat meals. Do not stop abruptly. Not interchangeable mg-for-mg with immediate-release guanfacine.', [R(Gf, '2.2'), R(Gf, '2.1'), R(Gf, '2.3')])])],
     [CI('hyper', 'حساسیت به گوانفاسین.', 'Hypersensitivity to guanfacine.', [R(Gf, '4')])],
     exs=[ex('adhd', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=10, weightKg=30)])

Tx = fda('trintellix', 'FDA Trintellix', 'Trintellix (vortioxetine) tablets — Prescribing Information', sid('trintellix'))
drug('vortioxetine', 'nervous-system', 'وورتیوکستین', 'Vortioxetine', T('ضدافسردگی چندحالته', 'Multimodal antidepressant'), [{'name': 'Trintellix', 'market': 'US'}], ['trintellix', 'brintellix', 'ترینتلیکس', 'وورتیوکستین'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Tx, '3')]) for m in (5, 10, 20)],
     [reg('mdd', 'mdd', T('افسردگی اساسی — شروع ۱۰ mg یک بار در روز، سپس ۲۰ mg', 'Major depression — start 10 mg once daily, then 20 mg'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 10, 'increment': 10, 'incrementEveryDays': 7, 'targetMin': 20, 'targetMax': 20, 'max': 20}}, [R(Tx, '2.1')],
          notes=[note('در عدم تحمل تا ۵ mg کاهش. پیش از شروع سابقه دوقطبی بررسی شود.', 'May reduce to 5 mg if not tolerated. Screen for bipolar disorder before starting.', [R(Tx, '2.1'), R(Tx, '2.2')])])],
     [CI('ci', 'حساسیت؛ MAOI همزمان، ظرف ۱۴ روز پس از قطع MAOI یا ۲۱ روز پس از قطع وورتیوکستین؛ لینزولید یا متیلن بلو وریدی.', 'Hypersensitivity; MAOIs, within 14 days of stopping an MAOI or 21 days of stopping vortioxetine; linezolid or IV methylene blue.', [R(Tx, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش افکار و رفتار خودکشی در کودکان و جوانان؛ در کودکان تأیید نشده.', 'Boxed warning: increased suicidal thoughts and behaviour in children and young adults; not approved in children.', [R(Tx, 'Boxed Warning')])],
     exs=[ex('mdd', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

# --- neurology ---
Py = fda('pyridostigmine', 'FDA Pyridostigmine', 'Pyridostigmine bromide tablets (Method) — Prescribing Information', sid('pyridostigmine')); d = R(Py, 'Dosage and Administration')
drug('pyridostigmine', 'nervous-system', 'پیریدوستیگمین', 'Pyridostigmine', T('مهارکننده کولین‌استراز', 'Cholinesterase inhibitor'), [{'name': 'Mestinon', 'market': 'US'}], ['mestinon', 'مستینون', 'پیریدوستیگمین'],
     [tab('tab-30', 30, '30 mg tablet', [d])],
     [reg('mg', 'myasthenia-gravis', T('میاستنی گراویس — دوز و دفعات بر اساس پاسخ بیمار', 'Myasthenia gravis — dose and frequency by response'), A18, 'notCalculated',
          {'reason': T('برچسب: میانگین روزانه معادل ۶۰۰ mg (ده قرص ۶۰ mg) با فاصله‌گذاری برای بیشترین اثر؛ موارد خفیف ۱۲۰ تا ۷۲۰ mg و شدید تا ۱۵۰۰ mg در روز. پاسخ ضعیف ممکن است از کم‌دوزی یا بیش‌دوزی (بحران کولینرژیک) باشد.', 'Label: average daily total equivalent to 600 mg (ten 60 mg tablets), spaced for peak effect; mild cases 120–720 mg and severe up to 1,500 mg/day. Poor response may reflect under- or overdosing (cholinergic crisis).')}, [d, R(Py, 'Warnings')])],
     [CI('ci', 'انسداد مکانیکی روده یا مجاری ادراری؛ در آسم با احتیاط.', 'Mechanical intestinal or urinary obstruction; caution in asthma.', [R(Py, 'Contraindications')])])

Rg = fda('rasagiline', 'FDA Rasagiline', 'Rasagiline tablets (Alvogen) — Prescribing Information', sid('rasagiline'))
drug('rasagiline', 'nervous-system', 'رازاژیلین', 'Rasagiline', T('مهارکننده MAO-B', 'MAO-B inhibitor'), [{'name': 'Azilect', 'market': 'US'}], ['azilect', 'آزیلکت', 'رازاژیلین'],
     [tab('tab-0-5', 0.5, '0.5 mg tablet', [R(Rg, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Rg, '3')])],
     [reg('mono', 'parkinsons', T('پارکینسون — تک‌درمانی یا همراه داروی غیر لوودوپا: ۱ mg یک بار در روز', 'Parkinson’s — monotherapy or with non-levodopa drugs: 1 mg once daily'), A18, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Rg, '2.1')],
          notes=[note('با سیپروفلوکساسین یا سایر مهارکننده‌های CYP1A2 و نارسایی خفیف کبد: ۰٫۵ mg؛ در نارسایی متوسط یا شدید کبد مصرف نشود.', 'With ciprofloxacin or other CYP1A2 inhibitors and in mild hepatic impairment: 0.5 mg; not for moderate or severe hepatic impairment.', [R(Rg, '2.2'), R(Rg, '2.3')])]),
      reg('levodopa', 'parkinsons', T('پارکینسون — همراه لوودوپا: ۰٫۵ mg یک بار در روز (تا ۱ mg)', 'Parkinson’s — with levodopa: 0.5 mg once daily (up to 1 mg)'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Rg, '2.1')], limits={'maxPerDose': 1, 'refs': [R(Rg, '2.1')]})],
     [CI('ci', 'مپریدین، ترامادول، متادون، دکسترومتورفان، سیکلوبنزاپرین، علف چای و سایر MAOIها (۱۴ روز فاصله) — خطر سندرم سروتونین.', 'Meperidine, tramadol, methadone, dextromethorphan, cyclobenzaprine, St John’s wort and other MAOIs (14-day gap) — serotonin syndrome risk.', [R(Rg, '4')])],
     exs=[ex('mono', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70), ex('levodopa', 'tab-0-5', {'perDose': 0.5, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

Lc = fda('vimpat', 'FDA Vimpat', 'Vimpat (lacosamide) tablets, injection and oral solution — Prescribing Information', sid('vimpat')); d = R(Lc, '2.1, Table 1')
drug('lacosamide', 'nervous-system', 'لاکوزامید', 'Lacosamide', T('ضدتشنج', 'Anticonvulsant'), [{'name': 'Vimpat', 'market': 'US'}], ['vimpat', 'ویمپت', 'لاکوزامید'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Lc, '3')]) for m in (50, 100, 150, 200)] + [liquid('sol-10', 10, 1, '10 mg/mL oral solution', [R(Lc, '3')], form_='solution')],
     [reg('adult', 'epilepsy', T('تشنج کانونی (افزودنی) — بزرگسال و کودک ۵۰ kg به بالا: شروع ۵۰ mg دو بار در روز', 'Partial-onset seizures (adjunctive) — adults and children ≥50 kg: start 50 mg twice daily'), {'minWeightKg': 50}, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 100, 'increment': 100, 'incrementEveryDays': 7, 'targetMin': 200, 'targetMax': 400, 'max': 400}}, [d],
          notes=[note('هفتگی ۵۰ mg دو بار در روز افزایش. نگهدارنده افزودنی ۱۰۰ تا ۲۰۰ mg دو بار؛ تک‌درمانی بزرگسال: شروع ۱۰۰ mg دو بار، نگهدارنده ۱۵۰ تا ۲۰۰ mg دو بار.', 'Increase weekly by 50 mg twice daily. Adjunctive maintenance 100–200 mg twice daily; adult monotherapy: start 100 mg twice daily, maintain 150–200 mg twice daily.', [d])]),
      reg('child', 'epilepsy', T('تشنج کانونی — کودک ۱۱ تا کمتر از ۵۰ kg: شروع ۱ mg/kg دو بار در روز', 'Partial-onset seizures — child 11 to <50 kg: start 1 mg/kg twice daily'), {'minAge': age(1, 'month'), 'minWeightKg': 11, 'maxWeightKg': 49.99}, 'weightBased', {'perKgPerDose': 1, 'intervalHours': 12}, [d],
          notes=[note('هفتگی ۱ mg/kg دو بار افزایش. نگهدارنده: ۱۱ تا ۳۰ kg ← ۳ تا ۶ mg/kg دو بار؛ ۳۰ تا ۵۰ kg ← ۲ تا ۴ mg/kg دو بار.', 'Increase weekly by 1 mg/kg twice daily. Maintenance: 11–30 kg → 3–6 mg/kg twice daily; 30–50 kg → 2–4 mg/kg twice daily.', [d])])],
     exs=[ex('adult', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('child', 'sol-10', {'perDose': 20, 'mlPerDose': 2}, ageYears=6, weightKg=20)])

Et = fda('ethosuximide', 'FDA Ethosuximide soln', 'Ethosuximide oral solution 250 mg/5 mL (Mylan) — Prescribing Information', sid('ethosuximide')); d = R(Et, 'Dosage and Administration')
drug('ethosuximide', 'nervous-system', 'اتوسوکسیماید', 'Ethosuximide', T('ضدتشنج سوکسینیمید', 'Succinimide anticonvulsant'), [{'name': 'Zarontin', 'market': 'US'}], ['zarontin', 'زارونتین', 'اتوسوکسیماید'],
     [liquid('sol-250-5', 250, 5, '250 mg / 5 mL oral solution', [R(Et, 'How Supplied')], form_='solution')],
     [reg('absence', 'absence-epilepsy', T('صرع ابسانس — شروع: ۳ تا ۶ سال ۲۵۰ mg و ۶ سال به بالا ۵۰۰ mg در روز', 'Absence epilepsy — start: 3–6 y 250 mg/day; ≥6 y 500 mg/day'), {'minAge': age(3, 'year')}, 'ageBand',
          {'bands': [{'minAge': age(3, 'year'), 'maxAge': age(6, 'year'), 'perDose': 250, 'dosesPerDay': 1}, {'minAge': age(6, 'year'), 'maxAge': None, 'perDose': 500, 'dosesPerDay': 1}]}, [d],
          notes=[note('هر ۴ تا ۷ روز ۲۵۰ mg در روز افزایش تا کنترل. دوز بهینه بیشتر کودکان ۲۰ mg/kg/روز. بالای ۱٫۵ g در روز (در دوزهای منقسم) فقط با نظارت دقیق.', 'Increase by 250 mg/day every 4–7 days until controlled. Optimal for most children 20 mg/kg/day. Above 1.5 g/day (divided) only under strict supervision.', [d])])],
     [CI('hyper', 'حساسیت به سوکسینیمیدها.', 'Hypersensitivity to succinimides.', [R(Et, 'Contraindications')])],
     warn=[W('دیسکرازی خونی (گاهی کشنده) و ترومبوسیتوپنی ایمنی؛ شمارش خون دوره‌ای.', 'Blood dyscrasias (sometimes fatal) and immune thrombocytopenia; periodic blood counts.', [R(Et, 'Warnings')])],
     exs=[ex('absence', 'sol-250-5', {'perDose': 250, 'mlPerDose': 5}, ageYears=4, weightKg=16), ex('absence', 'sol-250-5', {'perDose': 500, 'mlPerDose': 10}, ageYears=8, weightKg=25)])

Cb = fda('onfi', 'FDA Onfi', 'Onfi (clobazam) tablets and oral suspension — Prescribing Information', sid('onfi')); d = R(Cb, '2.1, Table 1')
drug('clobazam', 'nervous-system', 'کلوبازام', 'Clobazam', T('بنزودیازپین ضدتشنج', 'Benzodiazepine anticonvulsant'), [{'name': 'Onfi', 'market': 'US'}], ['onfi', 'frisium', 'فریزیوم', 'کلوبازام'],
     [tab('tab-10', 10, '10 mg tablet (scored)', [R(Cb, '3')], scored=True), tab('tab-20', 20, '20 mg tablet (scored)', [R(Cb, '3')], scored=True), liquid('susp-2-5', 2.5, 1, '2.5 mg/mL oral suspension', [R(Cb, '3')])],
     [reg('lgs', 'lennox-gastaut', T('لنوکس-گاستو (افزودنی، ۲ سال به بالا) — دوز شروع بر اساس وزن', 'Lennox-Gastaut (adjunctive, ≥2 y) — starting dose by weight'), {'minAge': age(2, 'year')}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 30, 'perDose': 5, 'dosesPerDay': 1}, {'minWeightKg': 30, 'maxWeightKg': None, 'perDose': 5, 'dosesPerDay': 2}]}, [d],
          notes=[note('۳۰ kg و کمتر: ۵ mg/روز، روز ۷ ← ۱۰ mg، روز ۱۴ ← ۲۰ mg. بالای ۳۰ kg: ۱۰ mg/روز، روز ۷ ← ۲۰ mg، روز ۱۴ ← ۴۰ mg. بالای ۵ mg در روز در ۲ دوز. سریع‌تر از هفتگی افزایش نه؛ قطع تدریجی.', '≤30 kg: 5 mg/day, day 7 → 10 mg, day 14 → 20 mg. >30 kg: 10 mg/day, day 7 → 20 mg, day 14 → 40 mg. Above 5 mg/day give in 2 doses. No faster than weekly; taper to stop.', [d, R(Cb, '2.2')])])],
     [CI('hyper', 'سابقه حساسیت به کلوبازام.', 'History of hypersensitivity to clobazam.', [R(Cb, '4')])],
     warn=[W('هشدار جعبه‌ای: مصرف همزمان با اپیوئید (آرام‌بخشی شدید، دپرسیون تنفسی، مرگ)، سوءمصرف و وابستگی، واکنش ترک.', 'Boxed warning: concomitant opioids (profound sedation, respiratory depression, death), abuse and dependence, withdrawal reactions.', [R(Cb, 'Boxed Warning')])],
     exs=[ex('lgs', 'susp-2-5', {'perDose': 5, 'mlPerDose': 2}, ageYears=6, weightKg=20), ex('lgs', 'tab-10', {'perDose': 5, 'tabletsPerDoseRounded': 0.5, 'dosesPerDay': 2}, ageYears=14, weightKg=45)])

Ng = fda('nurtec', 'FDA Nurtec ODT', 'Nurtec ODT (rimegepant) — Prescribing Information', sid('nurtec'))
drug('rimegepant', 'nervous-system', 'ریمژپانت', 'Rimegepant', T('آنتاگونیست گیرنده CGRP', 'CGRP receptor antagonist'), [{'name': 'Nurtec ODT', 'market': 'US'}], ['nurtec', 'vydura', 'نورتک', 'ریمژپانت'],
     [tab('odt-75', 75, '75 mg orally disintegrating tablet', [R(Ng, '3')], form_='odt')],
     [reg('acute', 'migraine-acute', T('حمله میگرن — ۷۵ mg در صورت نیاز (حداکثر ۷۵ mg در ۲۴ ساعت)', 'Acute migraine — 75 mg as needed (max 75 mg per 24 h)'), A18, 'fixed', {'perDose': 75, 'dosesPerDay': 1}, [R(Ng, '2.1')], limits={'maxPerDay': 75, 'refs': [R(Ng, '2.1')]},
          notes=[note('ایمنی بیش از ۱۸ دوز در ۳۰ روز ثابت نشده. روی یا زیر زبان بدون آب.', 'Safety of more than 18 doses in 30 days not established. On or under the tongue, no water needed.', [R(Ng, '2.1'), R(Ng, '2.3')])]),
      reg('prev', 'migraine-prophylaxis', T('پیشگیری میگرن اپیزودیک — ۷۵ mg یک روز در میان', 'Episodic migraine prevention — 75 mg every other day'), A18, 'notCalculated',
          {'reason': T('۷۵ mg یک روز در میان (نه روزانه)، با یا بدون غذا.', '75 mg every OTHER day (not daily), with or without food.')}, [R(Ng, '2.2')])],
     [CI('hyper', 'سابقه حساسیت به ریمژپانت.', 'History of hypersensitivity to rimegepant.', [R(Ng, '4')])],
     exs=[ex('acute', 'odt-75', {'perDose': 75, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=60)])

# --- eye ---
Vg = fda('vigamox', 'FDA Vigamox', 'Vigamox (moxifloxacin 0.5%) ophthalmic solution — Prescribing Information', sid('vigamox'))
drug('moxifloxacin-eye', 'sensory-organs', 'قطره چشمی موکسی‌فلوکساسین', 'Moxifloxacin eye drops', T('فلوروکینولون چشمی', 'Ophthalmic fluoroquinolone'), [{'name': 'Vigamox', 'market': 'US'}], ['vigamox', 'ویگاموکس', 'موکسی فلوکساسین چشمی'],
     [drops('sol-05', 'Moxifloxacin 0.5% eye drops', Vg)],
     [reg('conj', 'bacterial-conjunctivitis', T('ورم ملتحمه باکتریایی — یک قطره ۳ بار در روز، ۷ روز', 'Bacterial conjunctivitis — 1 drop three times daily, 7 days'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 3}, [R(Vg, '2')], unit='drop', dur={'min': 7, 'max': 7})],
     [CI('hyper', 'حساسیت به موکسی‌فلوکساسین یا سایر کینولون‌ها.', 'Hypersensitivity to moxifloxacin or other quinolones.', [R(Vg, '4')])],
     exs=[ex('conj', 'sol-05', {'perDose': 1, 'dosesPerDay': 3}, ageYears=30, weightKg=70)])

Bm = fda('brimonidine', 'FDA Brimonidine 0.1%', 'Brimonidine tartrate ophthalmic solution 0.1% (Lifestar) — Prescribing Information', sid('alphagan'))
drug('brimonidine', 'sensory-organs', 'قطره چشمی بریمونیدین', 'Brimonidine eye drops', T('آگونیست α2 (کاهش فشار چشم)', 'α2 agonist (IOP-lowering)'), [{'name': 'Alphagan P', 'market': 'US'}], ['alphagan', 'آلفاگان', 'بریمونیدین'],
     [drops('sol-01', 'Brimonidine tartrate 0.1% eye drops', Bm)],
     [reg('iop', 'glaucoma', T('گلوکوم زاویه باز یا فشار بالای چشم — یک قطره ۳ بار در روز (هر ۸ ساعت)', 'Open-angle glaucoma or ocular hypertension — 1 drop three times daily (every 8 h)'), {'minAge': age(2, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 3}, [R(Bm, '2')], unit='drop',
          notes=[note('با سایر قطره‌ها دست‌کم ۵ دقیقه فاصله.', 'At least 5 minutes apart from other eye drops.', [R(Bm, '2')])])],
     [CI('infant', 'نوزاد و شیرخوار زیر ۲ سال.', 'Neonates and infants under 2 years.', [R(Bm, '4')], rule={'maxAge': age(2, 'year')}), CI('hyper', 'واکنش حساسیتی قبلی.', 'Previous hypersensitivity reaction.', [R(Bm, '4')])],
     exs=[ex('iop', 'sol-01', {'perDose': 1, 'dosesPerDay': 3}, ageYears=60, weightKg=70)])

Co = fda('cosopt', 'FDA Dorzolamide/timolol', 'Dorzolamide hydrochloride and timolol maleate ophthalmic solution (Aurobindo) — Prescribing Information', sid('cosopt'))
drug('dorzolamide-timolol', 'sensory-organs', 'قطره چشمی دورزولامید + تیمولول', 'Dorzolamide + timolol eye drops', T('مهارکننده کربنیک انیدراز + بتابلاکر', 'Carbonic anhydrase inhibitor + beta-blocker'), [{'name': 'Cosopt', 'market': 'US'}], ['cosopt', 'کوزوپت', 'دورزولامید تیمولول'],
     [drops('sol', 'Dorzolamide 2% + timolol 0.5% eye drops', Co)],
     [reg('iop', 'glaucoma', T('گلوکوم یا فشار بالای چشم — یک قطره دو بار در روز', 'Glaucoma or ocular hypertension — 1 drop twice daily'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 2}, [R(Co, '2')], unit='drop',
          notes=[note('با سایر قطره‌ها دست‌کم ۵ دقیقه فاصله.', 'At least 5 minutes apart from other eye drops.', [R(Co, '2')])])],
     [CI('ci', 'آسم یا سابقه آسم، COPD شدید؛ برادی‌کاردی سینوسی، بلوک AV درجه ۲ یا ۳، نارسایی آشکار قلب، شوک کاردیوژنیک؛ حساسیت.', 'Asthma or history of asthma, severe COPD; sinus bradycardia, 2nd/3rd-degree AV block, overt heart failure, cardiogenic shock; hypersensitivity.', [R(Co, '4')])],
     exs=[ex('iop', 'sol', {'perDose': 1, 'dosesPerDay': 2}, ageYears=60, weightKg=70)])

Az = fda('acetazolamide', 'FDA Acetazolamide', 'Acetazolamide tablets (Ajanta) — Prescribing Information', sid('acetazolamide')); d = R(Az, 'Dosage and Administration')
drug('acetazolamide', 'sensory-organs', 'استازولامید', 'Acetazolamide', T('مهارکننده کربنیک انیدراز', 'Carbonic anhydrase inhibitor'), [{'name': 'Diamox', 'market': 'US'}], ['diamox', 'دیاموکس', 'استازولامید'],
     [tab('tab-125', 125, '125 mg tablet (scored)', [R(Az, 'How Supplied')], scored=True), tab('tab-250', 250, '250 mg tablet (quarter-scored)', [R(Az, 'How Supplied')], scored=True)],
     [reg('glaucoma', 'glaucoma', T('گلوکوم زاویه باز (کمکی) — ۲۵۰ mg تا ۱ g در روز در دوزهای منقسم', 'Open-angle glaucoma (adjunct) — 250 mg–1 g/day in divided doses'), A18, 'fixed', {'perDose': 250, 'dosesPerDay': 1}, [d], limits={'maxPerDay': 1000, 'refs': [d]},
          notes=[note('بیش از ۲۵۰ mg در دوزهای منقسم؛ بالای ۱ g در روز اثر بیشتری ندارد. گلوکوم ثانویه و پیش از جراحی گلوکوم حاد زاویه بسته طبق برچسب.', 'Divide doses above 250 mg; more than 1 g/day adds no effect. Secondary and acute angle-closure glaucoma per label.', [d])]),
      reg('ams', 'altitude-sickness', T('بیماری کوهستان — ۵۰۰ تا ۱۰۰۰ mg در روز در دوزهای منقسم', 'Acute mountain sickness — 500–1,000 mg/day in divided doses'), A18, 'fixed', {'perDose': 250, 'perDoseMax': 500, 'dosesPerDay': 2}, [R(Az, 'Dosage and Administration — Acute Mountain Sickness')],
          notes=[note('بهتر است ۲۴ تا ۴۸ ساعت پیش از صعود شروع و تا ۴۸ ساعت در ارتفاع ادامه. صعود سریع (امداد، نظامی): ۱۰۰۰ mg.', 'Preferably start 24–48 h before ascent and continue for 48 h at altitude. Rapid ascent (rescue, military): 1,000 mg.', [R(Az, 'Dosage and Administration — Acute Mountain Sickness')])])],
     [CI('ci', 'حساسیت به استازولامید یا سولفونامیدها؛ کمبود سدیم یا پتاسیم؛ بیماری شدید کلیه یا کبد؛ نارسایی آدرنال؛ اسیدوز هیپرکلرمیک.', 'Hypersensitivity to acetazolamide or sulfonamides; low sodium or potassium; marked renal or hepatic disease; adrenal failure; hyperchloraemic acidosis.', [R(Az, 'Contraindications')])],
     exs=[ex('glaucoma', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70), ex('ams', 'tab-250', {'perDose': 250, 'upperPerDose': 500}, ageYears=30, weightKg=70)])

Rs = fda('restasis', 'FDA Restasis', 'Restasis MultiDose (cyclosporine 0.05%) ophthalmic emulsion — Prescribing Information', sid('restasis'))
drug('cyclosporine-eye', 'sensory-organs', 'قطره چشمی سیکلوسپورین', 'Cyclosporine eye emulsion', T('تعدیل‌کننده ایمنی چشمی', 'Ophthalmic immunomodulator'), [{'name': 'Restasis', 'market': 'US'}], ['restasis', 'رستاسیس', 'سیکلوسپورین چشمی'],
     [drops('em-005', 'Cyclosporine 0.05% ophthalmic emulsion', Rs)],
     [reg('dry', 'dry-eye', T('خشکی چشم (افزایش تولید اشک) — یک قطره دو بار در روز در هر چشم', 'Dry eye (to increase tear production) — 1 drop twice daily in each eye'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 2}, [R(Rs, '2.2')], unit='drop',
          notes=[note('حدود ۱۲ ساعت فاصله؛ با اشک مصنوعی ۱۵ دقیقه فاصله. نوک بطری به چشم نخورد.', 'About 12 h apart; 15 min apart from artificial tears. Do not touch the bottle tip to the eye.', [R(Rs, '2.1'), R(Rs, '5.1')])])],
     [CI('hyper', 'حساسیت شناخته‌شده یا مشکوک به اجزا.', 'Known or suspected hypersensitivity to any ingredient.', [R(Rs, '4')])],
     exs=[ex('dry', 'em-005', {'perDose': 1, 'dosesPerDay': 2}, ageYears=50, weightKg=65)])

Td = fda('tobradex-st', 'FDA TobraDex ST', 'TobraDex ST (tobramycin/dexamethasone) ophthalmic suspension — Prescribing Information', sid('tobradex'))
drug('tobramycin-dexamethasone-eye', 'sensory-organs', 'قطره چشمی توبرامایسین + دگزامتازون', 'Tobramycin + dexamethasone eye drops', T('آنتی‌بیوتیک + کورتیکواستروئید چشمی', 'Ophthalmic antibiotic + corticosteroid'), [{'name': 'TobraDex', 'market': 'US'}], ['tobradex', 'توبرادکس', 'توبرامایسین دگزامتازون'],
     [drops('susp', 'Tobramycin 0.3% + dexamethasone 0.05% suspension', Td)],
     [reg('std', 'ocular-inflammation', T('التهاب چشم پاسخ‌دهنده به کورتون با عفونت یا خطر عفونت باکتریایی — یک قطره هر ۴ تا ۶ ساعت', 'Steroid-responsive eye inflammation with bacterial infection or risk — 1 drop every 4–6 h'), {'minAge': age(2, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 4}, [R(Td, '2.1')], unit='drop',
          notes=[note('در ۲۴ تا ۴۸ ساعت اول می‌توان هر ۲ ساعت. با بهبود به‌تدریج کم شود. پیش از تجویز و تمدید فشار چشم و معاینه با اسلیت‌لامپ.', 'In the first 24–48 h may be every 2 h. Taper gradually with improvement. Check IOP and slit-lamp examination before prescribing and renewing.', [R(Td, '2.1')])])],
     [CI('ci', 'بیشتر بیماری‌های ویروسی قرنیه و ملتحمه (هرپس دندریتیک، واکسینیا، آبله‌مرغان)، عفونت مایکوباکتریایی یا قارچی چشم؛ حساسیت.', 'Most viral diseases of cornea and conjunctiva (dendritic herpes, vaccinia, varicella), mycobacterial or fungal eye infection; hypersensitivity.', [R(Td, '4')])],
     exs=[ex('std', 'susp', {'perDose': 1, 'dosesPerDay': 4}, ageYears=40, weightKg=70)])

Kt = fda('acular', 'FDA Acular', 'Acular (ketorolac 0.5%) ophthalmic solution — Prescribing Information', sid('acular'))
drug('ketorolac-eye', 'sensory-organs', 'قطره چشمی کتورولاک', 'Ketorolac eye drops', T('NSAID چشمی', 'Ophthalmic NSAID'), [{'name': 'Acular', 'market': 'US'}], ['acular', 'آکولار', 'کتورولاک چشمی'],
     [drops('sol-05', 'Ketorolac tromethamine 0.5% eye drops', Kt)],
     [reg('itch', 'allergic-conjunctivitis', T('خارش چشم در ورم ملتحمه آلرژیک فصلی — یک قطره ۴ بار در روز', 'Itching of seasonal allergic conjunctivitis — 1 drop four times daily'), {'minAge': age(2, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 4}, [R(Kt, '2.1')], unit='drop'),
      reg('postop', 'ocular-inflammation', T('التهاب پس از جراحی آب‌مروارید — یک قطره ۴ بار در روز از ۲۴ ساعت بعد تا ۲ هفته', 'Post-cataract inflammation — 1 drop four times daily from 24 h after surgery for 2 weeks'), A18, 'fixed', {'perDose': 1, 'dosesPerDay': 4}, [R(Kt, '2.1')], unit='drop', dur={'min': 14, 'max': 14})],
     [CI('hyper', 'حساسیت به اجزای فرآورده.', 'Hypersensitivity to any ingredient.', [R(Kt, '4')])],
     warn=[W('تأخیر در ترمیم، حساسیت متقاطع با آسپرین و NSAIDها، افزایش زمان خونریزی و کراتیت.', 'Delayed healing, cross-sensitivity with aspirin and NSAIDs, prolonged bleeding time and keratitis.', [R(Kt, '5')])],
     exs=[ex('itch', 'sol-05', {'perDose': 1, 'dosesPerDay': 4}, ageYears=25, weightKg=60), ex('postop', 'sol-05', {'perDose': 1, 'dosesPerDay': 4}, ageYears=70, weightKg=70)])
print('s8 ok')
