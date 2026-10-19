"""Stage 13a (part 2) — ceftaroline, rifabutin, rifapentine, pretomanid, peramivir, molnupiravir, ledipasvir/sofosbuvir, glecaprevir/pibrentasvir, nevirapine, lopinavir/ritonavir, fesoterodine, brinzolamide."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's13_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
cap = lambda id, mg, src, label=None, sec='3': tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
HCV_W = lambda src: W('هشدار جعبه‌ای: فعال شدن مجدد HBV در عفونت همزمان (گاه نارسایی کبد و مرگ) — پیش از شروع HBsAg و anti-HBc.', 'Boxed warning: HBV reactivation in HCV/HBV co-infection (sometimes fulminant hepatitis and death) — test HBsAg and anti-HBc first.', [R(src, 'Boxed Warning')])

add_disease('latent-tuberculosis', 'عفونت نهفته سل', 'Latent tuberculosis infection', ['LTBI', 'سل نهفته', 'PPD مثبت'], ['Z22.7'], 'infectious')
add_disease('mac-infection', 'عفونت منتشر مایکوباکتریوم آویوم (MAC) در HIV', 'Disseminated Mycobacterium avium complex (MAC) in HIV', ['MAC', 'MAI', 'مایکوباکتریوم آویوم'], ['A31.2'], 'infectious')

Tf = fda('teflaro', 'FDA Teflaro', 'Teflaro (ceftaroline fosamil) for injection — Prescribing Information', sid('ceftaroline'))
drug('ceftaroline', 'anti-infectives', 'سفتارولین', 'Ceftaroline fosamil', T('سفالوسپورین نسل پنجم (فعال علیه MRSA)', 'Fifth-generation cephalosporin (anti-MRSA)'), [{'name': 'Teflaro', 'market': 'US'}], ['teflaro', 'zinforo', 'تفلارو', 'سفتارولین'],
     [form('vial-600', 'powder-for-injection', 'iv', '600 mg vial', 600, 'mg', [R(Tf, '3')], per='vial'), form('vial-400', 'powder-for-injection', 'iv', '400 mg vial', 400, 'mg', [R(Tf, '3')], per='vial')],
     [reg('adult', 'skin-soft-tissue-infection', T('عفونت حاد پوست (۵ تا ۱۴ روز) یا پنومونی اکتسابی (۵ تا ۷ روز) — بزرگسال ۶۰۰ mg هر ۱۲ ساعت', 'ABSSSI (5–14 days) or CABP (5–7 days) — adult 600 mg every 12 h'), A18, 'fixed', {'perDose': 600, 'dosesPerDay': 2}, [R(Tf, '2.1, Table 1')], allowed=['vial-600'],
          notes=[note('انفوزیون ۵ تا ۶۰ دقیقه.', 'Infuse over 5–60 min.', [R(Tf, '2.1')])]),
      reg('cap', 'community-acquired-pneumonia', T('پنومونی اکتسابی از جامعه — بزرگسال ۶۰۰ mg هر ۱۲ ساعت، ۵ تا ۷ روز', 'Community-acquired pneumonia — adult 600 mg every 12 h for 5–7 days'), A18, 'fixed', {'perDose': 600, 'dosesPerDay': 2}, [R(Tf, '2.1, Table 1')], dur={'min': 5, 'max': 7}, allowed=['vial-600']),
      reg('inf', 'skin-soft-tissue-infection', T('کودک ۲ ماه تا <۲ سال — ۸ mg/kg هر ۸ ساعت', 'Children 2 months–<2 y — 8 mg/kg every 8 h'), {'minAge': age(2, 'month'), 'maxAge': age(2, 'year')}, 'weightBased', {'perKgPerDose': 8, 'intervalHours': 8}, [R(Tf, '2.2, Table 2')], allowed=['vial-400']),
      reg('child', 'skin-soft-tissue-infection', T('کودک ۲ تا <۱۸ سال و ≤۳۳ kg — ۱۲ mg/kg هر ۸ ساعت', 'Children 2–<18 y and ≤33 kg — 12 mg/kg every 8 h'), {'minAge': age(2, 'year'), 'maxAge': age(18, 'year'), 'maxWeightKg': 33}, 'weightBased', {'perKgPerDose': 12, 'intervalHours': 8}, [R(Tf, '2.2, Table 2')], allowed=['vial-400'],
          notes=[note('بالای ۳۳ kg: ۴۰۰ mg هر ۸ ساعت یا ۶۰۰ mg هر ۱۲ ساعت. زیر ۲ ماه فقط برای عفونت پوست طبق جدول ۳.', '>33 kg: 400 mg every 8 h or 600 mg every 12 h. Under 2 months only for ABSSSI per Table 3.', [R(Tf, '2.2, Table 2'), R(Tf, '2.2')])])],
     [CI('hyper', 'حساسیت جدی به سفتارولین یا سایر سفالوسپورین‌ها.', 'Serious hypersensitivity to ceftaroline or other cephalosporins.', [R(Tf, '4')])],
     warn=[W('واکنش حساسیتی (حساسیت متقاطع با بتالاکتام‌ها)؛ اسهال C. difficile؛ عوارض عصبی (انسفالوپاتی، تشنج) به‌ویژه در نارسایی کلیه؛ تست کومبس مثبت.', 'Hypersensitivity (beta-lactam cross-reactivity); C. difficile diarrhoea; neurological reactions (encephalopathy, seizures) especially in renal impairment; positive Coombs test.', [R(Tf, '5')])],
     renal=[{'egfrBelow': 51, 'severity': 'warn', 'text': T('ClCr ۵۰ و کمتر: کاهش دوز طبق جدول برچسب.', 'CrCl ≤50: reduce dose per label table.'), 'refs': [R(Tf, '2.3')]}],
     exs=[ex('adult', 'vial-600', {'perDose': 600, 'dosesPerDay': 2}, ageYears=50, weightKg=70), ex('cap', 'vial-600', {'perDose': 600}, ageYears=50, weightKg=70),
          ex('inf', 'vial-400', {'perDose': 80}, ageMonths=10, weightKg=10), ex('child', 'vial-400', {'perDose': 240}, ageYears=6, weightKg=20)])

Rb = fda('rifabutin', 'FDA Rifabutin', 'Rifabutin capsules USP 150 mg (ANI/Novitium) — Prescribing Information', sid('rifabutin')); d = R(Rb, 'Dosage and Administration')
drug('rifabutin', 'anti-infectives', 'ریفابوتین', 'Rifabutin', T('ریفامایسین', 'Rifamycin'), [{'name': 'Mycobutin', 'market': 'US'}], ['mycobutin', 'مایکوبوتین', 'ریفابوتین'],
     [cap('cap-150', 150, Rb, sec='How Supplied')],
     [reg('mac', 'mac-infection', T('پیشگیری MAC منتشر در HIV پیشرفته — ۳۰۰ mg یک بار در روز', 'Prevention of disseminated MAC in advanced HIV — 300 mg once daily'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [d],
          notes=[note('در تهوع: ۱۵۰ mg دو بار با غذا. در سل فعال تک‌دارویی نه (مقاومت). با لوپیناویر/ریتوناویر دست‌کم ۷۵٪ کاهش.', 'If nausea: 150 mg twice daily with food. Never alone in active TB (resistance). With lopinavir/ritonavir reduce by at least 75%.', [d, R(Rb, 'Warnings'), R(Rb, 'Precautions')])])],
     [CI('ci', 'حساسیت به ریفابوتین یا سایر ریفامایسین‌ها؛ کابوتگراویر/ریلپیویرین تزریقی.', 'Hypersensitivity to rifabutin or other rifamycins; cabotegravir/rilpivirine injectable.', [R(Rb, 'Contraindications')])],
     warn=[W('در سل فعال نباید برای پیشگیری MAC داده شود؛ اسهال C. difficile؛ تغییر رنگ ادرار و اشک؛ یووئیت.', 'Must not be used for MAC prophylaxis in active TB; C. difficile diarrhoea; discoloured urine and tears; uveitis.', [R(Rb, 'Warnings')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰: دوز ۵۰٪ کم شود.', 'CrCl <30: consider reducing the dose by 50%.'), 'refs': [d]}],
     exs=[ex('mac', 'cap-150', {'perDose': 300, 'tabletsPerDoseRounded': 2}, ageYears=40, weightKg=65)])

Pf = fda('priftin', 'FDA Priftin', 'Priftin (rifapentine) tablets 150 mg — Prescribing Information', sid('rifapentine'))
drug('rifapentine', 'anti-infectives', 'ریفاپنتین', 'Rifapentine', T('ریفامایسین', 'Rifamycin'), [{'name': 'Priftin', 'market': 'US'}], ['priftin', 'پریفتین', 'ریفاپنتین'],
     [tab('tab-150', 150, '150 mg tablet', [R(Pf, '3')])],
     [reg('ltbi', 'latent-tuberculosis', T('سل نهفته (۲ سال به بالا) — هفته‌ای یک بار بر اساس وزن همراه ایزونیازید، ۱۲ هفته (DOT)', 'Latent TB (≥2 y) — once weekly by weight with isoniazid for 12 weeks (DOT)'), {'minAge': age(2, 'year'), 'minWeightKg': 10}, 'weightBand',
          {'weightBands': [{'minWeightKg': 10, 'maxWeightKg': 14, 'perDose': 300, 'dosesPerDay': 1}, {'minWeightKg': 14.01, 'maxWeightKg': 25, 'perDose': 450, 'dosesPerDay': 1}, {'minWeightKg': 25.01, 'maxWeightKg': 32, 'perDose': 600, 'dosesPerDay': 1},
                           {'minWeightKg': 32.01, 'maxWeightKg': 50, 'perDose': 750, 'dosesPerDay': 1}, {'minWeightKg': 50.01, 'maxWeightKg': None, 'perDose': 900, 'dosesPerDay': 1}]}, [R(Pf, '2.2, Table 1')], dur=ONE,
          notes=[note('ایزونیازید هفتگی ۱۵ mg/kg (۱۲ سال به بالا) یا ۲۵ mg/kg (۲ تا ۱۱ سال)، حداکثر ۹۰۰ mg. با غذا.', 'Weekly isoniazid 15 mg/kg (≥12 y) or 25 mg/kg (2–11 y), max 900 mg. With meals.', [R(Pf, '2.2'), R(Pf, '2.3')])]),
      reg('tb', 'tuberculosis', T('سل ریوی فعال حساس — ۶۰۰ mg دو بار در هفته ۲ ماه، سپس یک بار در هفته ۴ ماه (DOT)', 'Active drug-susceptible pulmonary TB — 600 mg twice weekly for 2 months, then once weekly for 4 months (DOT)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 600, 'dosesPerDay': 1}, [R(Pf, '2.1')], dur=ONE,
          notes=[note('همراه سایر داروهای ضدسل؛ دست‌کم ۷۲ ساعت بین دوزهای مرحله اول. در سویه مقاوم به ریفامپین نه.', 'With other antituberculosis drugs; at least 72 h between initial-phase doses. Not for rifampin-resistant strains.', [R(Pf, '2.1')])])],
     [CI('hyper', 'حساسیت به ریفامایسین‌ها.', 'Hypersensitivity to rifamycins.', [R(Pf, '4')])],
     warn=[W('سمیت کبدی؛ واکنش حساسیتی و پوستی شدید؛ عود سل؛ تداخلات دارویی زیاد (القاگر CYP3A)؛ تغییر رنگ مایعات بدن؛ پورفیری.', 'Hepatotoxicity; hypersensitivity and severe skin reactions; TB relapse; many drug interactions (CYP3A inducer); body-fluid discoloration; porphyria.', [R(Pf, '5')])],
     exs=[ex('ltbi', 'tab-150', {'perDose': 900, 'tabletsPerDoseRounded': 6}, ageYears=30, weightKg=70), ex('ltbi', 'tab-150', {'perDose': 450, 'tabletsPerDoseRounded': 3}, ageYears=5, weightKg=18),
          ex('tb', 'tab-150', {'perDose': 600, 'tabletsPerDoseRounded': 4}, ageYears=30, weightKg=70)])

Pm = fda('pretomanid', 'FDA Pretomanid', 'Pretomanid tablets 200 mg — Prescribing Information', sid('pretomanid'))
drug('pretomanid', 'anti-infectives', 'پرتومانید', 'Pretomanid', T('نیتروایمیدازوکسازین (ضدسل)', 'Nitroimidazooxazine (antimycobacterial)'), [{'name': 'Pretomanid', 'market': 'US'}], ['pretomanid', 'پرتومانید', 'BPaL'],
     [tab('tab-200', 200, '200 mg tablet', [R(Pm, '3')])],
     [reg('mdr', 'tuberculosis', T('سل ریوی مقاوم (XDR یا MDR غیرپاسخ‌دهنده) — ۲۰۰ mg یک بار در روز ۲۶ هفته همراه بداکیلین و لینزولید', 'Pulmonary XDR or treatment-intolerant/non-responsive MDR-TB — 200 mg once daily for 26 weeks with bedaquiline and linezolid'), A18, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Pm, '2.2')],
          notes=[note('فقط همراه بداکیلین و لینزولید، با غذا، تحت DOT. پیش از شروع آزمایش کبد، CBC، ECG و الکترولیت. اگر بداکیلین یا پرتومانید قطع شود کل رژیم قطع.', 'Only with bedaquiline and linezolid, with food, under DOT. Liver tests, CBC, ECG and electrolytes before starting. If bedaquiline or pretomanid stops, stop the whole regimen.', [R(Pm, '2.1'), R(Pm, '2.3'), R(Pm, '2.4')])])],
     [CI('ci', 'هر منع مصرف بداکیلین یا لینزولید.', 'Any contraindication to bedaquiline or linezolid.', [R(Pm, '4')])],
     warn=[W('سمیت کبدی؛ سرکوب مغز استخوان؛ نوروپاتی محیطی و بینایی؛ طولانی شدن QT؛ اسیدوز لاکتیک؛ اثر بر باروری مردان.', 'Hepatotoxicity; myelosuppression; peripheral and optic neuropathy; QT prolongation; lactic acidosis; male reproductive effects.', [R(Pm, '5')])],
     exs=[ex('mdr', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=60)])

Rp = fda('rapivab', 'FDA Rapivab', 'Rapivab (peramivir) injection 200 mg/20 mL — Prescribing Information', sid('peramivir'))
drug('peramivir', 'anti-infectives', 'پرامیویر', 'Peramivir', T('مهارکننده نورآمینیداز (وریدی)', 'IV neuraminidase inhibitor'), [{'name': 'Rapivab', 'market': 'US'}], ['rapivab', 'راپیواب', 'پرامیویر'],
     [form('vial-10', 'injection', 'iv', '200 mg/20 mL (10 mg/mL) vial', 10, 'mg', [R(Rp, '3')], vol=1)],
     [reg('adult', 'influenza', T('آنفلوانزای حاد بدون عارضه (۱۳ سال به بالا) — ۶۰۰ mg وریدی یک دوز ظرف ۲ روز از شروع علائم', 'Acute uncomplicated influenza (≥13 y) — 600 mg IV single dose within 2 days of symptom onset'), {'minAge': age(13, 'year')}, 'fixed', {'perDose': 600, 'dosesPerDay': 1}, [R(Rp, '2.1')], dur=ONE,
          notes=[note('انفوزیون دست‌کم ۱۵ دقیقه.', 'Infuse over at least 15 min.', [R(Rp, '2.1')])]),
      reg('child', 'influenza', T('کودک ۶ ماه تا ۱۲ سال — ۱۲ mg/kg وریدی یک دوز (حداکثر ۶۰۰ mg)', 'Children 6 months–12 y — 12 mg/kg IV single dose (max 600 mg)'), {'minAge': age(6, 'month'), 'maxAge': age(13, 'year')}, 'weightBased', {'perKgPerDose': 12, 'intervalHours': 24}, [R(Rp, '2.1')], dur=ONE,
          limits={'maxPerDose': 600, 'refs': [R(Rp, '2.1')]})],
     [CI('hyper', 'حساسیت جدی یا آنافیلاکسی به پرامیویر.', 'Serious hypersensitivity or anaphylaxis to peramivir.', [R(Rp, '4')])],
     warn=[W('واکنش پوستی و حساسیتی شدید (SJS)؛ رویدادهای عصبی-روانی (به‌ویژه کودکان)؛ عفونت باکتریایی همزمان.', 'Serious skin/hypersensitivity reactions (SJS); neuropsychiatric events (especially children); bacterial co-infection.', [R(Rp, '5')])],
     renal=[{'egfrBelow': 50, 'severity': 'warn', 'text': T('ClCr زیر ۵۰: کاهش دوز طبق جداول ۱ و ۲؛ همودیالیز پس از دیالیز.', 'CrCl <50: reduce per Tables 1 and 2; haemodialysis — give after dialysis.'), 'refs': [R(Rp, '2.2')]}],
     exs=[ex('adult', 'vial-10', {'perDose': 600, 'mlPerDose': 60}, ageYears=40, weightKg=70), ex('child', 'vial-10', {'perDose': 240, 'mlPerDose': 24}, ageYears=6, weightKg=20)])

Lg = fda('lagevrio', 'FDA Lagevrio (EUA)', 'Lagevrio (molnupiravir) capsules — Fact Sheet for Healthcare Providers (EUA)', sid('molnupiravir'))
drug('molnupiravir', 'anti-infectives', 'مولنوپیراویر', 'Molnupiravir', T('آنالوگ نوکلئوزید ضد SARS-CoV-2', 'Nucleoside analogue (SARS-CoV-2)'), [{'name': 'Lagevrio', 'market': 'US'}], ['lagevrio', 'لاگوریو', 'مولنوپیراویر'],
     [cap('cap-200', 200, Lg)],
     [reg('covid', 'covid-19', T('کووید-۱۹ خفیف تا متوسط پرخطر بزرگسال (مجوز اضطراری) — ۸۰۰ mg هر ۱۲ ساعت، ۵ روز', 'Mild-to-moderate COVID-19 at high risk, adults (EUA) — 800 mg every 12 h for 5 days'), A18, 'fixed', {'perDose': 800, 'dosesPerDay': 2}, [R(Lg, '2.1')], dur={'min': 5, 'max': 5},
          notes=[note('هرچه زودتر و ظرف ۵ روز از شروع علائم. تنظیم کلیوی یا کبدی ندارد. فقط با مجوز استفاده اضطراری (EUA).', 'As soon as possible and within 5 days of symptom onset. No renal or hepatic adjustment. Emergency Use Authorization only.', [R(Lg, '2.1'), R(Lg, '2.2')])])],
     warn=[W('سمیت جنینی (در بارداری توصیه نمی‌شود؛ پیشگیری حین درمان و ۴ روز بعد)؛ حساسیت؛ سمیت استخوان و غضروف (زیر ۱۸ سال نه).', 'Embryo-fetal toxicity (not recommended in pregnancy; contraception during and 4 days after); hypersensitivity; bone and cartilage toxicity (not under 18).', [R(Lg, '5')])],
     exs=[ex('covid', 'cap-200', {'perDose': 800, 'tabletsPerDoseRounded': 4}, ageYears=60, weightKg=75)])

Hv = fda('harvoni', 'FDA Harvoni', 'Harvoni (ledipasvir/sofosbuvir) tablets and pellets — Prescribing Information', sid('ledipasvir'))
drug('ledipasvir-sofosbuvir', 'anti-infectives', 'لدیپاسویر/سوفوسبوویر', 'Ledipasvir/sofosbuvir', T('ضد ویروس مستقیم HCV', 'HCV direct-acting antiviral'), [{'name': 'Harvoni', 'market': 'US'}], ['harvoni', 'هاروونی', 'ledipasvir', 'لدیپاسویر', 'sovodak'],
     [form('tab-90', 'tablet', 'oral', '90 mg ledipasvir / 400 mg sofosbuvir tablet', 90, 'mg', [R(Hv, '3')], per='tablet'), form('tab-45', 'tablet', 'oral', '45 mg / 200 mg tablet', 45, 'mg', [R(Hv, '3')], per='tablet')],
     [reg('hcv', 'hepatitis-c', T('هپاتیت C ژنوتیپ ۱، ۴، ۵، ۶ — یک قرص ۹۰/۴۰۰ mg یک بار (معمولاً ۱۲ هفته)', 'Hepatitis C genotype 1, 4, 5, 6 — one 90/400 mg tablet once daily (usually 12 weeks)'), {'minAge': age(3, 'year'), 'minWeightKg': 35}, 'fixed', {'perDose': 90, 'dosesPerDay': 1}, [R(Hv, '2.3'), R(Hv, '2.4, Table 2')], doseComponent='ledipasvir',
          notes=[note('مدت طبق جدول ۱ (۸ تا ۲۴ هفته؛ با یا بدون ریباویرین). کودک ۱۷ تا <۳۵ kg: ۴۵/۲۰۰ mg؛ زیر ۱۷ kg: پلت ۳۳٫۷۵/۱۵۰ mg. نارسایی کلیه تنظیم ندارد.', 'Duration per Table 1 (8–24 weeks; with or without ribavirin). Children 17–<35 kg: 45/200 mg; <17 kg: 33.75/150 mg pellets. No renal adjustment.', [R(Hv, '2.2'), R(Hv, '2.4, Table 2'), R(Hv, '2.6')])]),
      reg('child', 'hepatitis-c', T('کودک ۳ سال به بالا، ۱۷ تا <۳۵ kg — ۴۵/۲۰۰ mg یک بار', 'Children ≥3 y, 17–<35 kg — 45/200 mg once daily'), {'minAge': age(3, 'year'), 'minWeightKg': 17, 'maxWeightKg': 34.99}, 'fixed', {'perDose': 45, 'dosesPerDay': 1}, [R(Hv, '2.4, Table 2')], allowed=['tab-45'], doseComponent='ledipasvir')],
     [CI('ci', 'در صورت مصرف همراه ریباویرین، منع مصرف‌های ریباویرین هم صدق می‌کند.', 'When given with ribavirin, ribavirin contraindications also apply.', [R(Hv, '4')])],
     warn=[HCV_W(Hv), W('برادیکاردی شدید علامت‌دار با آمیودارون (همزمان توصیه نمی‌شود)؛ کاهش اثر با القاگرهای P-gp (ریفامپین، گل راعی).', 'Serious symptomatic bradycardia with amiodarone (not recommended together); reduced effect with P-gp inducers (rifampin, St John’s wort).', [R(Hv, '5')])],
     exs=[ex('hcv', 'tab-90', {'perDose': 90, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70), ex('child', 'tab-45', {'perDose': 45, 'tabletsPerDoseRounded': 1}, ageYears=7, weightKg=25)])

Mv = fda('mavyret', 'FDA Mavyret', 'Mavyret (glecaprevir/pibrentasvir) tablets and pellets — Prescribing Information', sid('glecaprevir'))
drug('glecaprevir-pibrentasvir', 'anti-infectives', 'گلکاپرویر/پیبرنتاسویر', 'Glecaprevir/pibrentasvir', T('ضد ویروس مستقیم HCV (پان‌ژنوتیپ)', 'Pangenotypic HCV direct-acting antiviral'), [{'name': 'Mavyret', 'market': 'US'}], ['mavyret', 'maviret', 'ماویرت', 'glecaprevir', 'گلکاپرویر'],
     [form('tab-100', 'tablet', 'oral', '100 mg glecaprevir / 40 mg pibrentasvir tablet', 100, 'mg', [R(Mv, '3')], per='tablet')],
     [reg('hcv', 'hepatitis-c', T('هپاتیت C همه ژنوتیپ‌ها (بزرگسال و ≥۱۲ سال یا ≥۴۵ kg) — ۳ قرص با هم یک بار با غذا؛ درمان‌نشده ۸ هفته', 'Hepatitis C, all genotypes (adults and ≥12 y or ≥45 kg) — 3 tablets together once daily with food; treatment-naive 8 weeks'), {'minAge': age(3, 'year'), 'minWeightKg': 45}, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Mv, '2.3'), R(Mv, '2.4')], doseComponent='glecaprevir',
          notes=[note('مدت طبق جداول ۱ و ۲ (درمان‌شده قبلی یا پیوند ۱۲ تا ۱۶ هفته). ۳ تا <۱۲ سال و زیر ۴۵ kg: پلت بر اساس وزن. هر درجه نارسایی کلیه تنظیم ندارد.', 'Duration per Tables 1–2 (experienced or transplant 12–16 weeks). 3–<12 y and <45 kg: weight-based pellets. No adjustment for any renal impairment.', [R(Mv, '2.2'), R(Mv, '2.6'), R(Mv, '2.4')])])],
     [CI('ci', 'نارسایی متوسط یا شدید کبد (Child-Pugh B/C) یا سابقه جبران‌نشدن کبد؛ آتازاناویر یا ریفامپین همزمان.', 'Moderate or severe hepatic impairment (Child-Pugh B/C) or prior hepatic decompensation; concomitant atazanavir or rifampin.', [R(Mv, '4')])],
     warn=[HCV_W(Mv), W('جبران‌نشدن یا نارسایی کبد در سیروز پیشرفته.', 'Hepatic decompensation/failure in advanced cirrhosis.', [R(Mv, '5.2')])],
     exs=[ex('hcv', 'tab-100', {'perDose': 300, 'tabletsPerDoseRounded': 3}, ageYears=45, weightKg=70)])

Nv = fda('nevirapine', 'FDA Nevirapine', 'Nevirapine tablets USP 200 mg (Aurobindo) — Prescribing Information', sid('nevirapine'))
drug('nevirapine', 'anti-infectives', 'نویراپین', 'Nevirapine', T('NNRTI', 'NNRTI'), [{'name': 'Viramune', 'market': 'US'}], ['viramune', 'ویرامون', 'نویراپین', 'NVP'],
     [tab('tab-200', 200, '200 mg tablet (scored)', [R(Nv, '3')], scored=True)],
     [reg('adult', 'hiv', T('HIV-1 بزرگسال (۱۶ سال به بالا) — ۲۰۰ mg یک بار ۱۴ روز، سپس ۲۰۰ mg دو بار', 'HIV-1, adults (≥16 y) — 200 mg once daily for 14 days, then 200 mg twice daily'), {'minAge': age(16, 'year')}, 'fixed', {'perDose': 200, 'dosesPerDay': 2}, [R(Nv, '2.1')],
          notes=[note('دوره آغازین ۱۴ روزه حتماً رعایت شود (کاهش راش). اگر در این دوره راش آمد افزایش نده؛ بیش از ۲۸ روز ادامه نده. وقفه بیش از ۷ روز: دوره آغازین از نو. همراه سایر ضدرتروویروس‌ها.', 'The 14-day lead-in must be followed (fewer rashes). Do not escalate with rash during lead-in; do not extend beyond 28 days. Interruption >7 days: restart lead-in. With other antiretrovirals.', [R(Nv, '2.4'), R(Nv, '2.1')])]),
      reg('child', 'hiv', T('کودک ۱۵ روزه به بالا — ۱۵۰ mg/m² یک بار ۱۴ روز، سپس ۱۵۰ mg/m² دو بار (حداکثر ۴۰۰ mg/روز)', 'Children ≥15 days — 150 mg/m² once daily for 14 days, then 150 mg/m² twice daily (max 400 mg/day)'), {'minAge': age(15, 'day'), 'maxAge': age(16, 'year')}, 'bsa', {'perM2PerDay': 300, 'dividedDoses': 2}, [R(Nv, '2.2')],
          limits={'maxPerDay': 400, 'refs': [R(Nv, '2.2')]})],
     [CI('ci', 'نارسایی متوسط یا شدید کبد (Child-Pugh B/C)؛ استفاده در پیشگیری پس از مواجهه (PEP).', 'Moderate or severe hepatic impairment (Child-Pugh B/C); use in post-exposure prophylaxis (PEP).', [R(Nv, '4')])],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی کشنده (به‌ویژه ۱۸ هفته اول، زنان و CD4 بالا) و واکنش پوستی کشنده (SJS/TEN) — پایش شدید ۱۸ هفته اول.', 'Boxed warning: fatal hepatotoxicity (especially first 18 weeks, women and higher CD4) and fatal skin reactions (SJS/TEN) — intensive monitoring for the first 18 weeks.', [R(Nv, 'Boxed Warning')])],
     exs=[ex('adult', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65), ex('child', 'tab-200', {'perDose': 100, 'tabletsPerDoseRounded': 0.5}, ageYears=4, weightKg=16, heightCm=100)])

Kl = fda('kaletra', 'FDA Kaletra', 'Kaletra (lopinavir/ritonavir) tablets and oral solution — Prescribing Information', sid('lopinavir'))
drug('lopinavir-ritonavir', 'anti-infectives', 'لوپیناویر/ریتوناویر', 'Lopinavir/ritonavir', T('مهارکننده پروتئاز (تقویت‌شده با ریتوناویر)', 'Ritonavir-boosted protease inhibitor'), [{'name': 'Kaletra', 'market': 'US'}], ['kaletra', 'کالترا', 'aluvia', 'lopinavir', 'لوپیناویر'],
     [form('tab-200', 'tablet', 'oral', '200 mg lopinavir / 50 mg ritonavir tablet', 200, 'mg', [R(Kl, '3')], per='tablet'), liquid('sol-80', 80, 1, '80 mg lopinavir / 20 mg ritonavir per mL oral solution', [R(Kl, '3')], form_='solution')],
     [reg('bid', 'hiv', T('HIV-1 بزرگسال — ۴۰۰/۱۰۰ mg دو بار (یا ۸۰۰/۲۰۰ mg یک بار در موارد مناسب)', 'HIV-1, adults — 400/100 mg twice daily (or 800/200 mg once daily when suitable)'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 2}, [R(Kl, '2.3, Table 2')], doseComponent='lopinavir',
          notes=[note('یک بار در روز نه: با ۳ جهش مقاومت یا بیشتر، کاربامازپین/فنوباربیتال/فنی‌توئین، یا بارداری. بارداری: ۴۰۰/۱۰۰ دو بار. قرص کامل بلعیده؛ محلول با غذا. کودک: طبق جداول وزن/BSA.', 'Not once daily: with ≥3 resistance substitutions, carbamazepine/phenobarbital/phenytoin, or pregnancy. Pregnancy: 400/100 twice daily. Swallow tablets whole; solution with food. Children: per weight/BSA tables.', [R(Kl, '2.3'), R(Kl, '2.5'), R(Kl, '2.1'), R(Kl, '2.4')])])],
     [CI('ci', 'حساسیت قبلی جدی (TEN، SJS، آنژیوادم) به اجزا؛ داروهای وابسته به CYP3A با دامنه باریک و القاگرهای قوی CYP3A (طبق جدول برچسب).', 'Prior serious hypersensitivity (TEN, SJS, angioedema) to any ingredient; CYP3A-dependent narrow-index drugs and potent CYP3A inducers (per label table).', [R(Kl, '4')])],
     warn=[W('تداخلات دارویی جدی؛ سمیت در نوزاد نارس (محلول: الکل و پروپیلن‌گلیکول)؛ پانکراتیت؛ سمیت کبد؛ طولانی شدن QT و PR؛ دیابت؛ افزایش چربی خون.', 'Serious drug interactions; toxicity in preterm neonates (solution: ethanol and propylene glycol); pancreatitis; hepatotoxicity; QT and PR prolongation; diabetes; lipid elevations.', [R(Kl, '5')])],
     exs=[ex('bid', 'tab-200', {'perDose': 400, 'tabletsPerDoseRounded': 2}, ageYears=35, weightKg=65), ex('bid', 'sol-80', {'perDose': 400, 'mlPerDose': 5}, ageYears=35, weightKg=65)])

Tv = fda('toviaz', 'FDA Toviaz', 'Toviaz (fesoterodine fumarate) extended-release tablets — Prescribing Information', sid('fesoterodine'))
drug('fesoterodine', 'genitourinary-sex-hormones', 'فزوترودین', 'Fesoterodine', T('آنتی‌موسکارینی', 'Antimuscarinic'), [{'name': 'Toviaz', 'market': 'US'}], ['toviaz', 'توویاز', 'فزوترودین'],
     [tab('er-4', 4, '4 mg ER tablet', [R(Tv, '3')]), tab('er-8', 8, '8 mg ER tablet', [R(Tv, '3')])],
     [reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال بزرگسال — ۴ mg یک بار؛ تا ۸ mg', 'Overactive bladder, adults — 4 mg once daily; up to 8 mg'), A18, 'fixed', {'perDose': 4, 'perDoseMax': 8, 'dosesPerDay': 1}, [R(Tv, '2.1')]),
      reg('ndo', 'neurogenic-bladder', T('بیش‌فعالی دترسور نوروژنیک کودک ۶ سال به بالا و >۲۵ kg — ۴ mg یک بار؛ بالای ۳۵ kg پس از یک هفته ۸ mg', 'Neurogenic detrusor overactivity, children ≥6 y and >25 kg — 4 mg once daily; >35 kg increase to 8 mg after one week'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 25.01}, 'fixed', {'perDose': 4, 'perDoseMax': 8, 'dosesPerDay': 1}, [R(Tv, '2')])],
     [CI('ci', 'حساسیت به فزوترودین یا تولترودین؛ احتباس ادرار؛ احتباس معده؛ گلوکوم زاویه بسته کنترل‌نشده.', 'Hypersensitivity to fesoterodine or tolterodine; urinary retention; gastric retention; uncontrolled narrow-angle glaucoma.', [R(Tv, '4')])],
     warn=[W('آنژیوادم؛ احتباس ادرار؛ کاهش حرکات گوارش؛ عوارض CNS؛ تشدید میاستنی گراو.', 'Angioedema; urinary retention; decreased GI motility; CNS effects; worsening myasthenia gravis.', [R(Tv, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('بزرگسال ClCr ۱۵ تا ۲۹: حداکثر ۴ mg؛ کمتر طبق جدول ۱.', 'Adults CrCl 15–29: max 4 mg; lower per Table 1.'), 'refs': [R(Tv, '2.3, Table 1')]}],
     exs=[ex('oab', 'er-4', {'perDose': 4, 'tabletsPerDoseRounded': 1, 'upperPerDose': 8}, ageYears=60, weightKg=70), ex('ndo', 'er-4', {'perDose': 4, 'tabletsPerDoseRounded': 1, 'upperPerDose': 8}, ageYears=10, weightKg=40)])

Az = fda('azopt', 'FDA Azopt', 'Azopt (brinzolamide ophthalmic suspension) 1% — Prescribing Information', sid('brinzolamide'))
drug('brinzolamide', 'sensory-organs', 'برینزولامید', 'Brinzolamide', T('مهارکننده کربنیک انیدراز (چشمی)', 'Carbonic anhydrase inhibitor (ophthalmic)'), [{'name': 'Azopt', 'market': 'US'}], ['azopt', 'آزوپت', 'برینزولامید'],
     [form('drops', 'eye-drops', 'ophthalmic', '1% eye suspension', 1, 'drop', [R(Az, '3')], per='drop')],
     [reg('glc', 'glaucoma', T('گلوکوم زاویه باز یا فشار بالای چشم — یک قطره در چشم مبتلا ۳ بار در روز', 'Open-angle glaucoma or ocular hypertension — 1 drop in the affected eye(s) three times daily'), A18, 'fixed', {'perDose': 1, 'dosesPerDay': 3}, [R(Az, '2')], unit='drop',
          notes=[note('پیش از مصرف تکان داده شود؛ با سایر قطره‌ها دست‌کم ۱۰ دقیقه فاصله.', 'Shake well; separate other eye drops by at least 10 min.', [R(Az, '2')])])],
     [CI('hyper', 'حساسیت به اجزای فرآورده.', 'Hypersensitivity to any component.', [R(Az, '4')])],
     warn=[W('سولفونامید است (واکنش‌های شدید سولفا)؛ آسیب اندوتلیوم قرنیه؛ نارسایی شدید کلیه توصیه نمی‌شود؛ گلوکوم زاویه بسته حاد؛ لنز تماسی.', 'Sulfonamide (severe sulfa reactions); corneal endothelium; not recommended in severe renal impairment; acute angle-closure glaucoma; contact lenses.', [R(Az, '5')])],
     exs=[ex('glc', 'drops', {'perDose': 1}, ageYears=60, weightKg=70)])
print('s13a2 ok')
