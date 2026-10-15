"""Stage 3 — corrections after enrich.py (run after enrichment; enrich would overwrite them)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from gen import find, T

def edit(id, fn):
    p = find(id); d = json.load(open(p)); fn(d)
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')

def truvada(d):
    # The classifier matched a registry-method sentence; the label's risk summary reports no increased risk.
    d['populations']['pregnancy'].update(level='caution',
        text=T('برچسب: داده‌های مشاهده‌ای افزایش خطر نقص مادرزادی عمده را نشان نداده‌اند.', 'Label: observational data have shown no increased risk of major birth defects.'),
        quote='Data on the use of TRUVADA during pregnancy from observational studies have shown no increased risk of major birth defects.')

def epclusa(d):
    # Contraindication applies only to the ribavirin combination.
    d['populations']['pregnancy'].update(level='caution',
        text=T('برچسب: منع مصرف فقط برای ترکیب با ریباویرین (در زن باردار و مردی که همسرش باردار است)؛ برای اپکلوسا به‌تنهایی داده کافی نیست.', 'Label: contraindicated only in combination with ribavirin (pregnant women and men whose partners are pregnant); limited data for Epclusa alone.'))

def glucantime(d):
    # Darooyab page lists an unrelated product in its sidebar.
    d['iran']['forms'] = [f for f in d['iran']['forms'] if 'MEGLUMINE' in f['en']]

edit('emtricitabine-tenofovir', truvada)
edit('sofosbuvir-velpatasvir', epclusa)
edit('meglumine-antimoniate', glucantime)
print('s3_post ok')
