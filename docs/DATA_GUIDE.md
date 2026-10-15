# Doz data guide

This guide explains how drug data is stored, how to add or change a drug, and the reference rules every entry must follow. All data lives in `data/` as JSON. No code change is needed to add a drug.

> **Safety rule:** every dose, limit, contraindication, warning and note must cite a source you have opened and read. Never enter a value or a section/page number from memory. If you cannot verify something, do not enter it.

## Folder layout

```
data/
  sources.json                     every source Doz can cite
  diseases.json                    diseases / indications
  categories.json                  drug categories shown on the home page
  drugs/<category>/<drug-id>.json  one file per drug
schema/*.schema.json               rules the files must follow (checked in CI)
```

A drug file must be at `data/drugs/<category>/<id>.json`, where `<category>` equals the drug's `category` field and the file name equals its `id`. IDs use lowercase letters, digits and hyphens (`amoxicillin-clavulanate`).

## Commands

```bash
npm run data:validate   # schema + integrity checks (unknown sources, missing refs, units, examples…)
npm test                # engine tests + every drug's worked examples
npm run dev             # run the app locally
```

CI runs both before every deploy. A pull request with a data error cannot be published.

## Sources (`data/sources.json`)

| field | meaning |
|---|---|
| `id` | short id used in refs, e.g. `fda-zithromax` |
| `type` | `fda-label`, `ema-smpc`, `guideline`, `licensed-reference`, `ifda-leaflet`, `textbook` |
| `short` | label shown on citation chips (max 24 characters), e.g. `FDA Zithromax` |
| `title` | full title |
| `publisher`, `edition`, `year`, `citation` | as printed by the source. For journal guidelines put `Authors. Journal Year;Vol(Issue):pages` in `citation` |
| `url` | link to the source (DailyMed: `https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=…`) |
| `accessed` | date you checked it (`YYYY-MM-DD`) |
| `license` | `public`, `licensed` or `pending` |

For FDA labels, record the SPL effective date and version in `edition` (shown on the DailyMed page, or in the SPL XML `effectiveTime` / `versionNumber`).

### Adding the licensed reference (medical school license)

1. In `sources.json`, replace the `licensed-primary` placeholder with the real details: `title`, `publisher`, `edition`, `year`, and set `license: "licensed"`.
2. Add refs with `"source": "licensed-primary"` and a `page` (and `section` if useful) to each regimen, limit or warning you have checked against it.
3. Only cite; do not paste text from a licensed book into Doz.

The drug page's reference status table then shows ✅ for the licensed reference automatically.

## References (`refs`)

```json
{ "source": "fda-zithromax", "section": "2.2, Table 3", "note": { "en": "…", "fa": "…" } }
```

- `source` must exist in `sources.json`.
- At least one of `section` or `page` is required.
- `page` accepts only printed page numbers or ranges: `39`, `e964`, `39-44`. Tables, headings and label sections go in `section` (`"2.2, Table 1"`, `"Directions"`).
- `url` (optional) overrides the source URL for a deep link.
- `note` (optional) explains what in the source supports the item, e.g. "50 kg and above row".

Everything that carries `refs` must have at least one: formulations, regimens, limits, contraindications, warnings, renal rules, monitoring, interactions and notes.

## Diseases (`data/diseases.json`)

`id`, `name` (`fa` and `en`), `synonyms` (search terms in both languages, abbreviations), `icd10` (ICD-10-CM codes; check them, e.g. via `https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code&terms=H66.90`), `specialty`.

## Drugs

Copy an existing file that is close to what you need (`antibiotics/amoxicillin.json` for weight-based, `psychiatry/risperidone.json` for titration) and edit it.

### Top-level fields

| field | meaning |
|---|---|
| `name`, `class` | `{ "fa": "…", "en": "…" }` |
| `brands` | `[{ "name": "Zithromax", "market": "US" }]` (two-letter market code) |
| `synonyms` | extra search terms, including common misspellings and Persian variants |
| `formulations` | products and strengths |
| `regimens` | one per disease × population × dosing scheme |
| `contraindications`, `warnings`, `renal`, `monitoring`, `interactions` | safety information, each item with refs |
| `review` | `{ "status": "unverified", "reviewer": null, "date": null }` |
| `examples` | worked examples, tested automatically |

### Formulations

```json
{
  "id": "susp-400-57", "form": "suspension", "route": "oral",
  "label": "400/57 mg per 5 mL (7:1)",
  "concentration": { "amount": 400, "unit": "mg", "perVolumeMl": 5 },
  "components": { "amoxicillin": { "name": {…}, "amount": 400, "unit": "mg" },
                  "clavulanate": { "name": {…}, "amount": 57, "unit": "mg" } },
  "markets": ["US"], "refs": [ … ]
}
```

- `concentration` is always the amount of the **dosed** ingredient, per `perVolumeMl` (liquids) or `perUnit` (`tablet`, `capsule`, `sachet`). Set `scored: true` for scored tablets so half tablets are allowed.
- `components` lists every ingredient of a combination product. A component may have its own `limits`; the engine blocks the calculation if that ingredient exceeds them (only add limits the source states).
- `markets`: where the product exists. Iranian products need an IFDA or leaflet source before `IR` is added.

### Regimens

Common fields: `id`, `disease` (id from `diseases.json`), `label`, `population`, `type`, `unit` (`mg`, `mcg`, `g`, `unit`, `mL`; default `mg`), `dose`, `refs`, and optionally `limits`, `durationDays`, `allowedFormulations`, `doseComponent`, `notes`.

`population` (and contraindication `rule`): `minAge`, `maxAge` as `{ "value": 3, "unit": "month" }` (units: `day`, `week`, `month`, `year`), `minWeightKg`, `maxWeightKg`.
- Age: `minAge` inclusive, `maxAge` exclusive. "3 months to 12 years" → `minAge 3 month`, `maxAge 13 year`.
- Weight: both inclusive. "≤ 40 kg" → `maxWeightKg: 40`. For "< 20 kg" / "≥ 20 kg" splits use titration `weightBands` (lower bound inclusive, upper exclusive).

| `type` | `dose` fields | example |
|---|---|---|
| `weightBased` | `perKgPerDay` + `dividedDoses`, or `perKgPerDose` + `intervalHours`. With `"unit": "mL"` the dose is a volume per kg | amoxicillin |
| `fixed` | `perDose` + `dosesPerDay` | adult 500 mg q12h |
| `ageBand` | `bands`: `[{ minAge, maxAge (null = no upper), perDose, dosesPerDay, refs? }]` | cetirizine, OTC ibuprofen |
| `bsa` | `perM2PerDay` + `dividedDoses` (needs height) | — |
| `loading` | `dividedDoses` + `days`: `[{ fromDay, toDay, perKgPerDay, maxPerDay }]` | azithromycin 5-day |
| `titration` | `dividedDoses` + `titration` `{ start, increment, incrementEveryDays, targetMin, targetMax, max }` (per day) or `weightBands` (same fields + `minWeightKg`, `maxWeightKg`) | risperidone |
| `notCalculated` | `reason` (bilingual) | codeine combinations, labels without pediatric dosing |

`limits`: `maxPerDose`, `maxPerDay`, `maxPerKgPerDose`, `maxPerKgPerDay` plus `refs`. The engine applies them in that order and shows the user every limit that was applied. Only add a limit the source states. If you derive one (e.g. the adult dose used as a ceiling), say so in the ref `note`.

`allowedFormulations`: restricts which products can be used with this regimen. Use it whenever the source ties a regimen to specific strengths (e.g. Augmentin q12h → 200/400 mg per 5 mL only; 90 mg/kg → ES-600 only). Choosing another product blocks the calculation.

`doseComponent`: for combination products, which component the dose refers to (e.g. `amoxicillin`).

### Contraindications

```json
{ "id": "under-6-months", "severity": "block", "rule": { "maxAge": { "value": 6, "unit": "month" } }, "text": {…}, "refs": [ … ] }
```

- `severity: "block"` stops the calculation when `rule` matches; `"warn"` shows a warning.
- Omit `rule` for conditions the calculator cannot check (allergy, CABG). Those are shown on the drug page but never evaluated.

### Renal rules

`{ "egfrBelow": 30, "severity": "warn", "text": {…}, "refs": [ … ] }`: triggered when height and creatinine are entered and bedside Schwartz eGFR (patients under 18) is below the value.

### Examples (required for every calculable regimen)

```json
{ "regimen": "aom-5day", "formulation": "susp-200-5",
  "input": { "ageYears": 15, "weightKg": 60 },
  "expect": { "perDose": 500 } }
```

Work out the expected numbers **by hand from the source**, not by copying the app's output. Use `"status": "blocked"` to prove a block works (e.g. too young, wrong formulation). If an example fails, find whether the data or the engine is wrong; do not change the expected number to match the app.

ML rounding shown to users: below 1 mL → nearest 0.05 mL; 1–10 mL → 0.1 mL; above 10 mL → 0.5 mL (`mlPerDoseRounded`). `mlPerDose` is the exact value.

## Clinical review

Every drug starts as `"status": "unverified"`, and every page and result shows an "Unverified" badge. Only a named clinical reviewer may set:

```json
"review": { "status": "verified", "reviewer": "Dr. Full Name, PharmD", "date": "2026-11-01" }
```

Validation rejects `verified` without both reviewer and date. Any later change to a verified drug should go back to `unverified` until it is reviewed again.
