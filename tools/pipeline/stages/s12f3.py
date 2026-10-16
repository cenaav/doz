"""Stage 12f (part 3) — urology (alfuzosin, silodosin, darifenacin, trospium, vibegron), dermatology (acitretin, tazarotene, efinaconazole, tavaborole) and eye (bimatoprost, travoprost, pilocarpine, lifitegrast, ranibizumab, aflibercept)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's12_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
NC = lambda id, dis, fa, en, pop, rfa, ren, refs: reg(id, dis, T(fa, en), pop, 'notCalculated', {'reason': T(rfa, ren)}, refs)
cap = lambda id, mg, src, label=None, sec='3': tab(id, mg, label or f'{mg} mg capsule', [R(src, sec)], per='capsule', form_='capsule')
drops = lambda label, src: form('drops', 'eye-drops', 'ophthalmic', label, 1, 'drop', [R(src, '3')], per='drop')
drop_reg = lambda id, dis, fa, en, n, refs, pop=A18, notes=None: reg(id, dis, T(fa, en), pop, 'fixed', {'perDose': 1, 'dosesPerDay': n}, refs, unit='drop', notes=notes)
ivt = lambda id, mg, label, src: form(id, 'injection', 'ophthalmic', label, mg, 'mg', [R(src, '3')], per='vial')
ANTIM_CI = lambda src, extra_fa='', extra_en='': CI('ci', 'احتباس ادرار؛ احتباس معده؛ گلوکوم زاویه بسته کنترل‌نشده' + extra_fa + '.', 'Urinary retention; gastric retention; uncontrolled narrow-angle glaucoma' + extra_en + '.', [R(src, '4')])
ANTIM_W = lambda src: W('احتباس ادرار (به‌ویژه با انسداد خروجی مثانه)؛ آنژیوادم؛ کاهش حرکات گوارش؛ عوارض CNS (گیجی، خواب‌آلودگی).', 'Urinary retention (especially with bladder outlet obstruction); angioedema; decreased GI motility; CNS effects (confusion, somnolence).', [R(src, '5')])
ALPHA_W = lambda src: W('افت فشار وضعیتی و سنکوپ؛ سرطان پروستات پیش از شروع رد شود؛ سندرم عنبیه شل حین جراحی آب مروارید (IFIS).', 'Postural hypotension and syncope; exclude prostate cancer first; intraoperative floppy iris syndrome (IFIS) in cataract surgery.', [R(src, '5')])
PGA_W = lambda src: W('افزایش رنگدانه عنبیه (دائمی)، پلک و تغییر مژه؛ التهاب داخل چشم؛ ادم ماکولا.', 'Increased iris (permanent), eyelid pigmentation and eyelash changes; intraocular inflammation; macular oedema.', [R(src, '5')])
VEGF_CI = lambda src: CI('ci', 'عفونت چشم یا اطراف چشم؛ التهاب فعال داخل چشم؛ حساسیت.', 'Ocular or periocular infection; active intraocular inflammation; hypersensitivity.', [R(src, '4')])
VEGF_W = lambda src: W('اندوفتالمیت و جداشدگی شبکیه پس از تزریق؛ افزایش فشار چشم؛ رویدادهای ترومبوآمبولیک شریانی.', 'Endophthalmitis and retinal detachment after injection; raised intraocular pressure; arterial thromboembolic events.', [R(src, '5')])

add_disease('wet-amd', 'دژنراسیون ماکولای وابسته به سن نوع مرطوب (نئوواسکولار)', 'Neovascular (wet) age-related macular degeneration', ['wet AMD', 'AMD', 'دژنراسیون ماکولا', 'ماکولار دژنراسیون'], ['H35.32'], 'ophthalmology')
add_disease('diabetic-macular-edema', 'ادم ماکولای دیابتی و رتینوپاتی دیابتی', 'Diabetic macular oedema and diabetic retinopathy', ['DME', 'رتینوپاتی دیابتی', 'ادم ماکولا دیابتی'], ['E11.311'], 'ophthalmology')
add_disease('retinal-vein-occlusion', 'ادم ماکولا پس از انسداد ورید شبکیه', 'Macular oedema after retinal vein occlusion', ['RVO', 'انسداد ورید شبکیه', 'ترومبوز ورید شبکیه'], ['H34.8'], 'ophthalmology')
add_disease('presbyopia', 'پیرچشمی', 'Presbyopia', ['presbyopia', 'پیرچشمی', 'ضعف دید نزدیک'], ['H52.4'], 'ophthalmology')

# ===================== urology =====================
Af = fda('alfuzosin', 'FDA Alfuzosin ER', 'Alfuzosin HCl extended-release tablets 10 mg (Apotex) — Prescribing Information', sid('alfuzosin'))
drug('alfuzosin', 'genitourinary-sex-hormones', 'آلفوزوسین', 'Alfuzosin', T('آلفا-۱ بلاکر', 'Alpha-1 blocker'), [{'name': 'Uroxatral', 'market': 'US'}], ['uroxatral', 'xatral', 'زاترال', 'آلفوزوسین'],
     [tab('er-10', 10, '10 mg extended-release tablet (do not crush)', [R(Af, '3')])],
     [reg('bph', 'bph', T('علائم هیپرپلازی خوش‌خیم پروستات — ۱۰ mg یک بار، پس از همان وعده غذایی هر روز', 'Symptoms of benign prostatic hyperplasia — 10 mg once daily after the same meal each day'), A18, 'fixed', {'perDose': 10, 'dosesPerDay': 1}, [R(Af, '2')],
          notes=[note('ناشتا جذب ۵۰٪ کمتر است. قرص جویده یا خرد نشود.', 'Absorption is 50% lower fasting. Do not chew or crush.', [R(Af, '2')])])],
     [CI('ci', 'نارسایی متوسط یا شدید کبد؛ مهارکننده‌های قوی CYP3A4 (کتوکونازول، ایتراکونازول، ریتوناویر)؛ حساسیت.', 'Moderate or severe hepatic impairment; potent CYP3A4 inhibitors (ketoconazole, itraconazole, ritonavir); hypersensitivity.', [R(Af, '4')])],
     warn=[ALPHA_W(Af), W('پریاپیسم؛ نارسایی کرونری؛ QT طولانی مادرزادی یا اکتسابی؛ نارسایی شدید کلیه با احتیاط.', 'Priapism; coronary insufficiency; congenital or acquired QT prolongation; caution in severe renal impairment.', [R(Af, '5')])],
     exs=[ex('bph', 'er-10', {'perDose': 10, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

Sd = fda('silodosin', 'FDA Silodosin', 'Silodosin capsules 4/8 mg — Prescribing Information', sid('silodosin'))
drug('silodosin', 'genitourinary-sex-hormones', 'سیلودوزین', 'Silodosin', T('آلفا-۱A بلاکر', 'Alpha-1A blocker'), [{'name': 'Rapaflo', 'market': 'US'}], ['rapaflo', 'رپافلو', 'urorec', 'سیلودوزین'],
     [cap('cap-8', 8, Sd), cap('cap-4', 4, Sd)],
     [reg('bph', 'bph', T('علائم هیپرپلازی خوش‌خیم پروستات — ۸ mg یک بار با غذا', 'Symptoms of benign prostatic hyperplasia — 8 mg once daily with a meal'), A18, 'fixed', {'perDose': 8, 'dosesPerDay': 1}, [R(Sd, '2.1')], allowed=['cap-8'],
          notes=[note('در مشکل بلع می‌توان کپسول را باز و روی پوره سیب ریخت.', 'If swallowing is difficult, the capsule may be opened onto applesauce.', [R(Sd, '2.1')])])],
     [CI('ci', 'نارسایی شدید کلیه (ClCr زیر ۳۰)؛ نارسایی شدید کبد (Child-Pugh ≥۱۰)؛ مهارکننده‌های قوی CYP3A4؛ حساسیت.', 'Severe renal impairment (CrCl <30); severe hepatic impairment (Child-Pugh ≥10); strong CYP3A4 inhibitors; hypersensitivity.', [R(Sd, '4')])],
     warn=[ALPHA_W(Sd)],
     renal=[{'egfrBelow': 50, 'severity': 'warn', 'text': T('ClCr ۳۰ تا ۵۰: ۴ mg یک بار؛ زیر ۳۰ منع مصرف.', 'CrCl 30–50: 4 mg once daily; below 30 contraindicated.'), 'refs': [R(Sd, '2.2')]}],
     exs=[ex('bph', 'cap-8', {'perDose': 8, 'tabletsPerDoseRounded': 1}, ageYears=65, weightKg=75)])

Dr = fda('darifenacin', 'FDA Darifenacin ER', 'Darifenacin extended-release tablets 7.5/15 mg — Prescribing Information', sid('darifenacin'))
drug('darifenacin', 'genitourinary-sex-hormones', 'داریفناسین', 'Darifenacin', T('آنتی‌موسکارینی M3', 'M3 antimuscarinic'), [{'name': 'Enablex', 'market': 'US'}], ['enablex', 'emselex', 'داریفناسین'],
     [tab('er-7-5', 7.5, '7.5 mg extended-release tablet', [R(Dr, '3')]), tab('er-15', 15, '15 mg extended-release tablet', [R(Dr, '3')])],
     [reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال بزرگسال — ۷٫۵ mg یک بار؛ پس از ۲ هفته تا ۱۵ mg', 'Overactive bladder, adults — 7.5 mg once daily; after 2 weeks up to 15 mg'), A18, 'fixed', {'perDose': 7.5, 'perDoseMax': 15, 'dosesPerDay': 1}, [R(Dr, '2')],
          notes=[note('کامل بلعیده شود. نارسایی متوسط کبد یا مهارکننده قوی CYP3A4: حداکثر ۷٫۵ mg؛ نارسایی شدید کبد توصیه نمی‌شود.', 'Swallow whole. Moderate hepatic impairment or potent CYP3A4 inhibitors: max 7.5 mg; severe hepatic impairment not recommended.', [R(Dr, '2')])])],
     [ANTIM_CI(Dr)], warn=[ANTIM_W(Dr)],
     exs=[ex('oab', 'er-7-5', {'perDose': 7.5, 'tabletsPerDoseRounded': 1, 'upperPerDose': 15}, ageYears=60, weightKg=70)])

Ts = fda('trospium', 'FDA Trospium', 'Trospium chloride tablets 20 mg — Prescribing Information', sid('trospium'))
drug('trospium', 'genitourinary-sex-hormones', 'تروسپیوم', 'Trospium', T('آنتی‌موسکارینی (آمین چهارتایی)', 'Quaternary-amine antimuscarinic'), [{'name': 'Sanctura', 'market': 'US'}], ['sanctura', 'spasmex', 'تروسپیوم'],
     [tab('tab-20', 20, '20 mg tablet', [R(Ts, '3')])],
     [reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال بزرگسال — ۲۰ mg دو بار، دست‌کم ۱ ساعت پیش از غذا', 'Overactive bladder, adults — 20 mg twice daily, at least 1 h before meals'), A18, 'fixed', {'perDose': 20, 'dosesPerDay': 2}, [R(Ts, '2')],
          notes=[note('۷۵ سال به بالا: بر اساس تحمل تا ۲۰ mg یک بار.', '≥75 y: may reduce to 20 mg once daily by tolerability.', [R(Ts, '2')])])],
     [ANTIM_CI(Ts, '؛ حساسیت', '; hypersensitivity')], warn=[ANTIM_W(Ts)],
     renal=[{'egfrBelow': 30, 'severity': 'warn', 'text': T('ClCr زیر ۳۰: ۲۰ mg یک بار هنگام خواب.', 'CrCl <30: 20 mg once daily at bedtime.'), 'refs': [R(Ts, '2')]}],
     exs=[ex('oab', 'tab-20', {'perDose': 20, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Gm = fda('gemtesa', 'FDA Gemtesa', 'Gemtesa (vibegron) tablets 75 mg — Prescribing Information', sid('vibegron'))
drug('vibegron', 'genitourinary-sex-hormones', 'ویبگرون', 'Vibegron', T('آگونیست بتا-۳', 'Beta-3 adrenergic agonist'), [{'name': 'Gemtesa', 'market': 'US'}], ['gemtesa', 'جمتسا', 'ویبگرون'],
     [tab('tab-75', 75, '75 mg tablet', [R(Gm, '3')])],
     [reg('oab', 'overactive-bladder', T('مثانه بیش‌فعال بزرگسال — ۷۵ mg یک بار', 'Overactive bladder, adults — 75 mg once daily'), A18, 'fixed', {'perDose': 75, 'dosesPerDay': 1}, [R(Gm, '2.1')],
          notes=[note('با یا بدون غذا؛ در بزرگسال می‌توان خرد کرد و با پوره سیب داد.', 'With or without food; in adults may be crushed into applesauce.', [R(Gm, '2.1')])])],
     [CI('hyper', 'حساسیت به ویبگرون (آنژیوادم).', 'Hypersensitivity to vibegron (angioedema).', [R(Gm, '4')])],
     warn=[W('احتباس ادرار (به‌ویژه با انسداد خروجی یا همراه آنتی‌موسکارینی)؛ آنژیوادم.', 'Urinary retention (especially with outlet obstruction or with antimuscarinics); angioedema.', [R(Gm, '5')])],
     exs=[ex('oab', 'tab-75', {'perDose': 75, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

# ===================== dermatology =====================
Ac = fda('acitretin', 'FDA Acitretin', 'Acitretin capsules USP 10/17.5/25 mg — Prescribing Information', sid('acitretin')); d = R(Ac, 'Dosage and Administration')
drug('acitretin', 'dermatology', 'آسیترتین', 'Acitretin', T('رتینوئید سیستمیک', 'Systemic retinoid'), [{'name': 'Soriatane', 'market': 'US'}], ['soriatane', 'neotigason', 'نئوتیگازون', 'آسیترتین'],
     [cap('cap-25', 25, Ac, sec='How Supplied'), cap('cap-10', 10, Ac, sec='How Supplied'), tab('cap-17-5', 17.5, '17.5 mg capsule', [R(Ac, 'How Supplied')], per='capsule', form_='capsule')],
     [reg('pso', 'psoriasis', T('پسوریازیس شدید بزرگسال — ۲۵ تا ۵۰ mg یک بار با وعده اصلی', 'Severe psoriasis, adults — 25–50 mg once daily with the main meal'), A18, 'fixed', {'perDose': 25, 'perDoseMax': 50, 'dosesPerDay': 1}, [d],
          notes=[note('نگهدارنده ۲۵ تا ۵۰ mg بر اساس پاسخ. با فوتوتراپی دوز نور کم شود. حداکثر یک ماه دارو در هر بار تحویل.', 'Maintenance 25–50 mg by response. Reduce phototherapy dose if combined. Dispense no more than a month at a time.', [d])])],
     [CI('ci', 'بارداری یا قصد بارداری حین درمان و تا ۳ سال پس از قطع؛ نارسایی شدید کبد یا کلیه؛ چربی خون بالای مزمن؛ متوترکسات همزمان (هپاتیت)؛ تتراسایکلین‌ها (فشار داخل جمجمه)؛ الکل در زنان (تبدیل به اترتینات).',
         'Pregnancy or intended pregnancy during and for 3 years after; severe hepatic or renal impairment; chronic hyperlipidaemia; concomitant methotrexate (hepatitis); tetracyclines (raised intracranial pressure); alcohol in women (converts to etretinate).', [R(Ac, 'Contraindications'), R(Ac, 'Boxed Warning')])],
     warn=[W('هشدار جعبه‌ای: ناهنجاری شدید جنینی — زنان تا ۳ سال پس از قطع پیشگیری مطمئن (دو روش) و الکل ممنوع؛ سمیت کبدی.', 'Boxed warning: severe birth defects — women need reliable contraception (two methods) and no alcohol for 3 years after stopping; hepatotoxicity.', [R(Ac, 'Boxed Warning')])],
     exs=[ex('pso', 'cap-25', {'perDose': 25, 'tabletsPerDoseRounded': 1, 'upperPerDose': 50}, ageYears=45, weightKg=80)])

Tz = fda('tazorac-cream', 'FDA Tazorac cream', 'Tazorac (tazarotene) cream 0.05%/0.1% — Prescribing Information', sid('tazarotene'))
drug('tazarotene', 'dermatology', 'تازاروتن (موضعی)', 'Tazarotene (topical)', T('رتینوئید موضعی', 'Topical retinoid'), [{'name': 'Tazorac', 'market': 'US'}], ['tazorac', 'تازوراک', 'تازاروتن'],
     [unitform('cream', 'cream', 'topical', 'Cream 0.05% and 0.1%', [R(Tz, '3')])],
     [NC('pso', 'psoriasis', 'پسوریازیس پلاک — لایه نازک کرم ۰٫۰۵٪ (در صورت تحمل ۰٫۱٪) یک بار شب فقط روی ضایعات', 'Plaque psoriasis — thin film of 0.05% cream (0.1% if tolerated) once nightly on lesions only', A18,
         'دوز وزنی ندارد؛ حدود ۲ mg/cm² فقط روی ضایعه؛ پوست خشک باشد؛ نرم‌کننده یک ساعت قبل.', 'Not weight-dosed; about 2 mg/cm² on lesions only; skin dry; emollients an hour before.', [R(Tz, '2.2')]),
      NC('acne', 'acne', 'آکنه — لایه نازک کرم ۰٫۱٪ یک بار شب روی نواحی درگیر', 'Acne — thin layer of 0.1% cream once nightly to affected areas', {'minAge': age(12, 'year')},
         'پس از شستن ملایم و خشک شدن پوست؛ ضدآفتاب و پوشش محافظ.', 'After gentle cleansing and drying; use sunscreen and protective clothing.', [R(Tz, '2.3')])],
     [CI('ci', 'بارداری؛ حساسیت به اجزا.', 'Pregnancy; hypersensitivity to any component.', [R(Tz, '4')])],
     warn=[W('سمیت جنینی (تست بارداری منفی پیش از شروع و پیشگیری)؛ تحریک موضعی؛ حساسیت به نور و آفتاب‌سوختگی.', 'Embryofetal toxicity (negative pregnancy test and contraception); local irritation; photosensitivity and sunburn.', [R(Tz, '5')])])

Jb = fda('jublia', 'FDA Jublia', 'Jublia (efinaconazole) topical solution 10% — Prescribing Information', sid('efinaconazole'))
drug('efinaconazole', 'dermatology', 'افیناکونازول', 'Efinaconazole', T('ضدقارچ آزولی موضعی ناخن', 'Topical azole for nails'), [{'name': 'Jublia', 'market': 'US'}], ['jublia', 'جوبلیا', 'افیناکونازول'],
     [unitform('sol', 'solution', 'topical', '10% topical solution with flow-through brush', [R(Jb, '3')])],
     [NC('ony', 'onychomycosis', 'اونیکومایکوز ناخن پا — روزانه یک بار روی ناخن مبتلا، ۴۸ هفته', 'Toenail onychomycosis — apply to affected toenails once daily for 48 weeks', {'minAge': age(6, 'year')},
         'کل ناخن، چین‌ها، بستر ناخن، هیپونیکیوم و زیر صفحه ناخن پوشانده شود. فقط موضعی.', 'Cover the whole nail, nail folds, nail bed, hyponychium and underside of the nail plate. Topical use only.', [R(Jb, '2')])])

Kr = fda('tavaborole', 'FDA Tavaborole', 'Tavaborole topical solution 5% — Prescribing Information', sid('tavaborole'))
drug('tavaborole', 'dermatology', 'تاوابورول', 'Tavaborole', T('ضدقارچ اکسابورول موضعی', 'Topical oxaborole antifungal'), [{'name': 'Kerydin', 'market': 'US'}], ['kerydin', 'کریدین', 'تاوابورول'],
     [unitform('sol', 'solution', 'topical', '5% topical solution', [R(Kr, '3')])],
     [NC('ony', 'onychomycosis', 'اونیکومایکوز ناخن پا — روزانه یک بار روی کل سطح و زیر نوک ناخن، ۴۸ هفته', 'Toenail onychomycosis — apply once daily to the entire nail surface and under the tip for 48 weeks', {'minAge': age(6, 'year')},
         'فقط موضعی؛ چشمی، خوراکی یا واژینال نه.', 'Topical only; not ophthalmic, oral or intravaginal.', [R(Kr, '2')])])

# ===================== eye =====================
Lm = fda('lumigan', 'FDA Lumigan 0.01%', 'Lumigan (bimatoprost ophthalmic solution) 0.01% — Prescribing Information', sid('bimatoprost'))
drug('bimatoprost', 'sensory-organs', 'بیماتوپروست', 'Bimatoprost', T('آنالوگ پروستاگلاندین (چشمی)', 'Prostaglandin analogue (ophthalmic)'), [{'name': 'Lumigan', 'market': 'US'}], ['lumigan', 'لومیگان', 'بیماتوپروست'],
     [drops('0.01% (0.1 mg/mL) eye drops', Lm)],
     [drop_reg('glc', 'glaucoma', 'گلوکوم زاویه باز یا فشار بالای چشم — یک قطره در چشم مبتلا یک بار شب', 'Open-angle glaucoma or ocular hypertension — 1 drop in the affected eye(s) once nightly', 1, [R(Lm, '2')],
               notes=[note('بیش از یک بار در روز اثر را کم می‌کند. با سایر قطره‌ها ۵ دقیقه فاصله.', 'More than once daily reduces the effect. Separate other drops by 5 min.', [R(Lm, '2')])])],
     [CI('hyper', 'حساسیت به بیماتوپروست.', 'Hypersensitivity to bimatoprost.', [R(Lm, '4')])], warn=[PGA_W(Lm)],
     exs=[ex('glc', 'drops', {'perDose': 1}, ageYears=60, weightKg=70)])

Tv = fda('travatan-z', 'FDA Travatan Z', 'Travatan Z (travoprost ophthalmic solution) 0.004% — Prescribing Information', sid('travoprost'))
drug('travoprost', 'sensory-organs', 'تراووپروست', 'Travoprost', T('آنالوگ پروستاگلاندین (چشمی)', 'Prostaglandin analogue (ophthalmic)'), [{'name': 'Travatan Z', 'market': 'US'}], ['travatan', 'تراواتان', 'تراووپروست'],
     [drops('0.004% (0.04 mg/mL) eye drops', Tv)],
     [drop_reg('glc', 'glaucoma', 'گلوکوم زاویه باز یا فشار بالای چشم — یک قطره در چشم مبتلا یک بار شب', 'Open-angle glaucoma or ocular hypertension — 1 drop in the affected eye(s) once nightly', 1, [R(Tv, '2')], pop={'minAge': age(16, 'year')},
               notes=[note('بیش از یک بار در روز اثر را کم می‌کند.', 'More than once daily reduces the effect.', [R(Tv, '2')])])],
     warn=[PGA_W(Tv), W('عفونت قرنیه با ظرف آلوده؛ لنز تماسی ۱۵ دقیقه پس از قطره.', 'Bacterial keratitis from contaminated containers; reinsert contact lenses 15 min after.', [R(Tv, '5')])],
     exs=[ex('glc', 'drops', {'perDose': 1}, ageYears=60, weightKg=70)])

Pc = fda('pilocarpine-125', 'FDA Pilocarpine 1.25%', 'Pilocarpine HCl ophthalmic solution 1.25% — Prescribing Information', sid('pilocarpine'))
drug('pilocarpine-presbyopia', 'sensory-organs', 'پیلوکارپین ۱٫۲۵٪ (پیرچشمی)', 'Pilocarpine 1.25% (presbyopia)', T('کولینرژیک (میوتیک)', 'Cholinergic (miotic)'), [{'name': 'Vuity', 'market': 'US'}], ['vuity', 'ویوتی', 'pilocarpine', 'پیلوکارپین'],
     [drops('1.25% eye drops', Pc)],
     [drop_reg('presb', 'presbyopia', 'پیرچشمی بزرگسال — یک قطره در هر چشم یک بار در روز', 'Presbyopia, adults — 1 drop in each eye once daily', 1, [R(Pc, '2')],
               notes=[note('با سایر قطره‌های چشمی دست‌کم ۵ دقیقه فاصله.', 'Separate other eye drops by at least 5 min.', [R(Pc, '2')])])],
     [CI('hyper', 'حساسیت به پیلوکارپین.', 'Hypersensitivity to pilocarpine.', [R(Pc, '4')])],
     warn=[W('تاری دید و دید کم در نور ضعیف (رانندگی شبانه با احتیاط)؛ خطر جداشدگی شبکیه؛ ایریت.', 'Blurred vision and poor dim-light vision (caution driving at night); risk of retinal detachment; iritis.', [R(Pc, '5')])],
     exs=[ex('presb', 'drops', {'perDose': 1}, ageYears=50, weightKg=70)])

Xi = fda('xiidra', 'FDA Xiidra', 'Xiidra (lifitegrast ophthalmic solution) 5% — Prescribing Information', sid('lifitegrast'))
drug('lifitegrast', 'sensory-organs', 'لیفیتگراست', 'Lifitegrast', T('آنتاگونیست LFA-1 (چشمی)', 'LFA-1 antagonist (ophthalmic)'), [{'name': 'Xiidra', 'market': 'US'}], ['xiidra', 'زیدرا', 'لیفیتگراست'],
     [drops('5% (50 mg/mL) single-use containers', Xi)],
     [drop_reg('dry', 'dry-eye', 'خشکی چشم — یک قطره در هر چشم دو بار در روز (حدود ۱۲ ساعت فاصله)', 'Dry eye disease — 1 drop in each eye twice daily (about 12 h apart)', 2, [R(Xi, '2')], pop={'minAge': age(17, 'year')},
               notes=[note('ظرف یک‌بارمصرف پس از استفاده دور ریخته شود؛ لنز تماسی پیش از قطره برداشته و ۱۵ دقیقه بعد گذاشته شود.', 'Discard the single-use container after use; remove contact lenses before and reinsert 15 min after.', [R(Xi, '2')])])],
     [CI('hyper', 'حساسیت به لیفیتگراست.', 'Hypersensitivity to lifitegrast.', [R(Xi, '4')])],
     exs=[ex('dry', 'drops', {'perDose': 1}, ageYears=45, weightKg=65)])

Lc = fda('lucentis', 'FDA Lucentis', 'Lucentis (ranibizumab) intravitreal injection — Prescribing Information', sid('ranibizumab'))
drug('ranibizumab', 'sensory-organs', 'رانی‌بیزوماب', 'Ranibizumab', T('مهارکننده VEGF (داخل زجاجیه)', 'VEGF inhibitor (intravitreal)'), [{'name': 'Lucentis', 'market': 'US'}], ['lucentis', 'لوسنتیس', 'رانیبیزوماب'],
     [ivt('pfs-0-5', 0.5, '0.5 mg (0.05 mL of 10 mg/mL) prefilled syringe', Lc), ivt('pfs-0-3', 0.3, '0.3 mg (0.05 mL of 6 mg/mL) prefilled syringe', Lc)],
     [reg('amd', 'wet-amd', T('AMD مرطوب — ۰٫۵ mg داخل زجاجیه ماهانه', 'Wet AMD — 0.5 mg intravitreal monthly'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Lc, '2.2')], dur=ONE, allowed=['pfs-0-5'],
          notes=[note('فقط توسط چشم‌پزشک. با کارایی کمتر: ۳ دوز ماهانه سپس فواصل بیشتر با پایش.', 'Ophthalmologist only. Less effective alternative: 3 monthly doses then less frequent with monitoring.', [R(Lc, '2.2')])]),
      reg('rvo', 'retinal-vein-occlusion', T('ادم ماکولا پس از انسداد ورید شبکیه — ۰٫۵ mg ماهانه', 'Macular oedema after RVO — 0.5 mg monthly'), A18, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Lc, '2.3')], dur=ONE, allowed=['pfs-0-5']),
      reg('dme', 'diabetic-macular-edema', T('ادم ماکولای دیابتی و رتینوپاتی دیابتی — ۰٫۳ mg ماهانه', 'DME and diabetic retinopathy — 0.3 mg monthly'), A18, 'fixed', {'perDose': 0.3, 'dosesPerDay': 1}, [R(Lc, '2.4')], dur=ONE, allowed=['pfs-0-3'])],
     [CI('ci', 'عفونت چشم یا اطراف چشم؛ حساسیت به رانی‌بیزوماب.', 'Ocular or periocular infection; hypersensitivity to ranibizumab.', [R(Lc, '4')])],
     warn=[VEGF_W(Lc), W('واسکولیت شبکیه.', 'Retinal vasculitis.', [R(Lc, '5.5')])],
     exs=[ex('amd', 'pfs-0-5', {'perDose': 0.5}, ageYears=75, weightKg=70), ex('rvo', 'pfs-0-5', {'perDose': 0.5}, ageYears=65, weightKg=70), ex('dme', 'pfs-0-3', {'perDose': 0.3}, ageYears=60, weightKg=80)])

Ey = fda('eylea', 'FDA Eylea', 'Eylea (aflibercept) intravitreal injection 2 mg — Prescribing Information', sid('aflibercept'))
drug('aflibercept', 'sensory-organs', 'افلیبرسپت (چشمی)', 'Aflibercept (ophthalmic)', T('مهارکننده VEGF (داخل زجاجیه)', 'VEGF inhibitor (intravitreal)'), [{'name': 'Eylea', 'market': 'US'}], ['eylea', 'آیلیا', 'افلیبرسپت'],
     [ivt('pfs-2', 2, '2 mg (0.05 mL of 40 mg/mL) syringe or vial', Ey)],
     [reg('amd', 'wet-amd', T('AMD مرطوب — ۲ mg داخل زجاجیه هر ۴ هفته ×۳، سپس هر ۸ هفته', 'Wet AMD — 2 mg intravitreal every 4 weeks ×3, then every 8 weeks'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Ey, '2.5')], dur=ONE),
      reg('rvo', 'retinal-vein-occlusion', T('ادم ماکولا پس از انسداد ورید شبکیه — ۲ mg هر ۴ هفته', 'Macular oedema after RVO — 2 mg every 4 weeks'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Ey, '2.6')], dur=ONE),
      reg('dme', 'diabetic-macular-edema', T('ادم ماکولای دیابتی یا رتینوپاتی دیابتی — ۲ mg هر ۴ هفته برای ۵ تزریق، سپس هر ۸ هفته', 'DME or diabetic retinopathy — 2 mg every 4 weeks for 5 injections, then every 8 weeks'), A18, 'fixed', {'perDose': 2, 'dosesPerDay': 1}, [R(Ey, '2.7'), R(Ey, '2.8')], dur=ONE)],
     [VEGF_CI(Ey)], warn=[VEGF_W(Ey)],
     exs=[ex('amd', 'pfs-2', {'perDose': 2}, ageYears=75, weightKg=70), ex('rvo', 'pfs-2', {'perDose': 2}, ageYears=65, weightKg=70), ex('dme', 'pfs-2', {'perDose': 2}, ageYears=60, weightKg=80)])
print('s12f3 ok')
