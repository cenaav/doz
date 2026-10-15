"""Make every weightBand regimen in data/drugs contiguous (see gen.fix_bands). Idempotent."""
import glob, json, os
from gen import ROOT, fix_bands
for p in sorted(glob.glob(os.path.join(ROOT, 'drugs', '*', '*.json'))):
    d = json.load(open(p)); before = json.dumps(d)
    if json.dumps(fix_bands(d)) != before:
        json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n'); print('fixed', d['id'])
