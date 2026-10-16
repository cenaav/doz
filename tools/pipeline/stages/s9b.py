"""Stage 9b — new diseases (with MedlinePlus symptom lists), label-backed links from existing drugs, and their new drugs."""
import copy, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's9_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}

# --- diseases ---
add_disease('brucellosis', 'بروسلوز (تب مالت)', 'Brucellosis', ['brucellosis', 'تب مالت', 'تب مواج', 'undulant fever', 'بروسلا'], ['A23.9'], 'infectious')
add_disease('low-back-pain', 'کمردرد حاد', 'Acute low back pain', ['back pain', 'کمر درد', 'لومباگو', 'کمردرد'], ['M54.50'], 'musculoskeletal')
add_disease('muscle-strain', 'کشیدگی عضله و پیچ‌خوردگی', 'Muscle strain and sprain', ['strain', 'sprain', 'کشیدگی', 'رگ به رگ', 'پیچ خوردگی'], ['S39.012A'], 'musculoskeletal')
add_disease('tendonitis', 'تاندونیت و بورسیت', 'Tendonitis and bursitis', ['tendinitis', 'bursitis', 'تاندونیت', 'التهاب تاندون', 'بورسیت'], ['M77.9'], 'musculoskeletal')
add_disease('tension-headache', 'سردرد تنشی', 'Tension-type headache', ['tension headache', 'سردرد عصبی', 'سردرد فشاری'], ['G44.209'], 'neurology')
add_disease('measles', 'سرخک (پیشگیری پس از تماس)', 'Measles (post-exposure prophylaxis)', ['measles', 'سرخک'], ['B05.9'], 'infectious')
add_disease('hemorrhoids', 'هموروئید (بواسیر)', 'Haemorrhoids', ['hemorrhoids', 'piles', 'بواسیر', 'هموروئید'], ['K64.9'], 'gastroenterology')
add_disease('anal-fissure', 'شقاق مقعد (فیشر)', 'Anal fissure', ['fissure', 'فیشر', 'شقاق'], ['K60.2'], 'gastroenterology')
add_disease('blepharitis', 'بلفاریت (التهاب پلک)', 'Blepharitis', ['blepharitis', 'demodex', 'التهاب لبه پلک', 'دمودکس'], ['H01.009'], 'ophthalmology')
add_disease('obesity', 'چاقی', 'Obesity', ['obesity', 'overweight', 'چاقی', 'کاهش وزن', 'اضافه وزن'], ['E66.9'], 'endocrinology')
add_disease('vitiligo', 'ویتیلیگو (پیسی)', 'Vitiligo', ['vitiligo', 'پیسی', 'لک سفید'], ['L80'], 'dermatology')
add_disease('hyperhidrosis', 'تعریق زیاد زیر بغل', 'Axillary hyperhidrosis', ['hyperhidrosis', 'تعریق زیاد', 'عرق زیاد'], ['L74.510'], 'dermatology')
add_disease('molluscum', 'مولوسکوم کنتاژیوزوم', 'Molluscum contagiosum', ['molluscum', 'مولوسکوم'], ['B08.1'], 'dermatology')

def ml(aid, title, review):
    m, dd, y = review.split('/')
    return add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                   edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
NOTE = {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}
def symptoms(did, items, *srcs):
    d = json.load(open(os.path.join(ROOT, 'diseases.json')))
    for x in d:
        if x['id'] == did:
            x['symptoms'] = {'items': [T(fa, en) for fa, en in items], 'refs': [{'source': s, 'section': 'Symptoms', 'note': NOTE} for s in srcs]}
    json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')

symptoms('shock', [('افت فشار خون، به‌ویژه هنگام ایستادن', 'Low blood pressure, especially on standing'), ('ضربان تند و نبض ضعیف', 'Rapid heart rate and weak pulse'), ('گیجی، بی‌قراری یا کاهش هوشیاری', 'Confusion, restlessness or reduced alertness'),
                   ('ادرار کم یا قطع ادرار', 'Little or no urine'), ('تنفس تند و تنگی نفس', 'Fast breathing and shortness of breath'), ('پوست سرد، رنگ‌پریده یا لکه‌دار (کاردیوژنیک) یا گرم و برافروخته (سپتیک)', 'Cool, pale or blotchy skin (cardiogenic) or warm, flushed skin (septic)'),
                   ('تب بالا یا دمای خیلی پایین و لرز (سپتیک)', 'High or very low temperature and chills (septic)'), ('درد قفسه سینه (کاردیوژنیک)', 'Chest pain (cardiogenic)')],
         ml('000668', 'Septic shock', '12/13/2025'), ml('000185', 'Cardiogenic shock', '6/1/2026'))
symptoms('acute-ischemic-stroke', [('ضعف ناگهانی صورت، دست یا پا، معمولاً یک طرف بدن', 'Sudden weakness of the face, arm or leg, usually on one side'), ('بی‌حسی یا گزگز یک طرف بدن', 'Numbness or tingling on one side of the body'),
                                   ('اشکال در صحبت کردن یا فهمیدن', 'Trouble speaking or understanding'), ('اختلال دید: کاهش دید، دوبینی', 'Vision problems: reduced or double vision'), ('سرگیجه، عدم تعادل یا اشکال در راه رفتن', 'Dizziness, loss of balance or trouble walking'),
                                   ('گیجی یا کاهش هوشیاری', 'Confusion or reduced alertness'), ('اشکال در بلع', 'Trouble swallowing')], ml('000726', 'Stroke', '4/16/2025'))
symptoms('pulmonary-embolism', [('درد قفسه سینه، اغلب تیز و بدتر با نفس عمیق', 'Chest pain, often sharp and worse with deep breathing'), ('تنفس تند یا خس‌خس', 'Fast breathing or wheezing'), ('ضربان تند', 'Fast heart rate'),
                                ('سرگیجه، سبکی سر یا غش', 'Dizziness, lightheadedness or fainting'), ('اضطراب', 'Anxiety'), ('درد، قرمزی یا تورم پا', 'Leg pain, redness or swelling'), ('افت فشار خون', 'Low blood pressure')], ml('000132', 'Pulmonary embolus', '10/21/2025'))
symptoms('metabolic-acidosis', [('تنفس تند و عمیق', 'Rapid, deep breathing'), ('گیجی یا خواب‌آلودگی', 'Confusion or lethargy'), ('در موارد شدید شوک', 'Shock in severe cases'), ('علائم بیماری زمینه‌ای', 'Symptoms of the underlying cause')], ml('000335', 'Metabolic acidosis', '10/1/2025'))
symptoms('hypokalemia', [('ضعف یا گرفتگی عضلات', 'Muscle weakness or spasms'), ('خستگی', 'Fatigue'), ('یبوست', 'Constipation'), ('تپش قلب یا حس جا افتادن ضربان', 'Palpitations or skipped beats'), ('گزگز یا بی‌حسی', 'Tingling or numbness'),
                         ('در افت شدید: آریتمی، سبکی سر یا غش', 'With a large drop: abnormal heart rhythm, lightheadedness or fainting')], ml('000479', 'Low blood potassium', '5/19/2025'))
symptoms('hyponatremia', [('گیجی، تحریک‌پذیری، بی‌قراری', 'Confusion, irritability, restlessness'), ('سردرد', 'Headache'), ('تهوع و استفراغ', 'Nausea and vomiting'), ('خستگی', 'Fatigue'), ('ضعف، گرفتگی یا اسپاسم عضلات', 'Muscle weakness, spasms or cramps'),
                          ('بی‌اشتهایی', 'Loss of appetite'), ('تشنج', 'Seizures')], ml('000394', 'Low blood sodium', '5/19/2025'))
symptoms('brucellosis', [('تب و لرز، تب موجی که اغلب عصرها بالا می‌رود', 'Fever and chills; undulating fever, often spiking in the afternoon'), ('تعریق زیاد', 'Excessive sweating'), ('درد مفاصل و عضلات', 'Joint and muscle pain'), ('کمردرد', 'Back pain'),
                         ('خستگی و ضعف', 'Fatigue and weakness'), ('سردرد', 'Headache'), ('بی‌اشتهایی و کاهش وزن', 'Loss of appetite and weight loss'), ('درد شکم', 'Abdominal pain'), ('تورم غدد لنفاوی', 'Swollen glands')], ml('000597', 'Brucellosis', '8/5/2025'))
symptoms('low-back-pain', [('درد مبهم، تیز یا سوزشی در کمر', 'Dull ache, sharp or burning pain in the lower back'), ('گزگز در کمر', 'Tingling'), ('درد منتشر به پا، لگن یا کف پا', 'Pain spreading to the leg, hip or sole of the foot'),
                           ('محدودیت حرکت در درد شدید', 'Limited movement when severe'), ('ضعف پا (در برخی علل)', 'Leg weakness (with some causes)')], ml('007425', 'Low back pain - acute', '6/27/2026'))
symptoms('muscle-strain', [('درد عضله یا مفصل', 'Muscle or joint pain'), ('تورم', 'Swelling'), ('خشکی مفصل', 'Joint stiffness'), ('کبودی و تغییر رنگ پوست', 'Bruising or skin discolouration')], ml('000041', 'Sprains', '4/1/2025'))
symptoms('tendonitis', [('درد و حساسیت در طول تاندون، معمولاً نزدیک مفصل', 'Pain and tenderness along a tendon, usually near a joint'), ('درد شبانه', 'Pain at night'), ('درد بدتر با حرکت یا فعالیت', 'Pain worse with movement or activity'), ('خشکی صبحگاهی', 'Morning stiffness')],
         ml('001229', 'Tendinitis', '7/23/2024'))
symptoms('tension-headache', [('درد مبهم و فشاری (نه ضربان‌دار)', 'Dull, pressure-like pain (not throbbing)'), ('حس بند سفت یا گیره دور سر', 'A tight band or vise around the head'), ('درد در کل سر، بیشتر پوست سر، شقیقه یا پشت گردن', 'Pain all over, worse in the scalp, temples or back of the neck'),
                              ('مدت ۳۰ دقیقه تا ۷ روز', 'Lasting 30 minutes to 7 days'), ('تشدید با استرس، خستگی، سر و صدا یا نور', 'Triggered or worsened by stress, fatigue, noise or glare'), ('معمولاً بدون تهوع', 'Usually no nausea')],
         ml('000797', 'Tension headache', '10/27/2025'))
symptoms('measles', [('بثورات که از سر شروع و به پایین بدن پخش می‌شود (۳ تا ۵ روز پس از شروع بیماری)', 'Rash starting on the head and spreading down the body (3–5 days after illness begins)'), ('تب', 'Fever'), ('سرفه و آبریزش بینی', 'Cough and runny nose'),
                     ('قرمزی و التهاب چشم، حساسیت به نور', 'Red, inflamed eyes and light sensitivity'), ('گلودرد', 'Sore throat'), ('لکه‌های سفید ریز داخل دهان (کوپلیک)', 'Tiny white spots inside the mouth (Koplik spots)'), ('درد عضلات', 'Muscle pain')],
         ml('001569', 'Measles', '7/16/2024'))
symptoms('hemorrhoids', [('خون قرمز روشن بدون درد هنگام دفع', 'Painless bright red rectal bleeding'), ('خارش مقعد', 'Anal itching'), ('درد مقعد، به‌ویژه هنگام نشستن یا دفع', 'Anal pain, especially when sitting or passing stool'), ('برآمدگی سفت یا دردناک کنار مقعد', 'Hard or tender lump near the anus')],
         ml('000292', 'Hemorrhoids', '7/22/2025'))
symptoms('anal-fissure', [('دفع دردناک', 'Painful bowel movements'), ('خون روی مدفوع یا دستمال توالت', 'Blood on the stool or toilet paper'), ('ترک دیده‌شده در پوست مقعد', 'A visible crack in the anal skin')], ml('001130', 'Anal fissure', '4/11/2026'))
symptoms('blepharitis', [('قرمزی و تحریک پلک', 'Red, irritated eyelids'), ('پوسته چسبیده به ریشه مژه‌ها', 'Scales stuck to the base of the lashes'), ('سوزش، خارش و تورم پلک', 'Burning, itching and swelling of the lids'), ('حس شن یا گرد در چشم', 'Gritty, sandy feeling'), ('ریزش مژه', 'Loss of eyelashes')],
         ml('001619', 'Blepharitis', '8/5/2024'))
symptoms('vitiligo', [('لکه‌های صاف بدون رنگدانه با حاشیه تیره‌تر و لبه نامنظم', 'Flat patches without pigment with a darker, irregular border'), ('بیشتر روی صورت، آرنج، زانو، پشت دست و پا و ناحیه تناسلی', 'Mostly face, elbows, knees, backs of hands and feet, genitals'), ('معمولاً قرینه در دو طرف بدن', 'Usually symmetrical')],
         ml('000831', 'Vitiligo', '4/9/2026'))
symptoms('molluscum', [('برجستگی کوچک بدون درد، مرواریدی یا همرنگ پوست', 'Small painless, pearly or flesh-coloured bump'), ('فرورفتگی در وسط برجستگی', 'A dimple in the centre'), ('اندازه ۲ تا ۵ میلی‌متر', '2–5 mm in size'), ('پخش شدن در خط یا گروه با خاراندن', 'Spreads in lines or groups with scratching')],
         ml('000826', 'Molluscum contagiosum', '4/1/2025'))

# --- links from existing drugs (copy of the existing label-cited regimen under the new disease) ---
def clone(drug_id, src_id, new_id, disease, fa, en, extra_notes=()):
    p = find(drug_id); d = json.load(open(p))
    r = copy.deepcopy(next(x for x in d['regimens'] if x['id'] == src_id))
    r.update(id=new_id, disease=disease, label=T(fa, en)); r['notes'] = list(r.get('notes', [])) + list(extra_notes)
    d['regimens'] = [x for x in d['regimens'] if x['id'] != new_id] + [r]
    d['examples'] = [e for e in d['examples'] if e['regimen'] != new_id] + [dict(copy.deepcopy(e), regimen=new_id) for e in d['examples'] if e['regimen'] == src_id][:1]
    fix_bands(d); json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

clone('cyclobenzaprine', 'spasm', 'back', 'low-back-pain', 'کمردرد حاد با اسپاسم عضلانی — کوتاه‌مدت (۲ تا ۳ هفته)', 'Acute low back pain with muscle spasm — short term (2–3 weeks)')
clone('cyclobenzaprine', 'spasm', 'strain', 'muscle-strain', 'کشیدگی یا پیچ‌خوردگی با اسپاسم عضلانی — کوتاه‌مدت', 'Strain or sprain with muscle spasm — short term')
clone('ibuprofen', 'otc-adult', 'back-otc', 'low-back-pain', 'کمردرد و درد عضلانی (بدون نسخه) — ۱۲ سال به بالا', 'Backache and muscular aches (OTC) — ≥12 y')
clone('ibuprofen', 'otc-adult', 'strain-otc', 'muscle-strain', 'درد عضلانی (بدون نسخه) — ۱۲ سال به بالا', 'Muscular aches (OTC) — ≥12 y')
clone('ibuprofen', 'otc-adult', 'headache-otc', 'tension-headache', 'سردرد (بدون نسخه) — ۱۲ سال به بالا', 'Headache (OTC) — ≥12 y')
clone('ibuprofen', 'pain-otc', 'headache-child', 'tension-headache', 'سردرد کودک (سوسپانسیون بدون نسخه)', 'Headache in children (OTC suspension)')
clone('acetaminophen', 'pain', 'headache', 'tension-headache', 'سردرد کودک', 'Headache in children')
clone('naproxen', 'pain', 'tendonitis', 'tendonitis', 'تاندونیت و بورسیت حاد — بزرگسال', 'Acute tendonitis and bursitis — adult')

Mm = 'fda-mmr'
patch('mmr-vaccine', add_regs=[reg('measles-pep', 'measles', T('پیشگیری پس از تماس با سرخک — یک دوز ظرف ۷۲ ساعت', 'Measles post-exposure prophylaxis — one dose within 72 h'), {'minAge': age(12, 'month')}, 'fixed', {'perDose': 0.5, 'dosesPerDay': 1}, [R(Mm, '2.1')], unit='mL', dur=ONE)],
      add_exs=[ex('measles-pep', 'vial-05', {'perDose': 0.5, 'mlPerDose': 0.5}, ageYears=3, weightKg=14)])

Dx, Ds = 'fda-doxycycline', 'fda-doxysusp'
BRU = note('برچسب: بروسلوز «همراه با استرپتومایسین». مدت درمان در برچسب ذکر نشده است.', 'Label: brucellosis “in conjunction with streptomycin”. The label gives no duration.', [R(Dx, 'Indications and Usage')])
patch('doxycycline', add_regs=[
    reg('brucella-adult', 'brucellosis', T('بروسلوز — بزرگسال: ۱۰۰ mg هر ۱۲ ساعت (همراه استرپتومایسین)', 'Brucellosis — adult: 100 mg every 12 h (with streptomycin)'), {'minWeightKg': 45}, 'fixed', {'perDose': 100, 'dosesPerDay': 2}, [R(Dx, 'Dosage and Administration — Adults')], notes=[BRU]),
    reg('brucella-child', 'brucellosis', T('بروسلوز — کودک زیر ۴۵ kg (عفونت شدید): ۲٫۲ mg/kg هر ۱۲ ساعت', 'Brucellosis — child <45 kg (severe infection): 2.2 mg/kg every 12 h'), {'minAge': age(8, 'year'), 'maxWeightKg': 44.99}, 'weightBased', {'perKgPerDose': 2.2, 'intervalHours': 12}, [R(Dx, 'Dosage and Administration — Pediatric Patients')],
        allowed=['susp-25'], notes=[BRU, note('زیر ۸ سال (خطر تغییر رنگ دائمی دندان) فقط در عفونت شدید یا تهدیدکننده حیات؛ برای آن از رژیم «عفونت شدید کودک» همین دارو استفاده کنید.', 'Under 8 y (risk of permanent tooth discolouration) only for severe or life-threatening infection; use this drug’s severe-infection pediatric regimen.', [R(Dx, 'Warnings')])])],
    add_exs=[ex('brucella-adult', 'tab-100', {'perDose': 100, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('brucella-child', 'susp-25', {'perDose': 66, 'mlPerDose': 13.2}, ageYears=10, weightKg=30)])

St = fda('streptomycin', 'FDA Streptomycin', 'Streptomycin for injection 1 g (XGen) — Prescribing Information', sid('streptomycin')); d = R(St, 'Dosage and Administration — Other Infections')
drug('streptomycin', 'anti-infectives', 'استرپتومایسین', 'Streptomycin', T('آمینوگلیکوزید', 'Aminoglycoside'), [{'name': 'Streptomycin', 'market': 'US'}], ['streptomycin', 'استرپتومایسین'],
     [form('vial-1g', 'powder-for-injection', 'im', '1 g vial (IM after reconstitution)', 1000, 'mg', [R(St, 'How Supplied')], per='vial')],
     [reg('adult', 'brucellosis', T('بروسلوز و سایر عفونت‌ها — بزرگسال: ۱ تا ۲ g در روز در دوزهای منقسم (عضلانی)', 'Brucellosis and other infections — adult: 1–2 g/day in divided doses (IM)'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 1000, 'dosesPerDay': 2}, [d],
          limits={'maxPerDay': 2000, 'refs': [d]}, notes=[note('هر ۶ تا ۱۲ ساعت؛ معمولاً بیش از ۲ g در روز نشود. بالای ۶۰ سال و نارسایی کلیه دوز کمتر.', 'Every 6–12 h; generally not over 2 g/day. Reduce over 60 y and in renal impairment.', [d, R(St, 'Dosage and Administration')])]),
      reg('child', 'brucellosis', T('کودک — ۲۰ تا ۴۰ mg/kg/روز در دوزهای منقسم هر ۶ تا ۱۲ ساعت', 'Child — 20–40 mg/kg/day in divided doses every 6–12 h'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDay': 20, 'perKgPerDayMax': 40, 'dividedDoses': 2}, [d],
          notes=[note('از دوز بیش از حد در کودک به‌ویژه پرهیز شود (افسردگی CNS در شیرخوار).', 'Take particular care to avoid excessive doses in children (CNS depression in infants).', [d, R(St, 'Dosage and Administration')])])],
     [CI('hyper', 'سابقه حساسیت به استرپتومایسین یا سایر آمینوگلیکوزیدها.', 'History of hypersensitivity to streptomycin or other aminoglycosides.', [R(St, 'Contraindications')])],
     warn=[W('هشدار جعبه‌ای: خطر سمیت عصبی شدید (اختلال تعادل و شنوایی، عصب بینایی، نوریت محیطی، انسفالوپاتی) در نارسایی کلیه یا ازوتمی پیش‌کلیوی به‌شدت بیشتر است؛ عملکرد کلیه و شنوایی پایش شود.', 'Boxed warning: risk of severe neurotoxicity (vestibular and cochlear dysfunction, optic nerve dysfunction, peripheral neuritis, encephalopathy) is sharply increased with impaired renal function or prerenal azotaemia; monitor renal function and hearing.', [R(St, 'Boxed Warning'), R(St, 'Warnings')])],
     exs=[ex('adult', 'vial-1g', {'perDose': 500, 'upperPerDose': 1000}, ageYears=40, weightKg=70), ex('child', 'vial-1g', {'perDose': 200, 'upperPerDose': 400}, ageYears=6, weightKg=20)])

# --- new drugs for the new diseases ---
Ph = fda('preparation-h', 'FDA Preparation H oint.', 'Preparation H ointment (phenylephrine/petrolatum/mineral oil) — Drug Facts', sid('prepH'))
drug('preparation-h', 'cardiovascular', 'پماد ضدبواسیر (فنیل‌افرین + وازلین)', 'Haemorrhoid ointment (phenylephrine + petrolatum)', T('ضد هموروئید موضعی', 'Topical antihaemorrhoidal'), [{'name': 'Preparation H', 'market': 'US'}], ['preparation h', 'پماد بواسیر', 'پماد هموروئید'],
     [unitform('oint', 'ointment', 'rectal', 'Ointment (phenylephrine 0.25%, petrolatum 74.9%, mineral oil 14%)', [R(Ph, 'Package label')])],
     [reg('hem', 'hemorrhoids', T('هموروئید — تا ۴ بار در روز (بزرگسال)', 'Haemorrhoids — up to 4 times daily (adults)'), A18, 'notCalculated',
          {'reason': T('ناحیه را با دستمال مرطوب تمیز و خشک کنید؛ تا ۴ بار در روز، به‌ویژه شب، صبح یا پس از هر دفع روی ناحیه یا داخل مقعد با اپلیکاتور. زیر ۱۲ سال با نظر پزشک.', 'Clean and pat dry; apply externally or intrarectally with the applicator up to 4 times daily, especially at night, in the morning or after each bowel movement. Under 12: ask a doctor.')}, [R(Ph, 'Directions'), R(Ph, 'Uses')])])

Hc = fda('hc-supp', 'FDA HC suppository', 'Hydrocortisone acetate rectal suppositories 25/30 mg (Aarna) — Prescribing Information', sid('anusolhc')); d = R(Hc, 'Dosage and Administration')
drug('hydrocortisone-suppository', 'cardiovascular', 'شیاف هیدروکورتیزون (ضدبواسیر)', 'Hydrocortisone acetate suppository', T('کورتیکواستروئید رکتال', 'Rectal corticosteroid'), [{'name': 'Anusol-HC', 'market': 'US'}], ['anusol-hc', 'شیاف بواسیر', 'هیدروکورتیزون رکتال'],
     [form('supp-25', 'suppository', 'rectal', '25 mg suppository', 25, 'mg', [R(Hc, 'How Supplied')], per='application')],
     [reg('hem', 'hemorrhoids', T('هموروئید ملتهب و پروکتیت — یک شیاف دو بار در روز، ۲ هفته', 'Inflamed haemorrhoids and proctitis — one suppository twice daily, 2 weeks'), A18, 'fixed', {'perDose': 25, 'dosesPerDay': 2}, [d], dur={'min': 14, 'max': 14},
          notes=[note('موارد شدیدتر: یک شیاف ۳ بار در روز یا دو شیاف دو بار در روز. پیش از مصرف معاینه مقعد لازم است.', 'More severe: one suppository three times daily or two twice daily. Proctological examination first.', [d, R(Hc, 'Precautions')])])],
     [CI('hyper', 'حساسیت به هیدروکورتیزون استات.', 'Hypersensitivity to hydrocortisone acetate.', [R(Hc, 'Contraindications')])],
     exs=[ex('hem', 'supp-25', {'perDose': 25, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])

Rc = fda('rectiv', 'FDA Rectiv', 'Rectiv (nitroglycerin 0.4%) ointment — Prescribing Information', sid('rectiv'))
drug('nitroglycerin-ointment', 'cardiovascular', 'پماد نیتروگلیسرین ۰٫۴٪ (شقاق مقعد)', 'Nitroglycerin 0.4% ointment (anal fissure)', T('نیترات موضعی', 'Topical nitrate'), [{'name': 'Rectiv', 'market': 'US'}], ['rectiv', 'رکتیو', 'پماد نیتروگلیسرین'],
     [unitform('oint', 'ointment', 'rectal', '0.4% ointment (1 inch = 1.5 mg nitroglycerin)', [R(Rc, '3')])],
     [reg('fissure', 'anal-fissure', T('درد شقاق مزمن مقعد — ۱ اینچ (۱٫۵ mg) داخل مقعد هر ۱۲ ساعت تا ۳ هفته', 'Chronic anal fissure pain — 1 inch (1.5 mg) intra-anally every 12 h up to 3 weeks'), A18, 'notCalculated',
          {'reason': T('با انگشت پوشیده (دستکش یا کاور)، به اندازه خط ۱ اینچی روی جعبه (۳۷۵ mg پماد = ۱٫۵ mg نیتروگلیسرین) آرام داخل مجرای مقعد؛ هر ۱۲ ساعت، حداکثر ۳ هفته.', 'With a covered finger, a 1-inch line as marked on the carton (375 mg ointment = 1.5 mg nitroglycerin) gently into the anal canal; every 12 h for up to 3 weeks.')}, [R(Rc, '2')])],
     [CI('ci', 'مصرف مهارکننده‌های PDE5 (سیلدنافیل، تادالافیل، واردنافیل)؛ کم‌خونی شدید؛ افزایش فشار داخل جمجمه؛ حساسیت به نیترات‌ها.', 'PDE5 inhibitors (sildenafil, tadalafil, vardenafil); severe anaemia; raised intracranial pressure; nitrate hypersensitivity.', [R(Rc, '4')])],
     inter=[IA('pde5', 'سیلدنافیل، تادالافیل و واردنافیل: افت شدید فشار — ممنوع.', 'Sildenafil, tadalafil and vardenafil: severe hypotension — contraindicated.', [R(Rc, '4')])])

Xd = fda('xdemvy', 'FDA Xdemvy', 'Xdemvy (lotilaner 0.25%) ophthalmic solution — Prescribing Information', sid('xdemvy'))
drug('lotilaner-eye', 'sensory-organs', 'قطره چشمی لوتیلانر (بلفاریت دمودکسی)', 'Lotilaner eye drops (Demodex blepharitis)', T('ضدانگل چشمی', 'Ophthalmic antiparasitic'), [{'name': 'Xdemvy', 'market': 'US'}], ['xdemvy', 'لوتیلانر'],
     [unitform('sol', 'eye-drops', 'ophthalmic', 'Lotilaner 0.25% eye drops', [R(Xd, '3')], unit='drop', per='drop')],
     [reg('demodex', 'blepharitis', T('بلفاریت دمودکسی — یک قطره در هر چشم دو بار در روز، ۶ هفته', 'Demodex blepharitis — 1 drop in each eye twice daily, 6 weeks'), {}, 'fixed', {'perDose': 1, 'dosesPerDay': 2}, [R(Xd, '2')], unit='drop', dur={'min': 42, 'max': 42},
          notes=[note('حدود ۱۲ ساعت فاصله؛ با سایر قطره‌ها ۵ دقیقه فاصله. لنز تماسی قبل از قطره درآورده و ۱۵ دقیقه بعد گذاشته شود.', 'About 12 h apart; 5 min from other drops. Remove contact lenses and reinsert after 15 min.', [R(Xd, '2'), R(Xd, '5.2')])])],
     exs=[ex('demodex', 'sol', {'perDose': 1, 'dosesPerDay': 2}, ageYears=50, weightKg=70)])

Xn = fda('xenical', 'FDA Xenical', 'Xenical (orlistat) 120 mg capsules — Prescribing Information', sid('xenical'))
drug('orlistat', 'alimentary-metabolism', 'اورلیستات', 'Orlistat', T('مهارکننده لیپاز (ضدچاقی)', 'Lipase inhibitor (anti-obesity)'), [{'name': 'Xenical', 'market': 'US'}], ['xenical', 'زنیکال', 'اورلیستات'],
     [tab('cap-120', 120, '120 mg capsule', [R(Xn, '3')], per='capsule', form_='capsule')],
     [reg('obesity', 'obesity', T('چاقی — ۱۲۰ mg سه بار در روز با هر وعده اصلی حاوی چربی', 'Obesity — 120 mg three times daily with each fat-containing main meal'), A18, 'fixed', {'perDose': 120, 'dosesPerDay': 3}, [R(Xn, '2')],
          notes=[note('حین یا تا ۱ ساعت پس از غذا؛ اگر وعده بدون چربی یا حذف شد، دوز حذف. رژیم کم‌کالری با حدود ۳۰٪ چربی. مولتی‌ویتامین حاوی ویتامین‌های محلول در چربی با ۲ ساعت فاصله.', 'During or up to 1 h after the meal; skip if the meal is missed or fat-free. Reduced-calorie diet with about 30% fat. Multivitamin with fat-soluble vitamins 2 h apart.', [R(Xn, '2')])])],
     [CI('ci', 'بارداری؛ سندرم سوءجذب مزمن؛ کلستاز؛ حساسیت.', 'Pregnancy; chronic malabsorption; cholestasis; hypersensitivity.', [R(Xn, '4')])],
     exs=[ex('obesity', 'cap-120', {'perDose': 120, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=100)])

GLP = lambda src: CI('mtc', 'سابقه شخصی یا خانوادگی کارسینوم مدولاری تیروئید یا MEN 2؛ حساسیت جدی.', 'Personal or family history of medullary thyroid carcinoma or MEN 2; serious hypersensitivity.', [R(src, '4')])
GLPW = lambda src: W('هشدار جعبه‌ای: تومور سلول C تیروئید در جوندگان.', 'Boxed warning: thyroid C-cell tumours in rodents.', [R(src, 'Boxed Warning')])
Wg = fda('wegovy', 'FDA Wegovy', 'Wegovy (semaglutide) injection and tablets — Prescribing Information', sid('wegovy'))
patch('semaglutide', add_regs=[reg('obesity', 'obesity', T('چاقی (Wegovy) — هفته‌ای یک بار: ۰٫۲۵ → ۰٫۵ → ۱ → ۱٫۷ → نگهدارنده ۲٫۴ mg', 'Obesity (Wegovy) — weekly: 0.25 → 0.5 → 1 → 1.7 → maintenance 2.4 mg'), {'minAge': age(12, 'year')}, 'notCalculated',
    {'reason': T('هفته‌ای یک بار زیرجلدی (نه روزانه): هفته ۱ تا ۴ ← ۰٫۲۵ mg؛ ۵ تا ۸ ← ۰٫۵؛ ۹ تا ۱۲ ← ۱؛ ۱۳ تا ۱۶ ← ۱٫۷؛ از هفته ۱۷ نگهدارنده ۲٫۴ mg (یا ۱٫۷). بزرگسال با تحمل ۲٫۴ mg تا ۴ هفته: حداکثر ۷٫۲ mg. همراه رژیم کم‌کالری و فعالیت.',
                 'Once WEEKLY SC (not daily): weeks 1–4 → 0.25 mg; 5–8 → 0.5; 9–12 → 1; 13–16 → 1.7; from week 17 maintenance 2.4 mg (or 1.7). Adults tolerating 2.4 mg for 4 weeks: up to 7.2 mg. With a reduced-calorie diet and activity.')},
    [R(Wg, '2.2, Table 1'), R(Wg, '2.2')])])
Sx = fda('saxenda', 'FDA Saxenda', 'Saxenda (liraglutide) injection — Prescribing Information', sid('saxenda'))
patch('liraglutide', add_forms=[liquid('saxenda-6', 6, 1, 'Saxenda 6 mg/mL pen (doses 0.6–3 mg)', [R(Sx, '3')], form_='injection', route='sc')],
      add_regs=[reg('obesity', 'obesity', T('چاقی (Saxenda، ۱۲ سال به بالا) — روزانه: ۰٫۶ و هر هفته ۰٫۶ mg بیشتر تا ۳ mg', 'Obesity (Saxenda, ≥12 y) — daily: 0.6 mg, increase 0.6 mg weekly to 3 mg'), {'minAge': age(12, 'year')}, 'titration',
                    {'dividedDoses': 1, 'titration': {'start': 0.6, 'increment': 0.6, 'incrementEveryDays': 7, 'targetMin': 3, 'targetMax': 3, 'max': 3}}, [R(Sx, '2.2, Table 1')], allowed=['saxenda-6'],
                    notes=[note('بزرگسال: اگر ۳ mg تحمل نشد قطع. کودک: در عدم تحمل ۲٫۴ mg؛ افزایش تا ۸ هفته طول بکشد.', 'Adults: stop if 3 mg is not tolerated. Children: may reduce to 2.4 mg; escalation may take up to 8 weeks.', [R(Sx, '2.2')])])],
      add_exs=[ex('obesity', 'saxenda-6', {'perDose': 0.6, 'mlPerDose': 0.1}, ageYears=40, weightKg=100)], pin_old=True)
Zb = fda('zepbound', 'FDA Zepbound', 'Zepbound (tirzepatide) injection — Prescribing Information', sid('zepbound'))
patch('tirzepatide', add_regs=[reg('obesity', 'obesity', T('چاقی (Zepbound) — هفته‌ای یک بار: ۲٫۵ mg × ۴ هفته، سپس ۵ mg؛ نگهدارنده ۵، ۱۰ یا ۱۵ mg', 'Obesity (Zepbound) — weekly: 2.5 mg × 4 weeks, then 5 mg; maintenance 5, 10 or 15 mg'), A18, 'notCalculated',
    {'reason': T('هفته‌ای یک بار زیرجلدی (نه روزانه). ۲٫۵ mg فقط برای شروع (۴ هفته)، سپس ۵ mg؛ در صورت نیاز هر دست‌کم ۴ هفته ۲٫۵ mg افزایش. نگهدارنده ۵، ۱۰ یا ۱۵ mg؛ حداکثر ۱۵ mg.', 'Once WEEKLY SC (not daily). 2.5 mg for initiation only (4 weeks), then 5 mg; increase by 2.5 mg after at least 4 weeks as needed. Maintenance 5, 10 or 15 mg; max 15 mg.')},
    [R(Zb, '2.1'), R(Zb, '2.2')])])
for i, src in (('semaglutide', Wg), ('tirzepatide', Zb), ('liraglutide', Sx)):
    p = find(i); dd = json.load(open(p))
    for c in dd['contraindications']:
        if c['id'] == 'mtc' and all(r['source'] != src for r in c['refs']): c['refs'].append(R(src, '4'))
    json.dump(dd, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Oz = fda('opzelura', 'FDA Opzelura', 'Opzelura (ruxolitinib 1.5%) cream — Prescribing Information', sid('opzelura'))
drug('ruxolitinib-cream', 'dermatology', 'کرم روکسولیتینیب ۱٫۵٪', 'Ruxolitinib cream 1.5%', T('مهارکننده JAK موضعی', 'Topical JAK inhibitor'), [{'name': 'Opzelura', 'market': 'US'}], ['opzelura', 'اپزلورا', 'روکسولیتینیب'],
     [unitform('cream', 'cream', 'topical', 'Ruxolitinib 1.5% cream (60 g, 100 g)', [R(Oz, '3')])],
     [reg('vitiligo', 'vitiligo', T('ویتیلیگوی غیرسگمنتال (۱۲ سال به بالا) — لایه نازک دو بار در روز تا ۱۰٪ سطح بدن', 'Nonsegmental vitiligo (≥12 y) — thin layer twice daily up to 10% BSA'), {'minAge': age(12, 'year')}, 'notCalculated',
          {'reason': T('لایه نازک دو بار در روز روی نواحی درگیر تا ۱۰٪ سطح بدن؛ پانسمان بسته نه؛ حداکثر یک لوله ۶۰ گرمی در هفته یا ۱۰۰ گرمی در ۲ هفته.', 'Thin layer twice daily to affected areas up to 10% BSA; no occlusion; max one 60 g tube per week or 100 g per 2 weeks.')}, [R(Oz, '2.2')]),
      reg('ad', 'atopic-dermatitis', T('درماتیت آتوپیک خفیف تا متوسط — دو بار در روز تا ۲۰٪ سطح بدن', 'Mild–moderate atopic dermatitis — twice daily up to 20% BSA'), {'minAge': age(2, 'year')}, 'notCalculated',
          {'reason': T('لایه نازک دو بار در روز تا ۲۰٪ سطح بدن. ۱۲ سال به بالا: حداکثر ۶۰ g در هفته؛ ۲ تا ۱۱ سال: ۶۰ g در ۲ هفته.', 'Thin layer twice daily up to 20% BSA. ≥12 y: max 60 g per week; 2–11 y: 60 g per 2 weeks.')}, [R(Oz, '2.1')])],
     warn=[W('هشدار جعبه‌ای (مهارکننده‌های JAK): عفونت جدی، مرگ، بدخیمی، حوادث قلبی و ترومبوز.', 'Boxed warning (JAK inhibitors): serious infections, mortality, malignancy, MACE and thrombosis.', [R(Oz, 'Boxed Warning')])])

Qb = fda('qbrexza', 'FDA Qbrexza', 'Qbrexza (glycopyrronium 2.4%) cloth — Prescribing Information', sid('qbrexza'))
drug('glycopyrronium-cloth', 'dermatology', 'دستمال گلیکوپیرونیوم (تعریق زیر بغل)', 'Glycopyrronium cloth', T('آنتی‌کولینرژیک موضعی', 'Topical anticholinergic'), [{'name': 'Qbrexza', 'market': 'US'}], ['qbrexza', 'گلیکوپیرونیوم'],
     [unitform('cloth', 'cream', 'topical', 'Single-use cloth with 2.4% glycopyrronium', [R(Qb, '3')])],
     [reg('axilla', 'hyperhidrosis', T('تعریق اولیه زیر بغل (۹ سال به بالا) — یک دستمال روزانه برای هر دو زیر بغل', 'Primary axillary hyperhidrosis (≥9 y) — one cloth daily for both underarms'), {'minAge': age(9, 'year')}, 'notCalculated',
          {'reason': T('روی پوست تمیز و خشک فقط زیر بغل؛ یک دستمال یک بار روی هر زیر بغل؛ حداکثر هر ۲۴ ساعت یک بار. پس از مصرف دست‌ها شسته شود (تاری دید با تماس چشم).', 'On clean dry underarm skin only; wipe one cloth once across each underarm; no more than once every 24 h. Wash hands afterwards (blurred vision if it reaches the eyes).')}, [R(Qb, '2'), R(Qb, '1')])],
     [CI('ci', 'بیماری‌هایی که با اثر آنتی‌کولینرژیک بدتر می‌شوند: گلوکوم، ایلئوس فلجی، وضعیت ناپایدار قلبی در خونریزی، کولیت اولسروز شدید، مگاکولون توکسیک، میاستنی گراویس، شوگرن.',
         'Conditions worsened by anticholinergic effects: glaucoma, paralytic ileus, unstable cardiovascular status in haemorrhage, severe ulcerative colitis, toxic megacolon, myasthenia gravis, Sjögren’s.', [R(Qb, '4')])])

Zv = fda('zelsuvmi', 'FDA Zelsuvmi', 'Zelsuvmi (berdazimer 10.3%) topical gel — Prescribing Information', sid('zelsuvmi'))
drug('berdazimer', 'dermatology', 'ژل بردازیمر (مولوسکوم)', 'Berdazimer gel', T('آزادکننده نیتریک اکسید موضعی', 'Topical nitric oxide releaser'), [{'name': 'Zelsuvmi', 'market': 'US'}], ['zelsuvmi', 'بردازیمر'],
     [unitform('gel', 'gel', 'topical', 'Berdazimer 10.3% gel (two tubes, mixed before use)', [R(Zv, '3')])],
     [reg('mc', 'molluscum', T('مولوسکوم (۱ سال به بالا) — روزانه روی هر ضایعه تا ۱۲ هفته', 'Molluscum (≥1 y) — once daily to each lesion up to 12 weeks'), {'minAge': age(1, 'year')}, 'notCalculated',
          {'reason': T('مقدار مساوی از لوله A و B طبق راهنما مخلوط و فوراً لایه نازک روی هر ضایعه، روزانه تا ۱۲ هفته. نه برای چشم، دهان یا واژن.', 'Mix equal amounts of tube A and B per the dosing guide and immediately apply a thin layer to each lesion, once daily for up to 12 weeks. Not for eye, mouth or vagina.')}, [R(Zv, '2')])],
     warn=[W('واکنش محل مصرف از جمله درماتیت تماسی آلرژیک.', 'Application site reactions including allergic contact dermatitis.', [R(Zv, '5.1')])])
print('s9b ok')
