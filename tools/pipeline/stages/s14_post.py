"""Stage 14 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def pop(key, level, fa, en, quote, section, source=None):
    def fn(d):
        src = source or d['populations'][key]['refs'][0]['source']
        d['populations'][key] = {**d['populations'].get(key, {}), 'level': level, 'text': T(fa, en), 'quote': quote, 'refs': [{'source': src, 'section': section}]}
    return fn

# Pregnancy: the classifier read the placental-transfer sentence as a risk statement.
edit('ivig', pop('pregnancy', 'caution', 'برچسب: مطالعه حیوانی نشده و خطر جنینی نامعلوم است؛ فقط در صورت نیاز واضح.', 'Label: no animal studies and fetal risk unknown; give only if clearly needed.',
                 'It is not known whether GAMMAGARD LIQUID can cause fetal harm when administered to a pregnant woman or can affect reproduction capacity. Immune globulins cross the placenta from maternal circulation increasingly after 30 weeks of gestation. GAMMAGARD LIQUID should be given to a pregnant woman only if clearly indicated.', '8.1'))
# Paediatric: the label's lead-poisoning dosing applies to children; the matched sentence is about encephalopathy risk, not avoidance.
edit('edetate-calcium-disodium', pop('pediatric', 'caution', 'برچسب: انسفالوپاتی سربی در کودکان شایع‌تر و مرگ‌بار است؛ در ادم مغزی تزریق عضلانی ترجیح دارد و انفوزیون سریع وریدی ممنوع.', 'Label: lead encephalopathy is more common and lethal in children; with cerebral oedema the IM route is preferred and rapid IV infusion avoided.',
                                       'Lead encephalopathy is relatively rare in adults, but occurs more often in pediatric patients in whom it may be incipient and thus overlooked. The mortality rate in pediatric patients has been high. Patients with lead encephalopathy and cerebral edema may experience a lethal increase in intracranial pressure following intravenous infusion; the intramuscular route is preferred for these patients.', 'Boxed Warning'))
# Sildenafil: the pediatric tag came from the Viagra label; Revatio is approved for PAH in children 1–17 years.
edit('sildenafil', pop('pediatric', 'caution', 'برچسب Revatio: برای PAH در کودکان ۱ تا ۱۷ سال تأیید شده؛ برای اختلال نعوظ در کودکان کاربرد ندارد.', 'Revatio label: approved for PAH in children 1–17 years; erectile-dysfunction use does not apply to children.',
                         'The safety and efficacy of REVATIO have been established in pediatric patients 1 to 17 years old, for the treatment of PAH (WHO Group I) to improve exercise ability and, in patients too young to perform standard exercising testing, pulmonary hemodynamics thought to underlie improvements in exercise.', '8.4', source='fda-revatio'))
# Oncology: classifier read a cumulative-dose limit as paediatric avoidance and missed the summary fetal-harm statements; daratumumab's contraindication is only in combination.
edit('daunorubicin', pop('pediatric', 'caution', 'برچسب: در کودکان حد دوز تجمعی کمتر است (۳۰۰ mg/m² بالای ۲ سال، ۱۰ mg/kg زیر ۲ سال) — سمیت قلبی.', 'Label: children have lower cumulative limits (300 mg/m² over 2 years, 10 mg/kg under 2) — cardiotoxicity.',
                         'The incidence of myocardial toxicity increases after a total cumulative dose exceeding 400 to 550 mg/m 2 in adults, 300 mg/m 2 in children more than 2 years of age, or 10 mg/kg in children less than 2 years of age.', 'Warnings'))
FH_FA, FH_EN = 'برچسب: می‌تواند به جنین آسیب برساند؛ پیشگیری مؤثر لازم است.', 'Label: can cause fetal harm; effective contraception required.'
edit('fludarabine', pop('pregnancy', 'avoid', FH_FA, FH_EN, 'Can cause fetal harm. Advise patients of the potential risk to a fetus and to use effective contraception.', '5.8'))
edit('bendamustine', pop('pregnancy', 'avoid', FH_FA, FH_EN, 'Can cause fetal harm. Advise females of reproductive potential and males with female partners of reproductive potential of the potential risk to a fetus and to use an effective method of contraception.', '5.10'))
edit('daratumumab', pop('pregnancy', 'avoid', 'برچسب: ترکیب با لنالیدومید، پومالیدومید یا تالیدومید در بارداری منع مصرف است.', 'Label: combination with lenalidomide, pomalidomide or thalidomide is contraindicated in pregnancy.',
                        'The combination of DARZALEX and lenalidomide, pomalidomide, or thalidomide is contraindicated in pregnant women, because lenalidomide, pomalidomide, and thalidomide may cause birth defects and death of the unborn child.', '8.1'))
print('s14_post ok')
