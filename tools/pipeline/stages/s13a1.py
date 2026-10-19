"""Stage 13a (part 1) — urokinase, mexiletine, niacin ER, colesevelam, saxagliptin, alogliptin, lanreotide, mannitol, mercaptopurine, methylnaltrexone, naloxegol, levalbuterol, ciclesonide, mixed amphetamine salts XR."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's13_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
cap = lambda id, mg, src, label=None, sec='3': tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
inh = lambda id, mcg, label, src: form(id, 'inhaler', 'inhaled', label, mcg, 'mcg', [R(src, '3')], per='actuation')
DPP4_W = lambda src: W('پانکراتیت؛ نارسایی قلب؛ هیپوگلیسمی با انسولین یا سولفونیل‌اوره؛ واکنش حساسیتی؛ درد مفصلی شدید؛ پمفیگوئید بولوز.', 'Pancreatitis; heart failure; hypoglycaemia with insulin or sulfonylureas; hypersensitivity; severe arthralgia; bullous pemphigoid.', [R(src, '5')])
PAMORA_W = lambda src: W('سوراخ‌شدگی گوارش؛ اسهال یا درد شکمی شدید؛ علائم ترک اپیوئید.', 'GI perforation; severe diarrhoea or abdominal pain; opioid withdrawal.', [R(src, '5')])

add_disease('raised-intracranial-pressure', 'افزایش فشار داخل جمجمه و ادم مغزی', 'Raised intracranial pressure and cerebral oedema', ['ICP', 'ادم مغزی', 'فشار داخل جمجمه'], ['G93.6'], 'neurology')
add_disease('acute-lymphoblastic-leukemia', 'لوسمی لنفوبلاستیک حاد (ALL)', 'Acute lymphoblastic leukaemia (ALL)', ['ALL', 'لوسمی حاد لنفوبلاستیک', 'سرطان خون کودکان'], ['C91.0'], 'oncology')

Uk = fda('kinlytic', 'FDA Kinlytic', 'Kinlytic (urokinase) for injection 250,000 IU — Prescribing Information', sid('urokinase')); d = R(Uk, 'Dosage and Administration')
drug('urokinase', 'blood', 'اوروکیناز', 'Urokinase', T('ترومبولیتیک', 'Thrombolytic'), [{'name': 'Kinlytic', 'market': 'US'}], ['kinlytic', 'abbokinase', 'اوروکیناز'],
     [form('vial-250k', 'powder-for-injection', 'iv', '250,000 IU vial', 250000, 'unit', [R(Uk, 'How Supplied')], per='vial')],
     [once('pe', 'pulmonary-embolism', 'آمبولی ریه حاد — بارگذاری ۴۴۰۰ واحد/kg طی ۱۰ دقیقه، سپس ۴۴۰۰ واحد/kg/ساعت ۱۲ ساعت', 'Acute pulmonary embolism — loading 4,400 IU/kg over 10 min, then 4,400 IU/kg/h for 12 h', A18, 4400, None, [d], unit='unit',
           notes=[note('عدد ماشین‌حساب دوز بارگذاری است؛ انفوزیون نگهدارنده همان مقدار در هر ساعت به مدت ۱۲ ساعت. هرچه زودتر پس از شروع آمبولی. پس از پایان، هپارین بدون بولوس.', 'The calculator gives the loading dose; the maintenance infusion is the same amount per hour for 12 h. Start as soon as possible after PE onset. Afterwards, heparin without a bolus.', [d])])],
     [CI('ci', 'خونریزی داخلی فعال؛ سکته مغزی، جراحی داخل جمجمه یا نخاع در ۲ ماه اخیر؛ ترومای اخیر از جمله CPR؛ تومور، AVM یا آنوریسم داخل جمجمه؛ اختلال خونریزی‌دهنده؛ فشار خون شدید کنترل‌نشده؛ حساسیت.',
         'Active internal bleeding; stroke, intracranial or intraspinal surgery within 2 months; recent trauma including CPR; intracranial neoplasm, AVM or aneurysm; bleeding diathesis; severe uncontrolled hypertension; hypersensitivity.', [R(Uk, 'Contraindications')])],
     warn=[W('خونریزی جدی و کشنده (داخل جمجمه، رتروپریتوئن)؛ با سایر ضدانعقادها خطر بیشتر.', 'Serious and fatal bleeding (intracranial, retroperitoneal); higher with other anticoagulants.', [R(Uk, 'Warnings')])],
     exs=[ex('pe', 'vial-250k', {'perDose': 308000}, ageYears=55, weightKg=70)])

Mx = fda('mexiletine', 'FDA Mexiletine', 'Mexiletine HCl capsules 150/200/250 mg — Prescribing Information', sid('mexiletine')); d = R(Mx, 'Dosage and Administration')
drug('mexiletine', 'cardiovascular', 'مگزیلتین', 'Mexiletine', T('ضدآریتمی کلاس IB', 'Class IB antiarrhythmic'), [{'name': 'Mexiletine', 'market': 'US'}], ['mexitil', 'مکزیلتین', 'مگزیلتین'],
     [cap('cap-200', 200, Mx, sec='How Supplied'), cap('cap-150', 150, Mx, sec='How Supplied'), cap('cap-250', 250, Mx, sec='How Supplied')],
     [reg('va', 'ventricular-arrhythmia', T('آریتمی بطنی تهدیدکننده حیات — شروع ۲۰۰ mg هر ۸ ساعت با غذا', 'Life-threatening ventricular arrhythmia — start 200 mg every 8 h with food'), A18, 'fixed', {'perDose': 200, 'perDoseMax': 300, 'dosesPerDay': 3}, [d],
          notes=[note('بیشتر بیماران با ۲۰۰ تا ۳۰۰ mg هر ۸ ساعت کنترل می‌شوند؛ تغییر ۵۰ یا ۱۰۰ mg با فاصله ۲ تا ۳ روز. کنترل سریع: بارگذاری ۴۰۰ mg و ۸ ساعت بعد ۲۰۰ mg. ECG و هولتر.', 'Most are controlled by 200–300 mg every 8 h; adjust by 50 or 100 mg every 2–3 days. Rapid control: 400 mg loading then 200 mg 8 h later. ECG and Holter monitoring.', [d])])],
     [CI('ci', 'شوک کاردیوژنیک؛ بلوک AV درجه ۲ یا ۳ بدون پیس‌میکر.', 'Cardiogenic shock; second- or third-degree AV block without a pacemaker.', [R(Mx, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: افزایش مرگ با ضدآریتمی‌های کلاس I پس از MI (مطالعه CAST) — فقط برای آریتمی بطنی تهدیدکننده حیات.', 'Boxed warning: increased mortality with class I antiarrhythmics after MI (CAST) — reserve for life-threatening ventricular arrhythmia.', [R(Mx, 'Boxed Warning')])],
     exs=[ex('va', 'cap-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=75)])

Nc = fda('niacin-er', 'FDA Niacin ER', 'Niacin extended-release tablets 500/1000 mg (Amneal) — Prescribing Information', sid('niacin'))
drug('niacin', 'cardiovascular', 'نیاسین (آهسته‌رهش)', 'Niacin (extended-release)', T('کاهنده چربی خون (اسید نیکوتینیک)', 'Lipid-modifying agent (nicotinic acid)'), [{'name': 'Niaspan', 'market': 'US'}], ['niaspan', 'نیاسپان', 'nicotinic acid', 'اسید نیکوتینیک', 'نیاسین'],
     [tab('er-500', 500, '500 mg ER tablet (do not break)', [R(Nc, '3')]), tab('er-1000', 1000, '1000 mg ER tablet (do not break)', [R(Nc, '3')])],
     [reg('lip', 'hyperlipidemia', T('دیس‌لیپیدمی — شروع ۵۰۰ mg هنگام خواب؛ نگهدارنده ۱۰۰۰ تا ۲۰۰۰ mg یک بار', 'Dyslipidaemia — start 500 mg at bedtime; maintenance 1000–2000 mg once daily'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 2000, 'dosesPerDay': 1}, [R(Nc, '2.1'), R(Nc, '2.2')],
          notes=[note('با میان‌وعده کم‌چرب هنگام خواب. در هر ۴ هفته بیش از ۵۰۰ mg افزایش نه. بیش از ۲۰۰۰ mg/روز توصیه نمی‌شود.', 'At bedtime after a low-fat snack. Do not increase by more than 500 mg in any 4 weeks. Above 2000 mg/day not recommended.', [R(Nc, '2.1'), R(Nc, '2.2')])])],
     [CI('ci', 'بیماری فعال کبد یا افزایش بی‌علت ترانس‌آمینازها؛ زخم پپتیک فعال؛ خونریزی شریانی؛ حساسیت.', 'Active liver disease or unexplained transaminase elevation; active peptic ulcer; arterial bleeding; hypersensitivity.', [R(Nc, '4')])],
     warn=[W('بدون کاهش رویداد قلبی؛ میوپاتی (به‌ویژه با استاتین)؛ آسیب کبد؛ افزایش قند و اسید اوریک؛ گرگرفتگی.', 'No reduction in cardiovascular events; myopathy (especially with statins); liver injury; raised glucose and uric acid; flushing.', [R(Nc, '5')])],
     exs=[ex('lip', 'er-500', {'perDose': 500, 'tabletsPerDoseRounded': 1, 'upperPerDose': 2000}, ageYears=55, weightKg=80)])

Wc = fda('welchol', 'FDA Welchol', 'Welchol (colesevelam) tablets and oral suspension — Prescribing Information', sid('colesevelam'))
drug('colesevelam', 'cardiovascular', 'کولسولام', 'Colesevelam', T('جاذب اسید صفراوی', 'Bile acid sequestrant'), [{'name': 'Welchol', 'market': 'US'}], ['welchol', 'ولکول', 'کولسولام'],
     [tab('tab-625', 625, '625 mg tablet', [R(Wc, '3')]), form('pkt-3750', 'sachet', 'oral', '3.75 g packet for oral suspension', 3750, 'mg', [R(Wc, '3')], per='sachet')],
     [reg('lip', 'hyperlipidemia', T('هیپرلیپیدمی اولیه (بزرگسال و ۱۰ تا ۱۷ سال) یا دیابت نوع ۲ — ۳٫۷۵ g/روز (۶ قرص یک بار یا ۳ قرص دو بار) با غذا', 'Primary hyperlipidaemia (adults and 10–17 y) or type 2 diabetes — 3.75 g/day (6 tablets once or 3 twice daily) with a meal'), {'minAge': age(10, 'year')}, 'fixed', {'perDose': 3750, 'dosesPerDay': 1}, [R(Wc, '2.2')],
          notes=[note('یا یک بسته ۳٫۷۵ g روزانه. پیش از شروع تری‌گلیسرید؛ داروهای دیگر طبق برچسب با فاصله.', 'Or one 3.75 g packet daily. Check triglycerides first; separate other drugs per label.', [R(Wc, '2.2'), R(Wc, '2.1')])])],
     [CI('ci', 'تری‌گلیسرید بالای ۵۰۰ mg/dL؛ سابقه پانکراتیت ناشی از تری‌گلیسرید؛ سابقه انسداد روده.', 'Triglycerides >500 mg/dL; history of hypertriglyceridaemia-induced pancreatitis; history of bowel obstruction.', [R(Wc, '4')])],
     warn=[W('افزایش تری‌گلیسرید و پانکراتیت؛ انسداد گوارش؛ کمبود ویتامین‌های محلول در چربی؛ تداخل جذب داروها؛ فنیل‌کتونوری (سوسپانسیون).', 'Raised triglycerides and pancreatitis; GI obstruction; fat-soluble vitamin deficiency; drug absorption interactions; PKU (suspension).', [R(Wc, '5')])],
     exs=[ex('lip', 'tab-625', {'perDose': 3750, 'tabletsPerDoseRounded': 6}, ageYears=55, weightKg=80), ex('lip', 'pkt-3750', {'perDose': 3750, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=80)])

Sx = fda('saxagliptin', 'FDA Saxagliptin', 'Saxagliptin tablets 2.5/5 mg (Glenmark) — Prescribing Information', sid('saxagliptin'))
drug('saxagliptin', 'alimentary-metabolism', 'ساکساگلیپتین', 'Saxagliptin', T('مهارکننده DPP-4', 'DPP-4 inhibitor'), [{'name': 'Onglyza', 'market': 'US'}], ['onglyza', 'انگلیزا', 'ساکساگلیپتین'],
     [tab('tab-5', 5, '5 mg tablet', [R(Sx, '3')]), tab('tab-2-5', 2.5, '2.5 mg tablet', [R(Sx, '3')])],
     [reg('t2dm', 'type-2-diabetes', T('دیابت نوع ۲ بزرگسال — ۲٫۵ یا ۵ mg یک بار', 'Type 2 diabetes, adults — 2.5 or 5 mg once daily'), A18, 'fixed', {'perDose': 2.5, 'perDoseMax': 5, 'dosesPerDay': 1}, [R(Sx, '2.1')],
          notes=[note('با مهارکننده قوی CYP3A4/5 حداکثر ۲٫۵ mg. قرص خرد یا جویده نشود.', 'With strong CYP3A4/5 inhibitors max 2.5 mg. Do not cut, crush or chew.', [R(Sx, '2.3'), R(Sx, '2.1')])])],
     [CI('hyper', 'سابقه حساسیت جدی به ساکساگلیپتین (آنافیلاکسی، آنژیوادم، ضایعات پوستی اکسفولیاتیو).', 'History of serious hypersensitivity to saxagliptin (anaphylaxis, angioedema, exfoliative skin conditions).', [R(Sx, '4')])], warn=[DPP4_W(Sx)],
     renal=[{'egfrBelow': 45, 'severity': 'warn', 'text': T('eGFR زیر ۴۵: ۲٫۵ mg یک بار.', 'eGFR <45: 2.5 mg once daily.'), 'refs': [R(Sx, '2.2')]}],
     exs=[ex('t2dm', 'tab-2-5', {'perDose': 2.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 5}, ageYears=55, weightKg=80)])

Ns = fda('nesina', 'FDA Nesina', 'Nesina (alogliptin) tablets — Prescribing Information', sid('alogliptin'))
drug('alogliptin', 'alimentary-metabolism', 'آلوگلیپتین', 'Alogliptin', T('مهارکننده DPP-4', 'DPP-4 inhibitor'), [{'name': 'Nesina', 'market': 'US'}], ['nesina', 'نزینا', 'vipidia', 'آلوگلیپتین'],
     [tab('tab-25', 25, '25 mg tablet', [R(Ns, '3')]), tab('tab-12-5', 12.5, '12.5 mg tablet', [R(Ns, '3')]), tab('tab-6-25', 6.25, '6.25 mg tablet', [R(Ns, '3')])],
     [reg('t2dm', 'type-2-diabetes', T('دیابت نوع ۲ بزرگسال — ۲۵ mg یک بار', 'Type 2 diabetes, adults — 25 mg once daily'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Ns, '2.1')],
          notes=[note('قرص نصف نشود.', 'Do not split tablets.', [R(Ns, '2.1')])])],
     [CI('hyper', 'سابقه حساسیت جدی به آلوگلیپتین.', 'History of serious hypersensitivity to alogliptin.', [R(Ns, '4')])],
     warn=[DPP4_W(Ns), W('اثرات کبدی (آزمایش کبد پیش از شروع).', 'Hepatic effects (check liver tests before starting).', [R(Ns, '5.4')])],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr ۳۰ تا <۶۰: ۱۲٫۵ mg؛ زیر ۳۰ و ESRD: ۶٫۲۵ mg یک بار.', 'CrCl 30–<60: 12.5 mg; <30 and ESRD: 6.25 mg once daily.'), 'refs': [R(Ns, '2.2')]}],
     exs=[ex('t2dm', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=80)])

Sm = fda('somatuline', 'FDA Somatuline Depot', 'Somatuline Depot (lanreotide) injection — Prescribing Information', sid('lanreotide'))
lsy = lambda mg, ml: form(f'pfs-{mg}', 'injection', 'sc', f'{mg} mg/{ml} mL prefilled syringe (deep SC)', mg, 'mg', [R(Sm, '3')], per='application')
drug('lanreotide', 'systemic-hormones', 'لانرئوتاید', 'Lanreotide', T('آنالوگ سوماتوستاتین', 'Somatostatin analogue'), [{'name': 'Somatuline Depot', 'market': 'US'}], ['somatuline', 'سوماتولین', 'لانرئوتید'],
     [lsy(90, 0.3), lsy(120, 0.5), lsy(60, 0.2)],
     [reg('acro', 'acromegaly', T('آکرومگالی — ۹۰ mg زیرجلدی عمقی هر ۴ هفته به مدت ۳ ماه، سپس تنظیم با GH/IGF-1', 'Acromegaly — 90 mg deep SC every 4 weeks for 3 months, then adjust by GH/IGF-1'), A18, 'fixed', {'perDose': 90, 'dosesPerDay': 1}, [R(Sm, '2')], dur=ONE, allowed=['pfs-90'],
          notes=[note('فقط توسط کادر درمان در ربع خارجی فوقانی باسن؛ محل عوض شود. نارسایی متوسط/شدید کلیه یا کبد: تنظیم طبق برچسب.', 'Healthcare provider only, superior outer buttock quadrant; alternate sites. Moderate/severe renal or hepatic impairment: adjust per label.', [R(Sm, '2.1'), R(Sm, '2')])]),
      reg('net', 'carcinoid-tumors', T('تومورهای نوروآندوکرین گوارشی-پانکراسی یا سندرم کارسینوئید — ۱۲۰ mg هر ۴ هفته', 'GEP-NETs or carcinoid syndrome — 120 mg every 4 weeks'), A18, 'fixed', {'perDose': 120, 'dosesPerDay': 1}, [R(Sm, '2')], dur=ONE, allowed=['pfs-120'])],
     [CI('hyper', 'حساسیت به لانرئوتاید.', 'Hypersensitivity to lanreotide.', [R(Sm, '4')])],
     warn=[W('سنگ صفرا؛ هیپر/هیپوگلیسمی؛ برادیکاردی؛ اختلال تیروئید؛ استئاتوره.', 'Cholelithiasis; hyper/hypoglycaemia; bradycardia; thyroid abnormalities; steatorrhoea.', [R(Sm, '5')])],
     exs=[ex('acro', 'pfs-90', {'perDose': 90, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=80), ex('net', 'pfs-120', {'perDose': 120, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Om = fda('osmitrol', 'FDA Osmitrol', 'Osmitrol (mannitol) injection 10%/20% — Prescribing Information', sid('mannitol'))
drug('mannitol', 'blood', 'مانیتول', 'Mannitol', T('دیورتیک اسموتیک', 'Osmotic diuretic'), [{'name': 'Osmitrol', 'market': 'US'}], ['osmitrol', 'مانیتول', 'manitol'],
     [form('bag-20', 'injection', 'iv', '20% (0.2 g/mL) 250/500 mL bag', 0.2, 'g', [R(Om, '3')], vol=1), form('bag-10', 'injection', 'iv', '10% (0.1 g/mL) 500 mL bag', 0.1, 'g', [R(Om, '3')], vol=1)],
     [once('icp', 'raised-intracranial-pressure', 'کاهش فشار داخل جمجمه — ۰٫۲۵ g/kg وریدی طی ۳۰ دقیقه، هر ۶ تا ۸ ساعت در صورت نیاز', 'Reduce intracranial pressure — 0.25 g/kg IV over 30 min, repeat every 6–8 h', {}, 0.25, None, [R(Om, '2.2')], unit='g',
           notes=[note('ترجیحاً ورید مرکزی. پیش از شروع وضعیت کلیه، قلب و ریه و الکترولیت‌ها اصلاح؛ پایش اسمولالیته. با خون از یک ست نه.', 'Preferably a central vein. Assess renal, cardiac and pulmonary status and correct electrolytes first; monitor osmolality. Not with blood products in the same set.', [R(Om, '2.1'), R(Om, '2.2')])]),
      once('iop', 'glaucoma', 'کاهش فشار داخل چشم — ۱٫۵ تا ۲ g/kg (محلول ۲۰٪) وریدی طی دست‌کم ۳۰ دقیقه، یک دوز', 'Reduce intraocular pressure — 1.5–2 g/kg (20% solution) IV over at least 30 min, single dose', {}, 1.5, 2, [R(Om, '2.2')], unit='g', allowed=['bag-20'])],
     [CI('ci', 'حساسیت به مانیتول؛ آنوری؛ کمبود حجم شدید؛ احتقان یا ادم شدید ریه؛ خونریزی فعال داخل جمجمه (جز حین کرانیوتومی).', 'Hypersensitivity to mannitol; anuria; severe hypovolaemia; severe pulmonary congestion or oedema; active intracranial bleeding (except during craniotomy).', [R(Om, '4')])],
     warn=[W('نارسایی کلیه؛ سمیت CNS؛ اختلال آب و الکترولیت و هیپراسمولاریته؛ واکنش محل انفوزیون.', 'Renal failure; CNS toxicity; fluid/electrolyte imbalance and hyperosmolarity; infusion-site reactions.', [R(Om, '5')])],
     exs=[ex('icp', 'bag-20', {'perDose': 17.5, 'mlPerDose': 87.5}, ageYears=40, weightKg=70), ex('iop', 'bag-20', {'perDose': 105, 'mlPerDose': 525, 'upperPerDose': 140}, ageYears=60, weightKg=70)])

Mp = fda('mercaptopurine', 'FDA Mercaptopurine susp', 'Mercaptopurine oral suspension 20 mg/mL (Hikma) — Prescribing Information', sid('mercaptopurine'))
drug('mercaptopurine', 'antineoplastic-immunomodulating', 'مرکاپتوپورین', 'Mercaptopurine', T('آنتی‌متابولیت پورین', 'Purine antimetabolite'), [{'name': 'Purixan', 'market': 'US'}], ['purinethol', 'purixan', '6-MP', 'مرکاپتوپورین'],
     [liquid('susp-20', 20, 1, '20 mg/mL oral suspension', [R(Mp, '3')])],
     [reg('all', 'acute-lymphoblastic-leukemia', T('ALL — نگهدارنده در رژیم ترکیبی: ۱٫۵ تا ۲٫۵ mg/kg یک بار در روز', 'ALL — combination maintenance: 1.5–2.5 mg/kg once daily'), {}, 'weightBased', {'perKgPerDose': 1.5, 'perKgPerDoseMax': 2.5, 'intervalHours': 24}, [R(Mp, '2.1')],
          notes=[note('معادل ۵۰ تا ۷۵ mg/m². تنظیم با ANC. کمبود TPMT/NUDT15 هموزیگوت: ۱۰٪ یا کمتر. با آلوپورینول یک‌سوم تا یک‌چهارم. ClCr زیر ۵۰ یا نارسایی کبد: کمترین دوز یا فاصله ۳۶ تا ۴۸ ساعت.', 'Equals 50–75 mg/m². Adjust to ANC. Homozygous TPMT/NUDT15 deficiency: ≤10%. With allopurinol one-third to one-quarter. CrCl <50 or hepatic impairment: lowest dose or every 36–48 h.', [R(Mp, '2.1'), R(Mp, '2.2'), R(Mp, '2.4'), R(Mp, '2.3')])])],
     warn=[W('سرکوب مغز استخوان؛ سمیت کبدی؛ سرکوب ایمنی؛ بدخیمی ثانویه؛ سندرم فعال شدن ماکروفاژ؛ سمیت جنینی.', 'Myelosuppression; hepatotoxicity; immunosuppression; secondary malignancy; macrophage activation syndrome; embryo-fetal toxicity.', [R(Mp, '5')])],
     exs=[ex('all', 'susp-20', {'perDose': 30, 'mlPerDose': 1.5, 'upperPerDose': 50}, ageYears=6, weightKg=20)])

Rl = fda('relistor', 'FDA Relistor', 'Relistor (methylnaltrexone) tablets and injection — Prescribing Information', sid('methylnaltrexone'))
drug('methylnaltrexone', 'alimentary-metabolism', 'متیل‌نالترکسون', 'Methylnaltrexone', T('آنتاگونیست محیطی گیرنده اپیوئید (PAMORA)', 'Peripherally acting opioid antagonist (PAMORA)'), [{'name': 'Relistor', 'market': 'US'}], ['relistor', 'رلیستور', 'متیل نالترکسون'],
     [tab('tab-150', 150, '150 mg tablet', [R(Rl, '3')]), form('pfs-12', 'injection', 'sc', '12 mg/0.6 mL vial or syringe (8 mg/0.4 mL syringe)', 20, 'mg', [R(Rl, '3')], vol=1)],
     [reg('cncp-po', 'opioid-induced-constipation', T('یبوست ناشی از اپیوئید در درد مزمن غیرسرطانی — ۴۵۰ mg خوراکی صبح', 'OIC in chronic non-cancer pain — 450 mg orally each morning'), A18, 'fixed', {'perDose': 450, 'dosesPerDay': 1}, [R(Rl, '2.2')], allowed=['tab-150'],
          notes=[note('ملین نگهدارنده پیش از شروع قطع. نزدیک دستشویی باشد. با قطع اپیوئید قطع شود.', 'Stop maintenance laxatives before starting. Stay near a toilet. Stop when the opioid is stopped.', [R(Rl, '2.1')])]),
      reg('cncp-sc', 'opioid-induced-constipation', T('یبوست ناشی از اپیوئید در درد مزمن غیرسرطانی — ۱۲ mg زیرجلدی روزانه', 'OIC in chronic non-cancer pain — 12 mg SC daily'), A18, 'fixed', {'perDose': 12, 'dosesPerDay': 1}, [R(Rl, '2.2')], allowed=['pfs-12']),
      reg('adv', 'opioid-induced-constipation', T('یبوست ناشی از اپیوئید در بیماری پیشرفته — یک روز در میان: ۳۸ تا <۶۲ kg: ۸ mg؛ ۶۲ تا ۱۱۴ kg: ۱۲ mg', 'OIC in advanced illness — every other day: 38–<62 kg: 8 mg; 62–114 kg: 12 mg'), {'minAge': age(18, 'year'), 'minWeightKg': 38, 'maxWeightKg': 114}, 'weightBand',
          {'weightBands': [{'minWeightKg': 38, 'maxWeightKg': 61.99, 'perDose': 8, 'dosesPerDay': 1}, {'minWeightKg': 62, 'maxWeightKg': 114, 'perDose': 12, 'dosesPerDay': 1}]}, [R(Rl, '2.3, Table 1')], dur=ONE, allowed=['pfs-12'],
          notes=[note('زیر ۳۸ یا بالای ۱۱۴ kg: ۰٫۱۵ mg/kg. بیش از یک دوز در ۲۴ ساعت نه.', '<38 or >114 kg: 0.15 mg/kg. Not more than one dose per 24 h.', [R(Rl, '2.3, Table 1')])])],
     [CI('ci', 'انسداد گوارشی شناخته یا مشکوک و خطر انسداد مجدد.', 'Known or suspected GI obstruction and risk of recurrent obstruction.', [R(Rl, '4')])], warn=[PAMORA_W(Rl)],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr زیر ۶۰: قرص ۱۵۰ mg؛ تزریق ۶ mg (درد غیرسرطانی)؛ بیماری پیشرفته نصف دوز جدول.', 'CrCl <60: tablets 150 mg; injection 6 mg (non-cancer pain); advanced illness half the table dose.'), 'refs': [R(Rl, '2.4')]}],
     exs=[ex('cncp-po', 'tab-150', {'perDose': 450, 'tabletsPerDoseRounded': 3}, ageYears=50, weightKg=75), ex('cncp-sc', 'pfs-12', {'perDose': 12, 'mlPerDose': 0.6}, ageYears=50, weightKg=75),
          ex('adv', 'pfs-12', {'perDose': 8, 'mlPerDose': 0.4}, ageYears=70, weightKg=55), ex('adv', 'pfs-12', {'perDose': 12, 'mlPerDose': 0.6}, ageYears=70, weightKg=75)])

Mv = fda('movantik', 'FDA Movantik', 'Movantik (naloxegol) tablets — Prescribing Information', sid('naloxegol'))
drug('naloxegol', 'alimentary-metabolism', 'نالوکسگول', 'Naloxegol', T('آنتاگونیست محیطی گیرنده اپیوئید (PAMORA)', 'Peripherally acting opioid antagonist (PAMORA)'), [{'name': 'Movantik', 'market': 'US'}], ['movantik', 'موونتیک', 'نالوکسگول'],
     [tab('tab-25', 25, '25 mg tablet', [R(Mv, '3')]), tab('tab-12-5', 12.5, '12.5 mg tablet', [R(Mv, '3')])],
     [reg('oic', 'opioid-induced-constipation', T('یبوست ناشی از اپیوئید در درد مزمن غیرسرطانی — ۲۵ mg صبح ناشتا', 'OIC in chronic non-cancer pain — 25 mg each morning on an empty stomach'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 1}, [R(Mv, '2.2')],
          notes=[note('عدم تحمل: ۱۲٫۵ mg. مهارکننده متوسط CYP3A4: پرهیز یا ۱۲٫۵ mg. ملین نگهدارنده قطع شود.', 'If not tolerated: 12.5 mg. Moderate CYP3A4 inhibitors: avoid or 12.5 mg. Stop maintenance laxatives.', [R(Mv, '2.2'), R(Mv, '2.4'), R(Mv, '2')])])],
     [CI('ci', 'انسداد گوارشی شناخته یا مشکوک؛ مهارکننده‌های قوی CYP3A4 (کلاریترومایسین، کتوکونازول)؛ حساسیت.', 'Known or suspected GI obstruction; strong CYP3A4 inhibitors (clarithromycin, ketoconazole); hypersensitivity.', [R(Mv, '4')])], warn=[PAMORA_W(Mv)],
     renal=[{'egfrBelow': 60, 'severity': 'warn', 'text': T('ClCr زیر ۶۰: شروع ۱۲٫۵ mg.', 'CrCl <60: start 12.5 mg.'), 'refs': [R(Mv, '2.3')]}],
     exs=[ex('oic', 'tab-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=50, weightKg=75)])

Xp = fda('xopenex-hfa', 'FDA Xopenex HFA', 'Xopenex HFA (levalbuterol tartrate) inhalation aerosol — Prescribing Information', sid('levalbuterol'))
drug('levalbuterol', 'respiratory', 'لِوآلبوترول', 'Levalbuterol', T('آگونیست بتا-۲ کوتاه‌اثر (SABA)', 'Short-acting beta2-agonist (SABA)'), [{'name': 'Xopenex HFA', 'market': 'US'}], ['xopenex', 'زوپنکس', 'levosalbutamol', 'لووسالبوتامول'],
     [inh('hfa', 45, '45 mcg per actuation (HFA)', Xp)],
     [reg('bs', 'asthma', T('برونکواسپاسم (۴ سال به بالا) — ۲ پاف (۹۰ mcg) هر ۴ تا ۶ ساعت', 'Bronchospasm (≥4 y) — 2 puffs (90 mcg) every 4–6 h'), {'minAge': age(4, 'year')}, 'fixed', {'perDose': 90, 'dosesPerDay': 4}, [R(Xp, '2.1')], unit='mcg',
          notes=[note('برخی بیماران با ۱ پاف هر ۴ ساعت کافی است. نیاز بیشتر نشانه بدتر شدن آسم است. پیش از اولین استفاده یا پس از ۳ روز، ۴ پاف در هوا.', 'Some patients need only 1 puff every 4 h. Needing more signals worsening asthma. Prime with 4 sprays before first use or after 3 days.', [R(Xp, '2.1'), R(Xp, '2.2')])])],
     [CI('hyper', 'حساسیت به لووآلبوترول یا آلبوترول راسمیک.', 'Hypersensitivity to levalbuterol or racemic albuterol.', [R(Xp, '4')])],
     warn=[W('برونکواسپاسم متناقض؛ بدتر شدن آسم؛ اثرات قلبی؛ بیش از دوز توصیه‌شده نه؛ هیپوکالمی.', 'Paradoxical bronchospasm; deteriorating asthma; cardiovascular effects; do not exceed recommended dose; hypokalaemia.', [R(Xp, '5')])],
     exs=[ex('bs', 'hfa', {'perDose': 90, 'tabletsPerDoseRounded': 2}, ageYears=10, weightKg=30)])

Al = fda('alvesco', 'FDA Alvesco', 'Alvesco (ciclesonide) inhalation aerosol — Prescribing Information', sid('ciclesonide'))
drug('ciclesonide', 'respiratory', 'سیکلزونید', 'Ciclesonide', T('کورتیکواستروئید استنشاقی', 'Inhaled corticosteroid'), [{'name': 'Alvesco', 'market': 'US'}], ['alvesco', 'آلوسکو', 'سیکلزونید'],
     [inh('hfa-80', 80, '80 mcg per actuation', Al), inh('hfa-160', 160, '160 mcg per actuation', Al)],
     [reg('asthma', 'asthma', T('نگهدارنده آسم (۱۲ سال به بالا) — ۸۰ mcg دو بار (حداکثر ۱۶۰ یا ۳۲۰ mcg دو بار بر اساس درمان قبلی)', 'Asthma maintenance (≥12 y) — 80 mcg twice daily (max 160 or 320 mcg twice daily by prior therapy)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 80, 'perDoseMax': 320, 'dosesPerDay': 2}, [R(Al, '2.2, Table 1')], unit='mcg',
          notes=[note('فقط برونکودیلاتور قبلی: حداکثر ۱۶۰ mcg دو بار؛ ICS قبلی: تا ۳۲۰؛ کورتیکواستروئید خوراکی: ۳۲۰ mcg دو بار. پس از مصرف دهان شسته شود.', 'Bronchodilators alone before: max 160 mcg twice; prior ICS: up to 320; oral steroids: 320 mcg twice. Rinse mouth after use.', [R(Al, '2.2, Table 1'), R(Al, '2.1')])])],
     [CI('ci', 'درمان اولیه استاتوس آسماتیکوس یا حمله حاد؛ حساسیت به سیکلزونید.', 'Primary treatment of status asthmaticus or acute episodes; hypersensitivity to ciclesonide.', [R(Al, '4')])],
     warn=[W('کاندیدیاز دهان؛ برای حمله حاد نیست؛ سرکوب ایمنی؛ سرکوب آدرنال هنگام قطع استروئید خوراکی؛ کاهش تراکم استخوان؛ اثر بر رشد؛ گلوکوم و آب مروارید.', 'Oral candidiasis; not for acute episodes; immunosuppression; adrenal suppression when switching from oral steroids; reduced bone density; effect on growth; glaucoma and cataract.', [R(Al, '5')])],
     exs=[ex('asthma', 'hfa-80', {'perDose': 80, 'tabletsPerDoseRounded': 1, 'upperPerDose': 320}, ageYears=30, weightKg=70)])

Ad = fda('adderall-xr', 'FDA Adderall XR', 'Adderall XR (mixed amphetamine salts) extended-release capsules — Prescribing Information', sid('amphetamine'))
drug('amphetamine', 'nervous-system', 'آمفتامین (نمک‌های ترکیبی، آهسته‌رهش)', 'Mixed amphetamine salts (extended-release)', T('محرک CNS', 'CNS stimulant'), [{'name': 'Adderall XR', 'market': 'US'}], ['adderall', 'آدرال', 'dextroamphetamine', 'دکستروآمفتامین', 'آمفتامین'],
     [cap('xr-10', 10, Ad, '10 mg XR capsule'), cap('xr-20', 20, Ad, '20 mg XR capsule'), cap('xr-5', 5, Ad, '5 mg XR capsule'), cap('xr-30', 30, Ad, '30 mg XR capsule')],
     [reg('c6', 'adhd', T('ADHD کودک ۶ تا ۱۲ سال — ۱۰ mg صبح؛ هفتگی ۵ یا ۱۰ mg افزایش تا حداکثر ۳۰ mg', 'ADHD, children 6–12 y — 10 mg in the morning; +5 or 10 mg weekly to max 30 mg'), {'minAge': age(6, 'year'), 'maxAge': age(13, 'year')}, 'fixed', {'perDose': 10, 'perDoseMax': 30, 'dosesPerDay': 1}, [R(Ad, '2.3')],
          notes=[note('پیش از شروع بیماری قلبی و تیک بررسی شود. کپسول کامل یا محتوا روی پوره سیب.', 'Screen for cardiac disease and tics first. Swallow whole or sprinkle on applesauce.', [R(Ad, '2.1'), R(Ad, '2.2')])]),
      reg('c13', 'adhd', T('ADHD نوجوان ۱۳ تا ۱۷ سال — ۱۰ mg؛ پس از یک هفته تا ۲۰ mg', 'ADHD, adolescents 13–17 y — 10 mg; may increase to 20 mg after one week'), {'minAge': age(13, 'year'), 'maxAge': age(18, 'year')}, 'fixed', {'perDose': 10, 'perDoseMax': 20, 'dosesPerDay': 1}, [R(Ad, '2.4')]),
      reg('adult', 'adhd', T('ADHD بزرگسال — ۲۰ mg صبح', 'ADHD, adults — 20 mg in the morning'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Ad, '2.5')])],
     [CI('ci', 'حساسیت به آمفتامین؛ MAOI همزمان یا ظرف ۱۴ روز (بحران فشار خون).', 'Hypersensitivity to amphetamine; MAOIs concomitantly or within 14 days (hypertensive crisis).', [R(Ad, '4')])],
     warn=[W('هشدار جعبه‌ای: پتانسیل بالای سوءمصرف، اعتیاد، بیش‌مصرفی و مرگ.', 'Boxed warning: high potential for abuse, misuse and addiction, overdose and death.', [R(Ad, 'Boxed Warning')]),
           W('خطر در بیماری قلبی جدی؛ افزایش فشار و ضربان؛ عوارض روانی؛ مهار رشد؛ تشنج؛ رینود؛ سندرم سروتونین؛ تیک.', 'Risk in serious cardiac disease; raised BP and HR; psychiatric reactions; growth suppression; seizures; Raynaud; serotonin syndrome; tics.', [R(Ad, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('GFR ۱۵ تا <۳۰: بزرگسال ۱۵ mg، کودک ۵ mg (۶ تا ۱۲ سال حداکثر ۲۰)؛ ESRD توصیه نمی‌شود.', 'GFR 15–<30: adults 15 mg, children 5 mg (6–12 y max 20); ESRD not recommended.'), 'refs': [R(Ad, '2.6')]}],
     exs=[ex('c6', 'xr-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'upperPerDose': 30}, ageYears=8, weightKg=25), ex('c13', 'xr-10', {'perDose': 10, 'tabletsPerDoseRounded': 1, 'upperPerDose': 20}, ageYears=14, weightKg=50),
          ex('adult', 'xr-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])
print('s13a1 ok')
