"""Stage 11b — vaccines and immunoprophylaxis missing from stage 4: IPV, rotavirus, MenACWY, typhoid, zoster, RSV, COVID-19, BCG, tuberculin PPD, palivizumab."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's11_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
vac = lambda id, label, src, sec='3', ml=0.5, route='im', form_='injection': form(id, form_, route, label, ml, 'mL', [R(src, sec)], vol=ml)
fx = lambda id, dis, fa, en, pop, ml, refs, notes=None: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': ml, 'dosesPerDay': 1}, refs, unit='mL', dur=ONE, notes=notes)
def vaccine(id, fa, en, cls_fa, cls_en, brand, syn, forms, regs, ci, warn=(), exs=(), market='US'):
    drug(id, 'anti-infectives', fa, en, T(cls_fa, cls_en), [{'name': brand, 'market': market}], syn, forms, regs, ci, warn=warn, exs=exs)
ANA = lambda src, sec, what_fa='', what_en='': CI('allergy', 'واکنش آلرژیک شدید (آنافیلاکسی) به اجزای واکسن یا دوز قبلی' + what_fa + '.', 'Severe allergic reaction (anaphylaxis) to a vaccine component or a previous dose' + what_en + '.', [R(src, sec)])

Ip = fda('ipol', 'FDA IPOL', 'IPOL (inactivated poliovirus vaccine) — Prescribing Information', sid('ipv')); d = R(Ip, 'Dosage and Administration')
vaccine('ipv-vaccine', 'واکسن فلج اطفال تزریقی (IPV)', 'Inactivated polio vaccine (IPV)', 'واکسن غیرفعال', 'Inactivated vaccine', 'IPOL', ['ipol', 'IPV', 'واکسن فلج اطفال', 'پولیو', 'polio'],
        [vac('syr-05', '0.5 mL dose', Ip, 'Dosage and Administration')],
        [fx('child', 'immunization', 'کودک — سری اولیه ۳ دوز ۰٫۵ mL (۲، ۴ و ۶ تا ۱۸ ماهگی) و یادآور ۴ تا ۶ سالگی', 'Children — primary 3 × 0.5 mL (2, 4 and 6–18 months) and a booster at 4–6 y', {'minAge': age(6, 'week'), 'maxAge': age(18, 'year')}, 0.5, [d],
            [note('عضلانی یا زیرجلدی؛ ترجیحاً با فاصله ۸ هفته یا بیشتر و هرگز کمتر از ۴ هفته. در ایران برنامه کشوری را دنبال کنید.', 'IM or SC; preferably 8 or more weeks apart and never less than 4 weeks. In Iran follow the national schedule.', [d])]),
         fx('adult', 'immunization', 'بزرگسال واکسینه‌نشده در معرض خطر — ۳ دوز ۰٫۵ mL', 'Unvaccinated adults at risk of exposure — 3 × 0.5 mL', A18, 0.5, [d],
            [note('دو دوز با فاصله ۱ تا ۲ ماه و دوز سوم ۶ تا ۱۲ ماه بعد (طبق برچسب).', 'Two doses 1–2 months apart and a third 6–12 months later (per label).', [d])])],
        [CI('allergy', 'حساسیت به اجزای واکسن از جمله ۲-فنوکسی‌اتانول، فرمالدئید، نئومایسین، استرپتومایسین و پلی‌میکسین B؛ آنافیلاکسی ظرف ۲۴ ساعت پس از دوز قبلی.', 'Hypersensitivity to vaccine components including 2-phenoxyethanol, formaldehyde, neomycin, streptomycin and polymyxin B; anaphylaxis within 24 h of a previous dose.', [R(Ip, 'Contraindications')])],
        exs=[ex('child', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageMonths=2, weightKg=5), ex('adult', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=30, weightKg=70)])

Rx = fda('rotarix', 'FDA Rotarix', 'Rotarix (rotavirus vaccine, live, oral) — Prescribing Information', sid('rota'))
vaccine('rotavirus-vaccine', 'واکسن روتاویروس (خوراکی)', 'Rotavirus vaccine (oral)', 'واکسن زنده ضعیف‌شده خوراکی', 'Live attenuated oral vaccine', 'Rotarix', ['rotarix', 'rotateq', 'روتاریکس', 'روتاویروس', 'واکسن اسهال'],
        [vac('oral-15', '1.5 mL oral dosing applicator', Rx, '3', ml=1.5, route='oral', form_='solution')],
        [fx('std', 'immunization', 'شیرخوار — ۲ دوز ۱٫۵ mL خوراکی: از ۶ هفتگی، با فاصله دست‌کم ۴ هفته، تا ۲۴ هفتگی', 'Infants — 2 oral doses of 1.5 mL: from 6 weeks, ≥4 weeks apart, completed by 24 weeks', {'minAge': age(6, 'week'), 'maxAge': age(24, 'week')}, 1.5, [R(Rx, '2.1')],
            [note('اگر شیرخوار بیشتر دوز را بیرون داد، می‌توان در همان مراجعه یک دوز جایگزین داد. دو نوع واکسن روتاویروس با هم ترکیب نشوند.', 'If the infant spits out most of the dose, one replacement dose may be given at the same visit. Do not mix different rotavirus vaccines in one series.', [R(Rx, '2.1')])])],
        [CI('ci', 'حساسیت به واکسن؛ ناهنجاری مادرزادی اصلاح‌نشده گوارش مستعد انواژیناسیون؛ سابقه انواژیناسیون؛ نقص ایمنی شدید ترکیبی (SCID).', 'Hypersensitivity to the vaccine; uncorrected congenital GI malformation predisposing to intussusception; history of intussusception; severe combined immunodeficiency (SCID).', [R(Rx, '4')])],
        warn=[W('خطر انواژیناسیون (به‌ویژه ۷ روز پس از دوز اول).', 'Risk of intussusception (mainly within 7 days of the first dose).', [R(Rx, '5')])],
        exs=[ex('std', 'oral-15', {'perDose': 1.5, 'mlPerDose': 1.5}, ageMonths=2, weightKg=5)])

Mv = fda('menveo', 'FDA Menveo', 'Menveo (meningococcal ACWY conjugate vaccine) — Prescribing Information', sid('menacwy')); d = R(Mv, '2.4, Table 1')
vaccine('meningococcal-vaccine', 'واکسن مننگوکوک ACWY (کونژوگه)', 'Meningococcal ACWY conjugate vaccine', 'واکسن کونژوگه', 'Conjugate vaccine', 'Menveo', ['menveo', 'menactra', 'mcv4', 'واکسن مننژیت', 'مننگوکوک'],
        [vac('vial-05', '0.5 mL dose (two-vial for 2 months–55 y; one-vial for 10–55 y)', Mv)],
        [fx('infant', 'immunization', 'شیرخوار از ۲ ماهگی — ۴ دوز در ۲، ۴، ۶ و ۱۲ ماهگی', 'Infants from 2 months — 4 doses at 2, 4, 6 and 12 months', {'minAge': age(2, 'month'), 'maxAge': age(7, 'month')}, 0.5, [d]),
         fx('toddler', 'immunization', '۷ تا ۲۳ ماه — ۲ دوز (دوز دوم در سال دوم و دست‌کم ۳ ماه پس از اول)', '7–23 months — 2 doses (second in the 2nd year, ≥3 months after the first)', {'minAge': age(7, 'month'), 'maxAge': age(2, 'year')}, 0.5, [d]),
         fx('std', 'immunization', '۲ تا ۵۵ سال — یک دوز ۰٫۵ mL عضلانی', '2–55 y — single 0.5 mL IM dose', {'minAge': age(2, 'year'), 'maxAge': age(56, 'year')}, 0.5, [d],
            [note('کودک ۲ تا ۵ سال در خطر مداوم: دوز دوم ۲ ماه بعد. یادآور ۱۵ تا ۵۵ سال در خطر مداوم: یک دوز. زیر ۱۰ سال فقط فرآورده دوویالی.', 'Children 2–5 y at continued risk: a second dose 2 months later. Booster at 15–55 y if at continued risk: one dose. Under 10 y only the two-vial presentation.', [d, R(Mv, '8.4')])])],
        [ANA(Mv, '4', ' یا هر واکسن حاوی توکسوئید دیفتری', ' or any diphtheria toxoid-containing vaccine')],
        exs=[ex('infant', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageMonths=2, weightKg=5), ex('toddler', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageMonths=10, weightKg=9), ex('std', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=17, weightKg=60)])

Ty = uk('emc-typhim', 'eMC Typhim Vi', 'Typhim Vi (typhoid Vi polysaccharide vaccine) — SmPC', 'Sanofi', '4 January 2025', 1393)
vaccine('typhoid-vaccine', 'واکسن حصبه (Vi پلی‌ساکاریدی)', 'Typhoid Vi polysaccharide vaccine', 'واکسن پلی‌ساکاریدی', 'Polysaccharide vaccine', 'Typhim Vi', ['typhim', 'واکسن حصبه', 'واکسن تیفوئید', 'typhoid vaccine'],
        [vac('syr-05', '0.5 mL prefilled syringe', Ty, '6.5') | {'markets': ['UK']}],
        [fx('std', 'typhoid', 'پیشگیری از حصبه — بزرگسال و کودک ۲ سال به بالا: یک دوز ۰٫۵ mL', 'Typhoid prevention — adults and children ≥2 y: single 0.5 mL dose', {'minAge': age(2, 'year')}, 0.5, [R(Ty, '4.2')],
            [note('عضلانی (یا زیرجلدی)، دست‌کم ۲ هفته پیش از احتمال مواجهه. یادآور هر ۳ سال برای کسانی که در خطر می‌مانند. از پاراتیفوئید محافظت نمی‌کند. زیر ۲ سال پاسخ ناکافی است.', 'IM (or SC), at least 2 weeks before possible exposure. Revaccinate every 3 years if at continued risk. No protection against paratyphoid. Inadequate response under 2 y.', [R(Ty, '4.2'), R(Ty, '4.4')])])],
        [CI('allergy', 'حساسیت به ماده مؤثره، اجزا یا بقایای فرمالدئید و کازئین. در بیماری تب‌دار حاد واکسن به تعویق افتد.', 'Hypersensitivity to the active substance, excipients or residues such as formaldehyde or casein. Postpone in acute febrile illness.', [R(Ty, '4.3')])],
        exs=[ex('std', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=30, weightKg=70)], market='UK')

Sh = fda('shingrix', 'FDA Shingrix', 'Shingrix (zoster vaccine recombinant, adjuvanted) — Prescribing Information', sid('shingrix'))
vaccine('zoster-vaccine', 'واکسن زونا (نوترکیب)', 'Recombinant zoster vaccine', 'واکسن نوترکیب با ادجوانت', 'Recombinant adjuvanted vaccine', 'Shingrix', ['shingrix', 'شینگریکس', 'واکسن زونا', 'zoster'],
        [vac('syr-05', '0.5 mL dose', Sh)],
        [fx('std', 'herpes-zoster', 'پیشگیری از زونا — ۵۰ سال به بالا: ۲ دوز ۰٫۵ mL با فاصله ۲ تا ۶ ماه', 'Shingles prevention — ≥50 y: 2 × 0.5 mL, 2–6 months apart', {'minAge': age(50, 'year')}, 0.5, [R(Sh, '2.4'), R(Sh, '1')]),
         fx('immuno', 'herpes-zoster', 'نقص یا سرکوب ایمنی — ۱۸ سال به بالا: ۲ دوز با فاصله ۱ تا ۲ ماه', 'Immunodeficient or immunosuppressed — ≥18 y: 2 doses 1–2 months apart', A18, 0.5, [R(Sh, '2.4'), R(Sh, '1')],
            [note('برای پیشگیری از آبله‌مرغان اولیه نیست.', 'Not for prevention of primary varicella (chickenpox).', [R(Sh, '1')])])],
        [ANA(Sh, '4')], exs=[ex('std', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=60, weightKg=70), ex('immuno', 'syr-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=40, weightKg=70)])

Ar = fda('arexvy', 'FDA Arexvy', 'Arexvy (RSV vaccine recombinant, adjuvanted) — Prescribing Information', sid('arexvy'))
vaccine('rsv-vaccine', 'واکسن RSV بزرگسال', 'RSV vaccine (adult)', 'واکسن نوترکیب با ادجوانت', 'Recombinant adjuvanted vaccine', 'Arexvy', ['arexvy', 'abrysvo', 'واکسن RSV', 'ویروس سنسیشیال'],
        [vac('vial-05', '0.5 mL dose after reconstitution', Ar)],
        [fx('std', 'immunization', 'پیشگیری از عفونت تحتانی RSV — ۶۰ سال به بالا، یا ۱۸ تا ۵۹ سال پرخطر: یک دوز ۰٫۵ mL', 'Prevention of RSV lower respiratory disease — ≥60 y, or 18–59 y at increased risk: single 0.5 mL dose', A18, 0.5, [R(Ar, '2.1'), R(Ar, '1')],
            [note('برای بارداری نیست. زیر ۲ سال احتمالاً ناایمن (بیماری تشدیدشونده تنفسی در مدل حیوانی).', 'Not for use in pregnancy. Likely unsafe under 2 y (enhanced respiratory disease in animal models).', [R(Ar, '1'), R(Ar, '8.4')])])],
        [ANA(Ar, '4')], exs=[ex('std', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=65, weightKg=70)])

Cm = fda('comirnaty', 'FDA Comirnaty', 'Comirnaty (COVID-19 vaccine, mRNA) — Prescribing Information', sid('covid'))
vaccine('covid-vaccine', 'واکسن کووید-۱۹ (mRNA)', 'COVID-19 vaccine (mRNA)', 'واکسن mRNA', 'mRNA vaccine', 'Comirnaty', ['comirnaty', 'pfizer', 'فایزر', 'واکسن کرونا', 'کووید'],
        [vac('dose-03', '0.3 mL single dose (5–11 y vial; ≥12 y prefilled syringe)', Cm, '3', ml=0.3)],
        [fx('std', 'covid-19', 'کووید-۱۹ — ۵ سال به بالا: یک دوز ۰٫۳ mL عضلانی', 'COVID-19 — ≥5 y: single 0.3 mL IM dose', {'minAge': age(5, 'year')}, 0.3, [R(Cm, '2.3'), R(Cm, '2.2')],
            [note('اگر قبلاً واکسن کووید زده، دست‌کم ۲ ماه پس از آخرین دوز. ۵ تا ۱۱ سال: ویال درپوش آبی؛ ۱۲ سال به بالا: سرنگ پرشده خاکستری.', 'If previously vaccinated, at least 2 months after the last COVID-19 dose. 5–11 y: blue-cap vial; ≥12 y: grey-label prefilled syringe.', [R(Cm, '2.3'), R(Cm, '3')])])],
        [ANA(Cm, '4', ' واکسن فایزر', ' of a Pfizer-BioNTech COVID-19 vaccine')],
        warn=[W('میوکاردیت و پریکاردیت (بیشتر مردان جوان، ظرف چند روز پس از تزریق)؛ سنکوپ.', 'Myocarditis and pericarditis (mainly young males, within days of vaccination); syncope.', [R(Cm, '5')])],
        exs=[ex('std', 'dose-03', {'perDose': 0.3, 'mlPerDose': 0.3}, ageYears=40, weightKg=70)])

Bc = fda('bcg-vaccine', 'FDA BCG vaccine', 'BCG vaccine (Tice strain, percutaneous) — Prescribing Information', sid('bcg')); d = R(Bc, 'Dosage and Administration')
vaccine('bcg-vaccine', 'واکسن ب‌ث‌ژ (BCG)', 'BCG vaccine', 'واکسن زنده ضعیف‌شده', 'Live attenuated vaccine', 'BCG Vaccine (Tice)', ['BCG', 'ب ث ژ', 'واکسن سل', 'بی سی جی'],
        [unitform('vial', 'powder-for-injection', 'percutaneous', 'Lyophilised vial (percutaneous use with multiple-puncture device)', [R(Bc, 'How Supplied')])],
        [reg('std', 'tuberculosis', T('پیشگیری از سل — فرآورده آمریکایی Tice با دستگاه چندسوزنی (پوستی)', 'TB prevention — US Tice product, percutaneous multiple-puncture device'), {}, 'notCalculated',
             {'reason': T('این فرآورده آمریکایی فقط از راه پوستی با دستگاه چندسوزنی زده می‌شود و داخل جلدی، زیرجلدی یا عضلانی نیست؛ با واکسن داخل‌جلدی ب‌ث‌ژ برنامه کشوری ایران فرق دارد — برای آن دستورالعمل وزارت بهداشت را دنبال کنید. ویال با ۱ mL آب استریل؛ شیرخوار زیر ۱ ماه نصف دوز (با ۲ mL آب). فقط افراد منفی به تست توبرکولین.',
                          'This US product is given only percutaneously with a multiple-puncture device — NOT intradermal, SC or IM; it differs from the intradermal BCG used in Iran’s national schedule (follow Ministry of Health guidance for that). Reconstitute with 1 mL sterile water; infants <1 month half dose (2 mL water). Tuberculin-negative persons only.')},
             [d, R(Bc, 'Warnings'), R(Bc, 'Indications and Usage')])],
        [CI('immuno', 'نقص ایمنی (HIV، نقص مادرزادی، لوسمی، لنفوم، بدخیمی گسترده) یا سرکوب ایمنی با استروئید، داروهای آلکیله‌کننده، آنتی‌متابولیت یا پرتو؛ بارداری.', 'Impaired immunity (HIV, congenital immunodeficiency, leukaemia, lymphoma, generalised malignancy) or suppression by steroids, alkylating agents, antimetabolites or radiation; pregnancy.', [R(Bc, 'Contraindications')])],
        warn=[W('لنفادنوپاتی و زخم محل؛ عفونت منتشر BCG در نقص ایمنی؛ هرگز وریدی، زیرجلدی، عضلانی یا داخل جلدی (این فرآورده).', 'Lymphadenopathy and local ulceration; disseminated BCG infection in immunodeficiency; never IV, SC, IM or intradermal (this product).', [R(Bc, 'Warnings')])])

Tu = fda('tubersol', 'FDA Tubersol', 'Tubersol (tuberculin PPD, Mantoux) — Prescribing Information', sid('ppd')); d = R(Tu, 'Dosage and Administration')
drug('tuberculin-ppd', 'various', 'تست پوستی توبرکولین (PPD، مانتو)', 'Tuberculin PPD (Mantoux test)', T('آنتی‌ژن تشخیصی', 'Diagnostic antigen'), [{'name': 'Tubersol / Aplisol', 'market': 'US'}], ['PPD', 'tubersol', 'mantoux', 'تست مانتو', 'تست سل', 'TST'],
     [form('vial', 'injection', 'intradermal', '5 TU per 0.1 mL (intradermal)', 0.1, 'mL', [R(Tu, 'How Supplied')], vol=0.1)],
     [reg('test', 'tuberculosis', T('تست مانتو — ۰٫۱ mL (۵ TU) داخل جلدی سطح داخلی ساعد', 'Mantoux test — 0.1 mL (5 TU) intradermal, volar forearm'), {}, 'fixed', {'perDose': 0.1, 'dosesPerDay': 1}, [d], unit='mL', dur=ONE,
          notes=[note('فقط داخل جلدی (برجستگی ۶ تا ۱۰ mm)؛ وریدی، عضلانی یا زیرجلدی نه — تزریق زیرجلدی قابل تفسیر نیست. خواندن ۴۸ تا ۷۲ ساعت بعد (اندازه سفتی، نه قرمزی).', 'Intradermal only (6–10 mm wheal); not IV, IM or SC — an SC injection cannot be interpreted. Read at 48–72 h (induration, not redness).', [d])])],
     [CI('ci', 'حساسیت به اجزا یا واکنش شدید قبلی به تست (نکروز، تاول، آنافیلاکسی، زخم)؛ سل فعال مستند یا سابقه روشن درمان سل؛ سوختگی وسیع یا اگزما.', 'Allergy to a component or severe reaction to a previous test (necrosis, blistering, anaphylaxis, ulceration); documented active TB or a clear history of TB treatment; extensive burns or eczema.', [R(Tu, 'Contraindications')])],
     exs=[ex('test', 'vial', {'perDose': 0.1, 'mlPerDose': 0.1}, ageYears=30, weightKg=70)])

Sy = uk('emc-synagis', 'eMC Synagis', 'Synagis (palivizumab) 50 mg/0.5 mL and 100 mg/1 mL — SmPC', 'AstraZeneca UK', '26 March 2024', 6963)
drug('palivizumab', 'anti-infectives', 'پالیویزوماب', 'Palivizumab', T('آنتی‌بادی مونوکلونال ضد RSV', 'Anti-RSV monoclonal antibody'), [{'name': 'Synagis', 'market': 'UK'}], ['synagis', 'سیناژیس', 'پالیویزوماب'],
     [form('vial-100', 'injection', 'im', '100 mg/mL (50 mg/0.5 mL or 100 mg/1 mL vial)', 100, 'mg', [R(Sy, '6.5')], vol=1, markets=('UK',))],
     [reg('rsv', 'rsv-prophylaxis', T('پیشگیری RSV در کودک پرخطر — ۱۵ mg/kg عضلانی ماهی یک بار در فصل RSV', 'RSV prophylaxis in high-risk children — 15 mg/kg IM once a MONTH during the RSV season'), {'maxAge': age(2, 'year')}, 'weightBased',
          {'perKgPerDose': 15, 'intervalHours': 24}, [R(Sy, '4.2')], dur=ONE,
          notes=[note('یک دوز در هر ماه (نه روزانه) در طول فصل RSV؛ اولین دوز ترجیحاً پیش از شروع فصل؛ اغلب ۵ دوز در فصل. حجم (mL) = وزن × ۰٫۱۵.', 'One dose each MONTH (not daily) through the RSV season; first dose preferably before the season starts; most experience is with 5 doses per season. Volume (mL) = weight × 0.15.', [R(Sy, '4.2')]),
                 note('اندیکاسیون: نوزاد ≤۳۵ هفته و زیر ۶ ماه در شروع فصل؛ زیر ۲ سال با دیسپلازی برونکوپولمونری درمان‌شده در ۶ ماه اخیر؛ زیر ۲ سال با بیماری مادرزادی قلبی مهم.', 'Indications: born ≤35 weeks and <6 months at season onset; <2 y treated for bronchopulmonary dysplasia in the last 6 months; <2 y with haemodynamically significant congenital heart disease.', [R(Sy, '4.1')])])],
     [CI('hyper', 'حساسیت به پالیویزوماب، اجزا یا سایر آنتی‌بادی‌های مونوکلونال انسانی‌شده.', 'Hypersensitivity to palivizumab, excipients or other humanised monoclonal antibodies.', [R(Sy, '4.3')])],
     warn=[W('آنافیلاکسی (گاه کشنده) — داروی درمان آن در دسترس باشد.', 'Anaphylaxis (sometimes fatal) — have treatment available.', [R(Sy, '4.4')])],
     exs=[ex('rsv', 'vial-100', {'perDose': 75, 'mlPerDose': 0.75}, ageMonths=4, weightKg=5)])
print('s11b ok')
