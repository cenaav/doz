"""Stage 10 — plague, STI gaps (chancroid, LGV, donovanosis, pubic lice, HPV), bites/stings, diabetes-related infections, neuromuscular disorders."""
import copy, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *
C = os.path.join(os.path.dirname(__file__), '..', '.cache')
S = json.load(open(os.path.join(C, 's10_setids.json')))
sid = lambda k: S[k][0]
ONE = {'min': 1, 'max': 1}
A13 = {'minAge': age(13, 'year')}

# --- diseases ---
add_disease('plague', 'طاعون (خیارکی، سپتی‌سمیک، ریوی)', 'Plague (bubonic, septicaemic, pneumonic)', ['plague', 'black death', 'طاعون', 'طاعون سیاه', 'مرگ سیاه', 'yersinia pestis', 'طاعون خیارکی', 'طاعون ریوی'], ['A20.9'], 'infectious')
add_disease('chancroid', 'شانکروئید (زخم نرم تناسلی)', 'Chancroid', ['chancroid', 'شانکروئید', 'زخم تناسلی', 'ducreyi'], ['A57'], 'infectious')
add_disease('lymphogranuloma-venereum', 'لنفوگرانولوم ونروم (LGV)', 'Lymphogranuloma venereum (LGV)', ['LGV', 'لنفوگرانولوم'], ['A55'], 'infectious')
add_disease('donovanosis', 'دونووانوز (گرانولوم اینگوینال)', 'Donovanosis (granuloma inguinale)', ['granuloma inguinale', 'donovanosis', 'دونووانوز', 'گرانولوم اینگوینال'], ['A58'], 'infectious')
add_disease('pubic-lice', 'شپش عانه (شپش ناحیه تناسلی)', 'Pubic (crab) lice', ['crabs', 'pubic lice', 'شپش عانه', 'شپش تناسلی', 'شپش خرچنگی'], ['B85.3'], 'dermatology')
add_disease('spider-bite', 'عنکبوت‌گزیدگی (بیوه سیاه، عنکبوت گوشه‌گیر)', 'Spider bite (black widow, recluse)', ['spider bite', 'black widow', 'رتیل', 'عنکبوت', 'بیوه سیاه', 'رتیل گزیدگی'], ['T63.31'], 'toxicology')
add_disease('diabetic-foot-infection', 'عفونت پای دیابتی', 'Diabetic foot infection', ['diabetic foot', 'پای دیابتی', 'زخم پای دیابتی', 'عفونت قند'], ['E11.621', 'L08.9'], 'infectious')
add_disease('mucormycosis', 'موکورمایکوزیس (قارچ سیاه)', 'Mucormycosis', ['mucormycosis', 'black fungus', 'قارچ سیاه', 'موکور', 'زیگومایکوزیس'], ['B46.9'], 'infectious')
add_disease('als', 'اسکلروز جانبی آمیوتروفیک (ALS)', 'Amyotrophic lateral sclerosis (ALS)', ['ALS', 'motor neuron disease', 'بیماری نورون حرکتی', 'لو گریگ'], ['G12.21'], 'neurology')
add_disease('huntington-chorea', 'کره هانتینگتون', 'Huntington disease chorea', ['huntington', 'chorea', 'هانتینگتون', 'کره'], ['G10'], 'neurology')
add_disease('tardive-dyskinesia', 'دیسکینزی دیررس', 'Tardive dyskinesia', ['TD', 'tardive', 'دیسکینزی تاخیری', 'دیسکینزی'], ['G24.01'], 'neurology')
add_disease('duchenne', 'دیستروفی عضلانی دوشن', 'Duchenne muscular dystrophy', ['DMD', 'muscular dystrophy', 'دوشن', 'دیستروفی عضلانی'], ['G71.01'], 'neurology')
add_disease('multiple-sclerosis', 'مولتیپل اسکلروزیس (MS عودکننده)', 'Multiple sclerosis (relapsing)', ['MS', 'ام اس', 'مالتیپل اسکلروزیس'], ['G35'], 'neurology')
add_disease('lambert-eaton', 'سندرم لامبرت-ایتون (LEMS)', 'Lambert-Eaton myasthenic syndrome', ['LEMS', 'لامبرت ایتون'], ['G73.1'], 'neurology')
add_disease('periodic-paralysis', 'فلج دوره‌ای (هیپو/هیپرکالمیک)', 'Primary periodic paralysis', ['periodic paralysis', 'فلج دوره ای', 'فلج متناوب'], ['G72.3'], 'neurology')
d = json.load(open(os.path.join(ROOT, 'diseases.json')))
for x in d:
    if x['id'] == 'genital-warts':
        x['synonyms'] = list(dict.fromkeys(x['synonyms'] + ['HPV', 'human papillomavirus', 'ویروس پاپیلومای انسانی', 'زیگیل', 'اچ پی وی']))
json.dump(d, open(os.path.join(ROOT, 'diseases.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'diseases.json'), 'a').write('\n')

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

symptoms('plague', [('خیارکی (شایع‌ترین): شروع ناگهانی ۲ تا ۸ روز پس از گزش کک — تب، لرز، سردرد، درد عضلانی', 'Bubonic (most common): sudden onset 2–8 days after a flea bite — fever, chills, headache, muscle pain'),
                    ('خیارکی: تورم صاف و دردناک غدد لنفاوی (بوبو) در کشاله ران، زیر بغل یا گردن', 'Bubonic: smooth, painful swollen lymph glands (buboes) in the groin, armpit or neck'),
                    ('سپتی‌سمیک (عفونت خون): درد شکم، تهوع، استفراغ، اسهال، ضعف شدید و شوک', 'Septicaemic (blood): abdominal pain, nausea, vomiting, diarrhoea, extreme weakness and shock'),
                    ('سپتی‌سمیک: خونریزی زیر پوست و اندام‌ها؛ سیاه شدن و مرگ بافت انگشتان دست و پا و بینی («مرگ سیاه»)', 'Septicaemic: bleeding into skin and organs; blackened, dying tissue of fingers, toes and nose (“Black Death”)'),
                    ('ریوی (خطرناک‌ترین، تنها نوع قابل انتقال بین انسان‌ها): سرفه شدید، خلط خونی، درد قفسه سینه، تنگی نفس', 'Pneumonic (most serious, the only form spread person to person): severe cough, bloody sputum, chest pain, shortness of breath'),
                    ('تشنج', 'Seizures')], ml('000596', 'Plague', '5/12/2025'))
symptoms('chancroid', [('برجستگی کوچک روی دستگاه تناسلی ۱ روز تا ۲ هفته پس از تماس که ظرف یک روز زخم می‌شود', 'A small genital bump 1 day–2 weeks after infection that turns into an ulcer within a day'),
                       ('زخم دردناک و نرم با لبه مشخص، کف خاکستری-زرد و خونریزی آسان', 'Painful, soft ulcer with sharp borders, grey-yellow base that bleeds easily'), ('مردان اغلب یک زخم؛ زنان اغلب ۴ زخم یا بیشتر', 'Men often one ulcer; women often 4 or more'),
                       ('درد هنگام ادرار و نزدیکی در زنان', 'Pain with urination and intercourse in women'), ('تورم غدد لنفاوی کشاله ران که ممکن است سر باز کند و آبسه تخلیه‌شونده بدهد', 'Swollen groin lymph nodes that may break through the skin as draining abscesses')],
         ml('000635', 'Chancroid', '8/5/2025'))
symptoms('lymphogranuloma-venereum', [('زخم کوچک بدون درد روی دستگاه تناسلی', 'Small painless genital sore'), ('تورم غدد لنفاوی کشاله ران در یک یا دو طرف', 'Swollen groin lymph nodes on one or both sides'),
                                      ('تخلیه چرک از غدد لنفاوی از راه پوست', 'Drainage through the skin from groin lymph nodes'), ('دفع دردناک؛ خون یا چرک از مقعد', 'Painful bowel movements; blood or pus from the rectum'), ('تورم و قرمزی پوست کشاله ران؛ تورم لابیا', 'Swelling and redness of the groin skin; labial swelling')],
         ml('000634', 'Lymphogranuloma venereum', '8/5/2025'))
symptoms('donovanosis', [('برجستگی‌های کوچک قرمز گوشتی روی دستگاه تناسلی یا اطراف مقعد (۱ تا ۱۲ هفته پس از تماس)', 'Small beefy-red bumps on the genitals or around the anus (1–12 weeks after contact)'), ('ندول‌های مخملی قرمز، اغلب بدون درد ولی با خونریزی آسان', 'Raised beefy-red velvety nodules, often painless but bleed easily'),
                         ('پیشرفت آهسته و تخریب بافت تناسلی و گسترش به کشاله ران', 'Slow spread destroying genital tissue, extending to the groin'), ('از دست رفتن رنگ پوست ناحیه تناسلی', 'Loss of skin colour around the genitals')], ml('000636', 'Donovanosis (granuloma inguinale)', '8/5/2025'))
symptoms('pubic-lice', [('خارش ناحیه موهای عانه، بدتر در شب', 'Itching in the pubic hair area, worse at night'), ('واکنش پوستی قرمز یا خاکستری-آبی محل گزش', 'Red or bluish-grey skin reaction at bite sites'), ('زخم ناحیه تناسلی از گزش و خاراندن', 'Genital sores from bites and scratching')],
         ml('000841', 'Pubic lice', '10/13/2024'))
symptoms('genital-warts', [('برجستگی‌های همرنگ پوست، صاف یا برجسته، یا شبیه گل‌کلم', 'Flesh-coloured flat or raised spots, or cauliflower-like growths'), ('زنان: داخل یا اطراف واژن و مقعد، روی دهانه رحم', 'Women: in or around the vagina and anus, on the cervix'),
                           ('مردان: آلت، کیسه بیضه، کشاله ران، ران، اطراف مقعد', 'Men: penis, scrotum, groin, thighs, around the anus'), ('گاهی خارش، رطوبت یا ترشح بیشتر، خونریزی پس از نزدیکی', 'Sometimes itching, dampness or more discharge, bleeding after sex')], ml('000886', 'Genital warts', '10/15/2024'))
symptoms('spider-bite', [('بیوه سیاه: درد سوزنی محل گزش، سپس ۱۵ دقیقه تا ۱ ساعت بعد درد عضلانی پخش‌شونده', 'Black widow: pinprick pain at the bite, then spreading muscle pain 15 min–1 h later'),
                         ('بیوه سیاه: درد شدید شکم یا قفسه سینه و گرفتگی عضلات (شبیه آپاندیسیت یا حمله قلبی)', 'Black widow: severe abdominal or chest pain and cramps (can mimic appendicitis or heart attack)'),
                         ('بیوه سیاه: تعریق و بزاق زیاد، فشار خون بالا، تنگی نفس، تهوع، بی‌قراری؛ در کودک تشنج', 'Black widow: sweating, salivation, high blood pressure, breathing difficulty, nausea, restlessness; seizures in children'),
                         ('عنکبوت گوشه‌گیر: درد چند ساعت پس از گزش، حلقه قرمز-بنفش، تب، لرز، خارش', 'Recluse: pain within hours, red-purple ring, fever, chills, itching'),
                         ('عنکبوت گوشه‌گیر: زخم بزرگ و گاهی بافت سیاه (اسکار) که ماه‌ها طول می‌کشد بهبود یابد', 'Recluse: large ulcer and sometimes black eschar that takes months to heal'), ('به‌ندرت: ادرار خونی، زردی، نارسایی کلیه، تشنج', 'Rarely: blood in urine, jaundice, kidney failure, seizures')],
         ml('002858', 'Black widow spider', '7/1/2025'), ml('002859', 'Brown recluse spider', '7/1/2025'))
symptoms('scorpion-sting', [('خفیف: سوزش یا گزگز محل نیش', 'Mild: tingling or burning at the sting'), ('حساسیت شدید به لمس محل نیش، تعریق', 'Marked sensitivity to touch at the sting, sweating'), ('آبریزش دهان، حس کلفت شدن زبان، اسپاسم حنجره', 'Drooling, thick-feeling tongue, laryngeal spasm'),
                            ('حرکات غیرارادی سر، چشم یا گردن؛ دوبینی', 'Random head, eye or neck movements; double vision'), ('اسپاسم عضلات، بی‌قراری، تشنج، فلج', 'Muscle spasms, restlessness, seizures, paralysis'), ('تنفس تند یا مشکل تنفسی', 'Rapid or difficult breathing'),
                            ('ضربان تند، کند یا نامنظم', 'Fast, slow or irregular heartbeat'), ('تهوع، استفراغ، دل‌پیچه، بی‌اختیاری ادرار و مدفوع', 'Nausea, vomiting, abdominal cramps, urinary or stool incontinence')], ml('002850', 'Scorpions', '7/1/2025'))
symptoms('snakebite', [('جای نیش، درد شدید و تورم محل گزش', 'Fang marks, severe pain and swelling at the bite'), ('خونریزی از زخم و تغییر رنگ پوست', 'Bleeding from the wound and skin discolouration'), ('مرگ بافت', 'Tissue death'),
                       ('تاری دید، افتادگی پلک، اشکال تنفسی، فلج (مارهای عصبی)', 'Blurred vision, drooping eyelids, breathing difficulty, paralysis (neurotoxic snakes)'), ('افت فشار، نبض تند و ضعیف، شوک', 'Low blood pressure, rapid weak pulse, shock'),
                       ('تهوع، استفراغ، تعریق، تشنگی، سرگیجه، غش', 'Nausea, vomiting, sweating, thirst, dizziness, fainting'), ('بی‌حسی و گزگز، تشنج', 'Numbness and tingling, seizures'), ('برخی گزش‌ها اول بی‌درد است و علائم ساعت‌ها بعد ظاهر می‌شود', 'Some bites are painless at first; major symptoms may appear hours later')],
         ml('000031', 'Snake bites', '10/14/2025'))
symptoms('mucormycosis', [('بینی-مغزی (شایع در دیابت کنترل‌نشده): تورم و بیرون‌زدگی چشم، دلمه سیاه در بینی', 'Rhinocerebral (common in uncontrolled diabetes): swollen, protruding eyes, dark scabs in the nose'),
                          ('درد یا گرفتگی سینوس و قرمزی پوست روی سینوس', 'Sinus pain or congestion and redness of the skin over the sinuses'), ('تب، سردرد، تغییر وضعیت ذهنی', 'Fever, headache, mental status changes'),
                          ('ریوی: سرفه، گاهی خلط خونی، تب، تنگی نفس', 'Pulmonary: cough, occasionally coughing blood, fever, shortness of breath'), ('گوارشی: درد شکم، مدفوع یا استفراغ خونی', 'GI: abdominal pain, bloody stool or vomit'),
                          ('پوستی: ناحیه سفت و گاهی دردناک با مرکز سیاه', 'Skin: hardened, sometimes painful area with a blackened centre')], ml('000649', 'Mucormycosis', '11/10/2024'))
symptoms('als', [('ضعف عضلانی که از یک اندام (دست یا پا) شروع و به‌تدریج پیشرفت می‌کند', 'Muscle weakness starting in one limb and slowly worsening'), ('اشکال در بالا رفتن از پله، راه رفتن و برخاستن', 'Difficulty climbing stairs, walking and getting up'),
                 ('اشکال در بلع، آبریزش دهان، خفگی', 'Difficulty swallowing, drooling, choking'), ('گفتار کند یا نامفهوم، گرفتگی صدا', 'Slow or slurred speech, hoarseness'), ('اشکال تنفسی', 'Breathing difficulty'),
                 ('پرش عضلانی (فاسیکولاسیون)، گرفتگی و سفتی عضلات', 'Muscle twitching (fasciculations), cramps and stiffness'), ('افتادن سر از ضعف گردن؛ کاهش وزن', 'Head drop from neck weakness; weight loss'), ('حواس سالم؛ تفکر معمولاً طبیعی', 'Senses intact; thinking usually normal')],
         ml('000688', 'Amyotrophic lateral sclerosis (ALS)', '5/4/2026'))
symptoms('huntington-chorea', [('حرکات ناگهانی، سریع و غیرارادی دست، پا، صورت (کره)', 'Quick, sudden, uncontrolled jerking of the arms, legs and face (chorea)'), ('شکلک‌های صورت؛ حرکات آهسته و کنترل‌نشده', 'Facial grimacing; slow uncontrolled movements'),
                               ('راه رفتن ناپایدار و با پاهای باز؛ زمین خوردن', 'Unsteady, wide-based gait; falls'), ('تحریک‌پذیری، نوسان خلق، بی‌قراری، توهم یا سایکوز', 'Irritability, moodiness, restlessness, hallucinations or psychosis'),
                               ('زوال عقل پیشرونده: گیجی، از دست دادن حافظه و قضاوت', 'Progressive dementia: confusion, loss of memory and judgement'), ('اشکال در بلع و گفتار', 'Difficulty swallowing and speaking')], ml('000770', 'Huntington disease', '4/16/2025'))
symptoms('tardive-dyskinesia', [('شکلک صورت (بیشتر پایین صورت)', 'Facial grimacing (mainly lower face)'), ('بیرون آوردن زبان، جویدن مکرر، حرکت فک', 'Tongue thrusting, repetitive chewing, jaw swinging'), ('پلک زدن سریع', 'Rapid eye blinking'),
                                ('حرکت انگشتان شبیه پیانو زدن', 'Piano-playing finger movements'), ('تکان دادن لگن، بی‌قراری', 'Pelvic rocking or thrusting, restlessness')], ml('000685', 'Tardive dyskinesia', '5/4/2026'))
symptoms('duchenne', [('شروع معمولاً پیش از ۶ سالگی در پسران', 'Usually starts before age 6 in boys'), ('ضعف عضلات که از پاها و لگن شروع می‌شود', 'Muscle weakness beginning in the legs and pelvis'), ('زمین خوردن مکرر، اشکال در دویدن، پریدن و بالا رفتن از پله', 'Frequent falls, trouble running, jumping and climbing stairs'),
                      ('اشکال در برخاستن از حالت درازکش', 'Trouble getting up from lying down'), ('ناتوانی پیشرونده در راه رفتن (اغلب تا ۱۲ سالگی ویلچر)', 'Progressive loss of walking (often a wheelchair by 12)'), ('ضعف عضله قلب و تنفس در نوجوانی و جوانی', 'Heart and breathing muscle weakness in teens and twenties'),
                      ('خستگی؛ گاهی مشکل یادگیری', 'Fatigue; sometimes learning difficulties')], ml('000705', 'Duchenne muscular dystrophy', '10/27/2025'))
symptoms('multiple-sclerosis', [('حمله‌هایی با علائم که روزها تا ماه‌ها طول می‌کشد و سپس بهبود نسبی', 'Attacks lasting days to months followed by remissions'), ('ضعف، بی‌حسی، گزگز یا سوزش در دست و پا', 'Weakness, numbness, tingling or burning in the limbs'),
                                ('عدم تعادل، اشکال در راه رفتن و هماهنگی، لرزش', 'Loss of balance, trouble walking and coordinating, tremor'), ('کاهش دید (معمولاً یک چشم)، دوبینی', 'Vision loss (usually one eye), double vision'),
                                ('مشکلات ادراری و روده: فوریت، تکرر، بی‌اختیاری، یبوست', 'Bladder and bowel problems: urgency, frequency, incontinence, constipation'), ('خستگی، افسردگی، مشکل حافظه و تمرکز', 'Fatigue, depression, memory and attention problems'),
                                ('تشدید با تب، حمام داغ، آفتاب یا استرس', 'Worsened by fever, hot baths, sun or stress')], ml('000737', 'Multiple sclerosis', '1/27/2026'))
symptoms('lambert-eaton', [('ضعف بیشتر در عضلات پا؛ اشکال در بالا رفتن از پله و برخاستن', 'Weakness mostly in the legs; trouble climbing stairs and standing up'), ('بهبود موقت ضعف پس از فعالیت', 'Weakness may improve briefly after exercise'),
                           ('افتادن سر، اشکال در جویدن، بلع و صحبت', 'Head drooping, trouble chewing, swallowing and talking'), ('تاری یا دوبینی', 'Blurred or double vision'), ('خشکی دهان و چشم، یبوست، کاهش تعریق، افت فشار ایستاده، اختلال نعوظ', 'Dry mouth and eyes, constipation, reduced sweating, dizziness on standing, erectile dysfunction')],
         ml('000710', 'Lambert-Eaton myasthenic syndrome', '5/4/2026'))
symptoms('periodic-paralysis', [('حمله‌های ضعف یا فلج عضلانی که می‌آید و می‌رود؛ قدرت طبیعی بین حمله‌ها', 'Attacks of muscle weakness or paralysis that come and go; normal strength between attacks'), ('بیشتر شانه و لگن؛ گاهی عضلات تنفس و بلع', 'Mostly shoulders and hips; sometimes breathing and swallowing muscles'),
                                ('بیشتر هنگام بیدار شدن یا استراحت پس از ورزش', 'Often on waking or resting after exercise'), ('تحریک با غذای پرکربوهیدرات یا پرنمک، استرس، سرما', 'Triggered by high-carbohydrate or salty meals, stress, cold'), ('هر حمله چند ساعت تا یک روز؛ هوشیاری حفظ می‌شود', 'Each attack lasts hours to a day; the person stays alert')],
         ml('000312', 'Hypokalemic periodic paralysis', '10/23/2025'))

# --- links from existing drugs (copy of a label-cited regimen under the new disease) ---
def clone(drug_id, src_id, new_id, disease, fa, en, notes=(), dur=None, refs=None):
    p = find(drug_id); d = json.load(open(p))
    r = copy.deepcopy(next(x for x in d['regimens'] if x['id'] == src_id))
    r.update(id=new_id, disease=disease, label=T(fa, en)); r['notes'] = list(r.get('notes', [])) + list(notes)
    if dur: r['durationDays'] = dur
    if refs: r['refs'] = refs
    d['regimens'] = [x for x in d['regimens'] if x['id'] != new_id] + [r]
    d['examples'] = [e for e in d['examples'] if e['regimen'] != new_id] + [dict(copy.deepcopy(e), regimen=new_id) for e in d['examples'] if e['regimen'] == src_id][:1]
    fix_bands(d); json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

Dx = 'fda-doxycycline'; Ind = lambda what_fa, what_en: note(f'برچسب داکسی‌سایکلین «{what_fa}» را در موارد مصرف آورده؛ دوز عمومی برچسب.', f'The doxycycline label lists “{what_en}” among indications; general label dosing.', [R(Dx, 'Indications and Usage')])
clone('doxycycline', 'adult', 'plague-adult', 'plague', 'طاعون — بزرگسال (دوز عمومی برچسب)', 'Plague — adult (general label dose)', [Ind('طاعون ناشی از یرسینیا پستیس', 'Plague due to Yersinia pestis')])
clone('doxycycline', 'severe-child', 'plague-child', 'plague', 'طاعون — کودک زیر ۴۵ kg (عفونت شدید): ۲٫۲ mg/kg هر ۱۲ ساعت', 'Plague — child <45 kg (severe infection): 2.2 mg/kg every 12 h', [Ind('طاعون ناشی از یرسینیا پستیس', 'Plague due to Yersinia pestis')])
clone('doxycycline', 'adult', 'chancroid', 'chancroid', 'شانکروئید — بزرگسال (دوز عمومی برچسب)', 'Chancroid — adult (general label dose)', [Ind('شانکروئید ناشی از هموفیلوس دوکره‌ای', 'Chancroid caused by Haemophilus ducreyi')])
clone('doxycycline', 'adult', 'lgv', 'lymphogranuloma-venereum', 'لنفوگرانولوم ونروم — بزرگسال (دوز عمومی برچسب)', 'LGV — adult (general label dose)', [Ind('لنفوگرانولوم ونروم ناشی از کلامیدیا تراکوماتیس', 'Lymphogranuloma venereum caused by Chlamydia trachomatis')])
clone('doxycycline', 'adult', 'donovanosis', 'donovanosis', 'گرانولوم اینگوینال — بزرگسال (دوز عمومی برچسب)', 'Granuloma inguinale — adult (general label dose)', [Ind('گرانولوم اینگوینال ناشی از کلبسیلا گرانولوماتیس', 'Granuloma inguinale caused by Klebsiella granulomatis')])
St = 'fda-streptomycin'; SInd = lambda fa, en: note(f'برچسب استرپتومایسین «{fa}» را در موارد مصرف آورده (وقتی داروی کم‌خطرتر مناسب نیست)؛ دوز عمومی «سایر عفونت‌ها».', f'The streptomycin label lists “{en}” (when less toxic agents are not suitable); general “other infections” dosing.', [R(St, 'Indications and Usage')])
clone('streptomycin', 'adult', 'plague-adult', 'plague', 'طاعون — بزرگسال: ۱ تا ۲ g در روز در دوزهای منقسم (عضلانی)', 'Plague — adult: 1–2 g/day in divided doses (IM)', [SInd('یرسینیا پستیس (طاعون)', 'Yersinia pestis (plague)')])
clone('streptomycin', 'child', 'plague-child', 'plague', 'طاعون — کودک: ۲۰ تا ۴۰ mg/kg/روز در دوزهای منقسم', 'Plague — child: 20–40 mg/kg/day in divided doses', [SInd('یرسینیا پستیس (طاعون)', 'Yersinia pestis (plague)')])
clone('streptomycin', 'adult', 'chancroid', 'chancroid', 'شانکروئید — بزرگسال (دوز عمومی برچسب)', 'Chancroid — adult (general label dose)', [SInd('هموفیلوس دوکره‌ای (شانکروئید)', 'H. ducreyi (chancroid)')])
clone('streptomycin', 'adult', 'donovanosis', 'donovanosis', 'گرانولوم اینگوینال — بزرگسال (دوز عمومی برچسب)', 'Granuloma inguinale — adult (general label dose)', [SInd('کالیماتوباکتریوم گرانولوماتیس (دونووانوز)', 'Calymmatobacterium granulomatis (donovanosis)')])
clone('hpv-vaccine', 'std', 'warts-prevent', 'genital-warts', 'پیشگیری از زگیل تناسلی (HPV نوع ۶ و ۱۱) — واکسیناسیون ۹ تا ۴۵ سال', 'Prevention of genital warts (HPV 6 and 11) — vaccination 9–45 y',
      [note('برچسب Gardasil 9: پیشگیری از زگیل تناسلی (کوندیلوما) ناشی از HPV نوع ۶ و ۱۱. درمان زگیل موجود نیست.', 'Gardasil 9 label: prevention of genital warts (condyloma acuminata) caused by HPV types 6 and 11. It does not treat existing warts.', [R('fda-gardasil', '1.1')])])
clone('linezolid', 'adult', 'dfi', 'diabetic-foot-infection', 'عفونت پای دیابتی بدون استئومیلیت — ۱۲ سال به بالا ۶۰۰ mg هر ۱۲ ساعت', 'Diabetic foot infection without osteomyelitis — ≥12 y 600 mg every 12 h',
      [note('برچسب: عفونت عارضه‌دار پوست شامل پای دیابتی بدون استئومیلیت همزمان.', 'Label: complicated skin infections including diabetic foot infections without concomitant osteomyelitis.', [R('fda-linezolid', '1')])])

Cp = 'fda-ciprofloxacin'; Lv = 'fda-levofloxacin'; Mx = 'fda-moxifloxacin'
ANIMAL = lambda src, sec: note('تأیید طاعون بر اساس مطالعات حیوانی است (مطالعه انسانی ممکن نبود). شروع هرچه زودتر پس از تماس یا تشخیص.', 'Plague approval is based on animal studies (human trials not feasible). Start as soon as possible after exposure or diagnosis.', [R(src, sec)])
patch('ciprofloxacin', add_regs=[
    reg('plague', 'plague', T('طاعون (درمان یا پیشگیری) — بزرگسال ۵۰۰ تا ۷۵۰ mg هر ۱۲ ساعت، ۱۴ روز', 'Plague (treatment or prophylaxis) — adult 500–750 mg every 12 h, 14 days'), A18, 'fixed', {'perDose': 500, 'perDoseMax': 750, 'dosesPerDay': 2}, [R(Cp, '2.1')], dur={'min': 14, 'max': 14}, notes=[ANIMAL(Cp, '1.8')]),
    reg('plague-child', 'plague', T('طاعون — کودک (تولد تا ۱۷ سال): ۱۵ mg/kg هر ۸ تا ۱۲ ساعت (حداکثر ۵۰۰ mg)، ۱۴ روز', 'Plague — child (birth–17 y): 15 mg/kg every 8–12 h (max 500 mg), 14 days'), {'maxAge': age(18, 'year')}, 'weightBased', {'perKgPerDose': 15, 'intervalHours': 12}, [R(Cp, '2.2')],
        limits={'maxPerDose': 500, 'refs': [R(Cp, '2.2')]}, dur={'min': 14, 'max': 14}, allowed=['susp-250', 'susp-500'], notes=[ANIMAL(Cp, '1.8'), note('ماشین‌حساب فاصله را ۱۲ ساعت نشان می‌دهد؛ برچسب ۸ تا ۱۲ ساعت.', 'The calculator shows 12-hourly; the label allows every 8–12 h.', [R(Cp, '2.2')])])],
    add_exs=[ex('plague', 'tab-500', {'perDose': 500, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('plague-child', 'susp-250', {'perDose': 300, 'mlPerDose': 6}, ageYears=6, weightKg=20)])
patch('levofloxacin', add_regs=[
    reg('plague', 'plague', T('طاعون — بزرگسال و کودک ≥۵۰ kg: ۵۰۰ mg هر ۲۴ ساعت، ۱۰ تا ۱۴ روز', 'Plague — adults and children ≥50 kg: 500 mg every 24 h, 10–14 days'), {'minAge': age(6, 'month'), 'minWeightKg': 50}, 'fixed', {'perDose': 500, 'dosesPerDay': 1}, [R(Lv, '2.1'), R(Lv, '2.2, Table 2')], dur={'min': 10, 'max': 14}, notes=[ANIMAL(Lv, '1.8')]),
    reg('plague-child', 'plague', T('طاعون — کودک ۳۰ تا <۵۰ kg: ۲۵۰ mg هر ۱۲ ساعت، ۱۰ تا ۱۴ روز', 'Plague — child 30 to <50 kg: 250 mg every 12 h, 10–14 days'), {'minAge': age(6, 'month'), 'maxAge': age(18, 'year'), 'minWeightKg': 30, 'maxWeightKg': 49.99}, 'fixed', {'perDose': 250, 'dosesPerDay': 2}, [R(Lv, '2.2, Table 2')],
        dur={'min': 10, 'max': 14}, allowed=['tab-250'], notes=[ANIMAL(Lv, '1.8'), note('زیر ۳۰ kg قرص مناسب نیست؛ فرآورده دیگر لازم است.', 'Tablets cannot be used under 30 kg; another formulation is needed.', [R(Lv, '2.2')])])],
    add_exs=[ex('plague', 'tab-500', {'perDose': 500, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70), ex('plague-child', 'tab-250', {'perDose': 250, 'tabletsPerDoseRounded': 1}, ageYears=11, weightKg=38)])
patch('moxifloxacin', add_regs=[reg('plague', 'plague', T('طاعون (درمان یا پیشگیری) — بزرگسال ۴۰۰ mg یک بار در روز، ۱۰ تا ۱۴ روز', 'Plague (treatment or prophylaxis) — adult 400 mg once daily, 10–14 days'), A18, 'fixed', {'perDose': 400, 'dosesPerDay': 1}, [R(Mx, '2.1')], dur={'min': 10, 'max': 14}, notes=[ANIMAL(Mx, '1.5')])],
      add_exs=[ex('plague', 'tab-400', {'perDose': 400, 'tabletsPerDoseRounded': 1}, ageYears=40, weightKg=70)])
Az = 'fda-zithromax'; AZ1 = ['tab-250', 'tab-500']
patch('azithromycin', add_regs=[
    reg('chancroid', 'chancroid', T('شانکروئید (زخم تناسلی مردان) — یک دوز واحد ۱ g', 'Chancroid (genital ulcer disease in men) — single 1 g dose'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Az, '2.1')], dur=ONE, allowed=AZ1,
        notes=[note('اثربخشی در زنان به دلیل تعداد کم در کارآزمایی ثابت نشده است.', 'Efficacy in women has not been established (few women studied).', [R(Az, '1.1')])]),
    reg('ngu', 'chlamydia', T('اورتریت و سرویسیت غیرگنوکوکی (کلامیدیا) — یک دوز واحد ۱ g', 'Non-gonococcal urethritis and cervicitis (chlamydia) — single 1 g dose'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Az, '2.1')], dur=ONE, allowed=AZ1),
    reg('gono', 'gonorrhea', T('اورتریت و سرویسیت گنوکوکی — یک دوز واحد ۲ g', 'Gonococcal urethritis and cervicitis — single 2 g dose'), A18, 'fixed', {'perDose': 2000, 'dosesPerDay': 1}, [R(Az, '2.1')], dur=ONE, allowed=AZ1)],
    add_exs=[ex('chancroid', 'tab-500', {'perDose': 1000, 'tabletsPerDoseRounded': 2}, ageYears=30, weightKg=75), ex('ngu', 'tab-500', {'perDose': 1000, 'tabletsPerDoseRounded': 2}, ageYears=25, weightKg=65),
             ex('gono', 'tab-500', {'perDose': 2000, 'tabletsPerDoseRounded': 4}, ageYears=25, weightKg=65)])

# --- new drugs: STI / lice ---
Vg = fda('veregen', 'FDA Veregen', 'Veregen (sinecatechins) 15% ointment — Prescribing Information', sid('veregen'))
drug('sinecatechins', 'dermatology', 'پماد سینکاتچین (عصاره چای سبز)', 'Sinecatechins ointment', T('عصاره چای سبز موضعی (ضد زگیل)', 'Topical green-tea extract (anti-wart)'), [{'name': 'Veregen', 'market': 'US'}], ['veregen', 'سینکاتچین', 'پماد چای سبز'],
     [unitform('oint', 'ointment', 'topical', 'Sinecatechins 15% ointment (30 g tube)', [R(Vg, '3')])],
     [reg('warts', 'genital-warts', T('زگیل خارجی تناسلی و اطراف مقعد (۱۸ سال به بالا) — سه بار در روز تا ۱۶ هفته', 'External genital and perianal warts (≥18 y) — three times daily up to 16 weeks'), A18, 'notCalculated',
          {'reason': T('حدود ۰٫۵ cm پماد روی هر زگیل با انگشت، لایه نازک؛ سه بار در روز تا پاک شدن کامل، حداکثر ۱۶ هفته. شستن قبل از نوبت بعد لازم نیست. نه برای چشم، دهان، داخل واژن یا داخل مقعد.', 'About 0.5 cm strand per wart dabbed on with a finger, thin layer; three times daily until complete clearance, max 16 weeks. No need to wash off before the next dose. Not for eye, mouth, intravaginal or intra-anal use.')},
          [R(Vg, '2.1'), R(Vg, '2.2')])],
     warn=[W('برای HPV داخل مجرای ادرار، واژن، دهانه رحم یا مقعد نه؛ روی زخم باز نه؛ ناحیه از نور خورشید و UV دور بماند.', 'Not for urethral, intravaginal, cervical, rectal or intra-anal HPV disease; avoid open wounds; avoid sun/UV exposure of the treated area.', [R(Vg, '5')])])

Rd = fda('rid', 'FDA RID kit', 'RID lice treatment (pyrethrum extract 0.33% + piperonyl butoxide 4%) — Drug Facts', sid('rid'))
drug('pyrethrins-pbo', 'antiparasitic', 'شامپو پیرترین + پیپرونیل بوتوکساید (ضد شپش)', 'Pyrethrins + piperonyl butoxide', T('ضد شپش موضعی', 'Topical pediculicide'), [{'name': 'RID', 'market': 'US'}], ['rid', 'pyrethrins', 'شامپو ضد شپش', 'پیرترین'],
     [unitform('sh', 'shampoo', 'topical', 'Shampoo: pyrethrum extract (0.33% pyrethrins) + piperonyl butoxide 4%', [R(Rd, 'Active ingredients')])],
     [reg('pubic', 'pubic-lice', T('شپش عانه — روی موی خشک ناحیه، ۱۰ دقیقه، شستشو؛ تکرار پس از ۷ تا ۱۰ روز', 'Pubic lice — to dry hair of the area, 10 min, wash off; repeat in 7–10 days'), {'minAge': age(2, 'year')}, 'notCalculated',
          {'reason': T('روی موی خشک یا ناحیه درگیر کامل بمالید، ۱۰ دقیقه (نه بیشتر) بماند، با آب گرم کف کرده و آبکشی شود؛ رشک‌ها با شانه برداشته شوند. درمان دوم پس از ۷ تا ۱۰ روز لازم است. زیر ۲ سال با نظر پزشک. نه برای مژه و ابرو.', 'Apply thoroughly to dry hair or the affected area, leave 10 minutes (no longer), lather with warm water and rinse; remove nits with the comb. A second treatment is needed in 7–10 days. Under 2: ask a doctor. Not for eyelashes or eyebrows.')},
          [R(Rd, 'Directions'), R(Rd, 'Uses')]),
      reg('head', 'head-lice', T('شپش سر — همان روش؛ تکرار پس از ۷ تا ۱۰ روز', 'Head lice — same method; repeat in 7–10 days'), {'minAge': age(2, 'year')}, 'notCalculated',
          {'reason': T('اول پشت گوش و گردن، روی موی خشک؛ ۱۰ دقیقه، سپس شامپو و آبکشی و شانه رشک. درمان دوم ۷ تا ۱۰ روز بعد.', 'First behind the ears and back of the neck, on dry hair; 10 minutes, then lather, rinse and comb out nits. Second treatment 7–10 days later.')}, [R(Rd, 'Directions')])],
     warn=[W('نزدیک چشم، داخل بینی، دهان یا واژن نه. حساسیت به گل ابروسی (رگوید) ممکن است تنگی نفس یا حمله آسم بدهد.', 'Not near the eyes or inside the nose, mouth or vagina. Ragweed allergy: may cause breathing difficulty or an asthma attack.', [R(Rd, 'Warnings')])])

# --- diabetes-related infections ---
Ep = fda('ertapenem', 'FDA Ertapenem', 'Ertapenem for injection 1 g (Apotex) — Prescribing Information', sid('invanz'))
EPT = {'minAge': age(3, 'month'), 'maxAge': age(13, 'year')}
drug('ertapenem', 'anti-infectives', 'ارتاپنم', 'Ertapenem', T('کارباپنم', 'Carbapenem'), [{'name': 'Invanz', 'market': 'US'}], ['invanz', 'اینوانز', 'ارتاپنم'],
     [form('vial-1g', 'powder-for-injection', 'iv', '1 g vial (IV or IM)', 1000, 'mg', [R(Ep, '3')], per='vial')],
     [reg('dfi', 'diabetic-foot-infection', T('عفونت پای دیابتی بدون استئومیلیت — ۱۳ سال به بالا ۱ g یک بار در روز، ۷ تا ۱۴ روز', 'Diabetic foot infection without osteomyelitis — ≥13 y 1 g once daily, 7–14 days'), A13, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Ep, '2.2, Table 1')], dur={'min': 7, 'max': 14},
          notes=[note('در پای دیابتی با استئومیلیت همزمان بررسی نشده است. انفوزیون ۳۰ دقیقه‌ای؛ با دکستروز رقیق نشود.', 'Not studied in diabetic foot infection with concomitant osteomyelitis. Infuse over 30 min; no dextrose diluents.', [R(Ep, '2.2, Table 1'), R(Ep, '2.1')])]),
      reg('dfi-child', 'diabetic-foot-infection', T('عفونت پوست شامل پای دیابتی — کودک ۳ ماه تا ۱۲ سال: ۱۵ mg/kg دو بار در روز (حداکثر ۱ g/روز)', 'Skin infection incl. diabetic foot — child 3 months–12 y: 15 mg/kg twice daily (max 1 g/day)'), EPT, 'weightBased', {'perKgPerDose': 15, 'intervalHours': 12}, [R(Ep, '2.2, Table 1')],
          limits={'maxPerDay': 1000, 'refs': [R(Ep, '2.2')]}, dur={'min': 7, 'max': 14}),
      reg('iai', 'intra-abdominal-infection', T('عفونت عارضه‌دار داخل شکم — ۱۳ سال به بالا ۱ g یک بار در روز، ۵ تا ۱۴ روز', 'Complicated intra-abdominal infection — ≥13 y 1 g once daily, 5–14 days'), A13, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Ep, '2.2, Table 1')], dur={'min': 5, 'max': 14}),
      reg('iai-child', 'intra-abdominal-infection', T('عفونت داخل شکم — کودک ۳ ماه تا ۱۲ سال: ۱۵ mg/kg دو بار در روز (حداکثر ۱ g/روز)', 'Intra-abdominal infection — child 3 months–12 y: 15 mg/kg twice daily (max 1 g/day)'), EPT, 'weightBased', {'perKgPerDose': 15, 'intervalHours': 12}, [R(Ep, '2.2, Table 1')],
          limits={'maxPerDay': 1000, 'refs': [R(Ep, '2.2')]}, dur={'min': 5, 'max': 14}),
      reg('proph', 'surgical-prophylaxis', T('پیشگیری از عفونت پس از جراحی انتخابی کولورکتال — ۱ g وریدی یک ساعت پیش از برش', 'Prophylaxis for elective colorectal surgery — 1 g IV 1 h before incision'), A18, 'fixed', {'perDose': 1000, 'dosesPerDay': 1}, [R(Ep, '2.3')], dur=ONE)],
     [CI('hyper', 'حساسیت به اجزای فرآورده یا سایر کارباپنم‌ها؛ آنافیلاکسی با بتالاکتام‌ها. تزریق عضلانی (با لیدوکائین): حساسیت به بی‌حس‌کننده‌های آمیدی.', 'Hypersensitivity to any component or other carbapenems; anaphylaxis with beta-lactams. IM (lidocaine diluent): hypersensitivity to amide local anaesthetics.', [R(Ep, '4')])],
     warn=[W('واکنش آلرژیک جدی؛ تشنج و عوارض CNS؛ اسهال C. difficile. با والپروات سطح آن کم و خطر تشنج بیشتر می‌شود.', 'Serious hypersensitivity; seizures and CNS effects; C. difficile diarrhoea. Lowers valproate levels with breakthrough seizure risk.', [R(Ep, '5')])],
     inter=[IA('valproate', 'والپروات و دیوالپروکس: کاهش سطح والپروات و تشنج.', 'Valproic acid and divalproex: reduced valproate levels and seizures.', [R(Ep, '5')])],
     renal=[{'egfrBelow': 31, 'severity': 'warn', 'text': T('ClCr ۳۰ و کمتر (و ESRD): ۵۰۰ mg روزانه. همودیالیز: اگر دوز ظرف ۶ ساعت پیش از دیالیز داده شد ۱۵۰ mg مکمل پس از دیالیز.', 'CrCl ≤30 (and ESRD): 500 mg daily. Haemodialysis: give 150 mg after dialysis if the daily dose was given within 6 h before.'), 'refs': [R(Ep, '2.4'), R(Ep, '2.5')]}],
     exs=[ex('dfi', 'vial-1g', {'perDose': 1000, 'dosesPerDay': 1}, ageYears=60, weightKg=85), ex('dfi-child', 'vial-1g', {'perDose': 300, 'dosesPerDay': 2}, ageYears=6, weightKg=20),
          ex('iai', 'vial-1g', {'perDose': 1000, 'dosesPerDay': 1}, ageYears=50, weightKg=70), ex('iai-child', 'vial-1g', {'perDose': 300, 'dosesPerDay': 2}, ageYears=6, weightKg=20), ex('proph', 'vial-1g', {'perDose': 1000}, ageYears=60, weightKg=80)])

Ab = fda('amphotericin-b', 'FDA Amphotericin B', 'Amphotericin B for injection 50 mg (conventional, X-Gen) — Prescribing Information', 'a0a54943-9ce4-4f3e-b681-a1a9144c16ce'); d = R(Ab, 'Dosage and Administration')
AMBN = note('فقط برای عفونت قارچی پیشرونده و تهدیدکننده حیات. دوز آزمایشی ۱ mg در ۲۰ تا ۳۰ دقیقه. شروع ۰٫۲۵ mg/kg/روز (عفونت شدید سریع ۰٫۳)، افزایش تدریجی تا ۰٫۵ تا ۰٫۷ mg/kg/روز؛ حداکثر ۱ mg/kg روزانه یا ۱٫۵ mg/kg یک روز در میان. انفوزیون ۲ تا ۶ ساعت با غلظت ۰٫۱ mg/mL.',
            'Only for progressive, life-threatening fungal infection. Test dose 1 mg over 20–30 min. Start 0.25 mg/kg/day (0.3 if severe and rapidly progressive), increase gradually to 0.5–0.7 mg/kg/day; max 1 mg/kg daily or 1.5 mg/kg on alternate days. Infuse over 2–6 h at 0.1 mg/mL.', [d])
drug('amphotericin-b', 'anti-infectives', 'آمفوتریسین B (معمولی، دزوکسی‌کولات)', 'Amphotericin B (conventional deoxycholate)', T('ضدقارچ پلی‌ان', 'Polyene antifungal'), [{'name': 'Fungizone', 'market': 'US'}], ['fungizone', 'آمفوتریسین', 'amphotericin'],
     [form('vial-50', 'powder-for-injection', 'iv', '50 mg vial (conventional — NOT liposomal)', 50, 'mg', [R(Ab, 'How Supplied')], per='vial')],
     [reg('mucor', 'mucormycosis', T('موکورمایکوزیس — شروع ۰٫۲۵ mg/kg/روز، افزایش تا ۰٫۵ تا ۰٫۷ mg/kg/روز', 'Mucormycosis — start 0.25 mg/kg/day, increase to 0.5–0.7 mg/kg/day'), {}, 'weightBased', {'perKgPerDay': 0.25, 'perKgPerDayMax': 0.7, 'dividedDoses': 1}, [d],
          limits={'maxPerKgPerDay': 1, 'refs': [d]}, notes=[AMBN, note('موکورمایکوزیس بینی-مغزی معمولاً همراه کتواسیدوز دیابتی است؛ کنترل دیابت برای موفقیت درمان ضروری است.', 'Rhinocerebral mucormycosis generally occurs with diabetic ketoacidosis; restoring diabetic control is imperative for treatment to succeed.', [d])]),
      reg('fungal', 'invasive-fungal', T('عفونت قارچی سیستمیک تهدیدکننده حیات — شروع ۰٫۲۵ mg/kg/روز، تا ۰٫۵ تا ۰٫۷ mg/kg/روز', 'Life-threatening systemic fungal infection — start 0.25 mg/kg/day, up to 0.5–0.7 mg/kg/day'), {}, 'weightBased', {'perKgPerDay': 0.25, 'perKgPerDayMax': 0.7, 'dividedDoses': 1}, [d],
          limits={'maxPerKgPerDay': 1, 'refs': [d]}, notes=[AMBN])],
     [CI('hyper', 'حساسیت به آمفوتریسین B، مگر در عفونت تهدیدکننده حیات که فقط به آن پاسخ می‌دهد.', 'Hypersensitivity to amphotericin B, unless the infection is life-threatening and amenable only to amphotericin B.', [R(Ab, 'Contraindications')])],
     warn=[W('اشتباه دوز کشنده است: هرگز بیش از ۱٫۵ mg/kg در روز؛ نام فرآورده (معمولی یا لیپوزومال) را چک کنید — جایگزین هم نیستند. سمیت کلیه، هیپوکالمی، واکنش انفوزیون.', 'Overdose can be fatal: never exceed 1.5 mg/kg/day; verify the product name (conventional vs liposomal — not interchangeable). Nephrotoxicity, hypokalaemia, infusion reactions.', [R(Ab, 'Warnings'), d])],
     exs=[ex('mucor', 'vial-50', {'perDose': 17.5, 'upperPerDose': 49}, ageYears=50, weightKg=70), ex('fungal', 'vial-50', {'perDose': 17.5, 'upperPerDose': 49}, ageYears=50, weightKg=70)])

Cr = fda('cresemba', 'FDA Cresemba', 'Cresemba (isavuconazonium sulfate) capsules and injection — Prescribing Information', sid('cresemba'))
ISN = note('بارگذاری: ۳۷۲ mg هر ۸ ساعت برای ۶ دوز (۴۸ ساعت)، سپس نگهدارنده یک بار در روز ۱۲ تا ۲۴ ساعت پس از آخرین دوز بارگذاری. ۳۷۲ mg ایزاووکونازونیوم = ۲۰۰ mg ایزاووکونازول.', 'Loading: 372 mg every 8 h for 6 doses (48 h), then once daily maintenance starting 12–24 h after the last loading dose. 372 mg isavuconazonium = 200 mg isavuconazole.', [R(Cr, '2.2, Table 1')])
drug('isavuconazonium', 'anti-infectives', 'ایزاووکونازونیوم (کرسمبا)', 'Isavuconazonium (isavuconazole)', T('ضدقارچ آزولی', 'Azole antifungal'), [{'name': 'Cresemba', 'market': 'US'}], ['cresemba', 'کرسمبا', 'isavuconazole', 'ایزاووکونازول'],
     [tab('cap-186', 186, '186 mg capsule (= 100 mg isavuconazole)', [R(Cr, '3')], per='capsule', form_='capsule'), tab('cap-74', 74.5, '74.5 mg capsule (= 40 mg isavuconazole)', [R(Cr, '3')], per='capsule', form_='capsule'),
      form('vial-372', 'powder-for-injection', 'iv', '372 mg vial (= 200 mg isavuconazole)', 372, 'mg', [R(Cr, '3')], per='vial')],
     [reg('mucor', 'mucormycosis', T('موکورمایکوزیس تهاجمی — بزرگسال: نگهدارنده ۳۷۲ mg یک بار در روز (پس از بارگذاری)', 'Invasive mucormycosis — adult: maintenance 372 mg once daily (after loading)'), A18, 'fixed', {'perDose': 372, 'dosesPerDay': 1}, [R(Cr, '2.2, Table 1')], notes=[ISN]),
      reg('asperg', 'invasive-fungal', T('آسپرژیلوز تهاجمی — بزرگسال: نگهدارنده ۳۷۲ mg یک بار در روز (پس از بارگذاری)', 'Invasive aspergillosis — adult: maintenance 372 mg once daily (after loading)'), A18, 'fixed', {'perDose': 372, 'dosesPerDay': 1}, [R(Cr, '2.2, Table 1')], notes=[ISN]),
      reg('child', 'mucormycosis', T('کودک (تزریقی از ۱ سال، کپسول از ۶ سال و ۱۶ kg) — دوز بر اساس جدول وزن برچسب', 'Children (IV from 1 y, capsules from 6 y and 16 kg) — dose per label weight table'), {'minAge': age(1, 'year'), 'maxAge': age(18, 'year')}, 'notCalculated',
          {'reason': T('دوز کودک طبق جدول ۲ برچسب بر اساس سن و وزن؛ هیچ دوز بارگذاری یا نگهدارنده از ۳۷۲ mg بیشتر نشود.', 'Pediatric dose per label Table 2 by age and weight; no loading or maintenance dose may exceed 372 mg.')}, [R(Cr, '2.3')])],
     [CI('ci', 'حساسیت به ایزاووکونازول؛ مهارکننده قوی CYP3A4 (کتوکونازول، ریتوناویر دوز بالا)؛ القاگر قوی CYP3A4 (ریفامپین، کاربامازپین، گل راعی، باربیتورات طولانی‌اثر)؛ سندرم QT کوتاه خانوادگی.',
         'Hypersensitivity to isavuconazole; strong CYP3A4 inhibitors (ketoconazole, high-dose ritonavir); strong CYP3A4 inducers (rifampin, carbamazepine, St John’s wort, long-acting barbiturates); familial short QT syndrome.', [R(Cr, '4')])],
     warn=[W('آسیب کبدی جدی (آزمایش کبد در شروع و حین درمان)؛ واکنش انفوزیون؛ آنافیلاکسی.', 'Serious hepatic reactions (check liver tests at start and during therapy); infusion reactions; anaphylaxis.', [R(Cr, '5')])],
     exs=[ex('mucor', 'cap-186', {'perDose': 372, 'tabletsPerDoseRounded': 2}, ageYears=55, weightKg=75), ex('asperg', 'vial-372', {'perDose': 372}, ageYears=55, weightKg=75)])

# --- neuromuscular / movement ---
Rz = fda('riluzole', 'FDA Riluzole', 'Riluzole tablets 50 mg — Prescribing Information', sid('riluzole'))
drug('riluzole', 'nervous-system', 'ریلوزول', 'Riluzole', T('مهارکننده گلوتامات', 'Glutamate inhibitor'), [{'name': 'Rilutek', 'market': 'US'}], ['rilutek', 'ریلوزول'],
     [tab('tab-50', 50, '50 mg tablet', [R(Rz, '3')])],
     [reg('als', 'als', T('ALS — ۵۰ mg دو بار در روز، ۱ ساعت قبل یا ۲ ساعت بعد از غذا', 'ALS — 50 mg twice daily, 1 h before or 2 h after a meal'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 2}, [R(Rz, '2')],
          notes=[note('آنزیم‌های کبد قبل و حین درمان.', 'Check aminotransferases before and during treatment.', [R(Rz, '2')])])],
     [CI('hyper', 'سابقه حساسیت شدید به ریلوزول (آنافیلاکسی رخ داده).', 'History of severe hypersensitivity to riluzole (anaphylaxis has occurred).', [R(Rz, '4')])],
     warn=[W('آسیب کبدی (ALT بالای ۵ برابر: توصیه نمی‌شود)؛ نوتروپنی (گزارش تب)؛ بیماری بینابینی ریه.', 'Hepatic injury (not recommended if ALT >5× ULN); neutropenia (report fever); interstitial lung disease.', [R(Rz, '5')])],
     exs=[ex('als', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=60, weightKg=70)])

Rv = fda('radicava', 'FDA Radicava', 'Radicava / Radicava ORS (edaravone) — Prescribing Information', sid('radicava'))
drug('edaravone', 'nervous-system', 'اداراوون', 'Edaravone', T('آنتی‌اکسیدان (پاک‌کننده رادیکال آزاد)', 'Free-radical scavenger'), [{'name': 'Radicava', 'market': 'US'}], ['radicava', 'اداراوون'],
     [form('bag-30', 'injection', 'iv', '30 mg/100 mL bag (dose = 2 bags)', 30, 'mg', [R(Rv, '3')], vol=100), liquid('ors', 105, 5, 'Radicava ORS 105 mg/5 mL oral suspension', [R(Rv, '3')])],
     [reg('als', 'als', T('ALS — دوره‌ای: ۶۰ mg وریدی یا ۱۰۵ mg خوراکی روزانه ۱۴ روز، ۱۴ روز استراحت؛ سپس ۱۰ از ۱۴ روز', 'ALS — cycles: 60 mg IV or 105 mg oral daily for 14 days, 14 days off; then 10 of 14 days'), A18, 'notCalculated',
          {'reason': T('دوره اول: روزانه ۱۴ روز، سپس ۱۴ روز بدون دارو. دوره‌های بعد: ۱۰ روز از ۱۴ روز، سپس ۱۴ روز بدون دارو. وریدی ۶۰ mg (دو کیسه ۳۰ mg) در ۶۰ دقیقه؛ خوراکی ۱۰۵ mg (۵ mL) صبح ناشتا و تا ۱ ساعت بعد غذا نخورد.', 'First cycle: daily for 14 days, then 14 days off. Later cycles: 10 of 14 days, then 14 days off. IV 60 mg (two 30 mg bags) over 60 min; oral 105 mg (5 mL) in the morning fasting, no food for 1 h after.')},
          [R(Rv, '2.1'), R(Rv, '2.2'), R(Rv, '2.3')])],
     [CI('hyper', 'سابقه حساسیت به اداراوون یا اجزای فرآورده.', 'History of hypersensitivity to edaravone or its inactive ingredients.', [R(Rv, '4')])],
     warn=[W('واکنش حساسیتی؛ حاوی سدیم بی‌سولفیت (واکنش آلرژیک و آسم در افراد حساس به سولفیت).', 'Hypersensitivity; contains sodium bisulfite (allergic reactions and asthma in sulfite-sensitive people).', [R(Rv, '5')])])

VMAT_W = lambda src: W('هشدار جعبه‌ای: افسردگی و افکار خودکشی در بیماری هانتینگتون؛ در افسردگی درمان‌نشده یا افکار خودکشی ممنوع.', 'Boxed warning: depression and suicidality in Huntington’s disease; contraindicated with untreated depression or suicidality.', [R(src, 'Boxed Warning')])
Tb = fda('tetrabenazine', 'FDA Tetrabenazine', 'Tetrabenazine tablets 12.5/25 mg (Apotex) — Prescribing Information', sid('tetrabenazine'))
drug('tetrabenazine', 'nervous-system', 'تترابنازین', 'Tetrabenazine', T('مهارکننده VMAT2', 'VMAT2 inhibitor'), [{'name': 'Xenazine', 'market': 'US'}], ['xenazine', 'تترابنازین'],
     [tab('tab-12.5'.replace('.', '-'), 12.5, '12.5 mg tablet (unscored)', [R(Tb, '3')]), tab('tab-25', 25, '25 mg tablet (scored)', [R(Tb, '3')], scored=True)],
     [reg('hd', 'huntington-chorea', T('کره هانتینگتون — هفته ۱: ۱۲٫۵ mg صبح؛ هفته ۲: ۱۲٫۵ دو بار؛ سپس هر هفته ۱۲٫۵ mg بیشتر (تا ۵۰ mg)', 'Huntington chorea — week 1: 12.5 mg AM; week 2: 12.5 mg twice; then +12.5 mg weekly (up to 50 mg)'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 12.5, 'increment': 12.5, 'incrementEveryDays': 7, 'max': 50}}, [R(Tb, '2.2')],
          notes=[note('۳۷٫۵ تا ۵۰ mg در سه دوز؛ هر دوز حداکثر ۲۵ mg. بالای ۵۰ mg فقط پس از ژنوتایپ CYP2D6 (متابولیزر سریع/متوسط: حداکثر ۱۰۰ mg/روز، دوز ۳۷٫۵). با مهارکننده قوی CYP2D6 حداکثر ۵۰ mg.', '37.5–50 mg in three doses; max single dose 25 mg. Above 50 mg only after CYP2D6 genotyping (EM/IM: max 100 mg/day, single 37.5 mg). With strong CYP2D6 inhibitors max 50 mg.', [R(Tb, '2.2'), R(Tb, '2.3')])])],
     [CI('ci', 'افکار فعال خودکشی یا افسردگی درمان‌نشده؛ نارسایی کبد؛ MAOI (یا ظرف ۱۴ روز)؛ رزرپین (۲۰ روز فاصله)؛ دوتترابنازین یا والبنازین.', 'Active suicidality or untreated/inadequately treated depression; hepatic impairment; MAOIs (or within 14 days); reserpine (20 days apart); deutetrabenazine or valbenazine.', [R(Tb, '4')])],
     warn=[VMAT_W(Tb), W('سندرم نورولپتیک بدخیم؛ آکاتیزی و پارکینسونیسم؛ خواب‌آلودگی؛ طولانی شدن QT.', 'Neuroleptic malignant syndrome; akathisia and parkinsonism; sedation; QTc prolongation.', [R(Tb, '5')])],
     exs=[ex('hd', 'tab-12-5', {'perDose': 12.5, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70)])

Au = fda('austedo', 'FDA Austedo', 'Austedo / Austedo XR (deutetrabenazine) — Prescribing Information', sid('austedo'))
AUT = {'dividedDoses': 2, 'titration': {'start': 12, 'increment': 6, 'incrementEveryDays': 7, 'max': 48}}
AUN = note('با غذا؛ دوز ۱۲ mg و بیشتر در دو نوبت. XR یک بار در روز. با مهارکننده قوی CYP2D6 یا متابولیزر ضعیف حداکثر ۳۶ mg. تعویض از تترابنازین طبق جدول ۲ برچسب.', 'With food; 12 mg/day or more in two doses. XR once daily. Strong CYP2D6 inhibitors or poor metabolizers: max 36 mg. Switching from tetrabenazine per label Table 2.', [R(Au, '2.1'), R(Au, '2.2'), R(Au, '2.3')])
drug('deutetrabenazine', 'nervous-system', 'دوتترابنازین', 'Deutetrabenazine', T('مهارکننده VMAT2', 'VMAT2 inhibitor'), [{'name': 'Austedo', 'market': 'US'}], ['austedo', 'دوتترابنازین'],
     [tab(f'tab-{m}', m, f'{m} mg tablet (swallow whole)', [R(Au, '3')]) for m in (6, 9, 12)],
     [reg('hd', 'huntington-chorea', T('کره هانتینگتون — شروع ۶ mg دو بار در روز، هر هفته ۶ mg/روز بیشتر تا حداکثر ۴۸ mg', 'Huntington chorea — start 6 mg twice daily, +6 mg/day weekly up to 48 mg'), A18, 'titration', AUT, [R(Au, '2.1')], notes=[AUN]),
      reg('td', 'tardive-dyskinesia', T('دیسکینزی دیررس — شروع ۶ mg دو بار در روز، هر هفته ۶ mg/روز بیشتر تا حداکثر ۴۸ mg', 'Tardive dyskinesia — start 6 mg twice daily, +6 mg/day weekly up to 48 mg'), A18, 'titration', AUT, [R(Au, '2.1')], notes=[AUN])],
     [CI('ci', 'هانتینگتون با افکار خودکشی یا افسردگی درمان‌نشده؛ نارسایی کبد؛ رزرپین (۲۰ روز)؛ MAOI (۱۴ روز)؛ تترابنازین یا والبنازین.', 'Huntington’s with suicidality or untreated depression; hepatic impairment; reserpine (20 days); MAOIs (14 days); tetrabenazine or valbenazine.', [R(Au, '4')])],
     warn=[VMAT_W(Au), W('طولانی شدن QT؛ سندرم نورولپتیک بدخیم؛ آکاتیزی و پارکینسونیسم؛ خواب‌آلودگی.', 'QT prolongation; neuroleptic malignant syndrome; akathisia and parkinsonism; sedation.', [R(Au, '5')])],
     exs=[ex('hd', 'tab-6', {'perDose': 6, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70), ex('td', 'tab-6', {'perDose': 6, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=75)])

Ig = fda('ingrezza', 'FDA Ingrezza', 'Ingrezza / Ingrezza Sprinkle (valbenazine) capsules — Prescribing Information', sid('ingrezza'))
drug('valbenazine', 'nervous-system', 'والبنازین', 'Valbenazine', T('مهارکننده VMAT2', 'VMAT2 inhibitor'), [{'name': 'Ingrezza', 'market': 'US'}], ['ingrezza', 'والبنازین'],
     [tab(f'cap-{m}', m, f'{m} mg capsule', [R(Ig, '3')], per='capsule', form_='capsule') for m in (40, 60, 80)],
     [reg('td', 'tardive-dyskinesia', T('دیسکینزی دیررس — ۴۰ mg یک بار در روز، پس از یک هفته ۸۰ mg', 'Tardive dyskinesia — 40 mg once daily, 80 mg after one week'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 40, 'increment': 40, 'incrementEveryDays': 7, 'max': 80}}, [R(Ig, '2.1')],
          notes=[note('۴۰ یا ۶۰ mg هم بسته به پاسخ و تحمل ممکن است.', '40 or 60 mg may be considered depending on response and tolerability.', [R(Ig, '2.1')])]),
      reg('hd', 'huntington-chorea', T('کره هانتینگتون — ۴۰ mg یک بار در روز، هر ۲ هفته ۲۰ mg بیشتر تا ۸۰ mg', 'Huntington chorea — 40 mg once daily, +20 mg every 2 weeks to 80 mg'), A18, 'titration',
          {'dividedDoses': 1, 'titration': {'start': 40, 'increment': 20, 'incrementEveryDays': 14, 'max': 80}}, [R(Ig, '2.1')])],
     [CI('hyper', 'سابقه حساسیت به والبنازین (کهیر، آنژیوادم).', 'History of hypersensitivity to valbenazine (rash, urticaria, angioedema).', [R(Ig, '4')])],
     warn=[VMAT_W(Ig), W('خواب‌آلودگی؛ طولانی شدن QT؛ سندرم نورولپتیک بدخیم؛ پارکینسونیسم.', 'Somnolence; QT prolongation; neuroleptic malignant syndrome; parkinsonism.', [R(Ig, '5')])],
     exs=[ex('td', 'cap-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=55, weightKg=75), ex('hd', 'cap-40', {'perDose': 40, 'tabletsPerDoseRounded': 1}, ageYears=45, weightKg=70)])

Ef = fda('emflaza', 'FDA Emflaza', 'Emflaza (deflazacort) tablets and oral suspension — Prescribing Information', sid('emflaza'))
drug('deflazacort', 'systemic-hormones', 'دفلازاکورت', 'Deflazacort', T('کورتیکواستروئید', 'Corticosteroid'), [{'name': 'Emflaza', 'market': 'US'}], ['emflaza', 'دفلازاکورت'],
     [liquid('susp', 22.75, 1, '22.75 mg/mL oral suspension', [R(Ef, '3')])] + [tab(f'tab-{m}', m, f'{m} mg tablet', [R(Ef, '3')]) for m in (6, 18, 30, 36)],
     [reg('dmd', 'duchenne', T('دیستروفی دوشن (۲ سال به بالا) — حدود ۰٫۹ mg/kg یک بار در روز', 'Duchenne muscular dystrophy (≥2 y) — about 0.9 mg/kg once daily'), {'minAge': age(2, 'year')}, 'weightBased', {'perKgPerDay': 0.9, 'dividedDoses': 1}, [R(Ef, '2.2')], allowed=['susp'],
          notes=[note('قرص: به نزدیک‌ترین دوز ممکن (ترکیب ۴ قدرت) گرد به بالا؛ سوسپانسیون: به نزدیک‌ترین ۰٫۱ mL بالا. مصرف بیش از چند روز: قطع تدریجی. با مهارکننده متوسط/قوی CYP3A4 یک‌سوم دوز. واکسن زنده ۴ تا ۶ هفته قبل.', 'Tablets: round up to the nearest possible dose (any combination of the 4 strengths); suspension: round up to the nearest 0.1 mL. After more than a few days: taper. Moderate/strong CYP3A4 inhibitors: one-third of the dose. Live vaccines 4–6 weeks before starting.', [R(Ef, '2.2'), R(Ef, '2.3'), R(Ef, '2.5'), R(Ef, '2.1')])])],
     [CI('hyper', 'حساسیت به دفلازاکورت یا اجزای فرآورده.', 'Hypersensitivity to deflazacort or its inactive ingredients.', [R(Ef, '4')])],
     warn=[W('سرکوب محور HPA، کوشینگ، هیپرگلیسمی؛ عفونت؛ افزایش فشار و کاهش پتاسیم؛ سوراخ شدن گوارش. سوسپانسیون بنزیل الکل دارد (زیر ۲ سال نه).', 'HPA-axis suppression, Cushing’s, hyperglycaemia; infections; raised BP and low potassium; GI perforation. Suspension contains benzyl alcohol (not under 2 y).', [R(Ef, '5'), R(Ef, '8.4')])],
     exs=[ex('dmd', 'susp', {'perDose': 22.5, 'mlPerDose': 0.99}, ageYears=8, weightKg=25)])

Fd = fda('firdapse', 'FDA Firdapse', 'Firdapse (amifampridine) 10 mg tablets — Prescribing Information', sid('firdapse'))
drug('amifampridine', 'nervous-system', 'آمیفامپریدین', 'Amifampridine', T('مسدودکننده کانال پتاسیم', 'Potassium channel blocker'), [{'name': 'Firdapse', 'market': 'US'}], ['firdapse', 'آمیفامپریدین', '3,4-diaminopyridine'],
     [tab('tab-10', 10, '10 mg tablet (functionally scored)', [R(Fd, '3')], scored=True)],
     [reg('adult', 'lambert-eaton', T('LEMS — بزرگسال و کودک ≥۴۵ kg: شروع ۱۵ mg/روز در ۳ دوز، هر ۳ تا ۴ روز ۵ mg بیشتر (حداکثر ۱۰۰ mg/روز)', 'LEMS — adults and children ≥45 kg: start 15 mg/day in 3 doses, +5 mg every 3–4 days (max 100 mg/day)'), {'minAge': age(6, 'year'), 'minWeightKg': 45}, 'titration',
          {'dividedDoses': 3, 'titration': {'start': 15, 'increment': 5, 'incrementEveryDays': 3, 'max': 100}}, [R(Fd, '2.1, Table 1')], limits={'maxPerDose': 20, 'refs': [R(Fd, '2.1, Table 1')]},
          notes=[note('شروع ۱۵ تا ۳۰ mg/روز در ۳ تا ۵ دوز. هر دوز حداکثر ۲۰ mg. نارسایی کلیه یا کبد و متابولیزر ضعیف NAT2: کمترین دوز شروع (۱۵ mg).', 'Start 15–30 mg/day in 3–5 doses. Max single dose 20 mg. Renal or hepatic impairment and NAT2 poor metabolizers: lowest starting dose (15 mg).', [R(Fd, '2.1, Table 1'), R(Fd, '2.2'), R(Fd, '2.3'), R(Fd, '2.4')])]),
      reg('child', 'lambert-eaton', T('LEMS — کودک ۶ سال به بالا زیر ۴۵ kg: شروع ۵ تا ۱۵ mg/روز در ۳ تا ۵ دوز (حداکثر ۵۰ mg/روز)', 'LEMS — child ≥6 y under 45 kg: start 5–15 mg/day in 3–5 doses (max 50 mg/day)'), {'minAge': age(6, 'year'), 'maxWeightKg': 44.99}, 'notCalculated',
          {'reason': T('افزایش ۲٫۵ mg هر ۳ تا ۴ روز؛ هر دوز حداکثر ۱۰ mg؛ حداکثر ۵۰ mg/روز. برای دوزهای کمتر از ۵ mg سوسپانسیون ۱ mg/mL طبق راهنمای برچسب تهیه شود.', 'Increase by 2.5 mg every 3–4 days; max single dose 10 mg; max 50 mg/day. For doses below 5 mg steps prepare the 1 mg/mL suspension per the label.')}, [R(Fd, '2.1, Table 1'), R(Fd, '2.5')])],
     [CI('ci', 'سابقه تشنج؛ حساسیت به آمیفامپریدین یا سایر آمینوپیریدین‌ها.', 'History of seizures; hypersensitivity to amifampridine or another aminopyridine.', [R(Fd, '4')])],
     warn=[W('تشنج (کاهش دوز یا قطع)؛ آنافیلاکسی.', 'Seizures (reduce dose or stop); anaphylaxis.', [R(Fd, '5')])],
     exs=[ex('adult', 'tab-10', {'perDose': 5, 'tabletsPerDoseRounded': 0.5}, ageYears=60, weightKg=70)])

Kv = fda('keveyis', 'FDA Keveyis', 'Keveyis (dichlorphenamide) 50 mg tablets — Prescribing Information', sid('keveyis'))
drug('dichlorphenamide', 'nervous-system', 'دی‌کلرفنامید', 'Dichlorphenamide', T('مهارکننده کربنیک انیدراز', 'Carbonic anhydrase inhibitor'), [{'name': 'Keveyis', 'market': 'US'}], ['keveyis', 'دی کلرفنامید'],
     [tab('tab-50', 50, '50 mg tablet (scored)', [R(Kv, '3')], scored=True)],
     [reg('pp', 'periodic-paralysis', T('فلج دوره‌ای اولیه هیپو/هیپرکالمیک — شروع ۵۰ mg یک یا دو بار در روز (حداکثر ۲۰۰ mg/روز)', 'Primary hypo/hyperkalaemic periodic paralysis — start 50 mg once or twice daily (max 200 mg/day)'), A18, 'fixed', {'perDose': 50, 'dosesPerDay': 1}, [R(Kv, '2.1')],
          limits={'maxPerDay': 200, 'refs': [R(Kv, '2.1')]}, notes=[note('تنظیم هفتگی بر اساس پاسخ؛ حداقل ۵۰ و حداکثر ۲۰۰ mg/روز. پاسخ پس از ۲ ماه ارزیابی شود. پتاسیم و بی‌کربنات پایه و دوره‌ای.', 'Adjust weekly by response; min 50 and max 200 mg/day. Evaluate response after 2 months. Baseline and periodic potassium and bicarbonate.', [R(Kv, '2.1'), R(Kv, '2.2'), R(Kv, '2.3')])])],
     [CI('ci', 'حساسیت به دی‌کلرفنامید یا سولفونامیدها؛ آسپرین دوز بالا همزمان؛ بیماری شدید ریوی؛ نارسایی کبد.', 'Hypersensitivity to dichlorphenamide or other sulfonamides; concomitant high-dose aspirin; severe pulmonary disease; hepatic insufficiency.', [R(Kv, '4')])],
     warn=[W('واکنش‌های تهدیدکننده حیات سولفونامیدی (قطع با اولین بثورات)؛ هیپوکالمی؛ اسیدوز متابولیک؛ زمین خوردن.', 'Life-threatening sulfonamide reactions (stop at first rash); hypokalaemia; metabolic acidosis; falls.', [R(Kv, '5')])],
     exs=[ex('pp', 'tab-50', {'perDose': 50, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=70)])

Tc = fda('tecfidera', 'FDA Tecfidera', 'Tecfidera (dimethyl fumarate) delayed-release capsules — Prescribing Information', sid('tecfidera'))
drug('dimethyl-fumarate', 'antineoplastic-immunomodulating', 'دی‌متیل فومارات', 'Dimethyl fumarate', T('تعدیل‌کننده ایمنی (MS)', 'Immunomodulator (MS)'), [{'name': 'Tecfidera', 'market': 'US'}], ['tecfidera', 'تکفیدرا', 'دی متیل فومارات'],
     [tab('cap-120', 120, '120 mg delayed-release capsule', [R(Tc, '3')], per='capsule', form_='capsule'), tab('cap-240', 240, '240 mg delayed-release capsule', [R(Tc, '3')], per='capsule', form_='capsule')],
     [reg('ms', 'multiple-sclerosis', T('MS عودکننده — ۱۲۰ mg دو بار در روز ۷ روز، سپس ۲۴۰ mg دو بار در روز', 'Relapsing MS — 120 mg twice daily for 7 days, then 240 mg twice daily'), A18, 'titration',
          {'dividedDoses': 2, 'titration': {'start': 240, 'increment': 240, 'incrementEveryDays': 7, 'max': 480}}, [R(Tc, '2.1')],
          notes=[note('کپسول کامل بلعیده شود. برافروختگی: با غذا یا آسپرین غیرروکش‌دار تا ۳۲۵ mg نیم ساعت قبل. CBC با لنفوسیت و آزمایش کبد قبل از شروع.', 'Swallow whole. Flushing: take with food or non-enteric-coated aspirin up to 325 mg 30 min before. CBC with lymphocytes and liver tests before starting.', [R(Tc, '2.1'), R(Tc, '2.2')])])],
     [CI('hyper', 'حساسیت به دی‌متیل فومارات (آنافیلاکسی، آنژیوادم).', 'Hypersensitivity to dimethyl fumarate (anaphylaxis, angioedema).', [R(Tc, '4')])],
     warn=[W('PML؛ زونا و عفونت فرصت‌طلب؛ لنفوپنی (CBC هر ۶ تا ۱۲ ماه)؛ آسیب کبدی.', 'PML; herpes zoster and opportunistic infections; lymphopenia (CBC every 6–12 months); liver injury.', [R(Tc, '5')])],
     exs=[ex('ms', 'cap-120', {'perDose': 120, 'tabletsPerDoseRounded': 1}, ageYears=35, weightKg=65)])

Ag = fda('aubagio', 'FDA Aubagio', 'Aubagio (teriflunomide) tablets — Prescribing Information', sid('aubagio'))
drug('teriflunomide', 'antineoplastic-immunomodulating', 'تری‌فلونوماید', 'Teriflunomide', T('تعدیل‌کننده ایمنی (MS)', 'Immunomodulator (MS)'), [{'name': 'Aubagio', 'market': 'US'}], ['aubagio', 'اوباجیو', 'تری فلونوماید'],
     [tab('tab-7', 7, '7 mg tablet', [R(Ag, '3')]), tab('tab-14', 14, '14 mg tablet', [R(Ag, '3')])],
     [reg('ms', 'multiple-sclerosis', T('MS عودکننده — ۷ یا ۱۴ mg یک بار در روز', 'Relapsing MS — 7 or 14 mg once daily'), A18, 'fixed', {'perDose': 7, 'perDoseMax': 14, 'dosesPerDay': 1}, [R(Ag, '2')])],
     [CI('ci', 'نارسایی شدید کبد؛ بارداری یا زن در سن باروری بدون پیشگیری مؤثر؛ حساسیت؛ مصرف همزمان لفلونوماید.', 'Severe hepatic impairment; pregnancy, or females of reproductive potential not using effective contraception; hypersensitivity; current leflunomide.', [R(Ag, '4'), R(Ag, 'Boxed Warning')])],
     warn=[W('هشدار جعبه‌ای: سمیت کبدی (ALT ماهانه ۶ ماه اول) و سمیت جنینی (رد بارداری قبل از شروع؛ حذف سریع با کلستیرامین یا زغال فعال).', 'Boxed warning: hepatotoxicity (monthly ALT for 6 months) and embryofetal toxicity (exclude pregnancy before starting; accelerated elimination with cholestyramine or charcoal).', [R(Ag, 'Boxed Warning'), R(Ag, '5')])],
     exs=[ex('ms', 'tab-7', {'perDose': 7, 'tabletsPerDoseRounded': 1, 'upperPerDose': 14}, ageYears=35, weightKg=65)])

Gl = fda('gilenya', 'FDA Gilenya', 'Gilenya (fingolimod) capsules — Prescribing Information', sid('gilenya'))
drug('fingolimod', 'antineoplastic-immunomodulating', 'فینگولیمود', 'Fingolimod', T('تعدیل‌کننده گیرنده S1P (MS)', 'S1P receptor modulator (MS)'), [{'name': 'Gilenya', 'market': 'US'}], ['gilenya', 'ژیلنیا', 'فینگولیمود'],
     [tab('cap-025', 0.25, '0.25 mg capsule', [R(Gl, '3')], per='capsule', form_='capsule'), tab('cap-05', 0.5, '0.5 mg capsule', [R(Gl, '3')], per='capsule', form_='capsule')],
     [reg('ms', 'multiple-sclerosis', T('MS عودکننده (۱۰ سال به بالا) — وزن >۴۰ kg: ۰٫۵ mg؛ ≤۴۰ kg: ۰٫۲۵ mg یک بار در روز', 'Relapsing MS (≥10 y) — >40 kg: 0.5 mg; ≤40 kg: 0.25 mg once daily'), {'minAge': age(10, 'year')}, 'weightBand',
          {'weightBands': [{'minWeightKg': 0, 'maxWeightKg': 40, 'perDose': 0.25, 'dosesPerDay': 1}, {'minWeightKg': 40, 'maxWeightKg': None, 'perDose': 0.5, 'dosesPerDay': 1}]}, [R(Gl, '2.3')],
          notes=[note('دوز اول با پایش ۶ ساعته (نبض و فشار هر ساعت، ECG قبل و بعد) برای برادی‌کاردی؛ شروع مجدد پس از قطع بیش از ۱۴ روز هم همین‌طور. CBC، آنزیم کبد و معاینه ته چشم.', 'First dose with 6-hour monitoring (hourly pulse and BP, ECG before and after) for bradycardia; same when restarting after >14 days off. CBC, liver enzymes and fundus exam.', [R(Gl, '2.4'), R(Gl, '2.1'), R(Gl, '2.5')])])],
     [CI('ci', 'در ۶ ماه گذشته MI، آنژین ناپایدار، سکته، TIA یا نارسایی قلبی جبران‌نشده؛ بلوک AV موبیتز II یا درجه ۳ یا سینوس بیمار بدون پیس‌میکر؛ QTc پایه ≥۵۰۰؛ ضدآریتمی کلاس Ia یا III؛ حساسیت.',
         'Within 6 months: MI, unstable angina, stroke, TIA or decompensated heart failure; Mobitz II/3rd-degree AV block or sick sinus without pacemaker; baseline QTc ≥500 ms; class Ia or III antiarrhythmics; hypersensitivity.', [R(Gl, '4')])],
     warn=[W('برادی‌کاردی دوز اول؛ عفونت و PML؛ ادم ماکولا؛ آسیب کبدی.', 'First-dose bradycardia; infections and PML; macular oedema; liver injury.', [R(Gl, '5'), R(Gl, '2.4')])],
     exs=[ex('ms', 'cap-05', {'perDose': 0.5, 'tabletsPerDoseRounded': 1}, ageYears=30, weightKg=65), ex('ms', 'cap-025', {'perDose': 0.25, 'tabletsPerDoseRounded': 1}, ageYears=12, weightKg=35)])

c = json.load(open(os.path.join(ROOT, 'collections.json')))
for col in c:
    if col['id'] == 'sexual-health':
        col['drugs'] += [x for x in ['sinecatechins', 'pyrethrins-pbo'] if x not in col['drugs']]
json.dump(c, open(os.path.join(ROOT, 'collections.json'), 'w'), ensure_ascii=False, indent=2); open(os.path.join(ROOT, 'collections.json'), 'a').write('\n')
print('s10 ok')
