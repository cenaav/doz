"""Stage 12e (part 1) — GI: dexlansoprazole, lubiprostone, plecanatide, alosetron, eluxadoline, vedolizumab; antiemetics aprepitant, fosaprepitant, palonosetron, dronabinol."""
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
cap = lambda id, mg, src, label=None, sec='3', unit='mg': form(id, 'capsule', 'oral', label or f'{mg} {unit} capsule', mg, unit, [R(src, sec)], per='capsule')
NK1_CI = lambda src: CI('ci', 'حساسیت به اجزای فرآورده؛ پیموزاید همزمان (QT).', 'Hypersensitivity to any component; concomitant pimozide (QT prolongation).', [R(src, '4')])
NK1_W = lambda src: W('تداخل مهم CYP3A4؛ کاهش INR با وارفارین (پایش ۷ تا ۱۰ روز)؛ کاهش اثر ضدبارداری هورمونی تا ۲۸ روز.', 'Clinically significant CYP3A4 interactions; decreased INR with warfarin (monitor days 7–10); reduced hormonal contraceptive efficacy for 28 days.', [R(src, '5')])

add_disease('ponv', 'تهوع و استفراغ پس از جراحی (PONV)', 'Postoperative nausea and vomiting (PONV)', ['PONV', 'تهوع بعد از عمل', 'استفراغ پس از بیهوشی'], ['R11.2'], 'procedures')
add_disease('opioid-induced-constipation', 'یبوست ناشی از اپیوئید', 'Opioid-induced constipation', ['OIC', 'یبوست مخدر', 'یبوست ناشی از مخدر'], ['K59.03'], 'gastroenterology')
add_disease('aids-anorexia', 'بی‌اشتهایی و کاهش وزن در ایدز', 'AIDS-associated anorexia and weight loss', ['AIDS wasting', 'لاغری ایدز', 'بی اشتهایی ایدز'], ['R63.0'], 'infectious')

Dx = fda('dexilant', 'FDA Dexilant', 'Dexilant (dexlansoprazole) delayed-release capsules — Prescribing Information', sid('dexlansoprazole'))
drug('dexlansoprazole', 'alimentary-metabolism', 'دکس‌لانزوپرازول', 'Dexlansoprazole', T('مهارکننده پمپ پروتون', 'Proton-pump inhibitor'), [{'name': 'Dexilant', 'market': 'US'}], ['dexilant', 'دکسیلانت', 'دکسلانزوپرازول'],
     [cap('dr-60', 60, Dx, '60 mg delayed-release capsule'), cap('dr-30', 30, Dx, '30 mg delayed-release capsule')],
     [reg('ee', 'erosive-esophagitis', T('درمان ازوفاژیت اروزیو (۱۲ سال به بالا) — ۶۰ mg یک بار، تا ۸ هفته', 'Healing of erosive oesophagitis (≥12 y) — 60 mg once daily up to 8 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 60, 'dosesPerDay': 1}, [R(Dx, '2.1, Table 1')], dur={'min': 1, 'max': 56}, allowed=['dr-60'],
          notes=[note('بدون توجه به غذا؛ کامل بلعیده شود. نارسایی متوسط کبد: ۳۰ mg تا ۸ هفته؛ شدید توصیه نمی‌شود.', 'Without regard to food; swallow whole. Moderate hepatic impairment: 30 mg up to 8 weeks; severe not recommended.', [R(Dx, '2'), R(Dx, '2.2')])]),
      reg('maint', 'erosive-esophagitis', T('نگهداری ازوفاژیت بهبودیافته و رفع سوزش سر دل — ۳۰ mg یک بار', 'Maintenance of healed EE and heartburn relief — 30 mg once daily'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Dx, '2.1, Table 1')], allowed=['dr-30']),
      reg('nerd', 'gerd', T('GERD غیراروزیو علامت‌دار — ۳۰ mg یک بار، ۴ هفته', 'Symptomatic non-erosive GERD — 30 mg once daily for 4 weeks'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 30, 'dosesPerDay': 1}, [R(Dx, '2.1, Table 1')], dur={'min': 28, 'max': 28}, allowed=['dr-30'])],
     [CI('ci', 'حساسیت به اجزای فرآورده (آنافیلاکسی، نفریت بینابینی)؛ فرآورده‌های حاوی ریلپیویرین.', 'Hypersensitivity to any component (anaphylaxis, interstitial nephritis); rilpivirine-containing products.', [R(Dx, '4')])],
     warn=[W('پوشاندن بدخیمی معده؛ نفریت توبولواینترستیشیال؛ اسهال C. difficile؛ شکستگی استخوان؛ لوپوس؛ کمبود B12 و منیزیم با مصرف طولانی.', 'Masking gastric malignancy; tubulointerstitial nephritis; C. difficile diarrhoea; bone fracture; lupus; vitamin B12 and magnesium deficiency with long use.', [R(Dx, '5')])],
     exs=[ex('ee', 'dr-60', {'perDose': 60, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('maint', 'dr-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('nerd', 'dr-30', {'perDose': 30, 'tabletsPerDoseRounded': 1}, ageYears=14, weightKg=50)])

Am = fda('amitiza', 'FDA Amitiza', 'Amitiza (lubiprostone) capsules — Prescribing Information', sid('lubiprostone'))
drug('lubiprostone', 'alimentary-metabolism', 'لوبی‌پروستون', 'Lubiprostone', T('فعال‌کننده کانال کلر (ملین)', 'Chloride-channel activator (laxative)'), [{'name': 'Amitiza', 'market': 'US'}], ['amitiza', 'آمیتیزا', 'لوبیپروستون'],
     [cap('cap-24', 24, Am, '24 mcg capsule', unit='mcg'), cap('cap-8', 8, Am, '8 mcg capsule', unit='mcg')],
     [reg('cic', 'chronic-idiopathic-constipation', T('یبوست مزمن ایدیوپاتیک بزرگسال — ۲۴ mcg دو بار با غذا', 'Chronic idiopathic constipation, adults — 24 mcg twice daily with food'), A18, 'fixed', {'perDose': 24, 'dosesPerDay': 2}, [R(Am, '2.1, Table 1')], unit='mcg', allowed=['cap-24'],
          notes=[note('نارسایی متوسط کبد: ۱۶ mcg دو بار؛ شدید: ۸ mcg دو بار. کامل بلعیده شود.', 'Moderate hepatic impairment: 16 mcg twice daily; severe: 8 mcg twice daily. Swallow whole.', [R(Am, '2.1, Table 1'), R(Am, '2.2')])]),
      reg('oic', 'opioid-induced-constipation', T('یبوست ناشی از اپیوئید در درد مزمن غیرسرطانی — ۲۴ mcg دو بار', 'Opioid-induced constipation in chronic non-cancer pain — 24 mcg twice daily'), A18, 'fixed', {'perDose': 24, 'dosesPerDay': 2}, [R(Am, '2.1, Table 1')], unit='mcg', allowed=['cap-24']),
      reg('ibsc', 'ibs', T('IBS با یبوست در زنان ۱۸ سال به بالا — ۸ mcg دو بار', 'IBS with constipation in women ≥18 y — 8 mcg twice daily'), A18, 'fixed', {'perDose': 8, 'dosesPerDay': 2}, [R(Am, '2.1, Table 1')], unit='mcg', allowed=['cap-8'])],
     [CI('ci', 'انسداد مکانیکی گوارش (شناخته یا مشکوک).', 'Known or suspected mechanical GI obstruction.', [R(Am, '4')])],
     warn=[W('تهوع؛ اسهال؛ سنکوپ و افت فشار؛ تنگی نفس.', 'Nausea; diarrhoea; syncope and hypotension; dyspnoea.', [R(Am, '5')])],
     exs=[ex('cic', 'cap-24', {'perDose': 24, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=65), ex('oic', 'cap-24', {'perDose': 24, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=70), ex('ibsc', 'cap-8', {'perDose': 8, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=60)])

Tr = fda('trulance', 'FDA Trulance', 'Trulance (plecanatide) tablets 3 mg — Prescribing Information', sid('plecanatide'))
drug('plecanatide', 'alimentary-metabolism', 'پلکاناتاید', 'Plecanatide', T('آگونیست گوانیلات سیکلاز-C', 'Guanylate cyclase-C agonist'), [{'name': 'Trulance', 'market': 'US'}], ['trulance', 'ترولانس', 'پلکاناتید'],
     [tab('tab-3', 3, '3 mg tablet', [R(Tr, '3')])],
     [reg('cic', 'chronic-idiopathic-constipation', T('یبوست مزمن ایدیوپاتیک بزرگسال — ۳ mg یک بار', 'Chronic idiopathic constipation, adults — 3 mg once daily'), A18, 'fixed', {'perDose': 3, 'dosesPerDay': 1}, [R(Tr, '2.1')]),
      reg('ibsc', 'ibs', T('IBS با یبوست بزرگسال — ۳ mg یک بار', 'IBS with constipation, adults — 3 mg once daily'), A18, 'fixed', {'perDose': 3, 'dosesPerDay': 1}, [R(Tr, '2.1')])],
     [CI('ci', 'کودک زیر ۶ سال (کم‌آبی شدید)؛ انسداد مکانیکی گوارش.', 'Children under 6 years (serious dehydration); mechanical GI obstruction.', [R(Tr, '4')])],
     warn=[W('هشدار جعبه‌ای: کم‌آبی شدید در کودکان — زیر ۶ سال منع، ۶ تا ۱۸ سال پرهیز. اسهال شدید.', 'Boxed warning: serious dehydration in children — contraindicated under 6 y, avoid 6–<18 y. Severe diarrhoea.', [R(Tr, 'Boxed Warning'), R(Tr, '5')])],
     exs=[ex('cic', 'tab-3', {'perDose': 3, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=65), ex('ibsc', 'tab-3', {'perDose': 3, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65)])

Al = fda('alosetron', 'FDA Alosetron', 'Alosetron tablets 0.5/1 mg — Prescribing Information', sid('alosetron'))
drug('alosetron', 'alimentary-metabolism', 'آلوسترون', 'Alosetron', T('آنتاگونیست 5-HT3', '5-HT3 antagonist'), [{'name': 'Lotronex', 'market': 'US'}], ['lotronex', 'لوترونکس', 'آلوسترون'],
     [tab('tab-0-5', 0.5, '0.5 mg tablet', [R(Al, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Al, '3')])],
     [reg('ibsd', 'ibs', T('IBS شدید با اسهال در زنان مقاوم به درمان معمول — شروع ۰٫۵ mg دو بار؛ پس از ۴ هفته تا ۱ mg دو بار', 'Severe diarrhoea-predominant IBS in women unresponsive to conventional therapy — start 0.5 mg twice daily; after 4 weeks up to 1 mg twice daily'), A18, 'fixed', {'perDose': 0.5, 'perDoseMax': 1, 'dosesPerDay': 2}, [R(Al, '2.1')],
          notes=[note('در یبوست فوراً قطع؛ پس از رفع با ۰٫۵ mg یک بار شروع مجدد؛ اگر تکرار شد قطع دائم. اگر پس از ۴ هفته با ۱ mg دو بار کنترل نشد قطع.', 'Stop at once if constipated; after resolution restart at 0.5 mg once daily; stop permanently if it recurs. Stop if not controlled after 4 weeks at 1 mg twice daily.', [R(Al, '2.1')])])],
     [CI('ci', 'یبوست فعلی؛ سابقه یبوست شدید یا عوارض آن، انسداد، تنگی، مگاکولون توکسیک، سوراخ‌شدگی یا چسبندگی روده؛ کولیت ایسکمیک، اختلال گردش روده، ترومبوفلبیت یا حالت انعقادپذیری؛ کرون یا کولیت اولسراتیو؛ دیورتیکولیت؛ نارسایی شدید کبد؛ فلووکسامین.',
         'Current constipation; history of severe constipation or its sequelae, obstruction, stricture, toxic megacolon, perforation or adhesions; ischaemic colitis, impaired intestinal circulation, thrombophlebitis or hypercoagulable state; Crohn disease or ulcerative colitis; diverticulitis; severe hepatic impairment; fluvoxamine.', [R(Al, '4')])],
     warn=[W('هشدار جعبه‌ای: عوارض جدی گوارشی (کولیت ایسکمیک، عوارض یبوست) گاه منجر به جراحی یا مرگ — فقط برای زنان با IBS-D شدید مقاوم؛ با یبوست یا خون در مدفوع فوراً قطع.', 'Boxed warning: serious GI adverse reactions (ischaemic colitis, complications of constipation) sometimes requiring surgery or causing death — only for women with severe refractory IBS-D; stop immediately with constipation or rectal bleeding.', [R(Al, 'Boxed Warning')])],
     exs=[ex('ibsd', 'tab-0-5', {'perDose': 0.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 1}, ageYears=35, weightKg=60)])

Vb = fda('viberzi', 'FDA Viberzi', 'Viberzi (eluxadoline) tablets — Prescribing Information', sid('eluxadoline'))
drug('eluxadoline', 'alimentary-metabolism', 'الوکسادولین', 'Eluxadoline', T('آگونیست گیرنده اپیوئیدی μ/κ روده (ضداسهال)', 'Gut mu/kappa opioid agonist (antidiarrhoeal)'), [{'name': 'Viberzi', 'market': 'US'}], ['viberzi', 'وایبرزی', 'الوکسادولین'],
     [tab('tab-100', 100, '100 mg tablet', [R(Vb, '3')]), tab('tab-75', 75, '75 mg tablet', [R(Vb, '3')])],
     [reg('ibsd', 'ibs', T('IBS با اسهال بزرگسال — ۱۰۰ mg دو بار با غذا', 'IBS with diarrhoea, adults — 100 mg twice daily with food'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [R(Vb, '2')], allowed=['tab-100'],
          notes=[note('۷۵ mg دو بار: عدم تحمل ۱۰۰ mg، مهارکننده OATP1B1، نارسایی خفیف/متوسط کبد، eGFR زیر ۶۰ یا ESRD بدون دیالیز. در یبوست شدید قطع.', '75 mg twice daily: intolerance of 100 mg, OATP1B1 inhibitors, mild/moderate hepatic impairment, eGFR <60, or ESRD not on dialysis. Stop if severe constipation.', [R(Vb, '2')])])],
     [CI('ci', 'نداشتن کیسه صفرا؛ انسداد مجرای صفراوی یا اختلال اسفنکتر اودی؛ الکلیسم یا بیش از ۳ نوشیدنی الکلی در روز؛ سابقه پانکراتیت یا بیماری ساختاری پانکراس؛ نارسایی شدید کبد؛ سابقه یبوست شدید یا انسداد مکانیکی روده؛ حساسیت.',
         'No gallbladder; biliary duct obstruction or sphincter of Oddi disease; alcoholism or >3 alcoholic drinks a day; history of pancreatitis or structural pancreatic disease; severe hepatic impairment; history of severe constipation or mechanical bowel obstruction; hypersensitivity.', [R(Vb, '4')])],
     warn=[W('پانکراتیت؛ اسپاسم اسفنکتر اودی؛ واکنش حساسیتی؛ یبوست.', 'Pancreatitis; sphincter of Oddi spasm; hypersensitivity; constipation.', [R(Vb, '5')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('eGFR زیر ۶۰ (و ESRD بدون دیالیز): ۷۵ mg دو بار.', 'eGFR <60 (and ESRD not on dialysis): 75 mg twice daily.'), 'refs': [R(Vb, '2')]}],
     exs=[ex('ibsd', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Ev = fda('entyvio', 'FDA Entyvio', 'Entyvio (vedolizumab) for injection and subcutaneous injection — Prescribing Information', sid('vedolizumab'))
drug('vedolizumab', 'antineoplastic-immunomodulating', 'ودولیزوماب', 'Vedolizumab', T('آنتی‌بادی ضد اینتگرین α4β7', 'Anti-α4β7 integrin antibody'), [{'name': 'Entyvio', 'market': 'US'}], ['entyvio', 'انتیویو', 'ودولیزوماب'],
     [form('vial-300', 'powder-for-injection', 'iv', '300 mg vial', 300, 'mg', [R(Ev, '3')], per='vial'), form('pfs-108', 'injection', 'sc', '108 mg/0.68 mL prefilled syringe or pen', 108, 'mg', [R(Ev, '3')], vol=0.68)],
     [reg('uc', 'ulcerative-colitis', T('کولیت اولسراتیو متوسط تا شدید بزرگسال — ۳۰۰ mg وریدی هفته ۰، ۲ و ۶، سپس هر ۸ هفته', 'Moderate–severe ulcerative colitis, adults — 300 mg IV at weeks 0, 2 and 6, then every 8 weeks'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Ev, '2')], dur=ONE, allowed=['vial-300'],
          notes=[note('انفوزیون حدود ۳۰ دقیقه. پس از ۲ دوز وریدی می‌توان به زیرجلدی ۱۰۸ mg هر ۲ هفته تغییر داد. اگر تا هفته ۱۴ سودی نبود قطع.', 'Infuse over about 30 min. After two IV doses, may switch to 108 mg SC every 2 weeks. Stop if no benefit by week 14.', [R(Ev, '2')])]),
      reg('cd', 'crohns', T('کرون متوسط تا شدید بزرگسال — ۳۰۰ mg وریدی هفته ۰، ۲ و ۶، سپس هر ۸ هفته', 'Moderate–severe Crohn disease, adults — 300 mg IV at weeks 0, 2 and 6, then every 8 weeks'), A18, 'fixed', {'perDose': 300, 'dosesPerDay': 1}, [R(Ev, '2')], dur=ONE, allowed=['vial-300']),
      reg('sc', 'ulcerative-colitis', T('نگهدارنده زیرجلدی (کولیت یا کرون) — ۱۰۸ mg هر ۲ هفته', 'Subcutaneous maintenance (UC or Crohn) — 108 mg every 2 weeks'), A18, 'fixed', {'perDose': 108, 'dosesPerDay': 1}, [R(Ev, '2')], dur=ONE, allowed=['pfs-108'])],
     [CI('hyper', 'حساسیت جدی قبلی به ودولیزوماب.', 'Prior serious hypersensitivity to vedolizumab.', [R(Ev, '4')])],
     warn=[W('واکنش انفوزیون و حساسیت؛ عفونت؛ لکوآنسفالوپاتی چندکانونی پیشرونده (PML)؛ آسیب کبدی؛ واکسن‌ها پیش از شروع کامل شود.', 'Infusion and hypersensitivity reactions; infections; progressive multifocal leukoencephalopathy (PML); liver injury; complete immunisations before starting.', [R(Ev, '5')])],
     exs=[ex('uc', 'vial-300', {'perDose': 300}, ageYears=35, weightKg=70), ex('cd', 'vial-300', {'perDose': 300}, ageYears=35, weightKg=70), ex('sc', 'pfs-108', {'perDose': 108, 'mlPerDose': 0.68}, ageYears=35, weightKg=70)])

Em = fda('emend', 'FDA Emend', 'Emend (aprepitant) capsules and oral suspension — Prescribing Information', sid('aprepitant'))
drug('aprepitant', 'alimentary-metabolism', 'آپری‌پیتانت', 'Aprepitant', T('آنتاگونیست گیرنده NK1', 'NK1 receptor antagonist'), [{'name': 'Emend', 'market': 'US'}], ['emend', 'امند', 'آپرپیتانت', 'آپریپیتانت'],
     [cap('cap-125', 125, Em), cap('cap-80', 80, Em)],
     [reg('d1', 'cinv', T('پیشگیری تهوع شیمی‌درمانی (بزرگسال و ۱۲ سال به بالا) — روز ۱: ۱۲۵ mg، ۱ ساعت پیش از شیمی‌درمانی', 'CINV prevention (adults and ≥12 y) — day 1: 125 mg, 1 h before chemotherapy'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 125, 'dosesPerDay': 1}, [R(Em, '2.1')], dur=ONE, allowed=['cap-125'],
          notes=[note('همراه کورتیکواستروئید و آنتاگونیست 5-HT3. ۶ ماه تا <۱۲ سال یا ناتوان از بلع: سوسپانسیون طبق جدول ۳.', 'With a corticosteroid and a 5-HT3 antagonist. 6 months to <12 y or unable to swallow: suspension per Table 3.', [R(Em, '2.1')])]),
      reg('d23', 'cinv', T('روز ۲ و ۳: ۸۰ mg یک بار (صبح اگر شیمی‌درمانی نیست)', 'Days 2 and 3: 80 mg once daily (in the morning if no chemotherapy)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 80, 'dosesPerDay': 1}, [R(Em, '2.1')], dur={'min': 2, 'max': 2}, allowed=['cap-80'])],
     [NK1_CI(Em)], warn=[NK1_W(Em)],
     exs=[ex('d1', 'cap-125', {'perDose': 125, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70), ex('d23', 'cap-80', {'perDose': 80, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=70)])

Fa = fda('fosaprepitant', 'FDA Fosaprepitant', 'Fosaprepitant for injection 150 mg — Prescribing Information', sid('fosaprepitant'))
drug('fosaprepitant', 'alimentary-metabolism', 'فوس‌آپری‌پیتانت', 'Fosaprepitant', T('آنتاگونیست گیرنده NK1 (وریدی)', 'NK1 receptor antagonist (IV)'), [{'name': 'Emend IV', 'market': 'US'}], ['emend iv', 'امند وریدی', 'فوزاپرپیتانت'],
     [form('vial-150', 'powder-for-injection', 'iv', '150 mg vial', 150, 'mg', [R(Fa, '3')], per='vial')],
     [reg('adult', 'cinv', T('پیشگیری تهوع شیمی‌درمانی بزرگسال — ۱۵۰ mg وریدی روز ۱، انفوزیون ۲۰ تا ۳۰ دقیقه', 'CINV prevention, adults — 150 mg IV on day 1, infused over 20–30 min'), A18, 'fixed', {'perDose': 150, 'dosesPerDay': 1}, [R(Fa, '2.1')], dur=ONE,
          notes=[note('انفوزیون حدود ۳۰ دقیقه پیش از شیمی‌درمانی تمام شود؛ همراه دگزامتازون و آنتاگونیست 5-HT3. کودک ۶ ماه تا ۱۷ سال (≥۶ kg) طبق جداول ۳ و ۴.', 'Finish about 30 min before chemotherapy; with dexamethasone and a 5-HT3 antagonist. Children 6 months–17 y (≥6 kg) per Tables 3 and 4.', [R(Fa, '2.1'), R(Fa, '2.2')])])],
     [NK1_CI(Fa)], warn=[NK1_W(Fa), W('واکنش حساسیتی؛ واکنش محل انفوزیون.', 'Hypersensitivity reactions; infusion-site reactions.', [R(Fa, '5')])],
     exs=[ex('adult', 'vial-150', {'perDose': 150}, ageYears=50, weightKg=70)])

Pl = fda('palonosetron', 'FDA Palonosetron', 'Palonosetron hydrochloride injection 0.25 mg/5 mL — Prescribing Information', sid('palonosetron'))
drug('palonosetron', 'alimentary-metabolism', 'پالونوسترون', 'Palonosetron', T('آنتاگونیست 5-HT3 (طولانی‌اثر)', 'Long-acting 5-HT3 antagonist'), [{'name': 'Aloxi', 'market': 'US'}], ['aloxi', 'آلوکسی', 'پالونوسترون'],
     [form('vial-0-05', 'injection', 'iv', '0.05 mg/mL (0.25 mg/5 mL) vial', 0.05, 'mg', [R(Pl, '3')], vol=1)],
     [reg('cinv', 'cinv', T('پیشگیری تهوع شیمی‌درمانی بزرگسال — ۰٫۲۵ mg وریدی طی ۳۰ ثانیه، ۳۰ دقیقه پیش از شیمی‌درمانی', 'CINV prevention, adults — 0.25 mg IV over 30 s, 30 min before chemotherapy'), A18, 'fixed', {'perDose': 0.25, 'dosesPerDay': 1}, [R(Pl, '2.1, Table 1')], dur=ONE),
      once('cinv-child', 'cinv', 'کودک ۱ ماه تا <۱۷ سال — ۲۰ mcg/kg (حداکثر ۱٫۵ mg) طی ۱۵ دقیقه', 'Children 1 month–<17 y — 20 mcg/kg (max 1.5 mg) over 15 min', {'minAge': age(1, 'month'), 'maxAge': age(17, 'year')}, 0.02, None, [R(Pl, '2.1, Table 1')], limits={'maxPerDose': 1.5, 'refs': [R(Pl, '2.1, Table 1')]}),
      reg('ponv', 'ponv', T('پیشگیری تهوع پس از جراحی بزرگسال — ۰٫۰۷۵ mg وریدی طی ۱۰ ثانیه درست پیش از القای بیهوشی', 'PONV prevention, adults — 0.075 mg IV over 10 s immediately before induction'), A18, 'fixed', {'perDose': 0.075, 'dosesPerDay': 1}, [R(Pl, '2.1')], dur=ONE)],
     [CI('hyper', 'حساسیت به پالونوسترون.', 'Hypersensitivity to palonosetron.', [R(Pl, '4')])],
     warn=[W('واکنش حساسیتی (حتی با حساسیت به سایر 5-HT3)؛ سندرم سروتونین.', 'Hypersensitivity (including in those allergic to other 5-HT3 antagonists); serotonin syndrome.', [R(Pl, '5')])],
     exs=[ex('cinv', 'vial-0-05', {'perDose': 0.25, 'mlPerDose': 5}, ageYears=50, weightKg=70), ex('cinv-child', 'vial-0-05', {'perDose': 0.4, 'mlPerDose': 8}, ageYears=6, weightKg=20), ex('ponv', 'vial-0-05', {'perDose': 0.075, 'mlPerDose': 1.5}, ageYears=40, weightKg=70)])

Mr = fda('marinol', 'FDA Marinol', 'Marinol (dronabinol) capsules — Prescribing Information', sid('dronabinol'))
drug('dronabinol', 'alimentary-metabolism', 'درونابینول', 'Dronabinol', T('کانابینوئید (THC مصنوعی)', 'Cannabinoid (synthetic THC)'), [{'name': 'Marinol', 'market': 'US'}], ['marinol', 'مارینول', 'درونابینول', 'THC'],
     [cap('cap-2-5', 2.5, Mr, '2.5 mg capsule'), cap('cap-5', 5, Mr), cap('cap-10', 10, Mr)],
     [reg('aids', 'aids-anorexia', T('بی‌اشتهایی و کاهش وزن در ایدز بزرگسال — ۲٫۵ mg دو بار، ۱ ساعت پیش از ناهار و شام', 'AIDS anorexia with weight loss, adults — 2.5 mg twice daily, 1 h before lunch and dinner'), A18, 'fixed', {'perDose': 2.5, 'perDoseMax': 10, 'dosesPerDay': 2}, [R(Mr, '2.1')],
          notes=[note('سالمند یا عدم تحمل: ۲٫۵ mg یک بار پیش از شام یا هنگام خواب. حداکثر ۱۰ mg دو بار.', 'Elderly or intolerant: 2.5 mg once before dinner or at bedtime. Max 10 mg twice daily.', [R(Mr, '2.1')])]),
      NC('cinv', 'cinv', 'تهوع شیمی‌درمانی مقاوم به ضدتهوع‌های معمول — شروع ۵ mg/m² ۱ تا ۳ ساعت پیش از شیمی‌درمانی، سپس هر ۲ تا ۴ ساعت (۴ تا ۶ دوز/روز)', 'CINV refractory to conventional antiemetics — start 5 mg/m² 1–3 h before chemotherapy, then every 2–4 h (4–6 doses/day)', A18,
         'دوز بر اساس سطح بدن و به نزدیک‌ترین کپسول ۲٫۵ mg گرد می‌شود؛ سالمند ۲٫۵ mg/m² یک بار. اولین دوز ناشتا.', 'BSA-based dose rounded to the nearest 2.5 mg capsule; elderly 2.5 mg/m² once. First dose on an empty stomach.', [R(Mr, '2.2')])],
     [CI('hyper', 'سابقه حساسیت به درونابینول یا روغن کنجد.', 'History of hypersensitivity to dronabinol or sesame oil.', [R(Mr, '4')])],
     warn=[W('عوارض عصبی-روانی (گیجی، سرخوشی، سایکوز)؛ ناپایداری همودینامیک؛ تشنج؛ سوءمصرف چندگانه؛ تهوع و استفراغ متناقض.', 'Neuropsychiatric reactions (confusion, euphoria, psychosis); haemodynamic instability; seizures; multiple substance abuse; paradoxical nausea and vomiting.', [R(Mr, '5')])],
     exs=[ex('aids', 'cap-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 10}, ageYears=40, weightKg=60)])
print('s12e1 ok')
