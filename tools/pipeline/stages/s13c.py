"""Stage 13c — Iranian routine childhood vaccines from Darooyab (no US/UK label): pentavalent (DTwP-HepB-Hib), oral polio (OPV), DTP.
Iran-only → low-confidence source, notCalculated (Darooyab gives no numeric volume per dose)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import *

IR = ('IR',)
NCR = lambda fa, en: T('رفرنس مطمئن نیست: برچسب آمریکا یا انگلیس برای این فرآورده ایرانی در دسترس نیست و اطلاعات از دارویاب است. ' + fa, 'Reference not reliable: no US/UK label for this Iranian product; information is from Darooyab. ' + en)
SCHED = note('برنامه، سن و حجم هر نوبت طبق برنامه کشوری ایمن‌سازی وزارت بهداشت ایران.', 'Schedule, ages and volume per dose follow the Iranian national immunisation programme (Ministry of Health).', [])

Pv = dy('ir-darooyab-pentavalent', 'Darooyab Pentavalent', 'واکسن دیفتری، کزاز، سیاه‌سرفه، هموفیلوس آنفلوانزا و هپاتیت بی — موارد مصرف، منع مصرف و اشکال دارویی', 'G-3448/Diphtheria,-Tetanus,-Pertussis,-Haemophilus-Influenzae,-and-Hepatitis-B-Vaccines')
drug('pentavalent-vaccine', 'anti-infectives', 'واکسن پنج‌گانه (پنتاوالان)', 'Pentavalent vaccine (DTwP-HepB-Hib)', T('واکسن ترکیبی', 'Combination vaccine'), [{'name': 'Pentavalent Biological E', 'market': 'IR'}], ['pentavalent', 'پنتاوالان', 'پنج گانه', 'DTP-HepB-Hib'],
     [form('vial-1', 'injection', 'im', '1-dose vial (also 10-dose vial)', 1, 'application', [R(Pv, 'اشکال دارویی')], per='vial', markets=IR)],
     [reg('child', 'immunization', T('ایمن‌سازی کودکان علیه دیفتری، کزاز، سیاه‌سرفه، هپاتیت B و هموفیلوس نوع b — عضلانی قدامی-خارجی ران؛ در ایران از ۲ ماهگی', 'Childhood immunisation against diphtheria, tetanus, pertussis, hepatitis B and Hib — IM anterolateral thigh; in Iran from 2 months'),
          {'minAge': age(6, 'week'), 'maxAge': age(7, 'year')}, 'notCalculated',
          {'reason': NCR('دارویاب حجم عددی هر نوبت را ذکر نکرده است. حداقل سن ۶ هفته؛ بعد از ۵ سالگی توصیه نمی‌شود (جز پرخطر) و از ۷ سالگی ممنوع (جزء سیاه‌سرفه). یادآور در سال دوم، دست‌کم ۶ ماه پس از دوره اولیه. بعد از ۳ سالگی در دلتوئید. هرگز وریدی؛ ۳۰ دقیقه پایش با اپی‌نفرین در دسترس.',
                         'Darooyab gives no numeric volume per dose. Minimum age 6 weeks; not recommended after 5 y (except high risk) and contraindicated from 7 y (pertussis component). Booster in year 2, at least 6 months after the primary series. After 3 y into the deltoid. Never IV; observe 30 min with epinephrine at hand.')},
          [R(Pv, 'موارد مصرف'), R(Pv, 'توصیه های دارویی')], notes=[note(SCHED['text']['fa'], SCHED['text']['en'], [R(Pv, 'توصیه های دارویی')])])],
     [CI('ci', 'حساسیت شدید به دوز قبلی. پس از عارضه شدید مرتبط با جزء سیاه‌سرفه: نوبت بعد دوگانه خردسالان + هپاتیت B + Hib جداگانه. تشنج شخصی اخیر: تا رد بیماری پیشرونده عصبی به تعویق. بیماری حاد متوسط تا شدید: تا بهبود به تعویق.',
         'Severe hypersensitivity to a previous dose. After a severe pertussis-related reaction: next dose as separate DT + hepatitis B + Hib. Recent personal seizure: defer until progressive neurological disease is excluded. Moderate–severe acute illness: defer until recovery.', [R(Pv, 'منع مصرف')])],
     warn=[W('سرماخوردگی، تب خفیف و اسهال دلیل تعویق نیست؛ سابقه خانوادگی تشنج و بیماری عصبی کنترل‌شده (صرع، CP) منع نیست.', 'Colds, mild fever and diarrhoea are not reasons to defer; family history of seizures and controlled neurological disease (epilepsy, CP) are not contraindications.', [R(Pv, 'منع مصرف')])])

Op = dy('ir-darooyab-opv', 'Darooyab OPV', 'واکسن خوراکی فلج اطفال — موارد مصرف، منع مصرف، هشدارها و اشکال دارویی', 'G-4595/Poliovirus-Oral-Vaccine-OPV')
drug('opv-vaccine', 'anti-infectives', 'واکسن خوراکی فلج اطفال (OPV)', 'Oral poliovirus vaccine (OPV)', T('واکسن زنده ضعیف‌شده', 'Live attenuated vaccine'), [{'name': 'OPVERO', 'market': 'IR'}], ['opv', 'فلج اطفال خوراکی', 'قطره فلج', 'polio oral'],
     [form('drop-mv', 'drops', 'oral', 'Oral drops, 10- or 20-dose vial', 1, 'drop', [R(Op, 'اشکال دارویی')], per='drop', markets=IR)],
     [reg('child', 'immunization', T('ایمن‌سازی فعال علیه ویروس فلج اطفال — قطره خوراکی طبق برنامه کشوری', 'Active immunisation against poliovirus — oral drops per the national schedule'), {'maxAge': age(18, 'year')}, 'notCalculated',
          {'reason': NCR('دارویاب تعداد قطره یا حجم هر نوبت را ذکر نکرده است. ایمنی پس از ۳ نوبت در بیش از ۹۵٪.', 'Darooyab gives no number of drops or volume per dose. Immunity after 3 doses in over 95%.')},
          [R(Op, 'موارد مصرف'), R(Op, 'مکانیسم اثر')], notes=[note(SCHED['text']['fa'], SCHED['text']['en'], [R(Op, 'توصیه های دارویی')])])],
     [CI('ci', 'حساسیت به اجزای واکسن؛ بیماری حاد، استفراغ یا اسهال پایدار؛ ضعف پیشرفته؛ نقص ایمنی، سابقه خانوادگی نقص ایمنی یا زندگی با فرد دچار نقص ایمنی — در این موارد واکسن تزریقی (IPV).',
         'Hypersensitivity to vaccine components; acute illness, persistent vomiting or diarrhoea; advanced debility; immunodeficiency, family history of immunodeficiency or living with an immunodeficient person — use injectable IPV instead.', [R(Op, 'منع مصرف'), R(Op, 'هشدار ها')])],
     warn=[W('ویروس تا ۶ تا ۸ هفته از مدفوع و بزاق دفع می‌شود — بهداشت دست. با داروهای سرکوب‌کننده ایمنی نه. با واکسن وبا یک ماه فاصله. در فریزر نگهداری.', 'Virus is shed in stool and saliva for 6–8 weeks — hand hygiene. Not with immunosuppressants. One month apart from cholera vaccine. Store frozen.', [R(Op, 'توصیه های دارویی'), R(Op, 'تداخلات دارویی')])])

Dt = dy('ir-darooyab-dtp', 'Darooyab DTP', 'توکسوئید دیفتری و کزاز و واکسن سیاه‌سرفه (DTP) — موارد مصرف، منع مصرف و هشدارها', 'G-4572/Diphtheria--Tetanus-Toxoids--Pertussis-Vaccine-DTP')
drug('dtp-vaccine', 'anti-infectives', 'واکسن سه‌گانه (DTP)', 'DTP vaccine (diphtheria, tetanus, whole-cell pertussis)', T('واکسن ترکیبی', 'Combination vaccine'), [{'name': 'DTP', 'market': 'IR'}], ['dtp', 'سه گانه', 'ثلاث', 'DTwP'],
     [form('vial', 'injection', 'im', 'Injectable suspension', 1, 'application', [R(Dt, 'موارد مصرف')], per='vial', markets=IR)],
     [reg('child', 'immunization', T('ایمن‌سازی فعال علیه کزاز، دیفتری و سیاه‌سرفه — نوزاد و کودک ۶ هفته تا ۷ سال', 'Active immunisation against tetanus, diphtheria and pertussis — infants and children 6 weeks to 7 years'), {'minAge': age(6, 'week'), 'maxAge': age(7, 'year')}, 'notCalculated',
          {'reason': NCR('دارویاب حجم عددی هر نوبت را ذکر نکرده است. ایمنی پس از نوبت سوم در بیش از ۹۰٪. بالای ۷ سال به‌جای آن Td.', 'Darooyab gives no numeric volume per dose. Immunity after the third dose in over 90%. Above 7 y use Td instead.')},
          [R(Dt, 'موارد مصرف'), R(Dt, 'هشدار ها')], notes=[note(SCHED['text']['fa'], SCHED['text']['en'], [R(Dt, 'توصیه های دارویی')])])],
     [CI('ci', 'سن بالای ۷ سال یا زیر ۶ هفته؛ سابقه بهبود از سیاه‌سرفه اثبات‌شده؛ حساسیت؛ تب یا عفونت حاد؛ عارضه عصبی پس از نوبت قبل؛ اختلال انعقادی یا کاهش پلاکت؛ هنگام شیوع پولیومیلیت. در منع جزء سیاه‌سرفه: DT.',
         'Age over 7 y or under 6 weeks; history of proven pertussis; hypersensitivity; fever or acute infection; neurological reaction after a previous dose; coagulation disorder or thrombocytopenia; during a poliomyelitis outbreak. If pertussis is contraindicated: DT.', [R(Dt, 'منع مصرف')])],
     warn=[W('اگر در نوبت قبل طی ۴۸ ساعت تب ۴۰٫۵، شوک، گریه مداوم یا تشنج رخ داده، نوبت بعد با احتیاط. برای درمان یا پیشگیری فوری کزاز/دیفتری پادزهر لازم است، نه واکسن.', 'If a previous dose was followed within 48 h by fever 40.5 °C, shock, persistent crying or seizure, give later doses with caution. Treatment or immediate prophylaxis of tetanus/diphtheria needs antitoxin, not vaccine.', [R(Dt, 'هشدار ها')])])
print('s13c ok')
