"""Stage 12f (part 1) — gout (probenecid, pegloticase) and rheumatology biologics (belimumab, anakinra, tocilizumab, abatacept, certolizumab, golimumab, ixekizumab)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
once = lambda id, dis, fa, en, pop, kg, kgmax, refs, unit='mg', notes=None, allowed=None, limits=None: reg(id, dis, T(fa, en), pop, 'weightBased',
    {'perKgPerDose': kg, **({'perKgPerDoseMax': kgmax} if kgmax else {}), 'intervalHours': 24}, refs, unit=unit, dur=ONE, notes=notes, allowed=allowed, limits=limits)
inj = lambda id, mg, ml, label, src, route='sc': form(id, 'injection', route, label, mg, 'mg', [R(src, '3')], vol=ml)
pw = lambda id, mg, label, src, route='iv': form(id, 'powder-for-injection', route, label, mg, 'mg', [R(src, '3')], per='vial')
fx = lambda id, dis, fa, en, pop, mg, refs, allowed=None, notes=None: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': mg, 'dosesPerDay': 1}, refs, dur=ONE, allowed=allowed, notes=notes)
TNF_W = lambda src: W('هشدار جعبه‌ای: عفونت‌های جدی (سل، قارچی تهاجمی، فرصت‌طلب) و بدخیمی (لنفوم، به‌ویژه در کودکان) — پیش از شروع تست سل نهفته و HBV.', 'Boxed warning: serious infections (TB, invasive fungal, opportunistic) and malignancy (lymphoma, especially in children) — test for latent TB and HBV first.', [R(src, 'Boxed Warning')])
TB = lambda src, sec='2.1': note('پیش از شروع: بررسی سل فعال و نهفته (درمان سل نهفته قبل از شروع) و واکسن‌های مناسب سن.', 'Before starting: screen for active and latent TB (treat latent TB first) and complete age-appropriate vaccines.', [R(src, sec)])

add_disease('lupus-nephritis', 'نفریت لوپوسی', 'Lupus nephritis', ['nephritis lupus', 'نفریت لوپوس', 'درگیری کلیه لوپوس'], ['M32.14'], 'rheumatology')
add_disease('giant-cell-arteritis', 'آرتریت سلول غول‌آسا (تمپورال)', 'Giant cell arteritis', ['GCA', 'آرتریت تمپورال', 'temporal arteritis'], ['M31.6'], 'rheumatology')
add_disease('cytokine-release-syndrome', 'سندرم آزادسازی سیتوکین (CRS)', 'Cytokine release syndrome', ['CRS', 'طوفان سیتوکین', 'سندرم رهایش سیتوکین'], ['D89.83'], 'oncology')
add_disease('caps', 'سندرم‌های تب دوره‌ای مرتبط با کرایوپیرین (CAPS/NOMID) و DIRA', 'Cryopyrin-associated periodic syndromes (CAPS/NOMID) and DIRA', ['CAPS', 'NOMID', 'DIRA', 'تب دوره‌ای'], ['M04.2'], 'rheumatology')

Pb = fda('probenecid', 'FDA Probenecid', 'Probenecid tablets USP 500 mg — Prescribing Information', sid('probenecid')); d = R(Pb, 'Dosage and Administration')
drug('probenecid', 'musculoskeletal', 'پروبنسید', 'Probenecid', T('اوریکوزوریک', 'Uricosuric'), [{'name': 'Probenecid', 'market': 'US'}], ['benemid', 'پروبنسید', 'probenecid'],
     [tab('tab-500', 500, '500 mg tablet (scored)', [R(Pb, 'How Supplied')], scored=True)],
     [reg('gout', 'gout', T('هیپراوریسمی نقرس (بین حملات) — ۲۵۰ mg دو بار یک هفته، سپس ۵۰۰ mg دو بار', 'Hyperuricaemia of gout (between attacks) — 250 mg twice daily for one week, then 500 mg twice daily'), A18, 'fixed', {'perDose': 250, 'perDoseMax': 500, 'dosesPerDay': 2}, [d],
          limits={'maxPerDay': 2000, 'refs': [d]}, notes=[note('تا حمله حاد فروکش نکرده شروع نشود. در صورت نیاز هر ۴ هفته ۵۰۰ mg/روز افزایش (معمولاً تا ۲۰۰۰ mg/روز). مایعات فراوان.', 'Do not start until an acute attack subsides. If needed, +500 mg/day every 4 weeks (usually up to 2000 mg/day). Plenty of fluids.', [d])])],
     [CI('ci', 'حساسیت؛ کودک زیر ۲ سال؛ دیسکرازی خونی یا سنگ اسید اوریک کلیه؛ شروع حین حمله حاد نقرس.', 'Hypersensitivity; children under 2; blood dyscrasias or uric acid kidney stones; starting during an acute gout attack.', [R(Pb, 'Contraindications')])],
     warn=[W('تشدید حمله نقرس؛ افزایش سطح متوترکسات؛ سالیسیلات‌ها اثر را خنثی می‌کنند.', 'Gout flare; raises methotrexate levels; salicylates antagonise the effect.', [R(Pb, 'Warnings')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('GFR ۳۰ یا کمتر: احتمالاً بی‌اثر.', 'GFR ≤30: may be ineffective.'), 'refs': [d]}],
     exs=[ex('gout', 'tab-500', {'perDose': 250, 'tabletsPerDoseRounded': 0.5, 'upperPerDose': 500}, ageYears=55, weightKg=85)])

Kx = fda('krystexxa', 'FDA Krystexxa', 'Krystexxa (pegloticase) injection — Prescribing Information', sid('pegloticase'))
drug('pegloticase', 'musculoskeletal', 'پگلوتیکاز', 'Pegloticase', T('اوریکاز پگیله', 'PEGylated uricase'), [{'name': 'Krystexxa', 'market': 'US'}], ['krystexxa', 'کریستکسا', 'پگلوتیکاز'],
     [inj('vial-8', 8, 1, '8 mg/mL vial (to be diluted)', Kx, route='iv')],
     [fx('gout', 'gout', 'نقرس مزمن مقاوم بزرگسال — ۸ mg انفوزیون وریدی هر ۲ هفته همراه متوترکسات ۱۵ mg هفتگی', 'Refractory chronic gout, adults — 8 mg IV infusion every 2 weeks with methotrexate 15 mg weekly', A18, 8, [R(Kx, '2.2')],
         notes=[note('متوترکسات و اسید فولیک دست‌کم ۴ هفته پیش از شروع. داروهای خوراکی کاهنده اسید اوریک قطع شود. پیش‌دارو آنتی‌هیستامین و کورتیکواستروئید. اسید اوریک پیش از هر انفوزیون (دو بار پیاپی بالای ۶ mg/dL: قطع).', 'Methotrexate and folic acid at least 4 weeks before. Stop oral urate-lowering drugs. Premedicate with antihistamine and corticosteroid. Check uric acid before each infusion (two consecutive >6 mg/dL: stop).', [R(Kx, '2.2'), R(Kx, '2'), R(Kx, 'Boxed Warning')])])],
     [CI('ci', 'کمبود G6PD؛ سابقه حساسیت جدی به پگلوتیکاز.', 'G6PD deficiency; prior serious hypersensitivity to pegloticase.', [R(Kx, '4')])],
     warn=[W('هشدار جعبه‌ای: آنافیلاکسی و واکنش انفوزیون (فقط در مرکز درمانی)؛ همولیز و مت‌هموگلوبینمی در کمبود G6PD — پیش از شروع تست G6PD.', 'Boxed warning: anaphylaxis and infusion reactions (healthcare setting only); haemolysis and methaemoglobinaemia in G6PD deficiency — screen for G6PD first.', [R(Kx, 'Boxed Warning')]),
           W('حمله نقرس در شروع؛ نارسایی قلب.', 'Gout flares at initiation; congestive heart failure.', [R(Kx, '5')])],
     exs=[ex('gout', 'vial-8', {'perDose': 8, 'mlPerDose': 1}, ageYears=55, weightKg=85)])

Bn = fda('benlysta', 'FDA Benlysta', 'Benlysta (belimumab) for injection and injection — Prescribing Information', sid('belimumab'))
drug('belimumab', 'antineoplastic-immunomodulating', 'بلیموماب', 'Belimumab', T('آنتی‌بادی ضد BLyS', 'Anti-BLyS antibody'), [{'name': 'Benlysta', 'market': 'US'}], ['benlysta', 'بنلیستا', 'بلیموماب'],
     [pw('vial-400', 400, '400 mg vial', Bn), pw('vial-120', 120, '120 mg vial', Bn), inj('ai-200', 200, 1, '200 mg/mL autoinjector or prefilled syringe', Bn)],
     [once('iv', 'lupus', 'لوپوس فعال یا نفریت لوپوسی (۵ سال به بالا) — ۱۰ mg/kg وریدی هر ۲ هفته برای ۳ دوز، سپس هر ۴ هفته', 'Active SLE or lupus nephritis (≥5 y) — 10 mg/kg IV every 2 weeks for 3 doses, then every 4 weeks', {'minAge': age(5, 'year')}, 10, None, [R(Bn, '2.2')],
           notes=[note('انفوزیون ۱ ساعته؛ پیش‌دارو برای واکنش انفوزیون در نظر گرفته شود.', '1-hour infusion; consider premedication for infusion reactions.', [R(Bn, '2.2')])], allowed=['vial-400', 'vial-120']),
      fx('sc', 'lupus', 'لوپوس فعال بزرگسال (زیرجلدی) — ۲۰۰ mg هفتگی', 'Active SLE, adults (SC) — 200 mg once weekly', A18, 200, [R(Bn, '2.3')], allowed=['ai-200'],
         notes=[note('کودک ۵ سال به بالا: ≥۴۰ kg ۲۰۰ mg هفتگی؛ ۱۵ تا <۴۰ kg ۲۰۰ mg هر ۲ هفته (فقط اتواینجکتور).', 'Children ≥5 y: ≥40 kg 200 mg weekly; 15–<40 kg 200 mg every 2 weeks (autoinjector only).', [R(Bn, '2.3')])]),
      fx('ln-sc', 'lupus-nephritis', 'نفریت لوپوسی بزرگسال (زیرجلدی) — ۴۰۰ mg هفتگی برای ۴ دوز، سپس ۲۰۰ mg هفتگی', 'Lupus nephritis, adults (SC) — 400 mg weekly for 4 doses, then 200 mg weekly', A18, 400, [R(Bn, '2.3')], allowed=['ai-200'])],
     [CI('ci', 'سابقه آنافیلاکسی، SJS یا TEN با بلیموماب.', 'Prior anaphylaxis, SJS or TEN with belimumab.', [R(Bn, '4')])],
     warn=[W('عفونت جدی؛ حساسیت و آنافیلاکسی (گاه تأخیری)؛ SJS/TEN؛ افسردگی و خودکشی؛ بدخیمی؛ واکسن زنده نه.', 'Serious infections; hypersensitivity and anaphylaxis (sometimes delayed); SJS/TEN; depression and suicidality; malignancy; no live vaccines.', [R(Bn, '5')])],
     exs=[ex('iv', 'vial-400', {'perDose': 700}, ageYears=35, weightKg=70), ex('sc', 'ai-200', {'perDose': 200, 'mlPerDose': 1}, ageYears=35, weightKg=70), ex('ln-sc', 'ai-200', {'perDose': 400, 'mlPerDose': 2}, ageYears=35, weightKg=70)])

Kn = fda('kineret', 'FDA Kineret', 'Kineret (anakinra) injection — Prescribing Information', sid('anakinra'))
drug('anakinra', 'antineoplastic-immunomodulating', 'آناکینرا', 'Anakinra', T('آنتاگونیست گیرنده IL-1', 'IL-1 receptor antagonist'), [{'name': 'Kineret', 'market': 'US'}], ['kineret', 'کینرت', 'آناکینرا'],
     [inj('pfs-100', 100, 0.67, '100 mg/0.67 mL graduated prefilled syringe (20–100 mg)', Kn)],
     [reg('ra', 'rheumatoid-arthritis', T('آرتریت روماتوئید بزرگسال — ۱۰۰ mg زیرجلدی روزانه', 'Rheumatoid arthritis, adults — 100 mg SC daily'), A18, 'fixed', {'perDose': 100, 'dosesPerDay': 1}, [R(Kn, '2.1')]),
      reg('caps', 'caps', T('NOMID/CAPS و DIRA — شروع ۱ تا ۲ mg/kg زیرجلدی روزانه (حداکثر ۸ mg/kg)', 'NOMID/CAPS and DIRA — start 1–2 mg/kg SC daily (max 8 mg/kg)'), {}, 'weightBased', {'perKgPerDose': 1, 'perKgPerDoseMax': 2, 'intervalHours': 24}, [R(Kn, '2.2'), R(Kn, '2.3')],
          notes=[note('تنظیم با گام ۰٫۵ تا ۱ mg/kg تا حداکثر ۸ mg/kg روزانه؛ می‌تواند در ۲ دوز. هر سرنگ یک بار.', 'Adjust in 0.5–1 mg/kg steps up to max 8 mg/kg daily; may be split twice daily. One syringe per dose.', [R(Kn, '2.2')])])],
     [CI('hyper', 'حساسیت به پروتئین‌های مشتق E. coli یا آناکینرا.', 'Hypersensitivity to E. coli-derived proteins or anakinra.', [R(Kn, '4')])],
     warn=[W('عفونت جدی؛ همراه مهارکننده TNF نه؛ حساسیت؛ نوتروپنی (شمارش نوتروفیل پایه، ماهانه ۳ ماه، سپس هر ۳ ماه)؛ واکسن زنده نه.', 'Serious infections; not with TNF blockers; hypersensitivity; neutropenia (ANC baseline, monthly for 3 months, then quarterly); no live vaccines.', [R(Kn, '5')])],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰ یا ESRD: همان دوز یک روز در میان.', 'CrCl <30 or ESRD: same dose every other day.'), 'refs': [R(Kn, '2.4')]}],
     exs=[ex('ra', 'pfs-100', {'perDose': 100, 'mlPerDose': 0.67}, ageYears=50, weightKg=70), ex('caps', 'pfs-100', {'perDose': 20, 'upperPerDose': 40}, ageYears=6, weightKg=20)])

Ac = fda('actemra', 'FDA Actemra', 'Actemra (tocilizumab) injection — Prescribing Information', sid('tocilizumab'))
TOC_N = note('شروع نکنید اگر ANC <۲۰۰۰، پلاکت <۱۰۰ هزار یا ALT/AST >۱٫۵ برابر حد بالا.', 'Do not start if ANC <2000, platelets <100,000 or ALT/AST >1.5× ULN.', [R(Ac, '2.1')])
drug('tocilizumab', 'antineoplastic-immunomodulating', 'توسیلیزوماب', 'Tocilizumab', T('آنتی‌بادی ضد گیرنده IL-6', 'Anti-IL-6 receptor antibody'), [{'name': 'Actemra', 'market': 'US'}], ['actemra', 'roactemra', 'اکتمرا', 'توسیلیزوماب'],
     [inj('vial-20', 20, 1, '20 mg/mL vial (80/200/400 mg) for IV infusion', Ac, route='iv'), inj('pfs-162', 162, 0.9, '162 mg/0.9 mL prefilled syringe or ACTPen', Ac)],
     [once('ra-iv', 'rheumatoid-arthritis', 'آرتریت روماتوئید بزرگسال (وریدی) — شروع ۴ mg/kg هر ۴ هفته؛ افزایش تا ۸ mg/kg', 'Rheumatoid arthritis, adults (IV) — start 4 mg/kg every 4 weeks; increase to 8 mg/kg', A18, 4, 8, [R(Ac, '2.2')], allowed=['vial-20'], notes=[TOC_N]),
      fx('ra-sc', 'rheumatoid-arthritis', 'آرتریت روماتوئید بزرگسال (زیرجلدی) — ۱۶۲ mg هر ۲ هفته (زیر ۱۰۰ kg؛ افزایش به هفتگی) یا هفتگی (۱۰۰ kg و بالاتر)', 'Rheumatoid arthritis, adults (SC) — 162 mg every other week (<100 kg; may increase to weekly) or weekly (≥100 kg)', A18, 162, [R(Ac, '2.2')], allowed=['pfs-162']),
      once('gca-iv', 'giant-cell-arteritis', 'آرتریت سلول غول‌آسا (وریدی) — ۶ mg/kg هر ۴ هفته همراه کاهش تدریجی گلوکوکورتیکوئید', 'Giant cell arteritis (IV) — 6 mg/kg every 4 weeks with tapering glucocorticoids', A18, 6, None, [R(Ac, '2.3')], allowed=['vial-20']),
      fx('gca-sc', 'giant-cell-arteritis', 'آرتریت سلول غول‌آسا (زیرجلدی) — ۱۶۲ mg هفتگی همراه کاهش گلوکوکورتیکوئید', 'Giant cell arteritis (SC) — 162 mg weekly with tapering glucocorticoids', A18, 162, [R(Ac, '2.3')], allowed=['pfs-162']),
      once('pjia-s', 'juvenile-arthritis', 'JIA پلی‌آرتیکولار (وریدی) — زیر ۳۰ kg: ۱۰ mg/kg هر ۴ هفته', 'Polyarticular JIA (IV) — <30 kg: 10 mg/kg every 4 weeks', {'minAge': age(2, 'year'), 'maxWeightKg': 29.99}, 10, None, [R(Ac, '2.5')], allowed=['vial-20']),
      once('pjia-l', 'juvenile-arthritis', 'JIA پلی‌آرتیکولار (وریدی) — ۳۰ kg و بالاتر: ۸ mg/kg هر ۴ هفته', 'Polyarticular JIA (IV) — ≥30 kg: 8 mg/kg every 4 weeks', {'minAge': age(2, 'year'), 'minWeightKg': 30}, 8, None, [R(Ac, '2.5')], allowed=['vial-20']),
      once('sjia-s', 'juvenile-arthritis', 'JIA سیستمیک (وریدی) — زیر ۳۰ kg: ۱۲ mg/kg هر ۲ هفته', 'Systemic JIA (IV) — <30 kg: 12 mg/kg every 2 weeks', {'minAge': age(2, 'year'), 'maxWeightKg': 29.99}, 12, None, [R(Ac, '2.6')], allowed=['vial-20']),
      once('sjia-l', 'juvenile-arthritis', 'JIA سیستمیک (وریدی) — ۳۰ kg و بالاتر: ۸ mg/kg هر ۲ هفته', 'Systemic JIA (IV) — ≥30 kg: 8 mg/kg every 2 weeks', {'minAge': age(2, 'year'), 'minWeightKg': 30}, 8, None, [R(Ac, '2.6')], allowed=['vial-20']),
      once('crs-s', 'cytokine-release-syndrome', 'سندرم آزادسازی سیتوکین (۲ سال به بالا) — زیر ۳۰ kg: ۱۲ mg/kg انفوزیون ۶۰ دقیقه', 'Cytokine release syndrome (≥2 y) — <30 kg: 12 mg/kg over 60 min', {'minAge': age(2, 'year'), 'maxWeightKg': 29.99}, 12, None, [R(Ac, '2.7')], allowed=['vial-20'],
           notes=[note('اگر بهبود نیافت تا ۳ دوز دیگر با فاصله دست‌کم ۸ ساعت. فقط وریدی.', 'If no improvement, up to 3 more doses at least 8 h apart. IV only.', [R(Ac, '2.7')])]),
      once('crs-l', 'cytokine-release-syndrome', 'سندرم آزادسازی سیتوکین — ۳۰ kg و بالاتر: ۸ mg/kg انفوزیون ۶۰ دقیقه', 'Cytokine release syndrome — ≥30 kg: 8 mg/kg over 60 min', {'minAge': age(2, 'year'), 'minWeightKg': 30}, 8, None, [R(Ac, '2.7')], allowed=['vial-20']),
      once('covid', 'covid-19', 'COVID-19 بستری با کورتیکواستروئید و اکسیژن — ۳۰ kg و بالاتر: ۸ mg/kg یک انفوزیون ۶۰ دقیقه', 'Hospitalised COVID-19 on corticosteroids and oxygen — ≥30 kg: 8 mg/kg single 60-min infusion', {'minAge': age(2, 'year'), 'minWeightKg': 30}, 8, None, [R(Ac, '2.8')], allowed=['vial-20'],
           notes=[note('زیر ۳۰ kg: ۱۲ mg/kg. اگر بدتر شد یک انفوزیون دیگر دست‌کم ۸ ساعت بعد.', '<30 kg: 12 mg/kg. If worse or no improvement, one more infusion at least 8 h later.', [R(Ac, '2.8')])])],
     [CI('hyper', 'حساسیت شناخته‌شده به توسیلیزوماب.', 'Known hypersensitivity to tocilizumab.', [R(Ac, '4')])],
     warn=[W('هشدار جعبه‌ای: عفونت‌های جدی (سل، قارچی، فرصت‌طلب) — در عفونت جدی قطع.', 'Boxed warning: serious infections (TB, fungal, opportunistic) — interrupt for serious infection.', [R(Ac, 'Boxed Warning')]),
           W('سوراخ‌شدگی گوارشی؛ سمیت کبدی؛ نوتروپنی، ترومبوسیتوپنی و افزایش چربی خون؛ بیماری دمیلینه‌کننده.', 'GI perforation; hepatotoxicity; neutropenia, thrombocytopenia and lipid elevation; demyelinating disorders.', [R(Ac, '5')])],
     exs=[ex('ra-iv', 'vial-20', {'perDose': 280, 'mlPerDose': 14, 'upperPerDose': 560}, ageYears=50, weightKg=70), ex('ra-sc', 'pfs-162', {'perDose': 162, 'mlPerDose': 0.9}, ageYears=50, weightKg=70),
          ex('gca-iv', 'vial-20', {'perDose': 420, 'mlPerDose': 21}, ageYears=70, weightKg=70), ex('gca-sc', 'pfs-162', {'perDose': 162, 'mlPerDose': 0.9}, ageYears=70, weightKg=70),
          ex('pjia-s', 'vial-20', {'perDose': 200, 'mlPerDose': 10}, ageYears=6, weightKg=20), ex('pjia-l', 'vial-20', {'perDose': 320, 'mlPerDose': 16}, ageYears=12, weightKg=40),
          ex('sjia-s', 'vial-20', {'perDose': 240, 'mlPerDose': 12}, ageYears=6, weightKg=20), ex('sjia-l', 'vial-20', {'perDose': 320, 'mlPerDose': 16}, ageYears=12, weightKg=40),
          ex('crs-s', 'vial-20', {'perDose': 240, 'mlPerDose': 12}, ageYears=6, weightKg=20), ex('crs-l', 'vial-20', {'perDose': 560, 'mlPerDose': 28}, ageYears=40, weightKg=70), ex('covid', 'vial-20', {'perDose': 560, 'mlPerDose': 28}, ageYears=60, weightKg=70)])

Or = fda('orencia', 'FDA Orencia', 'Orencia (abatacept) for injection and injection — Prescribing Information', sid('abatacept'))
drug('abatacept', 'antineoplastic-immunomodulating', 'آباتاسپت', 'Abatacept', T('تعدیل‌کننده هم‌تحریکی سلول T', 'T-cell co-stimulation modulator'), [{'name': 'Orencia', 'market': 'US'}], ['orencia', 'اورنسیا', 'آباتاسپت'],
     [pw('vial-250', 250, '250 mg vial', Or), inj('pfs-125', 125, 1, '125 mg/mL prefilled syringe or ClickJect', Or)],
     [reg('ra-iv', 'rheumatoid-arthritis', T('آرتریت روماتوئید یا پسوریاتیک بزرگسال (وریدی) — هفته ۰، ۲، ۴ و سپس هر ۴ هفته؛ زیر ۶۰ kg: ۵۰۰، ۶۰ تا ۱۰۰: ۷۵۰، بالای ۱۰۰: ۱۰۰۰ mg', 'RA or PsA, adults (IV) — weeks 0, 2, 4 then every 4 weeks; <60 kg: 500, 60–100: 750, >100: 1000 mg'), A18, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 59.99, 'perDose': 500, 'dosesPerDay': 1}, {'minWeightKg': 60, 'maxWeightKg': 100, 'perDose': 750, 'dosesPerDay': 1}, {'minWeightKg': 100.01, 'maxWeightKg': None, 'perDose': 1000, 'dosesPerDay': 1}]}, [R(Or, '2')], dur=ONE, allowed=['vial-250'],
          notes=[note('انفوزیون ۳۰ دقیقه. همراه مهارکننده JAK یا داروی بیولوژیک (مثل ضد TNF) نه.', '30-minute infusion. Not with JAK inhibitors or biologic DMARDs (e.g. TNF antagonists).', [R(Or, '2'), R(Or, '2.1')])]),
      fx('ra-sc', 'rheumatoid-arthritis', 'آرتریت روماتوئید یا پسوریاتیک بزرگسال (زیرجلدی) — ۱۲۵ mg هفتگی', 'RA or PsA, adults (SC) — 125 mg once weekly', A18, 125, [R(Or, '2')], allowed=['pfs-125'],
         notes=[note('بارگذاری وریدی اختیاری بر اساس وزن پیش از اولین دوز زیرجلدی.', 'Optional weight-based IV loading dose before the first SC dose.', [R(Or, '2')])])],
     warn=[W('عفونت (بیشتر با ضد TNF همزمان)؛ حساسیت؛ واکسن زنده نه؛ عوارض بیشتر در COPD؛ فعال شدن CMV و EBV در پیوند.', 'Infections (more with concurrent TNF antagonists); hypersensitivity; no live vaccines; more adverse effects in COPD; CMV/EBV reactivation in transplant.', [R(Or, '5')])],
     exs=[ex('ra-iv', 'vial-250', {'perDose': 500}, ageYears=50, weightKg=55), ex('ra-iv', 'vial-250', {'perDose': 750}, ageYears=50, weightKg=80), ex('ra-iv', 'vial-250', {'perDose': 1000}, ageYears=50, weightKg=110),
          ex('ra-sc', 'pfs-125', {'perDose': 125, 'mlPerDose': 1}, ageYears=50, weightKg=70)])

Cz = fda('cimzia', 'FDA Cimzia', 'Cimzia (certolizumab pegol) — Prescribing Information', sid('certolizumab'))
drug('certolizumab', 'antineoplastic-immunomodulating', 'سرتولیزوماب پگول', 'Certolizumab pegol', T('مهارکننده TNF', 'TNF blocker'), [{'name': 'Cimzia', 'market': 'US'}], ['cimzia', 'سیمزیا', 'سرتولیزوماب'],
     [inj('pfs-200', 200, 1, '200 mg/mL prefilled syringe', Cz)],
     [fx('load', 'rheumatoid-arthritis', 'بارگذاری (آرتریت روماتوئید، پسوریاتیک، اسپوندیلیت، کرون) — ۴۰۰ mg (دو تزریق ۲۰۰) هفته ۰، ۲ و ۴', 'Loading (RA, PsA, axSpA, Crohn) — 400 mg (two 200 mg injections) at weeks 0, 2 and 4', A18, 400, [R(Cz, '2.2'), R(Cz, '2.1'), R(Cz, '2.4'), R(Cz, '2.5')], notes=[TB(Cz, '2.10')]),
      fx('ra', 'rheumatoid-arthritis', 'نگهدارنده آرتریت روماتوئید یا پسوریاتیک — ۲۰۰ mg هر ۲ هفته (یا ۴۰۰ mg هر ۴ هفته)', 'Maintenance RA or PsA — 200 mg every 2 weeks (or 400 mg every 4 weeks)', A18, 200, [R(Cz, '2.2'), R(Cz, '2.4')]),
      fx('as', 'ankylosing-spondylitis', 'نگهدارنده اسپوندیلیت آنکیلوزان یا axSpA غیررادیوگرافیک — ۲۰۰ mg هر ۲ هفته یا ۴۰۰ mg هر ۴ هفته', 'Maintenance AS or non-radiographic axSpA — 200 mg every 2 weeks or 400 mg every 4 weeks', A18, 200, [R(Cz, '2.5'), R(Cz, '2.6')]),
      fx('cd', 'crohns', 'نگهدارنده کرون — ۴۰۰ mg هر ۴ هفته', 'Maintenance Crohn disease — 400 mg every 4 weeks', A18, 400, [R(Cz, '2.1')]),
      fx('pso', 'psoriasis', 'پسوریازیس پلاک متوسط تا شدید — ۴۰۰ mg هر ۲ هفته', 'Moderate–severe plaque psoriasis — 400 mg every other week', A18, 400, [R(Cz, '2.7')],
         notes=[note('وزن ۹۰ kg یا کمتر: می‌توان ۴۰۰ mg هفته ۰، ۲، ۴ سپس ۲۰۰ mg هر ۲ هفته.', '≤90 kg: may use 400 mg at weeks 0, 2, 4 then 200 mg every other week.', [R(Cz, '2.7')])]),
      reg('pjia', 'juvenile-arthritis', T('JIA پلی‌آرتیکولار (۲ سال به بالا) — نگهدارنده از هفته ۶ هر ۲ هفته بر اساس وزن', 'Polyarticular JIA (≥2 y) — maintenance from week 6 every 2 weeks by weight'), {'minAge': age(2, 'year'), 'minWeightKg': 10}, 'weightBand',
          {'weightBands': [{'minWeightKg': 10, 'maxWeightKg': 19.99, 'perDose': 50, 'dosesPerDay': 1}, {'minWeightKg': 20, 'maxWeightKg': 39.99, 'perDose': 100, 'dosesPerDay': 1}, {'minWeightKg': 40, 'maxWeightKg': None, 'perDose': 200, 'dosesPerDay': 1}]}, [R(Cz, '2.3')], dur=ONE,
          notes=[note('بارگذاری هفته ۰، ۲، ۴: ۱۰ تا <۲۰ kg: ۱۰۰؛ ۲۰ تا <۴۰: ۲۰۰؛ ≥۴۰: ۴۰۰ mg.', 'Loading at weeks 0, 2, 4: 10–<20 kg: 100; 20–<40: 200; ≥40: 400 mg.', [R(Cz, '2.3')])])],
     [CI('hyper', 'حساسیت جدی به سرتولیزوماب (آنژیوادم، آنافیلاکسی، بیماری سرم).', 'Serious hypersensitivity to certolizumab (angioedema, anaphylaxis, serum sickness).', [R(Cz, '4')])],
     warn=[TNF_W(Cz), W('نارسایی قلب؛ فعال شدن HBV؛ بیماری دمیلینه‌کننده؛ سیتوپنی؛ سندرم شبه‌لوپوس؛ همراه داروهای بیولوژیک دیگر نه.', 'Heart failure; HBV reactivation; demyelinating disease; cytopenias; lupus-like syndrome; not with other biologics.', [R(Cz, '5')])],
     exs=[ex('load', 'pfs-200', {'perDose': 400, 'mlPerDose': 2}, ageYears=45, weightKg=70), ex('ra', 'pfs-200', {'perDose': 200, 'mlPerDose': 1}, ageYears=45, weightKg=70), ex('as', 'pfs-200', {'perDose': 200, 'mlPerDose': 1}, ageYears=35, weightKg=70),
          ex('cd', 'pfs-200', {'perDose': 400, 'mlPerDose': 2}, ageYears=35, weightKg=70), ex('pso', 'pfs-200', {'perDose': 400, 'mlPerDose': 2}, ageYears=35, weightKg=95), ex('pjia', 'pfs-200', {'perDose': 100, 'mlPerDose': 0.5}, ageYears=8, weightKg=25)])

Sm = fda('simponi', 'FDA Simponi', 'Simponi (golimumab) injection — Prescribing Information', sid('golimumab'))
drug('golimumab', 'antineoplastic-immunomodulating', 'گولیموماب', 'Golimumab', T('مهارکننده TNF', 'TNF blocker'), [{'name': 'Simponi', 'market': 'US'}], ['simponi', 'سیمپونی', 'گولیموماب'],
     [inj('pfs-50', 50, 0.5, '50 mg/0.5 mL syringe or SmartJect', Sm), inj('pfs-100', 100, 1, '100 mg/mL syringe or SmartJect', Sm)],
     [fx('ra', 'rheumatoid-arthritis', 'آرتریت روماتوئید (با متوترکسات)، پسوریاتیک یا اسپوندیلیت آنکیلوزان بزرگسال — ۵۰ mg زیرجلدی ماهانه', 'RA (with methotrexate), PsA or AS, adults — 50 mg SC once a month', A18, 50, [R(Sm, '2.2')], allowed=['pfs-50'], notes=[TB(Sm)]),
      reg('uc', 'ulcerative-colitis', T('کولیت اولسراتیو (≥۱۵ kg) — نگهدارنده از هفته ۶ هر ۴ هفته بر اساس وزن', 'Ulcerative colitis (≥15 kg) — maintenance from week 6 every 4 weeks by weight'), {'minWeightKg': 15}, 'weightBand',
          {'weightBands': [{'minWeightKg': 15, 'maxWeightKg': 39.99, 'perDose': 50, 'dosesPerDay': 1}, {'minWeightKg': 40, 'maxWeightKg': None, 'perDose': 100, 'dosesPerDay': 1}]}, [R(Sm, '2.3, Table 1')], dur=ONE,
          notes=[note('القا: ≥۴۰ kg: ۲۰۰ mg هفته ۰ و ۱۰۰ mg هفته ۲؛ ۱۵ تا <۴۰ kg: ۱۰۰ و ۵۰ mg.', 'Induction: ≥40 kg: 200 mg week 0 and 100 mg week 2; 15–<40 kg: 100 and 50 mg.', [R(Sm, '2.3, Table 1')])])],
     warn=[TNF_W(Sm), W('نارسایی قلب؛ دمیلینه شدن؛ فعال شدن HBV؛ سیتوپنی؛ همراه آباتاسپت یا آناکینرا نه.', 'Heart failure; demyelination; HBV reactivation; cytopenias; not with abatacept or anakinra.', [R(Sm, '5')])],
     exs=[ex('ra', 'pfs-50', {'perDose': 50, 'mlPerDose': 0.5}, ageYears=45, weightKg=70), ex('uc', 'pfs-100', {'perDose': 100, 'mlPerDose': 1}, ageYears=35, weightKg=70), ex('uc', 'pfs-50', {'perDose': 50, 'mlPerDose': 0.5}, ageYears=10, weightKg=30)])

Tl = fda('taltz', 'FDA Taltz', 'Taltz (ixekizumab) injection — Prescribing Information', sid('ixekizumab'))
drug('ixekizumab', 'antineoplastic-immunomodulating', 'ایکسکیزوماب', 'Ixekizumab', T('آنتی‌بادی ضد IL-17A', 'Anti-IL-17A antibody'), [{'name': 'Taltz', 'market': 'US'}], ['taltz', 'تالتز', 'ایکسکیزوماب'],
     [inj('ai-80', 80, 1, '80 mg/mL autoinjector or syringe', Tl), inj('pfs-40', 40, 0.5, '40 mg/0.5 mL syringe', Tl)],
     [fx('pso', 'psoriasis', 'پسوریازیس پلاک بزرگسال — ۱۶۰ mg هفته ۰، سپس ۸۰ mg هفته ۲ تا ۱۲ هر ۲ هفته، سپس ۸۰ mg هر ۴ هفته', 'Plaque psoriasis, adults — 160 mg at week 0, then 80 mg every 2 weeks to week 12, then 80 mg every 4 weeks', A18, 80, [R(Tl, '2.2')], allowed=['ai-80'], notes=[TB(Tl)]),
      reg('pso-child', 'psoriasis', T('پسوریازیس پلاک کودک ۶ سال به بالا — هر ۴ هفته: ۲۵ تا ۵۰ kg: ۴۰ mg؛ بالای ۵۰ kg: ۸۰ mg', 'Plaque psoriasis, children ≥6 y — every 4 weeks: 25–50 kg: 40 mg; >50 kg: 80 mg'), {'minAge': age(6, 'year'), 'maxAge': age(18, 'year'), 'minWeightKg': 25}, 'weightBand',
          {'weightBands': [{'minWeightKg': 25, 'maxWeightKg': 50, 'perDose': 40, 'dosesPerDay': 1}, {'minWeightKg': 50.01, 'maxWeightKg': None, 'perDose': 80, 'dosesPerDay': 1}]}, [R(Tl, '2.3, Table 1')], dur=ONE,
          notes=[note('دوز شروع (هفته ۰): ۲۵ تا ۵۰ kg: ۸۰ mg؛ بالای ۵۰ kg: ۱۶۰ mg.', 'Starting dose (week 0): 25–50 kg: 80 mg; >50 kg: 160 mg.', [R(Tl, '2.3, Table 1')])]),
      fx('psa', 'psoriatic-arthritis', 'آرتریت پسوریاتیک — ۱۶۰ mg هفته ۰، سپس ۸۰ mg هر ۴ هفته', 'Psoriatic arthritis — 160 mg at week 0, then 80 mg every 4 weeks', A18, 80, [R(Tl, '2.4')], allowed=['ai-80']),
      fx('as', 'ankylosing-spondylitis', 'اسپوندیلیت آنکیلوزان — ۱۶۰ mg هفته ۰، سپس ۸۰ mg هر ۴ هفته (nr-axSpA: ۸۰ mg هر ۴ هفته)', 'Ankylosing spondylitis — 160 mg at week 0, then 80 mg every 4 weeks (nr-axSpA: 80 mg every 4 weeks)', A18, 80, [R(Tl, '2.5'), R(Tl, '2.6')], allowed=['ai-80'])],
     [CI('hyper', 'حساسیت جدی به ایکسکیزوماب.', 'Serious hypersensitivity to ixekizumab.', [R(Tl, '4')])],
     warn=[W('عفونت؛ سل (پیش از شروع بررسی)؛ حساسیت؛ ضایعات اگزمایی؛ بیماری التهابی روده (شروع یا تشدید)؛ واکسن زنده نه.', 'Infections; TB (screen first); hypersensitivity; eczematous eruptions; inflammatory bowel disease (new or worse); no live vaccines.', [R(Tl, '5')])],
     exs=[ex('pso', 'ai-80', {'perDose': 80, 'mlPerDose': 1}, ageYears=40, weightKg=80), ex('pso-child', 'pfs-40', {'perDose': 40, 'mlPerDose': 0.5}, ageYears=10, weightKg=35), ex('pso-child', 'ai-80', {'perDose': 80, 'mlPerDose': 1}, ageYears=15, weightKg=60),
          ex('psa', 'ai-80', {'perDose': 80, 'mlPerDose': 1}, ageYears=45, weightKg=80), ex('as', 'ai-80', {'perDose': 80, 'mlPerDose': 1}, ageYears=35, weightKg=75)])
print('s12f1 ok')
