"""Stage 11c — biologics, transplant immunosuppressants and oral JAK/PDE4 inhibitors."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's11_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
INF = lambda src, sec='Boxed Warning': W('هشدار جعبه‌ای: عفونت جدی (سل، قارچی، فرصت‌طلب) و بدخیمی. پیش از شروع تست سل نهفته و در صورت مثبت بودن درمان آن.', 'Boxed warning: serious infections (TB, fungal, opportunistic) and malignancy. Test for latent TB before starting and treat if positive.', [R(src, sec)])
JAK = lambda src: W('هشدار جعبه‌ای (مهارکننده JAK): عفونت جدی، مرگ، بدخیمی، حوادث قلبی‌عروقی بزرگ و ترومبوز. تست سل پیش از شروع.', 'Boxed warning (JAK inhibitors): serious infections, mortality, malignancy, major adverse cardiovascular events and thrombosis. TB test before starting.', [R(src, 'Boxed Warning')])
ONCE = lambda id, dis, fa, en, pop, kg, refs, notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased', {'perKgPerDose': kg, 'intervalHours': 24}, refs, dur=ONE, notes=notes, allowed=allowed, limits=limits)

add_disease('psoriatic-arthritis', 'آرتریت پسوریاتیک', 'Psoriatic arthritis', ['PsA', 'آرتریت پسوریازیسی', 'psoriatic arthritis'], ['L40.50'], 'rheumatology')
add_disease('transplant-rejection', 'پیشگیری از رد پیوند عضو', 'Prevention of organ transplant rejection', ['transplant', 'پیوند کلیه', 'پیوند کبد', 'رد پیوند', 'rejection'], ['T86.10'], 'nephrology')
add_disease('b-cell-lymphoma', 'لنفوم غیرهوچکین سلول B و CLL', 'B-cell non-Hodgkin lymphoma and CLL', ['NHL', 'lymphoma', 'لنفوم', 'CLL', 'لوسمی لنفوسیتی مزمن'], ['C85.10', 'C91.10'], 'oncology')
add_disease('pemphigus', 'پمفیگوس ولگاریس', 'Pemphigus vulgaris', ['pemphigus', 'پمفیگوس', 'تاول پوستی'], ['L10.0'], 'dermatology')
add_disease('hidradenitis', 'هیدرادنیت چرکی', 'Hidradenitis suppurativa', ['HS', 'hidradenitis', 'هیدرادنیت', 'آبسه زیر بغل'], ['L73.2'], 'dermatology')
def ml(aid, title, review):
    m, dd, y = review.split('/')
    return add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                   edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
NOTE = {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}
def symptoms(did, items, *srcs):
    d = json.load(open(os.path.join(ROOT, 'diseases.json')))
    for x in d:
        if x['id'] == did: x['symptoms'] = {'items': [T(fa, en) for fa, en in items], 'refs': [{'source': s, 'section': 'Symptoms', 'note': NOTE} for s in srcs]}
    json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')
symptoms('psoriatic-arthritis', [('درد و تورم مفاصل، اغلب مفاصل انتهای انگشتان دست و پا', 'Joint pain and swelling, often the end joints of fingers and toes'), ('گاهی یک‌طرفه', 'Sometimes one-sided'), ('درد و خشکی ستون فقرات، بیشتر کمر و ساکروم', 'Spine pain and stiffness, mainly lower back and sacrum'),
                                 ('تغییرات پوست و ناخن پسوریازیس که اغلب همزمان با آرتریت بدتر می‌شود', 'Psoriasis skin and nail changes, often flaring with the arthritis'), ('التهاب تاندون (آشیل، کف پا)', 'Tendon inflammation (Achilles, plantar fascia)'), ('التهاب چشم', 'Eye inflammation')], ml('000413', 'Psoriatic arthritis', '1/28/2025'))
symptoms('transplant-rejection', [('کاهش عملکرد عضو پیوندی', 'Declining function of the transplanted organ'), ('احساس کسالت عمومی', 'General discomfort or ill feeling'), ('درد یا تورم ناحیه عضو (نادر)، تب (نادر)', 'Pain or swelling over the organ (rare), fever (rare)'),
                                  ('علائم شبه‌آنفلوانزا: لرز، درد بدن، تهوع، سرفه، تنگی نفس', 'Flu-like symptoms: chills, body aches, nausea, cough, shortness of breath'), ('کلیه: ادرار کمتر؛ قلب: علائم نارسایی قلب', 'Kidney: less urine; heart: heart-failure symptoms')], ml('000815', 'Transplant rejection', '4/1/2025'))
symptoms('b-cell-lymphoma', [('تورم غدد لنفاوی گردن، زیر بغل یا کشاله ران', 'Swollen lymph nodes in the neck, armpits or groin'), ('تعریق شبانه، تب و لرز متناوب', 'Night sweats, fever and chills that come and go'), ('خستگی و کاهش وزن', 'Fatigue and weight loss'), ('خارش', 'Itching'),
                             ('سرفه یا تنگی نفس (درگیری قفسه سینه)', 'Cough or shortness of breath (chest involvement)'), ('درد یا تورم شکم', 'Abdominal pain or swelling')], ml('000581', 'Non-Hodgkin lymphoma', '2/3/2025'))
symptoms('pemphigus', [('تاول و زخم دردناک دهان (در ۵۰ تا ۷۰٪ اولین علامت)', 'Painful mouth blisters and sores (the first sign in 50–70%)'), ('تاول پوستی که می‌آید و می‌رود', 'Skin blisters that come and go'), ('زخم‌های ترشح‌دار، دلمه‌بسته یا پوسته‌ریزی که به‌آسانی کنده می‌شوند', 'Oozing, crusting or peeling sores that detach easily'),
                       ('در دهان و گلو، صورت و چشم، پوست سر و تنه', 'In the mouth and throat, face and eyes, scalp and trunk')], ml('000882', 'Pemphigus vulgaris', '4/9/2026'))

# --- TNF and other biologics ---
Hu = fda('humira', 'FDA Humira', 'Humira (adalimumab) injection — Prescribing Information', sid('humira'))
drug('adalimumab', 'antineoplastic-immunomodulating', 'آدالیمومب', 'Adalimumab', T('مهارکننده TNF', 'TNF blocker'), [{'name': 'Humira', 'market': 'US'}], ['humira', 'هومیرا', 'آدالیمومب', 'cinnora', 'سینورا'],
     [form('pen-40', 'injection', 'sc', '40 mg/0.4 mL or 40 mg/0.8 mL pen/syringe (also 80 mg, 20 mg, 10 mg)', 40, 'mg', [R(Hu, '3')], vol=0.4)],
     [NC('ra', 'rheumatoid-arthritis', 'آرتریت روماتوئید، پسوریاتیک، اسپوندیلیت — بزرگسال ۴۰ mg یک هفته در میان', 'RA, PsA, ankylosing spondylitis — adult 40 mg every other week', A18,
         'هر دو هفته یک بار ۴۰ mg زیرجلدی (نه روزانه). در RA بدون متوترکسات ممکن است ۴۰ mg هفتگی یا ۸۰ mg دو هفته یک بار سود بیشتری داشته باشد.', '40 mg SC every OTHER WEEK (not daily). In RA without methotrexate some benefit from 40 mg weekly or 80 mg every other week.', [R(Hu, '2.2')]),
      NC('jia', 'juvenile-arthritis', 'آرتریت ایدیوپاتیک نوجوانان (۲ سال به بالا) — ۱۰/۲۰/۴۰ mg یک هفته در میان بر اساس وزن', 'JIA (≥2 y) — 10 / 20 / 40 mg every other week by weight', {'minAge': age(2, 'year')},
         'یک هفته در میان: ۱۰ تا <۱۵ kg ← ۱۰ mg؛ ۱۵ تا <۳۰ kg ← ۲۰ mg؛ ≥۳۰ kg ← ۴۰ mg.', 'Every other week: 10 to <15 kg → 10 mg; 15 to <30 kg → 20 mg; ≥30 kg → 40 mg.', [R(Hu, '2')]),
      NC('crohn', 'crohns', 'کرون و کولیت اولسروز — بزرگسال: ۱۶۰ mg روز ۱، ۸۰ mg روز ۱۵، سپس ۴۰ mg یک هفته در میان', 'Crohn’s / UC — adult: 160 mg day 1, 80 mg day 15, then 40 mg every other week', A18,
         'روز ۱: ۱۶۰ mg (یک روز یا تقسیم در دو روز)؛ روز ۱۵: ۸۰ mg؛ از روز ۲۹: ۴۰ mg یک هفته در میان.', 'Day 1: 160 mg (one day or split over two days); day 15: 80 mg; from day 29: 40 mg every other week.', [R(Hu, '2')]),
      NC('hs', 'hidradenitis', 'هیدرادنیت چرکی — بزرگسال: ۱۶۰ mg، ۸۰ mg روز ۱۵، سپس ۴۰ mg هفتگی یا ۸۰ mg دو هفته یک بار', 'Hidradenitis suppurativa — adult: 160 mg, 80 mg day 15, then 40 mg weekly or 80 mg every other week', A18,
         'روز ۱: ۱۶۰ mg؛ روز ۱۵: ۸۰ mg؛ از روز ۲۹: ۴۰ mg هفتگی یا ۸۰ mg یک هفته در میان.', 'Day 1: 160 mg; day 15: 80 mg; from day 29: 40 mg weekly or 80 mg every other week.', [R(Hu, '2.7')])],
     warn=[INF(Hu), W('لنفوم و بدخیمی در کودک و نوجوان؛ فعال شدن هپاتیت B؛ نارسایی قلب؛ بیماری دمیلینه‌کننده؛ واکسن زنده نه.', 'Lymphoma and malignancy in children and adolescents; hepatitis B reactivation; heart failure; demyelinating disease; no live vaccines.', [R(Hu, '5')])])

En = fda('enbrel', 'FDA Enbrel', 'Enbrel (etanercept) — Prescribing Information', sid('enbrel'))
drug('etanercept', 'antineoplastic-immunomodulating', 'اتانرسپت', 'Etanercept', T('مهارکننده TNF', 'TNF blocker'), [{'name': 'Enbrel', 'market': 'US'}], ['enbrel', 'انبرل', 'اتانرسپت', 'altebrel', 'آلتبرل'],
     [form('syr-50', 'injection', 'sc', '50 mg/mL prefilled syringe or autoinjector', 50, 'mg', [R(En, '3')], vol=1), form('vial-25', 'injection', 'sc', '25 mg/0.5 mL single-dose vial', 25, 'mg', [R(En, '3')], vol=0.5)],
     [NC('ra', 'rheumatoid-arthritis', 'آرتریت روماتوئید، پسوریاتیک، اسپوندیلیت — ۵۰ mg هفته‌ای یک بار', 'RA, PsA, ankylosing spondylitis — 50 mg once WEEKLY', A18, 'هفته‌ای یک بار ۵۰ mg زیرجلدی (نه روزانه)، با یا بدون متوترکسات.', '50 mg SC once WEEKLY (not daily), with or without methotrexate.', [R(En, '2')]),
      NC('pso', 'psoriasis', 'پسوریازیس پلاک بزرگسال — ۵۰ mg دو بار در هفته ۳ ماه، سپس هفته‌ای یک بار', 'Adult plaque psoriasis — 50 mg twice weekly for 3 months, then once weekly', A18, '۵۰ mg دو بار در هفته به مدت ۳ ماه، سپس ۵۰ mg هفته‌ای یک بار.', '50 mg twice weekly for 3 months, then 50 mg once weekly.', [R(En, '2')]),
      ONCE('jia', 'juvenile-arthritis', 'pJIA، پسوریازیس و JPsA کودک — ۰٫۸ mg/kg هفته‌ای یک بار (حداکثر ۵۰ mg)', 'pJIA, pediatric psoriasis and JPsA — 0.8 mg/kg once weekly (max 50 mg)', {'maxAge': age(18, 'year')}, 0.8, [R(En, '2.4')], allowed=['vial-25'],
           limits={'maxPerDose': 50, 'refs': [R(En, '2.4')]}, notes=[note('یک دوز در هفته (نه روزانه). ۶۳ kg یا بیشتر: ۵۰ mg هفتگی. برای دوزهای غیر از ۲۵ یا ۵۰ mg از ویال استفاده شود.', 'One dose per WEEK (not daily). ≥63 kg: 50 mg weekly. Use the vial for doses other than 25 or 50 mg.', [R(En, '2.4')])])],
     [CI('sepsis', 'سپسیس.', 'Sepsis.', [R(En, '4')])], warn=[INF(En)],
     exs=[ex('jia', 'vial-25', {'perDose': 20, 'mlPerDose': 0.4}, ageYears=8, weightKg=25)])

Rm = fda('remicade', 'FDA Remicade', 'Remicade (infliximab) 100 mg vial — Prescribing Information', sid('remicade'))
IND = note('القا در هفته ۰، ۲ و ۶، سپس نگهدارنده هر ۸ هفته (نه روزانه). انفوزیون وریدی دست‌کم ۲ ساعت.', 'Induction at weeks 0, 2 and 6, then maintenance every 8 weeks (not daily). IV infusion over at least 2 hours.', [R(Rm, '2.1')])
drug('infliximab', 'antineoplastic-immunomodulating', 'اینفلیکسیمب', 'Infliximab', T('مهارکننده TNF', 'TNF blocker'), [{'name': 'Remicade', 'market': 'US'}], ['remicade', 'رمیکید', 'اینفلیکسیماب', 'infimab'],
     [form('vial-100', 'powder-for-injection', 'iv', '100 mg vial', 100, 'mg', [R(Rm, '3')], per='vial')],
     [ONCE('crohn', 'crohns', 'کرون — بزرگسال و کودک ۶ سال به بالا: ۵ mg/kg هر نوبت (هفته ۰، ۲، ۶ و سپس هر ۸ هفته)', 'Crohn’s — adults and children ≥6 y: 5 mg/kg per infusion (weeks 0, 2, 6, then every 8 weeks)', {'minAge': age(6, 'year')}, 5, [R(Rm, '2.1'), R(Rm, '2.2')],
           notes=[IND, note('بزرگسال با از دست رفتن پاسخ: ۱۰ mg/kg ممکن است. بدون پاسخ تا هفته ۱۴ ادامه سودی ندارد.', 'Adults who lose response: 10 mg/kg may be considered. No response by week 14 — unlikely to respond.', [R(Rm, '2.1')])]),
      ONCE('uc', 'ulcerative-colitis', 'کولیت اولسروز — بزرگسال و کودک ۶ سال به بالا: ۵ mg/kg هر نوبت', 'Ulcerative colitis — adults and children ≥6 y: 5 mg/kg per infusion', {'minAge': age(6, 'year')}, 5, [R(Rm, '2.3'), R(Rm, '2.4')], notes=[IND]),
      ONCE('ra', 'rheumatoid-arthritis', 'آرتریت روماتوئید — ۳ mg/kg هر نوبت همراه متوترکسات', 'Rheumatoid arthritis — 3 mg/kg per infusion with methotrexate', A18, 3, [R(Rm, '2.5')],
           notes=[IND, note('پاسخ ناکافی: تا ۱۰ mg/kg هر ۸ هفته یا هر ۴ هفته.', 'Incomplete response: up to 10 mg/kg every 8 weeks or as often as every 4 weeks.', [R(Rm, '2.5')])]),
      ONCE('as', 'ankylosing-spondylitis', 'اسپوندیلیت آنکیلوزان — ۵ mg/kg (هفته ۰، ۲، ۶، سپس هر ۶ هفته)', 'Ankylosing spondylitis — 5 mg/kg (weeks 0, 2, 6, then every 6 weeks)', A18, 5, [R(Rm, '2.6')]),
      ONCE('psa', 'psoriatic-arthritis', 'آرتریت پسوریاتیک — ۵ mg/kg هر نوبت', 'Psoriatic arthritis — 5 mg/kg per infusion', A18, 5, [R(Rm, '2.7')], notes=[IND]),
      ONCE('pso', 'psoriasis', 'پسوریازیس شدید مزمن — ۵ mg/kg هر نوبت', 'Chronic severe plaque psoriasis — 5 mg/kg per infusion', A18, 5, [R(Rm, '2.8')], notes=[IND])],
     [CI('ci', 'دوز بیش از ۵ mg/kg در نارسایی قلبی متوسط یا شدید؛ حساسیت شدید قبلی به اینفلیکسیمب یا پروتئین موشی.', 'Doses >5 mg/kg in moderate or severe heart failure; previous severe hypersensitivity to infliximab or murine proteins.', [R(Rm, '4')])],
     warn=[INF(Rm), W('لنفوم سلول T کبدی-طحالی (بیشتر جوانان با آزاتیوپرین یا ۶-MP)؛ واکنش انفوزیون؛ فعال شدن هپاتیت B.', 'Hepatosplenic T-cell lymphoma (mostly young patients on azathioprine/6-MP); infusion reactions; hepatitis B reactivation.', [R(Rm, 'Boxed Warning'), R(Rm, '5')])],
     exs=[ex('crohn', 'vial-100', {'perDose': 350}, ageYears=30, weightKg=70), ex('uc', 'vial-100', {'perDose': 175}, ageYears=10, weightKg=35), ex('ra', 'vial-100', {'perDose': 210}, ageYears=50, weightKg=70),
          ex('as', 'vial-100', {'perDose': 350}, ageYears=35, weightKg=70), ex('psa', 'vial-100', {'perDose': 350}, ageYears=45, weightKg=70), ex('pso', 'vial-100', {'perDose': 350}, ageYears=45, weightKg=70)])

Rt = fda('rituxan', 'FDA Rituxan', 'Rituxan (rituximab) IV — Prescribing Information', sid('rituxan'))
PRE = note('پیش‌دارو قبل از هر انفوزیون: استامینوفن و آنتی‌هیستامین (و کورتون طبق رژیم). فقط انفوزیون وریدی، نه بولوس.', 'Premedicate before each infusion: acetaminophen and an antihistamine (and steroid per regimen). IV infusion only, never push or bolus.', [R(Rt, '2.8'), R(Rt, '2.1')])
drug('rituximab', 'antineoplastic-immunomodulating', 'ریتوکسیمب', 'Rituximab', T('آنتی‌بادی ضد CD20', 'Anti-CD20 antibody'), [{'name': 'Rituxan', 'market': 'US'}], ['rituxan', 'mabthera', 'zytux', 'ریتوکسیماب', 'زیتوکس'],
     [form('vial-10', 'injection', 'iv', '10 mg/mL (100 mg/10 mL, 500 mg/50 mL vials)', 10, 'mg', [R(Rt, '3')], vol=1)],
     [reg('nhl', 'b-cell-lymphoma', T('لنفوم غیرهوچکین سلول B — ۳۷۵ mg/m² هر نوبت', 'B-cell NHL — 375 mg/m² per infusion'), {}, 'bsa', {'perM2PerDay': 375, 'dividedDoses': 1}, [R(Rt, '2.2')], dur=ONE,
          notes=[PRE, note('عودکننده یا مقاوم: هفته‌ای یک بار ۴ یا ۸ دوز؛ درمان‌نشده: روز ۱ هر دوره شیمی‌درمانی تا ۸ دوز. CLL: دوره ۱ ← ۳۷۵ و دوره ۲ تا ۶ ← ۵۰۰ mg/m².', 'Relapsed/refractory: weekly for 4 or 8 doses; untreated: day 1 of each chemo cycle up to 8 doses. CLL: cycle 1 → 375, cycles 2–6 → 500 mg/m².', [R(Rt, '2.2'), R(Rt, '2.3')])]),
      reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — دو انفوزیون ۱۰۰۰ mg با فاصله ۲ هفته (همراه متوترکسات)', 'Rheumatoid arthritis — two 1000 mg infusions 2 weeks apart (with methotrexate)'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Rt, '2.5')], dur=ONE,
          notes=[PRE, note('متیل‌پردنیزولون ۱۰۰ mg وریدی ۳۰ دقیقه قبل از هر انفوزیون. دوره بعدی هر ۲۴ هفته، نه زودتر از ۱۶ هفته.', 'Methylprednisolone 100 mg IV 30 min before each infusion. Next course every 24 weeks, not sooner than 16 weeks.', [R(Rt, '2.5')])]),
      reg('pv', 'pemphigus', T('پمفیگوس ولگاریس — دو انفوزیون ۱۰۰۰ mg با فاصله ۲ هفته، همراه کاهش تدریجی کورتون', 'Pemphigus vulgaris — two 1000 mg infusions 2 weeks apart, with tapering steroids'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Rt, '2.7')], dur=ONE,
          notes=[PRE, note('نگهدارنده: ۵۰۰ mg در ماه ۱۲ و سپس هر ۶ ماه. عود: ۱۰۰۰ mg.', 'Maintenance: 500 mg at month 12 and every 6 months. Relapse: 1000 mg.', [R(Rt, '2.7')])])],
     warn=[W('هشدار جعبه‌ای: واکنش انفوزیون کشنده (بیشتر انفوزیون اول)، واکنش شدید پوستی-مخاطی، فعال شدن هپاتیت B (غربالگری HBsAg و anti-HBc قبل)، PML.', 'Boxed warning: fatal infusion reactions (mostly the first), severe mucocutaneous reactions, hepatitis B reactivation (screen HBsAg and anti-HBc first), PML.', [R(Rt, 'Boxed Warning')])],
     exs=[ex('nhl', 'vial-10', {'perDose': 754.67, 'mlPerDose': 75.47}, ageYears=55, weightKg=81, heightCm=180), ex('ra', 'vial-10', {'perDose': 1000, 'mlPerDose': 100}, ageYears=50, weightKg=70), ex('pv', 'vial-10', {'perDose': 1000, 'mlPerDose': 100}, ageYears=50, weightKg=70)])

Dp = fda('dupixent', 'FDA Dupixent', 'Dupixent (dupilumab) injection — Prescribing Information', sid('dupixent'))
drug('dupilumab', 'dermatology', 'دوپیلومب', 'Dupilumab', T('آنتی‌بادی ضد گیرنده IL-4α', 'Anti-IL-4Rα antibody'), [{'name': 'Dupixent', 'market': 'US'}], ['dupixent', 'دوپیکسنت', 'دوپیلوماب'],
     [form('syr-300', 'injection', 'sc', '300 mg/2 mL (and 200 mg/1.14 mL) pen or syringe', 300, 'mg', [R(Dp, '3')], vol=2)],
     [NC('ad', 'atopic-dermatitis', 'درماتیت آتوپیک بزرگسال — ۶۰۰ mg سپس ۳۰۰ mg هر ۲ هفته', 'Adult atopic dermatitis — 600 mg, then 300 mg every 2 weeks', A18,
         'دوز اول ۶۰۰ mg (دو تزریق ۳۰۰)، سپس ۳۰۰ mg هر ۲ هفته زیرجلدی (نه روزانه). کودک ۶ ماه به بالا: بر اساس جدول وزن برچسب.', 'Initial 600 mg (two 300 mg injections), then 300 mg SC every 2 weeks (not daily). Children ≥6 months: per label weight table.', [R(Dp, '2.3')]),
      NC('asthma', 'asthma', 'آسم ائوزینوفیلیک یا وابسته به کورتون — ۴۰۰ یا ۶۰۰ mg، سپس ۲۰۰ یا ۳۰۰ mg هر ۲ هفته', 'Eosinophilic or steroid-dependent asthma — 400 or 600 mg, then 200 or 300 mg every 2 weeks', {'minAge': age(6, 'year')},
         'نگهدارنده هر ۲ هفته طبق برچسب؛ کودک ۶ تا ۱۱ سال بر اساس وزن. برای حمله حاد آسم نیست.', 'Maintenance every 2 weeks per label; children 6–11 y by weight. Not for acute asthma attacks.', [R(Dp, '2')]),
      NC('copd', 'copd', 'COPD با ائوزینوفیلی — بزرگسال ۳۰۰ mg هر ۲ هفته', 'COPD with eosinophilia — adult 300 mg every 2 weeks', A18, '۳۰۰ mg زیرجلدی هر ۲ هفته.', '300 mg SC every 2 weeks.', [R(Dp, '2.8')])],
     [CI('hyper', 'حساسیت به دوپیلومب یا اجزای فرآورده.', 'Hypersensitivity to dupilumab or its excipients.', [R(Dp, '4')])],
     warn=[W('ورم ملتحمه و کراتیت؛ ائوزینوفیلی؛ کورتون را ناگهانی قطع نکنید؛ واکسن زنده نه.', 'Conjunctivitis and keratitis; eosinophilic conditions; do not stop steroids abruptly; no live vaccines.', [R(Dp, '5')])])

Xo = fda('xolair', 'FDA Xolair', 'Xolair (omalizumab) — Prescribing Information', sid('xolair'))
drug('omalizumab', 'respiratory', 'اومالیزومب', 'Omalizumab', T('آنتی‌بادی ضد IgE', 'Anti-IgE antibody'), [{'name': 'Xolair', 'market': 'US'}], ['xolair', 'زولر', 'اومالیزوماب'],
     [form('syr-150', 'injection', 'sc', '150 mg/mL prefilled syringe (also 75 mg/0.5 mL, 300 mg/2 mL)', 150, 'mg', [R(Xo, '3')], vol=1)],
     [reg('csu', 'chronic-urticaria', T('کهیر مزمن خودبه‌خودی (۱۲ سال به بالا) — ۱۵۰ یا ۳۰۰ mg هر ۴ هفته', 'Chronic spontaneous urticaria (≥12 y) — 150 or 300 mg every 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 150, 'perDoseMax': 300, 'dosesPerDay': 1}, [R(Xo, '2.5')], dur=ONE,
          notes=[note('یک دوز هر ۴ هفته (نه روزانه)؛ مستقل از IgE و وزن.', 'One dose every 4 WEEKS (not daily); independent of IgE and weight.', [R(Xo, '2.5')])]),
      NC('asthma', 'asthma', 'آسم آلرژیک متوسط تا شدید (۶ سال به بالا) — ۷۵ تا ۳۷۵ mg هر ۲ یا ۴ هفته بر اساس IgE و وزن', 'Moderate–severe allergic asthma (≥6 y) — 75–375 mg every 2 or 4 weeks by IgE and weight', {'minAge': age(6, 'year')},
         'دوز و فاصله از جدول برچسب بر اساس IgE تام سرم پیش از درمان و وزن.', 'Dose and interval from the label tables by pre-treatment total serum IgE and body weight.', [R(Xo, '2.2')])],
     [CI('hyper', 'واکنش حساسیتی شدید به اومالیزومب.', 'Severe hypersensitivity reaction to omalizumab.', [R(Xo, '4')])],
     warn=[W('هشدار جعبه‌ای: آنافیلاکسی (حتی پس از یک سال)؛ شروع در مرکز درمانی با مشاهده پس از تزریق.', 'Boxed warning: anaphylaxis (even after a year); start in a healthcare setting with observation after injection.', [R(Xo, 'Boxed Warning')])],
     exs=[ex('csu', 'syr-150', {'perDose': 150, 'mlPerDose': 1, 'upperPerDose': 300}, ageYears=30, weightKg=70)])

Sl = fda('stelara', 'FDA Stelara', 'Stelara (ustekinumab) — Prescribing Information', sid('stelara'))
drug('ustekinumab', 'antineoplastic-immunomodulating', 'اوستکینومب', 'Ustekinumab', T('مهارکننده IL-12/23', 'IL-12/23 inhibitor'), [{'name': 'Stelara', 'market': 'US'}], ['stelara', 'استلارا', 'اوستکینوماب'],
     [form('iv-130', 'injection', 'iv', '130 mg/26 mL (5 mg/mL) IV vial', 5, 'mg', [R(Sl, '3')], vol=1), form('sc-45', 'injection', 'sc', '45 mg/0.5 mL prefilled syringe (also 90 mg/mL)', 45, 'mg', [R(Sl, '3')], vol=0.5)],
     [reg('cd-iv', 'crohns', T('کرون و کولیت اولسروز — القای وریدی یک‌باره بر اساس وزن: ≤۵۵ kg ۲۶۰، ۵۵ تا ۸۵ ← ۳۹۰، >۸۵ ← ۵۲۰ mg', 'Crohn’s / UC — single IV induction by weight: ≤55 kg 260, 55–85 → 390, >85 kg → 520 mg'), A18, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 55, 'perDose': 260, 'dosesPerDay': 1}, {'minWeightKg': 55, 'maxWeightKg': 85, 'perDose': 390, 'dosesPerDay': 1}, {'minWeightKg': 85, 'maxWeightKg': None, 'perDose': 520, 'dosesPerDay': 1}]},
          [R(Sl, '2.3, Table 4'), R(Sl, '2.5')], dur=ONE, allowed=['iv-130'], notes=[note('یک انفوزیون (دست‌کم ۱ ساعت)؛ سپس ۹۰ mg زیرجلدی ۸ هفته بعد و هر ۸ هفته.', 'One infusion (≥1 h); then 90 mg SC 8 weeks later and every 8 weeks.', [R(Sl, '2.3')])]),
      NC('pso', 'psoriasis', 'پسوریازیس پلاک بزرگسال — ≤۱۰۰ kg: ۴۵ mg؛ >۱۰۰ kg: ۹۰ mg (هفته ۰ و ۴، سپس هر ۱۲ هفته)', 'Adult plaque psoriasis — ≤100 kg: 45 mg; >100 kg: 90 mg (weeks 0 and 4, then every 12 weeks)', A18,
         'زیرجلدی در هفته ۰ و ۴، سپس هر ۱۲ هفته؛ دوز بر اساس وزن ۱۰۰ kg.', 'SC at weeks 0 and 4, then every 12 weeks; dose by the 100 kg cut-off.', [R(Sl, '2.1')]),
      NC('psa', 'psoriatic-arthritis', 'آرتریت پسوریاتیک — ۴۵ mg هفته ۰ و ۴، سپس هر ۱۲ هفته', 'Psoriatic arthritis — 45 mg at weeks 0 and 4, then every 12 weeks', A18, 'همراه پسوریازیس متوسط تا شدید و وزن >۱۰۰ kg: ۹۰ mg.', 'With moderate–severe psoriasis and weight >100 kg: 90 mg.', [R(Sl, '2.2')])],
     [CI('hyper', 'حساسیت قابل‌توجه به اوستکینومب یا اجزای آن.', 'Clinically significant hypersensitivity to ustekinumab or excipients.', [R(Sl, '4')])],
     warn=[W('عفونت جدی و سل (تست قبل)؛ بدخیمی؛ سندرم انسفالوپاتی برگشت‌پذیر خلفی؛ واکسن زنده نه.', 'Serious infections and TB (test first); malignancy; posterior reversible encephalopathy; no live vaccines.', [R(Sl, '5')])],
     exs=[ex('cd-iv', 'iv-130', {'perDose': 390, 'mlPerDose': 78}, ageYears=35, weightKg=70)])

Cs = fda('cosentyx', 'FDA Cosentyx', 'Cosentyx (secukinumab) — Prescribing Information', sid('cosentyx'))
LOAD = 'هفته ۰، ۱، ۲، ۳ و ۴ و سپس هر ۴ هفته زیرجلدی (نه روزانه).'; LOADEN = 'At weeks 0, 1, 2, 3 and 4 and then every 4 weeks SC (not daily).'
drug('secukinumab', 'antineoplastic-immunomodulating', 'سکوکینومب', 'Secukinumab', T('مهارکننده IL-17A', 'IL-17A inhibitor'), [{'name': 'Cosentyx', 'market': 'US'}], ['cosentyx', 'کوزنتیکس', 'سکوکینوماب'],
     [form('pen-150', 'injection', 'sc', '150 mg/mL pen or syringe (also 300 mg/2 mL, 75 mg/0.5 mL)', 150, 'mg', [R(Cs, '3')], vol=1)],
     [NC('pso', 'psoriasis', 'پسوریازیس پلاک بزرگسال — ۳۰۰ mg (هفته ۰ تا ۴، سپس هر ۴ هفته)', 'Adult plaque psoriasis — 300 mg (weeks 0–4, then every 4 weeks)', A18, LOAD + ' برای برخی بیماران ۱۵۰ mg کافی است.', LOADEN + ' 150 mg may be acceptable for some patients.', [R(Cs, '2.3')]),
      NC('as', 'ankylosing-spondylitis', 'اسپوندیلیت آنکیلوزان و آرتریت پسوریاتیک — ۱۵۰ mg (با یا بدون بارگذاری) هر ۴ هفته', 'Ankylosing spondylitis and PsA — 150 mg (with or without loading) every 4 weeks', A18, LOAD + ' بدون بارگذاری: ۱۵۰ mg هر ۴ هفته؛ در صورت فعال ماندن ۳۰۰ mg.', LOADEN + ' Without loading: 150 mg every 4 weeks; if still active, 300 mg.', [R(Cs, '2.4'), R(Cs, '2.6')]),
      NC('hs', 'hidradenitis', 'هیدرادنیت چرکی بزرگسال — ۳۰۰ mg (هفته ۰ تا ۴، سپس هر ۴ هفته)', 'Adult hidradenitis suppurativa — 300 mg (weeks 0–4, then every 4 weeks)', A18, LOAD + ' پاسخ ناکافی: ۳۰۰ mg هر ۲ هفته.', LOADEN + ' Inadequate response: 300 mg every 2 weeks.', [R(Cs, '2.10')])],
     [CI('hyper', 'حساسیت جدی به سکوکینومب (آنافیلاکسی، آنژیوادم).', 'Serious hypersensitivity to secukinumab (anaphylaxis, angioedema).', [R(Cs, '4')])],
     warn=[W('عفونت (تست سل قبل)؛ بیماری التهابی روده (تشدید یا شروع جدید)؛ اگزمای شدید.', 'Infections (TB test first); inflammatory bowel disease (exacerbation or new onset); eczematous eruptions.', [R(Cs, '5')])])

# --- transplant and oral immunosuppressants ---
Mf = fda('mycophenolate', 'FDA Mycophenolate', 'Mycophenolate mofetil capsules 250 mg — Prescribing Information', sid('mmf'))
drug('mycophenolate', 'antineoplastic-immunomodulating', 'مایکوفنولات موفتیل', 'Mycophenolate mofetil', T('سرکوب‌کننده ایمنی (آنتی‌متابولیت)', 'Immunosuppressant (antimetabolite)'), [{'name': 'CellCept', 'market': 'US'}], ['cellcept', 'سل سپت', 'MMF', 'مایکوفنولات', 'cellmune'],
     [tab('cap-250', 250, '250 mg capsule', [R(Mf, '3')], per='capsule', form_='capsule')],
     [reg('kidney', 'transplant-rejection', T('پیوند کلیه — بزرگسال ۱ g دو بار در روز', 'Kidney transplant — adult 1 g twice daily'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 2}, [R(Mf, '2.2')],
          notes=[note('همراه سیکلوسپورین یا تاکرولیموس و کورتون. GFR زیر ۲۵ در کلیه پیوندی: بیش از ۱ g دو بار در روز نه. ANC زیر ۱۳۰۰: قطع یا کاهش.', 'With cyclosporine or tacrolimus and steroids. Graft GFR <25: no more than 1 g twice daily. ANC <1300: interrupt or reduce.', [R(Mf, '2.5')])]),
      reg('heart', 'transplant-rejection', T('پیوند قلب یا کبد — بزرگسال ۱٫۵ g دو بار در روز', 'Heart or liver transplant — adult 1.5 g twice daily'), A18, 'fixed', {'perDose': 1500, 'dosesPerDay': 2}, [R(Mf, '2.3'), R(Mf, '2.4')]),
      reg('child', 'transplant-rejection', T('پیوند کلیه کودک (۳ ماه به بالا) — ۶۰۰ mg/m² دو بار در روز (حداکثر ۲ g/روز)', 'Pediatric kidney transplant (≥3 months) — 600 mg/m² twice daily (max 2 g/day)'), {'minAge': age(3, 'month'), 'maxAge': age(18, 'year')}, 'bsa', {'perM2PerDay': 1200, 'dividedDoses': 2}, [R(Mf, '2.2')],
          limits={'maxPerDay': 2000, 'refs': [R(Mf, '2.2')]}, notes=[note('کودک معمولاً سوسپانسیون CellCept؛ کپسول برای کودکی که قادر به بلع باشد.', 'Children usually receive CellCept oral suspension; capsules if able to swallow.', [R(Mf, '2.2')])])],
     [CI('hyper', 'حساسیت به مایکوفنولات یا مایکوفنولیک اسید.', 'Hypersensitivity to mycophenolate mofetil or mycophenolic acid.', [R(Mf, '4')])],
     warn=[W('هشدار جعبه‌ای: سقط و ناهنجاری جنینی (پیشگیری از بارداری لازم)، لنفوم و بدخیمی پوست، عفونت جدی.', 'Boxed warning: first-trimester loss and congenital malformations (contraception required), lymphoma and skin malignancy, serious infections.', [R(Mf, 'Boxed Warning')])],
     exs=[ex('kidney', 'cap-250', {'perDose': 1000, 'tabletsPerDoseRounded': 4}, ageYears=45, weightKg=70), ex('heart', 'cap-250', {'perDose': 1500, 'tabletsPerDoseRounded': 6}, ageYears=45, weightKg=70),
          ex('child', 'cap-250', {'perDose': 750, 'tabletsPerDoseRounded': 3}, ageYears=12, weightKg=37.5, heightCm=150)])

Pg = fda('prograf', 'FDA Prograf', 'Prograf (tacrolimus) capsules, granules and injection — Prescribing Information', sid('prograf')); T1 = R(Pg, '2.2, Table 1')
TDM = note('دوز اولیه؛ سپس بر اساس سطح خونی (TDM) طبق جدول. اولین دوز کبد، قلب و ریه دست‌کم ۶ ساعت پس از پیوند. گریپ‌فروت نه.', 'Initial dose; then adjust by whole-blood trough levels per the table. First dose for liver/heart/lung no sooner than 6 h after transplant. Avoid grapefruit.', [T1, R(Pg, '2.2'), R(Pg, '2.1')])
TAC = ['cap-05', 'cap-1', 'cap-5']
drug('tacrolimus-oral', 'antineoplastic-immunomodulating', 'تاکرولیموس خوراکی', 'Tacrolimus (oral)', T('مهارکننده کلسی‌نورین', 'Calcineurin inhibitor'), [{'name': 'Prograf', 'market': 'US'}], ['prograf', 'پروگراف', 'تاکرولیموس', 'tacrolimus'],
     [tab('cap-05', 0.5, '0.5 mg capsule', [R(Pg, '3')], per='capsule', form_='capsule'), tab('cap-1', 1, '1 mg capsule', [R(Pg, '3')], per='capsule', form_='capsule'), tab('cap-5', 5, '5 mg capsule', [R(Pg, '3')], per='capsule', form_='capsule')],
     [reg('kidney-mmf', 'transplant-rejection', T('پیوند کلیه همراه MMF یا آنتاگونیست IL-2 — ۰٫۱ mg/kg/روز در دو دوز هر ۱۲ ساعت', 'Kidney transplant with MMF or IL-2RA — 0.1 mg/kg/day in two doses every 12 h'), A18, 'weightBased', {'perKgPerDay': 0.1, 'dividedDoses': 2}, [T1], allowed=TAC, notes=[TDM]),
      reg('kidney-aza', 'transplant-rejection', T('پیوند کلیه همراه آزاتیوپرین — ۰٫۲ mg/kg/روز در دو دوز', 'Kidney transplant with azathioprine — 0.2 mg/kg/day in two doses'), A18, 'weightBased', {'perKgPerDay': 0.2, 'dividedDoses': 2}, [T1], allowed=TAC, notes=[TDM]),
      reg('liver', 'transplant-rejection', T('پیوند کبد — ۰٫۱ تا ۰٫۱۵ mg/kg/روز در دو دوز', 'Liver transplant — 0.1–0.15 mg/kg/day in two doses'), A18, 'weightBased', {'perKgPerDay': 0.1, 'perKgPerDayMax': 0.15, 'dividedDoses': 2}, [T1], allowed=TAC, notes=[TDM]),
      reg('heart', 'transplant-rejection', T('پیوند قلب — ۰٫۰۷۵ mg/kg/روز در دو دوز', 'Heart transplant — 0.075 mg/kg/day in two doses'), A18, 'weightBased', {'perKgPerDay': 0.075, 'dividedDoses': 2}, [T1], allowed=TAC, notes=[TDM])],
     [CI('hyper', 'حساسیت به تاکرولیموس؛ تزریقی: حساسیت به روغن کرچک هیدروژنه (HCO-60).', 'Hypersensitivity to tacrolimus; injection: hypersensitivity to HCO-60 (polyoxyl 60 hydrogenated castor oil).', [R(Pg, '4')])],
     warn=[W('هشدار جعبه‌ای: بدخیمی و عفونت جدی. سمیت کلیه و عصب، دیابت پس از پیوند، طولانی شدن QT؛ تداخل‌های زیاد با مهار/القاگر CYP3A.', 'Boxed warning: malignancy and serious infections. Nephrotoxicity, neurotoxicity, post-transplant diabetes, QT prolongation; many CYP3A interactions.', [R(Pg, 'Boxed Warning'), R(Pg, '5')])],
     exs=[ex('kidney-mmf', 'cap-05', {'perDose': 3.5, 'tabletsPerDoseRounded': 7}, ageYears=45, weightKg=70), ex('kidney-aza', 'cap-1', {'perDose': 7, 'tabletsPerDoseRounded': 7}, ageYears=45, weightKg=70),
          ex('liver', 'cap-05', {'perDose': 3.5, 'upperPerDose': 5.25}, ageYears=50, weightKg=70), ex('heart', 'cap-05', {'perDose': 3, 'tabletsPerDoseRounded': 6}, ageYears=50, weightKg=80)])

Nr = fda('neoral', 'FDA Neoral', 'Neoral (cyclosporine, modified) capsules and oral solution — Prescribing Information', sid('neoral')); d = R(Nr, 'Dosage and Administration')
NEO = note('Neoral و Sandimmune هم‌ارز زیستی نیستند و بدون نظارت پزشک جایگزین نمی‌شوند. همیشه در دو دوز. فشار خون و کراتینین پایش شود.', 'Neoral and Sandimmune are not bioequivalent and must not be interchanged without physician supervision. Always in two doses. Monitor BP and creatinine.', [d])
drug('cyclosporine-oral', 'antineoplastic-immunomodulating', 'سیکلوسپورین خوراکی (Neoral)', 'Cyclosporine (oral, modified)', T('مهارکننده کلسی‌نورین', 'Calcineurin inhibitor'), [{'name': 'Neoral', 'market': 'US'}], ['neoral', 'sandimmune', 'gengraf', 'سیکلوسپورین', 'ایمونورال', 'ciclosporin'],
     [liquid('sol-100', 100, 1, '100 mg/mL oral solution', [R(Nr, 'How Supplied')], form_='solution'), tab('cap-25', 25, '25 mg capsule', [R(Nr, 'How Supplied')], per='capsule', form_='capsule'), tab('cap-100', 100, '100 mg capsule', [R(Nr, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — شروع ۲٫۵ mg/kg/روز در دو دوز', 'Rheumatoid arthritis — start 2.5 mg/kg/day in two doses'), A18, 'weightBased', {'perKgPerDay': 2.5, 'dividedDoses': 2}, [d],
          limits={'maxPerKgPerDay': 4, 'refs': [d]}, notes=[NEO, note('اثر پس از ۴ تا ۸ هفته. افزایش ۰٫۵ تا ۰٫۷۵ mg/kg/روز پس از ۸ و ۱۲ هفته تا حداکثر ۴ mg/kg/روز.', 'Onset 4–8 weeks. Increase by 0.5–0.75 mg/kg/day after 8 and 12 weeks up to 4 mg/kg/day.', [d])]),
      reg('pso', 'psoriasis', T('پسوریازیس شدید — شروع ۲٫۵ mg/kg/روز (۱٫۲۵ mg/kg دو بار)', 'Severe psoriasis — start 2.5 mg/kg/day (1.25 mg/kg twice daily)'), A18, 'weightBased', {'perKgPerDay': 2.5, 'dividedDoses': 2}, [d],
          limits={'maxPerKgPerDay': 4, 'refs': [d]}, notes=[NEO, note('دست‌کم ۴ هفته؛ سپس هر ۲ هفته حدود ۰٫۵ mg/kg/روز افزایش تا حداکثر ۴ mg/kg/روز.', 'At least 4 weeks; then increase about 0.5 mg/kg/day every 2 weeks up to 4 mg/kg/day.', [d])]),
      NC('tx', 'transplant-rejection', 'پیوند عضو — دوز اولیه بر اساس عضو و پروتکل (میانگین ۷ تا ۹ mg/kg/روز)', 'Organ transplant — initial dose by organ and protocol (mean 7–9 mg/kg/day)', {},
         'برچسب فقط میانگین مراکز را ذکر کرده (کلیه ۹±۳، کبد ۸±۴، قلب ۷±۳ mg/kg/روز) و دوز بر اساس سطح خونی تنظیم می‌شود؛ طبق پروتکل مرکز پیوند.', 'The label only gives centre survey means (kidney 9±3, liver 8±4, heart 7±3 mg/kg/day); dose is adjusted by blood levels — follow the transplant centre protocol.', [d])],
     [CI('ci', 'حساسیت به سیکلوسپورین. RA و پسوریازیس: نارسایی کلیه، فشار خون کنترل‌نشده یا بدخیمی. پسوریازیس: همراه PUVA یا UVB، متوترکسات یا سایر سرکوب‌کننده‌ها، قطران یا پرتودرمانی نه.', 'Hypersensitivity to cyclosporine. RA and psoriasis: abnormal renal function, uncontrolled hypertension or malignancy. Psoriasis: not with PUVA or UVB, methotrexate or other immunosuppressants, coal tar or radiation.', [R(Nr, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: فقط توسط پزشک مجرب در سرکوب ایمنی؛ عفونت و لنفوم؛ سمیت کلیه و فشار خون؛ پسوریازیس با PUVA قبلی خطر سرطان پوست.', 'Boxed warning: only by physicians experienced in immunosuppression; infection and lymphoma; nephrotoxicity and hypertension; psoriasis after PUVA — skin cancer risk.', [R(Nr, 'Boxed Warning')])],
     exs=[ex('ra', 'sol-100', {'perDose': 87.5, 'mlPerDose': 0.88}, ageYears=50, weightKg=70), ex('pso', 'sol-100', {'perDose': 87.5, 'mlPerDose': 0.88}, ageYears=40, weightKg=70)])

Xj = fda('xeljanz', 'FDA Xeljanz', 'Xeljanz / Xeljanz XR (tofacitinib) — Prescribing Information', sid('xeljanz'))
drug('tofacitinib', 'antineoplastic-immunomodulating', 'توفاسیتینیب', 'Tofacitinib', T('مهارکننده JAK', 'JAK inhibitor'), [{'name': 'Xeljanz', 'market': 'US'}], ['xeljanz', 'زلجانز', 'توفاسیتینیب'],
     [tab('tab-5', 5, '5 mg tablet', [R(Xj, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Xj, '3')])],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید، پسوریاتیک، اسپوندیلیت — ۵ mg دو بار در روز (یا XR ۱۱ mg یک بار)', 'RA, PsA, AS — 5 mg twice daily (or XR 11 mg once daily)'), A18, 'fixed', {'perDose': 5, 'dosesPerDay': 2}, [R(Xj, '2.3, Table 1')],
          notes=[note('نارسایی کلیه متوسط/شدید یا کبد متوسط: ۵ mg یک بار در روز. لنفوسیت زیر ۵۰۰، ANC زیر ۱۰۰۰ یا Hb زیر ۸ شروع نشود.', 'Moderate/severe renal or moderate hepatic impairment: 5 mg once daily. Do not start if lymphocytes <500, ANC <1000 or Hb <8.', [R(Xj, '2.3, Table 1')])]),
      reg('uc', 'ulcerative-colitis', T('کولیت اولسروز — القا ۱۰ mg دو بار در روز دست‌کم ۸ هفته، سپس ۵ mg دو بار', 'Ulcerative colitis — induction 10 mg twice daily for ≥8 weeks, then 5 mg twice daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 2}, [R(Xj, '2.5, Table 3')],
          notes=[note('در صورت نیاز ۱۰ mg دو بار تا حداکثر ۱۶ هفته؛ بدون پاسخ کافی قطع شود.', 'If needed 10 mg twice daily up to 16 weeks maximum; stop if no adequate response.', [R(Xj, '2.5, Table 3')])])],
     warn=[JAK(Xj)], exs=[ex('ra', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('uc', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Ol = fda('olumiant', 'FDA Olumiant', 'Olumiant (baricitinib) tablets — Prescribing Information', sid('olumiant'))
drug('baricitinib', 'antineoplastic-immunomodulating', 'باریسیتینیب', 'Baricitinib', T('مهارکننده JAK', 'JAK inhibitor'), [{'name': 'Olumiant', 'market': 'US'}], ['olumiant', 'اولومیانت', 'باریسیتینیب'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Ol, '3')]) for m in (1, 2, 4)],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — ۲ mg یک بار در روز', 'Rheumatoid arthritis — 2 mg once daily'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Ol, '2.2')]),
      reg('covid', 'covid-19', T('کووید-۱۹ بستری — بزرگسال ۴ mg یک بار در روز تا ۱۴ روز', 'Hospitalised COVID-19 — adult 4 mg once daily up to 14 days'), A18, 'fixed', {'perDose': 4, 'dosesPerDay': 1}, [R(Ol, '2.3')], dur={'min': 1, 'max': 14},
          notes=[note('۱۴ روز یا تا ترخیص، هر کدام زودتر.', '14 days or until discharge, whichever comes first.', [R(Ol, '2.3')])]),
      reg('aa', 'alopecia', T('آلوپسی آره‌آتای شدید (۱۲ سال به بالا) — ۲ mg، در صورت پاسخ ناکافی ۴ mg', 'Severe alopecia areata (≥12 y) — 2 mg, 4 mg if inadequate response'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 2, 'perDoseMax': 4, 'dosesPerDay': 1}, [R(Ol, '2.4')],
          notes=[note('ریزش تقریباً کامل مو: شروع با ۴ mg قابل‌بررسی؛ پس از پاسخ به ۲ mg کاهش.', 'Nearly complete hair loss: consider starting with 4 mg; reduce to 2 mg once responding.', [R(Ol, '2.4')])])],
     warn=[JAK(Ol)], exs=[ex('ra', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('covid', 'tab-4', {'perDose': 4, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=80),
                         ex('aa', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1, 'upperPerDose': 4}, ageYears=30, weightKg=65)])

Rv = fda('rinvoq', 'FDA Rinvoq', 'Rinvoq (upadacitinib) extended-release tablets — Prescribing Information', sid('rinvoq'))
drug('upadacitinib', 'antineoplastic-immunomodulating', 'اوپاداسیتینیب', 'Upadacitinib', T('مهارکننده JAK', 'JAK inhibitor'), [{'name': 'Rinvoq', 'market': 'US'}], ['rinvoq', 'رینووک', 'اوپاداسیتینیب'],
     [tab(f'er-{m}', m, f'{m} mg extended-release tablet', [R(Rv, '3')]) for m in (15, 30, 45)],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — ۱۵ mg یک بار در روز', 'Rheumatoid arthritis — 15 mg once daily'), A18, 'fixed', {'perDose': 15, 'dosesPerDay': 1}, [R(Rv, '2.3')]),
      reg('ad', 'atopic-dermatitis', T('درماتیت آتوپیک (۱۲ سال و ≥۴۰ kg، زیر ۶۵ سال) — ۱۵ mg، در صورت پاسخ ناکافی ۳۰ mg', 'Atopic dermatitis (≥12 y and ≥40 kg, <65 y) — 15 mg, 30 mg if inadequate response'), {'minAge': age(12, 'year'), 'maxAge': age(65, 'year'), 'minWeightKg': 40}, 'fixed',
          {'perDose': 15, 'perDoseMax': 30, 'dosesPerDay': 1}, [R(Rv, '2.5')], notes=[note('۶۵ سال به بالا: ۱۵ mg. نارسایی شدید کلیه: ۱۵ mg.', '≥65 y: 15 mg. Severe renal impairment: 15 mg.', [R(Rv, '2.5'), R(Rv, '2.12')])]),
      reg('uc', 'ulcerative-colitis', T('کولیت اولسروز — القا ۴۵ mg روزانه ۸ هفته، نگهدارنده ۱۵ mg (تا ۳۰)', 'Ulcerative colitis — induction 45 mg daily for 8 weeks, maintenance 15 mg (up to 30)'), A18, 'fixed', {'perDose': 45, 'dosesPerDay': 1}, [R(Rv, '2.6')], dur={'min': 56, 'max': 56}),
      reg('cd', 'crohns', T('کرون — القا ۴۵ mg روزانه ۱۲ هفته، نگهدارنده ۱۵ mg (تا ۳۰)', 'Crohn’s — induction 45 mg daily for 12 weeks, maintenance 15 mg (up to 30)'), A18, 'fixed', {'perDose': 45, 'dosesPerDay': 1}, [R(Rv, '2.7')], dur={'min': 84, 'max': 84})],
     [CI('hyper', 'حساسیت به اوپاداسیتینیب.', 'Hypersensitivity to upadacitinib.', [R(Rv, '4')])], warn=[JAK(Rv)],
     exs=[ex('ra', 'er-15', {'perDose': 15, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('ad', 'er-15', {'perDose': 15, 'tabletsPerDoseRounded': 1, 'upperPerDose': 30}, ageYears=25, weightKg=65),
          ex('uc', 'er-45', {'perDose': 45, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70), ex('cd', 'er-45', {'perDose': 45, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=70)])

Oz = fda('otezla', 'FDA Otezla', 'Otezla / Otezla XR (apremilast) — Prescribing Information', sid('otezla'))
drug('apremilast', 'antineoplastic-immunomodulating', 'آپرمیلاست', 'Apremilast', T('مهارکننده PDE4', 'PDE4 inhibitor'), [{'name': 'Otezla', 'market': 'US'}], ['otezla', 'اوتزلا', 'آپرمیلاست'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Oz, '3')]) for m in (10, 20, 30)],
     [reg('pso', 'psoriasis', T('پسوریازیس پلاک، آرتریت پسوریاتیک، بهجت — بزرگسال نگهدارنده ۳۰ mg دو بار در روز (پس از تیتراسیون ۵ روزه)', 'Plaque psoriasis, PsA, Behçet’s — adult maintenance 30 mg twice daily (after 5-day titration)'), A18, 'fixed', {'perDose': 30, 'dosesPerDay': 2}, [R(Oz, '2.1')],
          notes=[note('تیتراسیون روز ۱ تا ۵ طبق جدول ۱ برچسب (از ۱۰ mg صبح) برای کاهش عوارض گوارشی. نارسایی شدید کلیه: ۳۰ mg یک بار در روز.', 'Days 1–5 titration per label Table 1 (from 10 mg in the morning) to reduce GI effects. Severe renal impairment: 30 mg once daily.', [R(Oz, '2.1'), R(Oz, '2')])]),
      reg('psa', 'psoriatic-arthritis', T('آرتریت پسوریاتیک — ۳۰ mg دو بار در روز', 'Psoriatic arthritis — 30 mg twice daily'), A18, 'fixed', {'perDose': 30, 'dosesPerDay': 2}, [R(Oz, '2.1')])],
     [CI('hyper', 'حساسیت به آپرمیلاست.', 'Hypersensitivity to apremilast.', [R(Oz, '4')])],
     warn=[W('اسهال، تهوع و استفراغ شدید؛ افسردگی و افکار خودکشی؛ کاهش وزن.', 'Severe diarrhoea, nausea and vomiting; depression and suicidal thoughts; weight loss.', [R(Oz, '5')])],
     exs=[ex('pso', 'tab-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=75), ex('psa', 'tab-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=75)])
print('s11c ok')
