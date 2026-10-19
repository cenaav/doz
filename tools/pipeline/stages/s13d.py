"""Stage 13d — symptoms for diseases that had none, from the MedlinePlus Medical Encyclopedia 'Symptoms' section (paraphrased and translated).
Skipped on purpose: prophylaxis/procedure entries (anaesthesia, contraception, surgical prophylaxis…) and entries that are themselves a symptom (fever, cough, itching…)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import ROOT, T, TODAY, add_src

NOTE = {'en': 'Symptom list paraphrased and translated into Persian by Doz', 'fa': 'فهرست علائم با بازنویسی و ترجمه Doz'}
D = json.load(open(os.path.join(ROOT, 'diseases.json')))
BY = {x['id']: x for x in D}

def S(did, aid, title, review, items):
    m, dd, y = review.split('/')
    src = add_src(id=f'medlineplus-{aid}', type='medlineplus', short='MedlinePlus', title=f'MedlinePlus Medical Encyclopedia: {title}', publisher='U.S. National Library of Medicine (A.D.A.M.)',
                  edition=f'Review date {y}-{int(m):02d}-{int(dd):02d}', url=f'https://medlineplus.gov/ency/article/{aid}.htm', accessed=TODAY, license='public')
    BY[did]['symptoms'] = {'items': [T(fa, en) for fa, en in items], 'refs': [{'source': src, 'section': 'Symptoms', 'note': NOTE}]}

S('faecal-impaction', '000230', 'Fecal impaction', '10/20/2025', [('گرفتگی و نفخ شکم', 'Abdominal cramping and bloating'), ('نشت مدفوع آبکی یا اسهال ناگهانی در فرد با یبوست مزمن', 'Leakage of watery stool or sudden diarrhoea in someone with chronic constipation'),
    ('خونریزی از مقعد', 'Rectal bleeding'), ('مدفوع کم و نیمه‌شکل', 'Small, semi-formed stools'), ('زور زدن هنگام دفع', 'Straining to pass stool'), ('فشار مثانه یا بی‌اختیاری ادرار، کمردرد', 'Bladder pressure or incontinence, low back pain')])
S('corneal-ulcer', '001032', 'Corneal ulcers and infections', '7/9/2024', [('تاری دید', 'Blurred or hazy vision'), ('قرمزی چشم', 'Red or bloodshot eye'), ('خارش و ترشح', 'Itching and discharge'),
    ('حساسیت به نور', 'Sensitivity to light'), ('درد شدید و اشک‌ریزش', 'Very painful, watery eye'), ('لکه سفید روی قرنیه', 'White patch on the cornea')])
S('ophthalmia-neonatorum-prophylaxis', '001606', 'Neonatal conjunctivitis', '10/7/2025', [('ترشح چشم نوزاد ۱ روز تا ۲ هفته پس از تولد', 'Eye drainage 1 day to 2 weeks after birth'), ('پلک‌های پف‌کرده، قرمز و دردناک', 'Puffy, red, tender eyelids'),
    ('ترشح آبکی، خونی یا چرکی غلیظ', 'Watery, bloody or thick pus-like drainage')])
S('acute-coronary-syndrome', '007639', 'Acute coronary syndrome', '6/1/2026', [('درد قفسه سینه (شایع‌ترین)', 'Chest pain (most common)'), ('درد شانه، بازو، گردن، فک، پشت یا شکم', 'Pain in the shoulder, arm, neck, jaw, back or belly'),
    ('احساس فشار، فشردگی یا سوزش که با استراحت یا دارو بهتر نمی‌شود', 'Tightness, squeezing or burning that does not ease with rest or medicine'), ('تنگی نفس', 'Shortness of breath'), ('تهوع و تعریق', 'Nausea and sweating'),
    ('سرگیجه و ضربان سریع یا نامنظم', 'Dizziness and fast or irregular heartbeat')])
S('hyperaldosteronism', '000330', 'Primary and secondary hyperaldosteronism', '7/13/2025', [('فشار خون بالا', 'High blood pressure'), ('پتاسیم پایین خون', 'Low blood potassium'), ('خستگی دائمی', 'Constant tiredness'),
    ('سردرد', 'Headache'), ('ضعف عضلانی', 'Muscle weakness'), ('بی‌حسی', 'Numbness')])
S('rheumatic-fever-prophylaxis', '003940', 'Rheumatic fever', '1/14/2026', [('۲ تا ۴ هفته پس از گلودرد چرکی یا مخملک، بیشتر در ۵ تا ۱۵ سالگی', '2–4 weeks after strep throat or scarlet fever, mostly at 5–15 y'), ('تب، خون‌دماغ، درد شکم', 'Fever, nosebleeds, abdominal pain'),
    ('درد، تورم و گرمی مفاصل بزرگ که از مفصلی به مفصل دیگر جابه‌جا می‌شود', 'Painful, swollen, warm large joints that move from joint to joint'), ('درگیری قلب: تنگی نفس و درد قفسه سینه', 'Heart involvement: breathlessness and chest pain'),
    ('بثورات حلقوی روی تنه و ندول زیر پوست', 'Ring-shaped rash on the trunk and skin nodules'), ('کره سیدنهام: حرکات پرشی و بی‌ثباتی هیجانی', 'Sydenham chorea: jerky movements and emotional lability')])
S('fmf', '000363', 'Familial Mediterranean fever', '8/14/2026', [('حملات تکراری تب بالا (اوج ۱۲ تا ۲۴ ساعت)، معمولاً از ۵ تا ۱۵ سالگی', 'Recurrent high-fever attacks (peak 12–24 h), usually starting at 5–15 y'), ('درد شکم', 'Abdominal pain'),
    ('درد تیز قفسه سینه که با نفس بدتر می‌شود', 'Sharp chest pain worse on breathing in'), ('درد مفاصل', 'Joint pain'), ('ضایعات پوستی قرمز و متورم', 'Red, swollen skin lesions'), ('بین حملات بدون علامت', 'Symptom-free between attacks')])
S('ankylosing-spondylitis', '000420', 'Ankylosing spondylitis', '4/1/2025', [('کمردرد التهابی که شب و صبح بدتر است و با فعالیت بهتر می‌شود', 'Inflammatory low back pain worse at night and morning, better with activity'),
    ('خشکی و کاهش انعطاف ستون فقرات؛ خمیدگی به جلو در طول زمان', 'Spinal stiffness and loss of flexibility; stooped posture over time'), ('درد و تورم شانه، زانو و مچ پا', 'Painful, swollen shoulders, knees and ankles'),
    ('محدودیت باز شدن قفسه سینه', 'Limited chest expansion'), ('قرمزی و درد چشم (یووئیت)', 'Red, painful eye (uveitis)'), ('خستگی', 'Fatigue')])
S('calcium-oxalate-stones', '000458', 'Kidney stones', '1/12/2026', [('درد شدید ناگهانی و متناوب در پهلو یا شکم', 'Sudden severe, colicky flank or abdominal pain'), ('انتشار درد به کشاله ران، بیضه یا لابیا', 'Pain spreading to the groin, testicles or labia'),
    ('خون در ادرار یا تغییر رنگ ادرار', 'Blood in urine or abnormal urine colour'), ('تهوع و استفراغ', 'Nausea and vomiting'), ('تب و لرز (در عفونت همراه)', 'Fever and chills (with infection)')])
S('neuropathic-pain', '000593', 'Peripheral neuropathy', '5/4/2026', [('گزگز یا سوزش دست و پا که اغلب از انگشتان پا شروع می‌شود', 'Tingling or burning in hands and feet, often starting in the toes'), ('درد عمقی پا و ساق', 'Deep pain in the feet and legs'),
    ('بی‌حسی و کاهش حس به درد و دما', 'Numbness and loss of feeling for pain and temperature'), ('از دست دادن تعادل', 'Loss of balance'), ('ضعف عضلانی', 'Muscle weakness')])
S('alcohol-withdrawal', '000764', 'Alcohol withdrawal', '1/1/2025', [('شروع معمولاً ۸ ساعت پس از آخرین نوشیدنی، اوج ۲۴ تا ۷۲ ساعت', 'Usually starts within 8 h of the last drink, peaks at 24–72 h'), ('اضطراب، تحریک‌پذیری، لرزش', 'Anxiety, irritability, shakiness'),
    ('تعریق، تپش قلب، مردمک گشاد', 'Sweating, fast heart rate, dilated pupils'), ('بی‌خوابی، کابوس، تهوع و استفراغ', 'Insomnia, nightmares, nausea and vomiting'),
    ('دلیریوم ترمنس: گیجی شدید، توهم، تب و تشنج', 'Delirium tremens: severe confusion, hallucinations, fever and seizures')])
S('bipolar-maintenance', '000926', 'Bipolar disorder', '7/17/2024', [('مانیا: کاهش نیاز به خواب، پرحرفی، افکار پرشتاب', 'Mania: little need for sleep, talkativeness, racing thoughts'), ('رفتار پرخطر و بی‌پروا (خرج زیاد، قمار، مصرف مواد)', 'Reckless behaviour (overspending, gambling, substance use)'),
    ('تحریک‌پذیری شدید و باورهای غیرواقعی درباره خود', 'Very irritable mood and false beliefs about oneself'), ('افسردگی: غم روزانه، بی‌لذتی، کم‌انرژی', 'Depression: daily sadness, loss of pleasure, low energy'),
    ('احساس بی‌ارزشی و گناه؛ افکار مرگ یا خودکشی', 'Worthlessness and guilt; thoughts of death or suicide')])
S('folate-deficiency', '000551', 'Folate-deficiency anemia', '1/29/2026', [('خستگی', 'Fatigue'), ('ضعف', 'Weakness'), ('سردرد', 'Headache'), ('رنگ‌پریدگی', 'Pallor'), ('زخم و درد دهان و زبان', 'Sore mouth and tongue')])
S('b12-deficiency', '000569', 'Pernicious anemia', '1/29/2026', [('خستگی و سبکی سر هنگام ایستادن یا فعالیت', 'Fatigue and light-headedness on standing or exertion'), ('رنگ‌پریدگی و تنگی نفس هنگام فعالیت', 'Pale skin and breathlessness on exertion'),
    ('زبان قرمز و متورم یا خونریزی لثه', 'Swollen red tongue or bleeding gums'), ('اسهال یا یبوست، تهوع، بی‌اشتهایی', 'Diarrhoea or constipation, nausea, poor appetite'),
    ('بی‌حسی و گزگز دست و پا، اختلال تعادل', 'Numbness and tingling of hands and feet, poor balance'), ('گیجی، فراموشی، افسردگی', 'Confusion, memory loss, depression')])
S('diabetic-nephropathy', '000494', 'Diabetes and kidney disease', '1/10/2025', [('اغلب تا مراحل پیشرفته بی‌علامت', 'Often no symptoms until advanced'), ('خستگی و احساس ناخوشی', 'Fatigue and general ill feeling'), ('تورم پاها', 'Leg swelling'),
    ('تهوع، استفراغ و بی‌اشتهایی', 'Nausea, vomiting and poor appetite'), ('خارش پوست', 'Itchy skin'), ('تنگی نفس و ضربان نامنظم', 'Shortness of breath and irregular heartbeat')])
S('hypertriglyceridemia', '000397', 'Familial hypertriglyceridemia', '4/28/2026', [('معمولاً بدون علامت', 'Usually no symptoms'), ('گاهی بیماری عروق کرونر در سن پایین', 'Sometimes early coronary artery disease')])
S('pagets-disease', '000414', 'Paget disease of the bone', '10/19/2025', [('اغلب بی‌علامت و با عکس تصادفی کشف می‌شود', 'Often no symptoms; found on an incidental x-ray'), ('درد استخوان، مفصل یا گردن', 'Bone, joint or neck pain'),
    ('خمیدگی پاها و بدشکلی استخوان', 'Bowed legs and bone deformity'), ('بزرگ شدن سر و بدشکلی جمجمه', 'Enlarged head and skull deformity'), ('شکستگی', 'Fractures'), ('کاهش شنوایی و سردرد', 'Hearing loss and headache')])
S('strongyloidiasis', '000630', 'Strongyloidiasis', '11/10/2024', [('اغلب بی‌علامت', 'Often no symptoms'), ('درد بالای شکم', 'Upper abdominal pain'), ('سرفه', 'Cough'), ('اسهال و استفراغ', 'Diarrhoea and vomiting'),
    ('بثورات پوستی و کهیر اطراف مقعد', 'Rash and hive-like areas near the anus'), ('کاهش وزن و تب', 'Weight loss and fever')])
S('schistosomiasis', '001321', 'Schistosomiasis', '11/10/2024', [('خارش و بثورات محل ورود انگل به پوست', 'Itching and rash where the parasite entered the skin'), ('تب، لرز و تورم غدد لنفاوی', 'Fever, chills and swollen lymph nodes'),
    ('بزرگی کبد و طحال', 'Enlarged liver and spleen'), ('درد شکم و اسهال (گاه خونی)', 'Abdominal pain and diarrhoea (sometimes bloody)'), ('تکرر و سوزش ادرار و خون در ادرار', 'Frequent, painful urination and blood in the urine')])
EPS = [('کاهش حالت چهره', 'Reduced facial expression'), ('دشواری شروع و کنترل حرکت', 'Difficulty starting and controlling movement'), ('سفتی تنه، بازو یا پا', 'Stiffness of the trunk, arms or legs'),
       ('لرزش', 'Tremor'), ('صدای آهسته', 'Soft voice')]
S('drug-induced-eps', '000759', 'Secondary parkinsonism', '1/27/2026', EPS)
S('drug-induced-parkinsonism', '000759', 'Secondary parkinsonism', '1/27/2026', EPS)
S('ulcerative-colitis', '000250', 'Ulcerative colitis', '1/13/2026', [('درد و گرفتگی شکم', 'Abdominal pain and cramping'), ('اسهال با خون و گاه چرک', 'Diarrhoea with blood and sometimes pus'), ('احساس دفع ناتمام (تنسموس)', 'Urge to pass stool despite empty bowels (tenesmus)'),
    ('تب و کاهش وزن', 'Fever and weight loss'), ('کندی رشد در کودکان', 'Slowed growth in children'), ('درد مفاصل، التهاب چشم و ضایعات پوستی', 'Joint pain, eye irritation and skin lesions')])
S('gallstones', '000273', 'Gallstones', '4/21/2025', [('اغلب بی‌علامت', 'Often no symptoms'), ('درد بالا و راست شکم بیش از ۳۰ دقیقه (کولیک صفراوی)', 'Right or middle upper abdominal pain for at least 30 min (biliary colic)'),
    ('تب', 'Fever'), ('زردی پوست و چشم', 'Yellow skin and eyes (jaundice)'), ('مدفوع کم‌رنگ', 'Clay-coloured stools'), ('تهوع و استفراغ', 'Nausea and vomiting')])
S('dry-eye', '000426', 'Dry eye syndrome', '10/2/2024', [('تاری دید', 'Blurred vision'), ('سوزش، خارش یا قرمزی چشم', 'Burning, itching or redness of the eye'), ('احساس شن یا خراش در چشم', 'Gritty or scratchy feeling'), ('حساسیت به نور', 'Sensitivity to light')])
S('ocular-inflammation', '001005', 'Uveitis', '7/9/2024', [('تاری دید', 'Blurred vision'), ('لکه‌های تیره شناور در دید', 'Dark floating spots in vision'), ('درد چشم', 'Eye pain'), ('قرمزی چشم', 'Red eye'), ('حساسیت به نور', 'Sensitivity to light')])
S('alopecia', '001177', 'Male pattern baldness', '4/1/2025', [('عقب رفتن خط موی جلوی سر به شکل M', 'Receding front hairline in an M shape'), ('نازک شدن موی پشت سر (ورتکس)', 'Thinning at the crown (vertex)'),
    ('موهای ظریف‌تر، کوتاه‌تر و کم‌پشت‌تر', 'Hair becomes finer, shorter and thinner'), ('در نهایت الگوی نعل‌اسبی مو در اطراف سر', 'Eventually a horseshoe pattern of hair around the sides')])
S('dandruff', '000963', 'Seborrheic dermatitis', '4/1/2025', [('پوسته‌های سفید یا زرد چرب (شوره)', 'White or yellowish greasy scales (dandruff)'), ('پوست چرب و قرمزی خفیف', 'Greasy skin with mild redness'),
    ('خارش', 'Itching'), ('محل‌ها: پوست سر، ابرو، پلک، چین بینی، پشت گوش و وسط قفسه سینه', 'Sites: scalp, eyebrows, eyelids, nose creases, behind ears and mid-chest')])
S('contact-dermatitis-plants', '000027', 'Poison ivy - oak - sumac rash', '7/3/2025', [('خارش شدید', 'Intense itching'), ('بثورات قرمز رگه‌ای در محل تماس با گیاه', 'Red streaky rash where the plant touched'),
    ('برجستگی‌های قرمز و تاول‌های ترشح‌دار', 'Red bumps and weeping blisters'), ('بدترین علائم روز ۴ تا ۷؛ بهبود طی ۱ تا ۳ هفته', 'Worst on days 4–7; lasts 1–3 weeks')])
S('xerosis', '000835', 'Dry skin', '10/13/2024', [('پوست خشک، پوسته‌دار و خارش‌دار', 'Dry, scaly, itchy skin'), ('قرمزی', 'Redness'), ('ترک‌های ریز', 'Fine cracks'), ('بیشتر در دست و پا', 'Mostly on the arms and legs')])
S('beriberi', '000339', 'Beriberi', '7/23/2024', [('خشک: دشواری راه رفتن، بی‌حسی و گزگز دست و پا', 'Dry: difficulty walking, numbness and tingling of hands and feet'), ('ضعف یا فلج عضلات ساق', 'Weakness or paralysis of the lower legs'),
    ('گیجی، اختلال گفتار، نیستاگموس', 'Confusion, speech difficulty, nystagmus'), ('مرطوب: تنگی نفس با فعالیت و بیدار شدن شبانه', 'Wet: breathlessness on exertion and waking at night short of breath'),
    ('ضربان سریع و تورم ساق‌ها', 'Fast heart rate and swollen lower legs')])
S('organophosphate-poisoning', '002832', 'Insecticide poisoning', '10/14/2025', [('ترشح بزاق و اشک، مردمک تنگ', 'Drooling and tearing, small pupils'), ('خس‌خس و دشواری تنفس', 'Wheezing and breathing difficulty'), ('ضربان کند', 'Slow heart rate'),
    ('گرفتگی شکم، اسهال، تهوع و استفراغ، تکرر ادرار', 'Abdominal cramps, diarrhoea, nausea and vomiting, increased urination'), ('ضعف، سرگیجه، سردرد، تشنج و کما', 'Weakness, dizziness, headache, seizures and coma'),
    ('کبودی لب‌ها و ناخن‌ها', 'Blue lips and fingernails')])
S('opioid-overdose', '000948', 'Opioid intoxication', '4/8/2025', [('گیجی یا کاهش هوشیاری', 'Confusion or decreased responsiveness'), ('کند شدن تنفس تا توقف آن', 'Slowed breathing that may stop'), ('خواب‌آلودگی شدید', 'Extreme sleepiness'),
    ('تهوع و استفراغ', 'Nausea and vomiting'), ('مردمک‌های تنگ', 'Small pupils')])
S('hypoglycemia', '000386', 'Low blood sugar', '1/25/2026', [('لرزش، تعریق و گرسنگی', 'Shakiness, sweating and hunger'), ('ضربان تند', 'Fast, pounding heartbeat'), ('عصبی بودن، تحریک‌پذیری یا رفتار پرخاشگرانه', 'Nervousness, irritability or aggression'),
    ('سردرد، تاری یا دوبینی', 'Headache, blurred or double vision'), ('گزگز پوست، ضعف و خستگی', 'Tingling skin, weakness and tiredness'), ('افت شدید: گیجی، تشنج و بیهوشی', 'Severe: confusion, seizures and loss of consciousness')])
S('eclampsia', '000899', 'Eclampsia', '3/17/2026', [('تشنج در بارداری', 'Seizures in pregnancy'), ('بی‌قراری شدید، گیجی یا بیهوشی', 'Severe agitation, confusion or unconsciousness'), ('پیش از تشنج: سردرد', 'Before the seizure: headache'),
    ('تهوع، استفراغ و درد معده', 'Nausea, vomiting and stomach pain'), ('تورم دست و صورت', 'Swelling of the hands and face'), ('اختلال دید (تاری، دوبینی، از دست رفتن بخشی از میدان دید)', 'Vision problems (blurring, double vision, missing areas)')])

S('vitamin-k-deficiency-bleeding', '007320', 'Vitamin K deficiency bleeding of the newborn', '10/3/2025', [('خونریزی از محل ختنه یا ناف', 'Bleeding from the circumcision site or belly button'), ('خون در مدفوع نوزاد', 'Blood in the baby’s stools'),
    ('خونریزی از بینی، دهان یا محل سوزن', 'Bleeding from the nose, mouth or needle sites'), ('خون در ادرار و کبودی', 'Blood in urine and bruising'), ('تشنج یا رفتار غیرطبیعی از خونریزی داخل جمجمه', 'Seizures or abnormal behaviour from bleeding inside the skull')])
S('acute-allergic-reaction', '000005', 'Allergic reactions', '1/20/2026', [('خفیف: کهیر محدود، خارش، گرفتگی بینی، چشم قرمز و اشک‌آلود', 'Mild: a few hives, itching, nasal congestion, red watery eyes'), ('تورم صورت، چشم یا زبان', 'Swelling of the face, eyes or tongue'),
    ('خس‌خس، دشواری تنفس یا بلع', 'Wheezing, difficulty breathing or swallowing'), ('درد شکم، تهوع، استفراغ یا اسهال', 'Abdominal pain, nausea, vomiting or diarrhoea'), ('سرگیجه، تپش قلب، کهیر منتشر', 'Dizziness, palpitations, widespread hives'),
    ('شدید: بیهوشی', 'Severe: unconsciousness')])
S('fluid-replacement', '000982', 'Dehydration', '7/1/2025', [('تشنگی و خشکی دهان', 'Thirst and dry mouth'), ('ادرار کم و تیره', 'Little, dark urine'), ('پوست خشک و خنک، سردرد، گرفتگی عضله', 'Dry, cool skin, headache, muscle cramps'),
    ('شدید: بی‌ادراری، چشم‌های گود، پوست چروکیده', 'Severe: no urine, sunken eyes, shrivelled skin'), ('ضربان و تنفس تند، سرگیجه', 'Rapid heartbeat and breathing, dizziness'), ('گیجی، بی‌حالی، شوک یا بیهوشی', 'Confusion, listlessness, shock or unconsciousness')])
S('acute-pulmonary-edema', '000140', 'Pulmonary edema', '1/27/2026', [('تنگی نفس شدید و احساس غرق شدن', 'Severe breathlessness and a feeling of drowning'), ('تنگی نفس در حالت خوابیده؛ بیدار شدن شبانه با نفس‌تنگی', 'Breathlessness lying flat; waking at night gasping'),
    ('سرفه با خلط کف‌آلود خونی', 'Coughing up bloody froth'), ('خس‌خس یا صدای قل‌قل در تنفس', 'Wheezing or gurgling breath sounds'), ('اضطراب، تعریق زیاد و رنگ‌پریدگی', 'Anxiety, heavy sweating and pallor'), ('تورم پا یا شکم', 'Leg or abdominal swelling')])
S('gingivitis', '001056', 'Gingivitis', '2/5/2026', [('خونریزی لثه هنگام مسواک یا نخ دندان', 'Gums bleed on brushing or flossing'), ('لثه قرمز روشن یا ارغوانی', 'Bright red or purple-red gums'), ('لثه متورم، براق و حساس به لمس', 'Swollen, shiny gums tender to touch'),
    ('زخم دهان', 'Mouth sores'), ('بوی بد دهان', 'Bad breath')])
S('mouth-pain', '000998', 'Canker sore', '4/3/2025', [('زخم دردناک قرمز با مرکز سفید یا زرد', 'Painful red sore with a white or yellow centre'), ('محل: داخل گونه و لب، زبان، کام، پایه لثه', 'Sites: inner cheeks and lips, tongue, palate, gum base'),
    ('اندازه معمولاً کمتر از ۱ سانتی‌متر', 'Usually under 1 cm'), ('درد ۷ تا ۱۰ روز؛ بهبود کامل ۱ تا ۳ هفته', 'Pain lasts 7–10 days; full healing in 1–3 weeks'), ('گاهی تب و تورم غدد لنفاوی', 'Sometimes fever and swollen lymph nodes')])
S('premature-ejaculation', '001524', 'Premature ejaculation', '1/1/2025', [('انزال زودتر از زمان دلخواه، از پیش از دخول تا کمی پس از آن', 'Ejaculation earlier than desired, from before to just after penetration'), ('نارضایتی زوج', 'Dissatisfaction for the couple')])
S('male-hypogonadism', '000395', 'Male hypogonadism', '4/24/2025', [('کاهش میل جنسی', 'Low sex drive'), ('ناباروری', 'Infertility'), ('بزرگی پستان (ژنیکوماستی)', 'Breast enlargement (gynaecomastia)'), ('کاهش توده عضلانی', 'Loss of muscle mass'),
    ('ریزش موی زیربغل و ناحیه تناسلی، نیاز کمتر به اصلاح', 'Loss of armpit and pubic hair; shaving less often'), ('پیش از بلوغ: تأخیر بلوغ و رشد قدی کمتر', 'Before puberty: delayed puberty and less height gain')])
S('ventricular-arrhythmia', '000187', 'Ventricular tachycardia', '6/1/2026', [('تپش قلب', 'Palpitations'), ('سبکی سر یا سرگیجه', 'Light-headedness or dizziness'), ('غش', 'Fainting'), ('درد قفسه سینه', 'Chest discomfort'),
    ('تنگی نفس', 'Shortness of breath'), ('شروع و پایان ناگهانی؛ گاهی بی‌علامت', 'Starts and stops suddenly; sometimes no symptoms')])
S('adrenal-insufficiency', '000378', 'Addison disease', '4/24/2025', [('ضعف و خستگی شدید', 'Extreme weakness and fatigue'), ('فشار خون پایین و سرگیجه هنگام ایستادن', 'Low blood pressure and dizziness on standing'), ('تیره شدن پوست و مخاط دهان', 'Darkening of the skin and inner cheeks'),
    ('تهوع، استفراغ، اسهال مزمن و درد شکم', 'Nausea, vomiting, chronic diarrhoea and abdominal pain'), ('هوس نمک، کاهش وزن و اشتها', 'Salt craving, weight and appetite loss'), ('قند خون پایین و تب خفیف', 'Low blood sugar and low-grade fever')])
S('diabetes-insipidus', '000460', 'Central diabetes insipidus', '10/23/2025', [('ادرار زیاد', 'Large amounts of urine'), ('تشنگی شدید', 'Excessive thirst'), ('گیجی و کاهش هوشیاری اگر نتواند آب بنوشد (کم‌آبی و سدیم بالا)', 'Confusion and reduced alertness if unable to drink (dehydration, high sodium)')])
S('menopause-symptoms', '000894', 'Menopause', '7/3/2025', [('قاعدگی نامنظم و سپس قطع', 'Irregular, then stopped periods'), ('گرگرفتگی و تعریق شبانه', 'Hot flashes and night sweats'), ('تپش قلب و برافروختگی پوست', 'Heart pounding and skin flushing'),
    ('بی‌خوابی', 'Insomnia'), ('نوسان خلق، تحریک‌پذیری، افسردگی و اضطراب', 'Mood swings, irritability, depression and anxiety'), ('کاهش میل جنسی، خشکی واژن و نشت ادرار', 'Lower sex drive, vaginal dryness and urine leakage')])
S('breast-cancer', '000913', 'Breast cancer', '2/3/2025', [('سرطان زودرس اغلب بی‌علامت (اهمیت غربالگری)', 'Early cancer is often symptomless (screening matters)'), ('توده سفت، نامنظم و معمولاً بدون درد در پستان یا زیربغل', 'Hard, irregular, usually painless lump in the breast or armpit'),
    ('تغییر اندازه، شکل یا پوست پستان (پوست پرتقالی، فرورفتگی)', 'Change in breast size, shape or skin (orange-peel, dimpling)'), ('ترشح از نوک پستان', 'Nipple discharge'),
    ('پیشرفته: درد استخوان، تنگی نفس، کاهش وزن، تورم غدد زیربغل', 'Advanced: bone pain, breathlessness, weight loss, swollen armpit nodes')])
S('tuberculosis', '000077', 'Pulmonary tuberculosis', '11/10/2024', [('سرفه طولانی (معمولاً با خلط)', 'Prolonged cough (usually with mucus)'), ('سرفه خونی', 'Coughing up blood'), ('تب و تعریق شبانه', 'Fever and night sweats'),
    ('کاهش وزن و خستگی', 'Weight loss and fatigue'), ('درد قفسه سینه و تنگی نفس', 'Chest pain and breathlessness')])
S('malaria', '000621', 'Malaria', '5/12/2025', [('تب، لرز و تعریق (اغلب دوره‌ای)', 'Fever, chills and sweating (often cyclical)'), ('سردرد و درد عضلانی', 'Headache and muscle pain'), ('تهوع و استفراغ', 'Nausea and vomiting'),
    ('کم‌خونی و زردی', 'Anaemia and jaundice'), ('مدفوع خونی', 'Bloody stools'), ('شدید: تشنج و کما', 'Severe: seizures and coma')])
S('lupus', '000435', 'Systemic lupus erythematosus', '1/28/2025', [('درد و تورم مفاصل انگشتان، دست، مچ و زانو', 'Joint pain and swelling of fingers, hands, wrists and knees'), ('بثورات پروانه‌ای روی گونه‌ها و بینی که با آفتاب بدتر می‌شود', 'Butterfly rash on cheeks and nose, worse in sunlight'),
    ('خستگی، تب بی‌دلیل و کاهش وزن', 'Fatigue, unexplained fever and weight loss'), ('ریزش مو و زخم دهان', 'Hair loss and mouth sores'), ('درد قفسه سینه هنگام نفس عمیق', 'Chest pain on deep breathing'),
    ('حساسیت به نور خورشید و تورم غدد لنفاوی', 'Sun sensitivity and swollen lymph nodes')])
S('acetaminophen-overdose', '002598', 'Acetaminophen overdose', '1/8/2025', [('ممکن است تا ۱۲ ساعت یا بیشتر بی‌علامت باشد', 'Symptoms may not appear for 12 h or more'), ('درد شکم، تهوع و استفراغ', 'Abdominal pain, nausea and vomiting'), ('بی‌اشتهایی و تعریق', 'Loss of appetite and sweating'),
    ('زردی پوست و چشم', 'Yellow skin and eyes (jaundice)'), ('تحریک‌پذیری، تشنج و کما', 'Irritability, seizures and coma')])
S('rosacea', '000879', 'Rosacea', '7/3/2025', [('قرمزی صورت و برافروختگی آسان', 'Facial redness and easy flushing'), ('رگ‌های عنکبوتی صورت', 'Spider-like facial blood vessels'), ('قرمزی و گاه پیازی شدن بینی', 'Red, sometimes bulbous nose'),
    ('ضایعات شبیه آکنه', 'Acne-like sores'), ('سوزش یا گزش صورت', 'Burning or stinging of the face'), ('چشم‌های قرمز، تحریک‌شده و اشک‌آلود', 'Red, irritated, watery eyes')])
S('atopic-dermatitis', '000853', 'Atopic dermatitis', '10/13/2024', [('خارش', 'Itching'), ('پوست خشک یا برجستگی‌های ریز پشت بازو و جلوی ران', 'Dry skin or bumpy areas on the back of arms and front of thighs'), ('تاول‌های ترشح‌دار و دلمه‌بسته', 'Oozing, crusting blisters'),
    ('ضخیم و چرمی شدن پوست با خاراندن طولانی', 'Thickened, leathery skin from long scratching'), ('زیر ۲ سال: صورت، پوست سر، دست و پا؛ بزرگ‌ترها: پشت زانو و جلوی آرنج', 'Under 2 y: face, scalp, hands, feet; older: inside knees and elbows')])
S('diaper-dermatitis', '000964', 'Diaper rash', '7/1/2025', [('بثورات قرمز روشن در ناحیه پوشک', 'Bright red rash in the diaper area'), ('نواحی قرمز و پوسته‌دار روی اسکروتوم، آلت یا لابیا', 'Red, scaly areas on the scrotum, penis or labia'),
    ('جوش، تاول، زخم یا ضایعات چرکی', 'Pimples, blisters, sores or pus-filled lesions'), ('لکه‌های قرمز کوچک اطراف (ضایعات اقماری)', 'Small surrounding red patches (satellite lesions)')])
S('head-lice', '000840', 'Head lice', '1/1/2026', [('خارش پوست سر', 'Itchy scalp'), ('برجستگی‌های قرمز کوچک روی پوست سر، گردن و شانه', 'Small red bumps on the scalp, neck and shoulders'), ('ذرات سفید ریز (رشک) چسبیده به پایه مو', 'Tiny white specks (nits) stuck to the base of hairs')])
S('glaucoma', '001620', 'Glaucoma', '7/9/2024', [('زاویه باز: اغلب بی‌علامت تا آسیب شدید', 'Open-angle: usually no symptoms until damage is severe'), ('از دست رفتن تدریجی دید محیطی (دید تونلی)', 'Gradual loss of side vision (tunnel vision)'),
    ('زاویه بسته: درد شدید ناگهانی یک چشم', 'Angle-closure: sudden severe pain in one eye'), ('تاری دید، هاله رنگین‌کمانی دور نور، قرمزی چشم', 'Cloudy vision, rainbow halos around lights, red eye'), ('تهوع و استفراغ', 'Nausea and vomiting')])
S('severe-acne', '000873', 'Acne', '8/2/2025', [('جوش‌های سرسفید و سرسیاه', 'Whiteheads and blackheads'), ('برجستگی‌های قرمز و جوش‌های چرکی', 'Red bumps (papules) and pus-filled pimples (pustules)'), ('کیست', 'Cysts'),
    ('قرمزی اطراف ضایعات و دلمه', 'Redness around the lesions and crusting'), ('اسکار پوست', 'Skin scarring'), ('محل: صورت، شانه، تنه، بازو و باسن', 'Sites: face, shoulders, trunk, arms and buttocks')])
S('sore-throat', '000655', 'Pharyngitis - sore throat', '7/3/2025', [('گلودرد', 'Sore throat'), ('تب', 'Fever'), ('سردرد', 'Headache'), ('درد مفاصل و عضلات', 'Joint and muscle aches'), ('بثورات پوستی', 'Skin rash'), ('تورم غدد لنفاوی گردن', 'Swollen neck lymph nodes')])
S('chronic-urticaria', '000845', 'Hives', '4/1/2025', [('خارش', 'Itching'), ('برجستگی‌های قرمز یا هم‌رنگ پوست با حاشیه مشخص', 'Red or skin-coloured welts with clear edges'), ('بزرگ و به هم پیوسته شدن ضایعات', 'Welts enlarge and join'),
    ('تغییر شکل و جابه‌جایی طی دقیقه‌ها تا ساعت‌ها (معمولاً کمتر از ۴۸ ساعت)', 'Change shape and move within minutes to hours (usually <48 h)'), ('درموگرافیسم: کهیر در محل فشار یا خاراندن', 'Dermatographism: hives where the skin is pressed or scratched')])
S('chlamydia', '001345', 'Chlamydia', '5/18/2026', [('بسیاری بی‌علامت‌اند', 'Many have no symptoms'), ('سوزش ادرار', 'Burning on urination'), ('ترشح از آلت، واژن یا مقعد', 'Discharge from the penis, vagina or rectum'),
    ('درد بیضه در مردان', 'Testicular pain in men'), ('درد هنگام نزدیکی یا خونریزی پس از آن در زنان', 'Painful intercourse or bleeding afterwards in women'), ('درد یا ترشح مقعد', 'Rectal pain or discharge')])
S('epididymitis', '001279', 'Epididymitis', '9/2/2024', [('تب خفیف و لرز', 'Low fever and chills'), ('سنگینی و درد پیشرونده بیضه', 'Heaviness and increasing pain in the testicle'), ('تورم دردناک اسکروتوم', 'Painful scrotal swelling'),
    ('ترشح از مجرا، سوزش ادرار', 'Urethral discharge, burning on urination'), ('خون در منی و درد هنگام انزال', 'Blood in semen and painful ejaculation'), ('شبیه پیچ‌خوردگی بیضه — اورژانس باید رد شود', 'Can mimic testicular torsion — emergency must be excluded')])
S('pid', '000888', 'Pelvic inflammatory disease (PID)', '8/18/2025', [('تب', 'Fever'), ('درد لگن، زیر شکم یا کمر', 'Pelvic, lower belly or lower back pain'), ('ترشح واژن غیرطبیعی از نظر رنگ یا بو', 'Abnormal vaginal discharge (colour or smell)'),
    ('درد هنگام نزدیکی یا خونریزی پس از آن', 'Pain during or bleeding after intercourse'), ('درد و تکرر ادرار', 'Painful, frequent urination'), ('قاعدگی دردناک‌تر یا لکه‌بینی نامنظم', 'More painful periods or irregular spotting')])
S('prostatitis', '000519', 'Prostatitis - bacterial', '7/1/2025', [('تب، لرز و درد بدن (حاد)', 'Fever, chills and body aches (acute)'), ('سوزش ادرار و خون در ادرار', 'Burning urination and blood in urine'), ('دشواری شروع ادرار و جریان ضعیف', 'Difficulty starting and weak stream'),
    ('درد زیر شکم، کمر، پرینه یا بیضه', 'Pain above the pubic bone, lower back, perineum or testicles'), ('درد هنگام انزال یا دفع', 'Painful ejaculation or bowel movements')])
S('scarlet-fever', '000974', 'Scarlet fever', '1/14/2026', [('تب و گلودرد ۱ تا ۲ روز پس از عفونت', 'Fever and sore throat 1–2 days after infection'), ('بثورات زبر مثل سنباده از گردن و سینه شروع و منتشر می‌شود', 'Sandpaper-like rash starting on the neck and chest, then spreading'),
    ('قرمزی شدید چین زیربغل و کشاله ران', 'Bright red underarm and groin creases'), ('زبان قرمز و متورم (توت‌فرنگی)', 'Swollen red "strawberry" tongue'), ('پوسته‌ریزی سر انگشتان با کمرنگ شدن بثورات', 'Peeling of fingertips as the rash fades'),
    ('سردرد، درد شکم و استفراغ', 'Headache, abdominal pain and vomiting')])
S('c-diff', '000259', 'Pseudomembranous colitis', '4/27/2026', [('اسهال آبکی (اغلب ۵ تا ۱۰ بار در روز)', 'Watery diarrhoea (often 5–10 times a day)'), ('گرفتگی شکم', 'Abdominal cramps'), ('مدفوع خونی', 'Bloody stools'), ('تب', 'Fever'), ('احساس فوری دفع', 'Urge to have a bowel movement')])
S('sepsis', '000666', 'Sepsis', '8/29/2024', [('تب یا دمای پایین بدن', 'Fever or low body temperature'), ('لرز', 'Chills'), ('تنفس و ضربان سریع', 'Rapid breathing and heartbeat'), ('گیجی یا دلیریوم', 'Confusion or delirium'),
    ('سبکی سر از افت فشار و شوک', 'Light-headedness from low blood pressure and shock'), ('پوست ابلق یا بثورات', 'Mottled skin or rash')])
LEISH_C = [('زخم پوستی که به‌آرامی بهبود می‌یابد', 'Skin sore that becomes a slow-healing ulcer'), ('گرفتگی یا آبریزش بینی و خون‌دماغ (درگیری مخاط)', 'Stuffy or runny nose and nosebleeds (mucosal involvement)'),
           ('زخم و فرسایش دهان، لب و بینی', 'Ulcers and erosion of the mouth, lips and nose'), ('دشواری بلع یا تنفس در درگیری مخاطی', 'Difficulty swallowing or breathing with mucosal disease')]
S('cutaneous-leishmaniasis', '001386', 'Leishmaniasis', '8/5/2025', LEISH_C)
S('visceral-leishmaniasis', '001386', 'Leishmaniasis', '8/5/2025', [('تب طولانی هفته‌ها تا ماه‌ها، گاه دوره‌ای', 'Prolonged fever for weeks to months, sometimes cyclical'), ('کودکان: شروع ناگهانی با تب، سرفه، اسهال و استفراغ', 'Children: sudden onset with fever, cough, diarrhoea and vomiting'),
    ('خستگی، ضعف و بی‌اشتهایی', 'Fatigue, weakness and appetite loss'), ('ناراحتی شکم (بزرگی کبد و طحال)', 'Abdominal discomfort (enlarged liver and spleen)'), ('تعریق شبانه و کاهش وزن', 'Night sweats and weight loss'),
    ('پوست تیره و خاکستری، نازک شدن مو', 'Dark, greyish skin and thinning hair')])

S('hepatitis-b', '000279', 'Hepatitis B', '1/13/2026', [('ممکن است بی‌علامت باشد؛ علائم تا ۶ ماه پس از عفونت', 'May be symptomless; symptoms up to 6 months after infection'), ('بی‌اشتهایی، خستگی و تب خفیف', 'Appetite loss, fatigue and low fever'),
    ('درد عضلات و مفاصل', 'Muscle and joint aches'), ('تهوع و استفراغ', 'Nausea and vomiting'), ('زردی پوست و ادرار تیره', 'Yellow skin and dark urine'), ('مزمن: اغلب بی‌علامت تا آسیب کبد و سیروز؛ قابل انتقال حتی بدون علامت', 'Chronic: often symptomless until liver damage and cirrhosis; still contagious')])
S('hepatitis-c', '000284', 'Hepatitis C', '4/21/2025', [('اغلب بی‌علامت تا سیروز', 'Often no symptoms until cirrhosis'), ('خستگی', 'Fatigue'), ('درد بالای راست شکم', 'Right upper abdominal pain'), ('زردی، ادرار تیره و مدفوع کم‌رنگ', 'Jaundice, dark urine and pale stools'),
    ('تورم شکم (آسیت)', 'Abdominal swelling (ascites)'), ('خارش، بی‌اشتهایی، تهوع', 'Itching, poor appetite, nausea')])
S('invasive-fungal', '001326', 'Aspergillosis', '5/12/2025', [('سرفه، گاه با خون یا خلط قهوه‌ای', 'Cough, sometimes with blood or brown mucus plugs'), ('تب و لرز', 'Fever and chills'), ('خس‌خس و تنگی نفس', 'Wheezing and shortness of breath'),
    ('درد قفسه سینه', 'Chest pain'), ('کاهش وزن و احساس ناخوشی', 'Weight loss and malaise'), ('بسته به محل: سردرد، درد استخوان، ضایعات پوستی، اختلال دید', 'Depending on site: headache, bone pain, skin lesions, vision problems')])
S('hsv-encephalitis', '001415', 'Encephalitis', '7/16/2024', [('تب و سردرد', 'Fever and headache'), ('گیجی، خواب‌آلودگی و تحریک‌پذیری', 'Confusion, drowsiness and irritability'), ('حساسیت به نور، سفتی گردن', 'Light sensitivity, stiff neck'),
    ('ناپایداری راه رفتن و استفراغ', 'Unsteady gait and vomiting'), ('نوزاد: بی‌قراری، تغذیه ضعیف، برجستگی ملاج', 'Infants: irritability, poor feeding, bulging fontanelle'),
    ('اورژانس: تشنج، ضعف یا فلج، کاهش هوشیاری', 'Emergency: seizures, weakness or paralysis, reduced consciousness')])
S('cutaneous-candidiasis', '000880', 'Candida infection of the skin', '10/9/2024', [('خارش شدید', 'Intense itching'), ('بثورات قرمز رو به گسترش', 'Red, spreading rash'), ('محل: چین‌های پوست، ناحیه تناسلی، زیر پستان و باسن', 'Sites: skin folds, genitals, under the breasts and buttocks'),
    ('عفونت فولیکول مو شبیه جوش', 'Hair-follicle infection that looks like pimples')])
S('svt', '000183', 'Paroxysmal supraventricular tachycardia (PSVT)', '1/27/2026', [('تپش قلب سریع با شروع و پایان ناگهانی', 'Racing heartbeat that starts and stops suddenly'), ('نبض تند', 'Rapid pulse'), ('فشار قفسه سینه', 'Chest tightness'),
    ('تنگی نفس و اضطراب', 'Shortness of breath and anxiety'), ('سرگیجه یا غش', 'Dizziness or fainting')])
S('iron-poisoning', '002659', 'Iron overdose', '10/14/2025', [('۶ ساعت اول: تهوع، استفراغ خونی، اسهال و طعم فلزی', 'First 6 h: nausea, vomiting blood, diarrhoea, metallic taste'), ('مدفوع سیاه یا خونی', 'Black or bloody stools'),
    ('افت فشار، نبض تند و ضعیف، شوک', 'Low blood pressure, fast weak pulse, shock'), ('خواب‌آلودگی، تشنج و کما', 'Drowsiness, seizures and coma'), ('آسیب کبد و زردی چند روز بعد', 'Liver damage and jaundice days later'),
    ('بهبود ظاهری گذرا ممکن است فریبنده باشد', 'Temporary improvement can be misleading')])
S('toxic-alcohol', '002680', 'Methanol poisoning', '1/8/2025', [('تاری دید یا کوری کامل/نسبی («برف‌کوری»)، مردمک گشاد', 'Blurred vision or partial/complete blindness ("snow blindness"), dilated pupils'), ('سردرد، سرگیجه، گیجی', 'Headache, dizziness, confusion'),
    ('درد شدید شکم، تهوع و استفراغ (گاه خونی)', 'Severe abdominal pain, nausea and vomiting (sometimes bloody)'), ('دشواری تنفس', 'Breathing difficulty'), ('تشنج و کما', 'Seizures and coma'), ('افت فشار و کبودی لب', 'Low blood pressure and blue lips')])
S('methemoglobinemia', '000562', 'Methemoglobinemia', '5/1/2026', [('کبودی پوست (سیانوز)', 'Bluish skin (cyanosis)'), ('سردرد و سرگیجه', 'Headache and giddiness'), ('خستگی و بی‌انرژی', 'Fatigue and lack of energy'), ('تنگی نفس', 'Shortness of breath'),
    ('تغییر وضعیت ذهنی', 'Altered mental state')])
S('digoxin-toxicity', '000165', 'Digitalis toxicity', '5/5/2025', [('تهوع، استفراغ، اسهال و بی‌اشتهایی', 'Nausea, vomiting, diarrhoea and appetite loss'), ('نبض نامنظم یا تند', 'Irregular or fast pulse'), ('گیجی', 'Confusion'),
    ('اختلال دید: تاری، لکه کور، تغییر رنگ‌ها', 'Vision changes: blurring, blind spots, altered colours'), ('کاهش ادرار و تورم بدن', 'Reduced urine output and generalised swelling')])
S('tetanus-prophylaxis', '000615', 'Tetanus', '12/13/2025', [('اسپاسم عضلات فک (قفل شدن فک)', 'Jaw muscle spasm (lockjaw)'), ('اسپاسم گردن، قفسه سینه، شکم و پشت (قوس پشت)', 'Spasms of the neck, chest, abdomen and back (arched back)'),
    ('انقباض‌های ناگهانی و دردناک عضلانی', 'Sudden painful muscle contractions'), ('دشواری بلع و آبریزش دهان', 'Swallowing difficulty and drooling'), ('تب و تعریق زیاد', 'Fever and heavy sweating'), ('اختلال تنفس در درگیری عضلات تنفسی', 'Breathing problems if respiratory muscles are involved')])
S('rabies-exposure', '001334', 'Rabies', '8/29/2024', [('دوره نهفتگی معمولاً ۳ تا ۱۲ هفته (۱۰ روز تا ۷ سال)', 'Incubation usually 3–12 weeks (10 days to 7 years)'), ('درد، گزگز یا حساسیت محل گزش', 'Pain, tingling or sensitivity at the bite site'),
    ('ترس از آب و اسپاسم حنجره هنگام نوشیدن', 'Fear of water and throat spasm when drinking'), ('تب، سردرد، بی‌قراری و تغییر خلق', 'Fever, headache, restlessness and mood change'), ('آبریزش دهان و دشواری بلع', 'Drooling and difficulty swallowing'),
    ('توهم، تشنج و فلج', 'Hallucinations, seizures and paralysis')])
S('postpartum-depression', '007215', 'Postpartum depression', '7/17/2024', [('غم یا خلق افسرده که پس از ۲ هفته بهتر نمی‌شود یا ۱ ماه یا بیشتر پس از زایمان شروع می‌شود', 'Low mood not fading after 2 weeks or starting 1 month or more after birth'), ('اضطراب شدید، تحریک‌پذیری', 'Marked anxiety, irritability'),
    ('بی‌لذتی و بی‌انرژی', 'Loss of pleasure and energy'), ('احساس بی‌ارزشی یا گناه', 'Worthlessness or guilt'), ('اختلال خواب و اشتها', 'Sleep and appetite changes'), ('افکار مرگ یا خودکشی', 'Thoughts of death or suicide')])
S('apnea-of-prematurity', '007227', 'Apnea of prematurity', '1/15/2025', [('مکث‌های تنفسی در نوزاد نارس', 'Breathing pauses in a premature baby'), ('مکث بیش از ۲۰ ثانیه جدی است', 'Pauses over 20 seconds are serious'), ('افت ضربان قلب (برادیکاردی)', 'Drop in heart rate (bradycardia)'),
    ('افت اکسیژن خون (دسچوریشن)', 'Drop in oxygen saturation (desaturation)')])
S('neonatal-rds', '001563', 'Neonatal respiratory distress syndrome', '4/6/2025', [('شروع معمولاً چند دقیقه پس از تولد', 'Usually starts within minutes of birth'), ('تنفس سریع و سطحی', 'Rapid, shallow breathing'), ('ناله هنگام تنفس و باز شدن پره‌های بینی', 'Grunting and nasal flaring'),
    ('توکشیدگی قفسه سینه', 'Chest retractions'), ('کبودی پوست و مخاط', 'Bluish skin and mucous membranes'), ('مکث تنفسی و کاهش ادرار', 'Breathing pauses and reduced urine')])
S('pda', '001560', 'Patent ductus arteriosus', '10/1/2025', [('مجرای کوچک ممکن است بی‌علامت باشد', 'A small PDA may cause no symptoms'), ('تنفس سریع و تنگی نفس', 'Fast breathing and breathlessness'), ('نبض تند', 'Rapid pulse'),
    ('تغذیه ضعیف و تعریق هنگام شیر خوردن', 'Poor feeding and sweating while feeding'), ('خستگی زودرس و رشد ناکافی', 'Tiring easily and poor growth')])
S('rsv-prophylaxis', '001564', 'Respiratory syncytial virus (RSV)', '1/1/2026', [('علائم ۴ تا ۶ روز پس از عفونت', 'Symptoms 4–6 days after infection'), ('بزرگسال و کودک بزرگ‌تر: آبریزش بینی، سرفه، عطسه، تب و خس‌خس', 'Adults and older children: runny nose, cough, sneezing, fever, wheezing'),
    ('شیرخوار: بی‌قراری، کاهش فعالیت و تغذیه', 'Infants: irritability, less activity and feeding'), ('تنفس سریع، پره زدن بینی و دشواری تنفس', 'Rapid breathing, nasal flaring and laboured breathing'),
    ('کبودی پوست در موارد شدید — هر مشکل تنفسی شیرخوار اورژانس است', 'Bluish skin in severe cases — any breathing problem in an infant is an emergency')])
S('hypertensive-emergency', '000491', 'Malignant hypertension', '4/1/2025', [('سردرد', 'Headache'), ('تاری دید', 'Blurred vision'), ('درد قفسه سینه و تنگی نفس', 'Chest pain and shortness of breath'), ('تهوع یا استفراغ', 'Nausea or vomiting'),
    ('گیجی، کاهش هوشیاری یا تشنج', 'Confusion, reduced alertness or seizure'), ('بی‌حسی یا ضعف اندام یا صورت، کاهش ادرار', 'Numbness or weakness of limbs or face, reduced urine')])
S('intermittent-claudication', '000170', 'Peripheral artery disease - legs', '4/28/2026', [('درد، گرفتگی یا خستگی عضلات پا، ساق یا ران هنگام راه رفتن که با چند دقیقه استراحت بهتر می‌شود', 'Pain, cramping or fatigue in the feet, calves or thighs on walking, relieved by a few minutes of rest'),
    ('بدتر شدن با سربالایی یا راه رفتن سریع‌تر', 'Worse uphill or walking faster'), ('پای سرد و رنگ‌پریده یا بی‌حس', 'Cool, pale or numb legs'), ('شدید: درد شبانه یا در استراحت، زخم‌های بدون بهبود، پوست تیره و آبی', 'Severe: pain at night or rest, non-healing sores, dark blue skin'),
    ('اختلال نعوظ', 'Erectile dysfunction')])
S('stroke-tia', '000726', 'Stroke', '4/16/2025', [('ضعف یا بی‌حسی ناگهانی صورت، بازو یا پا (اغلب یک طرف)', 'Sudden weakness or numbness of the face, arm or leg (often one side)'), ('دشواری گفتار یا فهم', 'Trouble speaking or understanding'),
    ('اختلال دید ناگهانی', 'Sudden vision problems'), ('سرگیجه، اختلال تعادل و راه رفتن', 'Dizziness, loss of balance or coordination'), ('سردرد ناگهانی شدید (خونریزی مغزی)', 'Sudden severe headache (brain bleed)'),
    ('کاهش هوشیاری', 'Change in alertness')])
S('iron-overload', '000327', 'Hemochromatosis', '1/29/2026', [('اغلب بی‌علامت تا آسیب اندام', 'Often symptomless until organ damage'), ('خستگی و ضعف', 'Fatigue and weakness'), ('درد مفاصل', 'Joint pain'), ('درد شکم', 'Abdominal pain'),
    ('تیره یا برنزی شدن پوست', 'Bronze darkening of the skin'), ('کاهش میل جنسی، ریزش موی بدن و کاهش وزن', 'Low sex drive, loss of body hair and weight loss')])
S('sickle-cell', '000527', 'Sickle cell disease', '1/29/2026', [('حملات درد (کریز) در کمر، پا، مفاصل و قفسه سینه', 'Pain crises in the back, legs, joints and chest'), ('شروع معمولاً پس از ۴ ماهگی', 'Usually starts after 4 months of age'),
    ('خستگی، رنگ‌پریدگی، تنگی نفس و ضربان تند', 'Fatigue, pallor, breathlessness and fast heart rate'), ('زردی پوست و چشم', 'Yellow skin and eyes'), ('درد شکم در کودکان', 'Abdominal pain in children'),
    ('نعوظ دردناک طولانی، اختلال دید و زخم ساق پا', 'Painful prolonged erection, vision problems and leg ulcers')])
S('hyperkalemia', '001179', 'High potassium level', '10/1/2025', [('اغلب بی‌علامت', 'Often no symptoms'), ('تپش قلب و نبض نامنظم، کند یا ضعیف', 'Palpitations and irregular, slow or weak pulse'), ('درد قفسه سینه', 'Chest pain'),
    ('دشواری تنفس', 'Difficulty breathing'), ('تهوع یا استفراغ', 'Nausea or vomiting'), ('کلاپس ناگهانی', 'Sudden collapse')])
S('crohns', '000249', 'Crohn disease', '1/24/2025', [('درد کرامپی شکم', 'Crampy abdominal pain'), ('اسهال آبکی، گاه خونی', 'Watery diarrhoea, sometimes bloody'), ('تب و خستگی', 'Fever and fatigue'), ('بی‌اشتهایی و کاهش وزن', 'Appetite and weight loss'),
    ('فیستول یا ترشح اطراف مقعد', 'Fistula or drainage around the anus'), ('زخم دهان، درد مفاصل، التهاب چشم و ندول‌های پوستی', 'Mouth ulcers, joint pain, eye inflammation and skin nodules')])
S('melasma', '000836', 'Melasma', '10/13/2024', [('لکه‌های قهوه‌ای یکنواخت و معمولاً قرینه', 'Even brown, usually symmetrical patches'), ('محل: گونه، پیشانی، بینی یا لب بالا', 'Sites: cheeks, forehead, nose or upper lip'), ('بدون علامت دیگر', 'No other symptoms')])
S('actinic-keratosis', '000827', 'Actinic keratosis', '10/13/2024', [('ضایعات صاف و پوسته‌دار در نواحی آفتاب‌خورده (صورت، پوست سر، پشت دست، سینه)', 'Flat, scaly patches on sun-exposed skin (face, scalp, back of hands, chest)'),
    ('پوسته سفید یا زرد روی ضایعه', 'White or yellow crusty scale'), ('رنگ خاکستری، صورتی، قرمز یا هم‌رنگ پوست', 'Grey, pink, red or skin-coloured'), ('بعداً سفت، زبر و شبیه زگیل', 'Later hard, rough and wart-like')])
S('alcohol-use-disorder', '000944', 'Alcohol use disorder', '4/19/2025', [('نوشیدن بیش از برنامه یا ناتوانی در کم کردن', 'Drinking more than planned or unable to cut down'), ('ولع مصرف الکل', 'Craving alcohol'),
    ('صرف وقت زیاد برای تهیه، مصرف یا بهبود از اثر الکل', 'Much time spent getting, using or recovering from alcohol'), ('اختلال در کار، تحصیل یا روابط', 'Problems at work, school or in relationships'),
    ('ادامه با وجود آسیب سلامت یا موقعیت خطرناک (رانندگی)', 'Continuing despite health harm or risky situations (driving)'), ('تحمل و علائم ترک', 'Tolerance and withdrawal symptoms')])
S('absence-epilepsy', '000696', 'Absence seizure', '1/27/2026', [('دوره‌های خیره شدن چند ثانیه‌ای، چندین بار در روز', 'Staring spells of a few seconds, many times a day'), ('توقف ناگهانی صحبت یا راه رفتن و ادامه پس از چند ثانیه', 'Stops talking or walking and resumes after seconds'),
    ('پلک زدن سریع، ملچ‌ملچ لب یا حرکات دست', 'Eyelid fluttering, lip smacking or hand fumbling'), ('معمولاً زمین نمی‌خورد و پس از آن هوشیار و بی‌خبر است', 'Usually no fall; alert and unaware afterwards'), ('افت تحصیلی که با حواس‌پرتی اشتباه گرفته می‌شود', 'School problems mistaken for daydreaming')])
S('myasthenia-gravis', '000712', 'Myasthenia gravis', '4/16/2025', [('ضعف عضلانی که با فعالیت بدتر و با استراحت بهتر می‌شود', 'Muscle weakness worse with activity, better with rest'), ('افتادگی پلک و دوبینی (شایع‌ترین علائم اولیه)', 'Drooping eyelids and double vision (most common first signs)'),
    ('دشواری جویدن، بلع یا صحبت', 'Difficulty chewing, swallowing or talking'), ('ضعف بازوها و پاها (بالا رفتن از پله، برخاستن)', 'Limb weakness (stairs, rising from a chair)'), ('دشواری تنفس در موارد شدید', 'Breathing difficulty in severe cases')])
S('altitude-sickness', '000133', 'Acute mountain sickness', '10/14/2025', [('سردرد', 'Headache'), ('سرگیجه، خستگی و بی‌خوابی', 'Dizziness, fatigue and poor sleep'), ('بی‌اشتهایی، تهوع یا استفراغ', 'Loss of appetite, nausea or vomiting'), ('تنگی نفس با فعالیت و نبض تند', 'Breathlessness on exertion and fast pulse'),
    ('شدید (ادم ریه یا مغز ارتفاع): تنگی نفس در استراحت، سرفه خونی، گیجی، ناتوانی در راه رفتن مستقیم', 'Severe (HAPE/HACE): breathlessness at rest, coughing blood, confusion, inability to walk straight')])
S('hyperhidrosis', '007259', 'Hyperhidrosis', '6/3/2025', [('تعریق بیش از حد', 'Excessive sweating')])
S('malignant-hyperthermia', '001315', 'Malignant hyperthermia', '5/19/2025', [('افزایش سریع دمای بدن تا ۴۰٫۶ درجه یا بیشتر (حین بیهوشی)', 'Rapid rise in body temperature to 40.6 °C or higher (during anaesthesia)'), ('سفتی و رژیدیتی عضلات', 'Muscle rigidity and stiffness'),
    ('درد عضلانی بی‌دلیل', 'Unexplained muscle aches'), ('ادرار قهوه‌ای تیره (میوگلوبین)', 'Dark brown urine (myoglobin)'), ('خونریزی', 'Bleeding')])
S('cmv-infection', '000568', 'Cytomegalovirus (CMV) infection', '8/29/2024', [('اغلب بی‌علامت یا شبیه سرماخوردگی/آنفلوانزا', 'Often no symptoms or cold/flu-like'), ('تب، خستگی و احساس ناخوشی', 'Fever, fatigue and malaise'), ('بزرگی غدد لنفاوی گردن', 'Enlarged neck lymph nodes'),
    ('گلودرد، درد عضلانی، بثورات', 'Sore throat, muscle aches, rash'), ('در نقص ایمنی: درگیری ریه، گوارش یا شبکیه (کاهش دید)', 'In immunosuppression: lung, gut or retinal involvement (vision loss)')])
S('toxoplasmosis', '000637', 'Toxoplasmosis', '12/13/2025', [('اغلب بی‌علامت', 'Often no symptoms'), ('بزرگی غدد لنفاوی سر و گردن', 'Enlarged head and neck lymph nodes'), ('تب، سردرد و درد عضلانی', 'Fever, headache and muscle pain'), ('گلودرد و بیماری خفیف شبیه مونونوکلئوز', 'Sore throat and mild mono-like illness'),
    ('اختلال دید', 'Visual disturbances'), ('در نقص ایمنی: گیجی، تشنج و تاری دید از التهاب شبکیه', 'In immunosuppression: confusion, seizures and blurred vision from retinitis')])

S('leprosy', '001347', 'Leprosy', '8/5/2025', [('ضایعات پوستی کم‌رنگ‌تر از پوست طبیعی', 'Skin lesions lighter than normal skin'), ('کاهش حس لمس، گرما یا درد در ضایعه', 'Lesions with reduced sensation to touch, heat or pain'),
    ('ضایعاتی که هفته‌ها تا ماه‌ها بهبود نمی‌یابند', 'Lesions that do not heal for weeks to months'), ('ضعف عضلانی', 'Muscle weakness'), ('بی‌حسی دست، بازو، پا و ساق', 'Numbness of the hands, arms, feet and legs')])
S('dermatitis-herpetiformis', '001480', 'Dermatitis herpetiformis', '6/3/2025', [('برجستگی‌ها یا تاول‌های بسیار خارش‌دار', 'Extremely itchy bumps or blisters'), ('محل: آرنج، زانو، پشت و باسن، قرینه', 'Sites: elbows, knees, back and buttocks, symmetrical'),
    ('گاهی فقط آثار خاراندن و ساییدگی پوست', 'Sometimes only scratch marks and erosions'), ('آسیب روده با گلوتن (همه علائم گوارشی ندارند)', 'Gluten-related gut damage (not all have gut symptoms)')])
S('growth-hormone-deficiency', '001176', 'Growth hormone deficiency - children', '7/1/2025', [('رشد قدی کند یا ثابت روی منحنی رشد', 'Slow or flat growth on the growth chart'), ('قد بسیار کوتاه‌تر از همسالان', 'Much shorter than peers'),
    ('تناسب بدن طبیعی، گاهی چاق', 'Normal body proportions, sometimes chubby'), ('صورت جوان‌تر از سن', 'Face looks younger than age'), ('تأخیر یا نبود بلوغ', 'Delayed or absent puberty')])
S('cushing-disease', '000348', 'Cushing disease', '4/24/2025', [('چاقی تنه با دست و پای لاغر', 'Central obesity with thin arms and legs'), ('صورت گرد و قرمز (ماه‌گرفته) و کوهان پشت گردن', 'Round, red moon face and buffalo hump'),
    ('ترک‌های بنفش پهن روی شکم، ران، بازو و پستان', 'Wide purple stretch marks on abdomen, thighs, arms and breasts'), ('پوست نازک با کبودی آسان، آکنه', 'Thin skin with easy bruising, acne'),
    ('ضعف عضلانی، کمردرد و شکستگی استخوان', 'Muscle weakness, back pain and fractures'), ('دیابت، فشار خون و چربی بالا؛ کندی رشد در کودک', 'Diabetes, hypertension and high lipids; slow growth in children')])
S('immune-thrombocytopenia', '000535', 'Immune thrombocytopenic purpura (ITP)', '1/29/2026', [('نقاط قرمز ریز روی پوست (پتشی)، اغلب ساق پا', 'Pinpoint red spots on the skin (petechiae), often on the shins'), ('کبودی آسان', 'Easy bruising'),
    ('خون‌دماغ یا خونریزی دهان', 'Nosebleeds or bleeding in the mouth'), ('قاعدگی بسیار سنگین', 'Abnormally heavy periods')])
S('aplastic-anemia', '000554', 'Aplastic anemia', '1/29/2026', [('خستگی، ضعف و رنگ‌پریدگی', 'Fatigue, weakness and pallor'), ('ضربان تند و تنگی نفس با فعالیت', 'Fast heart rate and breathlessness on exertion'), ('سبکی سر هنگام ایستادن', 'Light-headedness on standing'),
    ('خونریزی لثه و بینی، کبودی آسان، پتشی', 'Bleeding gums and nose, easy bruising, petechiae'), ('عفونت‌های مکرر', 'Frequent infections')])
S('hemophilia-a', '000538', 'Hemophilia A', '1/29/2026', [('خونریزی طولانی (اغلب اول در ختنه)', 'Prolonged bleeding (often first noticed at circumcision)'), ('خونریزی داخل مفصل با درد و تورم', 'Bleeding into joints with pain and swelling'),
    ('خونریزی خودبه‌خود و کبودی', 'Spontaneous bleeding and bruising'), ('خون‌دماغ', 'Nosebleeds'), ('خونریزی طولانی پس از بریدگی، کشیدن دندان یا جراحی', 'Prolonged bleeding after cuts, tooth extraction or surgery'), ('خونریزی گوارشی یا ادراری', 'GI or urinary bleeding')])
S('acute-radiation-syndrome', '000026', 'Radiation sickness', '7/1/2025', [('تهوع و استفراغ (گاه خونی)', 'Nausea and vomiting (sometimes blood)'), ('اسهال و مدفوع خونی', 'Diarrhoea and bloody stools'), ('ضعف، خستگی، غش و گیجی', 'Weakness, fatigue, fainting and confusion'),
    ('خونریزی از بینی، دهان، لثه و مقعد؛ کبودی', 'Bleeding from nose, mouth, gums and rectum; bruising'), ('سوختگی و زخم پوست، ریزش مو', 'Skin burns and sores, hair loss'), ('تب و زخم دهان و گوارش', 'Fever and mouth/GI ulcers')])
S('tuberous-sclerosis', '000787', 'Tuberous sclerosis', '8/14/2026', [('لکه‌های سفید پوستی (برگ زبان‌گنجشک یا کنفتی)', 'White skin patches (ash-leaf or confetti)'), ('لکه‌های قرمز عروقی صورت (آنژیوفیبروم)', 'Red vascular facial patches (angiofibromas)'),
    ('پلاک‌های پوست پرتقالی روی کمر', 'Orange-peel-textured patches on the back (shagreen spots)'), ('تشنج', 'Seizures'), ('تأخیر تکاملی، ناتوانی ذهنی و اوتیسم', 'Developmental delay, intellectual disability and autism'),
    ('رشد زیر یا اطراف ناخن و فرورفتگی مینای دندان', 'Growths around the nails and pitted tooth enamel')])
S('cystic-fibrosis', '000107', 'Cystic fibrosis', '1/1/2026', [('نوزاد: عدم دفع مدفوع در ۲۴ تا ۴۸ ساعت اول، پوست شور', 'Newborn: no stool in the first 24–48 h, salty-tasting skin'), ('رشد و وزن‌گیری ناکافی', 'Poor growth and weight gain'),
    ('مدفوع کم‌رنگ، بدبو، چرب و شناور؛ نفخ و درد شکم', 'Pale, foul, greasy floating stools; bloating and abdominal pain'), ('سرفه و خلط زیاد', 'Cough and increased mucus'), ('پنومونی‌های مکرر', 'Repeated pneumonia'),
    ('گرفتگی بینی و درد سینوس (پولیپ)', 'Nasal congestion and sinus pain (polyps)')])
S('nasal-polyps', '001641', 'Nasal polyps', '7/28/2025', [('گرفتگی و انسداد بینی', 'Stuffy, blocked nose'), ('آبریزش بینی و عطسه', 'Runny nose and sneezing'), ('کاهش بویایی و چشایی', 'Loss of smell and taste'),
    ('سردرد و درد سینوس در عفونت همراه', 'Headache and sinus pain with infection'), ('خروپف', 'Snoring')])
S('lupus-nephritis', '000481', 'Lupus nephritis', '9/2/2025', [('خون در ادرار', 'Blood in the urine'), ('ادرار کف‌آلود', 'Foamy urine'), ('تورم (ادم)', 'Swelling (oedema)'), ('فشار خون بالا', 'High blood pressure')])
S('giant-cell-arteritis', '000448', 'Giant cell arteritis', '1/28/2025', [('سردرد ضربان‌دار جدید یک‌طرفه یا پشت سر', 'New throbbing headache on one side or the back of the head'), ('حساسیت پوست سر به لمس', 'Scalp tenderness'),
    ('درد فک هنگام جویدن', 'Jaw pain on chewing'), ('درد و خشکی گردن، شانه و لگن', 'Neck, shoulder and hip pain and stiffness'), ('تب، خستگی و احساس ناخوشی', 'Fever, fatigue and malaise'),
    ('تاری یا دوبینی، کاهش ناگهانی دید (اورژانس)', 'Blurred or double vision, sudden vision loss (emergency)')])
S('retinal-vein-occlusion', '007330', 'Retinal vein occlusion', '1/27/2026', [('تاری یا کاهش ناگهانی دید در یک چشم', 'Sudden blurring or loss of vision in one eye'), ('در تمام یا بخشی از میدان دید', 'In all or part of the visual field')])
S('presbyopia', '001026', 'Presbyopia', '1/27/2026', [('کاهش توانایی تمرکز روی اشیای نزدیک', 'Reduced ability to focus on near objects'), ('خستگی چشم', 'Eyestrain'), ('سردرد', 'Headache')])
S('acute-lymphoblastic-leukemia', '000541', 'Acute lymphoblastic leukemia (ALL)', '2/3/2025', [('درد استخوان و مفاصل', 'Bone and joint pain'), ('کبودی و خونریزی آسان، پتشی', 'Easy bruising and bleeding, petechiae'), ('ضعف، خستگی و رنگ‌پریدگی', 'Weakness, tiredness and pallor'),
    ('تب و تعریق شبانه', 'Fever and night sweats'), ('بی‌اشتهایی و کاهش وزن', 'Appetite and weight loss'), ('تورم غدد لنفاوی و احساس پری زیر دنده‌ها (بزرگی کبد/طحال)', 'Swollen lymph nodes and fullness below the ribs (enlarged liver/spleen)')])
S('ovarian-cancer', '000889', 'Ovarian cancer', '10/8/2024', [('علائم مبهم؛ اگر روزانه و بیش از چند هفته باشد بررسی شود', 'Vague symptoms; get checked if daily for more than a few weeks'), ('نفخ یا تورم شکم', 'Bloating or abdominal swelling'),
    ('سیری زودرس یا دشواری غذا خوردن', 'Early fullness or difficulty eating'), ('درد لگن یا زیر شکم و کمردرد', 'Pelvic or lower abdominal pain and back pain'), ('تکرر یا فوریت ادرار، یبوست', 'Urinary frequency or urgency, constipation')])
S('testicular-cancer', '001288', 'Testicular cancer', '5/1/2026', [('توده بدون درد در بیضه', 'Painless lump in the testicle'), ('بزرگی یا تغییر قوام بیضه', 'Enlarged testicle or change in feel'), ('سنگینی یا ناراحتی اسکروتوم', 'Heaviness or discomfort in the scrotum'),
    ('درد کمر یا زیر شکم', 'Back or lower abdominal pain'), ('بزرگی بافت پستان', 'Excess breast tissue')])
S('bladder-cancer', '000486', 'Bladder cancer', '1/29/2026', [('خون در ادرار', 'Blood in the urine'), ('درد هنگام ادرار', 'Painful urination'), ('تکرر و فوریت ادرار، بی‌اختیاری', 'Frequency, urgency and leakage of urine'), ('درد شکم', 'Abdominal pain'),
    ('خستگی و کاهش وزن', 'Fatigue and weight loss'), ('درد استخوان در انتشار', 'Bone pain if spread')])
S('lung-cancer', '000122', 'Lung cancer - small cell', '7/9/2025', [('سرفه', 'Cough'), ('خلط خونی', 'Bloody sputum'), ('درد قفسه سینه', 'Chest pain'), ('تنگی نفس و خس‌خس', 'Shortness of breath and wheezing'), ('بی‌اشتهایی و کاهش وزن', 'Appetite and weight loss'),
    ('دیررس: تورم صورت، گرفتگی صدا، دشواری بلع، ضعف', 'Later: facial swelling, hoarseness, swallowing difficulty, weakness')])
S('gastric-cancer', '000223', 'Stomach cancer', '10/14/2024', [('درد یا پری شکم حتی پس از غذای کم', 'Abdominal pain or fullness even after a small meal'), ('مدفوع تیره یا استفراغ خونی', 'Dark stools or vomiting blood'), ('دشواری بلع رو به افزایش', 'Worsening difficulty swallowing'),
    ('آروغ زیاد و تهوع', 'Excessive belching and nausea'), ('بی‌اشتهایی، کاهش وزن، ضعف و خستگی', 'Appetite loss, weight loss, weakness and fatigue')])
S('pancreatic-cancer', '000236', 'Pancreatic cancer', '7/9/2025', [('اغلب در ابتدا بی‌علامت و دیر تشخیص', 'Often symptomless early; found late'), ('درد بالای شکم', 'Upper abdominal pain'), ('زردی، خارش، ادرار تیره و مدفوع کم‌رنگ', 'Jaundice, itching, dark urine and pale stools'),
    ('بی‌اشتهایی، کاهش وزن، تهوع و استفراغ', 'Appetite loss, weight loss, nausea and vomiting'), ('خستگی و ضعف', 'Fatigue and weakness'), ('دیابت ناگهانی', 'Sudden-onset diabetes')])
S('acute-myeloid-leukemia', '000542', 'Acute myeloid leukemia - adult', '5/1/2026', [('خون‌دماغ، خونریزی لثه و کبودی', 'Nosebleeds, gum bleeding and bruising'), ('تب و خستگی', 'Fever and fatigue'), ('رنگ‌پریدگی و تنگی نفس با فعالیت', 'Pallor and breathlessness on exertion'),
    ('درد استخوان', 'Bone pain'), ('قاعدگی سنگین', 'Heavy periods'), ('کاهش وزن', 'Weight loss')])
S('multiple-myeloma', '000583', 'Multiple myeloma', '2/3/2025', [('درد استخوان، بیشتر دنده‌ها و کمر', 'Bone pain, mostly ribs and back'), ('شکستگی با فعالیت معمولی', 'Fractures with normal activity'), ('خستگی و تنگی نفس (کم‌خونی)', 'Fatigue and breathlessness (anaemia)'),
    ('عفونت‌های مکرر', 'Frequent infections'), ('خونریزی غیرطبیعی', 'Abnormal bleeding'), ('بی‌حسی یا ضعف اندام از فشار روی نخاع', 'Numbness or limb weakness from spinal compression')])
S('myelodysplastic-syndrome', '007716', 'Myelodysplastic syndrome', '10/21/2025', [('مراحل اولیه اغلب بی‌علامت', 'Often no symptoms early'), ('ضعف و خستگی (کم‌خونی)', 'Weakness and tiredness (anaemia)'), ('تنگی نفس', 'Shortness of breath'),
    ('کبودی و خونریزی آسان، پتشی', 'Easy bruising and bleeding, petechiae'), ('عفونت‌ها و تب مکرر', 'Frequent infections and fever')])
S('melanoma', '000850', 'Melanoma', '1/28/2026', [('خال یا ضایعه نامتقارن (A)', 'Asymmetric mole or lesion (A)'), ('حاشیه نامنظم (B)', 'Irregular border (B)'), ('چند رنگ: قهوه‌ای، سیاه، گاه سفید، قرمز یا آبی (C)', 'Mixed colours: tan, brown, black, sometimes white, red or blue (C)'),
    ('قطر معمولاً بیش از ۵ mm (D)', 'Diameter usually over 5 mm (D)'), ('تغییر مداوم ظاهر (E)', 'Changing appearance (E)'), ('ضایعه خونریزی‌دهنده یا متفاوت با سایر خال‌ها («جوجه اردک زشت»)', 'A bleeding lesion or one unlike other moles ("ugly duckling")')])
S('hydatid-disease', '000676', 'Echinococcosis', '7/16/2024', [('کیست‌ها ممکن است ۱۰ سال یا بیشتر بی‌علامت باشند', 'Cysts may cause no symptoms for 10 years or more'), ('کبد: درد بالای راست شکم و بزرگ شدن شکم', 'Liver: right upper abdominal pain and abdominal swelling'),
    ('ریه: سرفه، درد قفسه سینه و خلط خونی', 'Lung: cough, chest pain and bloody sputum'), ('پارگی کیست: واکنش آلرژیک شدید (آنافیلاکسی)', 'Cyst rupture: severe allergic reaction (anaphylaxis)')])
S('hypertension', '000468', 'High blood pressure in adults - hypertension', '2/13/2025', [('معمولاً بدون علامت (با اندازه‌گیری کشف می‌شود)', 'Usually no symptoms (found on measurement)'), ('آسیب بی‌صدای قلب و کلیه', 'Silent heart and kidney damage'),
    ('فشار بسیار بالا (بدخیم): سردرد شدید، تهوع و استفراغ', 'Very high (malignant): severe headache, nausea and vomiting'), ('گیجی، اختلال دید و خون‌دماغ', 'Confusion, vision changes and nosebleeds')])
S('chronic-suppurative-otitis', '000619', 'Ear infection - chronic', '1/1/2025', [('ترشح چرکی از گوش', 'Pus-like ear drainage'), ('کاهش شنوایی', 'Hearing loss'), ('درد خفیف یا احساس فشار در گوش', 'Mild ear pain or pressure'), ('تب خفیف', 'Low-grade fever'),
    ('بی‌قراری در شیرخوار', 'Fussiness in infants'), ('علائم پایدار یا متناوب، یک یا دو گوش', 'Persistent or recurring, one or both ears')])
S('hypomagnesemia', '000315', 'Magnesium deficiency', '5/19/2025', [('اسپاسم یا گرفتگی عضلات', 'Muscle spasms or cramps'), ('ضعف عضلانی', 'Muscle weakness'), ('بی‌حسی', 'Numbness'), ('خستگی', 'Fatigue'),
    ('حرکات غیرطبیعی چشم (نیستاگموس)', 'Abnormal eye movements (nystagmus)'), ('تشنج', 'Convulsions')])
S('secondary-hyperparathyroidism-ckd', '001215', 'Hyperparathyroidism', '5/18/2026', [('اغلب بی‌علامت', 'Often no symptoms'), ('درد استخوان و شکستگی آسان', 'Bone pain and fragile bones'), ('خستگی، ضعف و احساس ناخوشی', 'Tiredness, weakness and feeling unwell'),
    ('تکرر و افزایش ادرار، سنگ کلیه', 'Increased urination and kidney stones'), ('تهوع و بی‌اشتهایی', 'Nausea and appetite loss'), ('گیجی، افسردگی و فراموشی', 'Confusion, depression and forgetfulness')])
S('covid-19', '007768', 'Coronavirus disease 2019 (COVID-19)', '1/1/2025', [('تب و لرز', 'Fever and chills'), ('سرفه، گاه خونی', 'Cough, sometimes with blood'), ('تنگی نفس', 'Shortness of breath'), ('خستگی و درد عضلانی', 'Fatigue and muscle aches'),
    ('خطر شدید بیشتر در سالمندان و بیماری‌های زمینه‌ای (دیابت، قلب، ریه، کلیه، چاقی، نقص ایمنی، بارداری)', 'Higher risk of severe illness in older people and those with chronic conditions (diabetes, heart, lung, kidney, obesity, immunosuppression, pregnancy)')])
S('wet-amd', '001000', 'Age-related macular degeneration', '7/24/2025', [('ابتدا ممکن است بی‌علامت باشد', 'May have no symptoms at first'), ('نوع مرطوب: خطوط صاف موجدار و کج دیده می‌شوند (علامت اولیه)', 'Wet type: straight lines look wavy and distorted (early sign)'),
    ('لکه تیره در مرکز دید که بزرگ می‌شود', 'Dark central spot that enlarges'), ('تاری دید مرکزی و کم‌رنگ شدن رنگ‌ها', 'Blurred central vision and faded colours'), ('دشواری خواندن و تشخیص چهره', 'Trouble reading and recognising faces')])

if __name__ == '__main__' and len(sys.argv) == 1:
    json.dump(D, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')
    print('s13d ok', sum(1 for x in D if x.get('symptoms')))
