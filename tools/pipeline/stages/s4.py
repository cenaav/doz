"""Stage 4 — emergency, antidotes, vaccines and immunoglobulins."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's4_setids.json')))
sid = lambda k: S[k][0]

add_disease('svt', 'تاکی‌کاردی فوق بطنی حمله‌ای (PSVT)', 'Paroxysmal supraventricular tachycardia', ['SVT', 'PSVT', 'تاکی کاردی فوق بطنی', 'تپش قلب'], ['I47.10'], 'cardiology')
add_disease('cardiac-arrest', 'ایست قلبی و فیبریلاسیون بطنی', 'Cardiac arrest and ventricular fibrillation', ['cardiac arrest', 'VF', 'ایست قلبی', 'احیا'], ['I46.9', 'I49.01'], 'emergency')
add_disease('iron-poisoning', 'مسمومیت حاد با آهن', 'Acute iron poisoning', ['iron overdose', 'مسمومیت آهن', 'قرص آهن'], ['T45.4X1A'], 'toxicology')
add_disease('toxic-alcohol', 'مسمومیت با متانول یا اتیلن گلیکول', 'Methanol or ethylene glycol poisoning', ['methanol', 'ethylene glycol', 'متانول', 'الکل صنعتی', 'ضدیخ'], ['T51.1X1A', 'T52.3X1A'], 'toxicology')
add_disease('methemoglobinemia', 'مت‌هموگلوبینمی', 'Methaemoglobinaemia', ['methemoglobinemia', 'مت هموگلوبین', 'سیانوز'], ['D74.9'], 'toxicology')
add_disease('heparin-overdose', 'خنثی‌سازی هپارین / مصرف بیش از حد', 'Heparin reversal / overdose', ['heparin overdose', 'خنثی سازی هپارین', 'پروتامین'], ['T45.511A'], 'toxicology')
add_disease('digoxin-toxicity', 'مسمومیت با دیگوکسین', 'Digoxin toxicity', ['digoxin toxicity', 'مسمومیت دیگوکسین', 'دیژیتال'], ['T46.0X1A'], 'toxicology')
add_disease('cyanide-poisoning', 'مسمومیت با سیانید', 'Cyanide poisoning', ['cyanide', 'سیانور', 'سیانید', 'دود آتش‌سوزی'], ['T65.0X1A'], 'toxicology')
add_disease('snakebite', 'مارگزیدگی', 'Snakebite', ['snake bite', 'مار گزیدگی', 'نیش مار'], ['T63.001A'], 'toxicology')
add_disease('scorpion-sting', 'عقرب‌زدگی', 'Scorpion sting', ['scorpion', 'عقرب گزیدگی', 'نیش عقرب'], ['T63.2X1A'], 'toxicology')
add_disease('immunization', 'واکسیناسیون', 'Immunisation (vaccination)', ['vaccine', 'واکسن', 'ایمن سازی', 'واکسیناسیون'], ['Z23'], 'pediatrics')
add_disease('tetanus-prophylaxis', 'پیشگیری از کزاز (زخم)', 'Tetanus prophylaxis (wounds)', ['tetanus', 'کزاز', 'توگام', 'زخم آلوده'], ['Z23'], 'emergency')
add_disease('rabies-exposure', 'پیشگیری پس از تماس با هاری (گازگرفتگی حیوان)', 'Rabies post-exposure prophylaxis (animal bite)', ['rabies', 'هاری', 'سگ گزیدگی', 'گاز گرفتگی'], ['Z20.3'], 'emergency')
add_disease('hbv-exposure', 'تماس با هپاتیت B (سوزن‌زدگی، نوزاد مادر HBsAg مثبت)', 'Hepatitis B exposure (needlestick, infant of HBsAg-positive mother)', ['needlestick', 'سوزن زدگی', 'HBIG', 'تماس هپاتیت'], ['Z20.5'], 'infectious')
NOT_RELIABLE = 'رفرنس مطمئن نیست: برچسب آمریکا/انگلیس در دسترس نیست و اطلاعات از سایت ایرانی دارویاب است. دوز محاسبه نمی‌شود. '
NOT_RELIABLE_EN = 'Reference not reliable: no US/UK label available; information is from the Iranian site Darooyab. No dose is calculated. '
pv = lambda id, label, mg, src, sec, unit='mg': form(id, 'powder-for-injection', 'iv', label, mg, unit, [R(src, sec)], per='vial')
inj = lambda id, label, mg, ml, src, sec, route='iv', unit='mg': liquid(id, mg, ml, label, [R(src, sec)], form_='injection', route=route, unit=unit)
vac = lambda id, label, src, sec='3': form(id, 'injection', 'im', label, 1, 'mL', [R(src, sec)], vol=1)
ONE = {'min': 1, 'max': 1}

# --- emergency ---
Ad = fda('adenosine', 'FDA Adenosine inj.', 'Adenosine injection 3 mg/mL (Sagent) — Prescribing Information', sid('adenosine')); d = R(Ad, 'Dosage and Administration')
drug('adenosine', 'cardiovascular', 'آدنوزین (تزریقی)', 'Adenosine (injection)', T('ضدآریتمی', 'Antiarrhythmic'), [{'name': 'Adenocard', 'market': 'US'}], ['adenocard', 'آدنوزین', 'adenosine'],
     [inj('vial-3', '3 mg/mL (6 mg/2 mL, 12 mg/4 mL) vial', 3, 1, Ad, 'How Supplied')],
     [reg('adult', 'svt', T('PSVT — بزرگسال و کودک ۵۰ kg به بالا: ۶ mg بولوس سریع، در صورت نیاز ۱۲ mg', 'PSVT — adults and children ≥50 kg: 6 mg rapid bolus, then 12 mg if needed'), {'minWeightKg': 50}, 'fixed', {'perDose': 6, 'dosesPerDay': 1}, [d], dur=ONE,
          notes=[note('بولوس سریع در ۱ تا ۲ ثانیه و فوراً فلاش سالین. اگر ظرف ۱ تا ۲ دقیقه برنگشت: ۱۲ mg؛ همین ۱۲ mg را می‌توان یک بار دیگر تکرار کرد. دوز بالای ۱۲ mg توصیه نمی‌شود.',
                      'Rapid bolus over 1–2 s followed by a rapid saline flush. If no conversion within 1–2 min: 12 mg; the 12 mg dose may be repeated once. Doses over 12 mg not recommended.', [d])]),
      reg('child', 'svt', T('PSVT — کودک زیر ۵۰ kg: ۰٫۰۵ تا ۰٫۱ mg/kg بولوس سریع', 'PSVT — child <50 kg: 0.05–0.1 mg/kg rapid bolus'), {'maxWeightKg': 49.99}, 'weightBased', {'perKgPerDay': 0.05, 'perKgPerDayMax': 0.1, 'dividedDoses': 1}, [d],
          limits={'maxPerDose': 12, 'refs': [d]}, dur=ONE,
          notes=[note('اگر ظرف ۱ تا ۲ دقیقه برنگشت، هر بار ۰٫۰۵ تا ۰٫۱ mg/kg بیشتر تا حداکثر یک دوز ۰٫۳ mg/kg (و نه بیش از ۱۲ mg). هر دوز با فلاش سالین.', 'If no conversion in 1–2 min, increase each bolus by 0.05–0.1 mg/kg up to a maximum single dose of 0.3 mg/kg (not over 12 mg). Flush after each dose.', [d])])],
     [CI('ci', 'بلوک AV درجه ۲ یا ۳ یا بیماری گره سینوسی (بدون پیس‌میکر فعال)؛ حساسیت به آدنوزین.', 'Second- or third-degree AV block or sinus node disease (without a functioning pacemaker); hypersensitivity to adenosine.', [R(Ad, 'Contraindications')])],
     exs=[ex('adult', 'vial-3', {'perDose': 6, 'mlPerDose': 2}, ageYears=40, weightKg=70), ex('child', 'vial-3', {'perDose': 1, 'upperPerDose': 2}, ageYears=6, weightKg=20)])

Fp = fda('cerebyx', 'FDA Cerebyx', 'Cerebyx (fosphenytoin sodium) injection — Prescribing Information', sid('cerebyx'))
drug('fosphenytoin', 'nervous-system', 'فوس‌فنی‌توئین (تزریقی)', 'Fosphenytoin (injection)', T('ضدتشنج (پیش‌داروی فنی‌توئین)', 'Anticonvulsant (phenytoin prodrug)'), [{'name': 'Cerebyx', 'market': 'US'}], ['cerebyx', 'سربیکس', 'فوس فنی توئین'],
     [inj('vial-50', '50 mg PE/mL (100 mg PE/2 mL; 500 mg PE/10 mL)', 50, 1, Fp, '3')],
     [reg('se', 'status-epilepticus', T('صرع پایدار — دوز بارگذاری ۱۵ تا ۲۰ mg PE/kg (بزرگسال و کودک)', 'Status epilepticus — loading dose 15–20 mg PE/kg (adults and children)'), {}, 'weightBased', {'perKgPerDay': 15, 'perKgPerDayMax': 20, 'dividedDoses': 1}, [R(Fp, '2.3'), R(Fp, 'Highlights — Dosage and Administration')], dur=ONE,
          notes=[note('همه دوزها بر حسب «معادل فنی‌توئین سدیم» (PE). سرعت: بزرگسال ۱۰۰ تا ۱۵۰ mg PE/min (حداکثر ۱۵۰)؛ کودک ۲ mg PE/kg/min یا ۱۵۰ mg PE/min هر کدام کندتر. پیش از انفوزیون تا ۱٫۵ تا ۲۵ mg PE/mL رقیق شود. پایش مداوم ECG، فشار و تنفس. معمولاً همراه بنزودیازپین وریدی؛ سپس دوز نگهدارنده.',
                      'All doses in phenytoin sodium equivalents (PE). Rate: adults 100–150 mg PE/min (max 150); children 2 mg PE/kg/min or 150 mg PE/min, whichever is slower. Dilute to 1.5–25 mg PE/mL before infusion. Continuous ECG, BP and respiratory monitoring. Usually with an IV benzodiazepine; follow with maintenance dosing.', [R(Fp, '2.3'), R(Fp, '2.2')])])],
     [CI('ci', 'حساسیت به فوس‌فنی‌توئین، فنی‌توئین یا هیدانتوئین‌ها؛ برادی‌کاردی سینوسی، بلوک SA، بلوک AV درجه ۲ و ۳، سندرم آدامز-استوکس؛ سابقه سمیت کبدی با فنی‌توئین؛ مصرف همزمان دلاویردین.',
         'Hypersensitivity to fosphenytoin, phenytoin or hydantoins; sinus bradycardia, SA block, 2nd/3rd-degree AV block, Adams-Stokes syndrome; prior phenytoin hepatotoxicity; coadministration with delavirdine.', [R(Fp, '4')])],
     warn=[W('هشدار جعبه‌ای: انفوزیون سریع خطر افت شدید فشار و آریتمی دارد؛ از سرعت مجاز تجاوز نشود.', 'Boxed warning: rapid infusion risks severe hypotension and arrhythmias; do not exceed the rate limits.', [R(Fp, 'Boxed Warning')])],
     exs=[ex('se', 'vial-50', {'perDose': 1050, 'upperPerDose': 1400}, ageYears=40, weightKg=70), ex('se', 'vial-50', {'perDose': 300, 'upperPerDose': 400}, ageYears=6, weightKg=20)])

Am = fda('amiodarone-inj', 'FDA Amiodarone inj.', 'Amiodarone hydrochloride injection 50 mg/mL — Prescribing Information', sid('amioinj'))
patch('amiodarone', add_forms=[inj('inj-50', '50 mg/mL injection (dilute in D5W before infusion)', 50, 1, Am, '3')],
      add_regs=[reg('iv-load', 'ventricular-arrhythmia', T('VF/VT تهدیدکننده حیات — وریدی: حدود ۱۰۰۰ mg در ۲۴ ساعت اول', 'Life-threatening VF/VT — IV: about 1,000 mg over the first 24 h'), A18, 'notCalculated',
                    {'reason': T('برچسب: ۱۵۰ mg در ۱۰ دقیقه اول (۱۵ mg/min)، سپس ۳۶۰ mg در ۶ ساعت بعد (۱ mg/min)، سپس ۵۴۰ mg در ۱۸ ساعت باقی‌مانده (۰٫۵ mg/min)؛ پس از ۲۴ ساعت ادامه ۰٫۵ mg/min. در D5W رقیق شود؛ غلظت بالای ۲ mg/mL از ورید مرکزی.',
                                 'Label: 150 mg over the first 10 min (15 mg/min), then 360 mg over the next 6 h (1 mg/min), then 540 mg over the remaining 18 h (0.5 mg/min); continue 0.5 mg/min after 24 h. Dilute in D5W; concentrations >2 mg/mL via central line.')}, [R(Am, '2, Table 1')], allowed=['inj-50'])], pin_old=True)
p = find('amiodarone'); dd = json.load(open(p))
if not any(c['id'] == 'iv-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('iv-ci', 'تزریقی: حساسیت (از جمله به ید)، شوک کاردیوژنیک، برادی‌کاردی سینوسی شدید، بلوک AV درجه ۲ یا ۳ بدون پیس‌میکر.', 'Injection: hypersensitivity (including to iodine), cardiogenic shock, marked sinus bradycardia, 2nd/3rd-degree AV block without a pacemaker.', [R(Am, '4')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Lz = fda('lorazepam-inj', 'FDA Lorazepam inj.', 'Lorazepam injection 2 and 4 mg/mL (Hospira) — Prescribing Information', sid('lorazinj')); d = R(Lz, 'Dosage and Administration — Status Epilepticus')
patch('lorazepam', add_forms=[inj('inj-2', '2 mg/mL injection', 2, 1, Lz, 'How Supplied'), inj('inj-4', '4 mg/mL injection', 4, 1, Lz, 'How Supplied')],
      add_regs=[reg('se', 'status-epilepticus', T('صرع پایدار — ۱۸ سال به بالا: ۴ mg وریدی آهسته (۲ mg/min)', 'Status epilepticus — ≥18 y: 4 mg IV slowly (2 mg/min)'), A18, 'fixed', {'perDose': 4, 'dosesPerDay': 1}, [d], allowed=['inj-2', 'inj-4'], dur=ONE,
                    notes=[note('اگر تشنج پس از ۱۰ تا ۱۵ دقیقه ادامه یافت یا برگشت، یک دوز دیگر ۴ mg آهسته. تجربه با دوزهای بیشتر بسیار محدود. وسایل حفظ راه هوایی در دسترس باشد. ایمنی در کودکان ثابت نشده.',
                                'If seizures continue or recur after 10–15 min, one more 4 mg dose slowly. Very limited experience with further doses. Airway equipment must be at hand. Safety in children not established.', [d])])],
      add_exs=[ex('se', 'inj-2', {'perDose': 4, 'mlPerDose': 2}, ageYears=40, weightKg=70)], pin_old=True)
p = find('lorazepam'); dd = json.load(open(p))
if not any(c['id'] == 'inj-ci' for c in dd['contraindications']):
    dd['contraindications'].append(CI('inj-ci', 'تزریقی: گلوکوم زاویه بسته حاد، آپنه خواب، نارسایی شدید تنفسی (جز بیمار تحت تهویه)، تزریق داخل شریانی، نوزاد نارس (بنزیل الکل).', 'Injection: acute narrow-angle glaucoma, sleep apnoea, severe respiratory insufficiency (except ventilated patients), intra-arterial injection, premature infants (benzyl alcohol).', [R(Lz, 'Contraindications')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Lv = fda('levetiracetam-inj', 'FDA Levetiracetam IV', 'Levetiracetam in sodium chloride injection (WG Critical Care) — Prescribing Information', sid('levinj'))
BAGS = [f'bag-{m}' for m in (5, 10, 15)]
d0 = patch('levetiracetam', add_forms=[liquid(f'bag-{m}', m, 1, f'{m * 100} mg/100 mL ready-to-use IV bag ({m} mg/mL)', [R(Lv, '3')], form_='injection', route='iv') for m in (5, 10, 15)], pin_old=True)
p = find('levetiracetam'); dd = json.load(open(p))
for r in dd['regimens']:
    if r['id'] == 'adult':
        r['allowedFormulations'] = [f for f in r['allowedFormulations'] if f not in BAGS] + BAGS
        r['notes'] = [n for n in r.get('notes', []) if 'IV bag' not in n['text']['en']] + [note('کیسه وریدی (۱۶ سال به بالا، وقتی خوراکی ممکن نیست): همان دوز و دفعات خوراکی، انفوزیون ۱۵ دقیقه‌ای، بدون رقیق‌سازی.', 'IV bag (≥16 y, when oral use is not feasible): same dose and frequency as oral, 15-minute infusion, no further dilution.', [R(Lv, '1'), R(Lv, '2.1'), R(Lv, '2.3')])]
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

On = fda('ondansetron-inj', 'FDA Ondansetron inj.', 'Ondansetron injection 2 mg/mL (Civica) — Prescribing Information', sid('ondinj'))
patch('ondansetron', add_forms=[inj('inj-2', '2 mg/mL injection (2 mL vial)', 2, 1, On, '3', route='iv')],
      add_regs=[reg('ponv-adult', 'nausea-vomiting', T('پیشگیری از تهوع و استفراغ پس از عمل — بالای ۱۲ سال: ۴ mg وریدی یا عضلانی', 'Postoperative nausea/vomiting prevention — >12 y: 4 mg IV or IM'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 4, 'dosesPerDay': 1}, [R(On, '2.2, Table 1')], allowed=['inj-2'], dur=ONE,
                    notes=[note('وریدی حداقل در ۳۰ ثانیه (ترجیحاً ۲ تا ۵ دقیقه)؛ پیش از القای بیهوشی یا پس از عمل. دوز دوم ۴ mg فایده اضافه ندارد.', 'IV over at least 30 s (preferably 2–5 min); before induction or postoperatively. A second 4 mg dose adds no benefit.', [R(On, '2.2')])]),
                reg('ponv-child', 'nausea-vomiting', T('تهوع و استفراغ پس از عمل — ۱ ماه تا ۱۲ سال: ۰٫۱ mg/kg وریدی (بالای ۴۰ kg: ۴ mg)', 'Postoperative nausea/vomiting — 1 month to 12 y: 0.1 mg/kg IV (>40 kg: 4 mg)'), {'minAge': age(1, 'month'), 'maxAge': age(12, 'year')}, 'weightBased', {'perKgPerDay': 0.1, 'dividedDoses': 1}, [R(On, '2.2, Table 1')], allowed=['inj-2'],
                    limits={'maxPerDose': 4, 'refs': [R(On, '2.2, Table 1')]}, dur=ONE),
                reg('cinv-iv', 'cinv', T('تهوع شیمی‌درمانی — ۶ ماه به بالا: ۰٫۱۵ mg/kg وریدی، ۳ دوز (حداکثر ۱۶ mg در هر دوز)', 'Chemotherapy nausea — ≥6 months: 0.15 mg/kg IV, 3 doses (max 16 mg per dose)'), {'minAge': age(6, 'month')}, 'weightBased', {'perKgPerDose': 0.15, 'intervalHours': 4}, [R(On, '2.1'), R(On, '2')], allowed=['inj-2'],
                    limits={'maxPerDose': 16, 'refs': [R(On, '2')]}, dur=ONE,
                    notes=[note('فقط ۳ دوز: ۳۰ دقیقه پیش از شیمی‌درمانی و ۴ و ۸ ساعت پس از دوز اول؛ در ۵۰ mL رقیق و در ۱۵ دقیقه انفوزیون. نارسایی شدید کبد: حداکثر ۸ mg در روز.', 'Three doses only: 30 min before chemotherapy and 4 and 8 h after the first; dilute in 50 mL and infuse over 15 min. Severe hepatic impairment: max 8 mg/day.', [R(On, '2'), R(On, '2.3')])])],
      add_exs=[ex('ponv-adult', 'inj-2', {'perDose': 4, 'mlPerDose': 2}, ageYears=40, weightKg=70), ex('ponv-child', 'inj-2', {'perDose': 2, 'mlPerDose': 1}, ageYears=6, weightKg=20),
               ex('cinv-iv', 'inj-2', {'perDose': 3, 'mlPerDose': 1.5}, ageYears=6, weightKg=20)], pin_old=True)

# --- antidotes ---
Pr = fda('protopam', 'FDA Protopam', 'Protopam (pralidoxime chloride) for injection — Prescribing Information', sid('protopam')); d = R(Pr, 'Dosage and Administration')
drug('pralidoxime', 'various', 'پرالیدوکسیم', 'Pralidoxime', T('بازفعال‌کننده کولین‌استراز (پادزهر)', 'Cholinesterase reactivator (antidote)'), [{'name': 'Protopam', 'market': 'US'}], ['protopam', 'پروتوپام', '2-PAM', 'پرالیدوکسیم'],
     [pv('vial-1g', '1 g vial (reconstitute; 10–20 mg/mL for IV infusion)', 1000, Pr, 'How Supplied')],
     [reg('adult', 'organophosphate-poisoning', T('مسمومیت ارگانوفسفره — بزرگسال: ۱۰۰۰ تا ۲۰۰۰ mg وریدی در ۱۵ تا ۳۰ دقیقه', 'Organophosphate poisoning — adult: 1,000–2,000 mg IV over 15–30 min'), {'minAge': age(17, 'year')}, 'fixed', {'perDose': 1000, 'perDoseMax': 2000, 'dosesPerDay': 1}, [R(Pr, 'Dosage and Administration — Adult intravenous dosing')], dur=ONE,
          notes=[note('پس از آتروپین (اول هیپوکسی اصلاح شود). در ۱۰۰ mL سالین در ۱۵ تا ۳۰ دقیقه؛ حداکثر ۲۰۰ mg/min. اگر ضعف عضلانی ماند، دوز دوم پس از حدود ۱ ساعت و سپس هر ۱۰ تا ۱۲ ساعت. بیش از ۳۶ ساعت پس از قطع مواجهه فایده کمی دارد؛ ۴۸ تا ۷۲ ساعت مراقبت.',
                      'After atropine (correct hypoxia first). In 100 mL saline over 15–30 min; max 200 mg/min. If weakness persists, second dose after about 1 h, then every 10–12 h. Little benefit beyond 36 h after exposure ends; observe 48–72 h.', [d])]),
      reg('child', 'organophosphate-poisoning', T('مسمومیت ارگانوفسفره — ۱۶ سال و کمتر: ۲۰ تا ۵۰ mg/kg وریدی (حداکثر ۲۰۰۰ mg)', 'Organophosphate poisoning — ≤16 y: 20–50 mg/kg IV (max 2,000 mg)'), {'maxAge': age(17, 'year')}, 'weightBased', {'perKgPerDay': 20, 'perKgPerDayMax': 50, 'dividedDoses': 1}, [R(Pr, 'Dosage and Administration — Pediatric intravenous dosing')],
          limits={'maxPerDose': 2000, 'refs': [R(Pr, 'Dosage and Administration — Pediatric intravenous dosing')]}, dur=ONE,
          notes=[note('در ۱۵ تا ۳۰ دقیقه. ادامه: انفوزیون مداوم ۱۰ تا ۲۰ mg/kg/ساعت، یا دوز دوم پس از ۱ ساعت و تکرار هر ۱۰ تا ۱۲ ساعت.', 'Over 15–30 min. Then continuous infusion 10–20 mg/kg/h, or a second dose after 1 h and repeats every 10–12 h.', [R(Pr, 'Dosage and Administration — Pediatric intravenous dosing')])])],
     [CI('rel', 'منع مطلق ندارد؛ منع نسبی: حساسیت به دارو.', 'No absolute contraindications; relative: hypersensitivity to the drug.', [R(Pr, 'Contraindications')], sev='warn')],
     inter=[IA('op', 'در مسمومیت ارگانوفسفره از مورفین، تئوفیلین، آمینوفیلین، رزرپین و فنوتیازین‌ها پرهیز شود؛ سوکسینیل‌کولین با احتیاط.', 'In organophosphate poisoning avoid morphine, theophylline, aminophylline, reserpine and phenothiazines; succinylcholine with caution.', [d])],
     exs=[ex('adult', 'vial-1g', {'perDose': 1000, 'upperPerDose': 2000}, ageYears=40, weightKg=70), ex('child', 'vial-1g', {'perDose': 400, 'upperPerDose': 1000}, ageYears=6, weightKg=20)])

Df = fda('deferoxamine', 'FDA Deferoxamine', 'Deferoxamine mesylate for injection (Fresenius Kabi) — Prescribing Information', sid('desferal')); d = R(Df, '2.1')
drug('deferoxamine', 'various', 'دفروکسامین', 'Deferoxamine', T('شلاتور آهن', 'Iron chelator'), [{'name': 'Desferal', 'market': 'US'}], ['desferal', 'دسفرال', 'دفروکسامین'],
     [pv('vial-500', '500 mg vial', 500, Df, 'How Supplied'), pv('vial-2g', '2 g vial', 2000, Df, 'How Supplied')],
     [reg('acute', 'iron-poisoning', T('مسمومیت حاد آهن — ۱۰۰۰ mg، سپس ۵۰۰ mg هر ۴ تا ۱۲ ساعت (حداکثر ۶ g در ۲۴ ساعت)', 'Acute iron poisoning — 1,000 mg, then 500 mg every 4–12 h (max 6 g in 24 h)'), {}, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [d], limits={'maxPerDay': 6000, 'refs': [d]},
          notes=[note('بزرگسال و کودک. عضلانی برای بیمار بدون شوک؛ وریدی فقط در کلاپس قلبی-عروقی با سرعت حداکثر ۱۵ mg/kg/ساعت (دوزهای بعدی تا ۱۲۵ mg/ساعت). دوزهای بعدی ۵۰۰ mg بر اساس پاسخ بالینی.',
                      'Adults and children. IM for patients not in shock; IV only in cardiovascular collapse at ≤15 mg/kg/h (later doses up to 125 mg/h). Subsequent 500 mg doses by clinical response.', [d, R(Df, '2')])])],
     [CI('ci', 'حساسیت به دفروکسامین؛ بیماری شدید کلیه یا آنوری.', 'Hypersensitivity to deferoxamine; severe renal disease or anuria.', [R(Df, '4')])],
     exs=[ex('acute', 'vial-500', {'perDose': 1000}, ageYears=4, weightKg=16)])

Fm = fda('fomepizole', 'FDA Fomepizole', 'Fomepizole injection 1 g/mL (Zydus) — Prescribing Information', sid('fomepizole')); d = R(Fm, 'Dosage and Administration')
drug('fomepizole', 'various', 'فومپیزول', 'Fomepizole', T('مهارکننده الکل دهیدروژناز (پادزهر)', 'Alcohol dehydrogenase inhibitor (antidote)'), [{'name': 'Antizol', 'market': 'US'}], ['antizol', 'فومپیزول', 'پادزهر متانول'],
     [inj('vial-1g', '1 g/mL (1.5 g/1.5 mL) vial — dilute before infusion', 1000, 1, Fm, 'How Supplied')],
     [reg('std', 'toxic-alcohol', T('متانول یا اتیلن گلیکول — بارگذاری ۱۵ mg/kg، سپس ۱۰ mg/kg هر ۱۲ ساعت', 'Methanol or ethylene glycol — load 15 mg/kg, then 10 mg/kg every 12 h'), A18, 'weightBased', {'perKgPerDose': 10, 'intervalHours': 12}, [d],
          notes=[note('دوز اول ۱۵ mg/kg؛ سپس ۱۰ mg/kg هر ۱۲ ساعت برای ۴ دوز؛ سپس ۱۵ mg/kg هر ۱۲ ساعت تا سطح متانول یا اتیلن گلیکول غیرقابل‌اندازه‌گیری یا زیر ۲۰ mg/dL، بیمار بی‌علامت و pH طبیعی. هر دوز انفوزیون ۳۰ دقیقه‌ای. در همودیالیز هر ۴ ساعت. سرنگ پلی‌کربنات مصرف نشود. ایمنی در کودکان ثابت نشده.',
                      'First dose 15 mg/kg; then 10 mg/kg every 12 h for 4 doses; then 15 mg/kg every 12 h until methanol or ethylene glycol is undetectable or <20 mg/dL, the patient is asymptomatic and pH normal. Each dose over 30 min. Every 4 h during haemodialysis. Do not use polycarbonate syringes. Safety in children not established.', [d, R(Fm, 'Pediatric Use')])])],
     [CI('hyper', 'حساسیت جدی به فومپیزول یا سایر پیرازول‌ها.', 'Serious hypersensitivity to fomepizole or other pyrazoles.', [R(Fm, 'Contraindications')])],
     exs=[ex('std', 'vial-1g', {'perDose': 700, 'mlPerDose': 0.7}, ageYears=40, weightKg=70)])

Mb = fda('provayblue', 'FDA ProvayBlue', 'ProvayBlue (methylene blue) injection 0.5% — Prescribing Information', sid('provayblue')); d = R(Mb, '2.1')
drug('methylene-blue', 'various', 'متیلن بلو (تزریقی)', 'Methylene blue (injection)', T('پادزهر مت‌هموگلوبینمی', 'Methaemoglobinaemia antidote'), [{'name': 'ProvayBlue', 'market': 'US'}], ['provayblue', 'متیلن بلو', 'آبی متیلن'],
     [inj('amp-5', '5 mg/mL (10 mg/2 mL; 50 mg/10 mL)', 5, 1, Mb, '3')],
     [reg('std', 'methemoglobinemia', T('مت‌هموگلوبینمی اکتسابی — ۱ mg/kg وریدی در ۵ تا ۳۰ دقیقه', 'Acquired methaemoglobinaemia — 1 mg/kg IV over 5–30 min'), {}, 'weightBased', {'perKgPerDay': 1, 'dividedDoses': 1}, [d], dur=ONE,
          notes=[note('اگر مت‌هموگلوبین بالای ۳۰٪ ماند یا علائم ادامه یافت، ۱ mg/kg دیگر پس از ۱ ساعت؛ پس از ۲ دوز درمان دیگر. نارسایی متوسط تا شدید کلیه: فقط یک دوز. با D5W رقیق شود نه سالین؛ زیرجلدی نه.',
                      'If methaemoglobin stays >30% or symptoms persist, one more 1 mg/kg after 1 h; after 2 doses use other treatment. Moderate–severe renal impairment: single dose only. Dilute in D5W, not saline; never subcutaneous.', [d, R(Mb, '2.2'), R(Mb, '2.3')])])],
     [CI('ci', 'حساسیت شدید به متیلن بلو یا رنگ‌های تیازینی؛ کمبود G6PD (همولیز).', 'Severe hypersensitivity to methylene blue or thiazine dyes; G6PD deficiency (haemolysis).', [R(Mb, '4')])],
     warn=[W('هشدار جعبه‌ای: سندرم سروتونین با SSRI، SNRI، MAOI و اپیوئیدها — همزمان مصرف نشود.', 'Boxed warning: serotonin syndrome with SSRIs, SNRIs, MAOIs and opioids — avoid concomitant use.', [R(Mb, 'Boxed Warning')])],
     inter=[IA('serotonergic', 'SSRI، SNRI، MAOI و اپیوئیدها: سندرم سروتونین جدی یا کشنده.', 'SSRIs, SNRIs, MAOIs and opioids: serious or fatal serotonin syndrome.', [R(Mb, 'Boxed Warning')])],
     exs=[ex('std', 'amp-5', {'perDose': 70, 'mlPerDose': 14}, ageYears=40, weightKg=70)])

Pt = fda('protamine', 'FDA Protamine', 'Protamine sulfate injection 10 mg/mL (Fresenius Kabi) — Prescribing Information', sid('protamine')); d = R(Pt, 'Dosage and Administration')
drug('protamine', 'various', 'پروتامین سولفات', 'Protamine sulfate', T('خنثی‌کننده هپارین', 'Heparin antagonist'), [{'name': 'Protamine', 'market': 'US'}], ['protamine', 'پروتامین', 'خنثی کننده هپارین'],
     [inj('vial-10', '10 mg/mL (50 mg/5 mL; 250 mg/25 mL)', 10, 1, Pt, 'How Supplied')],
     [reg('heparin', 'heparin-overdose', T('خنثی‌سازی هپارین — ۱ mg برای هر ۱۰۰ واحد هپارین (حداکثر ۵۰ mg در هر تزریق)', 'Heparin neutralisation — 1 mg per 100 units heparin (max 50 mg per injection)'), {}, 'notCalculated',
          {'reason': T('برچسب: هر ۱ mg پروتامین دست‌کم ۱۰۰ واحد هپارین را خنثی می‌کند. وریدی بسیار آهسته در ۱۰ دقیقه، هر بار حداکثر ۵۰ mg. چون هپارین سریع از خون پاک می‌شود، دوز با گذشت زمان کم می‌شود (مثلاً ۳۰ دقیقه پس از هپارین، نصف دوز). دوز با تست‌های انعقادی تنظیم شود.',
                       'Label: each mg neutralises at least 100 USP heparin units. Very slow IV over 10 min, no more than 50 mg per dose. Because heparin clears quickly, the dose falls with time (e.g. half the dose 30 min after heparin). Guide by coagulation tests.')}, [d])],
     [CI('ci', 'سابقه عدم تحمل پروتامین.', 'Previous intolerance to protamine.', [R(Pt, 'Contraindications')])],
     warn=[W('تزریق سریع: افت شدید فشار و واکنش آنافیلاکتوئید؛ امکانات درمان شوک آماده باشد. پس از جراحی قلب احتمال بازگشت خونریزی.', 'Rapid injection: severe hypotension and anaphylactoid reactions; shock treatment must be available. Rebound bleeding possible after cardiac surgery.', [R(Pt, 'Warnings')])])

Dg = fda('digifab', 'FDA DigiFab', 'DigiFab (digoxin immune fab, ovine) — Prescribing Information', sid('digifab')); d = R(Dg, '2.1')
drug('digoxin-immune-fab', 'various', 'آنتی‌بادی ضد دیگوکسین (DigiFab)', 'Digoxin immune fab (DigiFab)', T('پادزهر دیگوکسین', 'Digoxin antidote'), [{'name': 'DigiFab', 'market': 'US'}], ['digifab', 'دیجی فب', 'digibind', 'پادزهر دیگوکسین'],
     [pv('vial-40', '40 mg vial (binds about 0.5 mg digoxin)', 40, Dg, '3')],
     [reg('std', 'digoxin-toxicity', T('مسمومیت با دیگوکسین — تعداد ویال بر اساس مقدار مصرف یا سطح سرمی', 'Digoxin toxicity — vials by amount ingested or serum level'), {}, 'notCalculated',
          {'reason': T('برچسب: مصرف حاد با مقدار نامعلوم و بدون سطح: ۲۰ ویال (در کودک زیر ۲۰ kg مراقب حجم؛ ۱۰ ویال و سپس ۱۰ ویال دیگر در صورت نیاز). مسمومیت مزمن بدون سطح: بزرگسال و کودک ۲۰ kg به بالا ۶ ویال؛ زیر ۲۰ kg یک ویال. مقدار مصرف معلوم: ویال = مقدار دیگوکسین (mg) ÷ ۰٫۵. سطح معلوم: ویال = (سطح دیگوکسین ng/mL × وزن kg) ÷ ۱۰۰. انفوزیون حداقل ۳۰ دقیقه.',
                       'Label: acute ingestion, unknown amount, no level: 20 vials (watch volume in children <20 kg; 10 vials then 10 more if needed). Chronic toxicity, no level: adults and children ≥20 kg 6 vials; <20 kg 1 vial. Known amount: vials = digoxin ingested (mg) ÷ 0.5. Known level: vials = (serum digoxin ng/mL × weight kg) ÷ 100. Infuse over at least 30 min.')}, [d, R(Dg, '2.2')])],
     [])

Ck = fda('cyanokit', 'FDA Cyanokit', 'Cyanokit (hydroxocobalamin) 5 g for injection — Prescribing Information', sid('cyanokit')); d = R(Ck, '2.2')
drug('hydroxocobalamin-cyanokit', 'various', 'هیدروکسوکوبالامین (سیانوکیت)', 'Hydroxocobalamin (Cyanokit)', T('پادزهر سیانید', 'Cyanide antidote'), [{'name': 'Cyanokit', 'market': 'US'}], ['cyanokit', 'سیانوکیت', 'پادزهر سیانور'],
     [pv('vial-5g', '5 g vial (reconstitute with 200 mL; 25 mg/mL)', 5000, Ck, '3')],
     [reg('adult', 'cyanide-poisoning', T('مسمومیت با سیانید — بزرگسال: ۵ g وریدی در ۱۵ دقیقه', 'Cyanide poisoning — adult: 5 g IV over 15 min'), A18, 'fixed', {'perDose': 5000, 'dosesPerDay': 1}, [d], dur=ONE,
          notes=[note('در صورت شک بالا بی‌درنگ. بسته به شدت، دوز دوم ۵ g (مجموع ۱۰ g) در ۱۵ دقیقه تا ۲ ساعت. حمایت راه هوایی، اکسیژن و گردش خون نباید به تأخیر بیفتد.', 'Give without delay if suspicion is high. Depending on severity, a second 5 g dose (total 10 g) over 15 min to 2 h. Do not delay airway, oxygen and circulatory support.', [d, R(Ck, '2.1')])])],
     [],
     exs=[ex('adult', 'vial-5g', {'perDose': 5000}, ageYears=40, weightKg=70)])

Ac = fda('acetadote', 'FDA Acetadote', 'Acetadote (acetylcysteine) injection 200 mg/mL — Prescribing Information', sid('acetadote')); da = R(Ac, '2.5, Table 2')
ACN = note('رژیم سه‌کیسه‌ای (مجموع ۳۰۰ mg/kg در ۲۱ ساعت): کیسه ۱: ۱۵۰ mg/kg در ۱ ساعت؛ کیسه ۲: ۵۰ mg/kg در ۴ ساعت؛ کیسه ۳: ۱۰۰ mg/kg در ۱۶ ساعت. حجم رقیق‌سازی بر اساس وزن طبق جدول ۲. وزن ۱۰۰ kg و بیشتر: سقف ۱۵۰۰۰ / ۵۰۰۰ / ۱۰۰۰۰ mg. حجم نمایش‌داده‌شده از محلول ۲۰۰ mg/mL پیش از رقیق‌سازی است.',
           'Three-bag regimen (300 mg/kg over 21 h): bag 1 150 mg/kg over 1 h; bag 2 50 mg/kg over 4 h; bag 3 100 mg/kg over 16 h. Diluent volume by weight per Table 2. 100 kg or more: capped at 15,000 / 5,000 / 10,000 mg. The volume shown is of the 200 mg/mL vial before dilution.', [da, R(Ac, '2.3')])
bag = lambda id, fa, en, mgkg, cap: reg(id, 'acetaminophen-overdose', T(fa, en), {'minWeightKg': 5}, 'weightBased', {'perKgPerDay': mgkg, 'dividedDoses': 1}, [da], allowed=['inj-200'], limits={'maxPerDose': cap, 'refs': [da]}, dur=ONE, notes=[ACN])
patch('acetylcysteine', add_forms=[inj('inj-200', '200 mg/mL (6 g/30 mL) vial — dilute before IV infusion', 200, 1, Ac, '3')],
      add_regs=[bag('iv-bag1', 'وریدی — کیسه ۱ (بارگذاری): ۱۵۰ mg/kg در ۱ ساعت', 'IV — bag 1 (loading): 150 mg/kg over 1 h', 150, 15000),
                bag('iv-bag2', 'وریدی — کیسه ۲: ۵۰ mg/kg در ۴ ساعت', 'IV — bag 2: 50 mg/kg over 4 h', 50, 5000),
                bag('iv-bag3', 'وریدی — کیسه ۳: ۱۰۰ mg/kg در ۱۶ ساعت', 'IV — bag 3: 100 mg/kg over 16 h', 100, 10000)],
      add_exs=[ex('iv-bag1', 'inj-200', {'perDose': 10500, 'mlPerDose': 52.5}, ageYears=40, weightKg=70), ex('iv-bag2', 'inj-200', {'perDose': 3500, 'mlPerDose': 17.5}, ageYears=40, weightKg=70),
               ex('iv-bag3', 'inj-200', {'perDose': 7000, 'mlPerDose': 35}, ageYears=40, weightKg=70)], pin_old=True)
p = find('acetylcysteine'); dd = json.load(open(p))
if not any(c['id'] == 'iv-hyper' for c in dd['contraindications']):
    dd['contraindications'].append(CI('iv-hyper', 'تزریقی: سابقه واکنش حساسیتی به استیل‌سیستئین.', 'Injection: previous hypersensitivity reaction to acetylcysteine.', [R(Ac, '4')]))
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

As = dy('ir-darooyab-antiscorpion', 'Darooyab Antiscorpion', 'ضدسم عقرب — موارد مصرف، هشدارها و اشکال دارویی', 'G-3514/Antiscorpion-Venum-Serum')
drug('antiscorpion-venom', 'various', 'ضدسم عقرب (پادزهر عقرب)', 'Scorpion antivenom', T('آنتی‌سرم اسبی', 'Equine antiserum'), [{'name': 'Alborz Daru antiscorpion', 'market': 'IR'}], ['antiscorpion', 'پادزهر عقرب', 'سرم ضد عقرب'],
     [unitform('vial-5', 'injection', 'im', '5 mL vial', [R(As, 'اشکال دارویی')], unit='mL', per='vial', markets=('IR',))],
     [reg('sting', 'scorpion-sting', T('عقرب‌زدگی', 'Scorpion sting'), {}, 'notCalculated',
          {'reason': T(NOT_RELIABLE + 'دارویاب: علیه سم عقرب‌های Buthotus saulcyi، Androctonus crassicauda، Odontobuthus doriae، Scorpio maurus و Mesobuthus eupeus. پیش از تزریق تست حساسیت به سرم اسب؛ اکسیژن و وسایل احیا آماده؛ عضلانی آهسته یا در صورت نیاز وریدی بسیار آهسته. دوز عددی در منبع نیست.',
                       NOT_RELIABLE_EN + 'Darooyab: covers venom of Buthotus saulcyi, Androctonus crassicauda, Odontobuthus doriae, Scorpio maurus and Mesobuthus eupeus. Skin-test for horse-serum sensitivity first; have oxygen and resuscitation ready; slow IM or, if needed, very slow IV. The source gives no numeric dose.')}, [R(As, 'هشدارها')])],
     [CI('horse', 'حساسیت به سرم اسب (تست حساسیت پیش از مصرف).', 'Horse-serum sensitivity (skin test before use).', [R(As, 'هشدارها')], sev='warn')])

Sv = dy('ir-darooyab-antisnake', 'Darooyab Antisnake', 'ضدسم مار — موارد مصرف، هشدارها و اشکال دارویی', 'G-3517/Antisnake-Venum-Serum')
drug('antisnake-venom', 'various', 'ضدسم مار (پادزهر مار)', 'Snake antivenom (polyvalent)', T('آنتی‌سرم اسبی', 'Equine antiserum'), [{'name': 'Alborz Daru antisnake', 'market': 'IR'}], ['antisnake', 'پادزهر مار', 'سرم ضد مار'],
     [unitform('vial-10', 'injection', 'iv', '10 mL vial (hexavalent)', [R(Sv, 'اشکال دارویی')], unit='mL', per='vial', markets=('IR',))],
     [reg('bite', 'snakebite', T('مارگزیدگی', 'Snakebite'), {}, 'notCalculated',
          {'reason': T(NOT_RELIABLE + 'دارویاب: علیه سم ۶ مار (افعی، کبرای آسیای میانه، Echis، Pseudocerastes، Agkistrodon و Vipera xanthina). وریدی بسیار آهسته ارجح است. در کودکان مقدار پادزهر نباید بر اساس وزن کم شود (ممکن است بیشتر لازم باشد). پیش از تزریق تست حساسیت؛ شوک مانند شوک هیپوولمیک درمان شود. دوز عددی در منبع نیست.',
                       NOT_RELIABLE_EN + 'Darooyab: covers venom of six snakes (Vipera, Naja naja oxiana, Echis, Pseudocerastes, Agkistrodon, Vipera xanthina). Very slow IV preferred. In children the amount must NOT be reduced by weight (they may need more). Skin test first; treat shock as hypovolaemic shock. The source gives no numeric dose.')}, [R(Sv, 'هشدارها')])],
     [CI('horse', 'حساسیت به سرم اسب (تست حساسیت پیش از مصرف).', 'Horse-serum sensitivity (skin test before use).', [R(Sv, 'هشدارها')], sev='warn')])

# --- immunoglobulins ---
Tg = fda('hypertet', 'FDA HyperTET', 'HyperTET (tetanus immune globulin, human) 250 units — Prescribing Information', sid('hypertet')); d = R(Tg, 'Dosage and Administration')
drug('tetanus-immune-globulin', 'antineoplastic-immunomodulating', 'ایمونوگلوبولین کزاز (TIG)', 'Tetanus immune globulin (human)', T('ایمونوگلوبولین اختصاصی', 'Specific immune globulin'), [{'name': 'HyperTET', 'market': 'US'}], ['hypertet', 'TIG', 'تتابولین', 'ایمونوگلوبولین کزاز'],
     [form('syr-250', 'injection', 'im', '250 units prefilled syringe', 250, 'unit', [R(Tg, 'How Supplied')], per='vial')],
     [reg('std', 'tetanus-prophylaxis', T('پیشگیری از کزاز — ۷ سال به بالا: ۲۵۰ واحد عضلانی عمیق', 'Tetanus prophylaxis — ≥7 y: 250 units deep IM'), {'minAge': age(7, 'year')}, 'fixed', {'perDose': 250, 'dosesPerDay': 1}, [d], unit='unit', dur=ONE,
          notes=[note('همزمان واکسن Td در اندام دیگر با سرنگ جدا؛ سپس تکمیل سری واکسن.', 'Give Td vaccine at the same time in another limb with a separate syringe; then complete the vaccine series.', [d])]),
      reg('child', 'tetanus-prophylaxis', T('پیشگیری از کزاز — زیر ۷ سال: ۴ واحد/kg یا کل سرنگ ۲۵۰ واحد', 'Tetanus prophylaxis — <7 y: 4 units/kg or the whole 250-unit syringe'), {'maxAge': age(7, 'year')}, 'weightBased', {'perKgPerDay': 4, 'dividedDoses': 1}, [d], unit='unit', dur=ONE,
          notes=[note('برچسب: ممکن است بهتر باشد بدون توجه به وزن کل ۲۵۰ واحد داده شود، چون مقدار سم تولیدشده در کودک و بزرگسال یکسان است. همزمان DTaP یا DT.', 'Label: it may be advisable to give the whole 250 units regardless of size, since the same amount of toxin is produced in a child as in an adult. Give DTaP or DT at the same time.', [d])])],
     [],
     exs=[ex('std', 'syr-250', {'perDose': 250}, ageYears=30, weightKg=70), ex('child', 'syr-250', {'perDose': 56}, ageYears=4, weightKg=14)])

Rg = fda('hyperrab', 'FDA HyperRAB', 'HyperRAB (rabies immune globulin, human) 300 IU/mL — Prescribing Information', sid('hyperrab')); d = R(Rg, '2.1')
drug('rabies-immune-globulin', 'antineoplastic-immunomodulating', 'ایمونوگلوبولین هاری (HRIG)', 'Rabies immune globulin (human)', T('ایمونوگلوبولین اختصاصی', 'Specific immune globulin'), [{'name': 'HyperRAB', 'market': 'US'}], ['hyperrab', 'HRIG', 'سرم ضد هاری', 'ایمونوگلوبولین هاری'],
     [liquid('vial-300', 300, 1, '300 IU/mL (1, 3, 5 mL vials)', [R(Rg, '3')], form_='injection', route='im', unit='unit'),
      liquid('vial-150', 150, 1, '150 IU/mL (older/other products, e.g. sold in Iran) — check the vial strength', [R(Rg, '2.2'), R('darooyab-generic', 'G-3504/Rabies-Immunoglobulins')], form_='injection', route='im', unit='unit', markets=('IR',))],
     [reg('pep', 'rabies-exposure', T('پیشگیری پس از تماس با هاری — ۲۰ IU/kg یک بار (همه سنین)', 'Rabies post-exposure prophylaxis — 20 IU/kg once (all ages)'), {}, 'weightBased', {'perKgPerDay': 20, 'dividedDoses': 1}, [d], unit='unit', dur=ONE,
          limits={'maxPerKgPerDose': 20, 'refs': [d]},
          notes=[note('فقط برای افرادی که قبلاً واکسن نزده‌اند، همراه واکسن (روز ۰ و حداکثر تا روز ۷). تا جای ممکن کل دوز داخل و اطراف زخم تزریق شود؛ باقی‌مانده عضلانی دور از محل واکسن. بیشتر از دوز توصیه‌شده نشود (پاسخ واکسن را کم می‌کند).',
                      'Only for previously unvaccinated people, together with vaccine (day 0, no later than day 7). Infiltrate as much as possible into and around the wound; the rest IM away from the vaccine site. Do not exceed the dose (it blunts the vaccine response).', [d, R(Rg, '2.3')])])],
     [],
     exs=[ex('pep', 'vial-300', {'perDose': 1400, 'mlPerDose': 4.67}, ageYears=30, weightKg=70), ex('pep', 'vial-300', {'perDose': 300, 'mlPerDose': 1}, ageYears=3, weightKg=15), ex('pep', 'vial-150', {'perDose': 1400, 'mlPerDose': 9.33}, ageYears=30, weightKg=70)])

Hg = fda('hyperhep', 'FDA HyperHEP B', 'HyperHEP B (hepatitis B immune globulin, human) — Prescribing Information', sid('hyperhep')); d = R(Hg, 'Dosage and Administration')
drug('hepatitis-b-immune-globulin', 'antineoplastic-immunomodulating', 'ایمونوگلوبولین هپاتیت B (HBIG)', 'Hepatitis B immune globulin (human)', T('ایمونوگلوبولین اختصاصی', 'Specific immune globulin'), [{'name': 'HyperHEP B', 'market': 'US'}], ['hyperhep b', 'HBIG', 'ایمونوگلوبولین هپاتیت'],
     [form('vial', 'injection', 'im', 'Single-dose syringe or vial (0.5, 1 or 5 mL)', 1, 'mL', [R(Hg, 'How Supplied')], vol=1)],
     [reg('exposure', 'hbv-exposure', T('تماس با خون HBsAg مثبت (سوزن‌زدگی، مخاط) یا تماس جنسی — ۰٫۰۶ mL/kg عضلانی', 'Exposure to HBsAg-positive blood (needlestick, mucosa) or sexual exposure — 0.06 mL/kg IM'), {'minAge': age(1, 'month')}, 'weightBased', {'perKgPerDay': 0.06, 'dividedDoses': 1}, [d], unit='mL', dur=ONE,
          notes=[note('هرچه زودتر و ترجیحاً ظرف ۲۴ ساعت (فایده پس از ۷ روز نامشخص؛ در تماس جنسی تا ۲ هفته). همراه شروع یا تکمیل سری واکسن هپاتیت B طبق جدول ۱ برچسب.', 'As soon as possible, preferably within 24 h (value after 7 days unclear; within 2 weeks for sexual exposure). Start or complete the hepatitis B vaccine series per label Table 1.', [d])]),
      reg('newborn', 'hbv-exposure', T('نوزاد مادر HBsAg مثبت — ۰٫۵ mL عضلانی ترجیحاً ظرف ۱۲ ساعت از تولد', 'Infant of HBsAg-positive mother — 0.5 mL IM, preferably within 12 h of birth'), {'maxAge': age(1, 'month')}, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Hg, 'Dosage and Administration — Prophylaxis of infants')], unit='mL', dur=ONE,
          notes=[note('اثر پس از ۴۸ ساعت به‌شدت کم می‌شود. همراه واکسن هپاتیت B (۳ دوز ۰٫۵ mL).', 'Efficacy falls sharply if delayed beyond 48 h. Give with hepatitis B vaccine (3 doses of 0.5 mL).', [R(Hg, 'Dosage and Administration — Prophylaxis of infants')])])],
     [],
     exs=[ex('exposure', 'vial', {'perDose': 4.2, 'mlPerDose': 4.2}, ageYears=30, weightKg=70), ex('newborn', 'vial', {'perDose': 0.5, 'mlPerDose': 0.5}, ageDays=1, weightKg=3.3)])

# --- vaccines ---
def vaccine(id, fa, en, cls_fa, cls_en, brand, syn, src, frm, regs, ci, warn=(), exs=()):
    drug(id, 'anti-infectives', fa, en, T(cls_fa, cls_en), [{'name': brand, 'market': 'US'}], syn, [frm], regs, ci, warn=warn, exs=exs)
fx = lambda id, dis, fa, en, pop, ml, refs, notes: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': ml, 'dosesPerDay': 1}, refs, unit='mL', dur=ONE, notes=notes)
LIVE = lambda src: [CI('live', 'بارداری، نقص ایمنی، بیماری تب‌دار متوسط تا شدید، سل فعال درمان‌نشده (واکسن زنده).', 'Pregnancy, immunosuppression, moderate or severe febrile illness, active untreated tuberculosis (live vaccine).', [R(src, '4')]),
                    CI('allergy', 'واکنش آلرژیک شدید به اجزای واکسن (از جمله ژلاتین و نئومایسین) یا دوز قبلی.', 'Severe allergic reaction to a vaccine component (including gelatin and neomycin) or a previous dose.', [R(src, '4')])]

Bx = fda('boostrix', 'FDA Boostrix', 'Boostrix (Tdap vaccine) — Prescribing Information', sid('boostrix')); d = R(Bx, '2.2')
vaccine('tdap-vaccine', 'واکسن کزاز، دیفتری و سیاه‌سرفه (Tdap)', 'Tdap vaccine (tetanus, diphtheria, pertussis)', 'واکسن غیرفعال', 'Inactivated vaccine', 'Boostrix', ['boostrix', 'adacel', 'Tdap', 'واکسن کزاز', 'سه گانه بزرگسال'], Bx,
        vac('syr-05', '0.5 mL prefilled syringe / vial', Bx),
        [fx('booster', 'immunization', 'یادآور — ۱۰ سال به بالا: ۰٫۵ mL عضلانی', 'Booster — ≥10 y: 0.5 mL IM', {'minAge': age(10, 'year')}, 0.5, [d],
            [note('۵ سال یا بیشتر پس از آخرین DTaP یا Td؛ دوز اضافه ۹ سال یا بیشتر پس از Tdap قبلی. بارداری: یک دوز در سه‌ماهه سوم برای محافظت نوزاد از سیاه‌سرفه.', '≥5 years after the last DTaP or Td; an additional dose ≥9 years after a previous Tdap. Pregnancy: one dose in the third trimester to protect the infant from pertussis.', [d])]),
         fx('wound', 'tetanus-prophylaxis', 'زخم مستعد کزاز — ۰٫۵ mL اگر ۵ سال یا بیشتر از واکسن قبلی گذشته', 'Tetanus-prone wound — 0.5 mL if ≥5 years since the last tetanus vaccine', {'minAge': age(10, 'year')}, 0.5, [d], [])],
        [CI('allergy', 'آنافیلاکسی به دوز قبلی واکسن حاوی کزاز، دیفتری یا سیاه‌سرفه یا اجزای Boostrix.', 'Anaphylaxis after a previous tetanus-, diphtheria- or pertussis-containing vaccine or to any Boostrix component.', [R(Bx, '4')]),
         CI('enceph', 'انسفالوپاتی ظرف ۷ روز پس از واکسن حاوی سیاه‌سرفه.', 'Encephalopathy within 7 days of a previous pertussis-containing vaccine.', [R(Bx, '4')])],
        exs=[ex('booster', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=30, weightKg=70), ex('wound', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=30, weightKg=70)])

Iv = fda('imovax', 'FDA Imovax Rabies', 'Imovax Rabies (rabies vaccine) — Prescribing Information', sid('imovax'))
vaccine('rabies-vaccine', 'واکسن هاری', 'Rabies vaccine', 'واکسن غیرفعال', 'Inactivated vaccine', 'Imovax Rabies', ['imovax', 'rabavert', 'واکسن هاری', 'verorab'], Iv,
        vac('vial-1', '1 mL dose after reconstitution', Iv),
        [fx('pep', 'rabies-exposure', 'پیشگیری پس از تماس — ۱ mL عضلانی در روزهای ۰، ۳، ۷، ۱۴ و ۲۸ (همه سنین)', 'Post-exposure — 1 mL IM on days 0, 3, 7, 14 and 28 (all ages)', {}, 1, [R(Iv, '2.2')],
            [note('افراد واکسن‌نزده یا با نقص ایمنی: روزهای ۰، ۳، ۷، ۱۴ و ۲۸ همراه ایمونوگلوبولین هاری در روز ۰. افرادی که قبلاً واکسن کامل زده‌اند: فقط روز ۰ و ۳، بدون ایمونوگلوبولین. دور از محل تزریق ایمونوگلوبولین.',
                  'Unvaccinated or immunosuppressed: days 0, 3, 7, 14 and 28, with rabies immune globulin on day 0. Previously vaccinated: days 0 and 3 only, no immune globulin. Away from the immune globulin site.', [R(Iv, '2.2')])]),
         fx('prep', 'immunization', 'پیشگیری پیش از تماس — ۱ mL عضلانی روز ۰ و ۷ (یا ۰، ۷ و ۲۱/۲۸)', 'Pre-exposure — 1 mL IM on days 0 and 7 (or 0, 7 and 21/28)', {}, 1, [R(Iv, '2.1')], [])],
        [CI('prep', 'پیشگیری پیش از تماس: حساسیت سیستمیک تهدیدکننده حیات به اجزای واکسن. پس از تماس منع مصرف ندارد.', 'Pre-exposure: life-threatening systemic hypersensitivity to a component. No contraindication after exposure.', [R(Iv, '4')], sev='warn')],
        exs=[ex('pep', 'vial-1', {'perDose': 1, 'mlPerDose': 1}, ageYears=8, weightKg=25), ex('prep', 'vial-1', {'perDose': 1, 'mlPerDose': 1}, ageYears=30, weightKg=70)])

Eb = fda('engerix', 'FDA Engerix-B', 'Engerix-B (hepatitis B vaccine) — Prescribing Information', sid('engerix')); d = R(Eb, '2.3')
vaccine('hepatitis-b-vaccine', 'واکسن هپاتیت B', 'Hepatitis B vaccine', 'واکسن نوترکیب', 'Recombinant vaccine', 'Engerix-B', ['engerix', 'heberbiovac', 'واکسن هپاتیت ب'], Eb,
        vac('susp', '0.5 mL (10 mcg) or 1 mL (20 mcg)', Eb),
        [reg('primary', 'immunization', T('سری اولیه — تولد تا ۱۹ سال: ۰٫۵ mL؛ ۲۰ سال به بالا: ۱ mL (ماه ۰، ۱ و ۶)', 'Primary series — birth to 19 y: 0.5 mL; ≥20 y: 1 mL (months 0, 1, 6)'), {}, 'ageBand',
             {'bands': [{'minAge': age(0, 'day'), 'maxAge': age(20, 'year'), 'perDose': 0.5, 'dosesPerDay': 1}, {'minAge': age(20, 'year'), 'maxAge': None, 'perDose': 1, 'dosesPerDay': 1}]}, [d], unit='mL', dur=ONE,
             notes=[note('۳ دوز در ماه ۰، ۱ و ۶. همودیالیز: ۲ mL در ماه ۰، ۱، ۲ و ۶. عضلانی، نه در باسن.', '3 doses at months 0, 1 and 6. Haemodialysis: 2 mL at months 0, 1, 2 and 6. IM, not in the buttock.', [d, R(Eb, '2.2')])])],
        [CI('allergy', 'آنافیلاکسی به دوز قبلی واکسن هپاتیت B یا اجزای آن (از جمله مخمر).', 'Anaphylaxis to a previous hepatitis B vaccine dose or a component (including yeast).', [R(Eb, '4')])],
        exs=[ex('primary', 'susp', {'perDose': 0.5, 'mlPerDose': 0.5}, ageDays=1, weightKg=3.3), ex('primary', 'susp', {'perDose': 1, 'mlPerDose': 1}, ageYears=30, weightKg=70)])

Fz = fda('fluzone', 'FDA Fluzone', 'Fluzone (influenza vaccine) 2026–2027 — Prescribing Information', sid('fluzone')); d = R(Fz, '2.1, Table 1')
vaccine('influenza-vaccine', 'واکسن آنفلوانزا (غیرفعال)', 'Influenza vaccine (inactivated)', 'واکسن غیرفعال', 'Inactivated vaccine', 'Fluzone', ['fluzone', 'vaxigrip', 'واکسن آنفولانزا', 'flu shot'], Fz,
        vac('syr-05', '0.5 mL prefilled syringe / multidose vial', Fz),
        [reg('std', 'immunization', T('سالانه — ۶ ماه به بالا: ۰٫۵ mL عضلانی (۶ تا ۳۵ ماه: ۰٫۲۵ یا ۰٫۵ mL)', 'Yearly — ≥6 months: 0.5 mL IM (6–35 months: 0.25 or 0.5 mL)'), {'minAge': age(6, 'month')}, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [d], unit='mL', dur=ONE,
             notes=[note('۶ ماه تا ۸ سال که قبلاً واکسن نزده‌اند: ۲ دوز با فاصله دست‌کم ۴ هفته. ۶ تا ۳۵ ماه: هر دوز ۰٫۲۵ یا ۰٫۵ mL. ۹ سال به بالا: یک دوز ۰٫۵ mL.', '6 months–8 y not previously vaccinated: 2 doses at least 4 weeks apart. 6–35 months: each dose 0.25 or 0.5 mL. ≥9 y: one 0.5 mL dose.', [d])])],
        [CI('allergy', 'واکنش آلرژیک شدید به اجزای واکسن (از جمله پروتئین تخم‌مرغ) یا دوز قبلی هر واکسن آنفلوانزا.', 'Severe allergic reaction to a component (including egg protein) or a previous dose of any influenza vaccine.', [R(Fz, '4')])],
        exs=[ex('std', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=30, weightKg=70)])

Mm = fda('mmr', 'FDA M-M-R II', 'M-M-R II (measles, mumps, rubella vaccine live) — Prescribing Information', sid('mmr')); d = R(Mm, '2.1')
vaccine('mmr-vaccine', 'واکسن سرخک، اوریون و سرخجه (MMR)', 'MMR vaccine (measles, mumps, rubella)', 'واکسن زنده ضعیف‌شده', 'Live attenuated vaccine', 'M-M-R II', ['mmr', 'ام ام آر', 'واکسن سرخک', 'priorix'], Mm,
        vac('vial-05', '0.5 mL dose after reconstitution', Mm),
        [fx('std', 'immunization', 'دو دوز ۰٫۵ mL — ۱۲ تا ۱۵ ماهگی و ۴ تا ۶ سالگی', 'Two 0.5 mL doses — at 12–15 months and 4–6 years', {'minAge': age(12, 'month')}, 0.5, [d],
            [note('دوز دوم پیش از ۴ سالگی هم مجاز است اگر دست‌کم ۱ ماه فاصله باشد. پیشگیری پس از تماس با سرخک: یک دوز ظرف ۷۲ ساعت. عضلانی یا زیرجلدی.', 'The second dose may be given before 4 y if at least 1 month apart. Measles post-exposure: one dose within 72 h. IM or SC.', [d])])],
        LIVE(Mm), exs=[ex('std', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=1, weightKg=10)])

Vx = fda('varivax', 'FDA Varivax', 'Varivax (varicella vaccine live) — Prescribing Information', sid('varivax')); d = R(Vx, '2.1')
vaccine('varicella-vaccine', 'واکسن آبله‌مرغان', 'Varicella vaccine', 'واکسن زنده ضعیف‌شده', 'Live attenuated vaccine', 'Varivax', ['varivax', 'واکسن آبله مرغان', 'varilrix'], Vx,
        vac('vial-05', '0.5 mL dose after reconstitution', Vx),
        [fx('std', 'immunization', 'دو دوز ۰٫۵ mL — ۱۲ ماه تا ۱۲ سال: ۱۲ تا ۱۵ ماهگی و ۴ تا ۶ سالگی؛ ۱۳ سال به بالا: با فاصله ۴ هفته', 'Two 0.5 mL doses — 12 months–12 y: at 12–15 months and 4–6 y; ≥13 y: 4 weeks apart', {'minAge': age(12, 'month')}, 0.5, [d],
            [note('کودک: حداقل ۳ ماه فاصله بین دو دوز. عضلانی یا زیرجلدی.', 'Children: at least 3 months between doses. IM or SC.', [d, R(Vx, '2.3')])])],
        LIVE(Vx), exs=[ex('std', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=1, weightKg=10)])

Gd = fda('gardasil', 'FDA Gardasil 9', 'Gardasil 9 (HPV 9-valent vaccine) — Prescribing Information', sid('gardasil')); d = R(Gd, '2.1')
vaccine('hpv-vaccine', 'واکسن HPV (پاپیلومای انسانی)', 'HPV vaccine (9-valent)', 'واکسن نوترکیب', 'Recombinant vaccine', 'Gardasil 9', ['gardasil', 'گارداسیل', 'واکسن زگیل تناسلی', 'HPV'], Gd,
        vac('syr-05', '0.5 mL prefilled syringe / vial', Gd),
        [fx('std', 'immunization', '۰٫۵ mL عضلانی — ۹ تا ۱۴ سال: ۲ دوز (ماه ۰ و ۶ تا ۱۲)؛ ۱۵ تا ۴۵ سال: ۳ دوز (ماه ۰، ۲ و ۶)', '0.5 mL IM — 9–14 y: 2 doses (0, 6–12 months); 15–45 y: 3 doses (0, 2, 6 months)', {'minAge': age(9, 'year'), 'maxAge': age(46, 'year')}, 0.5, [d],
            [note('اگر دوز دوم زودتر از ۵ ماه پس از اول زده شد، دوز سوم دست‌کم ۴ ماه بعد.', 'If the second dose is given less than 5 months after the first, give a third dose at least 4 months later.', [d])])],
        [CI('allergy', 'حساسیت شدید به اجزای واکسن (از جمله مخمر) یا دوز قبلی.', 'Severe hypersensitivity to a component (including yeast) or a previous dose.', [R(Gd, '4')])],
        exs=[ex('std', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=12, weightKg=40)])

Pn = fda('prevnar20', 'FDA Prevnar 20', 'Prevnar 20 (pneumococcal 20-valent conjugate vaccine) — Prescribing Information', sid('prevnar'))
vaccine('pneumococcal-vaccine', 'واکسن پنوموکوک کونژوگه (PCV20)', 'Pneumococcal conjugate vaccine (PCV20)', 'واکسن کونژوگه', 'Conjugate vaccine', 'Prevnar 20', ['prevnar', 'پرونار', 'واکسن پنوموکوک', 'PCV'], Pn,
        vac('syr-05', '0.5 mL prefilled syringe', Pn),
        [fx('child', 'immunization', 'شیرخوار — ۰٫۵ mL در ۲، ۴، ۶ و ۱۲ تا ۱۵ ماهگی', 'Infant — 0.5 mL at 2, 4, 6 and 12–15 months', {'minAge': age(6, 'week'), 'maxAge': age(18, 'year')}, 0.5, [R(Pn, '2.3')],
            [note('دوز اول از ۶ هفتگی. جبرانی (بدون واکسن قبلی): ۷ تا ۱۱ ماه ۳ دوز؛ ۱۲ تا ۲۳ ماه ۲ دوز با فاصله ۲ ماه؛ ۲۴ ماه تا ۱۷ سال یک دوز.', 'First dose from 6 weeks. Catch-up (no prior PCV): 7–11 months 3 doses; 12–23 months 2 doses 2 months apart; 24 months–17 y one dose.', [R(Pn, '2.3'), R(Pn, '2.4, Table 1')])]),
         fx('adult', 'immunization', 'بزرگسال ۱۸ سال به بالا — یک دوز ۰٫۵ mL', 'Adults ≥18 y — one 0.5 mL dose', A18, 0.5, [R(Pn, '2.6'), R(Pn, '2.2')], [])],
        [CI('allergy', 'واکنش آلرژیک شدید به اجزای واکسن یا توکسوئید دیفتری.', 'Severe allergic reaction to a component or to diphtheria toxoid.', [R(Pn, '4')])],
        exs=[ex('child', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageMonths=2, weightKg=5), ex('adult', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=65, weightKg=70)])

Hv = fda('havrix', 'FDA Havrix', 'Havrix (hepatitis A vaccine) — Prescribing Information', sid('havrix')); d = R(Hv, '2.3')
vaccine('hepatitis-a-vaccine', 'واکسن هپاتیت A', 'Hepatitis A vaccine', 'واکسن غیرفعال', 'Inactivated vaccine', 'Havrix', ['havrix', 'هاوریکس', 'واکسن هپاتیت آ'], Hv,
        vac('susp', '0.5 mL (child) or 1 mL (adult)', Hv),
        [reg('std', 'immunization', T('۱۲ ماه تا ۱۸ سال: ۰٫۵ mL؛ ۱۹ سال به بالا: ۱ mL — دوز یادآور ۶ تا ۱۲ ماه بعد', '12 months–18 y: 0.5 mL; ≥19 y: 1 mL — booster 6–12 months later'), {'minAge': age(12, 'month')}, 'ageBand',
             {'bands': [{'minAge': age(12, 'month'), 'maxAge': age(19, 'year'), 'perDose': 0.5, 'dosesPerDay': 1}, {'minAge': age(19, 'year'), 'maxAge': None, 'perDose': 1, 'dosesPerDay': 1}]}, [d], unit='mL', dur=ONE,
             notes=[note('دست‌کم ۲ هفته پیش از مواجهه احتمالی. عضلانی، نه در باسن.', 'At least 2 weeks before expected exposure. IM, not in the buttock.', [R(Hv, '1'), R(Hv, '2.2')])])],
        [CI('allergy', 'آنافیلاکسی به دوز قبلی واکسن هپاتیت A یا اجزای آن (از جمله نئومایسین).', 'Anaphylaxis to a previous hepatitis A vaccine dose or a component (including neomycin).', [R(Hv, '4')])],
        exs=[ex('std', 'susp', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=2, weightKg=12), ex('std', 'susp', {'perDose': 1, 'mlPerDose': 1}, ageYears=30, weightKg=70)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['adenosine', 'fosphenytoin', 'lorazepam', 'amiodarone', 'ondansetron', 'pralidoxime', 'deferoxamine', 'fomepizole', 'methylene-blue', 'protamine', 'digoxin-immune-fab',
                                     'hydroxocobalamin-cyanokit', 'acetylcysteine', 'antiscorpion-venom', 'antisnake-venom', 'tetanus-immune-globulin', 'rabies-immune-globulin', 'tdap-vaccine', 'rabies-vaccine'] if x not in col['drugs']]
    if col['id'] == 'pediatric':
        col['drugs'] += [x for x in ['hepatitis-b-vaccine', 'mmr-vaccine', 'varicella-vaccine', 'pneumococcal-vaccine', 'hepatitis-a-vaccine', 'influenza-vaccine'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s4 ok')
