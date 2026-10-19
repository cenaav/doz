"""Stage 13 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def pop(key, level, fa, en, quote, section):
    def fn(d):
        src = d['populations'][key]['refs'][0]['source']
        d['populations'][key].update(level=level, text=T(fa, en), quote=quote, refs=[{'source': src, 'section': section}])
    return fn

APR_FA, APR_EN = 'برچسب: داده‌های رجیستری بارداری (APR) تفاوتی با میزان زمینه‌ای نقص مادرزادی نشان نمی‌دهد.', 'Label: Antiretroviral Pregnancy Registry data show no difference from the background birth-defect rate.'
# Pregnancy: the classifier matched the registry-methodology sentence or a combination-only statement.
edit('nevirapine', pop('pregnancy', 'caution', APR_FA, APR_EN, 'Available data from the APR show no difference in the risk of overall major birth defects for nevirapine compared with the background rate for major birth defects of 2.7% in the U.S. reference population of the Metropolitan Atlanta Congenital Defects Program (MACDP).', '8.1'))
edit('lopinavir-ritonavir', pop('pregnancy', 'caution', 'برچسب: داده‌های رجیستری تفاوتی با میزان زمینه‌ای نقص مادرزادی نشان نمی‌دهد؛ در بارداری قرص ۴۰۰/۱۰۰ mg دو بار؛ محلول خوراکی (الکل) پرهیز شود.', 'Label: registry data show no difference from the background rate; in pregnancy use tablets 400/100 mg twice daily; avoid the oral solution (ethanol).',
                                 'Available data from the Antiretroviral Pregnancy Registry show no difference in the risk of overall major birth defects compared to the background rate for major birth defects of 2.7% in the U.S. reference population of the Metropolitan Atlanta Congenital Defects Program (MACDP).', '8.1'))
edit('ledipasvir-sofosbuvir', pop('pregnancy', 'caution', 'برچسب: داده انسانی کافی نیست؛ در مطالعات حیوانی عارضه‌ای دیده نشد. همراه ریباویرین در بارداری منع مصرف است.', 'Label: no adequate human data; no adverse developmental outcomes in animals. With ribavirin the combination is contraindicated in pregnancy.',
                                   'No adequate human data are available to establish whether or not HARVONI poses a risk to pregnancy outcomes. In animal reproduction studies, no evidence of adverse developmental outcomes was observed with the components of HARVONI.', '8.1'))
edit('mesna', pop('pregnancy', 'caution', 'برچسب: مسنا همراه ایفوسفامید یا سایر سیتوتوکسیک‌ها مصرف می‌شود؛ خطر جنینی از ایفوسفامید است (برچسب آن را ببینید).', 'Label: mesna is used with ifosfamide or other cytotoxics; fetal harm comes from ifosfamide (see its label).',
                     'Mesna is used in combination with ifosfamide or other cytotoxic agents. Ifosfamide can cause fetal harm when administered to a pregnant woman.', '8.1'))
print('s13_post ok')
