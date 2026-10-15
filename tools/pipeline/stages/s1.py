"""Stage 1 — allergy, cold & cough, eye allergy, plus liquid forms of common drugs."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
S = json.load(open(os.path.join(os.path.dirname(__file__), '..', '.cache', 's1_setids.json')))
sid = lambda k: S[k][0]

add_disease('chronic-urticaria', 'کهیر مزمن ایدیوپاتیک', 'Chronic idiopathic urticaria', ['urticaria', 'hives', 'کهیر', 'کهیر مزمن'], ['L50.1'], 'dermatology')
add_disease('pyelonephritis', 'پیلونفریت / عفونت ادراری عارضه‌دار', 'Pyelonephritis / complicated urinary tract infection', ['pyelonephritis', 'عفونت کلیه', 'پیلونفریت'], ['N10'], 'urology')

# levocetirizine
Lt = fda('levocet', 'FDA Levocetirizine tab', 'Levocetirizine dihydrochloride tablets 5 mg (Glenmark) — Prescribing Information', sid('levocet'))
Ls = fda('levocetsol', 'FDA Levocetirizine sol.', 'Levocetirizine dihydrochloride oral solution 2.5 mg/5 mL — Prescribing Information', sid('levocetsol'))
drug('levocetirizine', 'respiratory', 'لووسیتیریزین', 'Levocetirizine', T('آنتی‌هیستامین نسل دوم', 'Second-generation antihistamine'), [{'name': 'Xyzal', 'market': 'US'}],
     ['xyzal', 'زایزال', 'لووسیتیریزین', 'لوسیتریزین'],
     [tab('tab-5', 5, '5 mg tablet (scored)', [R(Lt, '3')], scored=True), liquid('sol-2-5', 2.5, 5, '2.5 mg / 5 mL oral solution', [R(Ls, '3')], form_='solution')],
     [reg('ciu-12', 'chronic-urticaria', T('کهیر مزمن — ۱۲ سال به بالا: ۵ mg یک بار شب', 'Chronic urticaria — ≥12 y: 5 mg once in the evening'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 5, 'dosesPerDay': 1}, [R(Lt, '2.2')],
          notes=[note('بعضی بیماران با ۲٫۵ mg کنترل می‌شوند.', 'Some patients are controlled with 2.5 mg.', [R(Lt, '2.2')])]),
      reg('ciu-6-11', 'chronic-urticaria', T('کهیر مزمن — ۶ تا ۱۱ سال: ۲٫۵ mg یک بار شب', 'Chronic urticaria — 6–11 y: 2.5 mg once in the evening'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 2.5, 'dosesPerDay': 1}, [R(Lt, '2.2')]),
      reg('ciu-6m-5y', 'chronic-urticaria', T('کهیر مزمن — ۶ ماه تا ۵ سال: ۱٫۲۵ mg (۲٫۵ mL محلول) یک بار شب', 'Chronic urticaria — 6 months–5 y: 1.25 mg (2.5 mL solution) once in the evening'), {'minAge': age(6, 'month'), 'maxAge': age(6, 'year')}, 'fixed', {'perDose': 1.25, 'dosesPerDay': 1}, [R(Ls, '2.2')], allowed=['sol-2-5'], limits={'maxPerDay': 1.25, 'refs': [R(Ls, '2.1')]}),
      reg('par-6m-2y', 'allergic-rhinitis', T('رینیت آلرژیک دائمی — ۶ ماه تا ۲ سال: ۱٫۲۵ mg یک بار شب', 'Perennial allergic rhinitis — 6 months–2 y: 1.25 mg once in the evening'), {'minAge': age(6, 'month'), 'maxAge': age(2, 'year')}, 'fixed', {'perDose': 1.25, 'dosesPerDay': 1}, [R(Ls, '2.1')], allowed=['sol-2-5'], limits={'maxPerDay': 1.25, 'refs': [R(Ls, '2.1')]})],
     [CI('hyper', 'حساسیت به لووسیتیریزین یا سیتیریزین.', 'Hypersensitivity to levocetirizine or cetirizine.', [R(Lt, '4')]),
      CI('esrd', 'نارسایی کلیه پیشرفته (کلیرانس زیر ۱۰) یا دیالیز.', 'End-stage renal disease (CrCl <10 mL/min) or haemodialysis.', [R(Lt, '4')]),
      CI('child-renal', 'کودک ۶ ماه تا ۱۱ سال با نارسایی کلیه.', 'Children 6 months–11 years with renal impairment.', [R(Lt, '4')], sev='warn')],
     warn=[W('خواب‌آلودگی؛ رانندگی و الکل پرهیز شود؛ احتیاط در احتباس ادرار.', 'Somnolence; avoid driving and alcohol; caution with urinary retention.', [R(Lt, '5')])],
     exs=[ex('ciu-12', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('ciu-6-11', 'tab-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 0.5}, ageYears=8, weightKg=25),
          ex('ciu-6-11', 'sol-2-5', {'perDose': 2.5, 'mlPerDose': 5}, ageYears=8, weightKg=25), ex('ciu-6m-5y', 'sol-2-5', {'perDose': 1.25, 'mlPerDose': 2.5}, ageYears=3, weightKg=14), ex('par-6m-2y', 'sol-2-5', {'perDose': 1.25, 'mlPerDose': 2.5}, ageMonths=12, weightKg=10)])

# bilastine (UK)
Bl = uk('uk-smpc-ilaxten', 'UK SmPC Ilaxten 20mg', 'Ilaxten 20 mg tablets (bilastine) — Summary of Product Characteristics', 'A. Menarini Farmaceutica Internazionale', '11 February 2026', 4551)
drug('bilastine', 'respiratory', 'بیلاستین', 'Bilastine', T('آنتی‌هیستامین نسل دوم', 'Second-generation antihistamine'), [{'name': 'Ilaxten', 'market': 'GB'}], ['ilaxten', 'bilaxten', 'بیلاستین', 'بیلاکستن'],
     [tab('tab-20', 20, '20 mg tablet', [R(Bl, '2')], markets=('GB',))],
     [reg('ar', 'allergic-rhinitis', T('رینوکونژنکتیویت آلرژیک — ۱۲ سال به بالا: ۲۰ mg یک بار در روز', 'Allergic rhinoconjunctivitis — ≥12 y: 20 mg once daily'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Bl, '4.2')],
          notes=[note('یک ساعت قبل یا دو ساعت بعد از غذا یا آب‌میوه.', 'One hour before or two hours after food or fruit juice.', [R(Bl, '4.2')])]),
      reg('urticaria', 'chronic-urticaria', T('کهیر — ۱۲ سال به بالا: ۲۰ mg یک بار در روز', 'Urticaria — ≥12 y: 20 mg once daily'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Bl, '4.2')])],
     [CI('hyper', 'حساسیت به بیلاستین.', 'Hypersensitivity to bilastine.', [R(Bl, '4.3')])],
     warn=[W('در نارسایی متوسط یا شدید کلیه، مصرف با مهارکننده‌های P-gp (کتوکونازول، اریترومایسین، سیکلوسپورین، ریتوناویر، دیلتیازم) پرهیز شود.', 'In moderate/severe renal impairment avoid P-gp inhibitors (ketoconazole, erythromycin, ciclosporin, ritonavir, diltiazem).', [R(Bl, '4.4')])],
     exs=[ex('ar', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('urticaria', 'tab-20', {'perDose': 20}, ageYears=30, weightKg=70)])

# eye drops
eye = lambda id, label, src, sec, markets=('US',): unitform(id, 'eye-drops', 'ophthalmic', label, [R(src, sec)], unit='drop', per='drop', markets=markets)
DROP = lambda id, dis, lab, pop, dose, n, refs, notes=None: reg(id, dis, lab, pop, 'fixed', {'perDose': dose, 'dosesPerDay': n}, refs, unit='drop', notes=notes)
Ep = fda('epinastine', 'FDA Epinastine eye', 'Epinastine HCl ophthalmic solution 0.05% — Prescribing Information', sid('epinastine'))
drug('epinastine-eye', 'sensory-organs', 'قطره چشمی اپیناستین', 'Epinastine eye drops', T('آنتی‌هیستامین چشمی', 'Ophthalmic antihistamine'), [{'name': 'Elestat', 'market': 'US'}], ['elestat', 'relestat', 'اپیناستین'],
     [eye('drops', '0.05% ophthalmic solution', Ep, '3')],
     [DROP('ac', 'allergic-conjunctivitis', T('خارش چشم آلرژیک — ۱ قطره هر چشم دو بار در روز (۲ سال به بالا)', 'Allergic itching — 1 drop each eye twice daily (≥2 y)'), {'minAge': age(2, 'year')}, 1, 2, [R(Ep, '2')])],
     warn=[W('برای سوزش ناشی از لنز استفاده نشود؛ لنز پیش از قطره برداشته شود.', 'Not for contact-lens irritation; remove lenses before use.', [R(Ep, '5')])],
     exs=[ex('ac', 'drops', {'perDose': 1}, ageYears=20, weightKg=60)])
Cr = fda('cromolyneye', 'FDA Cromolyn 4% eye', 'Cromolyn sodium ophthalmic solution 4% (Sandoz) — Prescribing Information', sid('cromolyneye'))
drug('cromolyn-eye', 'sensory-organs', 'قطره چشمی کرومولین ۴٪', 'Cromolyn 4% eye drops', T('تثبیت‌کننده ماست‌سل چشمی', 'Ophthalmic mast-cell stabiliser'), [{'name': 'Crolom', 'market': 'US'}], ['crolom', 'opticrom', 'کرومولین چشمی', 'کروموگلیکات چشمی'],
     [eye('drops', '4% ophthalmic solution', Cr, 'How Supplied')],
     [DROP('ac', 'allergic-conjunctivitis', T('آلرژی چشم — ۱ تا ۲ قطره هر چشم ۴ تا ۶ بار در روز (۴ سال به بالا)', 'Allergic eye disease — 1–2 drops each eye 4–6 times daily (≥4 y)'), {'minAge': age(4, 'year')}, 1, 4, [R(Cr, 'Dosage and Administration')],
           notes=[note('اثر به مصرف منظم وابسته است.', 'Effect depends on regular use.', [R(Cr, 'Dosage and Administration')])])],
     [CI('hyper', 'حساسیت به کرومولین.', 'Hypersensitivity to cromolyn.', [R(Cr, 'Contraindications')])],
     exs=[ex('ac', 'drops', {'perDose': 1}, ageYears=10, weightKg=30)])
Az = fda('azelastineeye', 'FDA Azelastine eye', 'Azelastine hydrochloride ophthalmic solution 0.05% (Apotex) — Prescribing Information', sid('azelastineeye'))
drug('azelastine-eye', 'sensory-organs', 'قطره چشمی آزلاستین', 'Azelastine eye drops', T('آنتی‌هیستامین چشمی', 'Ophthalmic antihistamine'), [{'name': 'Optivar', 'market': 'US'}], ['optivar', 'آزلاستین چشمی'],
     [eye('drops', '0.05% ophthalmic solution', Az, 'How Supplied')],
     [DROP('ac', 'allergic-conjunctivitis', T('خارش چشم آلرژیک — ۱ قطره دو بار در روز (۳ سال به بالا)', 'Allergic itching — 1 drop twice daily (≥3 y)'), {'minAge': age(3, 'year')}, 1, 2, [R(Az, 'Dosage and Administration')])],
     [CI('hyper', 'حساسیت به اجزا.', 'Hypersensitivity to components.', [R(Az, 'Contraindications')])],
     exs=[ex('ac', 'drops', {'perDose': 1}, ageYears=20, weightKg=60)])
Nc = fda('naphcon', 'FDA Naphazoline+phenir.', 'Naphazoline 0.02675% + pheniramine 0.315% eye drops (eye allergy relief) — Drug Facts', sid('naphcon'))
drug('naphazoline-pheniramine', 'sensory-organs', 'قطره چشمی نافازولین + فنیرامین', 'Naphazoline + pheniramine eye drops', T('ضداحتقان + آنتی‌هیستامین چشمی', 'Ocular decongestant + antihistamine'), [{'name': 'Naphcon-A', 'market': 'US'}, {'name': 'Visine-A', 'market': 'US'}],
     ['naphcon-a', 'visine', 'نفکن', 'قطره قرمزی چشم', 'نافازولین'],
     [eye('drops', 'Naphazoline 0.02675% + pheniramine 0.315%', Nc, 'Active Ingredients')],
     [DROP('ac', 'allergic-conjunctivitis', T('خارش و قرمزی آلرژیک چشم — ۶ سال به بالا: ۱ تا ۲ قطره تا ۴ بار در روز', 'Allergic itch and redness — ≥6 y: 1–2 drops up to 4 times daily'), {'minAge': age(6, 'year')}, 1, 4, [R(Nc, 'Directions')])],
     [CI('glaucoma', 'گلوکوم زاویه بسته، بیماری قلبی، فشار خون، بزرگی پروستات: پیش از مصرف با پزشک.', 'Narrow-angle glaucoma, heart disease, high blood pressure, enlarged prostate: ask a doctor first.', [R(Nc, 'Warnings — Ask a doctor before use')], sev='warn'),
      CI('lt6', 'زیر ۶ سال با پزشک.', 'Under 6 years: ask a doctor.', [R(Nc, 'Directions')], sev='warn', rule={'maxAge': age(6, 'year')})],
     warn=[W('مصرف زیاد قرمزی را بیشتر می‌کند؛ ممکن است مردمک موقتاً گشاد شود.', 'Overuse may cause more redness; pupils may dilate temporarily.', [R(Nc, 'Warnings — When using this product')])],
     exs=[ex('ac', 'drops', {'perDose': 1}, ageYears=20, weightKg=60)])

# terbutaline
Tb = fda('terbutaline', 'FDA Terbutaline tab', 'Terbutaline sulfate tablets (Upsher-Smith) — Prescribing Information', sid('terbutaline')); d = R(Tb, 'Dosage and Administration')
drug('terbutaline', 'respiratory', 'تربوتالین', 'Terbutaline', T('آگونیست بتا-۲', 'Beta-2 agonist'), [{'name': 'Bricanyl', 'market': 'US'}], ['bricanyl', 'بریکانیل', 'تربوتالین'],
     [tab('tab-2-5', 2.5, '2.5 mg tablet (scored)', [R(Tb, 'How Supplied')], scored=True), tab('tab-5', 5, '5 mg tablet (scored)', [R(Tb, 'How Supplied')], scored=True)],
     [reg('adult', 'asthma', T('برونکواسپاسم — بزرگسال: ۵ mg سه بار در روز (حدود هر ۶ ساعت در بیداری)', 'Bronchospasm — adult: 5 mg three times daily (about every 6 h while awake)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 5, 'dosesPerDay': 3}, [d], limits={'maxPerDay': 15, 'refs': [d]},
          notes=[note('اگر عوارض آزاردهنده بود ۲٫۵ mg سه بار در روز.', 'If side effects are troublesome, 2.5 mg three times daily.', [d])]),
      reg('teen', 'asthma', T('برونکواسپاسم — ۱۲ تا ۱۵ سال: ۲٫۵ mg سه بار در روز', 'Bronchospasm — 12–15 y: 2.5 mg three times daily'), {'minAge': age(12, 'year'), 'maxAge': age(16, 'year')}, 'fixed', {'perDose': 2.5, 'dosesPerDay': 3}, [d], limits={'maxPerDay': 7.5, 'refs': [d]})],
     [CI('toco', 'برای جلوگیری از زایمان زودرس (توکولیز) مصرف نشود.', 'Not to be used for tocolysis.', [R(Tb, 'Contraindications')]), CI('hyper', 'حساسیت به آمین‌های سمپاتومیمتیک.', 'Hypersensitivity to sympathomimetic amines.', [R(Tb, 'Contraindications')]),
      CI('lt12', 'زیر ۱۲ سال توصیه نمی‌شود.', 'Not recommended under 12 years.', [R(Tb, 'Pediatric Use')], rule={'maxAge': age(12, 'year')})],
     warn=[W('هشدار جعبه‌ای: در بارداری برای توکولیز عوارض جدی و مرگ مادر گزارش شده.', 'Boxed warning: serious adverse reactions and maternal deaths when used for tocolysis.', [R(Tb, 'Boxed Warning')])],
     exs=[ex('adult', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('teen', 'tab-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1}, ageYears=13, weightKg=45)])

# aminophylline
Am = fda('aminophylline', 'FDA Aminophylline inj.', 'Aminophylline injection 25 mg/mL (Hospira) — Prescribing Information', sid('aminophylline')); d = R(Am, 'Dosage and Administration')
drug('aminophylline', 'respiratory', 'آمینوفیلین (تزریقی)', 'Aminophylline (injection)', T('متیل‌گزانتین برونکودیلاتور', 'Methylxanthine bronchodilator'), [{'name': 'Aminophylline', 'market': 'US'}], ['aminophylline', 'آمینوفیلین', 'آمپول آمینوفیلین'],
     [liquid('vial-25', 25, 1, '25 mg/mL (250 mg/10 mL) vial', [R(Am, 'How Supplied')], form_='injection', route='iv')],
     [reg('load', 'asthma', T('حمله حاد آسم/COPD — بارگذاری ۵٫۷ mg/kg (وزن ایدئال) وریدی طی ۳۰ دقیقه، فقط اگر در ۲۴ ساعت گذشته تئوفیلین نگرفته', 'Acute asthma/COPD — load 5.7 mg/kg (ideal body weight) IV over 30 min, only if no theophylline in the previous 24 h'), A18, 'weightBased', {'perKgPerDay': 5.7, 'dividedDoses': 1}, [d],
          notes=[note('با وزن ایدئال حساب شود. سپس انفوزیون طبق جدول سنی برچسب و سطح سرمی تئوفیلین (هدف ۱۰ تا ۲۰ mcg/mL). کودکان و نوزادان: جدول برچسب.', 'Use ideal body weight. Then infusion per the label age table and serum theophylline levels (target 10–20 mcg/mL). Children and neonates: label table.', [d])])],
     [CI('hyper', 'حساسیت به تئوفیلین یا اتیلن‌دی‌آمین.', 'Hypersensitivity to theophylline or ethylenediamine.', [R(Am, 'Contraindications')])],
     warn=[W('سطح سرمی پایش شود؛ سمیت (تشنج، آریتمی) بالای ۲۰ mcg/mL؛ داروهای مهارکننده متابولیسم تئوفیلین (مثل سایمتیدین، اریترومایسین، تاکرین) سطح آن را بالا می‌برند.', 'Monitor serum levels; toxicity (seizures, arrhythmia) above 20 mcg/mL; drugs that inhibit theophylline metabolism (e.g. cimetidine, erythromycin, tacrine) raise levels.', [R(Am, 'Warnings'), d])],
     exs=[ex('load', 'vial-25', {'perDose': 399, 'mlPerDose': 15.96}, ageYears=40, weightKg=70)])

# budesonide nasal
Rh = fda('rhinocort', 'FDA Rhinocort Aqua', 'Rhinocort Aqua (budesonide) nasal spray 32 mcg — Prescribing Information', sid('rhinocort')); d = R(Rh, '2')
drug('budesonide-nasal', 'respiratory', 'اسپری بینی بودزوناید', 'Budesonide nasal spray', T('کورتون بینی', 'Nasal corticosteroid'), [{'name': 'Rhinocort', 'market': 'US'}], ['rhinocort', 'رینوکورت', 'بودزوناید بینی'],
     [unitform('spray', 'nasal-spray', 'nasal', '32 mcg per spray', [R(Rh, '3')], unit='spray', per='spray')],
     [reg('adult', 'allergic-rhinitis', T('رینیت آلرژیک — ۱۲ سال به بالا: شروع ۱ پاف هر سوراخ یک بار در روز', 'Allergic rhinitis — ≥12 y: start 1 spray each nostril once daily'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [d], unit='spray', limits={'maxPerDay': 8, 'refs': [d]},
          notes=[note('حداکثر ۴ پاف هر سوراخ (۲۵۶ mcg) در روز.', 'Max 4 sprays per nostril (256 mcg) daily.', [d])]),
      reg('child', 'allergic-rhinitis', T('رینیت آلرژیک — ۶ تا زیر ۱۲ سال: ۱ پاف هر سوراخ یک بار در روز', 'Allergic rhinitis — 6 to <12 y: 1 spray each nostril once daily'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [d], unit='spray', limits={'maxPerDay': 4, 'refs': [d]},
          notes=[note('حداکثر ۲ پاف هر سوراخ (۱۲۸ mcg). کورتون بینی ممکن است رشد قدی کودک را کند کند.', 'Max 2 sprays per nostril (128 mcg). Nasal steroids may slow growth in children.', [d, R(Rh, '8.4')])])],
     [CI('hyper', 'حساسیت به اجزا.', 'Hypersensitivity to ingredients.', [R(Rh, '4')])],
     warn=[W('خون‌دماغ، کاندیدای بینی، سوراخ شدن دیواره؛ پس از جراحی یا زخم اخیر بینی پرهیز.', 'Epistaxis, nasal candida, septal perforation; avoid after recent nasal ulcer, surgery or trauma.', [R(Rh, '5')])],
     exs=[ex('adult', 'spray', {'perDose': 2}, ageYears=30, weightKg=70), ex('child', 'spray', {'perDose': 2}, ageYears=8, weightKg=25)])

# saline nasal
Sn = fda('salinenasal', 'FDA Saline nasal 0.65%', 'Saline nasal spray (sodium chloride 0.65%) — Drug Facts', sid('salinenasal'))
drug('saline-nasal', 'respiratory', 'اسپری/قطره بینی نمکی (سالین)', 'Saline nasal spray/drops', T('مرطوب‌کننده بینی', 'Nasal moisturiser'), [{'name': 'Ocean', 'market': 'US'}], ['saline', 'سرم بینی', 'قطره بینی نمکی', 'اسپری آب نمک', 'سدیم کلراید بینی'],
     [unitform('spray', 'nasal-spray', 'nasal', 'Sodium chloride 0.65% nasal spray / drops', [R(Sn, 'Active Ingredient')], unit='spray', per='spray')],
     [reg('dry', 'nasal-congestion', T('خشکی و تحریک بینی (سرماخوردگی، هوای خشک، آلرژی)', 'Dry, irritated nose (colds, dry air, allergies)'), {}, 'notCalculated',
          {'reason': T('برچسب: ۲ بار فشار در هر سوراخ در صورت نیاز. ۳ سال و کمتر با پزشک؛ برای نوزاد به شکل قطره.', 'Label: squeeze twice in each nostril as needed. 3 years and under ask a doctor; for infants use drops.')}, [R(Sn, 'Directions')])],
     warn=[W('استفاده یک قوطی توسط چند نفر عفونت را منتقل می‌کند.', 'Use by more than one person may spread infection.', [R(Sn, 'Warnings')])])

# antihistamine + pseudoephedrine
PSE = lambda src: {'pseudoephedrine': {'name': T('سودوافدرین', 'Pseudoephedrine'), 'amount': 120, 'unit': 'mg', 'limits': {'maxPerDay': 240, 'refs': [R(src, 'Directions')]}}}
PSE_CI = lambda src: CI('maoi', 'مصرف مهارکننده MAO در ۲ هفته اخیر. بیماری قلب، تیروئید، فشار خون، دیابت، بزرگی پروستات: پیش از مصرف با پزشک.', 'MAOI within 2 weeks. Heart disease, thyroid disease, high blood pressure, diabetes, enlarged prostate: ask a doctor first.', [R(src, 'Warnings')])
Cd = fda('claritind', 'FDA Claritin-D 12h', 'Claritin-D 12 Hour (loratadine 5 mg / pseudoephedrine sulfate 120 mg) — Drug Facts', sid('claritind'))
drug('loratadine-pseudoephedrine', 'respiratory', 'لوراتادین + سودوافدرین', 'Loratadine + pseudoephedrine', T('آنتی‌هیستامین + ضداحتقان', 'Antihistamine + decongestant'), [{'name': 'Claritin-D', 'market': 'US'}], ['claritin-d', 'کلاریتین دی', 'لوراتادین دی'],
     [form('tab', 'tablet', 'oral', 'Loratadine 5 mg + pseudoephedrine sulfate 120 mg ER tablet', 5, 'mg', [R(Cd, 'Active ingredient')], per='tablet', scored=False, components={'loratadine': {'name': T('لوراتادین', 'Loratadine'), 'amount': 5, 'unit': 'mg'}, **PSE(Cd)})],
     [reg('ar', 'allergic-rhinitis', T('آلرژی با احتقان بینی — ۱۲ سال به بالا: ۱ قرص هر ۱۲ ساعت', 'Allergy with congestion — ≥12 y: 1 tablet every 12 h'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 5, 'dosesPerDay': 2}, [R(Cd, 'Directions')], doseComponent='loratadine', limits={'maxPerDay': 10, 'refs': [R(Cd, 'Directions')]},
          notes=[note('قرص شکسته، خرد یا جویده نشود.', 'Do not divide, crush or chew.', [R(Cd, 'Directions')])])],
     [PSE_CI(Cd)], exs=[ex('ar', 'tab', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])
Zd = fda('zyrtecd', 'FDA Zyrtec-D', 'Zyrtec-D (cetirizine 5 mg / pseudoephedrine 120 mg) — Drug Facts', sid('zyrtecd'))
drug('cetirizine-pseudoephedrine', 'respiratory', 'سیتیریزین + سودوافدرین', 'Cetirizine + pseudoephedrine', T('آنتی‌هیستامین + ضداحتقان', 'Antihistamine + decongestant'), [{'name': 'Zyrtec-D', 'market': 'US'}], ['zyrtec-d', 'زیرتک دی', 'سیتریزین دی'],
     [form('tab', 'tablet', 'oral', 'Cetirizine 5 mg + pseudoephedrine 120 mg ER tablet', 5, 'mg', [R(Zd, 'Active ingredients')], per='tablet', scored=False, components={'cetirizine': {'name': T('سیتیریزین', 'Cetirizine'), 'amount': 5, 'unit': 'mg'}, **PSE(Zd)})],
     [reg('ar', 'allergic-rhinitis', T('آلرژی با احتقان بینی — ۱۲ سال به بالا: ۱ قرص هر ۱۲ ساعت', 'Allergy with congestion — ≥12 y: 1 tablet every 12 h'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 5, 'dosesPerDay': 2}, [R(Zd, 'Directions')], doseComponent='cetirizine', limits={'maxPerDay': 10, 'refs': [R(Zd, 'Directions')]},
          notes=[note('کامل بلعیده شود. ۶۵ سال به بالا با پزشک.', 'Swallow whole. 65 and over: ask a doctor.', [R(Zd, 'Directions')])])],
     [PSE_CI(Zd), CI('hydroxyzine', 'حساسیت به هیدروکسیزین.', 'Allergy to hydroxyzine.', [R(Zd, 'Warnings — Do not use')])], exs=[ex('ar', 'tab', {'perDose': 5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

# cold & flu liquids
Dq = fda('dayquil', 'FDA DayQuil liquid', 'Vicks DayQuil Cold & Flu (acetaminophen/dextromethorphan/phenylephrine) liquid — Drug Facts', sid('dayquil')); d = R(Dq, 'Directions')
comp = {'acetaminophen': {'name': T('استامینوفن', 'Acetaminophen'), 'amount': 325, 'unit': 'mg'}, 'dextromethorphan': {'name': T('دکسترومتورفان', 'Dextromethorphan'), 'amount': 10, 'unit': 'mg'}, 'phenylephrine': {'name': T('فنیل‌افرین', 'Phenylephrine'), 'amount': 5, 'unit': 'mg'}}
COLD_CI = lambda src: [CI('apap', 'با هر داروی دیگر حاوی استامینوفن مصرف نشود.', 'Do not use with any other acetaminophen-containing drug.', [R(src, 'Warnings — Do not use')]), CI('maoi', 'مصرف مهارکننده MAO در ۲ هفته اخیر.', 'MAOI within 2 weeks.', [R(src, 'Warnings — Do not use')]), CI('lt4', 'زیر ۴ سال مصرف نشود.', 'Do not use under 4 years.', [d if src == Dq else R(src, 'Directions')], rule={'maxAge': age(4, 'year')})]
drug('cold-flu-day', 'respiratory', 'شربت سرماخوردگی روزانه (استامینوفن + دکسترومتورفان + فنیل‌افرین)', 'Cold & flu day liquid (acetaminophen + dextromethorphan + phenylephrine)', T('ترکیب ضدسرماخوردگی', 'Cold and flu combination'), [{'name': 'Vicks DayQuil', 'market': 'US'}],
     ['dayquil', 'دی کوئیل', 'شربت سرماخوردگی', 'سرماخوردگی روزانه'],
     [form('liq', 'solution', 'oral', 'Per 15 mL: acetaminophen 325 mg, dextromethorphan 10 mg, phenylephrine 5 mg', 325, 'mg', [R(Dq, 'Active ingredients')], vol=15, components=comp)],
     [reg('adult', 'common-cold', T('سرماخوردگی/آنفلوانزا — ۱۲ سال به بالا: ۳۰ mL هر ۴ ساعت (حداکثر ۴ نوبت)', 'Cold/flu — ≥12 y: 30 mL every 4 h (max 4 doses)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 650, 'dosesPerDay': 4}, [d], doseComponent='acetaminophen', limits={'maxPerDay': 2600, 'refs': [d]}),
      reg('child', 'common-cold', T('سرماخوردگی/آنفلوانزا — ۶ تا زیر ۱۲ سال: ۱۵ mL هر ۴ ساعت (حداکثر ۴ نوبت)', 'Cold/flu — 6 to <12 y: 15 mL every 4 h (max 4 doses)'), {'minAge': age(6, 'year'), 'maxAge': age(12, 'year')}, 'fixed', {'perDose': 325, 'dosesPerDay': 4}, [d], doseComponent='acetaminophen', limits={'maxPerDay': 1300, 'refs': [d]},
          notes=[note('۴ تا زیر ۶ سال با پزشک.', '4 to <6 years: ask a doctor.', [d])])],
     COLD_CI(Dq), warn=[W('هشدار کبد: بیش از ۴ نوبت در ۲۴ ساعت، با داروی دیگر حاوی استامینوفن یا با ۳ نوشیدنی الکلی یا بیشتر در روز آسیب شدید کبد.', 'Liver warning: more than 4 doses in 24 h, other acetaminophen products, or 3+ alcoholic drinks daily can cause severe liver damage.', [R(Dq, 'Warnings — Liver warning')])],
     exs=[ex('adult', 'liq', {'perDose': 650, 'mlPerDose': 30}, ageYears=30, weightKg=70), ex('child', 'liq', {'perDose': 325, 'mlPerDose': 15}, ageYears=8, weightKg=25)])
Nq = fda('nyquil', 'FDA NyQuil liquid', 'Vicks NyQuil Cold & Flu (acetaminophen/dextromethorphan/doxylamine) liquid — Drug Facts', sid('nyquil')); dn = R(Nq, 'Directions')
compn = {'acetaminophen': {'name': T('استامینوفن', 'Acetaminophen'), 'amount': 650, 'unit': 'mg'}, 'dextromethorphan': {'name': T('دکسترومتورفان', 'Dextromethorphan'), 'amount': 30, 'unit': 'mg'}, 'doxylamine': {'name': T('دوکسیلامین', 'Doxylamine'), 'amount': 12.5, 'unit': 'mg'}}
drug('cold-flu-night', 'respiratory', 'شربت سرماخوردگی شبانه (استامینوفن + دکسترومتورفان + دوکسیلامین)', 'Cold & flu night liquid (acetaminophen + dextromethorphan + doxylamine)', T('ترکیب ضدسرماخوردگی', 'Cold and flu combination'), [{'name': 'Vicks NyQuil', 'market': 'US'}],
     ['nyquil', 'نای کوئیل', 'سرماخوردگی شبانه', 'شربت سرماخوردگی شب'],
     [form('liq', 'solution', 'oral', 'Per 30 mL: acetaminophen 650 mg, dextromethorphan 30 mg, doxylamine 12.5 mg', 650, 'mg', [R(Nq, 'Active ingredients')], vol=30, components=compn)],
     [reg('adult', 'common-cold', T('سرماخوردگی/آنفلوانزا — ۱۲ سال به بالا: ۳۰ mL هر ۶ ساعت (حداکثر ۴ نوبت)', 'Cold/flu — ≥12 y: 30 mL every 6 h (max 4 doses)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 650, 'dosesPerDay': 4}, [dn], doseComponent='acetaminophen', limits={'maxPerDay': 2600, 'refs': [dn]},
          notes=[note('۴ تا زیر ۱۲ سال با پزشک. خواب‌آور است.', '4 to <12 years: ask a doctor. Causes drowsiness.', [dn])])],
     [CI('apap', 'با هر داروی دیگر حاوی استامینوفن مصرف نشود.', 'Do not use with any other acetaminophen-containing drug.', [R(Nq, 'Warnings — Do not use')]), CI('maoi', 'مصرف مهارکننده MAO در ۲ هفته اخیر.', 'MAOI within 2 weeks.', [R(Nq, 'Warnings — Do not use')]),
      CI('lt4', 'زیر ۴ سال مصرف نشود.', 'Do not use under 4 years.', [dn], rule={'maxAge': age(4, 'year')})],
     exs=[ex('adult', 'liq', {'perDose': 650, 'mlPerDose': 30}, ageYears=30, weightKg=70)])

# Iran-only cold preparations
NOREF = lambda fa='', en='': T(f'رفرنس مطمئن نیست: برچسب مرجع آمریکا/انگلیس برای این فرآورده در دسترس نیست و اطلاعات فقط از سایت ایرانی دارویاب است. {fa} دوز محاسبه نمی‌شود؛ طبق بروشور داخل جعبه و نظر پزشک.', f'Reference not reliable: no US/UK label is available for this product; information comes only from the Iranian site Darooyab. {en} No dose is calculated; follow the box leaflet and a physician.')
Ac = dy('ir-darooyab-adult-cold', 'Darooyab Adult cold', 'سرماخوردگی بزرگسالان — موارد مصرف، ترکیب‌ها و اشکال دارویی', 'G-4501/Adult-cold')
drug('adult-cold', 'respiratory', 'قرص سرماخوردگی بزرگسالان', 'Adult cold preparation (Iran)', T('ترکیب ضدسرماخوردگی', 'Cold combination'), [{'name': 'Adult Cold', 'market': 'IR'}], ['adult cold', 'سرماخوردگی بزرگسالان', 'قرص سرماخوردگی', 'اکتوکلد'],
     [unitform('tab', 'tablet', 'oral', 'Adult cold preparation 1–7 tablets / softgels (composition differs by number)', [R(Ac, 'اشکال دارویی')], per='tablet', markets=('IR',))],
     [reg('cold', 'common-cold', T('علائم سرماخوردگی بزرگسالان', 'Adult cold symptoms'), A18, 'notCalculated', {'reason': NOREF('ترکیب هر شماره فرق می‌کند (استامینوفن یا ایبوپروفن، فنیل‌افرین یا سودوافدرین، کلرفنیرامین، دکسترومتورفان…).', 'Each numbered product has a different composition (acetaminophen or ibuprofen, phenylephrine or pseudoephedrine, chlorpheniramine, dextromethorphan…).')}, [R(Ac, 'موارد مصرف')])],
     warn=[W('با سایر داروهای حاوی استامینوفن یا ضداحتقان هم‌زمان مصرف نشود.', 'Do not combine with other acetaminophen or decongestant products.', [R(Ac, 'هشدارها')])])
Ad = dy('ir-darooyab-antihist-decong', 'Darooyab Antihist-Decong', 'آنتی‌هیستامین دکونژستانت — موارد مصرف و اشکال دارویی', 'G-4509/Antihistamine-Decongestant')
drug('antihistamine-decongestant', 'respiratory', 'قرص آنتی‌هیستامین دکونژستانت', 'Antihistamine-decongestant (Iran)', T('آنتی‌هیستامین + ضداحتقان', 'Antihistamine + decongestant'), [{'name': 'Antihistamine Decongestant', 'market': 'IR'}], ['آنتی هیستامین دکونژستانت', 'آنتی هیستامین دکونژستان', 'antihistamine decongestant', 'دکونژستانت'],
     [unitform('tab', 'tablet', 'oral', 'Antihistamine-decongestant tablet / SR tablet / softgel', [R(Ad, 'اشکال دارویی')], per='tablet', markets=('IR',))],
     [reg('ar', 'allergic-rhinitis', T('رینیت آلرژیک و احتقان بینی', 'Allergic rhinitis and nasal congestion'), {}, 'notCalculated', {'reason': NOREF()}, [R(Ad, 'موارد مصرف')])],
     warn=[W('از نوشیدنی‌های پرکافئین (قهوه) پرهیز شود؛ بی‌قراری و تپش قلب را تشدید می‌کند.', 'Avoid large amounts of caffeine (coffee); worsens restlessness and palpitations.', [R(Ad, 'نکات مصرف')])])

# new forms on existing drugs
Ct = fda('cetirizinetab', 'FDA Cetirizine 10mg tab', 'Cetirizine HCl 10 mg tablets (OTC) — Drug Facts', sid('cetirizinetab'))
patch('cetirizine', add_forms=[tab('tab-10', 10, '10 mg tablet (OTC)', [R(Ct, 'Active Ingredient')])],
      add_regs=[reg('otc-tab', 'allergic-rhinitis', T('آلرژی — ۶ سال به بالا: یک قرص ۱۰ mg روزانه', 'Allergy — ≥6 y: one 10 mg tablet daily'), {'minAge': age(6, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Ct, 'Directions')], allowed=['tab-10'], limits={'maxPerDay': 10, 'refs': [R(Ct, 'Directions')]},
                    notes=[note('در علائم خفیف‌تر فرآورده ۵ mg کافی است. ۶۵ سال به بالا و بیماری کبد یا کلیه با پزشک.', 'A 5 mg product may suit milder symptoms. 65+ or liver/kidney disease: ask a doctor.', [R(Ct, 'Directions')])])],
      add_exs=[ex('otc-tab', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)], pin_old=True)
Lo = fda('loratadinetab', 'FDA Loratadine 10mg tab', 'Loratadine 10 mg tablets (OTC) — Drug Facts', sid('loratadinetab'))
patch('loratadine', add_forms=[tab('tab-10', 10, '10 mg tablet (OTC)', [R(Lo, 'Active Ingredient')])],
      add_regs=[reg('otc-tab', 'allergic-rhinitis', T('آلرژی — ۶ سال به بالا: یک قرص ۱۰ mg روزانه', 'Allergy — ≥6 y: one 10 mg tablet daily'), {'minAge': age(6, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Lo, 'Directions')], allowed=['tab-10'], limits={'maxPerDay': 10, 'refs': [R(Lo, 'Directions')]})],
      add_exs=[ex('otc-tab', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)], pin_old=True)
Hs = fda('hydroxyzinesol', 'FDA Hydroxyzine solution', 'Hydroxyzine HCl oral solution 10 mg/5 mL — Prescribing Information', sid('hydroxyzinesol'))
patch('hydroxyzine', add_forms=[liquid('sol-10-5', 10, 5, '10 mg / 5 mL oral solution', [R(Hs, 'How Supplied')], form_='solution')], add_exs=[ex('pruritus-under6', 'sol-10-5', {'perDose': 12.5, 'mlPerDose': 6.25}, ageYears=4, weightKg=16)])
Ps = fda('promethazinesol', 'FDA Promethazine syrup', 'Promethazine HCl oral solution 6.25 mg/5 mL — Prescribing Information', sid('promethazinesol'))
patch('promethazine', add_forms=[liquid('syr-6-25', 6.25, 5, '6.25 mg / 5 mL syrup', [R(Ps, 'How Supplied')], form_='syrup')])
Cb = fda('carbamazepinesusp', 'FDA Carbamazepine susp.', 'Carbamazepine tablets, chewable, XR and oral suspension 100 mg/5 mL (Sun) — Prescribing Information', sid('carbamazepinesusp'))
patch('carbamazepine', add_forms=[liquid('susp-100-5', 100, 5, '100 mg / 5 mL suspension', [R(Cb, 'How Supplied')])], add_exs=[ex('epi-lt6', 'susp-100-5', {'perDose': 100, 'mlPerDose': 5}, ageYears=4, weightKg=20)])
On = fda('ondansetronsol', 'FDA Ondansetron sol.', 'Ondansetron oral solution 4 mg/5 mL — Prescribing Information', sid('ondansetronsol'))
patch('ondansetron', add_forms=[liquid('sol-4-5', 4, 5, '4 mg / 5 mL oral solution', [R(On, 'How Supplied')], form_='solution')])
Cp = fda('ciprosusp', 'FDA Cipro (tab+susp)', 'Cipro (ciprofloxacin) tablets and oral suspension (Bayer) — Prescribing Information', sid('ciprosusp')); dp = R(Cp, 'Dosage and Administration — Pediatric Dosage Guidelines')
patch('ciprofloxacin', add_forms=[liquid('susp-250', 250, 5, '5% (250 mg / 5 mL) oral suspension', [R(Cp, 'Dosage Forms and Strengths')]), liquid('susp-500', 500, 5, '10% (500 mg / 5 mL) oral suspension', [R(Cp, 'Dosage Forms and Strengths')])],
      add_regs=[reg('cuti-child', 'pyelonephritis', T('عفونت ادراری عارضه‌دار / پیلونفریت — ۱ تا ۱۷ سال: ۱۰ تا ۲۰ mg/kg هر ۱۲ ساعت', 'Complicated UTI / pyelonephritis — 1–17 y: 10–20 mg/kg every 12 h'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year')}, 'weightBased',
                    {'perKgPerDose': 10, 'perKgPerDoseMax': 20, 'intervalHours': 12}, [dp], limits={'maxPerDose': 750, 'refs': [dp]}, dur={'min': 10, 'max': 21},
                    notes=[note('حداکثر ۷۵۰ mg در هر دوز حتی بالای ۵۱ kg. در کودکان خطر عوارض مفصلی؛ داروی خط اول نیست.', 'Max 750 mg per dose even above 51 kg. Joint adverse events in children; not first choice.', [dp, R(Cp, '8.4')])])],
      add_exs=[ex('cuti-child', 'susp-250', {'perDose': 200, 'mlPerDose': 4, 'upperPerDose': 400}, ageYears=6, weightKg=20)], pin_old=True)
Ab = dy('ir-darooyab-albendazole', 'Darooyab Albendazole', 'آلبندازول — اشکال دارویی (سوسپانسیون ۴۰۰ mg/۱۰ mL)', 'G-214/Albendazole')
patch('albendazole', add_forms=[liquid('susp-200-5-ir', 200, 5, 'Albendazole 400 mg / 10 mL suspension (Iran)', [R(Ab, 'اشکال دارویی')], markets=('IR',))])
print('s1 ok')
