"""Stage 12f (part 2) — IL-23 inhibitors (guselkumab, risankizumab, tildrakizumab) and multiple sclerosis (natalizumab, ocrelizumab, ofatumumab, cladribine, siponimod, ozanimod, glatiramer, interferon beta-1a)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
inj = lambda id, mg, ml, label, src, route='sc', unit='mg': form(id, 'injection', route, label, mg, unit, [R(src, '3')], vol=ml)
fx = lambda id, dis, fa, en, pop, mg, refs, allowed=None, notes=None, unit='mg': reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': mg, 'dosesPerDay': 1}, refs, unit=unit, dur=ONE, allowed=allowed, notes=notes)
IL23_W = lambda src: W('حساسیت؛ عفونت؛ سل (پیش از شروع بررسی)؛ واکسن زنده نه.', 'Hypersensitivity; infections; tuberculosis (screen first); no live vaccines.', [R(src, '5')])
S1P_CI = lambda src, extra_fa, extra_en: CI('ci', 'در ۶ ماه اخیر: MI، آنژین ناپایدار، سکته، TIA، نارسایی قلب جبران‌نشده یا کلاس III/IV؛ بلوک AV موبیتز II یا درجه ۳ یا سندرم سینوس بیمار بدون پیس‌میکر؛ ' + extra_fa,
    'Within 6 months: MI, unstable angina, stroke, TIA, decompensated or class III/IV heart failure; Mobitz II or third-degree AV block or sick sinus syndrome without a pacemaker; ' + extra_en, [R(src, '4')])
S1P_W = lambda src: W('عفونت و PML؛ ادم ماکولا؛ برادی‌آریتمی در شروع؛ اثر تنفسی؛ آسیب کبد؛ سرطان پوست؛ افزایش فشار خون؛ خطر جنینی؛ تشدید شدید ناتوانی پس از قطع.', 'Infections and PML; macular oedema; bradyarrhythmia at initiation; respiratory effects; liver injury; skin cancer; raised blood pressure; fetal risk; severe disability increase after stopping.', [R(src, '5')])
CD20_W = lambda src: W('عفونت (HBV پیش از شروع)؛ PML؛ کاهش ایمونوگلوبولین‌ها؛ آسیب کبد.', 'Infections (screen HBV first); PML; reduced immunoglobulins; liver injury.', [R(src, '5')])

Tm = fda('tremfya', 'FDA Tremfya', 'Tremfya (guselkumab) injection — Prescribing Information', sid('guselkumab'))
drug('guselkumab', 'antineoplastic-immunomodulating', 'گوسلکوماب', 'Guselkumab', T('آنتی‌بادی ضد IL-23', 'Anti-IL-23 antibody'), [{'name': 'Tremfya', 'market': 'US'}], ['tremfya', 'ترمفیا', 'گوسلکوماب'],
     [inj('pfs-100', 100, 1, '100 mg/mL syringe, pen or One-Press', Tm), inj('vial-200', 200, 20, '200 mg/20 mL (10 mg/mL) vial for IV infusion', Tm, route='iv')],
     [fx('pso', 'psoriasis', 'پسوریازیس پلاک متوسط تا شدید (بزرگسال و کودک ۶ سال و ≥۴۰ kg) — ۱۰۰ mg هفته ۰، ۴ و سپس هر ۸ هفته', 'Moderate–severe plaque psoriasis (adults and children ≥6 y and ≥40 kg) — 100 mg at weeks 0, 4, then every 8 weeks', {'minAge': age(6, 'year'), 'minWeightKg': 40}, 100, [R(Tm, '2.2')], allowed=['pfs-100']),
      fx('psa', 'psoriatic-arthritis', 'آرتریت پسوریاتیک (بزرگسال و کودک ۶ سال و ≥۴۰ kg) — ۱۰۰ mg هفته ۰، ۴ و سپس هر ۸ هفته', 'Psoriatic arthritis (adults and children ≥6 y and ≥40 kg) — 100 mg at weeks 0, 4, then every 8 weeks', {'minAge': age(6, 'year'), 'minWeightKg': 40}, 100, [R(Tm, '2.3')], allowed=['pfs-100']),
      fx('uc-ind', 'ulcerative-colitis', 'کولیت اولسراتیو بزرگسال — القا ۲۰۰ mg وریدی (دست‌کم ۱ ساعت) هفته ۰، ۴ و ۸', 'Ulcerative colitis, adults — induction 200 mg IV (over ≥1 h) at weeks 0, 4 and 8', A18, 200, [R(Tm, '2.4')], allowed=['vial-200'],
         notes=[note('یا ۴۰۰ mg زیرجلدی (دو تزریق ۲۰۰) همان هفته‌ها. نگهدارنده: ۱۰۰ mg زیرجلدی هفته ۱۶ و سپس هر ۸ هفته. پیش از شروع آنزیم کبد و بیلی‌روبین.', 'Or 400 mg SC (two 200 mg injections) at the same weeks. Maintenance: 100 mg SC at week 16 then every 8 weeks. Check liver enzymes and bilirubin first.', [R(Tm, '2.4'), R(Tm, '2')])])],
     [CI('hyper', 'سابقه حساسیت جدی به گوسلکوماب.', 'History of serious hypersensitivity to guselkumab.', [R(Tm, '4')])],
     warn=[IL23_W(Tm), W('سمیت کبدی (به‌ویژه دوزهای القای IBD).', 'Hepatotoxicity (especially IBD induction doses).', [R(Tm, '5.4')])],
     exs=[ex('pso', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=40, weightKg=80), ex('psa', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=45, weightKg=80), ex('uc-ind', 'vial-200', {'perDose': 200, 'mlPerDose': 20}, ageYears=35, weightKg=70)])

Sk = fda('skyrizi', 'FDA Skyrizi', 'Skyrizi (risankizumab-rzaa) — Prescribing Information', sid('risankizumab'))
drug('risankizumab', 'antineoplastic-immunomodulating', 'ریسانکیزوماب', 'Risankizumab', T('آنتی‌بادی ضد IL-23', 'Anti-IL-23 antibody'), [{'name': 'Skyrizi', 'market': 'US'}], ['skyrizi', 'اسکایریزی', 'ریسانکیزوماب'],
     [inj('pen-150', 150, 1, '150 mg/mL pen or syringe', Sk), inj('pfs-55', 55, 0.37, '55 mg/0.37 mL syringe', Sk), inj('vial-600', 600, 10, '600 mg/10 mL vial for IV infusion', Sk, route='iv'), inj('cart-180', 180, 1.2, '180 mg/1.2 mL syringe or on-body cartridge', Sk), inj('cart-360', 360, 2.4, '360 mg/2.4 mL on-body cartridge', Sk)],
     [fx('pso', 'psoriasis', 'پسوریازیس پلاک یا آرتریت پسوریاتیک بزرگسال — ۱۵۰ mg هفته ۰، ۴ و سپس هر ۱۲ هفته', 'Plaque psoriasis or psoriatic arthritis, adults — 150 mg at weeks 0, 4, then every 12 weeks', A18, 150, [R(Sk, '2.3'), R(Sk, '2.4')], allowed=['pen-150']),
      reg('pso-child', 'psoriasis', T('پسوریازیس پلاک کودک ۶ سال به بالا — زیر ۴۰ kg: ۵۵ mg؛ ۴۰ kg و بالاتر: ۱۵۰ mg (هفته ۰، ۴، سپس هر ۱۲ هفته)', 'Plaque psoriasis, children ≥6 y — <40 kg: 55 mg; ≥40 kg: 150 mg (weeks 0, 4, then every 12 weeks)'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year')}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 39.99, 'perDose': 55, 'dosesPerDay': 1}, {'minWeightKg': 40, 'maxWeightKg': None, 'perDose': 150, 'dosesPerDay': 1}]}, [R(Sk, '2.3')], dur=ONE),
      fx('cd-ind', 'crohns', 'کرون بزرگسال — القا ۶۰۰ mg وریدی (دست‌کم ۱ ساعت) هفته ۰، ۴ و ۸', 'Crohn disease, adults — induction 600 mg IV (over ≥1 h) at weeks 0, 4 and 8', A18, 600, [R(Sk, '2.6')], allowed=['vial-600'],
         notes=[note('نگهدارنده ۱۸۰ یا ۳۶۰ mg زیرجلدی هفته ۱۲ و سپس هر ۸ هفته (کمترین دوز مؤثر). پیش از شروع آنزیم کبد و بیلی‌روبین.', 'Maintenance 180 or 360 mg SC at week 12 then every 8 weeks (lowest effective dose). Check liver enzymes and bilirubin first.', [R(Sk, '2.6'), R(Sk, '2')])]),
      fx('uc-ind', 'ulcerative-colitis', 'کولیت اولسراتیو بزرگسال — القا ۱۲۰۰ mg وریدی (دست‌کم ۲ ساعت) هفته ۰، ۴ و ۸', 'Ulcerative colitis, adults — induction 1200 mg IV (over ≥2 h) at weeks 0, 4 and 8', A18, 1200, [R(Sk, '2.7')], allowed=['vial-600']),
      reg('ibd-m', 'crohns', T('نگهدارنده کرون یا کولیت — ۱۸۰ یا ۳۶۰ mg زیرجلدی هر ۸ هفته', 'Maintenance Crohn or UC — 180 or 360 mg SC every 8 weeks'), A18, 'fixed', {'perDose': 180, 'perDoseMax': 360, 'dosesPerDay': 1}, [R(Sk, '2.6'), R(Sk, '2.7')], dur=ONE, allowed=['cart-180'])],
     [CI('hyper', 'سابقه حساسیت جدی به ریسانکیزوماب.', 'History of serious hypersensitivity to risankizumab.', [R(Sk, '4')])], warn=[IL23_W(Sk)],
     exs=[ex('pso', 'pen-150', {'perDose': 150, 'mlPerDose': 1}, ageYears=40, weightKg=80), ex('pso-child', 'pfs-55', {'perDose': 55, 'mlPerDose': 0.37}, ageYears=9, weightKg=30), ex('pso-child', 'pen-150', {'perDose': 150, 'mlPerDose': 1}, ageYears=14, weightKg=50),
          ex('cd-ind', 'vial-600', {'perDose': 600, 'mlPerDose': 10}, ageYears=35, weightKg=70), ex('uc-ind', 'vial-600', {'perDose': 1200, 'mlPerDose': 20}, ageYears=35, weightKg=70), ex('ibd-m', 'cart-180', {'perDose': 180, 'mlPerDose': 1.2, 'upperPerDose': 360}, ageYears=35, weightKg=70)])

Il = fda('ilumya', 'FDA Ilumya', 'Ilumya (tildrakizumab-asmn) injection — Prescribing Information', sid('tildrakizumab'))
drug('tildrakizumab', 'antineoplastic-immunomodulating', 'تیلدراکیزوماب', 'Tildrakizumab', T('آنتی‌بادی ضد IL-23', 'Anti-IL-23 antibody'), [{'name': 'Ilumya', 'market': 'US'}], ['ilumya', 'ایلومیا', 'تیلدراکیزوماب'],
     [inj('pfs-100', 100, 1, '100 mg/mL prefilled syringe', Il)],
     [fx('pso', 'psoriasis', 'پسوریازیس پلاک متوسط تا شدید بزرگسال — ۱۰۰ mg هفته ۰، ۴ و سپس هر ۱۲ هفته', 'Moderate–severe plaque psoriasis, adults — 100 mg at weeks 0, 4, then every 12 weeks', A18, 100, [R(Il, '2.2')])],
     [CI('hyper', 'حساسیت جدی به تیلدراکیزوماب.', 'Serious hypersensitivity to tildrakizumab.', [R(Il, '4')])], warn=[IL23_W(Il)],
     exs=[ex('pso', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=40, weightKg=80)])

Ty = fda('tysabri', 'FDA Tysabri', 'Tysabri (natalizumab) injection — Prescribing Information', sid('natalizumab'))
drug('natalizumab', 'antineoplastic-immunomodulating', 'ناتالیزوماب', 'Natalizumab', T('آنتی‌بادی ضد اینتگرین α4', 'Anti-α4 integrin antibody'), [{'name': 'Tysabri', 'market': 'US'}], ['tysabri', 'تیزابری', 'ناتالیزوماب'],
     [inj('vial-300', 300, 15, '300 mg/15 mL (20 mg/mL) vial for IV infusion', Ty, route='iv')],
     [fx('ms', 'multiple-sclerosis', 'ام‌اس عودکننده بزرگسال — ۳۰۰ mg انفوزیون وریدی ۱ ساعته هر ۴ هفته', 'Relapsing MS, adults — 300 mg IV infusion over 1 h every 4 weeks', A18, 300, [R(Ty, '2.1')],
         notes=[note('فقط در برنامه TOUCH؛ بولوس نه؛ تا ۴۸ ساعت پس از تهیه. ۱۲ انفوزیون اول یک ساعت پس از آن پایش.', 'TOUCH program only; never IV push; use within 48 h of preparation. Observe 1 h after each of the first 12 infusions.', [R(Ty, '2.1'), R(Ty, '2')])]),
      fx('cd', 'crohns', 'کرون متوسط تا شدید بزرگسال — ۳۰۰ mg وریدی هر ۴ هفته (بدون سرکوب‌کننده ایمنی یا ضد TNF همزمان)', 'Moderate–severe Crohn disease, adults — 300 mg IV every 4 weeks (no concomitant immunosuppressants or TNF inhibitors)', A18, 300, [R(Ty, '2.2')])],
     [CI('ci', 'PML فعلی یا قبلی؛ حساسیت به ناتالیزوماب.', 'Current or past PML; hypersensitivity to natalizumab.', [R(Ty, '4')])],
     warn=[W('هشدار جعبه‌ای: لکوآنسفالوپاتی چندکانونی پیشرونده (PML) — خطر با آنتی‌بادی JCV، مدت درمان و سرکوب ایمنی قبلی بیشتر.', 'Boxed warning: progressive multifocal leukoencephalopathy (PML) — risk rises with anti-JCV antibodies, treatment duration and prior immunosuppressants.', [R(Ty, 'Boxed Warning')]),
           W('عفونت هرپسی (آنسفالیت، رتینیت)؛ سمیت کبد؛ حساسیت.', 'Herpes infections (encephalitis, retinitis); hepatotoxicity; hypersensitivity.', [R(Ty, '5')])],
     exs=[ex('ms', 'vial-300', {'perDose': 300, 'mlPerDose': 15}, ageYears=35, weightKg=65), ex('cd', 'vial-300', {'perDose': 300, 'mlPerDose': 15}, ageYears=35, weightKg=65)])

Oc = fda('ocrevus', 'FDA Ocrevus', 'Ocrevus (ocrelizumab) injection for IV use — Prescribing Information', sid('ocrelizumab'))
drug('ocrelizumab', 'antineoplastic-immunomodulating', 'اوکرلیزوماب', 'Ocrelizumab', T('آنتی‌بادی ضد CD20', 'Anti-CD20 antibody'), [{'name': 'Ocrevus', 'market': 'US'}], ['ocrevus', 'اوکرووس', 'اکرلیزوماب'],
     [inj('vial-300', 300, 10, '300 mg/10 mL (30 mg/mL) vial', Oc, route='iv')],
     [reg('start', 'multiple-sclerosis', T('ام‌اس عودکننده یا پیشرونده اولیه — شروع: دو انفوزیون با ۲ هفته فاصله؛ ≥۳۵ kg: ۳۰۰ mg هر بار؛ کودک ۱۰ سال، ۲۵ تا <۳۵ kg: ۱۵۰ mg', 'Relapsing or primary progressive MS — start: two infusions 2 weeks apart; ≥35 kg: 300 mg each; children ≥10 y, 25–<35 kg: 150 mg'), {'minAge': age(10, 'year'), 'minWeightKg': 25}, 'weightBand',
          {'weightBands': [{'minWeightKg': 25, 'maxWeightKg': 34.99, 'perDose': 150, 'dosesPerDay': 1}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 300, 'dosesPerDay': 1}]}, [R(Oc, '2.3')], dur=ONE,
          notes=[note('پیش‌دارو متیل‌پردنیزولون و آنتی‌هیستامین پیش از هر انفوزیون؛ پایش تا ۱ ساعت بعد. پیش از شروع HBV، ایمونوگلوبولین و آنزیم کبد.', 'Premedicate with methylprednisolone and an antihistamine before each infusion; observe for 1 h after. Screen HBV, immunoglobulins and liver tests first.', [R(Oc, '2.2'), R(Oc, '2.1')])]),
      reg('maint', 'multiple-sclerosis', T('نگهدارنده هر ۶ ماه — ≥۳۵ kg: ۶۰۰ mg؛ ۲۵ تا <۳۵ kg: ۳۰۰ mg', 'Maintenance every 6 months — ≥35 kg: 600 mg; 25–<35 kg: 300 mg'), {'minAge': age(10, 'year'), 'minWeightKg': 25}, 'weightBand',
          {'weightBands': [{'minWeightKg': 25, 'maxWeightKg': 34.99, 'perDose': 300, 'dosesPerDay': 1}, {'minWeightKg': 35, 'maxWeightKg': None, 'perDose': 600, 'dosesPerDay': 1}]}, [R(Oc, '2.3')], dur=ONE)],
     [CI('ci', 'عفونت فعال HBV؛ سابقه واکنش انفوزیون تهدیدکننده حیات به اوکرلیزوماب.', 'Active HBV infection; history of life-threatening infusion reaction to ocrelizumab.', [R(Oc, '4')])],
     warn=[CD20_W(Oc), W('واکنش انفوزیون؛ بدخیمی (پستان)؛ کولیت ایمنی.', 'Infusion reactions; malignancies (breast); immune-mediated colitis.', [R(Oc, '5')])],
     exs=[ex('start', 'vial-300', {'perDose': 300, 'mlPerDose': 10}, ageYears=35, weightKg=65), ex('start', 'vial-300', {'perDose': 150, 'mlPerDose': 5}, ageYears=11, weightKg=30), ex('maint', 'vial-300', {'perDose': 600, 'mlPerDose': 20}, ageYears=35, weightKg=65)])

Ks = fda('kesimpta', 'FDA Kesimpta', 'Kesimpta (ofatumumab) injection — Prescribing Information', sid('ofatumumab'))
drug('ofatumumab', 'antineoplastic-immunomodulating', 'اوفاتوموماب', 'Ofatumumab', T('آنتی‌بادی ضد CD20 (زیرجلدی)', 'Anti-CD20 antibody (SC)'), [{'name': 'Kesimpta', 'market': 'US'}], ['kesimpta', 'کسیمپتا', 'اوفاتوموماب'],
     [inj('pen-20', 20, 0.4, '20 mg/0.4 mL Sensoready pen or syringe', Ks)],
     [fx('ms', 'multiple-sclerosis', 'ام‌اس عودکننده بزرگسال — ۲۰ mg زیرجلدی هفته ۰، ۱ و ۲، سپس ماهانه از هفته ۴', 'Relapsing MS, adults — 20 mg SC at weeks 0, 1 and 2, then monthly from week 4', A18, 20, [R(Ks, '2.2')],
         notes=[note('پیش از شروع HBV، ایمونوگلوبولین و آنزیم کبد.', 'Screen HBV, immunoglobulins and liver tests before starting.', [R(Ks, '2.1')])])],
     [CI('ci', 'عفونت فعال HBV؛ سابقه حساسیت یا واکنش تزریقی تهدیدکننده حیات.', 'Active HBV infection; prior hypersensitivity or life-threatening injection reaction.', [R(Ks, '4')])],
     warn=[CD20_W(Ks), W('واکنش تزریقی؛ خطر جنینی (پیشگیری تا ۶ ماه).', 'Injection-related reactions; fetal risk (contraception for 6 months).', [R(Ks, '5')])],
     exs=[ex('ms', 'pen-20', {'perDose': 20, 'mlPerDose': 0.4}, ageYears=35, weightKg=65)])

Mv = fda('mavenclad', 'FDA Mavenclad', 'Mavenclad (cladribine) tablets 10 mg — Prescribing Information', sid('cladribine'))
drug('cladribine', 'antineoplastic-immunomodulating', 'کلادریبین (خوراکی)', 'Cladribine (oral)', T('آنالوگ پورین', 'Purine analogue'), [{'name': 'Mavenclad', 'market': 'US'}], ['mavenclad', 'ماونکلاد', 'کلادریبین'],
     [tab('tab-10', 10, '10 mg tablet', [R(Mv, '3')])],
     [NC('ms', 'multiple-sclerosis', 'ام‌اس عودکننده بزرگسال — مجموع ۳٫۵ mg/kg طی ۲ دوره سالانه (هر دوره ۱٫۷۵ mg/kg در ۲ سیکل ۴ تا ۵ روزه)', 'Relapsing MS, adults — cumulative 3.5 mg/kg over 2 yearly courses (1.75 mg/kg per course in two 4–5-day cycles)', A18,
         'تعداد قرص هر روز از جدول ۱ برچسب بر اساس دسته وزنی تعیین می‌شود (نه محاسبه مستقیم). سیکل دوم ۲۳ تا ۲۷ روز پس از اولی. پیش از هر دوره CBC و لنفوسیت؛ پروفیلاکسی هرپس اگر لنفوسیت زیر ۲۰۰. با سایر داروهای خوراکی ۳ ساعت فاصله.',
         'Daily tablet numbers come from label Table 1 by weight band (not a direct calculation). Second cycle 23–27 days after the first. CBC with lymphocytes before each course; herpes prophylaxis if lymphocytes <200. Separate other oral drugs by 3 h.', [R(Mv, '2.2'), R(Mv, '2.5'), R(Mv, '2.6'), R(Mv, '2.4')])],
     [CI('ci', 'بدخیمی فعلی؛ بارداری و افراد بارور بدون پیشگیری مؤثر (تا ۶ ماه زن، ۱۴ هفته مرد)؛ HIV؛ عفونت مزمن فعال (هپاتیت، سل)؛ حساسیت؛ شیردهی در روزهای درمان و ۱۰ روز بعد.',
         'Current malignancy; pregnancy and people of reproductive potential without effective contraception (6 months women, 14 weeks men); HIV; active chronic infections (hepatitis, TB); hypersensitivity; breastfeeding on treatment days and for 10 days after.', [R(Mv, '4')])],
     warn=[W('هشدار جعبه‌ای: بدخیمی و خطر ناهنجاری جنینی.', 'Boxed warning: malignancies and risk of teratogenicity.', [R(Mv, 'Boxed Warning')]),
           W('لنفوپنی؛ عفونت (هرپس زوستر، سل)؛ سمیت خونی؛ GVHD با خون اشعه‌ندیده؛ آسیب کبد؛ نارسایی قلب.', 'Lymphopenia; infections (zoster, TB); haematologic toxicity; GVHD with non-irradiated blood; liver injury; cardiac failure.', [R(Mv, '5')])])

Mz = fda('mayzent', 'FDA Mayzent', 'Mayzent (siponimod) tablets — Prescribing Information', sid('siponimod'))
drug('siponimod', 'antineoplastic-immunomodulating', 'سیپونیمود', 'Siponimod', T('تعدیل‌کننده گیرنده S1P', 'S1P receptor modulator'), [{'name': 'Mayzent', 'market': 'US'}], ['mayzent', 'مایزنت', 'سیپونیمود'],
     [tab('tab-2', 2, '2 mg tablet', [R(Mz, '3')]), tab('tab-1', 1, '1 mg tablet', [R(Mz, '3')]), tab('tab-0-25', 0.25, '0.25 mg tablet (titration)', [R(Mz, '3')])],
     [reg('ms', 'multiple-sclerosis', T('ام‌اس عودکننده بزرگسال (CYP2C9 *1/*1، *1/*2، *2/*2) — نگهدارنده ۲ mg یک بار از روز ۶ پس از تیتراسیون ۵ روزه', 'Relapsing MS, adults (CYP2C9 *1/*1, *1/*2, *2/*2) — maintenance 2 mg once daily from day 6 after a 5-day titration'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Mz, '2.2')], allowed=['tab-2'],
          notes=[note('پیش از شروع ژنوتیپ CYP2C9. *1/*3 یا *2/*3: ۱ mg از روز ۵ پس از تیتراسیون ۴ روزه. قرص کامل. وقفه ۴ روز یا بیشتر: تیتراسیون از روز ۱. برادیکاردی یا بلوک AV یا سابقه MI/نارسایی قلب: پایش ۶ ساعته دوز اول.', 'Genotype CYP2C9 first. *1/*3 or *2/*3: 1 mg from day 5 after a 4-day titration. Swallow whole. Interruption ≥4 days: restart titration. Bradycardia, AV block or prior MI/HF: 6-hour first-dose monitoring.', [R(Mz, '2.2'), R(Mz, '2.3'), R(Mz, '2.5'), R(Mz, '2.4')])])],
     [S1P_CI(Mz, 'ژنوتیپ CYP2C9*3/*3؛ حساسیت به سیپونیمود.', 'CYP2C9*3/*3 genotype; hypersensitivity to siponimod.')], warn=[S1P_W(Mz)],
     exs=[ex('ms', 'tab-2', {'perDose': 2, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=65)])

Zp = fda('zeposia', 'FDA Zeposia', 'Zeposia (ozanimod) capsules — Prescribing Information', sid('ozanimod'))
drug('ozanimod', 'antineoplastic-immunomodulating', 'اوزانیمود', 'Ozanimod', T('تعدیل‌کننده گیرنده S1P', 'S1P receptor modulator'), [{'name': 'Zeposia', 'market': 'US'}], ['zeposia', 'زپوسیا', 'اوزانیمود'],
     [form('cap-0-92', 'capsule', 'oral', '0.92 mg capsule', 0.92, 'mg', [R(Zp, '3')], per='capsule')],
     [reg('ms', 'multiple-sclerosis', T('ام‌اس عودکننده بزرگسال — ۰٫۹۲ mg یک بار از روز ۸ پس از تیتراسیون ۷ روزه', 'Relapsing MS, adults — 0.92 mg once daily from day 8 after a 7-day titration'), A18, 'fixed', {'perDose': 0.92, 'dosesPerDay': 1}, [R(Zp, '2.2')],
          notes=[note('روز ۱–۴: ۰٫۲۳ mg؛ روز ۵–۷: ۰٫۴۶ mg. نارسایی خفیف/متوسط کبد: ۰٫۹۲ mg یک روز در میان. فراموشی دوز در ۲ هفته اول: تیتراسیون از نو.', 'Days 1–4: 0.23 mg; days 5–7: 0.46 mg. Mild/moderate hepatic impairment: 0.92 mg every other day. Missed dose in the first 2 weeks: restart titration.', [R(Zp, '2.2, Table 1'), R(Zp, '2.3'), R(Zp, '2.4')])]),
      reg('uc', 'ulcerative-colitis', T('کولیت اولسراتیو متوسط تا شدید بزرگسال — ۰٫۹۲ mg یک بار از روز ۸ پس از تیتراسیون', 'Moderate–severe ulcerative colitis, adults — 0.92 mg once daily from day 8 after titration'), A18, 'fixed', {'perDose': 0.92, 'dosesPerDay': 1}, [R(Zp, '2.2')])],
     [S1P_CI(Zp, 'آپنه خواب شدید درمان‌نشده؛ مهارکننده MAO همزمان.', 'severe untreated sleep apnoea; concomitant MAO inhibitors.')], warn=[S1P_W(Zp)],
     exs=[ex('ms', 'cap-0-92', {'perDose': 0.92, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=65), ex('uc', 'cap-0-92', {'perDose': 0.92, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=65)])

Cx = fda('copaxone', 'FDA Copaxone', 'Copaxone (glatiramer acetate) injection — Prescribing Information', sid('glatiramer'))
drug('glatiramer', 'antineoplastic-immunomodulating', 'گلاتیرامر استات', 'Glatiramer acetate', T('تعدیل‌کننده ایمنی ام‌اس', 'MS immunomodulator'), [{'name': 'Copaxone', 'market': 'US'}], ['copaxone', 'کوپاکسون', 'گلاتیرامر', 'سیناژن کوپاکسون'],
     [inj('pfs-20', 20, 1, '20 mg/mL prefilled syringe (white plunger)', Cx), inj('pfs-40', 40, 1, '40 mg/mL prefilled syringe (blue plunger)', Cx)],
     [reg('d20', 'multiple-sclerosis', T('ام‌اس عودکننده بزرگسال — ۲۰ mg زیرجلدی روزانه', 'Relapsing MS, adults — 20 mg SC daily'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 1}, [R(Cx, '2.1')], allowed=['pfs-20'],
          notes=[note('۲۰ mg و ۴۰ mg جایگزین هم نیستند. وریدی نه. پیش از تزریق به دمای اتاق برسد.', '20 mg and 40 mg are not interchangeable. Never IV. Warm to room temperature first.', [R(Cx, '2.1'), R(Cx, '2')])]),
      fx('w40', 'multiple-sclerosis', 'ام‌اس عودکننده بزرگسال — ۴۰ mg زیرجلدی سه بار در هفته (دست‌کم ۴۸ ساعت فاصله)', 'Relapsing MS, adults — 40 mg SC three times a week (at least 48 h apart)', A18, 40, [R(Cx, '2.1')], allowed=['pfs-40'])],
     [CI('hyper', 'حساسیت به گلاتیرامر یا مانیتول.', 'Hypersensitivity to glatiramer acetate or mannitol.', [R(Cx, '4')])],
     warn=[W('هشدار جعبه‌ای: آنافیلاکسی تهدیدکننده حیات، از اولین دوز تا سال‌ها بعد.', 'Boxed warning: life-threatening anaphylaxis, from the first dose up to years later.', [R(Cx, 'Boxed Warning')]),
           W('واکنش فوری پس از تزریق؛ درد قفسه سینه؛ لیپوآتروفی و نکروز پوست؛ آسیب کبد.', 'Immediate post-injection reaction; chest pain; lipoatrophy and skin necrosis; liver injury.', [R(Cx, '5')])],
     exs=[ex('d20', 'pfs-20', {'perDose': 20, 'mlPerDose': 1}, ageYears=35, weightKg=65), ex('w40', 'pfs-40', {'perDose': 40, 'mlPerDose': 1}, ageYears=35, weightKg=65)])

Av = fda('avonex', 'FDA Avonex', 'Avonex (interferon beta-1a) injection for IM use — Prescribing Information', sid('avonex'))
drug('interferon-beta-1a', 'antineoplastic-immunomodulating', 'اینترفرون بتا-۱a (عضلانی)', 'Interferon beta-1a (IM)', T('اینترفرون', 'Interferon'), [{'name': 'Avonex', 'market': 'US'}], ['avonex', 'آوونکس', 'cinnovex', 'سینووکس', 'interferon beta'],
     [inj('pfs-30', 30, 0.5, '30 mcg/0.5 mL prefilled syringe or autoinjector', Av, route='im', unit='mcg')],
     [fx('ms', 'multiple-sclerosis', 'ام‌اس عودکننده بزرگسال — ۳۰ mcg عضلانی یک بار در هفته', 'Relapsing MS, adults — 30 mcg IM once a week', A18, 30, [R(Av, '2.1')], unit='mcg',
         notes=[note('برای کاهش علائم شبه‌آنفلوانزا: شروع ۷٫۵ mcg و هر هفته ۷٫۵ mcg افزایش طی ۳ هفته. مسکن/تب‌بر روز تزریق.', 'To reduce flu-like symptoms: start 7.5 mcg and increase by 7.5 mcg weekly over 3 weeks. Analgesic/antipyretic on injection days.', [R(Av, '2.1'), R(Av, '2.3')])])],
     [CI('hyper', 'حساسیت به اینترفرون بتای طبیعی یا نوترکیب.', 'Hypersensitivity to natural or recombinant interferon beta.', [R(Av, '4')])],
     warn=[W('افسردگی، خودکشی و سایکوز؛ آسیب کبد؛ آنافیلاکسی؛ نکروز محل تزریق؛ نارسایی قلب؛ کاهش شمارش خون؛ میکروآنژیوپاتی ترومبوتیک؛ تشنج.', 'Depression, suicide and psychosis; hepatic injury; anaphylaxis; injection-site necrosis; heart failure; decreased blood counts; thrombotic microangiopathy; seizures.', [R(Av, '5')])],
     exs=[ex('ms', 'pfs-30', {'perDose': 30, 'mlPerDose': 0.5}, ageYears=35, weightKg=65)])
print('s12f2 ok')
