# Data pipeline (maintainer tools)

Python scripts used to add drugs and enrich them. The JSON in `data/` stays the source of truth;
these tools only write it. Network responses are cached in `.cache/` (git-ignored).

- `net.py` — cached HTTP GET/POST
- `labels.py` — DailyMed search/fetch, SPL sections and approval, UK eMC SmPC sections, label digest/grep
- `darooyab.py` — Darooyab search, generic-page forms/brands, pregnancy category
- `atc.py` — WHO ATC/DDD code check
- `gen.py` — helpers for writing drugs, sources and diseases
- `classify.py` — special-population tags from label wording
- `enrich.py` — adds `atc`-category move, `iran`, `usApproval`, `links`, `populations` to drugs
- `stages/sN.py` — one script per batch of drugs; re-runnable

Typical batch: `python3 tools/pipeline/stages/s1.py && python3 tools/pipeline/enrich.py <ids…> && npm run data:validate && npm test`
