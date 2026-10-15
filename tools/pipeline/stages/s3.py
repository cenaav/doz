"""Stage 3 — antiparasitic, antifungal and antiviral."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's3_setids.json')))
sid = lambda k: S[k][0]

add_disease('fascioliasis', 'فاسیولیازیس (کرم کبد گوسفند)', 'Fascioliasis (liver fluke)', ['fasciola', 'fascioliasis', 'فاسیولا', 'کرم کبد'], ['B66.3'], 'infectious')
add_disease('cutaneous-leishmaniasis', 'لیشمانیوز جلدی (سالک)', 'Cutaneous leishmaniasis', ['salak', 'سالک', 'لیشمانیا', 'cutaneous leishmaniasis'], ['B55.1'], 'infectious')
add_disease('visceral-leishmaniasis', 'لیشمانیوز احشایی (کالاآزار)', 'Visceral leishmaniasis (kala-azar)', ['kala-azar', 'کالاآزار', 'visceral leishmaniasis'], ['B55.0'], 'infectious')
add_disease('hepatitis-b', 'هپاتیت B مزمن', 'Chronic hepatitis B', ['HBV', 'hepatitis b', 'هپاتیت ب', 'هپاتیت B'], ['B18.1'], 'gastroenterology')
add_disease('hepatitis-c', 'هپاتیت C مزمن', 'Chronic hepatitis C', ['HCV', 'hepatitis c', 'هپاتیت سی', 'هپاتیت C'], ['B18.2'], 'gastroenterology')
add_disease('hiv-prep', 'پیشگیری پیش از مواجهه با HIV (PrEP)', 'HIV pre-exposure prophylaxis (PrEP)', ['PrEP', 'HIV prevention', 'پیشگیری ایدز', 'اچ آی وی'], ['Z29.81'], 'infectious')
add_disease('covid-19', 'کووید-۱۹', 'COVID-19', ['covid', 'کرونا', 'کووید', 'SARS-CoV-2'], ['U07.1'], 'infectious')
add_disease('invasive-fungal', 'عفونت قارچی تهاجمی (آسپرژیلوس، کاندیدمی، کریپتوکوک) — بیمارستانی', 'Invasive fungal infection (aspergillosis, candidaemia, cryptococcosis) — hospital', ['aspergillosis', 'candidemia', 'cryptococcus', 'آسپرژیلوس', 'کاندیدمی', 'قارچ سیستمیک'], ['B44.9', 'B37.7', 'B45.9'], 'infectious')
add_disease('hsv-encephalitis', 'آنسفالیت و عفونت شدید هرپسی', 'Herpes simplex encephalitis and severe HSV infection', ['HSV encephalitis', 'آنسفالیت هرپسی', 'هرپس نوزادی'], ['B00.4'], 'infectious')
add_disease('cutaneous-candidiasis', 'کاندیدیاز پوستی', 'Cutaneous candidiasis', ['candida skin', 'کاندیدای پوستی', 'عفونت قارچی پوست'], ['B37.2'], 'dermatology')
NOT_RELIABLE = 'رفرنس مطمئن نیست: برچسب آمریکا/انگلیس در دسترس نیست و اطلاعات از سایت ایرانی دارویاب است. دوز محاسبه نمی‌شود. '
NOT_RELIABLE_EN = 'Reference not reliable: no US/UK label available; information is from the Iranian site Darooyab. No dose is calculated. '
pv = lambda id, label, mg, src, sec: form(id, 'powder-for-injection', 'iv', label, mg, 'mg', [R(src, sec)], per='vial')
comp = lambda **kw: {k: {'name': T(*v[0]), 'amount': v[1], 'unit': 'mg'} for k, v in kw.items()}

# --- antimalarials ---
Co = fda('coartem', 'FDA Coartem', 'Coartem (artemether/lumefantrine) tablets — Prescribing Information', sid('coartem')); d = R(Co, '2.2–2.3')
f = form('tab-20-120', 'tablet', 'oral', 'Artemether 20 mg + lumefantrine 120 mg tablet (scored)', 20, 'mg', [R(Co, '3')], per='tablet', scored=True,
         components=comp(artemether=(('آرتمتر', 'Artemether'), 20), lumefantrine=(('لومفانترین', 'Lumefantrine'), 120)))
drug('artemether-lumefantrine', 'antiparasitic', 'آرتمتر + لومفانترین', 'Artemether + lumefantrine', T('ضدمالاریا (ترکیب آرتمیزینین)', 'Antimalarial (artemisinin combination)'), [{'name': 'Coartem', 'market': 'US'}], ['coartem', 'کوارتم', 'آرتمتر', 'artemether'],
     [f],
     [reg('treat', 'malaria', T('مالاریای حاد بدون عارضه — بر اساس وزن، ۶ نوبت در ۳ روز', 'Acute uncomplicated malaria — by weight, 6 doses over 3 days'), {'minAge': age(2, 'month'), 'minWeightKg': 5}, 'weightBand',
          {'weightBands': [{'minWeightKg': 5, 'maxWeightKg': 14.99, 'perDose': 20, 'dosesPerDay': 2}, {'minWeightKg': 15, 'maxWeightKg': 24.99, 'perDose': 40, 'dosesPerDay': 2},
                           {'minWeightKg': 25, 'maxWeightKg': 34.99, 'perDose': 60, 'dosesPerDay': 2}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 80, 'dosesPerDay': 2}]},
          [d], doseComponent='artemether', dur={'min': 3, 'max': 3},
          notes=[note('دوز به‌صورت جزء آرتمتر نمایش داده می‌شود (۲۰ mg در هر قرص). نوبت اول، نوبت دوم ۸ ساعت بعد، سپس روزی ۲ بار تا روز سوم (جمعاً ۶ نوبت). همراه غذا؛ اگر ظرف ۱ تا ۲ ساعت استفراغ شد، تکرار.',
                      'Shown as the artemether component (20 mg per tablet). First dose, second dose after 8 h, then twice daily for the next 2 days (6 doses total). Take with food; repeat a dose vomited within 1–2 h.', [d, R(Co, '2.1')])])],
     [CI('hyper', 'حساسیت به آرتمتر یا لومفانترین.', 'Hypersensitivity to artemether or lumefantrine.', [R(Co, '4')]),
      CI('ind', 'مصرف همزمان با القاکننده‌های قوی CYP3A4 (ریفامپین، کاربامازپین، فنی‌توئین، علف چای).', 'Coadministration with strong CYP3A4 inducers (rifampin, carbamazepine, phenytoin, St John’s wort).', [R(Co, '4')])],
     warn=[W('طولانی شدن QT: در QT طولانی، کمبود پتاسیم یا منیزیم و با داروهای طولانی‌کننده QT اجتناب شود.', 'QT prolongation: avoid with known long QT, hypokalaemia or hypomagnesaemia, and with QT-prolonging drugs.', [R(Co, '5')])],
     inter=[IA('cyp3a4-inducers', 'ریفامپین، کاربامازپین، فنی‌توئین و علف چای اثر را از بین می‌برند (ممنوع).', 'Rifampin, carbamazepine, phenytoin and St John’s wort cause loss of efficacy (contraindicated).', [R(Co, '4')])],
     exs=[ex('treat', 'tab-20-120', {'perDose': 40, 'tabletsPerDoseRounded': 2}, ageYears=6, weightKg=20), ex('treat', 'tab-20-120', {'perDose': 80, 'tabletsPerDoseRounded': 4}, ageYears=30, weightKg=70)])

Ma = fda('malarone', 'FDA Malarone', 'Malarone (atovaquone/proguanil) tablets — Prescribing Information', sid('malarone'))
ap = lambda id, a, p, label: form(id, 'tablet', 'oral', label, a, 'mg', [R(Ma, '3')], per='tablet', components=comp(atovaquone=(('آتوواکون', 'Atovaquone'), a), proguanil=(('پروگوانیل', 'Proguanil HCl'), p)))
drug('atovaquone-proguanil', 'antiparasitic', 'آتوواکون + پروگوانیل', 'Atovaquone + proguanil', T('ضدمالاریا', 'Antimalarial'), [{'name': 'Malarone', 'market': 'US'}], ['malarone', 'مالارون', 'آتوواکون'],
     [ap('tab-250-100', 250, 100, 'Adult tablet: atovaquone 250 mg + proguanil 100 mg'), ap('tab-62-25', 62.5, 25, 'Pediatric tablet: atovaquone 62.5 mg + proguanil 25 mg')],
     [reg('proph', 'malaria', T('پیشگیری مالاریا — روزانه بر اساس وزن (۱۱ kg به بالا)', 'Malaria prevention — daily by weight (≥11 kg)'), {'minWeightKg': 11}, 'weightBand',
          {'weightBands': [{'minWeightKg': 11, 'maxWeightKg': 20.99, 'perDose': 62.5, 'dosesPerDay': 1}, {'minWeightKg': 21, 'maxWeightKg': 30.99, 'perDose': 125, 'dosesPerDay': 1},
                           {'minWeightKg': 31, 'maxWeightKg': 40, 'perDose': 187.5, 'dosesPerDay': 1}, {'minWeightKg': 40.01, 'maxWeightKg': None, 'perDose': 250, 'dosesPerDay': 1}]},
          [R(Ma, '2.1, Table 1')], doseComponent='atovaquone',
          notes=[note('دوز به‌صورت جزء آتوواکون. از ۱ تا ۲ روز پیش از ورود به منطقه، روزانه در طول اقامت و تا ۷ روز پس از بازگشت؛ همراه غذا یا نوشیدنی شیری. بالای ۴۰ kg: یک قرص بزرگسال.',
                      'Shown as the atovaquone component. Start 1–2 days before entering the area, daily during the stay and for 7 days after return; with food or a milky drink. Over 40 kg: one adult tablet.', [R(Ma, '2.1'), R(Ma, '2')])]),
      reg('treat', 'malaria', T('درمان مالاریای حاد — یک بار در روز، ۳ روز، بر اساس وزن', 'Acute malaria treatment — once daily for 3 days, by weight'), {'minWeightKg': 5}, 'weightBand',
          {'weightBands': [{'minWeightKg': 5, 'maxWeightKg': 8.99, 'perDose': 125, 'dosesPerDay': 1}, {'minWeightKg': 9, 'maxWeightKg': 10.99, 'perDose': 187.5, 'dosesPerDay': 1},
                           {'minWeightKg': 11, 'maxWeightKg': 20.99, 'perDose': 250, 'dosesPerDay': 1}, {'minWeightKg': 21, 'maxWeightKg': 30.99, 'perDose': 500, 'dosesPerDay': 1},
                           {'minWeightKg': 31, 'maxWeightKg': 40, 'perDose': 750, 'dosesPerDay': 1}, {'minWeightKg': 40.01, 'maxWeightKg': None, 'perDose': 1000, 'dosesPerDay': 1}]},
          [R(Ma, '2.2, Table 2')], doseComponent='atovaquone', dur={'min': 3, 'max': 3},
          notes=[note('دوز به‌صورت جزء آتوواکون. بزرگسال: ۴ قرص بزرگسال یک‌جا روزانه، ۳ روز. اگر ظرف ۱ ساعت استفراغ شد، تکرار.', 'Shown as the atovaquone component. Adult: 4 adult tablets as one daily dose for 3 days. Repeat a dose vomited within 1 h.', [R(Ma, '2.2'), R(Ma, '2')])])],
     [CI('hyper', 'حساسیت به آتوواکون یا پروگوانیل.', 'Hypersensitivity to atovaquone or proguanil.', [R(Ma, '4')]),
      CI('renal', 'پیشگیری در نارسایی شدید کلیه (CrCl زیر ۳۰) ممنوع.', 'Prophylaxis contraindicated in severe renal impairment (CrCl <30).', [R(Ma, '4'), R(Ma, '2.3')])],
     exs=[ex('proph', 'tab-62-25', {'perDose': 62.5, 'tabletsPerDoseRounded': 1}, ageYears=4, weightKg=15), ex('treat', 'tab-250-100', {'perDose': 1000, 'tabletsPerDoseRounded': 4}, ageYears=30, weightKg=70)])

Mf = fda('mefloquine', 'FDA Mefloquine', 'Mefloquine hydrochloride tablets (Teva) — Prescribing Information', sid('mefloquine')); d = R(Mf, 'Dosage and Administration')
drug('mefloquine', 'antiparasitic', 'مفلوکین', 'Mefloquine', T('ضدمالاریا', 'Antimalarial'), [{'name': 'Lariam', 'market': 'US'}], ['lariam', 'لاریام', 'مفلوکین'],
     [tab('tab-250', 250, '250 mg tablet (scored)', [R(Mf, 'How Supplied')], scored=True)],
     [reg('treat-adult', 'malaria', T('درمان مالاریای خفیف تا متوسط — بزرگسال: ۱۲۵۰ mg (۵ قرص) یک‌جا', 'Mild–moderate malaria — adult: 1,250 mg (5 tablets) single dose'), A18, 'fixed', {'perDose': 1250, 'dosesPerDay': 1}, [d], dur={'min': 1, 'max': 1},
          notes=[note('همراه غذا و حداقل ۲۴۰ mL آب. در P. vivax برای پیشگیری از عود، بعداً پریماکین.', 'With food and at least 240 mL water. In P. vivax follow with primaquine to prevent relapse.', [d])]),
      reg('treat-child', 'malaria', T('درمان مالاریا — کودک: ۲۰ تا ۲۵ mg/kg (کل دوره)', 'Malaria treatment — child: 20–25 mg/kg (whole course)'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 20, 'perKgPerDayMax': 25, 'dividedDoses': 1}, [d],
          limits={'maxPerDose': 1250, 'refs': [d]}, dur={'min': 1, 'max': 1},
          notes=[note('می‌توان کل دوز را به ۲ نوبت با فاصله ۶ تا ۸ ساعت تقسیم کرد. بیشتر از دوز بزرگسال نشود. تجربه در زیر ۲۰ kg محدود است. اگر ظرف ۳۰ دقیقه استفراغ شد، دوز کامل دوم.', 'The total dose may be split into 2 doses 6–8 h apart. Not more than the adult dose. Limited experience under 20 kg. If vomited within 30 min, give a second full dose.', [d])]),
      reg('proph-adult', 'malaria', T('پیشگیری مالاریا — بزرگسال: ۲۵۰ mg هفته‌ای یک بار', 'Malaria prophylaxis — adult: 250 mg once weekly'), A18, 'fixed', {'perDose': 250, 'dosesPerDay': 1}, [d],
          notes=[note('هفته‌ای یک بار (نه روزانه)، همیشه در یک روز ثابت پس از غذا؛ از ۱ هفته پیش از سفر تا ۴ هفته پس از ترک منطقه.', 'Once WEEKLY (not daily), same day each week after the main meal; from 1 week before arrival until 4 weeks after leaving.', [d])]),
      reg('proph-child', 'malaria', T('پیشگیری مالاریا — کودک: حدود ۵ mg/kg هفته‌ای یک بار', 'Malaria prophylaxis — child: about 5 mg/kg once weekly'), {'maxAge': age(18, 'year')}, 'notCalculated',
          {'reason': T('برچسب: هفته‌ای یک بار — ۲۰ تا ۳۰ kg: نصف قرص؛ ۳۰ تا ۴۵ kg: سه‌چهارم قرص؛ بالای ۴۵ kg: یک قرص ۲۵۰ mg. تجربه در زیر ۲۰ kg محدود است.', 'Label: once weekly — 20–30 kg: ½ tablet; 30–45 kg: ¾ tablet; over 45 kg: one 250 mg tablet. Limited experience under 20 kg.')}, [d])],
     [CI('hyper', 'حساسیت به مفلوکین یا ترکیبات مشابه (کینین، کینیدین).', 'Hypersensitivity to mefloquine or related compounds (quinine, quinidine).', [R(Mf, 'Contraindications')]),
      CI('psych', 'پیشگیری در افسردگی فعال یا اخیر، اضطراب فراگیر، سایکوز، اسکیزوفرنی یا سایر اختلالات روانی مهم، یا سابقه تشنج ممنوع.', 'Not for prophylaxis with active or recent depression, generalised anxiety, psychosis, schizophrenia or other major psychiatric disorder, or a history of seizures.', [R(Mf, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: عوارض عصبی‌روانی که ممکن است پس از قطع ادامه یابد؛ با بروز علائم، قطع و جایگزینی.', 'Boxed warning: neuropsychiatric adverse reactions that can persist after stopping; stop and substitute if symptoms occur.', [R(Mf, 'Boxed Warning')])],
     exs=[ex('treat-adult', 'tab-250', {'perDose': 1250, 'tabletsPerDoseRounded': 5}, ageYears=30, weightKg=70), ex('treat-child', 'tab-250', {'perDose': 400, 'upperPerDose': 500}, ageYears=6, weightKg=20),
          ex('proph-adult', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Qn = fda('quinine', 'FDA Quinine sulfate', 'Quinine sulfate capsules 324 mg (Lupin) — Prescribing Information', sid('qualaquin'))
drug('quinine', 'antiparasitic', 'کینین (خوراکی)', 'Quinine sulfate (oral)', T('ضدمالاریا', 'Antimalarial'), [{'name': 'Qualaquin', 'market': 'US'}], ['qualaquin', 'کینین', 'quinine'],
     [tab('cap-324', 324, '324 mg capsule', [R(Qn, '3')], per='capsule', form_='capsule')],
     [reg('treat', 'malaria', T('مالاریای فالسیپاروم بدون عارضه — ۶۴۸ mg هر ۸ ساعت، ۷ روز (۱۶ سال به بالا)', 'Uncomplicated P. falciparum malaria — 648 mg every 8 h for 7 days (≥16 y)'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 648, 'dosesPerDay': 3}, [R(Qn, '2.1')], dur={'min': 7, 'max': 7},
          notes=[note('همراه غذا. نارسایی شدید مزمن کلیه: یک دوز بارگذاری ۶۴۸ mg، سپس ۳۲۴ mg هر ۱۲ ساعت. در نارسایی شدید کبد مصرف نشود.', 'With food. Severe chronic renal impairment: one 648 mg loading dose, then 324 mg every 12 h. Not for severe hepatic impairment.', [R(Qn, '2.1'), R(Qn, '2.2'), R(Qn, '2.3')])])],
     [CI('ci', 'QT طولانی، کمبود G6PD، میاستنی گراویس، نوریت اپتیک، حساسیت به کینین/مفلوکین/کینیدین.', 'Prolonged QT, G6PD deficiency, myasthenia gravis, optic neuritis, hypersensitivity to quinine/mefloquine/quinidine.', [R(Qn, '4')])],
     warn=[W('هشدار جعبه‌ای: برای گرفتگی شبانه پا مصرف نشود — واکنش‌های خونی کشنده (ترومبوسیتوپنی، HUS/TTP).', 'Boxed warning: not for nocturnal leg cramps — life-threatening haematologic reactions (thrombocytopenia, HUS/TTP).', [R(Qn, 'Boxed Warning')])],
     exs=[ex('treat', 'cap-324', {'perDose': 648, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=70)])

# --- other antiparasitics ---
Eg = fda('egaten', 'FDA Egaten', 'Egaten (triclabendazole) tablets — Prescribing Information', sid('egaten'))
drug('triclabendazole', 'antiparasitic', 'تریکلابندازول', 'Triclabendazole', T('ضدکرم (بنزیمیدازول)', 'Anthelmintic (benzimidazole)'), [{'name': 'Egaten', 'market': 'US'}], ['egaten', 'اگاتن', 'تریکلابندازول'],
     [tab('tab-250', 250, '250 mg tablet (scored)', [R(Eg, '3')], scored=True)],
     [reg('fasc', 'fascioliasis', T('فاسیولیازیس — ۱۰ mg/kg دو نوبت با فاصله ۱۲ ساعت (۶ سال به بالا)', 'Fascioliasis — 10 mg/kg twice, 12 h apart (≥6 y)'), {'minAge': age(6, 'year')}, 'weightBased', {'perKgPerDose': 10, 'intervalHours': 12}, [R(Eg, '2')], dur={'min': 1, 'max': 1},
          notes=[note('فقط ۲ نوبت. همراه غذا. برچسب: اگر دوز دقیق ممکن نیست، به سمت بالا گرد شود (نیم قرص = ۱۲۵ mg).', 'Two doses only. With food. Label: if the dose cannot be matched exactly, round up (half tablet = 125 mg).', [R(Eg, '2')])])],
     [CI('hyper', 'حساسیت به تریکلابندازول یا سایر بنزیمیدازول‌ها.', 'Hypersensitivity to triclabendazole or other benzimidazoles.', [R(Eg, '4')])],
     exs=[ex('fasc', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=8, weightKg=25)])

Pm = fda('humatin', 'FDA Humatin', 'Humatin (paromomycin) capsules — Prescribing Information', sid('paromomycin')); d = R(Pm, 'Dosage and Administration')
drug('paromomycin', 'antiparasitic', 'پارومومایسین (خوراکی)', 'Paromomycin (oral)', T('آمینوگلیکوزید روده‌ای ضدآمیب', 'Intestinal aminoglycoside amoebicide'), [{'name': 'Humatin', 'market': 'US'}], ['humatin', 'هوماتین', 'پارومومایسین'],
     [tab('cap-250', 250, '250 mg capsule', [R(Pm, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('amebiasis', 'intestinal-amebiasis', T('آمیبیازیس روده‌ای — ۲۵ تا ۳۵ mg/kg/روز در ۳ نوبت همراه غذا، ۵ تا ۱۰ روز', 'Intestinal amoebiasis — 25–35 mg/kg/day in 3 doses with meals, 5–10 days'), {}, 'weightBased',
          {'perKgPerDay': 25, 'perKgPerDayMax': 35, 'dividedDoses': 3}, [d], dur={'min': 5, 'max': 10}),
      reg('hepatic', 'hepatic-encephalopathy', T('کمای کبدی — بزرگسال: ۴ گرم در روز در دوزهای منقسم', 'Hepatic coma — adult: 4 g/day in divided doses'), A18, 'notCalculated',
          {'reason': T('برچسب: ۴ g در روز در دوزهای منقسم با فواصل منظم به مدت ۵ تا ۶ روز؛ تعداد نوبت مشخص نشده است.', 'Label: 4 g daily in divided doses at regular intervals for 5–6 days; the number of doses is not stated.')}, [d])],
     [CI('ci', 'حساسیت به پارومومایسین؛ انسداد روده.', 'Hypersensitivity to paromomycin; intestinal obstruction.', [R(Pm, 'Contraindications')])],
     exs=[ex('amebiasis', 'cap-250', {'perDose': 500, 'upperPerDose': 700}, ageYears=30, weightKg=60)])

Im = fda('impavido', 'FDA Impavido', 'Impavido (miltefosine) capsules — Prescribing Information', sid('impavido')); d = R(Im, '2, Table 1')
mb = {'weightBands': [{'minWeightKg': 30, 'maxWeightKg': 44.99, 'perDose': 50, 'dosesPerDay': 2}, {'minWeightKg': 45, 'maxWeightKg': None, 'perDose': 50, 'dosesPerDay': 3}]}
mpop = {'minAge': age(12, 'year'), 'minWeightKg': 30}
drug('miltefosine', 'antiparasitic', 'میلتفوسین', 'Miltefosine', T('ضدلیشمانیا خوراکی', 'Oral antileishmanial'), [{'name': 'Impavido', 'market': 'US'}], ['impavido', 'ایمپاویدو', 'میلتفوسین'],
     [tab('cap-50', 50, '50 mg capsule', [R(Im, '3')], per='capsule', form_='capsule')],
     [reg('cl', 'cutaneous-leishmaniasis', T('لیشمانیوز جلدی — ۵۰ mg دو یا سه بار در روز بر اساس وزن، ۲۸ روز', 'Cutaneous leishmaniasis — 50 mg two or three times daily by weight, 28 days'), mpop, 'weightBand', mb, [d], dur={'min': 28, 'max': 28},
          notes=[note('همراه غذا. گونه‌های تأییدشده در برچسب برای فرم جلدی: L. braziliensis، L. guyanensis و L. panamensis (آمریکای لاتین)؛ گونه‌های شایع ایران (L. major و L. tropica) در برچسب نیستند.',
                      'With food. Label-approved species for cutaneous disease: L. braziliensis, L. guyanensis, L. panamensis; the species common in Iran (L. major, L. tropica) are not in the label.', [d, R(Im, '1')])]),
      reg('vl', 'visceral-leishmaniasis', T('لیشمانیوز احشایی (L. donovani) — ۵۰ mg دو یا سه بار در روز بر اساس وزن، ۲۸ روز', 'Visceral leishmaniasis (L. donovani) — 50 mg two or three times daily by weight, 28 days'), mpop, 'weightBand', mb, [d], dur={'min': 28, 'max': 28})],
     [CI('preg', 'بارداری — ممنوع (مرگ و ناهنجاری جنین).', 'Pregnancy — contraindicated (fetal death and malformation).', [R(Im, '4')]), CI('sls', 'سندرم شوگرن-لارسون.', 'Sjögren-Larsson syndrome.', [R(Im, '4')]),
      CI('hyper', 'حساسیت به میلتفوسین.', 'Hypersensitivity to miltefosine.', [R(Im, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت جنینی. پیش از شروع تست بارداری؛ پیشگیری مؤثر از بارداری در طول درمان و تا ۵ ماه پس از آن.', 'Boxed warning: embryo-fetal toxicity. Pregnancy test before starting; effective contraception during treatment and for 5 months after.', [R(Im, 'Boxed Warning')])],
     exs=[ex('cl', 'cap-50', {'perDose': 50, 'tabletsPerDoseRounded': 1, 'dosesPerDay': 3}, ageYears=30, weightKg=60), ex('vl', 'cap-50', {'perDose': 50, 'dosesPerDay': 2}, ageYears=14, weightKg=40)])

Ov = fda('ovide', 'FDA Ovide', 'Ovide (malathion) lotion 0.5% — Prescribing Information', sid('malathion')); d = R(Ov, 'Dosage and Administration')
drug('malathion', 'antiparasitic', 'مالاتیون لوسیون', 'Malathion lotion', T('ضدشپش', 'Pediculicide'), [{'name': 'Ovide', 'market': 'US'}], ['ovide', 'اوید', 'مالاتیون', 'لوسیون شپش'],
     [unitform('lotion-05', 'lotion', 'topical', 'Malathion 0.5% lotion (59 mL)', [R(Ov, 'How Supplied')])],
     [reg('lice', 'head-lice', T('شپش سر — یک بار روی موی خشک، ۸ تا ۱۲ ساعت بعد شستشو (۶ سال به بالا)', 'Head lice — once on dry hair, shampoo after 8–12 h (≥6 y)'), {'minAge': age(6, 'year')}, 'notCalculated',
          {'reason': T('دوز وزنی ندارد: به اندازه‌ای که مو و پوست سر کامل خیس شود روی موی خشک بمالید (به‌ویژه پشت سر و گردن)، بگذارید خودبه‌خود خشک شود و سر را نپوشانید؛ پس از ۸ تا ۱۲ ساعت با شامپو بشویید و با شانه رشک‌گیر شانه کنید. اگر پس از ۷ تا ۹ روز هنوز شپش بود، یک بار تکرار.',
                       'Not weight-dosed: apply to DRY hair just enough to wet hair and scalp thoroughly (especially back of head and neck), let dry naturally and leave uncovered; shampoo after 8–12 h and use a nit comb. If lice remain after 7–9 days, repeat once.')}, [d, R(Ov, 'Pediatric Use')])],
     [CI('infant', 'نوزاد و شیرخوار — ممنوع (جذب بیشتر از پوست سر).', 'Neonates and infants — contraindicated (greater scalp absorption).', [R(Ov, 'Contraindications')]),
      CI('hyper', 'حساسیت به مالاتیون یا اجزای حامل.', 'Sensitivity to malathion or vehicle ingredients.', [R(Ov, 'Contraindications')])],
     warn=[W('قابل اشتعال: لوسیون و موی خیس از شعله، سشوار و بیگودی برقی دور بماند؛ سیگار نکشید.', 'Flammable: keep lotion and wet hair away from flames, hair dryers and electric curlers; do not smoke.', [R(Ov, 'Warnings')])])

Eu = fda('eurax', 'FDA Eurax', 'Eurax (crotamiton) cream 10% — Prescribing Information', sid('eurax')); d = R(Eu, 'Dosage and Administration')
drug('crotamiton', 'antiparasitic', 'کروتامیتون کرم', 'Crotamiton cream', T('ضدگال و ضدخارش', 'Scabicide and antipruritic'), [{'name': 'Eurax', 'market': 'US'}], ['eurax', 'یوراکس', 'کروتامیتون'],
     [unitform('cream-10', 'cream', 'topical', 'Crotamiton 10% cream (60 g)', [R(Eu, 'How Supplied')])],
     [reg('scabies', 'scabies', T('گال — از چانه به پایین، تکرار ۲۴ ساعت بعد', 'Scabies — chin down, repeat after 24 h'), A18, 'notCalculated',
          {'reason': T('دوز وزنی ندارد: کرم را روی کل بدن از چانه به پایین با دقت در چین‌ها ماساژ دهید؛ ۲۴ ساعت بعد تکرار؛ صبح روز بعد لباس و ملحفه عوض شود؛ ۴۸ ساعت پس از آخرین نوبت حمام. یک لوله ۶۰ گرمی برای ۲ نوبت کافی است.',
                       'Not weight-dosed: massage into the whole body from the chin down, especially folds; repeat after 24 h; change clothing and bed linen next morning; cleansing bath 48 h after the last application. One 60 g tube is enough for two applications.')}, [d, R(Eu, 'Directions for patients with scabies')],
          notes=[note('ایمنی و اثربخشی در کودکان ثابت نشده است.', 'Safety and effectiveness in children not established.', [R(Eu, 'Pediatric Use')])]),
      reg('itch', 'pruritus', T('خارش — مالیدن ملایم روی ناحیه در صورت نیاز', 'Pruritus — massage gently into the area as needed'), A18, 'notCalculated',
          {'reason': T('به آرامی روی ناحیه ماساژ دهید تا جذب شود؛ در صورت نیاز تکرار.', 'Massage gently into the affected area until absorbed; repeat as needed.')}, [d])],
     [CI('hyper', 'حساسیت یا تحریک اولیه پوست با داروهای موضعی.', 'Sensitivity or primary irritation response to topical medicines.', [R(Eu, 'Contraindications')])])

Gl = dy('ir-darooyab-glucantime', 'Darooyab Glucantime', 'مگلومین آنتی موان — موارد مصرف، منع مصرف و اشکال دارویی', 'G-4594/Meglumine-Antimonate')
drug('meglumine-antimoniate', 'antiparasitic', 'مگلومین آنتی‌موان (گلوکانتیم)', 'Meglumine antimoniate (Glucantime)', T('ترکیب آنتیموان پنج‌ظرفیتی ضدلیشمانیا', 'Pentavalent antimonial antileishmanial'), [{'name': 'Glucantime', 'market': 'IR'}], ['glucantime', 'گلوکانتیم', 'آمپول سالک', 'مگلومین'],
     [liquid('amp-300', 1500, 5, '1.5 g / 5 mL ampoule (300 mg/mL)', [R(Gl, 'اشکال دارویی')], form_='injection', route='im', markets=('IR',))],
     [reg('cl', 'cutaneous-leishmaniasis', T('سالک (لیشمانیوز جلدی) — داخل ضایعه یا تزریق سیستمیک', 'Cutaneous leishmaniasis — intralesional or systemic injection'), {}, 'notCalculated',
          {'reason': T(NOT_RELIABLE + 'دارویاب: در ضایعات کوچک و منفرد تزریق داخل ضایعه تا سفید شدن بافت اطراف؛ در ضایعات متعدد، بزرگ، روی غضروف یا صورت و مفاصل، تزریق سیستمیک ۱۰ تا ۲۰ روز. دوز عددی در منبع ذکر نشده است.',
                       NOT_RELIABLE_EN + 'Darooyab: small single lesions — intralesional injection until the surrounding tissue blanches; multiple, large, cartilage, face or joint lesions — systemic injection for 10–20 days. The source gives no numeric dose.')}, [R(Gl, 'موارد مصرف')]),
      reg('vl', 'visceral-leishmaniasis', T('کالاآزار — عضلانی عمیق یا وریدی آهسته ۲۰ تا ۲۸ روز', 'Kala-azar — deep IM or slow IV for 20–28 days'), {}, 'notCalculated',
          {'reason': T(NOT_RELIABLE + 'دارویاب: عضلانی عمیق یا انفوزیون آهسته وریدی ۲۰ تا ۲۸ روز متوالی با پایش نوار قلب (QT)، آنزیم‌های کبد، آمیلاز و لیپاز. دوز عددی در منبع ذکر نشده است.',
                       NOT_RELIABLE_EN + 'Darooyab: deep IM or slow IV infusion for 20–28 consecutive days with ECG (QT), liver enzyme, amylase and lipase monitoring. The source gives no numeric dose.')}, [R(Gl, 'موارد مصرف')])],
     [CI('organ', 'نارسایی شدید کلیه؛ بیماری قلبی (نارسایی، آریتمی، اختلال هدایت)؛ نارسایی کبد.', 'Severe renal failure; heart disease (failure, arrhythmia, conduction disorder); hepatic failure.', [R(Gl, 'منع مصرف')]),
      CI('preg', 'بارداری: منع نسبی تا مطلق؛ شیردهی توصیه نمی‌شود.', 'Pregnancy: relative to absolute contraindication; not recommended while breastfeeding.', [R(Gl, 'بارداری و شیردهی')], sev='warn')])

# --- antifungals ---
La = fda('lamisilat', 'FDA Lamisil AT cream', 'Lamisil AT (terbinafine 1%) cream — Drug Facts', sid('lamisilat')); d = R(La, 'Directions')
drug('terbinafine-cream', 'dermatology', 'تربینافین کرم', 'Terbinafine cream', T('ضدقارچ موضعی (آلیل‌آمین)', 'Topical antifungal (allylamine)'), [{'name': 'Lamisil AT', 'market': 'US'}], ['lamisil cream', 'لامیزیل', 'کرم تربینافین'],
     [unitform('cream-1', 'cream', 'topical', 'Terbinafine 1% cream', [R(La, 'Package label')])],
     [reg('tinea', 'tinea', T('پای ورزشکار، کشاله ران و تینه‌آ کورپوریس (۱۲ سال به بالا)', 'Athlete’s foot, jock itch and ringworm (≥12 y)'), {'minAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('بین انگشتان پا: روزی ۲ بار، ۱ هفته؛ کف یا کناره پا: روزی ۲ بار، ۲ هفته؛ کشاله ران و تینه‌آ بدن: روزی یک بار، ۱ هفته. پوست را پیش از مصرف بشویید و خشک کنید. زیر ۱۲ سال با نظر پزشک.',
                       'Between the toes: twice daily for 1 week; bottom or sides of foot: twice daily for 2 weeks; jock itch and ringworm: once daily for 1 week. Wash and dry the skin first. Under 12 y: ask a doctor.')}, [d])])

Ec = fda('econazole', 'FDA Econazole cream', 'Econazole nitrate cream 1% (Encube) — Prescribing Information', sid('econazole')); d = R(Ec, 'Dosage and Administration')
drug('econazole', 'dermatology', 'اکونازول کرم', 'Econazole cream', T('ضدقارچ موضعی (ایمیدازول)', 'Topical antifungal (imidazole)'), [{'name': 'Spectazole', 'market': 'US'}], ['spectazole', 'اکونازول', 'econazole'],
     [unitform('cream-1', 'cream', 'topical', 'Econazole nitrate 1% cream', [R(Ec, 'How Supplied')])],
     [reg('tinea', 'tinea', T('تینه‌آ پا، کشاله ران و بدن — روزی یک بار', 'Tinea pedis, cruris and corporis — once daily'), {}, 'notCalculated',
          {'reason': T('روزی یک بار روی ناحیه؛ کشاله ران و بدن ۲ هفته، پا ۱ ماه.', 'Once daily to cover the area; cruris and corporis 2 weeks, pedis 1 month.')}, [d]),
      reg('versicolor', 'pityriasis-versicolor', T('تینه‌آ ورسیکالر — روزی یک بار، ۲ هفته', 'Tinea versicolor — once daily, 2 weeks'), {}, 'notCalculated',
          {'reason': T('روزی یک بار؛ معمولاً پس از ۲ هفته پاک می‌شود.', 'Once daily; usually clears after 2 weeks.')}, [d]),
      reg('candida', 'cutaneous-candidiasis', T('کاندیدیاز پوستی — روزی ۲ بار، ۲ هفته', 'Cutaneous candidiasis — twice daily, 2 weeks'), {}, 'notCalculated',
          {'reason': T('روزی ۲ بار (صبح و عصر) به مدت ۲ هفته.', 'Twice daily (morning and evening) for 2 weeks.')}, [d])],
     [CI('hyper', 'حساسیت به اجزای کرم.', 'Hypersensitivity to any ingredient.', [R(Ec, 'Contraindications')])])

Ct = fda('clotroche', 'FDA Clotrimazole troche', 'Clotrimazole lozenges 10 mg (Rising) — Prescribing Information', sid('clotroche')); d = R(Ct, 'Dosage and Administration')
patch('clotrimazole', add_forms=[form('troche-10', 'lozenge', 'oral', '10 mg lozenge (troche)', 10, 'mg', [R(Ct, 'How Supplied')], per='tablet')],
      add_regs=[reg('thrush', 'oral-candidiasis', T('برفک دهان — یک قرص مکیدنی ۵ بار در روز، ۱۴ روز (۳ سال به بالا)', 'Oral thrush — one lozenge 5 times daily, 14 days (≥3 y)'), {'minAge': age(3, 'year')}, 'fixed', {'perDose': 10, 'dosesPerDay': 5}, [d], allowed=['troche-10'], dur={'min': 14, 'max': 14},
                    notes=[note('آهسته در دهان حل شود؛ جویده یا بلعیده نشود.', 'Dissolve slowly in the mouth; do not chew or swallow whole.', [d])]),
                reg('thrush-proph', 'oral-candidiasis', T('پیشگیری از برفک در نقص ایمنی (شیمی‌درمانی، پرتودرمانی، کورتون) — یک قرص ۳ بار در روز', 'Thrush prophylaxis in immunosuppression (chemo, radiotherapy, steroids) — one lozenge 3 times daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 3}, [d], allowed=['troche-10'],
                    notes=[note('در طول شیمی‌درمانی یا تا کاهش کورتون به دوز نگهدارنده. ایمنی پیشگیری در کودکان ثابت نشده.', 'For the duration of chemotherapy or until steroids are reduced to maintenance. Prophylactic safety not established in children.', [d, R(Ct, 'Pediatric Use')])])],
      add_exs=[ex('thrush', 'troche-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'dosesPerDay': 5}, ageYears=30, weightKg=70), ex('thrush-proph', 'troche-10', {'perDose': 10, 'dosesPerDay': 3}, ageYears=50, weightKg=70)], pin_old=True)

Vf = fda('vfend', 'FDA Vfend IV', 'Vfend I.V. (voriconazole) for injection — Prescribing Information', sid('vfend'))
drug('voriconazole', 'anti-infectives', 'وریکونازول (وریدی)', 'Voriconazole (IV)', T('ضدقارچ تری‌آزول', 'Triazole antifungal'), [{'name': 'Vfend', 'market': 'US'}], ['vfend', 'وفند', 'وریکونازول'],
     [pv('vial-200', '200 mg vial (reconstitute to 10 mg/mL, dilute to ≤5 mg/mL)', 200, Vf, '3')],
     [reg('adult', 'invasive-fungal', T('بزرگسال و ۱۵ سال به بالا — نگهدارنده ۴ mg/kg هر ۱۲ ساعت (پس از بارگذاری)', 'Adults and ≥15 y — maintenance 4 mg/kg every 12 h (after loading)'), {'minAge': age(15, 'year')}, 'weightBased', {'perKgPerDose': 4, 'intervalHours': 12}, [R(Vf, '2.3, Table 1')],
          notes=[note('بارگذاری: ۶ mg/kg هر ۱۲ ساعت در ۲۴ ساعت اول. کاندیدمی: ۳ تا ۴ mg/kg. حداقل ۷ روز وریدی، سپس خوراکی ۲۰۰ mg هر ۱۲ ساعت (زیر ۴۰ kg نصف). انفوزیون ۱ تا ۳ ساعت، حداکثر ۳ mg/kg در ساعت؛ هرگز بولوس. ۱۲ تا ۱۴ سال با وزن ۵۰ kg و بیشتر: دوز بزرگسال.',
                      'Loading: 6 mg/kg every 12 h for the first 24 h. Candidaemia: 3–4 mg/kg. At least 7 days IV, then oral 200 mg every 12 h (half if <40 kg). Infuse over 1–3 h, max 3 mg/kg/h; never as a bolus. 12–14 y weighing ≥50 kg: adult dose.', [R(Vf, '2.3'), R(Vf, '2.1'), R(Vf, '2.4')])]),
      reg('child', 'invasive-fungal', T('کودک ۲ تا کمتر از ۱۲ سال — نگهدارنده ۸ mg/kg هر ۱۲ ساعت (پس از بارگذاری)', 'Child 2 to <12 y — maintenance 8 mg/kg every 12 h (after loading)'), {'minAge': age(2, 'year'), 'maxAge': age(12, 'year')}, 'weightBased', {'perKgPerDose': 8, 'intervalHours': 12}, [R(Vf, '2.4, Table 2')],
          notes=[note('بارگذاری: ۹ mg/kg هر ۱۲ ساعت در ۲۴ ساعت اول. همین دوز برای ۱۲ تا ۱۴ سال زیر ۵۰ kg. خوراکی: ۹ mg/kg هر ۱۲ ساعت (حداکثر ۳۵۰ mg).', 'Loading: 9 mg/kg every 12 h for the first 24 h. Same dose for 12–14 y under 50 kg. Oral: 9 mg/kg every 12 h (max 350 mg).', [R(Vf, '2.4')])])],
     [CI('hyper', 'حساسیت به وریکونازول.', 'Hypersensitivity to voriconazole.', [R(Vf, '4')]),
      CI('cyp', 'همراه با داروهای وابسته به CYP3A4 با عوارض خطرناک (مثل اپلرنون، ارگوت‌ها، ایوابرادین، لورازیدون، پیموزاید، کینیدین، سیرولیموس، تولواپتان) و القاکننده‌ها (کاربامازپین، باربیتورات طولانی‌اثر، ریفابوتین، ریفامپین، ریتوناویر دوز بالا، علف چای).',
         'With CYP3A4-dependent drugs causing serious reactions (e.g. eplerenone, ergot alkaloids, ivabradine, lurasidone, pimozide, quinidine, sirolimus, tolvaptan) and inducers (carbamazepine, long-acting barbiturates, rifabutin, rifampin, high-dose ritonavir, St John’s wort).', [R(Vf, '4')])],
     exs=[ex('adult', 'vial-200', {'perDose': 280}, ageYears=40, weightKg=70), ex('child', 'vial-200', {'perDose': 160}, ageYears=6, weightKg=20)])

Ab = fda('ambisome', 'FDA AmBisome', 'AmBisome (amphotericin B liposome) for injection — Prescribing Information', sid('ambisome')); d = R(Ab, 'Dosage and Administration')
NOTSWAP = note('با سایر فرآورده‌های آمفوتریسین B میلی‌گرم به میلی‌گرم قابل جایگزینی نیست. انفوزیون حدود ۱۲۰ دقیقه (در صورت تحمل ۶۰ دقیقه). فقط با آب استریل حل شود، نه سالین.',
               'Not interchangeable mg-for-mg with other amphotericin B products. Infuse over about 120 min (60 min if tolerated). Reconstitute with sterile water only, not saline.', [d])
drug('amphotericin-b-liposomal', 'anti-infectives', 'آمفوتریسین B لیپوزومال', 'Amphotericin B liposomal', T('ضدقارچ پلی‌ان', 'Polyene antifungal'), [{'name': 'AmBisome', 'market': 'US'}], ['ambisome', 'آمبیزوم', 'آمفوتریسین'],
     [pv('vial-50', '50 mg vial (4 mg/mL after reconstitution)', 50, Ab, 'Dosage and Administration — Reconstitution')],
     [reg('empiric', 'invasive-fungal', T('درمان تجربی تب نوتروپنیک — ۳ mg/kg/روز', 'Empirical therapy (febrile neutropenia) — 3 mg/kg/day'), {}, 'weightBased', {'perKgPerDay': 3, 'dividedDoses': 1}, [d], notes=[NOTSWAP]),
      reg('systemic', 'invasive-fungal', T('آسپرژیلوس، کاندیدا، کریپتوکوک — ۳ تا ۵ mg/kg/روز', 'Aspergillus, Candida, Cryptococcus — 3–5 mg/kg/day'), {}, 'weightBased', {'perKgPerDay': 3, 'perKgPerDayMax': 5, 'dividedDoses': 1}, [d], notes=[NOTSWAP]),
      reg('crypto-hiv', 'invasive-fungal', T('مننژیت کریپتوکوکی در HIV — ۶ mg/kg/روز', 'Cryptococcal meningitis in HIV — 6 mg/kg/day'), {}, 'weightBased', {'perKgPerDay': 6, 'dividedDoses': 1}, [d], notes=[NOTSWAP]),
      reg('vl', 'visceral-leishmaniasis', T('لیشمانیوز احشایی (ایمنی سالم) — ۳ mg/kg روزهای ۱ تا ۵، ۱۴ و ۲۱', 'Visceral leishmaniasis (immunocompetent) — 3 mg/kg on days 1–5, 14 and 21'), {}, 'weightBased', {'perKgPerDay': 3, 'dividedDoses': 1}, [d],
          notes=[note('فقط در روزهای ۱ تا ۵، ۱۴ و ۲۱. نقص ایمنی: ۴ mg/kg در روزهای ۱ تا ۵، ۱۰، ۱۷، ۲۴، ۳۱ و ۳۸.', 'Only on days 1–5, 14 and 21. Immunocompromised: 4 mg/kg on days 1–5, 10, 17, 24, 31 and 38.', [d]), NOTSWAP])],
     [CI('hyper', 'حساسیت به آمفوتریسین B یا اجزای فرآورده، مگر اینکه به نظر پزشک سود بیشتر از خطر باشد.', 'Hypersensitivity to amphotericin B or any component, unless the physician judges benefit outweighs risk.', [R(Ab, 'Contraindications')])],
     exs=[ex('empiric', 'vial-50', {'perDose': 210}, ageYears=40, weightKg=70), ex('systemic', 'vial-50', {'perDose': 60, 'upperPerDose': 100}, ageYears=6, weightKg=20),
          ex('crypto-hiv', 'vial-50', {'perDose': 360}, ageYears=35, weightKg=60), ex('vl', 'vial-50', {'perDose': 90}, ageYears=10, weightKg=30)])

# --- antivirals ---
At = fda('acyclovir-tab', 'FDA Acyclovir tablets', 'Acyclovir tablets 400/800 mg (Avet) — Prescribing Information', sid('acytab'))
Ac = fda('acyclovir-cap', 'FDA Acyclovir capsules', 'Acyclovir capsules 200 mg (Avet) — Prescribing Information', sid('acycap'))
Ai = fda('acyclovir-inj', 'FDA Acyclovir injection', 'Acyclovir sodium injection 50 mg/mL (AuroMedics) — Prescribing Information', sid('acyinj')); di = R(Ai, 'Dosage')
ORAL = ['tab-400', 'tab-800', 'cap-200']; dt = R(At, 'Dosage and Administration')
RENAL = note('نارسایی کلیه: کاهش دوز طبق جدول ۳ برچسب (مثلاً ۸۰۰ mg: CrCl ۱۰ تا ۲۵ هر ۸ ساعت، زیر ۱۰ هر ۱۲ ساعت).', 'Renal impairment: reduce per label Table 3 (e.g. 800 mg: CrCl 10–25 every 8 h, <10 every 12 h).', [dt])
IVN = note('انفوزیون یکنواخت در ۱ ساعت؛ هرگز بولوس، عضلانی یا زیرجلدی. حداکثر معادل ۲۰ mg/kg هر ۸ ساعت. چاقی: بر اساس وزن ایده‌آل. حجم نمایش‌داده‌شده از محلول غلیظ ۵۰ mg/mL است و پیش از انفوزیون رقیق شود.',
           'Infuse at a constant rate over 1 h; never bolus, IM or SC. Max equivalent of 20 mg/kg every 8 h. Obese patients: ideal body weight. The volume shown is of the 50 mg/mL concentrate, which must be diluted before infusion.', [R(Ai, 'Dosage and Administration'), di])
LIM = {'maxPerKgPerDose': 20, 'refs': [R(Ai, 'Dosage and Administration')]}
ivreg = lambda id, dis, fa, en, pop, mgkg, days: reg(id, dis, T(fa, en), pop, 'weightBased', {'perKgPerDose': mgkg, 'intervalHours': 8}, [di], allowed=['inj-50'], limits=LIM, dur={'min': days, 'max': days}, notes=[IVN])
d0 = patch('acyclovir',
      add_forms=[tab('tab-400', 400, '400 mg tablet', [R(At, 'How Supplied')]), tab('tab-800', 800, '800 mg tablet', [R(At, 'How Supplied')]), tab('cap-200', 200, '200 mg capsule', [R(Ac, 'How Supplied')], per='capsule', form_='capsule'),
                 liquid('inj-50', 50, 1, '50 mg/mL concentrate (10 or 20 mL vial) — dilute before IV infusion', [R(Ai, 'How Supplied')], form_='injection', route='iv')],
      add_regs=[reg('zoster', 'herpes-zoster', T('زونا — ۸۰۰ mg پنج بار در روز (هر ۴ ساعت)، ۷ تا ۱۰ روز', 'Herpes zoster — 800 mg five times daily (every 4 h), 7–10 days'), A18, 'fixed', {'perDose': 800, 'dosesPerDay': 5}, [dt], allowed=ORAL, dur={'min': 7, 'max': 10}, notes=[RENAL]),
                reg('gh-initial', 'genital-herpes', T('تبخال تناسلی — نوبت اول: ۲۰۰ mg پنج بار در روز، ۱۰ روز', 'Genital herpes — first episode: 200 mg five times daily, 10 days'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 5}, [dt], allowed=ORAL, dur={'min': 10, 'max': 10}, notes=[RENAL]),
                reg('gh-episodic', 'genital-herpes', T('تبخال تناسلی — عود (درمان متناوب): ۲۰۰ mg پنج بار در روز، ۵ روز', 'Genital herpes — recurrence (intermittent): 200 mg five times daily, 5 days'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 5}, [dt], allowed=ORAL, dur={'min': 5, 'max': 5},
                    notes=[note('در اولین علامت (پرودروم) شروع شود.', 'Start at the earliest sign or symptom (prodrome).', [dt]), RENAL]),
                reg('gh-suppress', 'genital-herpes', T('تبخال تناسلی — سرکوب مزمن: ۴۰۰ mg دو بار در روز تا ۱۲ ماه', 'Genital herpes — chronic suppression: 400 mg twice daily for up to 12 months'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 2}, [dt], allowed=ORAL,
                    notes=[note('پس از ۱ سال ارزیابی مجدد. رژیم‌های جایگزین: ۲۰۰ mg سه تا پنج بار در روز.', 'Re-evaluate after 1 year. Alternatives: 200 mg three to five times daily.', [dt]), RENAL]),
                ivreg('iv-hse-adult', 'hsv-encephalitis', 'آنسفالیت هرپسی — ۱۲ سال به بالا: ۱۰ mg/kg وریدی هر ۸ ساعت، ۱۰ روز', 'HSV encephalitis — ≥12 y: 10 mg/kg IV every 8 h, 10 days', {'minAge': age(12, 'year')}, 10, 10),
                ivreg('iv-hse-child', 'hsv-encephalitis', 'آنسفالیت هرپسی — ۳ ماه تا ۱۲ سال: ۲۰ mg/kg وریدی هر ۸ ساعت، ۱۰ روز', 'HSV encephalitis — 3 months to 12 y: 20 mg/kg IV every 8 h, 10 days', {'minAge': age(3, 'month'), 'maxAge': age(12, 'year')}, 20, 10),
                ivreg('iv-neonatal', 'hsv-encephalitis', 'هرپس نوزادی — تولد تا ۳ ماه: ۱۰ mg/kg وریدی هر ۸ ساعت، ۱۰ روز', 'Neonatal HSV — birth to 3 months: 10 mg/kg IV every 8 h, 10 days', {'maxAge': age(3, 'month')}, 10, 10),
                ivreg('iv-zoster-adult', 'herpes-zoster', 'زونا در نقص ایمنی — ۱۲ سال به بالا: ۱۰ mg/kg وریدی هر ۸ ساعت، ۷ روز', 'Zoster in immunocompromised — ≥12 y: 10 mg/kg IV every 8 h, 7 days', {'minAge': age(12, 'year')}, 10, 7),
                ivreg('iv-zoster-child', 'herpes-zoster', 'زونا در نقص ایمنی — زیر ۱۲ سال: ۲۰ mg/kg وریدی هر ۸ ساعت، ۷ روز', 'Zoster in immunocompromised — <12 y: 20 mg/kg IV every 8 h, 7 days', {'maxAge': age(12, 'year')}, 20, 7)],
      add_exs=[ex('zoster', 'tab-800', {'perDose': 800, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70), ex('gh-initial', 'cap-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=25, weightKg=60),
               ex('iv-hse-adult', 'inj-50', {'perDose': 700, 'mlPerDose': 14}, ageYears=40, weightKg=70), ex('iv-hse-child', 'inj-50', {'perDose': 400, 'mlPerDose': 8}, ageYears=6, weightKg=20),
               ex('gh-episodic', 'cap-200', {'perDose': 200, 'dosesPerDay': 5}, ageYears=25, weightKg=60), ex('gh-suppress', 'tab-400', {'perDose': 400, 'dosesPerDay': 2}, ageYears=25, weightKg=60),
               ex('iv-neonatal', 'inj-50', {'perDose': 35, 'mlPerDose': 0.7}, ageDays=10, weightKg=3.5), ex('iv-zoster-adult', 'inj-50', {'perDose': 700, 'mlPerDose': 14}, ageYears=40, weightKg=70),
               ex('iv-zoster-child', 'inj-50', {'perDose': 400, 'mlPerDose': 8}, ageYears=6, weightKg=20)], pin_old=True)
# Chickenpox dosing is the same in the tablet/capsule labels, so the old regimens also accept the oral solids.
p = find('acyclovir'); dd = json.load(open(p))
for r in dd['regimens']:
    if r['id'].startswith('chickenpox'): r['allowedFormulations'] = ['susp-200-5'] + ORAL
# The "oral forms <2 y" contraindication must not block the IV regimens for infants; every oral regimen already starts at 2 y.
for c in dd['contraindications']:
    if c['text']['en'].startswith('Oral forms not established'): c.pop('rule', None)
json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Vr = fda('viread', 'FDA Viread', 'Viread (tenofovir disoproxil fumarate) — Prescribing Information', sid('viread'))
drug('tenofovir-df', 'anti-infectives', 'تنوفوویر دیزوپروکسیل', 'Tenofovir disoproxil fumarate', T('آنالوگ نوکلئوتیدی ضد HBV/HIV', 'Nucleotide analogue (HBV/HIV)'), [{'name': 'Viread', 'market': 'US'}], ['viread', 'ویرید', 'تنوفوویر', 'TDF'],
     [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Vr, '3')]) for m in (150, 200, 250, 300)],
     [reg('hbv', 'hepatitis-b', T('هپاتیت B مزمن — یک بار در روز بر اساس وزن (۲ سال به بالا، ۱۷ kg به بالا برای قرص)', 'Chronic hepatitis B — once daily by weight (≥2 y, ≥17 kg for tablets)'), {'minAge': age(2, 'year'), 'minWeightKg': 17}, 'weightBand',
          {'weightBands': [{'minWeightKg': 17, 'maxWeightKg': 21.99, 'perDose': 150, 'dosesPerDay': 1}, {'minWeightKg': 22, 'maxWeightKg': 27.99, 'perDose': 200, 'dosesPerDay': 1},
                           {'minWeightKg': 28, 'maxWeightKg': 34.99, 'perDose': 250, 'dosesPerDay': 1}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 300, 'dosesPerDay': 1}]},
          [R(Vr, '2.2, Table 1')], notes=[note('با یا بدون غذا. دوز HIV همین است. پیش از شروع، تست HIV و HBV؛ کراتینین، CrCl، قند و پروتئین ادرار. CrCl ۳۰ تا ۴۹: هر ۴۸ ساعت؛ ۱۰ تا ۲۹: هر ۷۲ تا ۹۶ ساعت؛ همودیالیز: هفته‌ای یک بار پس از دیالیز.',
                                               'With or without food. Same dose for HIV. Before starting test for HIV and HBV; creatinine, CrCl, urine glucose and protein. CrCl 30–49: every 48 h; 10–29: every 72–96 h; haemodialysis: weekly after dialysis.', [R(Vr, '2.2'), R(Vr, '2.4'), R(Vr, '2')])])],
     warn=[W('هشدار جعبه‌ای: تشدید شدید هپاتیت B پس از قطع؛ کبد تا چند ماه پایش شود.', 'Boxed warning: severe acute exacerbation of hepatitis B after stopping; monitor liver for several months.', [R(Vr, 'Boxed Warning')])],
     exs=[ex('hbv', 'tab-300', {'perDose': 300, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('hbv', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=8, weightKg=25)])

Bc = fda('baraclude', 'FDA Baraclude', 'Baraclude (entecavir) tablets and oral solution — Prescribing Information', sid('baraclude'))
EB = lambda k: {'weightBands': [{'minWeightKg': 10, 'maxWeightKg': 11, 'perDose': 0.15 * k, 'dosesPerDay': 1}] + [{'minWeightKg': lo + 0.01, 'maxWeightKg': hi, 'perDose': round(v * k, 2), 'dosesPerDay': 1} for lo, hi, v in
                [(11, 14, 0.2), (14, 17, 0.25), (17, 20, 0.3), (20, 23, 0.35), (23, 26, 0.4), (26, 30, 0.45)]] + [{'minWeightKg': 30.01, 'maxWeightKg': None, 'perDose': 0.5 * k, 'dosesPerDay': 1}]}
EMPTY = note('با معده خالی (۲ ساعت پس از غذا و ۲ ساعت پیش از غذای بعد). CrCl زیر ۵۰: کاهش دوز طبق جدول ۲ برچسب.', 'On an empty stomach (2 h after a meal and 2 h before the next). CrCl <50: reduce per label Table 2.', [R(Bc, '2.1'), R(Bc, '2.4')])
drug('entecavir', 'anti-infectives', 'انتکاویر', 'Entecavir', T('آنالوگ نوکلئوزیدی ضد HBV', 'Nucleoside analogue (HBV)'), [{'name': 'Baraclude', 'market': 'US'}], ['baraclude', 'باراکلود', 'انتکاویر'],
     [tab('tab-0-5', 0.5, '0.5 mg tablet', [R(Bc, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Bc, '3')]), liquid('sol-0-05', 0.05, 1, '0.05 mg/mL oral solution', [R(Bc, '3')], form_='solution')],
     [reg('naive-adult', 'hepatitis-b', T('هپاتیت B — بدون درمان قبلی، ۱۶ سال به بالا: ۰٫۵ mg روزانه', 'Hepatitis B — treatment-naive, ≥16 y: 0.5 mg daily'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Bc, '2.2')], notes=[EMPTY]),
      reg('lam-adult', 'hepatitis-b', T('هپاتیت B — مقاوم به لامیوودین یا سیروز جبران‌نشده، ۱۶ سال به بالا: ۱ mg روزانه', 'Hepatitis B — lamivudine-refractory or decompensated, ≥16 y: 1 mg daily'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Bc, '2.2')], notes=[EMPTY]),
      reg('naive-child', 'hepatitis-b', T('هپاتیت B — کودک ۲ سال به بالا بدون درمان قبلی: بر اساس وزن', 'Hepatitis B — child ≥2 y, treatment-naive: by weight'), {'minAge': age(2, 'year'), 'maxAge': age(16, 'year'), 'minWeightKg': 10}, 'weightBand', EB(1), [R(Bc, '2.3, Table 1')],
          notes=[note('تا ۳۰ kg محلول خوراکی. بالای ۳۰ kg: ۱۰ mL محلول یا یک قرص ۰٫۵ mg.', 'Oral solution up to 30 kg. Over 30 kg: 10 mL solution or one 0.5 mg tablet.', [R(Bc, '2.3')]), EMPTY]),
      reg('lam-child', 'hepatitis-b', T('هپاتیت B — کودک ۲ سال به بالا با سابقه لامیوودین: بر اساس وزن (دو برابر)', 'Hepatitis B — child ≥2 y, lamivudine-experienced: by weight (double)'), {'minAge': age(2, 'year'), 'maxAge': age(16, 'year'), 'minWeightKg': 10}, 'weightBand', EB(2), [R(Bc, '2.3, Table 1')],
          notes=[note('بالای ۳۰ kg: ۲۰ mL محلول یا یک قرص ۱ mg.', 'Over 30 kg: 20 mL solution or one 1 mg tablet.', [R(Bc, '2.3')]), EMPTY])],
     warn=[W('هشدار جعبه‌ای: تشدید شدید هپاتیت B پس از قطع؛ در عفونت همزمان HIV بدون درمان ضدرتروویروسی خطر مقاومت HIV؛ اسیدوز لاکتیک و کبد چرب شدید.', 'Boxed warning: severe hepatitis B flare after stopping; HIV resistance risk in untreated HIV co-infection; lactic acidosis and severe hepatomegaly with steatosis.', [R(Bc, 'Boxed Warning')])],
     exs=[ex('naive-adult', 'tab-0-5', {'perDose': 0.5, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('naive-child', 'sol-0-05', {'perDose': 0.2, 'mlPerDose': 4}, ageYears=3, weightKg=12),
          ex('lam-adult', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('lam-child', 'sol-0-05', {'perDose': 0.4, 'mlPerDose': 8}, ageYears=3, weightKg=12)])

Ep = fda('epclusa', 'FDA Epclusa', 'Epclusa (sofosbuvir/velpatasvir) — Prescribing Information', sid('epclusa'))
sv = lambda id, s, v: form(id, 'tablet', 'oral', f'Sofosbuvir {s} mg + velpatasvir {v} mg tablet', s, 'mg', [R(Ep, '3')], per='tablet', components=comp(sofosbuvir=(('سوفوسبوویر', 'Sofosbuvir'), s), velpatasvir=(('ولپاتاسویر', 'Velpatasvir'), v)))
drug('sofosbuvir-velpatasvir', 'anti-infectives', 'سوفوسبوویر + ولپاتاسویر', 'Sofosbuvir + velpatasvir', T('ضد HCV (همه ژنوتیپ‌ها)', 'Pangenotypic anti-HCV'), [{'name': 'Epclusa', 'market': 'US'}], ['epclusa', 'اپکلوسا', 'سوفوسبوویر', 'ولپاتاسویر'],
     [sv('tab-400-100', 400, 100), sv('tab-200-50', 200, 50)],
     [reg('hcv', 'hepatitis-c', T('هپاتیت C — یک بار در روز، ۱۲ هفته (۳ سال به بالا، قرص از ۱۷ kg)', 'Hepatitis C — once daily for 12 weeks (≥3 y; tablets from 17 kg)'), {'minAge': age(3, 'year'), 'minWeightKg': 17}, 'weightBand',
          {'weightBands': [{'minWeightKg': 17, 'maxWeightKg': 29.99, 'perDose': 200, 'dosesPerDay': 1}, {'minWeightKg': 30, 'maxWeightKg': None, 'perDose': 400, 'dosesPerDay': 1}]}, [R(Ep, '2.3'), R(Ep, '2.4, Table 2')],
          doseComponent='sofosbuvir', dur={'min': 84, 'max': 84},
          notes=[note('دوز به‌صورت جزء سوفوسبوویر. زیر ۱۷ kg: پلت خوراکی ۱۵۰/۳۷٫۵ mg. سیروز جبران‌نشده: همراه ریباویرین. پیش از شروع HBsAg و anti-HBc.', 'Shown as the sofosbuvir component. Under 17 kg: 150/37.5 mg oral pellets. Decompensated cirrhosis: add ribavirin. Test HBsAg and anti-HBc before starting.', [R(Ep, '2.2'), R(Ep, '2.4'), R(Ep, '2.1')])])],
     [CI('rbv', 'ترکیب با ریباویرین در مواردی که ریباویرین ممنوع است.', 'Combination with ribavirin where ribavirin is contraindicated.', [R(Ep, '4')])],
     warn=[W('هشدار جعبه‌ای: فعال شدن مجدد HBV در عفونت همزمان HCV/HBV.', 'Boxed warning: HBV reactivation in HCV/HBV co-infection.', [R(Ep, 'Boxed Warning')]),
           W('برادی‌کاردی علامت‌دار شدید با آمیودارون.', 'Serious symptomatic bradycardia with amiodarone.', [R(Ep, '5.2')])],
     inter=[IA('amiodarone', 'آمیودارون: برادی‌کاردی شدید و نیاز به پیس‌میکر؛ یک مورد ایست قلبی کشنده با رژیم‌های سوفوسبوویر.', 'Amiodarone: severe bradycardia needing pacing; a fatal cardiac arrest with a sofosbuvir regimen.', [R(Ep, '5.2')])],
     exs=[ex('hcv', 'tab-400-100', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('hcv', 'tab-200-50', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=7, weightKg=22)])

Tr = fda('truvada', 'FDA Truvada', 'Truvada (emtricitabine/tenofovir DF) — Prescribing Information', sid('truvada'))
drug('emtricitabine-tenofovir', 'anti-infectives', 'امتریسیتابین + تنوفوویر (PrEP)', 'Emtricitabine + tenofovir DF (PrEP)', T('ضدرتروویروس', 'Antiretroviral'), [{'name': 'Truvada', 'market': 'US'}], ['truvada', 'تروادا', 'PrEP', 'پرپ'],
     [form('tab-200-300', 'tablet', 'oral', 'Emtricitabine 200 mg + tenofovir DF 300 mg tablet', 200, 'mg', [R(Tr, '3')], per='tablet',
           components=comp(emtricitabine=(('امتریسیتابین', 'Emtricitabine'), 200), tenofovir=(('تنوفوویر دیزوپروکسیل', 'Tenofovir DF'), 300)))],
     [reg('prep', 'hiv-prep', T('پیشگیری پیش از مواجهه HIV — یک قرص روزانه (۳۵ kg به بالا)', 'HIV PrEP — one tablet daily (≥35 kg)'), {'minWeightKg': 35}, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Tr, '2.5')], doseComponent='emtricitabine',
          notes=[note('دوز به‌صورت جزء امتریسیتابین (یک قرص ۲۰۰/۳۰۰). منفی بودن HIV درست پیش از شروع و دست‌کم هر ۳ ماه تأیید شود.', 'Shown as the emtricitabine component (one 200/300 tablet). Confirm HIV-negative immediately before starting and at least every 3 months.', [R(Tr, '2.5'), R(Tr, 'Boxed Warning')])])],
     [CI('hiv', 'برای PrEP در وضعیت HIV نامعلوم یا مثبت ممنوع.', 'Contraindicated for PrEP with unknown or positive HIV-1 status.', [R(Tr, '4')])],
     warn=[W('هشدار جعبه‌ای: تشدید هپاتیت B پس از قطع؛ مقاومت دارویی HIV اگر عفونت حاد تشخیص داده نشود.', 'Boxed warning: hepatitis B flare after stopping; HIV drug resistance if acute infection is missed.', [R(Tr, 'Boxed Warning')])],
     exs=[ex('prep', 'tab-200-300', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Px = fda('paxlovid', 'FDA Paxlovid', 'Paxlovid (nirmatrelvir; ritonavir) — Prescribing Information', sid('paxlovid'))
drug('nirmatrelvir-ritonavir', 'anti-infectives', 'نیرماترلویر + ریتوناویر', 'Nirmatrelvir + ritonavir', T('مهارکننده پروتئاز SARS-CoV-2', 'SARS-CoV-2 protease inhibitor'), [{'name': 'Paxlovid', 'market': 'US'}], ['paxlovid', 'پکسلووید', 'پاکسلووید', 'نیرماترلویر'],
     [tab('tab-150', 150, 'Nirmatrelvir 150 mg tablet (co-packaged with ritonavir 100 mg)', [R(Px, '3')])],
     [reg('covid', 'covid-19', T('کووید-۱۹ خفیف تا متوسط در بزرگسال پرخطر — ۳۰۰ mg نیرماترلویر + ۱۰۰ mg ریتوناویر دو بار در روز، ۵ روز', 'Mild–moderate COVID-19 in high-risk adults — nirmatrelvir 300 mg + ritonavir 100 mg twice daily, 5 days'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 2}, [R(Px, '2.2')], dur={'min': 5, 'max': 5},
          notes=[note('هر نوبت: ۲ قرص نیرماترلویر + ۱ قرص ریتوناویر با هم. eGFR ۳۰ تا ۶۰: ۱۵۰ mg + ۱۰۰ mg دو بار در روز. eGFR زیر ۳۰: روز اول ۳۰۰ + ۱۰۰ یک بار، روز ۲ تا ۵ ۱۵۰ + ۱۰۰ یک بار. نارسایی شدید کبد توصیه نمی‌شود.',
                      'Each dose: 2 nirmatrelvir tablets + 1 ritonavir tablet together. eGFR 30–60: 150 mg + 100 mg twice daily. eGFR <30: day 1 300 + 100 once, days 2–5 150 + 100 once daily. Not recommended in severe hepatic impairment.', [R(Px, '2.2'), R(Px, '2.3, Table 1'), R(Px, '2.4')])])],
     [CI('hyper', 'سابقه حساسیت مهم (TEN، استیونس-جانسون) به نیرماترلویر یا ریتوناویر.', 'History of clinically significant hypersensitivity (TEN, Stevens-Johnson) to nirmatrelvir or ritonavir.', [R(Px, '4')]),
      CI('cyp', 'داروهایی که عمدتاً با CYP3A متابولیزه می‌شوند و افزایش سطح آن‌ها خطرناک است، و القاکننده‌های قوی CYP3A — فهرست کامل در بخش ۴ برچسب.', 'Drugs highly dependent on CYP3A where raised levels are dangerous, and strong CYP3A inducers — full list in label section 4.', [R(Px, '4')])],
     warn=[W('هشدار جعبه‌ای: تداخلات دارویی مهم (ریتوناویر مهارکننده قوی CYP3A)؛ پیش از تجویز همه داروهای بیمار بررسی شود.', 'Boxed warning: significant drug interactions (ritonavir is a strong CYP3A inhibitor); review all medicines before prescribing.', [R(Px, 'Boxed Warning')])],
     exs=[ex('covid', 'tab-150', {'perDose': 300, 'tabletsPerDoseRounded': 2}, ageYears=60, weightKg=70)])

Xf = fda('xofluza', 'FDA Xofluza', 'Xofluza (baloxavir marboxil) — Prescribing Information', sid('xofluza')); dx = R(Xf, '2.2, Tables 1–3')
XB = {'weightBands': [{'minWeightKg': 20, 'maxWeightKg': 79.99, 'perDose': 40, 'dosesPerDay': 1}, {'minWeightKg': 80, 'maxWeightKg': None, 'perDose': 80, 'dosesPerDay': 1}]}
XN = note('یک دوز، هرچه زودتر و ظرف ۴۸ ساعت از شروع علائم یا تماس. همزمان با لبنیات، نوشیدنی غنی از کلسیم، آنتی‌اسید، ملین یا مکمل کلسیم، آهن، منیزیم، سلنیوم یا روی مصرف نشود.',
          'Single dose, as soon as possible and within 48 h of symptom onset or contact. Not with dairy, calcium-fortified drinks, antacids, laxatives or calcium, iron, magnesium, selenium or zinc supplements.', [R(Xf, '2.2'), R(Xf, '2.1')])
drug('baloxavir', 'anti-infectives', 'بالوکساویر', 'Baloxavir marboxil', T('ضد آنفلوانزا (مهارکننده اندونوکلئاز)', 'Anti-influenza (endonuclease inhibitor)'), [{'name': 'Xofluza', 'market': 'US'}], ['xofluza', 'زوفلوزا', 'بالوکساویر'],
     [tab('tab-40', 40, '40 mg tablet', [R(Xf, '3')]), tab('tab-80', 80, '80 mg tablet', [R(Xf, '3')]), liquid('susp-2', 40, 20, '2 mg/mL suspension (40 mg/20 mL bottle after reconstitution)', [R(Xf, '3'), R(Xf, '2.4')])],
     [reg('treat', 'influenza', T('آنفلوانزای بدون عارضه — یک دوز بر اساس وزن (۵ سال به بالا، ۲۰ kg به بالا)', 'Uncomplicated influenza — single dose by weight (≥5 y, ≥20 kg)'), {'minAge': age(5, 'year'), 'minWeightKg': 20}, 'weightBand', XB, [dx], dur={'min': 1, 'max': 1}, notes=[XN]),
      reg('treat-small', 'influenza', T('آنفلوانزا — زیر ۲۰ kg (۵ سال به بالا): ۲ mg/kg یک دوز سوسپانسیون', 'Influenza — under 20 kg (≥5 y): 2 mg/kg single dose of suspension'), {'minAge': age(5, 'year'), 'maxWeightKg': 19.99}, 'weightBased', {'perKgPerDay': 2, 'dividedDoses': 1}, [dx], allowed=['susp-2'], dur={'min': 1, 'max': 1}, notes=[XN]),
      reg('pep', 'influenza-prophylaxis', T('پیشگیری پس از تماس — یک دوز بر اساس وزن (۵ سال به بالا، ۲۰ kg به بالا)', 'Post-exposure prophylaxis — single dose by weight (≥5 y, ≥20 kg)'), {'minAge': age(5, 'year'), 'minWeightKg': 20}, 'weightBand', XB, [dx], dur={'min': 1, 'max': 1}, notes=[XN]),
      reg('pep-small', 'influenza-prophylaxis', T('پیشگیری پس از تماس — زیر ۲۰ kg (۵ سال به بالا): ۲ mg/kg سوسپانسیون', 'Post-exposure prophylaxis — under 20 kg (≥5 y): 2 mg/kg suspension'), {'minAge': age(5, 'year'), 'maxWeightKg': 19.99}, 'weightBased', {'perKgPerDay': 2, 'dividedDoses': 1}, [dx], allowed=['susp-2'], dur={'min': 1, 'max': 1}, notes=[XN])],
     [CI('hyper', 'سابقه حساسیت به بالوکساویر (آنافیلاکسی، آنژیوادم، کهیر، اریتم مولتی‌فرم).', 'History of hypersensitivity to baloxavir (anaphylaxis, angioedema, urticaria, erythema multiforme).', [R(Xf, '4')])],
     inter=[IA('cations', 'لبنیات، آنتی‌اسید و مکمل‌های کلسیم، آهن، منیزیم، سلنیوم و روی جذب را کم می‌کنند.', 'Dairy, antacids and calcium, iron, magnesium, selenium and zinc supplements reduce absorption.', [R(Xf, '2.1')])],
     exs=[ex('treat', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70), ex('treat', 'tab-80', {'perDose': 80, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=90),
          ex('treat-small', 'susp-2', {'perDose': 36, 'mlPerDose': 18}, ageYears=6, weightKg=18),
          ex('pep', 'tab-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=40), ex('pep-small', 'susp-2', {'perDose': 34, 'mlPerDose': 17}, ageYears=5, weightKg=17)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'emergency':
        col['drugs'] += [x for x in ['acyclovir', 'amphotericin-b-liposomal', 'voriconazole'] if x not in col['drugs']]
    if col['id'] == 'sexual-health':
        col['drugs'] += [x for x in ['emtricitabine-tenofovir', 'acyclovir'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s3 ok')
