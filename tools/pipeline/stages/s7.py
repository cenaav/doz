"""Stage 7 — pain, rheumatology and bone, GI and skin."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's7_setids.json')))
sid = lambda k: S[k][0]

add_disease('crohns', 'بیماری کرون', 'Crohn’s disease', ['crohn', 'کرون', 'IBD'], ['K50.90'], 'gastroenterology')
add_disease('melasma', 'ملاسما (کک‌ومک بارداری)', 'Melasma', ['melasma', 'chloasma', 'ملاسما', 'لک صورت'], ['L81.1'], 'dermatology')
add_disease('genital-warts', 'زگیل تناسلی', 'Anogenital warts', ['condyloma', 'genital warts', 'زگیل تناسلی', 'کوندیلوما'], ['A63.0'], 'dermatology')
add_disease('actinic-keratosis', 'کراتوز اکتینیک', 'Actinic keratosis', ['actinic keratosis', 'کراتوز آفتابی'], ['L57.0'], 'dermatology')
add_disease('postherpetic-neuralgia', 'نورالژی پس از زونا', 'Postherpetic neuralgia', ['PHN', 'postherpetic neuralgia', 'درد بعد از زونا'], ['B02.29'], 'neurology')
add_disease('chronic-idiopathic-constipation', 'یبوست مزمن ایدیوپاتیک', 'Chronic idiopathic constipation', ['CIC', 'chronic constipation', 'یبوست مزمن'], ['K59.04'], 'gastroenterology')
NSAID_CI = lambda src, sec: CI('nsaid', 'حساسیت؛ سابقه آسم، کهیر یا واکنش آلرژیک با آسپرین یا NSAID؛ درد حین جراحی CABG.', 'Hypersensitivity; history of asthma, urticaria or allergic reaction to aspirin or NSAIDs; perioperative pain in CABG.', [R(src, sec)])
NSAID_W = lambda src: W('هشدار جعبه‌ای: خطر حوادث قلبی‌عروقی ترومبوتیک و خونریزی، زخم و سوراخ شدن دستگاه گوارش.', 'Boxed warning: risk of serious thrombotic cardiovascular events and GI bleeding, ulceration and perforation.', [R(src, 'Boxed Warning')])
OPI_CI = lambda src, extra_fa='', extra_en='': CI('ci', 'دپرسیون تنفسی قابل‌توجه؛ آسم حاد یا شدید بدون پایش؛ انسداد گوارشی یا ایلئوس فلجی؛ حساسیت' + extra_fa + '.', 'Significant respiratory depression; acute or severe asthma without monitoring; GI obstruction or paralytic ileus; hypersensitivity' + extra_en + '.', [R(src, '4')])
OPI_W = lambda src: W('هشدار جعبه‌ای: اعتیاد و سوءمصرف، دپرسیون تنفسی کشنده، مصرف تصادفی در کودک، سندرم ترک نوزادی، تداخل با بنزودیازپین‌ها و مهارکننده‌های CYP3A4. نالوکسان در دسترس باشد.', 'Boxed warning: addiction and misuse, life-threatening respiratory depression, accidental ingestion in children, neonatal opioid withdrawal, interactions with benzodiazepines and CYP3A4 inhibitors. Keep naloxone available.', [R(src, 'Boxed Warning'), R(src, '2.2')])

# --- pain ---
Ox = fda('oxycodone', 'FDA Oxycodone IR', 'Oxycodone hydrochloride tablets (SpecGx) — Prescribing Information', sid('oxycodone'))
drug('oxycodone', 'nervous-system', 'اکسی‌کدون', 'Oxycodone', T('آگونیست اپیوئیدی', 'Opioid agonist'), [{'name': 'Roxicodone', 'market': 'US'}], ['roxicodone', 'اکسی کدون', 'oxycodone'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (scored)', [R(Ox, '3')], scored=True) for m in (5, 10, 15, 20, 30)],
     [reg('pain', 'severe-pain', T('درد شدید (بیمار بدون مصرف قبلی اپیوئید) — ۵ تا ۱۵ mg هر ۴ تا ۶ ساعت در صورت نیاز', 'Severe pain (opioid-naive) — 5–15 mg every 4–6 h as needed'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 15, 'dosesPerDay': 4}, [R(Ox, '2.3')],
          notes=[note('کمترین دوز مؤثر در کوتاه‌ترین مدت. «هر ۴ تا ۶ ساعت در صورت نیاز»؛ عدد دفعات در ماشین‌حساب برای ۶ ساعت است. تبدیل از اپیوئید دیگر طبق برچسب.', 'Lowest effective dose for the shortest time. “Every 4–6 h as needed”; the calculator shows 6-hourly. Conversion from other opioids per label.', [R(Ox, '2.1'), R(Ox, '2.3')])])],
     [OPI_CI(Ox)], warn=[OPI_W(Ox)],
     exs=[ex('pain', 'tab-5', {'perDose': 5, 'upperPerDose': 15}, ageYears=40, weightKg=70)])

Mo = fda('morphine-tab', 'FDA Morphine IR tab', 'Morphine sulfate tablets 15/30 mg (SpecGx) — Prescribing Information', sid('morphine2'))
drug('morphine-oral', 'nervous-system', 'مورفین خوراکی (سریع‌رهش)', 'Morphine (oral, immediate-release)', T('آگونیست اپیوئیدی', 'Opioid agonist'), [{'name': 'MSIR', 'market': 'US'}], ['morphine tablet', 'مورفین خوراکی', 'قرص مورفین'],
     [tab('tab-15', 15, '15 mg tablet (scored)', [R(Mo, '3')], scored=True), tab('tab-30', 30, '30 mg tablet (scored)', [R(Mo, '3')], scored=True)],
     [reg('pain', 'severe-pain', T('درد شدید (بیمار بدون مصرف قبلی اپیوئید) — ۱۵ تا ۳۰ mg هر ۴ ساعت در صورت نیاز', 'Severe pain (opioid-naive) — 15–30 mg every 4 h as needed'), A18, 'fixed', {'perDose': 15, 'perDoseMax': 30, 'dosesPerDay': 6}, [R(Mo, '2.3')],
          notes=[note('کمترین دوز مؤثر در کوتاه‌ترین مدت. در کودک زیر ۵۰ kg قرص مناسب نیست.', 'Lowest effective dose for the shortest time. Tablets not suitable for children under 50 kg.', [R(Mo, '2.3')])])],
     [OPI_CI(Mo, '؛ MAOI همزمان یا ظرف ۱۴ روز', '; MAOIs now or within 14 days')], warn=[OPI_W(Mo)],
     exs=[ex('pain', 'tab-15', {'perDose': 15, 'upperPerDose': 30}, ageYears=60, weightKg=70)])

In = fda('indomethacin', 'FDA Indomethacin', 'Indomethacin capsules (Glenmark) — Prescribing Information', sid('indomethacin'))
drug('indomethacin', 'musculoskeletal', 'ایندومتاسین', 'Indomethacin', T('NSAID', 'NSAID'), [{'name': 'Indocin', 'market': 'US'}], ['indocin', 'ایندومتاسین', 'اندومتاسین'],
     [tab('cap-25', 25, '25 mg capsule', [R(In, '3')], per='capsule', form_='capsule'), tab('cap-50', 50, '50 mg capsule', [R(In, '3')], per='capsule', form_='capsule')],
     [reg('arthritis', 'rheumatoid-arthritis', T('آرتریت روماتوئید، استئوآرتریت، اسپوندیلیت — ۲۵ mg دو یا سه بار در روز', 'RA, OA, ankylosing spondylitis — 25 mg two or three times daily'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 3}, [R(In, '2.2')]),
      reg('gout', 'gout', T('حمله حاد نقرس — ۵۰ mg سه بار در روز', 'Acute gouty arthritis — 50 mg three times daily'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 3}, [R(In, '2.4')])],
     [NSAID_CI(In, '4')], warn=[NSAID_W(In)],
     exs=[ex('arthritis', 'cap-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('gout', 'cap-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=80)])

Pr = fda('piroxicam', 'FDA Piroxicam', 'Piroxicam capsules (Teva) — Prescribing Information', sid('piroxicam'))
drug('piroxicam', 'musculoskeletal', 'پیروکسیکام', 'Piroxicam', T('NSAID', 'NSAID'), [{'name': 'Feldene', 'market': 'US'}], ['feldene', 'فلدن', 'پیروکسیکام'],
     [tab('cap-10', 10, '10 mg capsule', [R(Pr, '3')], per='capsule', form_='capsule'), tab('cap-20', 20, '20 mg capsule', [R(Pr, '3')], per='capsule', form_='capsule')],
     [reg('arthritis', 'osteoarthritis', T('استئوآرتریت و آرتریت روماتوئید — ۲۰ mg یک بار در روز', 'OA and RA — 20 mg once daily'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Pr, '2')],
          notes=[note('در صورت تمایل می‌توان دوز روزانه را تقسیم کرد. سطح پایدار پس از ۷ تا ۱۲ روز.', 'The daily dose may be divided. Steady state after 7–12 days.', [R(Pr, '2')])])],
     [NSAID_CI(Pr, '4')], warn=[NSAID_W(Pr)],
     exs=[ex('arthritis', 'cap-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=75)])

Vg = fda('voltaren-gel', 'FDA Voltaren gel', 'Voltaren Arthritis Pain (diclofenac sodium 1%) gel — Drug Facts', sid('voltarengel'))
drug('diclofenac-gel', 'musculoskeletal', 'ژل دیکلوفناک ۱٪', 'Diclofenac gel 1%', T('NSAID موضعی', 'Topical NSAID'), [{'name': 'Voltaren Arthritis Pain', 'market': 'US'}], ['voltaren gel', 'ولتارن ژل', 'دیکلوفناک ژل'],
     [unitform('gel-1', 'gel', 'topical', 'Diclofenac sodium 1% gel (with dosing card)', [R(Vg, 'Package label')])],
     [reg('oa', 'osteoarthritis', T('درد آرتروز دست، مچ، آرنج، پا، مچ پا یا زانو — ۴ بار در روز', 'Arthritis pain of hand, wrist, elbow, foot, ankle or knee — 4 times daily'), A18, 'notCalculated',
          {'reason': T('هر ناحیه بالاتنه (دست، مچ، آرنج): ۲ گرم؛ هر ناحیه پایین‌تنه (پا، مچ پا، زانو): ۴ گرم؛ ۴ بار در روز با کارت اندازه‌گیری. همزمان بیش از ۲ ناحیه نه. تا ۲۱ روز. برای کشیدگی، پیچ‌خوردگی و ضرب‌دیدگی مؤثر نیست.',
                       'Each upper-body area (hand, wrist, elbow): 2 g; each lower-body area (foot, ankle, knee): 4 g; 4 times daily with the dosing card. Not more than 2 areas at once. Up to 21 days. Not effective for strains, sprains or bruises.')}, [R(Vg, 'Directions'), R(Vg, 'Uses')])],
     [CI('dnu', 'سابقه واکنش آلرژیک به مسکن یا تب‌بر؛ درست پیش یا پس از جراحی قلب.', 'Prior allergic reaction to any pain reliever or fever reducer; right before or after heart surgery.', [R(Vg, 'Do not use')])],
     warn=[W('حساسیت شدید (به‌ویژه در حساسیت به آسپرین)، آسیب کبد با مصرف بیش از حد، و خونریزی معده.', 'Severe allergy (especially with aspirin allergy), liver damage with overuse, and stomach bleeding.', [R(Vg, 'Warnings')])])

Ld = fda('lidoderm', 'FDA Lidoderm', 'Lidoderm (lidocaine patch 5%) — Prescribing Information', sid('lidoderm'))
drug('lidocaine-patch', 'nervous-system', 'چسب لیدوکائین ۵٪', 'Lidocaine patch 5%', T('بی‌حس‌کننده موضعی', 'Local anaesthetic'), [{'name': 'Lidoderm', 'market': 'US'}], ['lidoderm', 'versatis', 'چسب لیدوکائین'],
     [unitform('patch-5', 'cream', 'topical', 'Lidocaine 5% patch (700 mg)', [R(Ld, 'How Supplied')], unit='application', per='application')],
     [reg('phn', 'postherpetic-neuralgia', T('نورالژی پس از زونا — تا ۳ چسب حداکثر ۱۲ ساعت در ۲۴ ساعت', 'Postherpetic neuralgia — up to 3 patches for max 12 h in 24 h'), A18, 'notCalculated',
          {'reason': T('روی پوست سالم و دردناک‌ترین ناحیه؛ حداکثر ۳ چسب، فقط یک بار تا ۱۲ ساعت در هر ۲۴ ساعت. می‌توان چسب را برید. در بیمار ناتوان یا با دفع مختل، ناحیه کوچک‌تر.', 'On intact skin over the most painful area; max 3 patches, once for up to 12 h in any 24 h. Patches may be cut. Smaller areas in debilitated patients or impaired elimination.')}, [R(Ld, 'Dosage and Administration')])],
     [CI('amide', 'سابقه حساسیت به بی‌حس‌کننده‌های آمیدی یا اجزای چسب.', 'History of sensitivity to amide local anaesthetics or any component.', [R(Ld, 'Contraindications')])],
     warn=[W('خطر مت‌هموگلوبینمی (به‌ویژه در کمبود G6PD و شیرخوار زیر ۶ ماه).', 'Risk of methaemoglobinaemia (especially with G6PD deficiency and infants under 6 months).', [R(Ld, 'Warnings')])])

# --- rheumatology and bone ---
Mx = fda('methotrexate-tab', 'FDA Methotrexate tab', 'Methotrexate tablets 2.5 mg (Alembic) — Prescribing Information', sid('mtx'))
WEEKLY = 'هفته‌ای یک بار — نه روزانه. مصرف روزانه به اشتباه موجب مرگ شده است. '
WEEKLY_EN = 'ONCE WEEKLY — not daily. Daily dosing by mistake has caused deaths. '
drug('methotrexate', 'antineoplastic-immunomodulating', 'متوترکسات (خوراکی)', 'Methotrexate (oral)', T('آنتی‌متابولیت / DMARD', 'Antimetabolite / DMARD'), [{'name': 'Trexall', 'market': 'US'}], ['trexall', 'متوترکسات', 'MTX'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet (scored)', [R(Mx, '3')], scored=True)],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — شروع ۷٫۵ mg هفته‌ای یک بار', 'Rheumatoid arthritis — start 7.5 mg once weekly'), A18, 'notCalculated',
          {'reason': T(WEEKLY + 'شروع ۷٫۵ mg خوراکی هفته‌ای یک بار، افزایش تا پاسخ مطلوب؛ بالای ۲۰ mg در هفته خطر عوارض جدی (سرکوب مغز استخوان) بیشتر است.', WEEKLY_EN + 'Start 7.5 mg orally once weekly, escalate to response; above 20 mg weekly increases serious toxicity (myelosuppression).')}, [R(Mx, '2.3'), R(Mx, '2.1')]),
      reg('pjia', 'juvenile-arthritis', T('آرتریت ایدیوپاتیک نوجوانان چندمفصلی — شروع ۱۰ mg/m² هفته‌ای یک بار', 'Polyarticular JIA — start 10 mg/m² once weekly'), {'maxAge': age(18, 'year')}, 'notCalculated',
          {'reason': T(WEEKLY + 'شروع ۱۰ mg/m² خوراکی هفته‌ای یک بار، تنظیم تا پاسخ مطلوب.', WEEKLY_EN + 'Start 10 mg/m² orally once weekly; adjust to response.')}, [R(Mx, '2.4'), R(Mx, '2')]),
      reg('psoriasis', 'psoriasis', T('پسوریازیس شدید — ۱۰ تا ۲۵ mg هفته‌ای یک بار', 'Severe psoriasis — 10–25 mg once weekly'), A18, 'notCalculated',
          {'reason': T(WEEKLY + '۱۰ تا ۲۵ mg خوراکی هفته‌ای یک بار تا پاسخ کافی.', WEEKLY_EN + '10–25 mg orally once weekly until adequate response.')}, [R(Mx, '2.5'), R(Mx, '2')])],
     [CI('preg', 'بارداری (برای بیماری‌های غیرسرطانی)؛ سابقه حساسیت شدید به متوترکسات.', 'Pregnancy (non-neoplastic diseases); history of severe hypersensitivity to methotrexate.', [R(Mx, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی، واکنش حساسیتی، عوارض جدی (مغز استخوان، کبد، ریه، کلیه) و خطای دارویی؛ پیش از شروع وضعیت بارداری بررسی شود.', 'Boxed warning: embryo-fetal toxicity, hypersensitivity, serious adverse reactions (marrow, liver, lung, kidney) and medication errors; verify pregnancy status before starting.', [R(Mx, 'Boxed Warning')])])

Sf = fda('sulfasalazine', 'FDA Sulfasalazine DR', 'Sulfasalazine delayed-release tablets (Mylan) — Prescribing Information', sid('sulfasalazine')); d = R(Sf, 'Dosage and Administration')
drug('sulfasalazine', 'alimentary-metabolism', 'سولفاسالازین', 'Sulfasalazine', T('آمینوسالیسیلات / DMARD', 'Aminosalicylate / DMARD'), [{'name': 'Azulfidine EN-tabs', 'market': 'US'}], ['azulfidine', 'salazopyrin', 'سولفاسالازین'],
     [tab('tab-500', 500, '500 mg delayed-release tablet', [R(Sf, 'How Supplied')])],
     [reg('uc-adult', 'ulcerative-colitis', T('کولیت اولسروز — بزرگسال: ۳ تا ۴ g در روز در دوزهای مساوی', 'Ulcerative colitis — adult: 3–4 g/day in divided doses'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 3}, [d], limits={'maxPerDay': 4000, 'refs': [d]},
          notes=[note('فاصله دوزها حداکثر ۸ ساعت، پس از غذا، قرص کامل. می‌توان با ۱ تا ۲ g در روز شروع کرد. نگهدارنده: ۲ g در روز.', 'Dose intervals ≤8 h, after meals, swallow whole. May start at 1–2 g/day. Maintenance: 2 g/day.', [d])]),
      reg('uc-child', 'ulcerative-colitis', T('کولیت اولسروز — کودک ۶ سال به بالا: ۴۰ تا ۶۰ mg/kg/روز در ۳ تا ۶ دوز', 'Ulcerative colitis — child ≥6 y: 40–60 mg/kg/day in 3–6 doses'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 40, 'perKgPerDayMax': 60, 'dividedDoses': 3}, [d],
          notes=[note('نگهدارنده: ۳۰ mg/kg/روز در ۴ دوز.', 'Maintenance: 30 mg/kg/day in 4 doses.', [d])]),
      reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — ۲ g در روز در ۲ دوز', 'Rheumatoid arthritis — 2 g/day in 2 doses'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 2}, [d],
          notes=[note('بهتر است با ۰٫۵ تا ۱ g در روز شروع و تدریجی افزایش. پاسخ معمولاً پس از ۴ تا ۱۲ هفته.', 'Start at 0.5–1 g/day and increase gradually. Response usually after 4–12 weeks.', [d])])],
     [CI('ci', 'حساسیت به سولفاسالازین، سولفونامیدها یا سالیسیلات‌ها؛ انسداد روده یا ادراری؛ پورفیری.', 'Hypersensitivity to sulfasalazine, sulfonamides or salicylates; intestinal or urinary obstruction; porphyria.', [R(Sf, 'Contraindications')])],
     exs=[ex('uc-adult', 'tab-500', {'perDose': 1000, 'tabletsPerDoseRounded': 2}, ageYears=40, weightKg=70), ex('uc-child', 'tab-500', {'perDose': 1000, 'upperPerDose': 1500}, ageYears=15, weightKg=75),
          ex('ra', 'tab-500', {'perDose': 1000, 'tabletsPerDoseRounded': 2}, ageYears=50, weightKg=70)])

Lf = fda('leflunomide', 'FDA Leflunomide', 'Leflunomide tablets (Burel) — Prescribing Information', sid('leflunomide'))
drug('leflunomide', 'antineoplastic-immunomodulating', 'لفلونوماید', 'Leflunomide', T('DMARD (مهارکننده سنتز پیریمیدین)', 'DMARD (pyrimidine synthesis inhibitor)'), [{'name': 'Arava', 'market': 'US'}], ['arava', 'آراوا', 'لفلونوماید'],
     [tab('tab-10', 10, '10 mg tablet', [R(Lf, '3')]), tab('tab-20', 20, '20 mg tablet', [R(Lf, '3')])],
     [reg('load', 'rheumatoid-arthritis', T('آرتریت روماتوئید — بارگذاری ۱۰۰ mg روزانه، ۳ روز (کم‌خطر برای کبد و مغز استخوان)', 'Rheumatoid arthritis — loading 100 mg daily for 3 days (low hepatic/marrow risk)'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Lf, '2.1')], dur={'min': 3, 'max': 3}),
      reg('maint', 'rheumatoid-arthritis', T('آرتریت روماتوئید — نگهدارنده ۲۰ mg یک بار در روز (در عدم تحمل ۱۰ mg)', 'Rheumatoid arthritis — maintenance 20 mg once daily (10 mg if not tolerated)'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Lf, '2.1')],
          notes=[note('پیش از شروع: غربال سل، تست بارداری، فشار خون و آزمایش‌ها.', 'Before starting: TB screening, pregnancy test, blood pressure and labs.', [R(Lf, '2.2')])])],
     [CI('ci', 'بارداری؛ نارسایی شدید کبد؛ حساسیت؛ مصرف همزمان تری‌فلونوماید.', 'Pregnancy; severe hepatic impairment; hypersensitivity; concomitant teriflunomide.', [R(Lf, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی (پیش از شروع بارداری رد شود) و سمیت کبدی.', 'Boxed warning: embryo-fetal toxicity (exclude pregnancy first) and hepatotoxicity.', [R(Lf, 'Boxed Warning')])],
     exs=[ex('load', 'tab-20', {'perDose': 100, 'tabletsPerDoseRounded': 5}, ageYears=50, weightKg=70), ex('maint', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70)])

Fb = fda('febuxostat', 'FDA Febuxostat', 'Febuxostat tablets (HEC) — Prescribing Information', sid('febuxostat'))
drug('febuxostat', 'musculoskeletal', 'فبوکسوستات', 'Febuxostat', T('مهارکننده گزانتین اکسیداز', 'Xanthine oxidase inhibitor'), [{'name': 'Uloric', 'market': 'US'}], ['uloric', 'adenuric', 'فبوکسوستات'],
     [tab('tab-40', 40, '40 mg tablet', [R(Fb, '3')]), tab('tab-80', 80, '80 mg tablet', [R(Fb, '3')])],
     [reg('gout', 'gout', T('هیپراوریسمی مزمن در نقرس — شروع ۴۰ mg یک بار در روز (تا ۸۰ mg)', 'Chronic hyperuricaemia in gout — start 40 mg once daily (up to 80 mg)'), A18, 'fixed', {'perDose': 40, 'dosesPerDay': 1}, [R(Fb, '2.1')], limits={'maxPerDose': 80, 'refs': [R(Fb, '2.1')]},
          notes=[note('اگر پس از ۲ هفته اسید اوریک زیر ۶ نشد، ۸۰ mg. نارسایی شدید کلیه: حداکثر ۴۰ mg. در شروع درمان پیشگیری از حمله (NSAID یا کلشی‌سین).', 'If uric acid is not <6 after 2 weeks, 80 mg. Severe renal impairment: max 40 mg. Flare prophylaxis (NSAID or colchicine) when starting.', [R(Fb, '2')])])],
     [CI('ci', 'مصرف همزمان آزاتیوپرین یا مرکاپتوپورین.', 'Concomitant azathioprine or mercaptopurine.', [R(Fb, '4')])],
     warn=[W('هشدار جعبه‌ای: مرگ قلبی‌عروقی در بیماران نقرس با بیماری قلبی بیشتر از آلوپورینول؛ فقط اگر آلوپورینول مؤثر یا قابل تحمل نیست.', 'Boxed warning: higher cardiovascular death than allopurinol in gout patients with CV disease; use only when allopurinol fails or is not tolerated.', [R(Fb, 'Boxed Warning')])],
     inter=[IA('azathioprine', 'آزاتیوپرین و مرکاپتوپورین — ممنوع (افزایش سطح و سمیت).', 'Azathioprine and mercaptopurine — contraindicated (raised levels and toxicity).', [R(Fb, '4')])],
     exs=[ex('gout', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=85)])

Rs = fda('risedronate', 'FDA Risedronate DR', 'Risedronate sodium delayed-release tablets 35 mg (Mylan) — Prescribing Information', sid('risedronate'))
drug('risedronate', 'musculoskeletal', 'ریزدرونات', 'Risedronate', T('بیس‌فسفونات', 'Bisphosphonate'), [{'name': 'Atelvia', 'market': 'US'}], ['atelvia', 'actonel', 'آکتونل', 'ریزدرونات'],
     [tab('tab-35', 35, '35 mg delayed-release tablet', [R(Rs, '3')])],
     [reg('pmo', 'osteoporosis', T('پوکی استخوان یائسگی — ۳۵ mg هفته‌ای یک بار', 'Postmenopausal osteoporosis — 35 mg once weekly'), A18, 'notCalculated',
          {'reason': T('هفته‌ای یک بار (نه روزانه): یک قرص ۳۵ mg صبح بلافاصله پس از صبحانه با دست‌کم ۱۲۰ mL آب؛ ۳۰ دقیقه دراز نکشد. کلسیم و ویتامین D در صورت دریافت ناکافی.', 'Once WEEKLY (not daily): one 35 mg tablet in the morning right after breakfast with at least 4 oz water; stay upright 30 min. Calcium and vitamin D if intake is inadequate.')}, [R(Rs, '2.1'), R(Rs, '2.2')])],
     [CI('ci', 'اختلال مری که تخلیه را کند می‌کند (تنگی، آشالازی)؛ ناتوانی در نشستن یا ایستادن ۳۰ دقیقه؛ هیپوکلسمی؛ حساسیت.', 'Oesophageal abnormalities delaying emptying (stricture, achalasia); inability to stay upright 30 min; hypocalcaemia; hypersensitivity.', [R(Rs, '4')])])

Zl = fda('reclast', 'FDA Reclast', 'Reclast (zoledronic acid) 5 mg/100 mL injection — Prescribing Information', sid('reclast'))
drug('zoledronic-acid', 'musculoskeletal', 'زولدرونیک اسید (سالانه)', 'Zoledronic acid (yearly)', T('بیس‌فسفونات وریدی', 'IV bisphosphonate'), [{'name': 'Reclast', 'market': 'US'}], ['reclast', 'aclasta', 'آکلاستا', 'زولدرونیک اسید'],
     [form('bag-5', 'injection', 'iv', '5 mg/100 mL ready-to-infuse solution', 5, 'mg', [R(Zl, '3')], vol=100)],
     [reg('pmo', 'osteoporosis', T('پوکی استخوان یائسگی — ۵ mg وریدی سالی یک بار', 'Postmenopausal osteoporosis — 5 mg IV once a year'), A18, 'notCalculated',
          {'reason': T('درمان: ۵ mg انفوزیون وریدی سالی یک بار در دست‌کم ۱۵ دقیقه. پیشگیری: ۵ mg هر ۲ سال. پیش از تزریق آب کافی؛ کراتینین بررسی شود.', 'Treatment: 5 mg IV infusion once a year over at least 15 min. Prevention: 5 mg every 2 years. Hydrate before; check creatinine.')}, [R(Zl, '2.2'), R(Zl, '2.3')])],
     [CI('ci', 'هیپوکلسمی؛ CrCl زیر ۳۵ یا آسیب حاد کلیه؛ حساسیت.', 'Hypocalcaemia; CrCl <35 or acute renal impairment; hypersensitivity.', [R(Zl, '4')])])

Pl = fda('prolia', 'FDA Prolia', 'Prolia (denosumab) injection — Prescribing Information', sid('prolia'))
drug('denosumab', 'musculoskeletal', 'دنوزوماب (پرولیا)', 'Denosumab (Prolia)', T('آنتی‌بادی ضد RANKL', 'Anti-RANKL antibody'), [{'name': 'Prolia', 'market': 'US'}], ['prolia', 'پرولیا', 'دنوزوماب'],
     [liquid('syr-60', 60, 1, '60 mg/mL prefilled syringe', [R(Pl, '3')], form_='injection', route='sc')],
     [reg('pmo', 'osteoporosis', T('پوکی استخوان — ۶۰ mg زیرجلدی هر ۶ ماه', 'Osteoporosis — 60 mg SC every 6 months'), A18, 'notCalculated',
          {'reason': T('۶۰ mg زیرجلدی یک بار هر ۶ ماه توسط کادر درمان. کلسیم ۱۰۰۰ mg و ویتامین D دست‌کم ۴۰۰ واحد روزانه. پیش از شروع تست بارداری؛ در eGFR زیر ۳۰ ابتدا CKD-MBD بررسی شود.', '60 mg SC once every 6 months by a healthcare provider. Calcium 1,000 mg and vitamin D ≥400 IU daily. Pregnancy test before starting; with eGFR <30 evaluate CKD-MBD first.')}, [R(Pl, '2.3'), R(Pl, '2.1'), R(Pl, '2.2')])],
     [CI('ci', 'هیپوکلسمی (پیش از شروع اصلاح شود)؛ بارداری؛ حساسیت سیستمیک.', 'Hypocalcaemia (correct before starting); pregnancy; systemic hypersensitivity.', [R(Pl, '4')])],
     warn=[W('هشدار جعبه‌ای: هیپوکلسمی شدید در بیماری پیشرفته کلیه (eGFR زیر ۳۰ یا دیالیز).', 'Boxed warning: severe hypocalcaemia in advanced CKD (eGFR <30 or dialysis).', [R(Pl, 'Boxed Warning')])])

Rx = fda('raloxifene', 'FDA Raloxifene', 'Raloxifene hydrochloride tablets (Teva) — Prescribing Information', sid('raloxifene'))
drug('raloxifene', 'genitourinary-sex-hormones', 'رالوکسیفن', 'Raloxifene', T('تعدیل‌کننده انتخابی گیرنده استروژن (SERM)', 'Selective oestrogen receptor modulator'), [{'name': 'Evista', 'market': 'US'}], ['evista', 'اویستا', 'رالوکسیفن'],
     [tab('tab-60', 60, '60 mg tablet', [R(Rx, '3')])],
     [reg('pmo', 'osteoporosis', T('پوکی استخوان یائسگی (درمان یا پیشگیری) — ۶۰ mg یک بار در روز', 'Postmenopausal osteoporosis (treatment or prevention) — 60 mg once daily'), A18, 'fixed', {'perDose': 60, 'dosesPerDay': 1}, [R(Rx, '2.1')],
          notes=[note('بدون توجه به غذا. کلسیم و ویتامین D در صورت دریافت ناکافی.', 'With or without food. Calcium and vitamin D if intake is inadequate.', [R(Rx, '2.1'), R(Rx, '2.2')])])],
     [CI('ci', 'ترومبوآمبولی وریدی فعال یا قبلی (DVT، PE، ترومبوز ورید شبکیه)؛ بارداری.', 'Active or past VTE (DVT, PE, retinal vein thrombosis); pregnancy.', [R(Rx, '4')])],
     warn=[W('هشدار جعبه‌ای: افزایش خطر ترومبوآمبولی وریدی و مرگ ناشی از سکته.', 'Boxed warning: increased risk of venous thromboembolism and death from stroke.', [R(Rx, 'Boxed Warning')])],
     exs=[ex('pmo', 'tab-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=65)])

# --- GI ---
Sc = fda('carafate', 'FDA Carafate', 'Carafate (sucralfate) 1 g tablets — Prescribing Information', sid('sucralfate')); d = R(Sc, 'Dosage and Administration')
drug('sucralfate', 'alimentary-metabolism', 'سوکرالفات', 'Sucralfate', T('محافظ مخاط', 'Mucosal protectant'), [{'name': 'Carafate', 'market': 'US'}], ['carafate', 'سوکرالفات'],
     [tab('tab-1g', 1000, '1 g tablet', [R(Sc, 'How Supplied')])],
     [reg('du', 'peptic-ulcer-disease', T('زخم فعال دوازدهه — ۱ g چهار بار در روز با معده خالی، ۴ تا ۸ هفته', 'Active duodenal ulcer — 1 g four times daily on an empty stomach, 4–8 weeks'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 4}, [d],
          notes=[note('آنتی‌اسید نیم ساعت قبل یا بعد از سوکرالفات نه.', 'No antacid within 30 min before or after sucralfate.', [d])]),
      reg('maint', 'peptic-ulcer-disease', T('نگهدارنده پس از بهبود زخم دوازدهه — ۱ g دو بار در روز', 'Maintenance after duodenal ulcer healing — 1 g twice daily'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 2}, [d])],
     exs=[ex('du', 'tab-1g', {'perDose': 1000, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('maint', 'tab-1g', {'perDose': 1000, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Mg = fda('motegrity', 'FDA Motegrity', 'Motegrity (prucalopride) tablets — Prescribing Information', sid('motegrity'))
drug('prucalopride', 'alimentary-metabolism', 'پروکالوپراید', 'Prucalopride', T('آگونیست گیرنده 5-HT4', '5-HT4 receptor agonist'), [{'name': 'Motegrity', 'market': 'US'}], ['motegrity', 'resolor', 'پروکالوپراید'],
     [tab('tab-1', 1, '1 mg tablet', [R(Mg, '3')]), tab('tab-2', 2, '2 mg tablet', [R(Mg, '3')])],
     [reg('cic', 'chronic-idiopathic-constipation', T('یبوست مزمن ایدیوپاتیک — ۲ mg یک بار در روز', 'Chronic idiopathic constipation — 2 mg once daily'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Mg, '2')],
          notes=[note('CrCl زیر ۳۰: ۱ mg یک بار در روز.', 'CrCl <30: 1 mg once daily.', [R(Mg, '2')])])],
     [CI('ci', 'حساسیت؛ سوراخ یا انسداد روده، ایلئوس انسدادی، بیماری التهابی شدید روده (کرون، کولیت، مگاکولون توکسیک).', 'Hypersensitivity; intestinal perforation or obstruction, obstructive ileus, severe IBD (Crohn’s, colitis, toxic megacolon).', [R(Mg, '4')])],
     exs=[ex('cic', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=65)])

Lz = fda('linzess', 'FDA Linzess', 'Linzess (linaclotide) capsules — Prescribing Information', sid('linzess')); d = R(Lz, '2.1')
lcap = lambda m: form(f'cap-{m}', 'capsule', 'oral', f'{m} mcg capsule', m, 'mcg', [R(Lz, '3')], per='capsule')
drug('linaclotide', 'alimentary-metabolism', 'لیناکلوتاید', 'Linaclotide', T('آگونیست گوانیلات سیکلاز C', 'Guanylate cyclase-C agonist'), [{'name': 'Linzess', 'market': 'US'}], ['linzess', 'constella', 'لیناکلوتاید'],
     [lcap(72), lcap(145), lcap(290)],
     [reg('ibsc', 'ibs', T('سندرم روده تحریک‌پذیر با یبوست (IBS-C) — بزرگسال: ۲۹۰ mcg یک بار در روز', 'IBS with constipation — adult: 290 mcg once daily'), A18, 'fixed', {'perDose': 290, 'dosesPerDay': 1}, [d], unit='mcg', allowed=['cap-290'],
          notes=[note('ناشتا، دست‌کم ۳۰ دقیقه پیش از غذا، کپسول جویده نشود.', 'On an empty stomach at least 30 min before a meal; do not crush or chew.', [d, R(Lz, '2.2')])]),
      reg('cic', 'chronic-idiopathic-constipation', T('یبوست مزمن ایدیوپاتیک — بزرگسال: ۱۴۵ mcg (یا ۷۲ mcg) یک بار در روز', 'Chronic idiopathic constipation — adult: 145 mcg (or 72 mcg) once daily'), A18, 'fixed', {'perDose': 145, 'dosesPerDay': 1}, [d], unit='mcg', allowed=['cap-145']),
      reg('ibsc-child', 'ibs', T('IBS-C — کودک ۷ سال به بالا: ۱۴۵ mcg یک بار در روز', 'IBS-C — child ≥7 y: 145 mcg once daily'), {'minAge': age(7, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 145, 'dosesPerDay': 1}, [d], unit='mcg', allowed=['cap-145']),
      reg('fc-child', 'constipation', T('یبوست عملکردی — کودک ۲ سال به بالا: ۷۲ mcg یک بار در روز', 'Functional constipation — child ≥2 y: 72 mcg once daily'), {'minAge': age(2, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 72, 'dosesPerDay': 1}, [d], unit='mcg', allowed=['cap-72'])],
     [CI('lt2', 'زیر ۲ سال (خطر کم‌آبی شدید).', 'Under 2 years (risk of serious dehydration).', [R(Lz, '4')], rule={'maxAge': age(2, 'year')}),
      CI('obst', 'انسداد مکانیکی گوارشی شناخته‌شده یا مشکوک.', 'Known or suspected mechanical GI obstruction.', [R(Lz, '4')])],
     exs=[ex('ibsc', 'cap-290', {'perDose': 290, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=60), ex('cic', 'cap-145', {'perDose': 145, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=60),
          ex('ibsc-child', 'cap-145', {'perDose': 145, 'tabletsPerDoseRounded': 1}, ageYears=10, weightKg=30), ex('fc-child', 'cap-72', {'perDose': 72, 'tabletsPerDoseRounded': 1}, ageYears=4, weightKg=16)])

Bd = fda('budesonide-ec', 'FDA Budesonide EC', 'Budesonide delayed-release capsules 3 mg (Padagis) — Prescribing Information', sid('entocort'))
drug('budesonide-ec', 'alimentary-metabolism', 'بودزوناید خوراکی (کرون)', 'Budesonide oral (Crohn’s)', T('کورتیکواستروئید با اثر موضعی روده', 'Gut-acting corticosteroid'), [{'name': 'Entocort EC', 'market': 'US'}], ['entocort', 'budenofalk', 'بودزوناید خوراکی'],
     [tab('cap-3', 3, '3 mg delayed-release capsule', [R(Bd, '3')], per='capsule', form_='capsule')],
     [reg('active', 'crohns', T('کرون خفیف تا متوسط فعال — بزرگسال: ۹ mg صبح‌ها تا ۸ هفته', 'Mild–moderate active Crohn’s — adult: 9 mg every morning up to 8 weeks'), A18, 'fixed', {'perDose': 9, 'dosesPerDay': 1}, [R(Bd, '2.2')], dur={'min': 56, 'max': 56},
          notes=[note('کپسول کامل بلعیده شود؛ آب گریپ‌فروت نه. نگهدارنده بهبودی: ۶ mg روزانه تا ۳ ماه.', 'Swallow whole; avoid grapefruit juice. Maintenance of remission: 6 mg daily up to 3 months.', [R(Bd, '2.1'), R(Bd, '2.3')])]),
      reg('child', 'crohns', T('کرون فعال — کودک ۸ تا ۱۷ سال بالای ۲۵ kg: ۹ mg تا ۸ هفته سپس ۶ mg دو هفته', 'Active Crohn’s — child 8–17 y >25 kg: 9 mg up to 8 weeks, then 6 mg for 2 weeks'), {'minAge': age(8, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 25.01}, 'fixed', {'perDose': 9, 'dosesPerDay': 1}, [R(Bd, '2.2')])],
     [CI('hyper', 'حساسیت به بودزوناید.', 'Hypersensitivity to budesonide.', [R(Bd, '4')])],
     exs=[ex('active', 'cap-3', {'perDose': 9, 'tabletsPerDoseRounded': 3}, ageYears=30, weightKg=65), ex('child', 'cap-3', {'perDose': 9, 'tabletsPerDoseRounded': 3}, ageYears=12, weightKg=40)])

Az = fda('azathioprine', 'FDA Azathioprine', 'Azathioprine tablets 50 mg (Glenmark) — Prescribing Information', sid('azathioprine')); d = R(Az, 'Dosage and Administration — Rheumatoid Arthritis')
drug('azathioprine', 'antineoplastic-immunomodulating', 'آزاتیوپرین', 'Azathioprine', T('سرکوب‌کننده ایمنی (آنتی‌متابولیت)', 'Immunosuppressant (antimetabolite)'), [{'name': 'Imuran', 'market': 'US'}], ['imuran', 'ایموران', 'آزاتیوپرین'],
     [tab('tab-50', 50, '50 mg tablet (scored)', [R(Az, 'How Supplied')], scored=True)],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید — شروع حدود ۱ mg/kg روزانه (۵۰ تا ۱۰۰ mg)', 'Rheumatoid arthritis — start about 1 mg/kg daily (50–100 mg)'), A18, 'weightBased', {'perKgPerDay': 1, 'dividedDoses': 1}, [d],
          limits={'maxPerKgPerDay': 2.5, 'refs': [d]},
          notes=[note('یک‌جا یا دو بار در روز. از هفته ۶ تا ۸ هر ۴ هفته ۰٫۵ mg/kg افزایش تا حداکثر ۲٫۵ mg/kg. پیش از شروع TPMT و NUDT15 بررسی شود (کمبود ← کاهش شدید دوز).', 'Single or twice-daily. From week 6–8 increase 0.5 mg/kg every 4 weeks up to 2.5 mg/kg. Test TPMT and NUDT15 before starting (deficiency → major dose reduction).', [d, R(Az, 'Dosage and Administration')])])],
     [CI('ci', 'حساسیت؛ آرتریت روماتوئید در بارداری؛ RA با درمان قبلی آلکیله‌کننده (خطر بدخیمی).', 'Hypersensitivity; rheumatoid arthritis in pregnancy; RA previously treated with alkylating agents (malignancy risk).', [R(Az, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: بدخیمی (لنفوم و سرطان پوست) با سرکوب ایمنی مزمن.', 'Boxed warning: malignancy (lymphoma and skin cancer) with chronic immunosuppression.', [R(Az, 'Boxed Warning')])],
     inter=[IA('xo', 'آلوپورینول و فبوکسوستات: افزایش شدید سمیت (فبوکسوستات ممنوع).', 'Allopurinol and febuxostat: markedly increased toxicity (febuxostat contraindicated).', [R(Az, 'Drug Interactions')])],
     exs=[ex('ra', 'tab-50', {'perDose': 75, 'tabletsPerDoseRounded': 1.5}, ageYears=50, weightKg=75)])

Vq = fda('voquezna', 'FDA Voquezna', 'Voquezna (vonoprazan) tablets — Prescribing Information', sid('voquezna')); d = R(Vq, '2.1')
drug('vonoprazan', 'alimentary-metabolism', 'وونوپرازان', 'Vonoprazan', T('مسدودکننده رقابتی پمپ اسید (P-CAB)', 'Potassium-competitive acid blocker'), [{'name': 'Voquezna', 'market': 'US'}], ['voquezna', 'takecab', 'وونوپرازان'],
     [tab('tab-10', 10, '10 mg tablet', [R(Vq, '3')]), tab('tab-20', 20, '20 mg tablet', [R(Vq, '3')])],
     [reg('ee', 'erosive-esophagitis', T('ازوفاژیت اروزیو — ۲۰ mg یک بار در روز، ۸ هفته', 'Erosive oesophagitis healing — 20 mg once daily, 8 weeks'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [d], dur={'min': 56, 'max': 56},
          notes=[note('نگهدارنده: ۱۰ mg یک بار در روز تا ۶ ماه. GFR زیر ۳۰: ۱۰ mg.', 'Maintenance: 10 mg once daily up to 6 months. GFR <30: 10 mg.', [d, R(Vq, '2.2, Table 1')])]),
      reg('nerd', 'gerd', T('سوزش سر دل در ریفلاکس غیراروزیو — ۱۰ mg یک بار در روز، ۴ هفته', 'Heartburn in non-erosive GERD — 10 mg once daily, 4 weeks'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [d], dur={'min': 28, 'max': 28}),
      reg('hp', 'h-pylori', T('هلیکوباکتر پیلوری — ۲۰ mg دو بار در روز، ۱۴ روز (همراه آموکسی‌سیلین ± کلاریترومایسین)', 'H. pylori — 20 mg twice daily, 14 days (with amoxicillin ± clarithromycin)'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 2}, [d], dur={'min': 14, 'max': 14},
          notes=[note('سه‌گانه: + آموکسی‌سیلین ۱۰۰۰ mg و کلاریترومایسین ۵۰۰ mg هر کدام دو بار در روز. دوگانه: + آموکسی‌سیلین ۱۰۰۰ mg سه بار در روز. GFR زیر ۳۰ توصیه نمی‌شود.', 'Triple: + amoxicillin 1,000 mg and clarithromycin 500 mg each twice daily. Dual: + amoxicillin 1,000 mg three times daily. Not recommended with GFR <30.', [d, R(Vq, '2.2, Table 2')])])],
     [CI('ci', 'حساسیت به وونوپرازان؛ داروهای حاوی ریلپیویرین.', 'Hypersensitivity to vonoprazan; rilpivirine-containing products.', [R(Vq, '4')])],
     exs=[ex('ee', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=75), ex('nerd', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=75),
          ex('hp', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=75)])

# --- skin ---
Rt = fda('retin-a-micro', 'FDA Retin-A Micro', 'Retin-A Micro (tretinoin) gel — Prescribing Information', sid('tretinoin'))
drug('tretinoin-topical', 'dermatology', 'ترتینوئین موضعی', 'Tretinoin (topical)', T('رتینوئید موضعی', 'Topical retinoid'), [{'name': 'Retin-A Micro', 'market': 'US'}], ['retin-a', 'رتین ای', 'ترتینوئین', 'ترتینوئین کرم'],
     [unitform('gel', 'gel', 'topical', 'Tretinoin gel 0.04%, 0.06%, 0.08% or 0.1%', [R(Rt, '3')])],
     [reg('acne', 'acne', T('آکنه — لایه نازک یک بار در روز، عصر', 'Acne — thin layer once daily in the evening'), {'minAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('پس از شستن ملایم و خشک کردن، لایه نازک روی کل ناحیه آکنه یک بار در روز عصر؛ دور از چشم، دهان، چین‌های بینی و مخاط. بیش از لایه نازک نه. بهبود از ۲ هفته به بعد.', 'After gentle cleansing and drying, a thin layer over the whole acne area once daily in the evening; away from eyes, mouth, nasal creases and mucosa. No more than a thin layer. Improvement from about 2 weeks.')}, [R(Rt, '2')])],
     warn=[W('تحریک موضعی (خشکی، قرمزی، پوسته‌ریزی، سوزش)؛ روی پوست اگزمایی یا در هوای خیلی سرد یا بادی مصرف نشود؛ از آفتاب پرهیز.', 'Local irritation (dryness, redness, peeling, burning); avoid eczematous skin and extreme wind or cold; avoid sun.', [R(Rt, '5')])])

Tl = fda('triluma', 'FDA Tri-Luma', 'Tri-Luma (fluocinolone/hydroquinone/tretinoin) cream — Prescribing Information', sid('triluma'))
drug('tri-luma', 'dermatology', 'کرم سه‌گانه ملاسما (فلوسینولون + هیدروکینون + ترتینوئین)', 'Fluocinolone + hydroquinone + tretinoin cream', T('ترکیب ضدلک', 'Depigmenting combination'), [{'name': 'Tri-Luma', 'market': 'US'}], ['tri-luma', 'تری لوما', 'هیدروکینون', 'کرم ضد لک'],
     [unitform('cream', 'cream', 'topical', 'Fluocinolone 0.01% / hydroquinone 4% / tretinoin 0.05% cream', [R(Tl, '3')])],
     [reg('melasma', 'melasma', T('ملاسمای متوسط تا شدید صورت — لایه نازک شب‌ها، کوتاه‌مدت', 'Moderate–severe facial melasma — thin film nightly, short-term'), A18, 'notCalculated',
          {'reason': T('یک بار در روز دست‌کم ۳۰ دقیقه پیش از خواب، لایه نازک روی لک‌ها و حدود ۱ سانتی‌متر پوست سالم اطراف. با کنترل لک قطع شود. روزها ضدآفتاب SPF 30 و پرهیز از آفتاب.', 'Once daily at least 30 min before bedtime, a thin film on the patches and about 1/2 inch of surrounding skin. Stop when controlled. Daytime SPF 30 sunscreen and sun avoidance.')}, [R(Tl, '2'), R(Tl, '1')])],
     [CI('hyper', 'حساسیت به هر یک از اجزا.', 'Hypersensitivity to any component.', [R(Tl, '4')])],
     warn=[W('حاوی سولفیت (واکنش آلرژیک و حمله آسم در افراد حساس).', 'Contains sulfite (allergic reactions and asthma attacks in susceptible people).', [R(Tl, '5')])])

Sl = fda('soolantra', 'FDA Soolantra', 'Soolantra (ivermectin) cream 1% — Prescribing Information', sid('soolantra'))
drug('ivermectin-cream', 'dermatology', 'ایورمکتین کرم ۱٪ (روزاسه)', 'Ivermectin cream 1% (rosacea)', T('ضدالتهاب و ضدانگل موضعی', 'Topical anti-inflammatory/antiparasitic'), [{'name': 'Soolantra', 'market': 'US'}], ['soolantra', 'سولانترا', 'ایورمکتین کرم'],
     [unitform('cream-1', 'cream', 'topical', 'Ivermectin 1% cream (30, 45, 60 g)', [R(Sl, '3')])],
     [reg('rosacea', 'rosacea', T('ضایعات التهابی روزاسه — یک بار در روز روی صورت', 'Inflammatory lesions of rosacea — once daily to the face'), A18, 'notCalculated',
          {'reason': T('یک بار در روز به اندازه یک نخود برای هر ناحیه (پیشانی، چانه، بینی، هر گونه)؛ لایه نازک، دور از چشم و لب.', 'Once daily, a pea-sized amount for each area (forehead, chin, nose, each cheek); thin layer, away from eyes and lips.')}, [R(Sl, '2')])])

Pc = fda('pimecrolimus', 'FDA Pimecrolimus', 'Pimecrolimus cream 1% (Oceanside) — Prescribing Information', sid('elidel'))
drug('pimecrolimus', 'dermatology', 'پیمکرولیموس کرم ۱٪', 'Pimecrolimus cream 1%', T('مهارکننده کلسینورین موضعی', 'Topical calcineurin inhibitor'), [{'name': 'Elidel', 'market': 'US'}], ['elidel', 'الیدل', 'پیمکرولیموس'],
     [unitform('cream-1', 'cream', 'topical', 'Pimecrolimus 1% cream', [R(Pc, '3')])],
     [reg('ad', 'atopic-dermatitis', T('درماتیت آتوپیک خفیف تا متوسط (خط دوم، ۲ سال به بالا) — دو بار در روز', 'Mild–moderate atopic dermatitis (second line, ≥2 y) — twice daily'), {'minAge': age(2, 'year')}, 'notCalculated',
          {'reason': T('لایه نازک دو بار در روز تا رفع علائم؛ اگر بیش از ۶ هفته ادامه یافت، بیمار دوباره معاینه شود. مصرف طولانی و مداوم نه؛ فقط روی نواحی درگیر.', 'Thin layer twice daily until signs resolve; re-examine if symptoms persist beyond 6 weeks. Avoid continuous long-term use; affected areas only.')}, [R(Pc, '2'), R(Pc, '1')])],
     [CI('hyper', 'حساسیت به پیمکرولیموس.', 'Hypersensitivity to pimecrolimus.', [R(Pc, '4')])],
     warn=[W('هشدار جعبه‌ای: ایمنی طولانی‌مدت ثابت نشده؛ موارد نادر بدخیمی (پوست، لنفوم). در نقص ایمنی و زیر ۲ سال مصرف نشود.', 'Boxed warning: long-term safety not established; rare malignancy (skin, lymphoma). Not for immunocompromised patients or under 2 years.', [R(Pc, 'Boxed Warning')])])

Ds = fda('desonide', 'FDA Desonide cream', 'Desonide cream 0.05% (Alembic) — Prescribing Information', sid('desonide')); d = R(Ds, 'Dosage and Administration')
drug('desonide', 'dermatology', 'دزونید کرم ۰٫۰۵٪', 'Desonide cream 0.05%', T('کورتیکواستروئید موضعی ضعیف', 'Low-potency topical corticosteroid'), [{'name': 'DesOwen', 'market': 'US'}], ['desowen', 'دزونید', 'کرم کورتون ضعیف'],
     [unitform('cream', 'cream', 'topical', 'Desonide 0.05% cream (15, 60 g)', [R(Ds, 'How Supplied')])],
     [reg('dermatitis', 'dermatitis', T('درماتوزهای پاسخ‌دهنده به کورتون — ۲ تا ۴ بار در روز', 'Corticosteroid-responsive dermatoses — 2–4 times daily'), {}, 'notCalculated',
          {'reason': T('لایه نازک ۲ تا ۴ بار در روز بسته به شدت؛ با کنترل قطع. اگر ظرف ۲ هفته بهتر نشد، تشخیص بازبینی. پانسمان بسته نه.', 'Thin film 2–4 times daily by severity; stop when controlled. Reassess if no improvement in 2 weeks. No occlusive dressings.')}, [d])],
     [CI('hyper', 'حساسیت به اجزای کرم.', 'Hypersensitivity to any component.', [R(Ds, 'Contraindications')])],
     warn=[W('جذب سیستمیک ممکن است محور HPA را سرکوب کند (به‌ویژه در کودک، سطح وسیع یا پانسمان بسته).', 'Systemic absorption can suppress the HPA axis (especially children, large areas or occlusion).', [R(Ds, 'Precautions')])])

Iq = fda('imiquimod', 'FDA Imiquimod 3.75%', 'Imiquimod cream 3.75% — Prescribing Information', sid('imiquimod'))
drug('imiquimod', 'dermatology', 'ایمیکیمود کرم', 'Imiquimod cream', T('تعدیل‌کننده پاسخ ایمنی', 'Immune response modifier'), [{'name': 'Zyclara', 'market': 'US'}], ['aldara', 'zyclara', 'ایمیکیمود'],
     [unitform('cream', 'cream', 'topical', 'Imiquimod 3.75% cream, pump (0.235 g per actuation)', [R(Iq, '3')])],
     [reg('warts', 'genital-warts', T('زگیل تناسلی و اطراف مقعد — ۱۲ سال به بالا: شب‌ها تا ۸ هفته', 'External genital/perianal warts — ≥12 y: nightly up to 8 weeks'), {'minAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('لایه نازک یک بار شب‌ها تا پاک شدن کامل یا حداکثر ۸ هفته؛ هر بار حداکثر ۰٫۲۵ گرم. فقط پوست خارجی (نه داخل واژن یا مقعد).', 'Thin layer once nightly until clearance or up to 8 weeks; up to 0.25 g per application. External skin only (not intravaginal or intra-anal).')}, [R(Iq, '2.3'), R(Iq, '1')]),
      reg('ak', 'actinic-keratosis', T('کراتوز اکتینیک صورت یا سر طاس — دو دوره ۲ هفته‌ای شب‌ها', 'Actinic keratosis of face or balding scalp — two 2-week nightly cycles'), A18, 'notCalculated',
          {'reason': T('لایه نازک شب‌ها روی کل صورت یا سر طاس، دو دوره ۲ هفته‌ای با ۲ هفته استراحت بین آن‌ها؛ هر بار حداکثر ۰٫۵ گرم.', 'Thin layer nightly to the entire face or balding scalp, two 2-week cycles separated by 2 weeks off; up to 0.5 g per application.')}, [R(Iq, '2.2')])],
     warn=[W('واکنش التهابی شدید موضعی (ترشح، زخم)؛ تورم شدید فرج ممکن است احتباس ادرار بدهد؛ علائم شبه‌آنفلوانزا؛ از نور آفتاب و UV پرهیز.', 'Intense local inflammation (weeping, erosion); severe vulvar swelling may cause urinary retention; flu-like symptoms; avoid sunlight and UV.', [R(Iq, '5')])])

Pd = fda('condylox', 'FDA Condylox', 'Condylox (podofilox) gel 0.5% — Prescribing Information', sid('podofilox')); d = R(Pd, 'Dosage and Administration')
drug('podofilox', 'dermatology', 'پودوفیلوکس ژل', 'Podofilox gel', T('ضدمیتوز موضعی', 'Topical antimitotic'), [{'name': 'Condylox', 'market': 'US'}], ['condylox', 'podophyllotoxin', 'پودوفیلین', 'پودوفیلوکس'],
     [unitform('gel', 'gel', 'topical', 'Podofilox 0.5% gel', [R(Pd, 'How Supplied')])],
     [reg('warts', 'genital-warts', T('زگیل تناسلی خارجی — دو بار در روز ۳ روز، سپس ۴ روز استراحت', 'External genital warts — twice daily for 3 days, then 4 days off'), A18, 'notCalculated',
          {'reason': T('دو بار در روز ۳ روز پشت سر هم، سپس ۴ روز قطع؛ این چرخه هفتگی تا پاک شدن زگیل و حداکثر ۴ چرخه. بیشتر از ۴ چرخه بررسی نشده.', 'Twice daily for 3 consecutive days, then 4 days off; repeat this weekly cycle until clear, up to 4 cycles. More than 4 cycles not studied.')}, [d])],
     [CI('hyper', 'حساسیت یا عدم تحمل به اجزای ژل.', 'Hypersensitivity or intolerance to any component.', [R(Pd, 'Contraindications')])])

print('s7 ok')
