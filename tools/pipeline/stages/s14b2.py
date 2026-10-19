"""Stage 14b (part 2) — PAH (bosentan, ambrisentan, macitentan, riociguat, treprostinil, epoprostenol), iloprost (Aurlumyn, frostbite),
women's health / infertility (mifepristone, etonogestrel implant, levonorgestrel IUS, chorionic gonadotropin, menotropins), calcitonin salmon, iron dextran.
Prostacyclin infusions are dosed in ng/kg/min, which the engine has no unit for — they stay notCalculated with the label titration in the reason."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's14_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
ERA_W = lambda src, sec: W('هشدار جعبه‌ای: سمیت جنینی — در بارداری منع مصرف؛ پیش از شروع و ماهانه تست بارداری، پیشگیری مؤثر تا ۱ ماه پس از قطع (برنامه REMS).', 'Boxed warning: embryo-fetal toxicity — contraindicated in pregnancy; pregnancy test before and monthly, effective contraception until 1 month after stopping (REMS).', [R(src, sec)])
PAH = 'pulmonary-arterial-hypertension'

add_disease('frostbite', 'سرمازدگی شدید', 'Severe frostbite', ['frostbite', 'سرمازدگی', 'یخ‌زدگی انگشتان'], ['T33.90XA'], 'emergency')
add_disease('pregnancy-termination', 'ختم بارداری دارویی', 'Medical termination of pregnancy', ['medical abortion', 'سقط دارویی', 'ختم بارداری'], ['Z33.2'], 'gynecology')
add_disease('cryptorchidism', 'بیضه نزول‌نکرده (کریپتورکیدیسم)', 'Cryptorchidism (undescended testis)', ['cryptorchidism', 'بیضه نزول نکرده', 'کریپتورکیدیسم'], ['Q53.9'], 'urology')
add_disease('hypercalcemia', 'هیپرکلسمی', 'Hypercalcaemia', ['hypercalcemia', 'کلسیم بالا', 'هیپرکلسمی'], ['E83.52'], 'endocrinology')

Tr = fda('tracleer', 'FDA Tracleer', 'Tracleer (bosentan) tablets and tablets for oral suspension — Prescribing Information', sid('bosentan'))
drug('bosentan', 'cardiovascular', 'بوسنتان', 'Bosentan', T('آنتاگونیست گیرنده اندوتلین', 'Endothelin receptor antagonist'), [{'name': 'Tracleer', 'market': 'US'}], ['tracleer', 'تراکلیر', 'بوسنتان'],
     [tab('tab-62-5', 62.5, '62.5 mg tablet', [R(Tr, '3')]), tab('tab-125', 125, '125 mg tablet', [R(Tr, '3')]), tab('disp-32', 32, '32 mg tablet for oral suspension (scored)', [R(Tr, '3')], scored=True)],
     [reg('start', PAH, T('PAH بالای ۱۲ سال — ۶۲٫۵ mg دو بار در روز (۴ هفته اول؛ زیر ۴۰ kg همین دوز ادامه)', 'PAH, over 12 years — 62.5 mg twice daily (first 4 weeks; continue this dose if under 40 kg)'), {'minAge': age(12, 'year')}, 'fixed', {'perDose': 62.5, 'dosesPerDay': 2}, [R(Tr, '2.2, Table 1')], allowed=['tab-62-5']),
      reg('maint', PAH, T('PAH بالای ۱۲ سال و بالای ۴۰ kg — نگهدارنده ۱۲۵ mg دو بار در روز پس از ۴ هفته', 'PAH, over 12 years and over 40 kg — maintenance 125 mg twice daily after 4 weeks'), {'minAge': age(12, 'year'), 'minWeightKg': 40}, 'fixed', {'perDose': 125, 'dosesPerDay': 2}, [R(Tr, '2.2, Table 1')], allowed=['tab-125'],
          notes=[note('بالاتر از ۱۲۵ mg دو بار در روز سود اضافه ندارد و خطر کبدی بیشتر است.', 'Doses above 125 mg twice daily gave no added benefit offsetting liver risk.', [R(Tr, '2.2')])]),
      reg('child', PAH, T('PAH ۱۲ سال و کمتر — دو بار در روز بر اساس وزن: ۴ تا ۸ kg: ۱۶ mg؛ ۸ تا ۱۶: ۳۲؛ ۱۶ تا ۲۴: ۴۸؛ ۲۴ تا ۴۰: ۶۴ mg', 'PAH, 12 years and under — twice daily by weight: 4–8 kg: 16 mg; 8–16: 32; 16–24: 48; 24–40: 64 mg'), {'maxAge': age(12, 'year'), 'minWeightKg': 4, 'maxWeightKg': 40}, 'weightBand',
          {'weightBands': [{'minWeightKg': 4, 'maxWeightKg': 8, 'perDose': 16, 'dosesPerDay': 2}, {'minWeightKg': 8.01, 'maxWeightKg': 16, 'perDose': 32, 'dosesPerDay': 2}, {'minWeightKg': 16.01, 'maxWeightKg': 24, 'perDose': 48, 'dosesPerDay': 2}, {'minWeightKg': 24.01, 'maxWeightKg': 40, 'perDose': 64, 'dosesPerDay': 2}]},
          [R(Tr, '2.2, Table 1')], allowed=['disp-32'])],
     [CI('preg', 'بارداری.', 'Pregnancy.', [R(Tr, '4.1')]), CI('csa', 'مصرف همزمان سیکلوسپورین A.', 'Concomitant cyclosporine A.', [R(Tr, '4.2')]), CI('glyb', 'مصرف همزمان گلی‌بن‌کلامید (گلیبوراید).', 'Concomitant glyburide (glibenclamide).', [R(Tr, '4.3')]),
      CI('hyper', 'حساسیت به بوسنتان (DRESS، آنافیلاکسی، آنژیوادم).', 'Hypersensitivity to bosentan (DRESS, anaphylaxis, angioedema).', [R(Tr, '4.4')])],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی — آنزیم‌های کبد پیش از شروع و ماهانه؛ فقط از طریق برنامه REMS.', 'Boxed warning: hepatotoxicity — liver enzymes before starting and monthly; available only through REMS.', [R(Tr, 'Boxed Warning'), R(Tr, '2.1')]), ERA_W(Tr, 'Boxed Warning'),
           W('احتباس مایع؛ ادم ریه با بیماری انسدادی وریدهای ریه؛ کاهش اسپرم؛ کاهش هموگلوبین.', 'Fluid retention; pulmonary oedema with veno-occlusive disease; decreased sperm counts; haemoglobin decrease.', [R(Tr, '5')])],
     exs=[ex('start', 'tab-62-5', {'perDose': 62.5, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('maint', 'tab-125', {'perDose': 125, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70),
          ex('child', 'disp-32', {'perDose': 16, 'tabletsPerDoseRounded': 0.5}, ageYears=1, weightKg=7), ex('child', 'disp-32', {'perDose': 48, 'tabletsPerDoseRounded': 1.5}, ageYears=6, weightKg=20)])

Lt = fda('letairis', 'FDA Letairis', 'Letairis (ambrisentan) tablets — Prescribing Information', sid('ambrisentan'))
drug('ambrisentan', 'cardiovascular', 'آمبریسنتان', 'Ambrisentan', T('آنتاگونیست گیرنده اندوتلین', 'Endothelin receptor antagonist'), [{'name': 'Letairis', 'market': 'US'}], ['letairis', 'volibris', 'لتایریس', 'آمبریسنتان'],
     [tab('tab-5', 5, '5 mg tablet (do not split)', [R(Lt, '3')]), tab('tab-10', 10, '10 mg tablet', [R(Lt, '3')])],
     [reg('pah', PAH, T('PAH بزرگسال — شروع ۵ mg یک بار در روز (با یا بدون تادالافیل)؛ تا ۱۰ mg', 'PAH, adults — start 5 mg once daily (with or without tadalafil); up to 10 mg'), A18, 'fixed', {'perDose': 5, 'perDoseMax': 10, 'dosesPerDay': 1}, [R(Lt, '2.1')],
          notes=[note('افزایش با فاصله ۴ هفته. قرص شکسته، خرد یا جویده نشود.', 'Titrate at 4-week intervals. Do not split, crush or chew.', [R(Lt, '2.1')])])],
     [CI('preg', 'بارداری.', 'Pregnancy.', [R(Lt, '4.1')]), CI('ipf', 'فیبروز ایدیوپاتیک ریه (شامل فشار ریوی گروه ۳).', 'Idiopathic pulmonary fibrosis (including WHO group 3 pulmonary hypertension).', [R(Lt, '4.2')])],
     warn=[ERA_W(Lt, 'Boxed Warning'), W('احتباس مایع؛ ادم ریه با بیماری انسدادی وریدهای ریه؛ کاهش اسپرم؛ کاهش هموگلوبین.', 'Fluid retention; pulmonary oedema with veno-occlusive disease; decreased sperm counts; haemoglobin decrease.', [R(Lt, '5')])],
     exs=[ex('pah', 'tab-5', {'perDose': 5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 10}, ageYears=45, weightKg=65)])

Op = fda('opsumit', 'FDA Opsumit', 'Opsumit (macitentan) tablets — Prescribing Information', sid('macitentan'))
drug('macitentan', 'cardiovascular', 'ماسیتنتان', 'Macitentan', T('آنتاگونیست گیرنده اندوتلین', 'Endothelin receptor antagonist'), [{'name': 'Opsumit', 'market': 'US'}], ['opsumit', 'اپسومیت', 'ماسیتنتان'],
     [tab('tab-10', 10, '10 mg tablet', [R(Op, '3')])],
     [reg('pah', PAH, T('PAH بزرگسال — ۱۰ mg یک بار در روز', 'PAH, adults — 10 mg once daily'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Op, '2.1')],
          notes=[note('دوز بالاتر از ۱۰ mg بررسی نشده و توصیه نمی‌شود.', 'Doses above 10 mg have not been studied and are not recommended.', [R(Op, '2.1')])])],
     [CI('preg', 'بارداری.', 'Pregnancy.', [R(Op, '4.1')]), CI('hyper', 'حساسیت به ماسیتنتان.', 'Hypersensitivity to macitentan.', [R(Op, '4.2')])],
     warn=[ERA_W(Op, 'Boxed Warning'), W('سمیت کبدی؛ احتباس مایع؛ کاهش هموگلوبین؛ ادم ریه با بیماری انسدادی وریدهای ریه؛ کاهش اسپرم.', 'Hepatotoxicity; fluid retention; haemoglobin decrease; pulmonary oedema with veno-occlusive disease; decreased sperm counts.', [R(Op, '5')])],
     exs=[ex('pah', 'tab-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=65)])

Ad = fda('adempas', 'FDA Adempas', 'Adempas (riociguat) tablets — Prescribing Information', sid('riociguat'))
drug('riociguat', 'cardiovascular', 'ریوسیگوات', 'Riociguat', T('محرک گوانیلات سیکلاز محلول', 'Soluble guanylate cyclase stimulator'), [{'name': 'Adempas', 'market': 'US'}], ['adempas', 'ادمپاس', 'ریوسیگوات'],
     [tab(f'tab-{s.replace(".", "-")}', float(s), f'{s} mg tablet', [R(Ad, '3')]) for s in ('0.5', '1', '1.5', '2', '2.5')],
     [reg('pah', PAH, T('PAH و CTEPH بزرگسال — شروع ۱ mg سه بار در روز؛ هر ۲ هفته ۰٫۵ mg افزایش تا حداکثر ۲٫۵ mg سه بار', 'PAH and CTEPH, adults — start 1 mg three times daily; increase by 0.5 mg every 2 weeks to max 2.5 mg three times daily'), A18, 'fixed', {'perDose': 1, 'perDoseMax': 2.5, 'dosesPerDay': 3}, [R(Ad, '2.1')],
          notes=[note('افزایش فقط اگر فشار سیستولیک بالای ۹۵ و بدون علائم افت فشار. شروع ۰٫۵ mg در خطر افت فشار یا با مهارکننده‌های قوی CYP/P-gp. سیلدنافیل ۲۴ و تادالافیل ۴۸ ساعت قبل قطع شوند.', 'Increase only if systolic BP stays >95 mmHg without hypotension. Start 0.5 mg if at risk of hypotension or with strong CYP/P-gp inhibitors. Stop sildenafil 24 h and tadalafil 48 h before.', [R(Ad, '2.1'), R(Ad, '2.5'), R(Ad, '2.6')])])],
     [CI('preg', 'بارداری.', 'Pregnancy.', [R(Ad, '4.1')]), CI('nitrates', 'نیترات‌ها یا دهنده‌های نیتریک اکسید به هر شکل.', 'Nitrates or nitric oxide donors in any form.', [R(Ad, '4.2')]),
      CI('pde5', 'مهارکننده‌های PDE-5 (سیلدنافیل، تادالافیل، واردنافیل) یا غیراختصاصی (دی‌پیریدامول، تئوفیلین)؛ سایر محرک‌های sGC.', 'PDE-5 inhibitors (sildenafil, tadalafil, vardenafil) or non-specific PDE inhibitors (dipyridamole, theophylline); other sGC stimulators.', [R(Ad, '4.3'), R(Ad, '4.4')]),
      CI('phiip', 'فشار ریوی ناشی از پنومونی‌های بینابینی ایدیوپاتیک (PH-IIP).', 'Pulmonary hypertension associated with idiopathic interstitial pneumonias (PH-IIP).', [R(Ad, '4.5')])],
     warn=[ERA_W(Ad, 'Boxed Warning'), W('افت فشار؛ خونریزی (شامل هموپتیزی)؛ ادم ریه با بیماری انسدادی وریدهای ریه.', 'Hypotension; bleeding (including haemoptysis); pulmonary oedema with veno-occlusive disease.', [R(Ad, '5')])],
     exs=[ex('pah', 'tab-1', {'perDose': 1, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=70)])

Rm = fda('remodulin', 'FDA Remodulin', 'Remodulin (treprostinil) injection — Prescribing Information', sid('treprostinil'))
drug('treprostinil', 'cardiovascular', 'ترپروستینیل', 'Treprostinil', T('آنالوگ پروستاسیکلین', 'Prostacyclin analogue'), [{'name': 'Remodulin', 'market': 'US'}], ['remodulin', 'رمودولین', 'ترپروستینیل'],
     [form('vial-1', 'injection', 'sc', '1 mg/mL, 20 mL vial (also 0.1–20 mg/mL)', 1, 'mg', [R(Rm, '3')], vol=1)],
     [NC('pah', PAH, 'PAH (WHO گروه ۱، NYHA II–IV) — انفوزیون مداوم زیرجلدی (ترجیحی) یا وریدی مرکزی؛ شروع ۱٫۲۵ نانوگرم/kg/دقیقه', 'PAH (WHO group 1, NYHA II–IV) — continuous SC (preferred) or central IV infusion; start 1.25 ng/kg/min', A18,
         'دوز بر حسب نانوگرم/kg/دقیقه با پمپ تیتر می‌شود: افزایش ۱٫۲۵ در هفته طی ۴ هفته اول، سپس ۲٫۵ در هفته. تحمل نشد: ۰٫۶۲۵. نارسایی خفیف تا متوسط کبد: شروع ۰٫۶۲۵. قطع ناگهانی ممنوع. انتقال از اپوپروستنول در بیمارستان.',
         'Dosed in ng/kg/min by pump: increase 1.25 per week for the first 4 weeks, then 2.5 per week. Not tolerated: 0.625. Mild–moderate hepatic impairment: start 0.625. Avoid abrupt cessation. Transition from epoprostenol in hospital.', [R(Rm, '2.2'), R(Rm, '2.4'), R(Rm, '2.5'), R(Rm, '2.7')])],
     [],
     warn=[W('عفونت خونی مرتبط با کاتتر وریدی؛ بدتر شدن PAH با قطع ناگهانی؛ افت فشار؛ خونریزی.', 'Catheter-related bloodstream infection with IV use; worsening PAH on abrupt withdrawal; hypotension; bleeding.', [R(Rm, '5')])])

Ep = fda('epoprostenol', 'FDA Epoprostenol', 'Epoprostenol for injection 0.5 and 1.5 mg — Prescribing Information', sid('epoprostenol'))
drug('epoprostenol', 'cardiovascular', 'اپوپروستنول', 'Epoprostenol', T('پروستاسیکلین', 'Prostacyclin'), [{'name': 'Flolan', 'market': 'US'}, {'name': 'Veletri', 'market': 'US'}], ['flolan', 'veletri', 'فلولان', 'اپوپروستنول'],
     [form('vial-1-5', 'powder-for-injection', 'iv', '1.5 mg vial (also 0.5 mg)', 1.5, 'mg', [R(Ep, '3')], per='vial')],
     [NC('pah', PAH, 'PAH (WHO گروه ۱) — انفوزیون وریدی مداوم از کاتتر مرکزی؛ شروع ۲ نانوگرم/kg/دقیقه', 'PAH (WHO group 1) — continuous IV infusion via central catheter; start 2 ng/kg/min', A18,
         'هر ۱۵ دقیقه یا بیشتر ۲ نانوگرم/kg/دقیقه افزایش تا حد تحمل؛ تنظیم مزمن با گام‌های ۱ تا ۲. فقط با آب استریل یا سالین بازسازی؛ با داروی دیگر مخلوط نشود. قطع یا کاهش ناگهانی ممنوع (برگشت علائم، مرگ).',
         'Increase by 2 ng/kg/min every ≥15 min to tolerance; chronic adjustments in 1–2 ng/kg/min steps. Reconstitute only with sterile water or saline; do not mix with other drugs. Avoid abrupt withdrawal or large reductions (rebound, death).', [R(Ep, '2.1'), R(Ep, '2.2')])],
     [CI('chf', 'مصرف مزمن در نارسایی قلب ناشی از اختلال شدید سیستولیک بطن چپ؛ بروز ادم ریه در شروع دارو؛ حساسیت به دارو.', 'Chronic use in heart failure due to severe left ventricular systolic dysfunction; pulmonary oedema during dose initiation; hypersensitivity.', [R(Ep, '4')])],
     warn=[W('افت فشار و برافروختگی در شروع؛ علائم برگشتی با قطع؛ عفونت کاتتر؛ خونریزی (مهار پلاکت).', 'Hypotension and flushing at initiation; rebound symptoms on withdrawal; catheter infection; bleeding (platelet inhibition).', [R(Ep, '5')])])

Au = fda('aurlumyn', 'FDA Aurlumyn', 'Aurlumyn (iloprost) injection 100 mcg/mL — Prescribing Information', sid('iloprost'))
drug('iloprost', 'cardiovascular', 'ایلوپروست', 'Iloprost', T('مقلد پروستاسیکلین', 'Prostacyclin mimetic'), [{'name': 'Aurlumyn', 'market': 'US'}], ['aurlumyn', 'ventavis', 'ilomedin', 'ونتاویس', 'ایلومدین', 'ایلوپروست'],
     [form('vial-100', 'injection', 'iv', '100 mcg/mL single-dose vial', 100, 'mcg', [R(Au, '3')], vol=1)],
     [NC('frost', 'frostbite', 'سرمازدگی شدید بزرگسال (کاهش خطر قطع انگشت) — انفوزیون وریدی ۶ ساعت در روز تا ۸ روز؛ شروع ۰٫۵ نانوگرم/kg/دقیقه', 'Severe frostbite in adults (to reduce digit amputation) — IV infusion 6 h daily for up to 8 days; start 0.5 ng/kg/min', A18,
         'هر ۳۰ دقیقه ۰٫۵ نانوگرم/kg/دقیقه افزایش تا حداکثر ۲؛ روز ۲ و ۳ تیتراسیون تکرار؛ از روز ۴ با بالاترین دوز تحمل‌شده. نارسایی متوسط/شدید کبد: شروع ۰٫۲۵. علائم حیاتی پیش و پس از هر افزایش. شکل استنشاقی (Ventavis) برای PAH جداست.',
         'Increase by 0.5 ng/kg/min every 30 min to max 2; repeat titration on days 2 and 3; from day 4 start at the highest tolerated rate. Moderate/severe hepatic impairment: start 0.25. Vital signs before and after each increase. Inhaled Ventavis for PAH is a different product.', [R(Au, '2.1'), R(Au, '2.3')])],
     [],
     warn=[W('افت فشار علامت‌دار.', 'Symptomatic hypotension.', [R(Au, '5.1')])])

Mf = fda('mifeprex', 'FDA Mifeprex', 'Mifeprex (mifepristone) tablets 200 mg — Prescribing Information', sid('mifepristone'))
drug('mifepristone', 'genitourinary-sex-hormones', 'میفپریستون', 'Mifepristone', T('آنتاگونیست پروژسترون', 'Progestin antagonist'), [{'name': 'Mifeprex', 'market': 'US'}], ['mifeprex', 'ru-486', 'میفپرکس', 'میفپریستون'],
     [tab('tab-200', 200, '200 mg tablet', [R(Mf, '3')])],
     [reg('mtop', 'pregnancy-termination', T('ختم دارویی بارداری داخل رحمی تا ۷۰ روز — ۲۰۰ mg خوراکی روز ۱، سپس ۲۴ تا ۴۸ ساعت بعد میزوپروستول ۸۰۰ mcg باکال', 'Medical termination of intrauterine pregnancy through 70 days — 200 mg orally on day 1, then misoprostol 800 mcg buccally 24–48 h later'), {}, 'fixed', {'perDose': 200, 'dosesPerDay': 1}, [R(Mf, '2.1')], dur=ONE,
          notes=[note('IUD پیش از شروع خارج شود. پیگیری ۷ تا ۱۴ روز بعد برای تأیید ختم کامل الزامی است.', 'Remove any IUD before starting. Follow-up at 7–14 days to confirm complete termination is required.', [R(Mf, '2.1'), R(Mf, '2.3')])])],
     [CI('ci', 'حاملگی خارج رحمی قطعی یا مشکوک یا توده آدنکس تشخیص‌داده‌نشده؛ IUD در محل؛ نارسایی مزمن آدرنال؛ کورتیکواستروئید طولانی‌مدت؛ حساسیت به میفپریستون، میزوپروستول یا پروستاگلاندین‌ها؛ اختلال خونریزی یا داروی ضدانعقاد؛ پورفیری ارثی.',
         'Confirmed or suspected ectopic pregnancy or undiagnosed adnexal mass; IUD in place; chronic adrenal failure; long-term corticosteroid therapy; allergy to mifepristone, misoprostol or prostaglandins; haemorrhagic disorders or anticoagulant therapy; inherited porphyrias.', [R(Mf, '4')])],
     warn=[W('هشدار جعبه‌ای: عفونت و خونریزی جدی و گاه کشنده (عفونت ممکن است بدون تب باشد). فقط از طریق برنامه REMS.', 'Boxed warning: serious and sometimes fatal infections and bleeding (infection may present without fever). Available only through REMS.', [R(Mf, 'Boxed Warning')]),
           W('حاملگی خارج رحمی را درمان نمی‌کند؛ ایمن‌سازی Rh (ایمونوگلوبولین anti-D در Rh منفی).', 'Does not treat ectopic pregnancy; Rh immunisation (anti-D immune globulin if Rh-negative).', [R(Mf, '5')])],
     exs=[ex('mtop', 'tab-200', {'perDose': 200, 'tabletsPerDoseRounded': 1}, ageYears=28, weightKg=60)])

Nx = fda('nexplanon', 'FDA Nexplanon', 'Nexplanon (etonogestrel implant) 68 mg — Prescribing Information', sid('nexplanon'))
drug('etonogestrel-implant', 'genitourinary-sex-hormones', 'ایمپلنت اتونوژسترل', 'Etonogestrel implant', T('پروژستین (ضدبارداری طولانی‌اثر)', 'Progestin (long-acting contraceptive)'), [{'name': 'Nexplanon', 'market': 'US'}], ['nexplanon', 'implanon', 'نکسپلانون', 'ایمپلانون', 'ایمپلنت ضدبارداری'],
     [unitform('implant', 'implant', 'subdermal', 'One 68 mg etonogestrel rod in a preloaded applicator', [R(Nx, '3')])],
     [reg('contra', 'contraception', T('پیشگیری از بارداری تا ۵ سال — یک ایمپلنت زیرپوستی در بازوی غیرغالب', 'Prevention of pregnancy for up to 5 years — one subdermal implant in the non-dominant arm'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Nx, '1'), R(Nx, '2')], unit='application', dur=ONE,
          notes=[note('پیش از گذاشتن، بارداری رد شود؛ زمان گذاشتن به روش قبلی بستگی دارد. گذاشتن و خارج کردن فقط توسط فرد آموزش‌دیده (REMS).', 'Rule out pregnancy before insertion; timing depends on prior contraception. Insertion and removal only by trained providers (REMS).', [R(Nx, '2.1'), R(Nx, '2.2')])])],
     [CI('ci', 'بارداری قطعی یا مشکوک؛ سابقه فعلی یا قبلی ترومبوز؛ تومور کبد یا بیماری فعال کبد؛ خونریزی رحمی غیرطبیعی تشخیص‌داده‌نشده؛ سرطان پستان یا سرطان حساس به پروژستین (فعلی یا قبلی)؛ حساسیت به اجزا.',
         'Known or suspected pregnancy; current or past thrombosis; liver tumours or active liver disease; undiagnosed abnormal uterine bleeding; current or past breast or other progestin-sensitive cancer; allergy to components.', [R(Nx, '4')])],
     warn=[W('هشدار جعبه‌ای: عوارض گذاشتن یا خارج کردن نادرست (آسیب عصب و عروق، جابجایی، مهاجرت به عروق ریه).', 'Boxed warning: complications of improper insertion and removal (nerve/vascular injury, migration, including to pulmonary vessels).', [R(Nx, 'Boxed Warning')]),
           W('تغییر الگوی خونریزی؛ حاملگی خارج رحمی؛ ترومبوز؛ کیست تخمدان؛ افزایش فشار خون؛ کاهش اثر با القاکننده‌های CYP3A4.', 'Changed bleeding pattern; ectopic pregnancy; thrombosis; ovarian cysts; raised blood pressure; reduced efficacy with CYP3A4 inducers.', [R(Nx, '5')])],
     exs=[ex('contra', 'implant', {'perDose': 1}, ageYears=25, weightKg=60)])

Mr = fda('mirena', 'FDA Mirena', 'Mirena (levonorgestrel-releasing intrauterine system) 52 mg — Prescribing Information', sid('mirena'))
drug('levonorgestrel-ius', 'genitourinary-sex-hormones', 'سیستم داخل رحمی لوونورژسترل (میرنا)', 'Levonorgestrel intrauterine system 52 mg', T('پروژستین داخل رحمی', 'Intrauterine progestin'), [{'name': 'Mirena', 'market': 'US'}], ['mirena', 'میرنا', 'آی یو دی هورمونی', 'LNG-IUS', 'IUD'],
     [unitform('ius', 'intrauterine-system', 'intrauterine', 'One T-shaped system with 52 mg levonorgestrel (about 21 mcg/day at first)', [R(Mr, '3')])],
     [reg('contra', 'contraception', T('پیشگیری از بارداری تا ۸ سال — یک سیستم داخل رحمی', 'Prevention of pregnancy for up to 8 years — one intrauterine system'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Mr, '1'), R(Mr, '2.1')], unit='application', dur=ONE,
          notes=[note('گذاشتن توسط فرد آموزش‌دیده با روش استریل؛ معاینه مجدد ۴ تا ۶ هفته بعد و سپس سالانه.', 'Inserted by a trained provider with strict asepsis; re-examine at 4–6 weeks and then yearly.', [R(Mr, '2.2'), R(Mr, '2.3')])]),
      reg('hmb', 'heavy-menstrual-bleeding', T('خونریزی شدید قاعدگی در زنانی که IUD را برای پیشگیری انتخاب کرده‌اند — تا ۵ سال', 'Heavy menstrual bleeding in women choosing intrauterine contraception — up to 5 years'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 1}, [R(Mr, '1'), R(Mr, '2.1')], unit='application', dur=ONE)],
     [CI('ci', 'بارداری یا شک به آن؛ پیشگیری اورژانسی؛ ناهنجاری رحم که حفره را تغییر دهد؛ PID حاد یا سابقه آن؛ اندومتریت پس از زایمان یا سقط عفونی در ۳ ماه اخیر؛ سرطان پستان یا سرطان حساس به پروژستین؛ سرطان رحم یا دهانه رحم؛ بیماری حاد کبد یا تومور کبد.',
         'Pregnancy or suspicion; emergency contraception; uterine anomaly distorting the cavity; acute or prior PID; postpartum endometritis or infected abortion in the past 3 months; breast or progestin-sensitive cancer; uterine or cervical malignancy; acute liver disease or liver tumour.', [R(Mr, '4')])],
     warn=[W('حاملگی خارج رحمی؛ خطرات بارداری داخل رحمی با IUD؛ سپسیس؛ عفونت لگن؛ سوراخ شدن رحم؛ خروج خودبه‌خود؛ کیست تخمدان؛ تغییر الگوی خونریزی.', 'Ectopic pregnancy; risks of intrauterine pregnancy with the device; sepsis; pelvic infection; perforation; expulsion; ovarian cysts; bleeding pattern changes.', [R(Mr, '5')])],
     exs=[ex('contra', 'ius', {'perDose': 1}, ageYears=30, weightKg=60), ex('hmb', 'ius', {'perDose': 1}, ageYears=40, weightKg=70)])

Nv = fda('novarel', 'FDA Novarel', 'Novarel (chorionic gonadotropin for injection) — Prescribing Information', sid('hcg')); d = R(Nv, 'Dosage and Administration')
drug('chorionic-gonadotropin', 'genitourinary-sex-hormones', 'گنادوتروپین جفتی انسانی (hCG)', 'Chorionic gonadotropin (hCG)', T('گنادوتروپین', 'Gonadotropin'), [{'name': 'Novarel', 'market': 'US'}, {'name': 'Pregnyl', 'market': 'US'}], ['hcg', 'novarel', 'pregnyl', 'پرگنیل', 'اچ سی جی', 'گنادوتروپین کوریونیک'],
     [form('vial-10000', 'powder-for-injection', 'im', '10,000 USP units vial (also 5,000) — IM only', 10000, 'unit', [R(Nv, 'How Supplied')], per='vial')],
     [reg('ovul', 'female-infertility', T('القای تخمک‌گذاری پس از منوتروپین‌ها — ۵۰۰۰ تا ۱۰۰۰۰ واحد عضلانی یک روز پس از آخرین دوز منوتروپین', 'Ovulation induction after menotropins — 5,000–10,000 units IM one day after the last menotropins dose'), A18, 'fixed', {'perDose': 5000, 'perDoseMax': 10000, 'dosesPerDay': 1}, [d], unit='unit', dur=ONE,
          notes=[note('فقط توسط پزشک باتجربه در ناباروری. در خطر OHSS در پایش تخمدان، hCG داده نشود.', 'Only by physicians experienced in infertility. Withhold hCG if ovarian monitoring suggests OHSS risk.', [R(Nv, 'Warnings')])]),
      NC('crypt', 'cryptorchidism', 'بیضه نزول‌نکرده پیش از بلوغ (بدون انسداد آناتومیک) — رژیم‌های عضلانی برچسب', 'Prepubertal cryptorchidism (not due to anatomical obstruction) — labelled IM regimens', {'maxAge': age(18, 'year')},
         'یکی از رژیم‌ها: ۴۰۰۰ واحد سه بار در هفته ۳ هفته؛ ۵۰۰۰ واحد یک روز در میان ۴ تزریق؛ ۱۵ تزریق ۵۰۰ تا ۱۰۰۰ واحد طی ۶ هفته؛ ۵۰۰ واحد سه بار در هفته ۴ تا ۶ هفته.',
         'One of: 4,000 units three times weekly for 3 weeks; 5,000 units every other day for 4 injections; 15 injections of 500–1,000 units over 6 weeks; 500 units three times weekly for 4–6 weeks.', [d]),
      NC('hypogon', 'male-hypogonadism', 'هیپوگنادیسم هیپوگنادوتروپیک مردان (موارد منتخب) — رژیم‌های عضلانی برچسب', 'Selected hypogonadotropic hypogonadism in males — labelled IM regimens', A18,
         '۵۰۰ تا ۱۰۰۰ واحد سه بار در هفته ۳ هفته، سپس همان دوز دو بار در هفته ۳ هفته؛ یا ۴۰۰۰ واحد سه بار در هفته ۶ تا ۹ ماه، سپس ۲۰۰۰ واحد سه بار در هفته ۳ ماه دیگر.',
         '500–1,000 units three times weekly for 3 weeks, then twice weekly for 3 weeks; or 4,000 units three times weekly for 6–9 months, then 2,000 units three times weekly for 3 more months.', [d])],
     [CI('ci', 'بلوغ زودرس؛ سرطان پروستات یا سایر نئوپلاسم‌های وابسته به آندروژن؛ سابقه حساسیت به hCG.', 'Precocious puberty; prostatic carcinoma or other androgen-dependent neoplasm; prior allergic reaction to hCG.', [R(Nv, 'Contraindications')])],
     warn=[W('سندرم تحریک بیش از حد تخمدان (OHSS)؛ پارگی کیست تخمدان؛ بارداری چندقلو؛ ترومبوآمبولی. برای کاهش وزن مؤثر نیست.', 'Ovarian hyperstimulation syndrome; ovarian cyst rupture; multiple births; thromboembolism. Not effective for weight loss.', [R(Nv, 'Warnings'), R(Nv, 'Indications and Usage')])],
     exs=[ex('ovul', 'vial-10000', {'perDose': 5000, 'upperPerDose': 10000}, ageYears=32, weightKg=60)])

Mn = fda('menopur', 'FDA Menopur', 'Menopur (menotropins for injection) 75 IU — Prescribing Information', sid('menotropins'))
drug('menotropins', 'genitourinary-sex-hormones', 'منوتروپین (hMG)', 'Menotropins (hMG)', T('گنادوتروپین (FSH + LH)', 'Gonadotropin (FSH + LH)'), [{'name': 'Menopur', 'market': 'US'}], ['menopur', 'hmg', 'منوپور', 'منوتروپین', 'اچ ام جی'],
     [form('vial-75', 'powder-for-injection', 'sc', '75 IU FSH + 75 IU LH per vial', 75, 'unit', [R(Mn, '3')], per='vial')],
     [reg('art', 'female-infertility', T('تحریک تخمک‌گذاری در IVF (پس از آگونیست GnRH) — شروع ۲۲۵ واحد زیرجلدی روزانه از روز ۲ یا ۳ سیکل', 'Ovarian stimulation for IVF (after GnRH agonist) — start 225 IU SC daily from cycle day 2 or 3'), A18, 'fixed', {'perDose': 225, 'dosesPerDay': 1}, [R(Mn, '2.2')], unit='unit',
          notes=[note('پس از ۵ روز بر اساس سونوگرافی و استرادیول تنظیم؛ هر بار حداکثر ۱۵۰ واحد و نه زودتر از هر ۲ روز؛ حداکثر ۴۵۰ واحد/روز و ۲۰ روز. سپس hCG.', 'Adjust after 5 days by ultrasound and oestradiol; at most 150 IU per change and not more often than every 2 days; max 450 IU/day and 20 days. Then hCG.', [R(Mn, '2.2')])])],
     [CI('ci', 'حساسیت به منوتروپین؛ FSH بالا (نارسایی اولیه تخمدان)؛ بارداری؛ اختلال غدد درون‌ریز کنترل‌نشده غیرگنادی (تیروئید، آدرنال، هیپوفیز)؛ تومورهای وابسته به هورمون جنسی؛ کیست تخمدان غیر از PCOS؛ خونریزی رحمی نامشخص.',
         'Hypersensitivity to menotropins; high FSH (primary ovarian failure); pregnancy; uncontrolled non-gonadal endocrinopathies (thyroid, adrenal, pituitary); sex-hormone-dependent tumours; ovarian cysts not due to PCOS; abnormal uterine bleeding of undetermined origin.', [R(Mn, '4')])],
     warn=[W('بزرگی غیرطبیعی تخمدان؛ OHSS؛ عوارض ریوی و عروقی؛ پیچ‌خوردگی تخمدان؛ بارداری چندقلو؛ حاملگی خارج رحمی.', 'Abnormal ovarian enlargement; OHSS; pulmonary and vascular complications; ovarian torsion; multiple gestation; ectopic pregnancy.', [R(Mn, '5')])],
     exs=[ex('art', 'vial-75', {'perDose': 225}, ageYears=32, weightKg=60)])

Mc = fda('miacalcin-inj', 'FDA Miacalcin inj', 'Miacalcin (calcitonin salmon) injection 200 units/mL — Prescribing Information', sid('calcitonin'))
drug('calcitonin', 'systemic-hormones', 'کلسی‌تونین سالمون', 'Calcitonin salmon', T('هورمون تنظیم‌کننده کلسیم', 'Calcium-regulating hormone'), [{'name': 'Miacalcin', 'market': 'US'}], ['miacalcin', 'calcitonin', 'میاکلسین', 'کلسی تونین'],
     [form('inj-200', 'injection', 'sc', '200 units/mL, 2 mL multi-dose vial (SC or IM)', 200, 'unit', [R(Mc, '3')], vol=1)],
     [reg('paget', 'pagets-disease', T('بیماری پاژه علامت‌دار — ۱۰۰ واحد زیرجلدی یا عضلانی روزانه', 'Symptomatic Paget disease of bone — 100 units SC or IM daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Mc, '2.1')], unit='unit'),
      reg('op', 'osteoporosis', T('پوکی استخوان پس از یائسگی (بیش از ۵ سال) — ۱۰۰ واحد روزانه', 'Postmenopausal osteoporosis (>5 years after menopause) — 100 units daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Mc, '2.3')], unit='unit',
          notes=[note('کلسیم حداقل ۱۰۰۰ mg و ویتامین D حداقل ۴۰۰ واحد روزانه.', 'Calcium at least 1000 mg and vitamin D at least 400 IU daily.', [R(Mc, '2.5')])]),
      reg('hypercal', 'hypercalcemia', T('هیپرکلسمی — شروع ۴ واحد/kg هر ۱۲ ساعت؛ تا ۸ واحد/kg هر ۱۲ ساعت (سپس حداکثر ۸ واحد/kg هر ۶ ساعت)', 'Hypercalcaemia — start 4 units/kg every 12 h; up to 8 units/kg every 12 h (then max 8 units/kg every 6 h)'), A18, 'weightBased', {'perKgPerDose': 4, 'perKgPerDoseMax': 8, 'intervalHours': 12}, [R(Mc, '2.2')], unit='unit',
          notes=[note('اگر پس از ۱ تا ۲ روز پاسخ نبود ۸ واحد/kg هر ۱۲ ساعت؛ اگر ۲ روز بعد هم نبود حداکثر ۸ واحد/kg هر ۶ ساعت.', 'If no response after 1–2 days, 8 units/kg every 12 h; if still none after 2 more days, max 8 units/kg every 6 h.', [R(Mc, '2.2')])])],
     [CI('hyper', 'حساسیت به کلسی‌تونین سالمون یا اجزا (آنافیلاکسی کشنده گزارش شده).', 'Hypersensitivity to calcitonin salmon or excipients (fatal anaphylaxis reported).', [R(Mc, '4')])],
     warn=[W('حساسیت؛ هیپوکلسمی (تتانی)؛ بدخیمی در مصرف طولانی؛ تشکیل آنتی‌بادی.', 'Hypersensitivity; hypocalcaemia (tetany); malignancy with long-term use; antibody formation.', [R(Mc, '5')])],
     exs=[ex('paget', 'inj-200', {'perDose': 100, 'mlPerDose': 0.5}, ageYears=65, weightKg=70), ex('op', 'inj-200', {'perDose': 100, 'mlPerDose': 0.5}, ageYears=65, weightKg=60),
          ex('hypercal', 'inj-200', {'perDose': 280, 'mlPerDose': 1.4, 'upperPerDose': 560}, ageYears=60, weightKg=70)])

If = fda('infed', 'FDA INFeD', 'INFeD (iron dextran injection) 50 mg/mL — Prescribing Information', sid('iron-dextran'))
drug('iron-dextran', 'blood', 'آیرون دکستران', 'Iron dextran', T('آهن تزریقی', 'Parenteral iron'), [{'name': 'INFeD', 'market': 'US'}], ['infed', 'cosmofer', 'کاسموفر', 'آیرون دکستران', 'آهن دکستران'],
     [form('inj-50', 'injection', 'iv', '50 mg/mL, 2 mL vial (IV or IM)', 50, 'mg', [R(If, '3')], vol=1)],
     [NC('ida', 'iron-deficiency-anemia', 'فقر آهن وقتی آهن خوراکی ممکن نیست — دوز کل از جدول یا فرمول برچسب (هموگلوبین و وزن)', 'Iron deficiency when oral iron is not possible — total dose from the label table or formula (haemoglobin and weight)', {'minAge': age(4, 'month')},
         'بزرگسال و کودک بالای ۱۵ kg: حجم (mL) = ۰٫۰۴۴۲ × (Hb هدف − Hb فعلی) × وزن بدون چربی + ۰٫۲۶ × وزن بدون چربی (هدف ۱۴٫۸). ۵ تا ۱۵ kg: با وزن واقعی و هدف ۱۲. ابتدا دوز آزمایشی ۰٫۵ mL و ۱ ساعت صبر؛ حداکثر روزانه ۲ mL (۱۰۰ mg)؛ سرعت حداکثر ۵۰ mg/دقیقه.',
         'Adults and children >15 kg: volume (mL) = 0.0442 × (target Hb − observed Hb) × lean body weight + 0.26 × LBW (target 14.8). 5–15 kg: actual weight and target 12. Give a 0.5 mL test dose first and wait 1 h; max daily 2 mL (100 mg); rate max 50 mg/min.', [R(If, '2.2'), R(If, '2.4'), R(If, '2.1')])],
     [CI('hyper', 'سابقه حساسیت به آیرون دکستران.', 'Previous hypersensitivity to iron dextran.', [R(If, '4')])],
     warn=[W('هشدار جعبه‌ای: واکنش‌های آنافیلاکتیک کشنده — دوز آزمایشی پیش از اولین دوز درمانی و امکانات احیا در دسترس.', 'Boxed warning: fatal anaphylactic-type reactions — test dose before the first therapeutic dose, resuscitation equipment at hand.', [R(If, 'Boxed Warning')]),
           W('واکنش تأخیری (آرترالژی، میالژی، تب) ۱ تا ۲ روز بعد؛ اضافه بار آهن.', 'Delayed reactions (arthralgia, myalgia, fever) 1–2 days later; iron overload.', [R(If, '5')])])
print('s14b2 ok')
