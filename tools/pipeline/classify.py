"""Special-population tags from label wording. A level is set only when the wording matches; the sentence is kept as the quote."""
import re
def sents(t): return [s.strip() for s in re.split(r'(?<=[.;])\s+(?=[A-Z(\[])', t) if len(s.strip()) > 15]
def find(t, pats):
    ss = [s for s in sents(t) if not re.fullmatch(r'[^a-z]*\]\.?|.{0,30}\]\s*\.', s)]
    for p in pats:
        for s in ss:
            m = re.search(p, s, re.I)
            if m and not re.search(r'not known whether|unknown whether|cannot be ruled out|did not show an increase', s, re.I):
                return s if m.start() < 200 else '… ' + s[max(0, m.start() - 120):]
    return None
def cut(s, n=320):
    s = re.sub(r'\s*</?section\b.*$', '', s).strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'
def sec_label(title, fallback):
    if title and not re.match(r'\s*\d', title): return title
    m = re.match(r'\s*(\d+(?:\.\d+)?)\s', title or '')
    return m.group(1) if m else (title or fallback)

def pregnancy(sec):
    t = sec.get('pregnancy', ''); c = sec.get('contra', ''); b = sec.get('boxed', '')
    s = find(c, [r'contraindicated[^.]*pregnan', r'pregnan[^.]*contraindicated', r'pregnan'])
    if s: return 'contraindicated', s, 'contra'
    s = find(t, [r'category X', r'contraindicated in (?:women who are or may become )?pregnan'])
    if s: return 'contraindicated', s, 'pregnancy'
    s = find(b, [r'fetal toxicity', r'fetal harm', r'neonatal opioid withdrawal', r'embryo'])
    if s: return 'avoid', s, 'boxed'
    s = find(t, [r'can cause fetal harm', r'may cause (?:fetal )?harm', r'category D\b', r'positive evidence of human fetal risk', r'should be avoided', r'avoid use', r'discontinue[^.]*(?:when|if) pregnancy', r'(?:30|20) weeks', r'especially important not to use'])
    if s: return 'avoid', s, 'pregnancy'
    s = find(t, [r'not expected to result in fetal exposure', r'minimally absorbed systemically'])
    if s: return 'ok', s, 'pregnancy'
    if t:
        s = find(t, [r'category [ABC]\b', r'risk summary', r'should be used during pregnancy only', r'data .* (?:not|have not) (?:identified|shown)', r'.'])
        return 'caution', s, 'pregnancy'
    return None

def lactation(sec):
    t = sec.get('lactation') or sec.get('nursing', ''); c = sec.get('contra', '')
    s = find(c, [r'contraindicated[^.]*(?:breast-?feed|nursing|lactating)', r'breast-?feed', r'nursing mothers', r'lactating (?:women|mothers)', r'\blactation\b'])
    if s: return 'contraindicated', s, 'contra'
    if not t: return None
    s = find(t, [r'(?:is )?contraindicated', r'should not be used during lactation', r'should not be given to nursing', r'(?:do not|should not|not recommended to) breast-?feed', r'breastfeeding is not recommended', r'breast-?feeding:? not recommended', r'advise (?:a )?(?:women|patients|lactating)[^.]*not to breastfeed', r'breastfeeding is not recommended'])
    if s: return 'avoid', s, 'lactation'
    s = find(t, [r'decision should be made whether to discontinue nursing or to discontinue the drug'])
    if s: return 'avoid', s, 'lactation'
    s = find(t, [r'not expected to result in exposure', r'minimally absorbed'])
    if s: return 'ok', s, 'lactation'
    return 'caution', find(t, [r'caution should be exercised', r'risk summary', r'.']), 'lactation'

def pediatric(sec):
    t = sec.get('pediatric', ''); c = sec.get('contra', ''); b = sec.get('boxed', '')
    s = find(c, [r'(?:children|pediatric patients)[^.]*(?:younger than|less than|under) \d+', r'(?:younger than|less than|under) \d+ (?:years|months)'])
    if s: return 'contraindicated', s, 'contra'
    s = find(b, [r'pediatric', r'children'])
    if s: return 'avoid', s, 'boxed'
    if not t: return None
    est = find(t, [r'(?:safety and )?(?:effectiveness|efficacy)[^.]*(?:have|has) been established', r'established in pediatric', r'may be administered[^.]*(?:children|pediatric)', r'is indicated[^.]*(?:children|pediatric)'])
    if est: return 'caution', est, 'pediatric'
    s = find(t, [r'have not been established in (?:pediatric|children)', r'(?:safety|efficacy|effectiveness)[^.]*(?:pediatric|children|patients (?:less|younger) than)[^.]*(?:has|have) not been established', r'(?:safety|efficacy)[^.]*(?:children|paediatric|adolescents)[^.]*(?:has|have) not (?:yet )?been established', r'safety and effectiveness[^.]*(?:pediatric|children|infants)[^.]*have not been established', r'not been conducted in any pediatric', r'(?:safety|efficacy)[^.]*(?:pediatric|children)[^.]*(?:is|are) unknown', r'not (?:indicated|recommended) (?:for use )?in (?:children|pediatric)'])
    if s:
        m = re.search(r'(?:less than|younger than|below|under|aged?)(?: the age of)?\s*(\d+)\s*(year|month|week|day)?', s, re.I)
        if m and not (int(m.group(1)) >= 17 and (m.group(2) or 'year').lower().startswith('year')): return 'caution', s, 'pediatric'
        return 'not-established', s, 'pediatric'
    return 'caution', find(t, [r'safety and effectiveness[^.]*(?:have been|has been) established', r'.']), 'pediatric'

def geriatric(sec):
    t = sec.get('geriatric', ''); b = sec.get('boxed', '')
    s = find(b, [r'dementia-related psychosis', r'probable dementia'])
    if s: return 'avoid', s, 'boxed'
    s = find(b, [r'elderly patients[^.]*greater risk'])
    if s: return 'caution', s, 'boxed'
    if not t: return None
    s = find(t, [r'should (?:be avoided|not be used) in (?:the )?(?:elderly|geriatric|older)', r'avoid (?:use )?in (?:the )?(?:elderly|geriatric|older)', r'beers criteria'])
    if s: return 'avoid', s, 'geriatric'
    s = find(t, [r'cautious', r'caution', r'greater sensitivity', r'increased risk', r'lower (?:starting )?dose', r'dose selection', r'reduc', r'monitor'])
    if s: return 'caution', s, 'geriatric'
    s = find(t, [r'no dos(?:age|e) adjustment', r'no overall differences', r'same dos(?:age|ing)'])
    if s: return 'ok', s, 'geriatric'
    return 'caution', find(t, [r'.']), 'geriatric'

def reproductive(sec):
    t = sec.get('reproductive', '')
    if not t: return None
    return 'caution', find(t, [r'contracepti', r'pregnancy test', r'infertil', r'fertility', r'.']), 'reproductive'

FUN = {'pregnancy': pregnancy, 'lactation': lactation, 'pediatric': pediatric, 'geriatric': geriatric, 'reproductive': reproductive}
TXT = {
 'pregnancy': {'ok': ('برچسب: جذب سیستمیک ناچیز؛ مواجهه جنین انتظار نمی‌رود.', 'Label: minimal systemic absorption; fetal exposure not expected.'),
   'caution': ('برچسب خطر مشخصی برای بارداری ذکر نکرده یا داده کافی ندارد؛ فقط در صورت لزوم و با نظر پزشک.', 'Label states no clear risk or has limited data; use only if needed, under medical advice.'),
   'avoid': ('برچسب: می‌تواند به جنین آسیب بزند. در بارداری خطرناک است.', 'Label: can cause fetal harm. Dangerous in pregnancy.'),
   'contraindicated': ('برچسب: در بارداری منع مصرف دارد.', 'Label: contraindicated in pregnancy.')},
 'lactation': {'ok': ('برچسب: مواجهه شیرخوار انتظار نمی‌رود.', 'Label: infant exposure not expected.'),
   'caution': ('برچسب: در شیردهی با احتیاط؛ متن برچسب را ببینید.', 'Label: use with caution while breastfeeding; see the label text.'),
   'avoid': ('برچسب: شیردهی توصیه نمی‌شود یا باید بین دارو و شیردهی یکی انتخاب شود.', 'Label: breastfeeding not recommended, or choose between the drug and breastfeeding.'),
   'contraindicated': ('برچسب: در شیردهی منع مصرف دارد.', 'Label: contraindicated while breastfeeding.')},
 'pediatric': {'caution': ('برچسب برای کودکان شرط، محدودیت سنی یا نکته دارد؛ جمله برچسب در زیر آمده است.', 'The label has conditions, age limits or notes for children; the label sentence is quoted below.'),
   'not-established': ('برچسب: ایمنی و اثربخشی در کودکان ثابت نشده است.', 'Label: safety and effectiveness in children have not been established.'),
   'avoid': ('هشدار جعبه‌ای برچسب درباره کودکان.', 'Boxed warning in the label about children.'),
   'contraindicated': ('برچسب: در کودکان زیر سن مشخص منع مصرف دارد.', 'Label: contraindicated in children below a stated age.')},
 'geriatric': {'ok': ('برچسب: در سالمندان تفاوت یا تنظیم دوز خاصی ذکر نشده.', 'Label: no specific difference or dose adjustment stated for older adults.'),
   'caution': ('برچسب: در سالمندان با احتیاط و معمولاً از دوز پایین شروع شود.', 'Label: use with caution in older adults, usually starting at the low end of the dose range.'),
   'avoid': ('برچسب: در سالمندان هشدار جدی یا پرهیز.', 'Label: serious warning or avoid in older adults.')},
 'reproductive': {'caution': ('برچسب نکته‌ای درباره بارداری، پیشگیری یا باروری زنان و مردان دارد.', 'Label has advice on pregnancy testing, contraception or fertility for females and males.')}}

def smpc_sections(t):
    """Sections 4.2/4.3/4.6 from UK SmPC plain text."""
    def section(num, nxt):
        starts = [m.start() for m in re.finditer(re.escape(num) + r'\s+[A-Z]', t)]
        for s in reversed(starts):
            e = re.search(re.escape(nxt) + r'\s+[A-Z]', t[s + 5:])
            if e and e.start() > 40: return t[s:s + 5 + e.start()]
        return ''
    s42 = section('4.2', '4.3'); s43 = section('4.3', '4.4'); s46 = section('4.6', '4.7')
    out = {'contra': s43[3:].strip(), 'contra_title': '4.3'}
    pm = re.search(r'(?:Paediatric population|Children|Paediatric)[^:]{0,30}:?\s*(.{20,900}?)(?=(?:Older people|Elderly|Method of administration|Renal|Hepatic|$))', s42)
    if pm: out['pediatric'] = pm.group(0); out['pediatric_title'] = '4.2'
    em = re.search(r'(?:Elderly|Older people|Older patients)[^:]{0,20}:?\s*(.{20,600}?)(?=(?:Paediatric|Children|Method of administration|Renal|Hepatic|$))', s42)
    if em: out['geriatric'] = em.group(0); out['geriatric_title'] = '4.2'
    if s46:
        preg = re.search(r'Pregnancy\s*(.{10,1500}?)(?=Breast-?feeding|Lactation|Fertility|$)', s46[4:])
        lact = re.search(r'(?:Breast-?feeding|Lactation)\s*(.{10,1200}?)(?=Fertility|Pregnancy|$)', s46[4:])
        if preg: out['pregnancy'] = preg.group(1); out['pregnancy_title'] = '4.6'
        if lact: out['lactation'] = lact.group(1); out['lactation_title'] = '4.6'
    return out
