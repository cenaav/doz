"""Stage 9c — gap drugs: GI, cardiac, endocrine, hospital antibiotics, HIV, pain, psychiatry/neurology, respiratory, urology."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's9_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}

# --- new diseases ---
add_disease('acromegaly', 'آکرومگالی', 'Acromegaly', ['acromegaly', 'آکرومگالی', 'غول‌آسایی', 'هورمون رشد زیاد'], ['E22.0'], 'endocrinology')
add_disease('carcinoid-tumors', 'تومورهای کارسینوئید و VIPoma (اسهال و برافروختگی)', 'Carcinoid tumours and VIPomas (diarrhoea and flushing)', ['carcinoid', 'vipoma', 'کارسینوئید', 'ویپوما'], ['E34.0'], 'oncology')
add_disease('hiv', 'عفونت HIV (درمان)', 'HIV-1 infection (treatment)', ['HIV', 'AIDS', 'ایدز', 'اچ آی وی', 'ضدرتروویروس'], ['B20'], 'infectious')
add_disease('intra-abdominal-infection', 'عفونت عارضه‌دار داخل شکم و پریتونیت', 'Complicated intra-abdominal infection and peritonitis', ['peritonitis', 'appendicitis', 'پریتونیت', 'عفونت شکمی', 'آپاندیسیت پاره'], ['K65.9'], 'infectious')
add_disease('febrile-neutropenia', 'تب و نوتروپنی (درمان تجربی)', 'Febrile neutropenia (empiric therapy)', ['neutropenic fever', 'تب نوتروپنیک', 'نوتروپنی'], ['D70.9'], 'infectious')
add_disease('hospital-acquired-pneumonia', 'پنومونی بیمارستانی', 'Hospital-acquired (nosocomial) pneumonia', ['HAP', 'VAP', 'nosocomial pneumonia', 'پنومونی بیمارستانی', 'ذات‌الریه بیمارستانی'], ['J18.9'], 'infectious')
add_disease('bipolar-depression', 'افسردگی دوقطبی', 'Bipolar I depression', ['bipolar depression', 'دوقطبی افسرده', 'افسردگی دو قطبی'], ['F31.30'], 'psychiatry')
add_disease('schizoaffective-disorder', 'اختلال اسکیزوافکتیو', 'Schizoaffective disorder', ['schizoaffective', 'اسکیزوافکتیو'], ['F25.9'], 'psychiatry')
add_disease('neurogenic-bladder', 'مثانه نوروژنیک (بیش‌فعالی عصبی دترسور)', 'Neurogenic detrusor overactivity', ['NDO', 'neurogenic bladder', 'مثانه عصبی', 'مثانه نوروژنیک'], ['N31.9'], 'urology')
add_disease('general-anesthesia', 'بیهوشی عمومی و پیش‌دارو (کمکی)', 'General anaesthesia and premedication (adjunct)', ['anesthesia', 'بیهوشی', 'پیش دارو', 'premedication'], ['Z01.818'], 'procedures')

def ml(aid, title, review):
    m, dd, y = review.split('/')
    return add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                   edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
NOTE = {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}
def symptoms(did, items, *srcs):
    d = json.load(open(os.path.join(ROOT, 'diseases.json')))
    for x in d:
        if x['id'] == did:
            x['symptoms'] = {'items': [T(fa, en) for fa, en in items], 'refs': [{'source': s, 'section': 'Symptoms', 'note': NOTE} for s in srcs]}
    json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')

symptoms('acromegaly', [('بزرگ شدن دست و پا (تغییر سایز انگشتر یا کفش)', 'Large hands and feet (change in ring or shoe size)'), ('درشت شدن استخوان‌های صورت، فک و زبان؛ فاصله بین دندان‌ها', 'Large facial bones, jaw and tongue; gaps between teeth'),
                        ('سردرد', 'Headache'), ('تعریق زیاد و بوی بدن', 'Excessive sweating and body odour'), ('درد و تورم مفاصل', 'Joint pain and swelling'), ('سندرم تونل کارپ', 'Carpal tunnel syndrome'), ('آپنه خواب', 'Sleep apnoea'),
                        ('کاهش دید محیطی', 'Decreased peripheral vision'), ('پوست ضخیم و چرب', 'Thick, oily skin'), ('خستگی و ضعف عضلانی', 'Fatigue and muscle weakness'), ('صدای گرفته', 'Hoarseness')], ml('000321', 'Acromegaly', '4/24/2025'))
symptoms('carcinoid-tumors', [('برافروختگی صورت، گردن یا بالای سینه', 'Flushing of the face, neck or upper chest'), ('اسهال', 'Diarrhoea'), ('خس‌خس و تنگی نفس', 'Wheezing and difficulty breathing'),
                              ('مشکلات قلبی: نارسایی دریچه، تغییر فشار، تپش قلب', 'Heart problems: leaking valves, blood pressure changes, palpitations'), ('تشدید با فعالیت یا برخی غذاها و نوشیدنی‌ها', 'Triggered by exertion or certain foods and drinks')],
         ml('000347', 'Carcinoid syndrome', '7/29/2024'))
symptoms('intra-abdominal-infection', [('درد شکم', 'Abdominal pain'), ('نفخ و بزرگ شدن شکم', 'Swollen abdomen'), ('تب', 'Fever'), ('تهوع و استفراغ', 'Nausea and vomiting'), ('بی‌اشتهایی', 'Loss of appetite'),
                                       ('تشنگی و ادرار کم', 'Thirst and low urine output'), ('ممکن است علائم شوک باشد', 'Signs of shock may be present')], ml('000651', 'Peritonitis - secondary', '4/27/2026'))
symptoms('hospital-acquired-pneumonia', [('در سالمندان: گیجی یا تغییر وضعیت ذهنی (گاهی اولین علامت)', 'In older adults: confusion or mental change (may be the first sign)'), ('سرفه با خلط سبز یا چرکی', 'Cough with green or pus-like sputum'),
                                         ('تب و لرز', 'Fever and chills'), ('درد تیز قفسه سینه با نفس عمیق یا سرفه', 'Sharp chest pain worse with deep breathing or coughing'), ('تنگی نفس و تنفس تند', 'Shortness of breath and fast breathing'),
                                         ('افت فشار و ضربان تند', 'Low blood pressure and fast heart rate'), ('بی‌اشتهایی، تهوع و استفراغ', 'Loss of appetite, nausea and vomiting')], ml('000146', 'Hospital-acquired pneumonia', '7/25/2025'))
symptoms('bipolar-depression', [('خلق پایین یا غمگینی روزانه', 'Daily low mood or sadness'), ('از دست دادن لذت از فعالیت‌ها', 'Loss of pleasure in activities'), ('خستگی و بی‌انرژی بودن', 'Fatigue or lack of energy'),
                                ('اشکال در تمرکز، حافظه یا تصمیم‌گیری', 'Problems concentrating, remembering or deciding'), ('احساس بی‌ارزشی، ناامیدی یا گناه', 'Feelings of worthlessness, hopelessness or guilt'),
                                ('تغییر اشتها و وزن', 'Changes in appetite and weight'), ('بی‌خوابی یا پرخوابی', 'Trouble sleeping or sleeping too much'), ('افکار مرگ یا خودکشی', 'Thoughts of death or suicide'), ('دوره‌های مانیا در سابقه', 'History of manic episodes')],
         ml('000926', 'Bipolar disorder', '7/17/2024'))
symptoms('schizoaffective-disorder', [('توهم (دیدن یا شنیدن چیزهای غیرواقعی)', 'Hallucinations'), ('هذیان، مثلاً بدبینی', 'Delusions, e.g. paranoia'), ('گفتار آشفته و غیرمنطقی', 'Disorganised, illogical speech'),
                                      ('خلق خیلی بالا، افسرده یا تحریک‌پذیر', 'Mood too high, depressed or irritable'), ('اختلال خواب و تمرکز', 'Problems with sleep and concentration'), ('بی‌توجهی به بهداشت فردی', 'Poor hygiene and grooming'), ('انزوای اجتماعی', 'Social isolation')],
         ml('000930', 'Schizoaffective disorder', '5/15/2026'))
symptoms('neurogenic-bladder', [('ادرار مکرر با حجم کم', 'Frequent urination in small amounts'), ('بی‌اختیاری و از دست دادن کنترل مثانه', 'Incontinence and loss of bladder control'), ('تخلیه ناقص مثانه', 'Problems emptying the bladder fully'),
                                ('احتباس ادرار یا ندانستن پر بودن مثانه (مثانه کم‌کار)', 'Urinary retention or not sensing a full bladder (underactive bladder)')], ml('000754', 'Neurogenic bladder', '5/4/2026'))

# ===================== GI =====================
Rb = fda('rabeprazole', 'FDA Rabeprazole', 'Rabeprazole sodium delayed-release tablets — Prescribing Information', sid('rabeprazole'))
drug('rabeprazole', 'alimentary-metabolism', 'رابپرازول', 'Rabeprazole', T('مهارکننده پمپ پروتون', 'Proton pump inhibitor'), [{'name': 'Aciphex', 'market': 'US'}], ['aciphex', 'pariet', 'رابپرازول', 'پاریت'],
     [tab('tab-20', 20, '20 mg delayed-release tablet (swallow whole)', [R(Rb, '3')])],
     [reg('erosive', 'erosive-esophagitis', T('ازوفاژیت اروزیو — ۲۰ mg روزانه ۴ تا ۸ هفته', 'Erosive GERD — 20 mg daily for 4–8 weeks'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Rb, '2')], dur={'min': 28, 'max': 56},
          notes=[note('نگهدارنده پس از بهبود: ۲۰ mg روزانه. قرص کامل بلعیده شود.', 'Maintenance of healing: 20 mg daily. Swallow whole.', [R(Rb, '2')])]),
      reg('gerd', 'gerd', T('ریفلاکس علامت‌دار (۱۲ سال به بالا) — ۲۰ mg روزانه تا ۴ هفته', 'Symptomatic GERD (≥12 y) — 20 mg daily up to 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Rb, '2')], dur={'min': 28, 'max': 56},
          notes=[note('نوجوان ۱۲ سال به بالا: تا ۸ هفته.', 'Adolescents ≥12 y: up to 8 weeks.', [R(Rb, '2')])]),
      reg('du', 'peptic-ulcer-disease', T('زخم دوازدهه — ۲۰ mg روزانه پس از صبحانه تا ۴ هفته', 'Duodenal ulcer — 20 mg daily after the morning meal up to 4 weeks'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Rb, '2')], dur={'min': 28, 'max': 28}),
      reg('hp', 'h-pylori', T('ریشه‌کنی هلیکوباکتر — ۲۰ mg دو بار در روز + آموکسی‌سیلین ۱ g + کلاریترومایسین ۵۰۰ mg، ۷ روز', 'H. pylori eradication — 20 mg twice daily + amoxicillin 1 g + clarithromycin 500 mg, 7 days'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 2}, [R(Rb, '2')], dur={'min': 7, 'max': 7},
          notes=[note('هر سه دارو دو بار در روز با صبحانه و شام.', 'All three drugs twice daily with morning and evening meals.', [R(Rb, '2')])])],
     [CI('ci', 'حساسیت به رابپرازول یا بنزیمیدازول‌های جایگزین‌شده؛ مصرف همزمان ریلپیویرین.', 'Hypersensitivity to rabeprazole or substituted benzimidazoles; concomitant rilpivirine.', [R(Rb, '4')])],
     inter=[IA('rilpivirine', 'ریلپیویرین: منع مصرف همزمان.', 'Rilpivirine: contraindicated.', [R(Rb, '4')])],
     exs=[ex('erosive', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('hp', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Gr = fda('granisetron', 'FDA Granisetron tab', 'Granisetron hydrochloride tablets 1 mg — Prescribing Information', sid('granisetron'))
drug('granisetron', 'alimentary-metabolism', 'گرانیسترون', 'Granisetron', T('آنتاگونیست 5-HT3 (ضدتهوع)', '5-HT3 antagonist (antiemetic)'), [{'name': 'Kytril', 'market': 'US'}], ['kytril', 'گرانیسترون'],
     [tab('tab-1', 1, '1 mg tablet', [R(Gr, 'How Supplied')])],
     [reg('cinv', 'cinv', T('پیشگیری از تهوع شیمی‌درمانی — ۲ mg یک بار (یا ۱ mg دو بار) فقط در روز شیمی‌درمانی', 'Chemotherapy nausea prevention — 2 mg once (or 1 mg twice) on chemotherapy days only'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Gr, 'Dosage and Administration')],
          notes=[note('تا ۱ ساعت پیش از شیمی‌درمانی. رژیم دیگر: ۱ mg تا ۱ ساعت قبل و ۱ mg دوم ۱۲ ساعت بعد.', 'Up to 1 h before chemotherapy. Alternative: 1 mg up to 1 h before and a second 1 mg 12 h later.', [R(Gr, 'Dosage and Administration')])])],
     [CI('hyper', 'حساسیت به گرانیسترون یا اجزای فرآورده.', 'Hypersensitivity to granisetron or its components.', [R(Gr, 'Contraindications')])],
     warn=[W('سندرم سروتونین با داروهای سروتونرژیک.', 'Serotonin syndrome with serotonergic drugs.', [R(Gr, 'Warnings')])],
     exs=[ex('cinv', 'tab-1', {'perDose': 2, 'tabletsPerDoseRounded': 2}, ageYears=50, weightKg=70)])

# ===================== cardiovascular =====================
Pg = fda('prasugrel', 'FDA Prasugrel', 'Prasugrel tablets 5/10 mg — Prescribing Information', sid('prasugrel'))
LOAD = note('شروع با دوز بارگذاری ۶۰ mg یک‌جا، سپس روزانه. همراه آسپرین ۷۵ تا ۳۲۵ mg روزانه. ۷۵ سال به بالا معمولاً توصیه نمی‌شود.', 'Start with a single 60 mg loading dose, then daily. With aspirin 75–325 mg daily. Generally not recommended at ≥75 y.', [R(Pg, '2'), R(Pg, '5')])
drug('prasugrel', 'blood', 'پراسوگرل', 'Prasugrel', T('مهارکننده P2Y12 (ضدپلاکت)', 'P2Y12 inhibitor (antiplatelet)'), [{'name': 'Effient', 'market': 'US'}], ['effient', 'پراسوگرل'],
     [tab('tab-5', 5, '5 mg tablet', [R(Pg, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Pg, '3')])],
     [reg('acs', 'acute-coronary-syndrome', T('سندرم حاد کرونری با PCI — ۱۰ mg روزانه (پس از بارگذاری ۶۰ mg)', 'ACS managed with PCI — 10 mg daily (after a 60 mg load)'), {'minAge': age(18, 'year'), 'minWeightKg': 60}, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Pg, '2')], notes=[LOAD]),
      reg('acs-low', 'acute-coronary-syndrome', T('وزن زیر ۶۰ kg — ۵ mg روزانه (پس از بارگذاری ۶۰ mg)', 'Weight <60 kg — 5 mg daily (after a 60 mg load)'), {'minAge': age(18, 'year'), 'maxWeightKg': 59.99}, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(Pg, '2')], notes=[LOAD])],
     [CI('bleed', 'خونریزی فعال پاتولوژیک؛ سابقه TIA یا سکته مغزی؛ حساسیت.', 'Active pathological bleeding; prior TIA or stroke; hypersensitivity.', [R(Pg, '4')])],
     warn=[W('هشدار جعبه‌ای: خونریزی شدید و گاه کشنده. در ≥۷۵ سال معمولاً توصیه نمی‌شود. ۷ روز پیش از جراحی قطع شود.', 'Boxed warning: significant, sometimes fatal bleeding. Generally not recommended at ≥75 y. Stop 7 days before surgery.', [R(Pg, 'Boxed Warning')])],
     exs=[ex('acs', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80), ex('acs-low', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=55)])

Dz = fda('doxazosin', 'FDA Doxazosin', 'Doxazosin tablets (Apotex) — Prescribing Information', sid('doxazosin'))
FIRST = lambda src, sec: note('افت فشار وضعیتی و غش با دوز اول یا افزایش دوز؛ فشار تا ۶ ساعت پایش شود. شروع شب‌هنگام بهتر است.', 'Postural hypotension and syncope with the first dose or dose increases; monitor BP for up to 6 h.', [R(src, sec)])
drug('doxazosin', 'cardiovascular', 'دوکسازوسین', 'Doxazosin', T('آلفا-۱ بلاکر', 'Alpha-1 blocker'), [{'name': 'Cardura', 'market': 'US'}], ['cardura', 'دوکسازوسین'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(Dz, '3')], scored=True) for m in (1, 2, 4, 8)],
     [reg('bph', 'bph', T('BPH — شروع ۱ mg روزانه، دو برابر هر ۱ تا ۲ هفته تا حداکثر ۸ mg', 'BPH — start 1 mg daily, double every 1–2 weeks up to 8 mg'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 1, 'incrementEveryDays': 7, 'max': 8}}, [R(Dz, '2.2')], notes=[FIRST(Dz, '2.1')]),
      reg('htn', 'hypertension', T('فشار خون — شروع ۱ mg روزانه، تا حداکثر ۱۶ mg', 'Hypertension — start 1 mg daily, up to 16 mg'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 1, 'incrementEveryDays': 7, 'max': 16}}, [R(Dz, '2.3')], notes=[FIRST(Dz, '2.1')])],
     [CI('hyper', 'حساسیت به کینازولین‌ها (پرازوسین، ترازوسین، دوکسازوسین).', 'Hypersensitivity to quinazolines (prazosin, terazosin, doxazosin).', [R(Dz, '4')])],
     inter=[IA('pde5', 'مهارکننده‌های PDE5: افت فشار علامت‌دار.', 'PDE5 inhibitors: symptomatic hypotension.', [R(Dz, '5')])],
     exs=[ex('bph', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75), ex('htn', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=80)])

Tz = fda('terazosin', 'FDA Terazosin', 'Terazosin capsules — Prescribing Information', sid('terazosin')); d = R(Tz, 'Dosage and Administration')
drug('terazosin', 'genitourinary-sex-hormones', 'ترازوسین', 'Terazosin', T('آلفا-۱ بلاکر', 'Alpha-1 blocker'), [{'name': 'Hytrin', 'market': 'US'}], ['hytrin', 'ترازوسین'],
     [tab(f'cap-{m}', m, f'{m} mg capsule', [R(Tz, 'How Supplied')], per='capsule', form_='capsule') for m in (1, 2, 5, 10)],
     [reg('bph', 'bph', T('BPH — ۱ mg هنگام خواب، سپس پله‌ای ۲، ۵ و ۱۰ mg روزانه', 'BPH — 1 mg at bedtime, then stepwise to 2, 5 and 10 mg daily'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 1, 'targetMin': 10, 'targetMax': 10, 'max': 20}}, [d],
          notes=[note('دوز اول از ۱ mg بیشتر نشود. معمولاً ۱۰ mg لازم است و پاسخ پس از ۴ تا ۶ هفته ارزیابی می‌شود؛ داده ۲۰ mg محدود است. اگر چند روز قطع شد از ۱ mg شروع شود.', 'Do not exceed 1 mg as the first dose. 10 mg is usually needed; assess response after 4–6 weeks; data at 20 mg are limited. Restart at 1 mg after a break of several days.', [d])])],
     [CI('hyper', 'حساسیت به ترازوسین.', 'Hypersensitivity to terazosin.', [R(Tz, 'Contraindications')])],
     warn=[W('غش و افت فشار با دوز اول (اثر دوز اول).', 'Syncope and first-dose hypotension.', [R(Tz, 'Warnings')])],
     exs=[ex('bph', 'cap-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

So = fda('sotalol', 'FDA Sotalol', 'Sotalol hydrochloride tablets (Apotex) — Prescribing Information', sid('sotalol'))
SOT = note('شروع در مرکز با پایش ECG دست‌کم ۳ روز. افزایش ۸۰ mg/روز هر ۳ روز فقط اگر QTc زیر ۵۰۰ ms.', 'Start in a facility with ECG monitoring for at least 3 days. Increase by 80 mg/day every 3 days only if QTc <500 ms.', [R(So, '2.1'), R(So, '2.2')])
drug('sotalol', 'cardiovascular', 'سوتالول', 'Sotalol', T('ضدآریتمی کلاس III (بتابلاکر)', 'Class III antiarrhythmic (beta-blocker)'), [{'name': 'Betapace', 'market': 'US'}], ['betapace', 'سوتالول'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(So, '3')], scored=True) for m in (80, 120, 160, 240)],
     [reg('vt', 'ventricular-arrhythmia', T('آریتمی بطنی تهدیدکننده حیات — شروع ۸۰ mg دو بار در روز؛ معمولاً ۱۶۰ تا ۳۲۰ mg/روز', 'Life-threatening ventricular arrhythmia — start 80 mg twice daily; usually 160–320 mg/day'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 160, 'increment': 80, 'incrementEveryDays': 3, 'targetMin': 160, 'targetMax': 320, 'max': 640}}, [R(So, '2.2')],
          notes=[SOT, note('در آریتمی مقاوم تا ۴۸۰ تا ۶۴۰ mg/روز به کار رفته است.', 'Up to 480–640 mg/day has been used for refractory arrhythmias.', [R(So, '2.2')])]),
      reg('af', 'atrial-fibrillation', T('پیشگیری از عود AF/فلوتر — شروع ۸۰ mg دو بار در روز؛ اغلب ۱۲۰ mg دو بار', 'Maintenance of sinus rhythm in AF/AFL — start 80 mg twice daily; most respond to 120 mg twice daily'), A18, 'fixed',
          {'perDose': 80, 'perDoseMax': 120, 'dosesPerDay': 2}, [R(So, '2.3')], notes=[SOT, note('QTc بالای ۴۵۰ ms در شروع: منع مصرف.', 'Contraindicated if baseline QTc >450 ms.', [R(So, '2.3')])])],
     [CI('ci', 'برادی‌کاردی سینوسی، سندرم سینوس بیمار یا بلوک AV درجه ۲ و ۳ بدون پیس‌میکر؛ QT طولانی؛ شوک کاردیوژنیک یا نارسایی جبران‌نشده؛ پتاسیم زیر ۴؛ آسم برونشیال؛ حساسیت.',
         'Sinus bradycardia, sick sinus syndrome or 2nd/3rd-degree AV block without a pacemaker; long QT; cardiogenic shock or decompensated heart failure; serum potassium <4 mEq/L; bronchial asthma; hypersensitivity.', [R(So, '4')])],
     warn=[W('هشدار جعبه‌ای: آریتمی کشنده (تورساد). شروع و افزایش دوز در مرکز با پایش ECG و محاسبه کلیرانس کراتینین.', 'Boxed warning: life-threatening proarrhythmia (torsade). Initiate and up-titrate in a facility with ECG monitoring and creatinine clearance calculation.', [R(So, 'Boxed Warning')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('فاصله دوز: ClCr ۳۰ تا ۵۹ هر ۲۴ ساعت؛ ۱۰ تا ۲۹ هر ۳۶ تا ۴۸ ساعت؛ زیر ۱۰ فردی. افزایش دوز پس از دست‌کم ۵ دوز.', 'Interval: CrCl 30–59 every 24 h; 10–29 every 36–48 h; <10 individualised. Escalate after at least 5 doses.'), 'refs': [R(So, '2.5')]}],
     exs=[ex('vt', 'tab-80', {'perDose': 80, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=75), ex('af', 'tab-80', {'perDose': 80, 'upperPerDose': 120}, ageYears=60, weightKg=75)])

Pf = fda('propafenone', 'FDA Propafenone', 'Propafenone hydrochloride tablets — Prescribing Information', sid('propafenone'))
PFT = {'dividedDoses': 3, 'titration': {'start': 450, 'increment': 225, 'incrementEveryDays': 4, 'max': 900}}
PFN = note('۱۵۰ mg هر ۸ ساعت؛ پس از دست‌کم ۳ تا ۴ روز به ۲۲۵ و سپس ۳۰۰ mg هر ۸ ساعت. در بیماری ساختاری قلب نه.', '150 mg every 8 h; after at least 3–4 days to 225 then 300 mg every 8 h. Not with structural heart disease.', [R(Pf, '2')])
drug('propafenone', 'cardiovascular', 'پروپافنون', 'Propafenone', T('ضدآریتمی کلاس IC', 'Class IC antiarrhythmic'), [{'name': 'Rythmol', 'market': 'US'}], ['rythmol', 'پروپافنون'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(Pf, '3')], scored=True) for m in (150, 225, 300)],
     [reg('paf', 'atrial-fibrillation', T('AF حمله‌ای بدون بیماری ساختاری قلب — ۱۵۰ mg هر ۸ ساعت (تا ۹۰۰ mg/روز)', 'Paroxysmal AF without structural heart disease — 150 mg every 8 h (up to 900 mg/day)'), A18, 'titration', PFT, [R(Pf, '2')], notes=[PFN]),
      reg('psvt', 'svt', T('PSVT بدون بیماری ساختاری قلب — ۱۵۰ mg هر ۸ ساعت', 'PSVT without structural heart disease — 150 mg every 8 h'), A18, 'titration', PFT, [R(Pf, '2')], notes=[PFN])],
     [CI('ci', 'نارسایی قلبی؛ شوک کاردیوژنیک؛ اختلال گره سینوسی، دهلیزی-بطنی یا داخل‌بطنی بدون پیس‌میکر؛ سندرم بروگادا؛ برادی‌کاردی یا افت فشار شدید؛ بیماری برونکواسپاستیک؛ اختلال الکترولیت.',
         'Heart failure; cardiogenic shock; sinoatrial, AV or intraventricular conduction disorders without a pacemaker; Brugada syndrome; marked bradycardia or hypotension; bronchospastic disorders; electrolyte imbalance.', [R(Pf, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ‌ومیر در کارآزمایی CAST؛ فقط برای آریتمی‌های تهدیدکننده یا علامت‌دار در بیمار بدون بیماری ساختاری.', 'Boxed warning: increased mortality (CAST); reserve for documented life-threatening or symptomatic arrhythmias without structural heart disease.', [R(Pf, 'Boxed Warning')])],
     exs=[ex('paf', 'tab-150', {'perDose': 150, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=75)])

Fl = fda('flecainide', 'FDA Flecainide', 'Flecainide acetate tablets — Prescribing Information', sid('flecainide')); d = R(Fl, 'Dosage and Administration')
drug('flecainide', 'cardiovascular', 'فلکائینید', 'Flecainide', T('ضدآریتمی کلاس IC', 'Class IC antiarrhythmic'), [{'name': 'Tambocor', 'market': 'US'}], ['tambocor', 'فلکاینید', 'فلکائینید'],
     [tab('tab-50', 50, '50 mg tablet', [R(Fl, 'How Supplied')]), tab('tab-100', 100, '100 mg tablet (scored)', [R(Fl, 'How Supplied')], scored=True), tab('tab-150', 150, '150 mg tablet (scored)', [R(Fl, 'How Supplied')], scored=True)],
     [reg('pafpsvt', 'atrial-fibrillation', T('PAF یا PSVT — ۵۰ mg هر ۱۲ ساعت، افزایش ۵۰ mg دو بار در روز هر ۴ روز، حداکثر ۳۰۰ mg/روز', 'PAF or PSVT — 50 mg every 12 h, +50 mg twice daily every 4 days, max 300 mg/day'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 100, 'increment': 100, 'incrementEveryDays': 4, 'max': 300}}, [d]),
      reg('psvt', 'svt', T('PSVT — ۵۰ mg هر ۱۲ ساعت (حداکثر ۳۰۰ mg/روز)', 'PSVT — 50 mg every 12 h (max 300 mg/day)'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 100, 'increment': 100, 'incrementEveryDays': 4, 'max': 300}}, [d]),
      reg('vt', 'ventricular-arrhythmia', T('VT پایدار — ۱۰۰ mg هر ۱۲ ساعت، حداکثر ۴۰۰ mg/روز (شروع در بیمارستان)', 'Sustained VT — 100 mg every 12 h, max 400 mg/day (start in hospital)'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 200, 'increment': 100, 'incrementEveryDays': 4, 'targetMax': 300, 'max': 400}}, [d],
          notes=[note('با پایش ریتم در بیمارستان شروع شود؛ بیشتر بیماران بیش از ۱۵۰ mg هر ۱۲ ساعت لازم ندارند. افزایش دوز زودتر از هر ۴ روز نه.', 'Start in hospital with rhythm monitoring; most need no more than 150 mg every 12 h. Increase no more often than every 4 days.', [d])])],
     [CI('ci', 'بلوک AV درجه ۲ یا ۳، یا بلوک دودسته‌ای بدون پیس‌میکر؛ شوک کاردیوژنیک؛ حساسیت.', 'Pre-existing 2nd/3rd-degree AV block or bifascicular block without a pacemaker; cardiogenic shock; hypersensitivity.', [R(Fl, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ‌ومیر پس از MI (CAST)؛ در AF مزمن توصیه نمی‌شود؛ اثر پروآریتمیک.', 'Boxed warning: excess mortality after MI (CAST); not recommended for chronic AF; proarrhythmic effects.', [R(Fl, 'Warnings')])],
     exs=[ex('pafpsvt', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=75), ex('vt', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80)])

Am = fda('amiloride', 'FDA Amiloride', 'Amiloride hydrochloride tablets 5 mg — Prescribing Information', sid('amiloride')); d = R(Am, 'Dosage and Administration')
AMN = note('همراه غذا. معمولاً همراه دیورتیک دفع‌کننده پتاسیم؛ تا ۱۰ mg (در هیپوکالمی پایدار تا ۱۵ تا ۲۰ mg با پایش الکترولیت).', 'With food. Usually added to a kaliuretic diuretic; up to 10 mg (15–20 mg for persistent hypokalaemia, with electrolyte monitoring).', [d])
drug('amiloride', 'cardiovascular', 'آمیلوراید', 'Amiloride', T('دیورتیک نگهدارنده پتاسیم', 'Potassium-sparing diuretic'), [{'name': 'Midamor', 'market': 'US'}], ['midamor', 'آمیلوراید', 'آمیلورید'],
     [tab('tab-5', 5, '5 mg tablet', [R(Am, 'How Supplied')])],
     [reg('htn', 'hypertension', T('فشار خون (کمکی همراه تیازید) — ۵ mg روزانه، تا ۱۰ mg', 'Hypertension (adjunct to a thiazide) — 5 mg daily, up to 10 mg'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 1}, [d], notes=[AMN]),
      reg('hf', 'heart-failure', T('نارسایی قلبی (کمکی همراه دیورتیک) — ۵ mg روزانه، تا ۱۰ mg', 'Heart failure (adjunct to a diuretic) — 5 mg daily, up to 10 mg'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 1}, [d], notes=[AMN])],
     [CI('ci', 'پتاسیم بالای ۵٫۵؛ مصرف داروهای نگهدارنده پتاسیم دیگر (اسپیرونولاکتون، تریامترن) یا مکمل پتاسیم (جز هیپوکالمی شدید با پایش)؛ آنوری، نارسایی حاد یا مزمن کلیه، نفروپاتی دیابتی.', 'Serum potassium >5.5 mEq/L; other potassium-conserving agents (spironolactone, triamterene) or potassium supplements (except severe hypokalaemia with monitoring); anuria, acute or chronic renal insufficiency, diabetic nephropathy.', [R(Am, 'Contraindications')])],
     warn=[W('هیپرکالمی (پتاسیم بالای ۵٫۵) که اگر اصلاح نشود کشنده است؛ بدون دیورتیک دفع‌کننده پتاسیم حدود ۱۰٪ رخ می‌دهد.', 'Hyperkalaemia (K >5.5 mEq/L), potentially fatal if uncorrected; occurs in about 10% without a kaliuretic diuretic.', [R(Am, 'Warnings')])],
     exs=[ex('htn', 'tab-5', {'perDose': 5, 'upperPerDose': 10}, ageYears=60, weightKg=75)])

Mz = fda('metolazone', 'FDA Metolazone', 'Metolazone tablets 2.5/5/10 mg — Prescribing Information', sid('metolazone')); d = R(Mz, 'Dosage and Administration')
drug('metolazone', 'cardiovascular', 'متولازون', 'Metolazone', T('دیورتیک شبه‌تیازیدی', 'Thiazide-like diuretic'), [{'name': 'Zaroxolyn', 'market': 'US'}], ['zaroxolyn', 'متولازون'],
     [tab(f'tab-{str(m).replace(".", "-")}', m, f'{m} mg tablet', [R(Mz, 'How Supplied')]) for m in (2.5, 5, 10)],
     [reg('edema', 'edema', T('ادم نارسایی قلبی یا بیماری کلیه — ۵ تا ۲۰ mg یک بار در روز', 'Oedema of heart failure or renal disease — 5–20 mg once daily'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 20, 'dosesPerDay': 1}, [d]),
      reg('htn', 'hypertension', T('فشار خون خفیف تا متوسط — ۲٫۵ تا ۵ mg یک بار در روز', 'Mild–moderate hypertension — 2.5–5 mg once daily'), A18, 'fixed', {'perDose': 2.5, 'perDoseMax': 5, 'dosesPerDay': 1}, [d],
          notes=[note('با Mykrox جایگزین‌پذیر نیست (فراهمی زیستی متفاوت).', 'Not interchangeable with Mykrox (different bioavailability).', [d])])],
     [CI('ci', 'آنوری؛ کمای کبدی یا پیش‌کما؛ حساسیت به متولازون.', 'Anuria; hepatic coma or pre-coma; hypersensitivity to metolazone.', [R(Mz, 'Contraindications')])],
     exs=[ex('edema', 'tab-5', {'perDose': 5, 'upperPerDose': 20}, ageYears=65, weightKg=80), ex('htn', 'tab-2-5', {'perDose': 2.5, 'upperPerDose': 5}, ageYears=55, weightKg=80)])

# ===================== endocrine =====================
INS_CI = lambda src: CI('hypo', 'هنگام هیپوگلیسمی؛ حساسیت به انسولین یا اجزای فرآورده.', 'During episodes of hypoglycaemia; hypersensitivity to the insulin or its excipients.', [R(src, '4')])
Hl = fda('humalog', 'FDA Humalog', 'Humalog (insulin lispro) injection — Prescribing Information', sid('humalog'))
drug('insulin-lispro', 'alimentary-metabolism', 'انسولین لیسپرو', 'Insulin lispro', T('انسولین سریع‌الاثر', 'Rapid-acting insulin'), [{'name': 'Humalog', 'market': 'US'}], ['humalog', 'هومالوگ', 'لیسپرو'],
     [liquid('u100', 100, 1, '100 units/mL (U-100) vial, cartridge or KwikPen', [R(Hl, '3')], form_='injection', route='sc', unit='unit'), liquid('u200', 200, 1, '200 units/mL (U-200) KwikPen', [R(Hl, '3')], form_='injection', route='sc', unit='unit')],
     [reg('t1', 'type-1-diabetes', T('دیابت — دوز فردی، ۱۵ دقیقه قبل یا بلافاصله پس از غذا', 'Diabetes — individualised, within 15 min before or right after a meal'), {}, 'notCalculated',
          {'reason': T('برچسب: دوز بر اساس نیاز متابولیک، پایش قند و هدف درمان فردی شود. زیرجلدی ظرف ۱۵ دقیقه قبل یا بلافاصله پس از غذا؛ معمولاً همراه انسولین پایه. U-200 فقط با قلم مخصوص.', 'Label: individualise by metabolic needs, glucose monitoring and goals. SC within 15 min before or right after a meal; usually with a basal insulin. U-200 only in its own pen.')}, [R(Hl, '2.3'), R(Hl, '2.1')]),
      reg('t2', 'type-2-diabetes', T('دیابت نوع ۲ — دوز فردی همراه غذا', 'Type 2 diabetes — individualised mealtime dose'), A18, 'notCalculated',
          {'reason': T('برچسب: دوز فردی بر اساس پایش قند؛ زیرجلدی ظرف ۱۵ دقیقه قبل یا بلافاصله پس از غذا.', 'Label: individualise by glucose monitoring; SC within 15 min before or right after a meal.')}, [R(Hl, '2.3')])],
     [INS_CI(Hl)], warn=[W('هیپوگلیسمی؛ هیپوکالمی؛ قلم یا سرنگ مشترک بین بیماران ممنوع.', 'Hypoglycaemia; hypokalaemia; never share pens or syringes.', [R(Hl, '5')])])

Tb = fda('tresiba', 'FDA Tresiba', 'Tresiba (insulin degludec) injection — Prescribing Information', sid('tresiba'))
drug('insulin-degludec', 'alimentary-metabolism', 'انسولین دگلودک', 'Insulin degludec', T('انسولین پایه بسیار طولانی‌اثر', 'Ultra-long-acting basal insulin'), [{'name': 'Tresiba', 'market': 'US'}], ['tresiba', 'ترسیبا', 'دگلودک'],
     [liquid('u100', 100, 1, '100 units/mL (U-100) FlexTouch pen or vial', [R(Tb, '3')], form_='injection', route='sc', unit='unit'), liquid('u200', 200, 1, '200 units/mL (U-200) FlexTouch pen', [R(Tb, '3')], form_='injection', route='sc', unit='unit')],
     [reg('t2-naive', 'type-2-diabetes', T('دیابت نوع ۲، شروع انسولین — ۱۰ واحد یک بار در روز', 'Type 2 diabetes, insulin-naive — 10 units once daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Tb, '2.3')], unit='unit',
          notes=[note('هر روز در هر ساعتی؛ تنظیم دوز هر ۳ تا ۴ روز بر اساس قند ناشتا.', 'Any time of day; titrate every 3–4 days by fasting glucose.', [R(Tb, '2.2')])]),
      reg('t1', 'type-1-diabetes', T('دیابت نوع ۱ — یک‌سوم تا نیمی از کل دوز روزانه به‌صورت پایه', 'Type 1 diabetes — one-third to one-half of total daily insulin as basal'), {'minAge': age(1, 'year')}, 'notCalculated',
          {'reason': T('بیمار بدون انسولین قبلی: کل انسولین روزانه حدود ۰٫۲ تا ۰٫۴ واحد/kg؛ یک‌سوم تا نیمی از آن دگلودک یک بار در روز و بقیه انسولین کوتاه‌اثر با غذا. تنظیم هر ۳ تا ۴ روز.', 'Insulin-naive: total daily insulin about 0.2–0.4 units/kg; one-third to one-half as degludec once daily, the rest as short-acting with meals. Titrate every 3–4 days.')}, [R(Tb, '2.3')])],
     [INS_CI(Tb)], warn=[W('هیپوگلیسمی؛ هیپوکالمی؛ قلم مشترک ممنوع؛ برای کتواسیدوز نه.', 'Hypoglycaemia; hypokalaemia; never share pens; not for diabetic ketoacidosis.', [R(Tb, '5'), R(Tb, '1')])],
     exs=[ex('t2-naive', 'u100', {'perDose': 10, 'mlPerDose': 0.1}, ageYears=55, weightKg=90)])

Tr = fda('trulicity', 'FDA Trulicity', 'Trulicity (dulaglutide) injection — Prescribing Information', sid('trulicity'))
drug('dulaglutide', 'alimentary-metabolism', 'دولاگلوتاید', 'Dulaglutide', T('آگونیست GLP-1 هفتگی', 'Weekly GLP-1 agonist'), [{'name': 'Trulicity', 'market': 'US'}], ['trulicity', 'تروليسيتی', 'دولاگلوتاید'],
     [unitform('pen', 'injection', 'sc', 'Single-dose pen 0.75 / 1.5 / 3 / 4.5 mg in 0.5 mL', [R(Tr, '3')])],
     [reg('t2', 'type-2-diabetes', T('دیابت نوع ۲ — هفته‌ای یک بار: ۰٫۷۵ mg، سپس ۱٫۵ mg؛ حداکثر ۴٫۵ mg', 'Type 2 diabetes — once weekly: 0.75 mg, then 1.5 mg; max 4.5 mg'), A18, 'notCalculated',
          {'reason': T('هفته‌ای یک بار زیرجلدی (نه روزانه). شروع ۰٫۷۵ mg؛ پس از ۴ هفته ۱٫۵ mg؛ در صورت نیاز هر دست‌کم ۴ هفته ۱٫۵ mg افزایش تا حداکثر ۴٫۵ mg.', 'Once WEEKLY SC (not daily). Start 0.75 mg; after 4 weeks 1.5 mg; if needed increase by 1.5 mg after at least 4 weeks, to a max of 4.5 mg.')}, [R(Tr, '2.1')]),
      reg('t2-child', 'type-2-diabetes', T('دیابت نوع ۲ کودک (۱۰ سال به بالا) — هفته‌ای ۰٫۷۵ mg، حداکثر ۱٫۵ mg', 'Type 2 diabetes, children ≥10 y — 0.75 mg weekly, max 1.5 mg'), {'minAge': age(10, 'year'), 'maxAge': age(18, 'year')}, 'notCalculated',
          {'reason': T('هفته‌ای یک بار ۰٫۷۵ mg؛ در صورت نیاز پس از دست‌کم ۴ هفته ۱٫۵ mg (حداکثر).', 'Once weekly 0.75 mg; if needed, 1.5 mg after at least 4 weeks (maximum).')}, [R(Tr, '2.2')])],
     [CI('mtc', 'سابقه شخصی یا خانوادگی کارسینوم مدولاری تیروئید یا MEN 2؛ حساسیت جدی.', 'Personal or family history of medullary thyroid carcinoma or MEN 2; serious hypersensitivity.', [R(Tr, '4')])],
     warn=[W('هشدار جعبه‌ای: تومور سلول C تیروئید در جوندگان.', 'Boxed warning: thyroid C-cell tumours in rodents.', [R(Tr, 'Boxed Warning')])])

Fo = fda('forteo', 'FDA Forteo', 'Forteo (teriparatide) injection — Prescribing Information', sid('forteo'))
drug('teriparatide', 'systemic-hormones', 'تری‌پاراتاید', 'Teriparatide', T('آنالوگ هورمون پاراتیروئید (آنابولیک استخوان)', 'Parathyroid hormone analogue (bone anabolic)'), [{'name': 'Forteo', 'market': 'US'}], ['forteo', 'فورتئو', 'تری پاراتاید', 'سینوریتید'],
     [liquid('pen', 250, 1, 'Pen 250 mcg/mL (20 mcg per dose)', [R(Fo, '3')], form_='injection', route='sc', unit='mcg')],
     [reg('op', 'osteoporosis', T('پوکی استخوان پرخطر — ۲۰ mcg زیرجلدی یک بار در روز', 'High-risk osteoporosis — 20 mcg SC once daily'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Fo, '2.1')], unit='mcg',
          notes=[note('در ران یا شکم. دوز اول در وضعیت نشسته یا درازکش (افت فشار وضعیتی).', 'Into the thigh or abdomen. Give the first doses sitting or lying down (orthostatic hypotension).', [R(Fo, '2.2')])])],
     [CI('hyper', 'حساسیت به تری‌پاراتاید یا اجزای فرآورده.', 'Hypersensitivity to teriparatide or its excipients.', [R(Fo, '4')])],
     exs=[ex('op', 'pen', {'perDose': 20, 'mlPerDose': 0.08}, ageYears=70, weightKg=60)])

Ib = fda('ibandronate', 'FDA Ibandronate', 'Ibandronate sodium tablets 150 mg — Prescribing Information', sid('ibandronate'))
drug('ibandronate', 'musculoskeletal', 'ایباندرونات', 'Ibandronate', T('بیس‌فسفونات', 'Bisphosphonate'), [{'name': 'Boniva', 'market': 'US'}], ['boniva', 'بونیوا', 'ایباندرونیک اسید'],
     [tab('tab-150', 150, '150 mg tablet', [R(Ib, '3')])],
     [reg('op', 'osteoporosis', T('پوکی استخوان پس از یائسگی — ۱۵۰ mg ماهی یک بار', 'Postmenopausal osteoporosis — 150 mg once MONTHLY'), A18, 'notCalculated',
          {'reason': T('ماهی یک بار (نه روزانه) در یک تاریخ ثابت. ناشتا با یک لیوان پر آب ساده، دست‌کم ۶۰ دقیقه پیش از غذا، نوشیدنی یا داروی دیگر؛ تا ۶۰ دقیقه دراز نکشد؛ قرص جویده یا مکیده نشود. کلسیم و ویتامین D کافی.', 'Once MONTHLY (not daily) on the same date. Fasting with a full glass of plain water, at least 60 min before food, drink or other drugs; stay upright for 60 min; do not chew or suck. Adequate calcium and vitamin D.')}, [R(Ib, '2.1'), R(Ib, '2.2'), R(Ib, '2.3')])],
     [CI('ci', 'ناهنجاری مری که تخلیه آن را به تأخیر می‌اندازد (تنگی، آشالازی)؛ ناتوانی در ایستادن یا نشستن صاف به مدت ۶۰ دقیقه؛ هیپوکلسمی؛ حساسیت.', 'Oesophageal abnormalities delaying emptying (stricture, achalasia); inability to stand or sit upright for 60 min; hypocalcaemia; hypersensitivity.', [R(Ib, '4')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('کلیرانس کراتینین زیر ۳۰: توصیه نمی‌شود.', 'CrCl <30 mL/min: not recommended.'), 'refs': [R(Ib, '8.6')]}])

Lt = fda('liothyronine', 'FDA Liothyronine', 'Liothyronine sodium tablets 5/25/50 mcg — Prescribing Information', sid('liothyronine'))
drug('liothyronine', 'systemic-hormones', 'لیوتیرونین (T3)', 'Liothyronine (T3)', T('هورمون تیروئید', 'Thyroid hormone'), [{'name': 'Cytomel', 'market': 'US'}], ['cytomel', 'T3', 'لیوتیرونین', 'تری یدوتیرونین'],
     [form('tab-5', 'tablet', 'oral', '5 mcg tablet', 5, 'mcg', [R(Lt, '3')], per='tablet', scored=False), form('tab-25', 'tablet', 'oral', '25 mcg tablet (scored)', 25, 'mcg', [R(Lt, '3')], per='tablet', scored=True),
      form('tab-50', 'tablet', 'oral', '50 mcg tablet (scored)', 50, 'mcg', [R(Lt, '3')], per='tablet', scored=True)],
     [reg('hypo', 'hypothyroidism', T('کم‌کاری تیروئید — شروع ۲۵ mcg روزانه؛ نگهدارنده معمولاً ۲۵ تا ۷۵ mcg', 'Hypothyroidism — start 25 mcg daily; usual maintenance 25–75 mcg'), A18, 'fixed', {'perDose': 25, 'perDoseMax': 75, 'dosesPerDay': 1}, [R(Lt, '2.2')], unit='mcg',
          notes=[note('افزایش ۲۵ mcg هر ۱ تا ۲ هفته بر اساس TSH. سالمند یا بیمار قلبی: شروع ۵ mcg.', 'Increase by 25 mcg every 1–2 weeks by TSH. Elderly or cardiac patients: start 5 mcg.', [R(Lt, '2.2')])])],
     [CI('adrenal', 'نارسایی آدرنال اصلاح‌نشده.', 'Uncorrected adrenal insufficiency.', [R(Lt, '4')])],
     warn=[W('هشدار جعبه‌ای: برای چاقی یا کاهش وزن نه؛ دوز بالا سمیت جدی یا کشنده دارد.', 'Boxed warning: not for obesity or weight loss; large doses can cause serious or life-threatening toxicity.', [R(Lt, 'Boxed Warning')])],
     exs=[ex('hypo', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1, 'upperPerDose': 75}, ageYears=45, weightKg=70)])

Oc = fda('octreotide', 'FDA Octreotide', 'Octreotide acetate injection — Prescribing Information', sid('octreotide'))
drug('octreotide', 'systemic-hormones', 'اکترئوتاید', 'Octreotide', T('آنالوگ سوماتوستاتین', 'Somatostatin analogue'), [{'name': 'Sandostatin', 'market': 'US'}], ['sandostatin', 'ساندوستاتین', 'اکتروتاید'],
     [liquid(f'inj-{c}', c, 1, f'{c} mcg/mL ampule or vial', [R(Oc, '3')], form_='injection', route='sc', unit='mcg') for c in (50, 100, 500)],
     [reg('acro', 'acromegaly', T('آکرومگالی — شروع ۵۰ mcg سه بار در روز؛ نگهدارنده معمولاً ۱۰۰ تا ۵۰۰ mcg سه بار', 'Acromegaly — start 50 mcg three times daily; usual maintenance 100–500 mcg three times daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 3}, [R(Oc, '2.2')], unit='mcg',
          notes=[note('تیتراسیون بر اساس IGF-1 هر ۲ هفته. دوز بالای ۳۰۰ mcg/روز به‌ندرت سود بیشتری دارد.', 'Titrate by IGF-1 every 2 weeks. Doses above 300 mcg/day rarely add benefit.', [R(Oc, '2.2')])]),
      reg('carcinoid', 'carcinoid-tumors', T('کارسینوئید متاستاتیک — ۱۰۰ تا ۶۰۰ mcg/روز در ۲ تا ۴ دوز (۲ هفته اول)', 'Metastatic carcinoid — 100–600 mcg/day in 2–4 doses (first 2 weeks)'), A18, 'notCalculated',
          {'reason': T('۱۰۰ تا ۶۰۰ mcg/روز در ۲ تا ۴ دوز منقسم زیرجلدی در ۲ هفته اول (میانگین ۳۰۰)؛ سپس بر اساس پاسخ.', '100–600 mcg/day SC in 2–4 divided doses for the first 2 weeks (mean 300); then by response.')}, [R(Oc, '2.3')]),
      reg('vipoma', 'carcinoid-tumors', T('VIPoma — ۲۰۰ تا ۳۰۰ mcg/روز در ۲ تا ۴ دوز (۲ هفته اول)', 'VIPoma — 200–300 mcg/day in 2–4 doses (first 2 weeks)'), A18, 'notCalculated',
          {'reason': T('۲۰۰ تا ۳۰۰ mcg/روز در ۲ تا ۴ دوز منقسم زیرجلدی در ۲ هفته اول؛ سپس تنظیم بر اساس پاسخ.', '200–300 mcg/day SC in 2–4 divided doses for the first 2 weeks; then adjust to response.')}, [R(Oc, '2.4')])],
     [CI('hyper', 'حساسیت به اکترئوتاید یا اجزای فرآورده.', 'Sensitivity to octreotide or its components.', [R(Oc, '4')])],
     exs=[ex('acro', 'inj-100', {'perDose': 50, 'mlPerDose': 0.5}, ageYears=45, weightKg=80)])

# ===================== hospital antibiotics =====================
BL_CI = lambda src, extra_fa='', extra_en='': CI('hyper', 'حساسیت به دارو یا آنافیلاکسی با سایر بتالاکتام‌ها' + extra_fa + '.', 'Hypersensitivity to the drug or anaphylaxis with other beta-lactams' + extra_en + '.', [R(src, '4')])
CDI = lambda src: W('واکنش آلرژیک جدی؛ اسهال مرتبط با کلستریدیوم دیفیسیل؛ تشنج (به‌ویژه در نارسایی کلیه).', 'Serious hypersensitivity; Clostridioides difficile-associated diarrhoea; seizures (especially with renal impairment).', [R(src, '5')])
RENAL = lambda src, sec, fa, en, below=50: {'egfrBelow': below, 'severity': 'warn', 'text': T(fa, en), 'refs': [R(src, sec)]}
vial = lambda id, mg, label, src, sec='3': form(id, 'powder-for-injection', 'iv', label, mg, 'mg', [R(src, sec)], per='vial')

Mp = fda('meropenem', 'FDA Meropenem', 'Meropenem for injection 500 mg / 1 g — Prescribing Information', sid('meropenem'))
PEDMAX = lambda src, sec: {'minAge': age(3, 'month'), 'maxWeightKg': 50}
drug('meropenem', 'anti-infectives', 'مروپنم', 'Meropenem', T('کارباپنم', 'Carbapenem'), [{'name': 'Merrem', 'market': 'US'}], ['merrem', 'مروپنم', 'مروپنem'],
     [vial('vial-500', 500, '500 mg vial', Mp), vial('vial-1g', 1000, '1 g vial', Mp)],
     [reg('cssi', 'skin-soft-tissue-infection', T('عفونت عارضه‌دار پوست و بافت نرم — بزرگسال ۵۰۰ mg هر ۸ ساعت', 'Complicated skin and skin-structure infection — adult 500 mg every 8 h'), {'minWeightKg': 50.01}, 'fixed', {'perDose': 500, 'dosesPerDay': 3}, [R(Mp, '2.1')],
          notes=[note('در پسودوموناس آئروژینوزا ۱ g هر ۸ ساعت.', '1 g every 8 h if Pseudomonas aeruginosa is suspected or confirmed.', [R(Mp, '2.1')])]),
      reg('iai', 'intra-abdominal-infection', T('عفونت عارضه‌دار داخل شکم — بزرگسال ۱ g هر ۸ ساعت', 'Complicated intra-abdominal infection — adult 1 g every 8 h'), {'minWeightKg': 50.01}, 'fixed', {'perDose': 1000, 'dosesPerDay': 3}, [R(Mp, '2.1')]),
      reg('cssi-child', 'skin-soft-tissue-infection', T('عفونت عارضه‌دار پوست — کودک ۳ ماه به بالا: ۱۰ mg/kg هر ۸ ساعت (حداکثر ۵۰۰ mg)', 'cSSSI — child ≥3 months: 10 mg/kg every 8 h (max 500 mg)'), PEDMAX(Mp, '2.3'), 'weightBased', {'perKgPerDose': 10, 'intervalHours': 8}, [R(Mp, '2.3')],
          limits={'maxPerDose': 500, 'refs': [R(Mp, '2.3')]}),
      reg('iai-child', 'intra-abdominal-infection', T('عفونت داخل شکم — کودک ۳ ماه به بالا: ۲۰ mg/kg هر ۸ ساعت (حداکثر ۱ g)', 'cIAI — child ≥3 months: 20 mg/kg every 8 h (max 1 g)'), PEDMAX(Mp, '2.3'), 'weightBased', {'perKgPerDose': 20, 'intervalHours': 8}, [R(Mp, '2.3')],
          limits={'maxPerDose': 1000, 'refs': [R(Mp, '2.3')]}),
      reg('mening-child', 'bacterial-meningitis', T('مننژیت باکتریایی — کودک ۳ ماه به بالا: ۴۰ mg/kg هر ۸ ساعت (حداکثر ۲ g)', 'Bacterial meningitis — child ≥3 months: 40 mg/kg every 8 h (max 2 g)'), PEDMAX(Mp, '2.3'), 'weightBased', {'perKgPerDose': 40, 'intervalHours': 8}, [R(Mp, '2.3')],
          limits={'maxPerDose': 2000, 'refs': [R(Mp, '2.3')]}, notes=[note('کودک بالای ۵۰ kg: ۲ g هر ۸ ساعت.', 'Children over 50 kg: 2 g every 8 h.', [R(Mp, '2.3')])])],
     [BL_CI(Mp)], warn=[CDI(Mp)],
     inter=[IA('valproate', 'والپروات: کاهش شدید سطح والپروات و خطر تشنج — همزمان توصیه نمی‌شود.', 'Valproic acid: marked fall in valproate levels and breakthrough seizures — not recommended together.', [R(Mp, '5')])],
     renal=[RENAL(Mp, '2.2', 'ClCr ۲۶ تا ۵۰: دوز معمول هر ۱۲ ساعت؛ ۱۰ تا ۲۵: نصف دوز هر ۱۲ ساعت؛ زیر ۱۰: نصف دوز هر ۲۴ ساعت.', 'CrCl 26–50: usual dose every 12 h; 10–25: half dose every 12 h; <10: half dose every 24 h.')],
     exs=[ex('cssi', 'vial-500', {'perDose': 500, 'dosesPerDay': 3}, ageYears=50, weightKg=70), ex('cssi-child', 'vial-500', {'perDose': 200}, ageYears=5, weightKg=20),
          ex('iai-child', 'vial-1g', {'perDose': 400}, ageYears=5, weightKg=20), ex('mening-child', 'vial-1g', {'perDose': 800}, ageYears=5, weightKg=20)])

Im = fda('imipenem', 'FDA Primaxin', 'Primaxin (imipenem and cilastatin) for injection — Prescribing Information', sid('imipenem'))
drug('imipenem-cilastatin', 'anti-infectives', 'ایمی‌پنم-سیلاستاتین', 'Imipenem-cilastatin', T('کارباپنم', 'Carbapenem'), [{'name': 'Primaxin', 'market': 'US'}], ['primaxin', 'tienam', 'تینام', 'ایمی پنم'],
     [vial('vial-500', 500, '500 mg imipenem + 500 mg cilastatin vial (dose = imipenem)', Im)],
     [reg('adult', 'sepsis', T('عفونت‌های شدید بزرگسال (ClCr ≥۹۰) — ۵۰۰ mg هر ۶ ساعت (یا ۱ g هر ۸ ساعت)', 'Serious infections, adult (CrCl ≥90) — 500 mg every 6 h (or 1 g every 8 h)'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 4}, [R(Im, '2.1')],
          limits={'maxPerDay': 4000, 'refs': [R(Im, '2.1')]}, notes=[note('برای ارگانیسم با حساسیت کمتر: ۱ g هر ۶ ساعت. دوز بر حسب ایمی‌پنم.', 'Less susceptible organisms: 1 g every 6 h. Dose refers to imipenem.', [R(Im, '2.1')])]),
      reg('child', 'sepsis', T('کودک ۳ ماه به بالا (غیر CNS) — ۱۵ تا ۲۵ mg/kg هر ۶ ساعت', 'Child ≥3 months (non-CNS) — 15–25 mg/kg every 6 h'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 15, 'perKgPerDoseMax': 25, 'intervalHours': 6}, [R(Im, '2.2')],
          limits={'maxPerDay': 4000, 'refs': [R(Im, '2.2')]}, notes=[note('برای عفونت CNS کودکان توصیه نمی‌شود (خطر تشنج).', 'Not recommended for pediatric CNS infections (seizure risk).', [R(Im, '2.2')])])],
     [CI('hyper', 'حساسیت به هر جزء فرآورده.', 'Hypersensitivity to any component.', [R(Im, '4')])], warn=[CDI(Im)],
     inter=[IA('valproate', 'والپروات: کاهش سطح و خطر تشنج — همزمان توصیه نمی‌شود.', 'Valproic acid: reduced levels and seizure risk — not recommended.', [R(Im, '5')])],
     renal=[RENAL(Im, '2.3', 'ClCr زیر ۹۰ طبق جدول برچسب کاهش یابد؛ ClCr زیر ۱۵ فقط با دیالیز.', 'Reduce per label table when CrCl <90; CrCl <15 only if dialysis is started within 48 h.', 90)],
     exs=[ex('adult', 'vial-500', {'perDose': 500, 'dosesPerDay': 4}, ageYears=50, weightKg=70), ex('child', 'vial-500', {'perDose': 300, 'upperPerDose': 500}, ageYears=5, weightKg=20)])

Pt = fda('piptazo', 'FDA Pip-tazo', 'Piperacillin and tazobactam for injection 40.5 g pharmacy bulk — Prescribing Information', sid('piptazo'))
PTN = note('دوز بر حسب مجموع پیپراسیلین + تازوباکتام؛ انفوزیون ۳۰ دقیقه‌ای. بطری ۴۰٫۵ گرمی فقط داروخانه (فرآورده‌های تک‌دوز ۲٫۲۵/۳٫۳۷۵/۴٫۵ g هم موجود است).', 'Dose as total piperacillin + tazobactam; 30-min infusion. 40.5 g bottle is a pharmacy bulk package (single-dose 2.25/3.375/4.5 g also exist).', [R(Pt, '2'), R(Pt, '3')])
P_IAI = T('آپاندیسیت یا پریتونیت', 'appendicitis or peritonitis')
drug('piperacillin-tazobactam', 'anti-infectives', 'پیپراسیلین-تازوباکتام', 'Piperacillin-tazobactam', T('پنی‌سیلین + مهارکننده بتالاکتاماز', 'Penicillin + beta-lactamase inhibitor'), [{'name': 'Zosyn', 'market': 'US'}], ['zosyn', 'tazocin', 'تازوسین', 'پیپ تازو'],
     [vial('bulk', 40500, '40.5 g pharmacy bulk bottle (36 g piperacillin + 4.5 g tazobactam)', Pt)],
     [reg('adult', 'intra-abdominal-infection', T('عفونت داخل شکم، پوست، لگن، پنومونی اکتسابی — بزرگسال ۳٫۳۷۵ g هر ۶ ساعت', 'Intra-abdominal, skin, pelvic infections and CAP — adult 3.375 g every 6 h'), A18, 'fixed', {'perDose': 3375, 'dosesPerDay': 4}, [R(Pt, '2.1')], dur={'min': 7, 'max': 10}, notes=[PTN]),
      reg('hap', 'hospital-acquired-pneumonia', T('پنومونی بیمارستانی — بزرگسال ۴٫۵ g هر ۶ ساعت + آمینوگلیکوزید', 'Nosocomial pneumonia — adult 4.5 g every 6 h + an aminoglycoside'), A18, 'fixed', {'perDose': 4500, 'dosesPerDay': 4}, [R(Pt, '2.2')], dur={'min': 7, 'max': 14}, notes=[PTN]),
      reg('iai-infant', 'intra-abdominal-infection', T('آپاندیسیت یا پریتونیت — شیرخوار ۲ تا ۹ ماه: ۹۰ mg/kg هر ۸ ساعت', 'Appendicitis or peritonitis — infant 2–9 months: 90 mg/kg every 8 h'), {'minAge': age(2, 'month'), 'maxAge': age(9, 'month')}, 'weightBased', {'perKgPerDose': 90, 'intervalHours': 8}, [R(Pt, '2.4')], notes=[PTN]),
      reg('iai-child', 'intra-abdominal-infection', T('آپاندیسیت یا پریتونیت — بالای ۹ ماه تا ۴۰ kg: ۱۱۲٫۵ mg/kg هر ۸ ساعت', 'Appendicitis or peritonitis — >9 months up to 40 kg: 112.5 mg/kg every 8 h'), {'minAge': age(9, 'month'), 'maxWeightKg': 40}, 'weightBased', {'perKgPerDose': 112.5, 'intervalHours': 8}, [R(Pt, '2.4')], notes=[PTN]),
      reg('hap-infant', 'hospital-acquired-pneumonia', T('پنومونی بیمارستانی — شیرخوار ۲ تا ۹ ماه: ۹۰ mg/kg هر ۶ ساعت', 'Nosocomial pneumonia — infant 2–9 months: 90 mg/kg every 6 h'), {'minAge': age(2, 'month'), 'maxAge': age(9, 'month')}, 'weightBased', {'perKgPerDose': 90, 'intervalHours': 6}, [R(Pt, '2.4')], notes=[PTN]),
      reg('hap-child', 'hospital-acquired-pneumonia', T('پنومونی بیمارستانی — بالای ۹ ماه تا ۴۰ kg: ۱۱۲٫۵ mg/kg هر ۶ ساعت', 'Nosocomial pneumonia — >9 months up to 40 kg: 112.5 mg/kg every 6 h'), {'minAge': age(9, 'month'), 'maxWeightKg': 40}, 'weightBased', {'perKgPerDose': 112.5, 'intervalHours': 6}, [R(Pt, '2.4')], notes=[PTN])],
     [CI('hyper', 'سابقه واکنش آلرژیک به پنی‌سیلین‌ها، سفالوسپورین‌ها یا مهارکننده‌های بتالاکتاماز.', 'History of allergic reaction to penicillins, cephalosporins or beta-lactamase inhibitors.', [R(Pt, '4')])], warn=[CDI(Pt)],
     renal=[RENAL(Pt, '2.3', 'ClCr ۲۰ تا ۴۰ و زیر ۲۰: کاهش دوز طبق جدول برچسب.', 'CrCl 20–40 and <20: reduce per label table.', 40)],
     exs=[ex('adult', 'bulk', {'perDose': 3375, 'dosesPerDay': 4}, ageYears=50, weightKg=70), ex('iai-child', 'bulk', {'perDose': 2250}, ageYears=5, weightKg=20), ex('hap-infant', 'bulk', {'perDose': 540}, ageMonths=5, weightKg=6)])

Cp = fda('cefepime', 'FDA Cefepime', 'Cefepime for injection 1 g / 2 g — Prescribing Information', sid('cefepime'))
CPN = note('کودک بالای ۴۰ kg یا اگر دوز از بزرگسال بیشتر شود: دوز بزرگسال.', 'Children over 40 kg, or if the calculated dose exceeds it: use the adult dose.', [R(Cp, '2.2')])
PED = {'minAge': age(2, 'month'), 'maxAge': age(16, 'year'), 'maxWeightKg': 40}
drug('cefepime', 'anti-infectives', 'سفپیم', 'Cefepime', T('سفالوسپورین نسل چهارم', 'Fourth-generation cephalosporin'), [{'name': 'Maxipime', 'market': 'US'}], ['maxipime', 'سفپیم', 'سفیپیم'],
     [vial('vial-1g', 1000, '1 g vial', Cp), vial('vial-2g', 2000, '2 g vial', Cp)],
     [reg('pneu', 'community-acquired-pneumonia', T('پنومونی متوسط تا شدید — بزرگسال ۱ تا ۲ g هر ۸ تا ۱۲ ساعت', 'Moderate–severe pneumonia — adult 1–2 g every 8–12 h'), A18, 'fixed', {'perDose': 1000, 'perDoseMax': 2000, 'dosesPerDay': 2}, [R(Cp, '2.1')], dur={'min': 10, 'max': 10},
          notes=[note('پسودوموناس: ۲ g هر ۸ ساعت. ماشین‌حساب دفعات را برای ۱۲ ساعت نشان می‌دهد.', 'Pseudomonas: 2 g every 8 h. The calculator shows 12-hourly.', [R(Cp, '2.1')])]),
      reg('fn', 'febrile-neutropenia', T('تب و نوتروپنی (تجربی) — بزرگسال ۲ g هر ۸ ساعت', 'Empiric therapy for febrile neutropenia — adult 2 g every 8 h'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 3}, [R(Cp, '2.1')], dur={'min': 7, 'max': 7}),
      reg('uti', 'urinary-tract-infection', T('UTI خفیف تا متوسط — بزرگسال ۰٫۵ تا ۱ g هر ۱۲ ساعت', 'Mild–moderate UTI — adult 0.5–1 g every 12 h'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 1000, 'dosesPerDay': 2}, [R(Cp, '2.1')], dur={'min': 7, 'max': 10},
          notes=[note('UTI شدید: ۲ g هر ۱۲ ساعت.', 'Severe UTI: 2 g every 12 h.', [R(Cp, '2.1')])]),
      reg('skin', 'skin-soft-tissue-infection', T('عفونت پوست متوسط تا شدید — بزرگسال ۲ g هر ۱۲ ساعت', 'Moderate–severe skin infection — adult 2 g every 12 h'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 2}, [R(Cp, '2.1')], dur={'min': 10, 'max': 10}),
      reg('iai', 'intra-abdominal-infection', T('عفونت عارضه‌دار داخل شکم — بزرگسال ۲ g هر ۱۲ ساعت + مترونیدازول', 'Complicated intra-abdominal infection — adult 2 g every 12 h + metronidazole'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 2}, [R(Cp, '2.1')], dur={'min': 7, 'max': 10}),
      reg('child', 'community-acquired-pneumonia', T('کودک ۲ ماه تا ۱۶ سال (تا ۴۰ kg) — ۵۰ mg/kg هر ۱۲ ساعت (پنومونی، UTI، پوست)', 'Child 2 months–16 y (≤40 kg) — 50 mg/kg every 12 h (pneumonia, UTI, skin)'), PED, 'weightBased', {'perKgPerDose': 50, 'intervalHours': 12}, [R(Cp, '2.2')],
          limits={'maxPerDose': 2000, 'refs': [R(Cp, '2.2')]}, notes=[CPN]),
      reg('child-fn', 'febrile-neutropenia', T('تب و نوتروپنی — کودک ۲ ماه تا ۱۶ سال: ۵۰ mg/kg هر ۸ ساعت', 'Febrile neutropenia — child 2 months–16 y: 50 mg/kg every 8 h'), PED, 'weightBased', {'perKgPerDose': 50, 'intervalHours': 8}, [R(Cp, '2.2')],
          limits={'maxPerDose': 2000, 'refs': [R(Cp, '2.2')]}, notes=[CPN])],
     [CI('hyper', 'واکنش آلرژیک فوری به سفپیم، سفالوسپورین‌ها، پنی‌سیلین‌ها یا سایر بتالاکتام‌ها.', 'Immediate hypersensitivity to cefepime, cephalosporins, penicillins or other beta-lactams.', [R(Cp, '4')])],
     warn=[W('انسفالوپاتی، میوکلونوس و تشنج غیرتشنجی به‌ویژه در نارسایی کلیه بدون تعدیل دوز؛ اسهال C. difficile.', 'Encephalopathy, myoclonus and non-convulsive status, mainly with renal impairment without dose adjustment; C. difficile diarrhoea.', [R(Cp, '5')])],
     renal=[RENAL(Cp, '2.3', 'ClCr ۶۰ و کمتر: کاهش دوز یا افزایش فاصله طبق جدول برچسب.', 'CrCl ≤60: reduce dose or extend interval per label table.', 60)],
     exs=[ex('pneu', 'vial-1g', {'perDose': 1000, 'upperPerDose': 2000}, ageYears=50, weightKg=70), ex('fn', 'vial-2g', {'perDose': 2000, 'dosesPerDay': 3}, ageYears=50, weightKg=70), ex('child', 'vial-1g', {'perDose': 1000}, ageYears=5, weightKg=20)])

Lz = fda('linezolid', 'FDA Linezolid tab', 'Linezolid tablets 600 mg — Prescribing Information', sid('linezolid'))
drug('linezolid', 'anti-infectives', 'لاینزولید', 'Linezolid', T('اکسازولیدینون', 'Oxazolidinone'), [{'name': 'Zyvox', 'market': 'US'}], ['zyvox', 'لاینزولید', 'لینزولید'],
     [tab('tab-600', 600, '600 mg tablet', [R(Lz, '3')])],
     [reg('adult', 'hospital-acquired-pneumonia', T('پنومونی بیمارستانی یا اکتسابی، عفونت عارضه‌دار پوست، VRE — ۱۲ سال به بالا ۶۰۰ mg هر ۱۲ ساعت', 'Nosocomial or community pneumonia, cSSSI, VRE — ≥12 y 600 mg every 12 h'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 600, 'dosesPerDay': 2}, [R(Lz, '2.1')], dur={'min': 10, 'max': 14},
          notes=[note('VRE: ۱۴ تا ۲۸ روز. عفونت پوستی بدون عارضه بزرگسال: ۴۰۰ mg هر ۱۲ ساعت (قرص ۴۰۰ در این برچسب نیست).', 'VRE: 14–28 days. Uncomplicated SSSI in adults: 400 mg every 12 h (no 400 mg tablet in this label).', [R(Lz, '2.1')])]),
      reg('child', 'hospital-acquired-pneumonia', T('کودک زیر ۱۲ سال — ۱۰ mg/kg هر ۸ ساعت (فرم مایع)', 'Child <12 y — 10 mg/kg every 8 h (liquid form)'), {'maxAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('برچسب: ۱۰ mg/kg هر ۸ ساعت (عفونت پوستی بدون عارضه: زیر ۵ سال هر ۸ و ۵ تا ۱۱ سال هر ۱۲ ساعت). این برچسب فقط قرص ۶۰۰ mg دارد؛ برای کودک از سوسپانسیون استفاده شود.', 'Label: 10 mg/kg every 8 h (uncomplicated SSSI: <5 y every 8 h, 5–11 y every 12 h). This label only has the 600 mg tablet; children need the oral suspension.')}, [R(Lz, '2.1')])],
     [CI('ci', 'حساسیت به لاینزولید؛ مصرف MAOI یا ظرف ۲ هفته پس از آن.', 'Hypersensitivity to linezolid; MAOIs now or within 2 weeks.', [R(Lz, '4')])],
     warn=[W('سرکوب مغز استخوان (CBC هفتگی)؛ سندرم سروتونین با داروهای سروتونرژیک؛ نوروپاتی محیطی و بینایی در مصرف بیش از ۲۸ روز؛ اسیدوز لاکتیک؛ هیپوگلیسمی.', 'Myelosuppression (weekly CBC); serotonin syndrome with serotonergic drugs; peripheral and optic neuropathy beyond 28 days; lactic acidosis; hypoglycaemia.', [R(Lz, '5')])],
     inter=[IA('ssri', 'SSRI، SNRI، تریپتان‌ها و سایر داروهای سروتونرژیک: سندرم سروتونین.', 'SSRIs, SNRIs, triptans and other serotonergic drugs: serotonin syndrome.', [R(Lz, '5')])],
     exs=[ex('adult', 'tab-600', {'perDose': 600, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70)])

Cm = fda('colistimethate', 'FDA Coly-Mycin M', 'Coly-Mycin M Parenteral (colistimethate) 150 mg — Prescribing Information', sid('colistimethate')); d = R(Cm, 'Dosage and Administration')
drug('colistimethate', 'anti-infectives', 'کولیستیمتات (کولیستین تزریقی)', 'Colistimethate (colistin)', T('پلی‌میکسین', 'Polymyxin'), [{'name': 'Coly-Mycin M', 'market': 'US'}], ['colistin', 'coly-mycin', 'کولیستین', 'کلیستین'],
     [liquid('vial-150', 75, 1, '150 mg colistin base activity vial → 75 mg/mL after adding 2 mL water', [R(Cm, 'How Supplied'), d], form_='injection', route='iv')],
     [reg('std', 'sepsis', T('عفونت گرم‌منفی حساس (بزرگسال و کودک) — ۲٫۵ تا ۵ mg/kg/روز کولیستین پایه در ۲ تا ۴ دوز', 'Susceptible Gram-negative infection (adults and children) — 2.5–5 mg/kg/day colistin base in 2–4 doses'), {}, 'weightBased',
          {'perKgPerDay': 2.5, 'perKgPerDayMax': 5, 'dividedDoses': 2}, [d], limits={'maxPerKgPerDay': 5, 'refs': [d]},
          notes=[note('بر اساس وزن ایده‌آل. حداکثر ۵ mg/kg/روز. ماشین‌حساب ۲ دوز را نشان می‌دهد؛ ۳ یا ۴ دوز هم مجاز است.', 'Based on ideal body weight. Max 5 mg/kg/day. The calculator splits into 2 doses; 3 or 4 doses are also allowed.', [d])])],
     [CI('hyper', 'حساسیت به کولیستیمتات.', 'Hypersensitivity to colistimethate.', [R(Cm, 'Contraindications')])],
     warn=[W('سمیت کلیوی و عصبی (پارستزی، فلج تنفسی با شل‌کننده‌ها و آمینوگلیکوزیدها)؛ دوز در نارسایی کلیه کاهش یابد.', 'Nephrotoxicity and neurotoxicity (paraesthesia, respiratory arrest with curariform relaxants or aminoglycosides); reduce dose in renal impairment.', [R(Cm, 'Warnings')])],
     renal=[RENAL(Cm, 'Dosage and Administration', 'ClCr ۵۰ تا ۷۹: ۲٫۵ تا ۳٫۸ mg/kg/روز در ۲ دوز؛ ۳۰ تا ۴۹: ۲٫۵ mg/kg/روز در ۱ یا ۲ دوز؛ ۱۰ تا ۲۹: ۱٫۵ mg/kg هر ۳۶ ساعت.', 'CrCl 50–79: 2.5–3.8 mg/kg/day in 2 doses; 30–49: 2.5 mg/kg/day once or in 2 doses; 10–29: 1.5 mg/kg every 36 h.', 80)],
     exs=[ex('std', 'vial-150', {'perDose': 87.5, 'mlPerDose': 1.17, 'upperPerDose': 175}, ageYears=50, weightKg=70)])

# ===================== HIV =====================
Tv = fda('tivicay', 'FDA Tivicay', 'Tivicay / Tivicay PD (dolutegravir) — Prescribing Information', sid('tivicay'))
ART_D = note('همیشه همراه سایر داروهای ضدرتروویروس.', 'Always in combination with other antiretrovirals.', [R(Tv, '2.2')])
drug('dolutegravir', 'anti-infectives', 'دولوتگراویر', 'Dolutegravir', T('مهارکننده اینتگراز (INSTI)', 'Integrase inhibitor (INSTI)'), [{'name': 'Tivicay', 'market': 'US'}], ['tivicay', 'تیویکای', 'دولوتگراویر', 'DTG'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Tv, '3')]) for m in (10, 25, 50)],
     [reg('adult', 'hiv', T('HIV-1 (بدون مقاومت به INSTI) — ۵۰ mg یک بار در روز', 'HIV-1 (INSTI-naive) — 50 mg once daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Tv, '2.2')], notes=[ART_D]),
      reg('adult-bid', 'hiv', T('HIV-1 با القاگر (افاویرنز، ریفامپین و...) یا مقاومت به INSTI — ۵۰ mg دو بار در روز', 'HIV-1 with certain inducers (efavirenz, rifampin…) or INSTI resistance — 50 mg twice daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 2}, [R(Tv, '2.2')], notes=[ART_D]),
      reg('child', 'hiv', T('کودک ۱۴ kg به بالا (قرص) — ۱۴ تا <۲۰ kg: ۴۰ mg؛ ≥۲۰ kg: ۵۰ mg یک بار در روز', 'Child ≥14 kg (tablets) — 14 to <20 kg: 40 mg; ≥20 kg: 50 mg once daily'), {'minAge': age(4, 'week'), 'maxAge': age(18, 'year'), 'minWeightKg': 14}, 'weightBand',
          {'weightBands': [{'minWeightKg': 14, 'maxWeightKg': 19.99, 'perDose': 40, 'dosesPerDay': 1}, {'minWeightKg': 20, 'maxWeightKg': None, 'perDose': 50, 'dosesPerDay': 1}]}, [R(Tv, '2.3, Table 4')],
          allowed=['tab-10', 'tab-50'], notes=[ART_D, note('۱۴ تا <۲۰ kg: قرص محلول PD ارجح است (با قرص معمولی mg به mg جایگزین نیست). زیر ۱۴ kg فقط Tivicay PD. با القاگرها دوز دو بار در روز.', '14 to <20 kg: Tivicay PD preferred (not interchangeable mg-for-mg). Under 14 kg only Tivicay PD. With inducers give twice daily.', [R(Tv, '2.3'), R(Tv, '2.1')])])],
     [CI('ci', 'حساسیت قبلی به دولوتگراویر؛ مصرف همزمان دوفتیلید.', 'Previous hypersensitivity to dolutegravir; concomitant dofetilide.', [R(Tv, '4')])],
     warn=[W('واکنش حساسیتی و آسیب کبدی؛ سندرم بازسازی ایمنی.', 'Hypersensitivity and hepatotoxicity; immune reconstitution syndrome.', [R(Tv, '5')])],
     inter=[IA('dofetilide', 'دوفتیلید: منع مصرف همزمان.', 'Dofetilide: contraindicated.', [R(Tv, '4')]),
            IA('cations', 'آنتی‌اسید، مکمل کلسیم یا آهن: دولوتگراویر ۲ ساعت قبل یا ۶ ساعت بعد (یا همراه غذا برای کلسیم/آهن).', 'Antacids, calcium or iron supplements: take dolutegravir 2 h before or 6 h after (or together with food for calcium/iron).', [R(Tv, '7')])],
     exs=[ex('adult', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('child', 'tab-10', {'perDose': 40, 'tabletsPerDoseRounded': 4}, ageYears=4, weightKg=17)])

La = fda('lamivudine', 'FDA Lamivudine', 'Lamivudine tablets 150/300 mg (Apotex) — Prescribing Information', sid('lamivudine'))
ART_L = note('همیشه همراه سایر داروهای ضدرتروویروس.', 'Always in combination with other antiretrovirals.', [R(La, '2.1')])
drug('lamivudine', 'anti-infectives', 'لامیوودین', 'Lamivudine', T('مهارکننده نوکلئوزیدی ترانس‌کریپتاز معکوس (NRTI)', 'Nucleoside reverse transcriptase inhibitor (NRTI)'), [{'name': 'Epivir', 'market': 'US'}], ['epivir', '3TC', 'لامیودین', 'لامیوودین'],
     [tab('tab-150', 150, '150 mg tablet (scored)', [R(La, '3')], scored=True), tab('tab-300', 300, '300 mg tablet', [R(La, '3')])],
     [reg('adult', 'hiv', T('HIV-1 — بزرگسال: ۱۵۰ mg دو بار یا ۳۰۰ mg یک بار در روز', 'HIV-1 — adult: 150 mg twice daily or 300 mg once daily'), A18, 'fixed', {'perDose': 150, 'dosesPerDay': 2}, [R(La, '2.1')], notes=[ART_L]),
      reg('child', 'hiv', T('کودک ۱۴ kg به بالا (قرص شیاردار ۱۵۰) — یک بار در روز: ۱۵۰ / ۲۲۵ / ۳۰۰ mg بر اساس وزن', 'Child ≥14 kg (scored 150 mg tablet) — once daily: 150 / 225 / 300 mg by weight'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year'), 'minWeightKg': 14}, 'weightBand',
          {'weightBands': [{'minWeightKg': 14, 'maxWeightKg': 19.99, 'perDose': 150, 'dosesPerDay': 1}, {'minWeightKg': 20, 'maxWeightKg': 24.99, 'perDose': 225, 'dosesPerDay': 1}, {'minWeightKg': 25, 'maxWeightKg': None, 'perDose': 300, 'dosesPerDay': 1}]},
          [R(La, '2.2, Table 1')], allowed=['tab-150'],
          notes=[ART_L, note('رژیم دو بار در روز (همان جدول): ۱۴ تا <۲۰ kg نیم قرص صبح و شب؛ ۲۰ تا <۲۵ kg نیم قرص صبح و یک قرص شب؛ ≥۲۵ kg یک قرص صبح و شب. داده یک بار در روز محدود به بیمارانی است که پس از ۳۶ هفته از دو بار در روز تغییر داده‌اند. ناتوان در بلع قرص: محلول خوراکی.',
                             'Twice-daily option (same table): 14 to <20 kg ½ tablet AM and PM; 20 to <25 kg ½ tablet AM and 1 tablet PM; ≥25 kg 1 tablet AM and PM. Once-daily data are limited to patients switched from twice daily after 36 weeks. Unable to swallow tablets: oral solution.', [R(La, '2.2')])])],
     [CI('hyper', 'حساسیت قبلی به لامیوودین.', 'Previous hypersensitivity to lamivudine.', [R(La, '4')])],
     warn=[W('هشدار جعبه‌ای: تشدید شدید هپاتیت B پس از قطع در عفونت همزمان HBV؛ Epivir-HBV برای HIV مناسب نیست (مقاومت).', 'Boxed warning: severe acute exacerbation of hepatitis B on stopping in HBV co-infection; Epivir-HBV is not for HIV (resistance).', [R(La, 'Boxed Warning')])],
     renal=[RENAL(La, '2.3', 'ClCr ۳۰ تا ۴۹: ۱۵۰ mg روزانه؛ ۱۵ تا ۲۹: ۱۵۰ سپس ۱۰۰ mg؛ ۵ تا ۱۴: ۱۵۰ سپس ۵۰ mg؛ زیر ۵: ۵۰ سپس ۲۵ mg روزانه.', 'CrCl 30–49: 150 mg daily; 15–29: 150 then 100 mg daily; 5–14: 150 then 50 mg daily; <5: 50 then 25 mg daily.')],
     exs=[ex('adult', 'tab-150', {'perDose': 150, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('child', 'tab-150', {'perDose': 225, 'tabletsPerDoseRounded': 1.5}, ageYears=7, weightKg=22)])

Zd = fda('zidovudine', 'FDA Retrovir', 'Retrovir (zidovudine) capsules, tablets and syrup — Prescribing Information', sid('zidovudine'))
ART_Z = note('همیشه همراه سایر داروهای ضدرتروویروس؛ دوز کودک از دوز بزرگسال بیشتر نشود.', 'Always with other antiretrovirals; the pediatric dose must not exceed the adult dose.', [R(Zd, '2.1'), R(Zd, '2.2')])
ZB = lambda lo, hi: {'minAge': age(4, 'week'), 'maxAge': age(18, 'year'), 'minWeightKg': lo, **({'maxWeightKg': hi} if hi else {})}
drug('zidovudine', 'anti-infectives', 'زیدوودین (AZT)', 'Zidovudine (AZT)', T('NRTI', 'NRTI'), [{'name': 'Retrovir', 'market': 'US'}], ['retrovir', 'AZT', 'زیدوودین', 'رتروویر'],
     [tab('cap-100', 100, '100 mg capsule', [R(Zd, '3')], per='capsule', form_='capsule'), liquid('syr-10', 10, 1, '10 mg/mL oral solution', [R(Zd, '3')], form_='solution')],
     [reg('adult', 'hiv', T('HIV-1 — بزرگسال: ۳۰۰ mg دو بار در روز', 'HIV-1 — adult: 300 mg twice daily'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 2}, [R(Zd, '2.1')], notes=[ART_Z]),
      reg('child-4', 'hiv', T('کودک ۴ تا <۹ kg — ۱۲ mg/kg دو بار در روز', 'Child 4 to <9 kg — 12 mg/kg twice daily'), ZB(4, 8.99), 'weightBased', {'perKgPerDay': 24, 'dividedDoses': 2}, [R(Zd, '2.2, Table 1')], allowed=['syr-10'],
          notes=[ART_Z, note('یا ۸ mg/kg سه بار در روز. جایگزین: ۴۸۰ mg/m²/روز.', 'Or 8 mg/kg three times daily. Alternative: 480 mg/m²/day.', [R(Zd, '2.2')])]),
      reg('child-9', 'hiv', T('کودک ۹ تا <۳۰ kg — ۹ mg/kg دو بار در روز', 'Child 9 to <30 kg — 9 mg/kg twice daily'), ZB(9, 29.99), 'weightBased', {'perKgPerDay': 18, 'dividedDoses': 2}, [R(Zd, '2.2, Table 1')],
          notes=[ART_Z, note('یا ۶ mg/kg سه بار در روز.', 'Or 6 mg/kg three times daily.', [R(Zd, '2.2')])]),
      reg('child-30', 'hiv', T('کودک ۳۰ kg به بالا — ۳۰۰ mg دو بار در روز', 'Child ≥30 kg — 300 mg twice daily'), ZB(30, None), 'fixed', {'perDose': 300, 'dosesPerDay': 2}, [R(Zd, '2.2, Table 1')], notes=[ART_Z]),
      reg('pmtct', 'hiv', T('پیشگیری از انتقال مادر به جنین — مادر (بارداری بالای ۱۴ هفته): ۱۰۰ mg پنج بار در روز تا شروع زایمان', 'Prevention of maternal-fetal transmission — mother (>14 weeks): 100 mg five times daily until labour'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 5}, [R(Zd, '2.3')],
          notes=[note('حین زایمان: وریدی ۲ mg/kg در ۱ ساعت، سپس ۱ mg/kg/ساعت تا بستن بند ناف.', 'During labour: IV 2 mg/kg over 1 h, then 1 mg/kg/h until the cord is clamped.', [R(Zd, '2.3')])]),
      reg('neonate', 'hiv', T('نوزاد (پیشگیری) — ۲ mg/kg خوراکی هر ۶ ساعت از ۱۲ ساعت اول تا ۶ هفتگی', 'Neonate (prophylaxis) — 2 mg/kg orally every 6 h from within 12 h of birth to 6 weeks'), {'maxAge': age(6, 'week')}, 'weightBased', {'perKgPerDose': 2, 'intervalHours': 6}, [R(Zd, '2.3, Table 2')],
          allowed=['syr-10'], dur={'min': 42, 'max': 42}, notes=[note('اگر خوراکی ممکن نیست: وریدی ۱٫۵ mg/kg در ۳۰ دقیقه هر ۶ ساعت. سرنگ با درجه ۰٫۱ mL.', 'If oral dosing is not possible: IV 1.5 mg/kg over 30 min every 6 h. Use a syringe with 0.1 mL graduations.', [R(Zd, '2.3')])])],
     [CI('hyper', 'واکنش حساسیتی تهدیدکننده حیات (آنافیلاکسی، SJS) به زیدوودین.', 'Life-threatening hypersensitivity (anaphylaxis, Stevens-Johnson) to zidovudine.', [R(Zd, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت خونی (نوتروپنی، کم‌خونی شدید)، میوپاتی، اسیدوز لاکتیک و کبد چرب.', 'Boxed warning: haematological toxicity (neutropenia, severe anaemia), myopathy, lactic acidosis and hepatomegaly with steatosis.', [R(Zd, 'Boxed Warning')])],
     exs=[ex('adult', 'cap-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=35, weightKg=70), ex('child-4', 'syr-10', {'perDose': 72, 'mlPerDose': 7.2}, ageMonths=4, weightKg=6),
          ex('child-9', 'syr-10', {'perDose': 180, 'mlPerDose': 18}, ageYears=6, weightKg=20), ex('neonate', 'syr-10', {'perDose': 6, 'mlPerDose': 0.6}, ageDays=2, weightKg=3)])

# ===================== pain =====================
OPI_CI = lambda src, sec='4', extra_fa='', extra_en='': CI('ci', 'دپرسیون تنفسی قابل‌توجه؛ آسم حاد یا شدید بدون پایش؛ انسداد گوارشی یا ایلئوس فلجی؛ حساسیت' + extra_fa + '.', 'Significant respiratory depression; acute or severe asthma without monitoring; GI obstruction or paralytic ileus; hypersensitivity' + extra_en + '.', [R(src, sec)])
OPI_W = lambda src: W('هشدار جعبه‌ای: اعتیاد و سوءمصرف، دپرسیون تنفسی کشنده، مصرف تصادفی در کودک، سندرم ترک نوزادی، تداخل با بنزودیازپین‌ها و مهارکننده‌های CYP3A4. نالوکسان در دسترس باشد.', 'Boxed warning: addiction and misuse, life-threatening respiratory depression, accidental ingestion in children, neonatal opioid withdrawal, interactions with benzodiazepines and CYP3A4 inhibitors. Keep naloxone available.', [R(src, 'Boxed Warning'), R(src, '2.2')])

Hm = fda('hydromorphone-tab', 'FDA Hydromorphone tab', 'Hydromorphone hydrochloride tablets 2/4/8 mg (SpecGx) — Prescribing Information', sid('hydromorphone'))
drug('hydromorphone', 'nervous-system', 'هیدرومورفون', 'Hydromorphone', T('آگونیست اپیوئیدی', 'Opioid agonist'), [{'name': 'Dilaudid', 'market': 'US'}], ['dilaudid', 'هیدرومورفون'],
     [tab('tab-2', 2, '2 mg tablet', [R(Hm, '3')]), tab('tab-4', 4, '4 mg tablet', [R(Hm, '3')]), tab('tab-8', 8, '8 mg tablet (scored)', [R(Hm, '3')], scored=True)],
     [reg('pain', 'severe-pain', T('درد شدید (بیمار بدون مصرف قبلی اپیوئید) — ۲ تا ۴ mg هر ۴ تا ۶ ساعت در صورت نیاز', 'Severe pain (opioid-naive) — 2–4 mg every 4–6 h as needed'), A18, 'fixed', {'perDose': 2, 'perDoseMax': 4, 'dosesPerDay': 4}, [R(Hm, '2.3')],
          notes=[note('کمترین دوز مؤثر در کوتاه‌ترین مدت. «هر ۴ تا ۶ ساعت در صورت نیاز»؛ عدد دفعات در ماشین‌حساب برای ۶ ساعت است. نارسایی کبد یا کلیه: شروع با یک‌چهارم تا نصف دوز.', 'Lowest effective dose for the shortest time. “Every 4–6 h as needed”; the calculator shows 6-hourly. Hepatic or renal impairment: start at one-quarter to one-half the dose.', [R(Hm, '2.1'), R(Hm, '2.4'), R(Hm, '2.5')])])],
     [OPI_CI(Hm)], warn=[OPI_W(Hm)],
     renal=[RENAL(Hm, '2.5', 'شروع با یک‌چهارم تا نصف دوز معمول بسته به شدت نارسایی.', 'Start at one-quarter to one-half the usual dose depending on the degree of impairment.', 60)],
     exs=[ex('pain', 'tab-2', {'perDose': 2, 'upperPerDose': 4}, ageYears=50, weightKg=70)])

Nu = fda('nucynta', 'FDA Nucynta', 'Nucynta (tapentadol) tablets — Prescribing Information', sid('nucynta'))
drug('tapentadol', 'nervous-system', 'تاپنتادول', 'Tapentadol', T('آگونیست اپیوئیدی و مهارکننده بازجذب نوراپی‌نفرین', 'Opioid agonist and norepinephrine reuptake inhibitor'), [{'name': 'Nucynta', 'market': 'US'}], ['nucynta', 'تاپنتادول'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Nu, '3')]) for m in (50, 75, 100)],
     [reg('pain', 'severe-pain', T('درد حاد شدید — ۵۰ تا ۱۰۰ mg هر ۴ تا ۶ ساعت در صورت نیاز (بزرگسال و ۶ سال به بالا با وزن ≥۴۰ kg)', 'Severe acute pain — 50–100 mg every 4–6 h as needed (adults and ≥6 y weighing ≥40 kg)'), {'minAge': age(6, 'year'), 'minWeightKg': 40}, 'fixed',
          {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 4}, [R(Nu, '2.3')], limits={'maxPerDay': 600, 'refs': [R(Nu, '2.3')]},
          notes=[note('روز اول: دوز دوم می‌تواند ۱ ساعت پس از اول باشد. بیش از ۷۰۰ mg در روز اول و ۶۰۰ mg در روزهای بعد بررسی نشده است. عدد دفعات در ماشین‌حساب برای ۶ ساعت است.', 'Day 1: the second dose may be given 1 h after the first. Over 700 mg on day 1 and 600 mg thereafter not studied. The calculator shows 6-hourly.', [R(Nu, '2.3')]),
                 note('نارسایی کبدی متوسط: ۵۰ mg حداکثر هر ۸ ساعت؛ شدید: توصیه نمی‌شود.', 'Moderate hepatic impairment: 50 mg no more often than every 8 h; severe: not recommended.', [R(Nu, '2.5')])])],
     [OPI_CI(Nu, '4', '؛ MAOI همزمان یا ظرف ۱۴ روز', '; MAOIs now or within 14 days')], warn=[OPI_W(Nu), W('سندرم سروتونین با داروهای سروتونرژیک؛ تشنج.', 'Serotonin syndrome with serotonergic drugs; seizures.', [R(Nu, '5')])],
     exs=[ex('pain', 'tab-50', {'perDose': 50, 'upperPerDose': 100}, ageYears=40, weightKg=70)])

Fe = fda('fentanyl-inj', 'FDA Fentanyl inj.', 'Fentanyl citrate injection 50 mcg/mL — Prescribing Information', sid('fentanyl'))
drug('fentanyl-injection', 'nervous-system', 'فنتانیل تزریقی', 'Fentanyl (injection)', T('آگونیست اپیوئیدی (بیهوشی)', 'Opioid agonist (anaesthesia)'), [{'name': 'Sublimaze', 'market': 'US'}], ['sublimaze', 'فنتانیل', 'fentanyl citrate'],
     [liquid('amp-50', 50, 1, '50 mcg/mL ampule or vial', [R(Fe, '3')], form_='injection', route='iv', unit='mcg')],
     [reg('premed', 'general-anesthesia', T('پیش‌دارو بزرگسال — ۵۰ تا ۱۰۰ mcg عضلانی ۳۰ تا ۶۰ دقیقه پیش از جراحی', 'Adult premedication — 50–100 mcg IM 30–60 min before surgery'), A18, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 1}, [R(Fe, '2.2')], unit='mcg', dur=ONE,
          notes=[note('فقط توسط افراد آموزش‌دیده با تجهیزات احیا، اکسیژن و آنتاگونیست اپیوئید در دسترس.', 'Only by trained staff with resuscitation equipment, oxygen and an opioid antagonist available.', [R(Fe, '2.1')])]),
      reg('adjunct', 'general-anesthesia', T('کمکی بیهوشی عمومی — کم ۲، متوسط ۲ تا ۲۰، زیاد ۲۰ تا ۵۰ mcg/kg', 'Adjunct to general anaesthesia — low 2, moderate 2–20, high 20–50 mcg/kg'), A18, 'notCalculated',
          {'reason': T('جدول برچسب (کل دوز): کم ۲ mcg/kg برای جراحی کوچک؛ متوسط ۲ تا ۲۰ mcg/kg برای جراحی بزرگ؛ زیاد ۲۰ تا ۵۰ mcg/kg برای جراحی قلب باز و اعصاب (تهویه مکانیکی لازم). به‌عنوان بیهوش‌کننده تنها: ۵۰ تا ۱۰۰ و گاه تا ۱۵۰ mcg/kg.', 'Label table (total dose): low 2 mcg/kg for minor surgery; moderate 2–20 mcg/kg for major surgery; high 20–50 mcg/kg for open-heart or neuro surgery (ventilation required). As sole anaesthetic: 50–100, sometimes up to 150 mcg/kg.')},
          [R(Fe, '2.2, Table 1')]),
      reg('child', 'general-anesthesia', T('کودک ۲ تا ۱۲ سال — القا و نگهداری ۲ تا ۳ mcg/kg', 'Children 2–12 y — induction and maintenance 2–3 mcg/kg'), {'minAge': age(2, 'year'), 'maxAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('برچسب: دوز کاهش‌یافته ۲ تا ۳ mcg/kg برای القا و نگهداری. زیر ۲ سال ایمنی تعیین نشده است.', 'Label: reduced dose of 2–3 mcg/kg for induction and maintenance. Safety under 2 y not established.')}, [R(Fe, '2.2'), R(Fe, '8.4')])],
     [CI('hyper', 'حساسیت به فنتانیل (مثلاً آنافیلاکسی).', 'Hypersensitivity to fentanyl (e.g. anaphylaxis).', [R(Fe, '4')])],
     warn=[W('هشدار جعبه‌ای: دپرسیون تنفسی کشنده، اعتیاد، تداخل با بنزودیازپین‌ها و مهارکننده‌های CYP3A4. سفتی عضلات قفسه سینه با دوز بالا یا تزریق سریع.', 'Boxed warning: life-threatening respiratory depression, addiction, interactions with benzodiazepines and CYP3A4 inhibitors. Chest-wall rigidity with high doses or rapid injection.', [R(Fe, 'Boxed Warning'), R(Fe, '5')])],
     exs=[ex('premed', 'amp-50', {'perDose': 50, 'mlPerDose': 1, 'upperPerDose': 100, 'upperMlPerDose': 2}, ageYears=40, weightKg=70)])

Or = fda('orphenadrine', 'FDA Orphenadrine ER', 'Orphenadrine citrate extended-release tablets 100 mg (Lupin) — Prescribing Information', sid('orphenadrine'))
drug('orphenadrine', 'musculoskeletal', 'اورفنادرین', 'Orphenadrine', T('شل‌کننده عضلانی با اثر مرکزی', 'Centrally acting muscle relaxant'), [{'name': 'Norflex', 'market': 'US'}], ['norflex', 'اورفنادرین', 'ارفنادرین'],
     [tab('er-100', 100, '100 mg extended-release tablet', [R(Or, 'How Supplied')])],
     [reg('spasm', 'muscle-spasm', T('درد عضلانی-اسکلتی حاد (کمکی) — یک قرص صبح و یک قرص عصر', 'Acute painful musculoskeletal conditions (adjunct) — one tablet morning and evening'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [R(Or, 'Dosage and Administration'), R(Or, 'Indications and Usage')])],
     [CI('ci', 'گلوکوم؛ انسداد پیلور یا دوازدهه؛ زخم پپتیک تنگ‌کننده؛ هیپرتروفی پروستات یا انسداد گردن مثانه؛ آشالازی؛ میاستنی گراویس؛ حساسیت.', 'Glaucoma; pyloric or duodenal obstruction; stenosing peptic ulcer; prostatic hypertrophy or bladder-neck obstruction; cardiospasm (megaoesophagus); myasthenia gravis; hypersensitivity.', [R(Or, 'Contraindications')])],
     exs=[ex('spasm', 'er-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Ax = uk('emc-arcoxia', 'eMC Arcoxia', 'Arcoxia (etoricoxib) 30/60/90/120 mg film-coated tablets — SmPC', 'Organon Pharma (UK)', '19 March 2025', 10616)
drug('etoricoxib', 'musculoskeletal', 'اتوریکوکسیب', 'Etoricoxib', T('مهارکننده انتخابی COX-2', 'Selective COX-2 inhibitor'), [{'name': 'Arcoxia', 'market': 'UK'}], ['arcoxia', 'آرکوکسیا', 'اتوریکوکسیب'],
     [tab(f'tab-{m}', m, f'{m} mg film-coated tablet', [R(Ax, '6.5')], markets=('UK',)) for m in (30, 60, 90, 120)],
     [reg('oa', 'osteoarthritis', T('استئوآرتریت — ۳۰ mg یک بار در روز (حداکثر ۶۰ mg)', 'Osteoarthritis — 30 mg once daily (max 60 mg)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 30, 'perDoseMax': 60, 'dosesPerDay': 1}, [R(Ax, '4.2')], limits={'maxPerDay': 60, 'refs': [R(Ax, '4.2')]}),
      reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — ۶۰ mg یک بار در روز (حداکثر ۹۰ mg)', 'Rheumatoid arthritis — 60 mg once daily (max 90 mg)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 60, 'perDoseMax': 90, 'dosesPerDay': 1}, [R(Ax, '4.2')], limits={'maxPerDay': 90, 'refs': [R(Ax, '4.2')]}),
      reg('as', 'ankylosing-spondylitis', T('اسپوندیلیت آنکیلوزان — ۶۰ mg یک بار در روز (حداکثر ۹۰ mg)', 'Ankylosing spondylitis — 60 mg once daily (max 90 mg)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 60, 'perDoseMax': 90, 'dosesPerDay': 1}, [R(Ax, '4.2')], limits={'maxPerDay': 90, 'refs': [R(Ax, '4.2')]}),
      reg('gout', 'gout', T('نقرس حاد — ۱۲۰ mg یک بار در روز، حداکثر ۸ روز', 'Acute gout — 120 mg once daily, max 8 days'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 120, 'dosesPerDay': 1}, [R(Ax, '4.2')], dur={'min': 1, 'max': 8}),
      reg('dental', 'toothache', T('درد پس از جراحی دندان — ۹۰ mg یک بار در روز، حداکثر ۳ روز', 'Pain after dental surgery — 90 mg once daily, max 3 days'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 90, 'dosesPerDay': 1}, [R(Ax, '4.2')], dur={'min': 1, 'max': 3})],
     [CI('ci', 'زخم پپتیک یا خونریزی گوارشی فعال؛ آسم، کهیر یا رینیت با آسپرین یا NSAID؛ بارداری و شیردهی؛ نارسایی شدید کبد؛ ClCr زیر ۳۰؛ زیر ۱۶ سال؛ IBD؛ نارسایی قلب NYHA II–IV؛ فشار خون کنترل‌نشده بالای ۱۴۰/۹۰؛ بیماری ایسکمیک قلب، شریان محیطی یا مغزی؛ حساسیت.',
         'Active peptic ulcer or GI bleeding; bronchospasm, rhinitis, polyps, angioedema or urticaria with aspirin/NSAIDs; pregnancy and lactation; severe hepatic dysfunction; CrCl <30; under 16 y; inflammatory bowel disease; NYHA II–IV heart failure; uncontrolled BP >140/90; established ischaemic heart, peripheral arterial or cerebrovascular disease; hypersensitivity.', [R(Ax, '4.3')])],
     warn=[W('خطر قلبی‌عروقی با دوز و مدت بیشتر می‌شود؛ کمترین دوز در کوتاه‌ترین مدت. عوارض گوارشی جدی.', 'Cardiovascular risk rises with dose and duration; lowest dose for the shortest time. Serious GI complications.', [R(Ax, '4.2'), R(Ax, '4.4')])],
     renal=[RENAL(Ax, '4.3', 'ClCr زیر ۳۰: منع مصرف.', 'CrCl <30: contraindicated.', 30)],
     exs=[ex('oa', 'tab-30', {'perDose': 30, 'tabletsPerDoseRounded': 1, 'upperPerDose': 60}, ageYears=60, weightKg=75), ex('gout', 'tab-120', {'perDose': 120, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=85)])

Cd = uk('emc-circadin', 'eMC Circadin', 'Circadin (melatonin) 2 mg prolonged-release tablets — SmPC', 'Flynn Pharma', '1 January 2021', 2809)
drug('melatonin', 'nervous-system', 'ملاتونین', 'Melatonin', T('آگونیست گیرنده ملاتونین', 'Melatonin receptor agonist'), [{'name': 'Circadin', 'market': 'UK'}], ['circadin', 'سیرکادین', 'ملاتونین'],
     [tab('pr-2', 2, '2 mg prolonged-release tablet (swallow whole)', [R(Cd, '6.5')], markets=('UK',))],
     [reg('insomnia', 'insomnia', T('بی‌خوابی اولیه (۵۵ سال به بالا) — ۲ mg یک بار، ۱ تا ۲ ساعت پیش از خواب پس از غذا', 'Primary insomnia (≥55 y) — 2 mg once, 1–2 h before bedtime after food'), {'minAge': age(55, 'year')}, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Cd, '4.2'), R(Cd, '4.1')],
          dur={'min': 1, 'max': 91}, notes=[note('تا ۱۳ هفته. قرص کامل بلعیده شود. در نارسایی کبد توصیه نمی‌شود؛ بیماری خودایمنی: توصیه نمی‌شود.', 'Up to 13 weeks. Swallow whole. Not recommended with hepatic impairment or autoimmune disease.', [R(Cd, '4.2'), R(Cd, '4.4')])])],
     [CI('hyper', 'حساسیت به ملاتونین یا اجزای فرآورده.', 'Hypersensitivity to melatonin or excipients.', [R(Cd, '4.3')])],
     warn=[W('خواب‌آلودگی؛ در رانندگی احتیاط.', 'Drowsiness; caution when driving.', [R(Cd, '4.4')])],
     exs=[ex('insomnia', 'pr-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

# ===================== psychiatry / neurology =====================
SUI = lambda src: W('هشدار جعبه‌ای: افزایش افکار و رفتار خودکشی در کودکان، نوجوانان و جوانان.', 'Boxed warning: increased suicidal thoughts and behaviour in children, adolescents and young adults.', [R(src, 'Boxed Warning')])
DEM = lambda src: W('هشدار جعبه‌ای: افزایش مرگ در سالمندان با سایکوز ناشی از دمانس.', 'Boxed warning: increased mortality in elderly patients with dementia-related psychosis.', [R(src, 'Boxed Warning')])

Dv = fda('desvenlafaxine', 'FDA Desvenlafaxine', 'Desvenlafaxine extended-release tablets — Prescribing Information', sid('desvenlafaxine'))
drug('desvenlafaxine', 'nervous-system', 'دسونلافاکسین', 'Desvenlafaxine', T('SNRI', 'SNRI'), [{'name': 'Pristiq', 'market': 'US'}], ['pristiq', 'پریستیک', 'دسونلافاکسین'],
     [tab(f'er-{m}', m, f'{m} mg extended-release tablet (swallow whole)', [R(Dv, '3')]) for m in (25, 50, 100)],
     [reg('mdd', 'mdd', T('افسردگی اساسی — ۵۰ mg یک بار در روز', 'Major depressive disorder — 50 mg once daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Dv, '2.1')],
          notes=[note('۵۰ mg هم دوز شروع و هم درمانی است؛ دوز بالاتر سود بیشتری نشان نداده. قطع تدریجی (۲۵ mg برای کاهش تدریجی).', '50 mg is both the starting and therapeutic dose; higher doses showed no extra benefit. Taper on stopping (25 mg is for tapering).', [R(Dv, '2.1'), R(Dv, '2.5')])])],
     [CI('ci', 'حساسیت به دسونلافاکسین یا ونلافاکسین؛ MAOI همزمان یا ظرف ۷ روز پس از قطع (یا ۱۴ روز پس از قطع MAOI)؛ شروع در بیمار تحت لاینزولید یا متیلن بلو وریدی.', 'Hypersensitivity to desvenlafaxine or venlafaxine; MAOIs concurrently or within 7 days of stopping (or 14 days after stopping an MAOI); starting in a patient on linezolid or IV methylene blue.', [R(Dv, '4')])],
     warn=[SUI(Dv), W('سندرم سروتونین؛ افزایش فشار خون (پایش)؛ خونریزی با NSAID/آسپرین/ضدانعقاد.', 'Serotonin syndrome; raised blood pressure (monitor); bleeding with NSAIDs/aspirin/anticoagulants.', [R(Dv, '5')])],
     renal=[RENAL(Dv, '2.2', 'ClCr ۳۰ تا ۵۰: حداکثر ۵۰ mg/روز؛ ClCr زیر ۳۰ یا ESRD: ۲۵ mg روزانه یا ۵۰ mg یک روز در میان.', 'CrCl 30–50: max 50 mg/day; CrCl <30 or ESRD: 25 mg daily or 50 mg every other day.')],
     exs=[ex('mdd', 'er-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Iv = fda('invega', 'FDA Invega', 'Invega (paliperidone) extended-release tablets — Prescribing Information', sid('invega'))
drug('paliperidone', 'nervous-system', 'پالیپریدون', 'Paliperidone', T('آنتی‌سایکوتیک آتیپیک', 'Atypical antipsychotic'), [{'name': 'Invega', 'market': 'US'}], ['invega', 'اینوگا', 'پالیپریدون'],
     [tab(f'er-{m}', m, f'{m} mg extended-release tablet (swallow whole)', [R(Iv, '3')]) for m in (3, 6, 9)],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی — بزرگسال ۶ mg یک بار در روز (۳ تا ۱۲ mg)', 'Schizophrenia — adult 6 mg once daily (3–12 mg)'), A18, 'fixed', {'perDose': 6, 'dosesPerDay': 1}, [R(Iv, '2.1')], limits={'maxPerDay': 12, 'refs': [R(Iv, '2.1')]},
          notes=[note('افزایش بالای ۶ mg فقط پس از ارزیابی، با فاصله بیش از ۵ روز و پله‌های ۳ mg.', 'Increase above 6 mg only after reassessment, at >5-day intervals, in 3 mg steps.', [R(Iv, '2.1')])]),
      reg('scz-teen', 'schizophrenia', T('اسکیزوفرنی نوجوان ۱۲ تا ۱۷ سال — ۳ mg یک بار در روز (حداکثر ۶ mg زیر ۵۱ kg، ۱۲ mg از ۵۱ kg)', 'Schizophrenia, adolescents 12–17 y — 3 mg once daily (max 6 mg <51 kg, 12 mg ≥51 kg)'), {'minAge': age(12, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 3, 'dosesPerDay': 1}, [R(Iv, '2.1')],
          notes=[note('افزایش با پله ۳ mg و فاصله بیش از ۵ روز.', 'Increase in 3 mg steps at intervals of more than 5 days.', [R(Iv, '2.1')])]),
      reg('sza', 'schizoaffective-disorder', T('اسکیزوافکتیو — بزرگسال ۶ mg یک بار در روز (۳ تا ۱۲ mg)', 'Schizoaffective disorder — adult 6 mg once daily (3–12 mg)'), A18, 'fixed', {'perDose': 6, 'dosesPerDay': 1}, [R(Iv, '2.2')], limits={'maxPerDay': 12, 'refs': [R(Iv, '2.2')]})],
     [CI('hyper', 'حساسیت به پالیپریدون، ریسپریدون یا اجزای فرآورده.', 'Hypersensitivity to paliperidone, risperidone or excipients.', [R(Iv, '4')])],
     warn=[DEM(Iv), W('سندرم نورولپتیک بدخیم؛ طولانی شدن QT؛ دیسکینزی دیررس؛ تغییرات متابولیک؛ هیپرپرولاکتینمی.', 'Neuroleptic malignant syndrome; QT prolongation; tardive dyskinesia; metabolic changes; hyperprolactinaemia.', [R(Iv, '5')])],
     inter=[IA('risperidone', 'ریسپریدون: پالیپریدون متابولیت آن است؛ مواجهه جمعی در نظر گرفته شود.', 'Risperidone: paliperidone is its metabolite; consider additive exposure.', [R(Iv, '2.4')])],
     exs=[ex('scz', 'er-6', {'perDose': 6, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=75), ex('scz-teen', 'er-3', {'perDose': 3, 'tabletsPerDoseRounded': 1}, ageYears=15, weightKg=55)])

Lu = fda('latuda', 'FDA Latuda', 'Latuda (lurasidone) tablets — Prescribing Information', sid('latuda'))
FOOD = note('همراه غذا (دست‌کم ۳۵۰ کالری).', 'With food (at least 350 calories).', [R(Lu, '2.3')])
drug('lurasidone', 'nervous-system', 'لوراسیدون', 'Lurasidone', T('آنتی‌سایکوتیک آتیپیک', 'Atypical antipsychotic'), [{'name': 'Latuda', 'market': 'US'}], ['latuda', 'لاتودا', 'لوراسیدون'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Lu, '3')]) for m in (20, 40, 60, 80, 120)],
     [reg('scz', 'schizophrenia', T('اسکیزوفرنی — بزرگسال ۴۰ mg یک بار در روز (۴۰ تا ۱۶۰ mg)', 'Schizophrenia — adult 40 mg once daily (40–160 mg)'), A18, 'fixed', {'perDose': 40, 'dosesPerDay': 1}, [R(Lu, '2.1')], limits={'maxPerDay': 160, 'refs': [R(Lu, '2.1')]}, notes=[FOOD]),
      reg('scz-teen', 'schizophrenia', T('اسکیزوفرنی نوجوان ۱۳ تا ۱۷ سال — ۴۰ mg یک بار در روز (حداکثر ۸۰ mg)', 'Schizophrenia, adolescents 13–17 y — 40 mg once daily (max 80 mg)'), {'minAge': age(13, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 40, 'dosesPerDay': 1}, [R(Lu, '2.1')], limits={'maxPerDay': 80, 'refs': [R(Lu, '2.1')]}, notes=[FOOD]),
      reg('bpd', 'bipolar-depression', T('افسردگی دوقطبی I — بزرگسال ۲۰ mg یک بار در روز (۲۰ تا ۱۲۰ mg)', 'Bipolar I depression — adult 20 mg once daily (20–120 mg)'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Lu, '2.2')], limits={'maxPerDay': 120, 'refs': [R(Lu, '2.2')]},
          notes=[FOOD, note('تک‌دارویی یا همراه لیتیوم یا والپروات.', 'Monotherapy or adjunct to lithium or valproate.', [R(Lu, '2.2')])]),
      reg('bpd-child', 'bipolar-depression', T('افسردگی دوقطبی I کودک ۱۰ تا ۱۷ سال — ۲۰ mg یک بار در روز (حداکثر ۸۰ mg)', 'Bipolar I depression, 10–17 y — 20 mg once daily (max 80 mg)'), {'minAge': age(10, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Lu, '2.2')],
          limits={'maxPerDay': 80, 'refs': [R(Lu, '2.2')]}, notes=[FOOD, note('افزایش پس از یک هفته بر اساس پاسخ.', 'May increase after one week based on response.', [R(Lu, '2.2')])])],
     [CI('ci', 'حساسیت به لوراسیدون؛ مهارکننده‌های قوی CYP3A4 (کتوکونازول، کلاریترومایسین، ریتوناویر...)؛ القاگرهای قوی CYP3A4 (ریفامپین، فنی‌توئین، کاربامازپین، گل راعی...).',
         'Hypersensitivity to lurasidone; strong CYP3A4 inhibitors (ketoconazole, clarithromycin, ritonavir…); strong CYP3A4 inducers (rifampin, phenytoin, carbamazepine, St John’s wort…).', [R(Lu, '4')])],
     warn=[DEM(Lu), SUI(Lu), W('سندرم نورولپتیک بدخیم؛ دیسکینزی دیررس؛ تغییرات متابولیک.', 'Neuroleptic malignant syndrome; tardive dyskinesia; metabolic changes.', [R(Lu, '5')])],
     inter=[IA('cyp3a4-mod', 'مهارکننده متوسط CYP3A4 (مثلاً دیلتیازم): نصف دوز؛ شروع ۲۰ mg، حداکثر ۸۰ mg.', 'Moderate CYP3A4 inhibitor (e.g. diltiazem): halve the dose; start 20 mg, max 80 mg.', [R(Lu, '2')])],
     renal=[RENAL(Lu, '2.4', 'ClCr زیر ۵۰: شروع ۲۰ mg، حداکثر ۸۰ mg/روز.', 'CrCl <50: start 20 mg, max 80 mg/day.')],
     exs=[ex('scz', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=75), ex('bpd', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Zn = fda('zonegran', 'FDA Zonegran', 'Zonegran (zonisamide) capsules 25/100 mg — Prescribing Information', sid('zonisamide')); d = R(Zn, 'Dosage and Administration')
drug('zonisamide', 'nervous-system', 'زونیسامید', 'Zonisamide', T('ضدصرع (سولفونامید)', 'Antiepileptic (sulfonamide)'), [{'name': 'Zonegran', 'market': 'US'}], ['zonegran', 'زونیسامید'],
     [tab('cap-25', 25, '25 mg capsule', [R(Zn, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-100', 100, '100 mg capsule', [R(Zn, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('adj', 'epilepsy', T('صرع پارشیل (کمکی، بالای ۱۶ سال) — ۱۰۰ mg روزانه، هر ۲ هفته ۱۰۰ mg بیشتر تا ۴۰۰ mg', 'Partial seizures (adjunct, >16 y) — 100 mg daily, +100 mg every 2 weeks up to 400 mg'), {'minAge': age(16, 'year')}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 100, 'increment': 100, 'incrementEveryDays': 14, 'targetMin': 100, 'targetMax': 400, 'max': 600}}, [d],
          notes=[note('یک یا دو بار در روز. ۱۰۰ تا ۶۰۰ mg/روز مؤثر بوده ولی بالای ۴۰۰ پاسخ بیشتری دیده نشده؛ تجربه بالای ۶۰۰ کم است. کپسول کامل بلعیده شود.', 'Once or twice daily. 100–600 mg/day effective but no added response above 400; little experience above 600. Swallow capsules whole.', [d])])],
     [CI('ci', 'حساسیت به سولفونامیدها یا زونیسامید.', 'Hypersensitivity to sulfonamides or zonisamide.', [R(Zn, 'Contraindications')])],
     warn=[W('واکنش‌های کشنده سولفونامیدی (SJS/TEN، نکروز کبد، آنمی آپلاستیک)؛ کاهش تعریق و هیپرترمی در کودکان؛ اسیدوز متابولیک؛ سنگ کلیه؛ افکار خودکشی.', 'Potentially fatal sulfonamide reactions (SJS/TEN, hepatic necrosis, aplastic anaemia); oligohidrosis and hyperthermia in children; metabolic acidosis; kidney stones; suicidal ideation.', [R(Zn, 'Warnings')])],
     exs=[ex('adj', 'cap-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Bv = fda('briviact', 'FDA Briviact', 'Briviact (brivaracetam) tablets, oral solution and injection — Prescribing Information', sid('briviact'))
BV = lambda lo, hi: {'minAge': age(1, 'month'), 'maxAge': age(16, 'year'), **({'minWeightKg': lo} if lo else {}), **({'maxWeightKg': hi} if hi else {})}
drug('brivaracetam', 'nervous-system', 'بریواستام', 'Brivaracetam', T('ضدصرع (لیگاند SV2A)', 'Antiepileptic (SV2A ligand)'), [{'name': 'Briviact', 'market': 'US'}], ['briviact', 'بریویاکت', 'بریواستام'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Bv, '3')]) for m in (10, 25, 50, 75, 100)] + [liquid('sol-10', 10, 1, '10 mg/mL oral solution', [R(Bv, '3')], form_='solution')],
     [reg('adult', 'epilepsy', T('تشنج پارشیل — ۱۶ سال به بالا: ۵۰ mg دو بار در روز (۲۵ تا ۱۰۰ mg دو بار)', 'Partial-onset seizures — ≥16 y: 50 mg twice daily (25–100 mg twice daily)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 50, 'perDoseMax': 100, 'dosesPerDay': 2}, [R(Bv, '2.1, Table 1')],
          notes=[note('تیتراسیون تدریجی لازم نیست؛ قطع تدریجی. با ریفامپین تا دو برابر.', 'No titration needed; withdraw gradually. Up to double the dose with rifampin.', [R(Bv, '2.1'), R(Bv, '2.4'), R(Bv, '2.6')])]),
      reg('child-50', 'epilepsy', T('کودک ۵۰ kg به بالا — شروع ۲۵ تا ۵۰ mg دو بار در روز (تا ۱۰۰ mg دو بار)', 'Child ≥50 kg — start 25–50 mg twice daily (up to 100 mg twice daily)'), BV(50, None), 'fixed', {'perDose': 25, 'perDoseMax': 50, 'dosesPerDay': 2}, [R(Bv, '2.1, Table 1')]),
      reg('child-20', 'epilepsy', T('کودک ۲۰ تا <۵۰ kg — شروع ۰٫۵ تا ۱ mg/kg دو بار در روز (تا ۲ mg/kg دو بار)', 'Child 20 to <50 kg — start 0.5–1 mg/kg twice daily (up to 2 mg/kg twice daily)'), BV(20, 49.99), 'weightBased', {'perKgPerDose': 0.5, 'perKgPerDoseMax': 1, 'intervalHours': 12}, [R(Bv, '2.1, Table 1')],
          allowed=['sol-10'], limits={'maxPerKgPerDose': 2, 'refs': [R(Bv, '2.1, Table 1')]}),
      reg('child-11', 'epilepsy', T('کودک ۱۱ تا <۲۰ kg — شروع ۰٫۵ تا ۱٫۲۵ mg/kg دو بار در روز (تا ۲٫۵ mg/kg دو بار)', 'Child 11 to <20 kg — start 0.5–1.25 mg/kg twice daily (up to 2.5 mg/kg twice daily)'), BV(11, 19.99), 'weightBased', {'perKgPerDose': 0.5, 'perKgPerDoseMax': 1.25, 'intervalHours': 12}, [R(Bv, '2.1, Table 1')],
          allowed=['sol-10'], limits={'maxPerKgPerDose': 2.5, 'refs': [R(Bv, '2.1, Table 1')]}),
      reg('child-lt11', 'epilepsy', T('کودک زیر ۱۱ kg (۱ ماه به بالا) — شروع ۰٫۷۵ تا ۱٫۵ mg/kg دو بار در روز (تا ۳ mg/kg دو بار)', 'Child <11 kg (≥1 month) — start 0.75–1.5 mg/kg twice daily (up to 3 mg/kg twice daily)'), BV(None, 10.99), 'weightBased', {'perKgPerDose': 0.75, 'perKgPerDoseMax': 1.5, 'intervalHours': 12}, [R(Bv, '2.1, Table 1')],
          allowed=['sol-10'], limits={'maxPerKgPerDose': 3, 'refs': [R(Bv, '2.1, Table 1')]})],
     [CI('hyper', 'حساسیت به بریواستام یا اجزای فرآورده (برونکواسپاسم و آنژیوادم گزارش شده).', 'Hypersensitivity to brivaracetam or excipients (bronchospasm and angioedema reported).', [R(Bv, '4')])],
     warn=[W('افکار خودکشی؛ خواب‌آلودگی و خستگی؛ واکنش‌های روانی (تحریک‌پذیری، افسردگی، سایکوز).', 'Suicidal ideation; somnolence and fatigue; psychiatric reactions (irritability, depression, psychosis).', [R(Bv, '5')])],
     exs=[ex('adult', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'upperPerDose': 100}, ageYears=30, weightKg=70), ex('child-20', 'sol-10', {'perDose': 15, 'mlPerDose': 1.5, 'upperPerDose': 30}, ageYears=9, weightKg=30),
          ex('child-lt11', 'sol-10', {'perDose': 6, 'mlPerDose': 0.6}, ageMonths=8, weightKg=8)])

# ===================== respiratory / urology =====================
Dl = fda('daliresp', 'FDA Daliresp', 'Daliresp (roflumilast) tablets — Prescribing Information', sid('daliresp'))
drug('roflumilast', 'respiratory', 'روفلومیلاست', 'Roflumilast', T('مهارکننده PDE4', 'PDE4 inhibitor'), [{'name': 'Daliresp', 'market': 'US'}], ['daliresp', 'دالیرسپ', 'روفلومیلاست'],
     [form('tab-250', 'tablet', 'oral', '250 mcg tablet (starter)', 250, 'mcg', [R(Dl, '3')], per='tablet'), form('tab-500', 'tablet', 'oral', '500 mcg tablet', 500, 'mcg', [R(Dl, '3')], per='tablet')],
     [reg('copd', 'copd', T('COPD شدید با برونشیت مزمن و سابقه تشدید — ۵۰۰ mcg یک بار در روز', 'Severe COPD with chronic bronchitis and exacerbations — 500 mcg once daily'), A18, 'fixed', {'perDose': 500, 'dosesPerDay': 1}, [R(Dl, '2')], unit='mcg',
          notes=[note('اختیاری: ۲۵۰ mcg روزانه ۴ هفته برای کاهش قطع درمان، سپس ۵۰۰ mcg (۲۵۰ دوز درمانی نیست). برای برونکواسپاسم حاد نه.', 'Optional: 250 mcg daily for 4 weeks to improve tolerability, then 500 mcg (250 is not a therapeutic dose). Not for acute bronchospasm.', [R(Dl, '2'), R(Dl, '5')])])],
     [CI('liver', 'نارسایی متوسط تا شدید کبد (Child-Pugh B یا C).', 'Moderate to severe liver impairment (Child-Pugh B or C).', [R(Dl, '4')])],
     warn=[W('رویدادهای روانی از جمله افکار خودکشی؛ کاهش وزن.', 'Psychiatric events including suicidality; weight loss.', [R(Dl, '5')])],
     exs=[ex('copd', 'tab-500', {'perDose': 500, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=70)])

Av = fda('avodart', 'FDA Avodart', 'Avodart (dutasteride) 0.5 mg capsules — Prescribing Information', sid('avodart'))
drug('dutasteride', 'genitourinary-sex-hormones', 'دوتاستراید', 'Dutasteride', T('مهارکننده ۵-آلفا ردوکتاز', '5-alpha-reductase inhibitor'), [{'name': 'Avodart', 'market': 'US'}], ['avodart', 'آوودارت', 'دوتاستراید'],
     [tab('cap-05', 0.5, '0.5 mg soft capsule (swallow whole)', [R(Av, '3')], per='capsule', form_='capsule')],
     [reg('bph', 'bph', T('BPH علامت‌دار — ۰٫۵ mg یک بار در روز (تنها یا همراه تامسولوسین ۰٫۴ mg)', 'Symptomatic BPH — 0.5 mg once daily (alone or with tamsulosin 0.4 mg)'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Av, '2.1'), R(Av, '2.2')],
          notes=[note('کپسول باز یا جویده نشود (تحریک دهان و حلق). زنان باردار یا احتمال بارداری کپسول را لمس نکنند (جذب پوستی).', 'Do not open or chew (oropharyngeal irritation). Pregnant women or those who may become pregnant must not handle capsules (skin absorption).', [R(Av, '2'), R(Av, '16')])])],
     [CI('ci', 'بارداری؛ حساسیت قابل‌توجه به دوتاستراید یا سایر مهارکننده‌های ۵-آلفا ردوکتاز.', 'Pregnancy; clinically significant hypersensitivity to dutasteride or other 5-alpha-reductase inhibitors.', [R(Av, '4')])],
     warn=[W('PSA را حدود ۵۰٪ کاهش می‌دهد؛ افزایش تأییدشده PSA بررسی شود. احتمال افزایش سرطان پروستات درجه بالا. ۶ ماه پس از قطع خون اهدا نشود.', 'Lowers PSA by about 50%; evaluate any confirmed PSA rise. May increase high-grade prostate cancer. Do not donate blood until 6 months after the last dose.', [R(Av, '5')])],
     exs=[ex('bph', 'cap-05', {'perDose': 0.5, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

My = fda('myrbetriq', 'FDA Myrbetriq', 'Myrbetriq (mirabegron) extended-release tablets and granules — Prescribing Information', sid('myrbetriq'))
drug('mirabegron', 'genitourinary-sex-hormones', 'میرابگرون', 'Mirabegron', T('آگونیست بتا-۳ آدرنرژیک', 'Beta-3 adrenergic agonist'), [{'name': 'Myrbetriq', 'market': 'US'}], ['myrbetriq', 'betmiga', 'میرابگرون'],
     [tab('er-25', 25, '25 mg extended-release tablet (swallow whole)', [R(My, '3')]), tab('er-50', 50, '50 mg extended-release tablet (swallow whole)', [R(My, '3')])],
     [reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال — بزرگسال: ۲۵ mg یک بار در روز، پس از ۴ تا ۸ هفته تا ۵۰ mg', 'Overactive bladder — adult: 25 mg once daily, up to 50 mg after 4–8 weeks'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 25, 'increment': 25, 'incrementEveryDays': 28, 'max': 50}}, [R(My, '2.2')],
          notes=[note('همراه سولیفناسین: میرابگرون ۲۵ mg + سولیفناسین ۵ mg.', 'With solifenacin: mirabegron 25 mg + solifenacin 5 mg.', [R(My, '2.2')])]),
      reg('ndo', 'neurogenic-bladder', T('مثانه نوروژنیک کودک (۳ سال به بالا، ۳۵ kg به بالا) — ۲۵ mg روزانه، پس از ۴ تا ۸ هفته تا ۵۰ mg', 'Pediatric NDO (≥3 y, ≥35 kg) — 25 mg daily, up to 50 mg after 4–8 weeks'), {'minAge': age(3, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 35}, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 25, 'increment': 25, 'incrementEveryDays': 28, 'max': 50}}, [R(My, '2.3')],
          notes=[note('کودک زیر ۳۵ kg: گرانول Myrbetriq (با قرص mg به mg جایگزین نیست). کودک: همراه غذا.', 'Children <35 kg: Myrbetriq Granules (not interchangeable mg-for-mg). Children: take with food.', [R(My, '2.1'), R(My, '2.7')])])],
     [CI('hyper', 'حساسیت به میرابگرون یا اجزای فرآورده.', 'Hypersensitivity to mirabegron or excipients.', [R(My, '4')])],
     warn=[W('افزایش فشار خون (پایش)؛ احتباس ادرار با انسداد خروجی مثانه یا آنتی‌موسکارینی؛ آنژیوادم.', 'Raised blood pressure (monitor); urinary retention with outlet obstruction or antimuscarinics; angioedema.', [R(My, '5')])],
     renal=[RENAL(My, '2.4', 'eGFR ۱۵ تا ۲۹: حداکثر ۲۵ mg؛ زیر ۱۵: توصیه نمی‌شود.', 'eGFR 15–29: max 25 mg; <15: not recommended.', 30)],
     exs=[ex('oab', 'er-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

# --- calculator examples for every remaining calculated regimen ---
for i, exs_ in {
    'rabeprazole': [ex('du', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70), ex('gerd', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=14, weightKg=50)],
    'cefepime': [ex('uti', 'vial-1g', {'perDose': 500, 'upperPerDose': 1000}, ageYears=50, weightKg=70), ex('skin', 'vial-2g', {'perDose': 2000, 'dosesPerDay': 2}, ageYears=50, weightKg=70),
                 ex('iai', 'vial-2g', {'perDose': 2000, 'dosesPerDay': 2}, ageYears=50, weightKg=70), ex('child-fn', 'vial-1g', {'perDose': 1000, 'dosesPerDay': 3}, ageYears=5, weightKg=20)],
    'dolutegravir': [ex('adult-bid', 'tab-50', {'perDose': 50, 'dosesPerDay': 2}, ageYears=35, weightKg=70)],
    'meropenem': [ex('iai', 'vial-1g', {'perDose': 1000, 'dosesPerDay': 3}, ageYears=50, weightKg=70)],
    'piperacillin-tazobactam': [ex('hap', 'bulk', {'perDose': 4500, 'dosesPerDay': 4}, ageYears=60, weightKg=70), ex('hap-child', 'bulk', {'perDose': 2250, 'dosesPerDay': 4}, ageYears=5, weightKg=20),
                                ex('iai-infant', 'bulk', {'perDose': 540, 'dosesPerDay': 3}, ageMonths=5, weightKg=6)],
    'zidovudine': [ex('child-30', 'cap-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=12, weightKg=35), ex('pmtct', 'cap-100', {'perDose': 100, 'dosesPerDay': 5}, ageYears=28, weightKg=65)],
    'amiloride': [ex('hf', 'tab-5', {'perDose': 5, 'upperPerDose': 10}, ageYears=65, weightKg=75)],
    'flecainide': [ex('psvt', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70)],
    'propafenone': [ex('psvt', 'tab-150', {'perDose': 150, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70)],
    'mirabegron': [ex('ndo', 'er-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=40)],
    'etoricoxib': [ex('ra', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('as', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=75),
                   ex('dental', 'tab-90', {'perDose': 90, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)],
    'brivaracetam': [ex('child-50', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1, 'upperPerDose': 50}, ageYears=14, weightKg=55), ex('child-11', 'sol-10', {'perDose': 7.5, 'mlPerDose': 0.75}, ageYears=3, weightKg=15)],
    'lurasidone': [ex('scz-teen', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=15, weightKg=55), ex('bpd-child', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=40)],
    'paliperidone': [ex('sza', 'er-6', {'perDose': 6, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=75)],
}.items():
    patch(i, add_exs=exs_)

print('s9c ok')
