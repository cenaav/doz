# Doz — Design Spec

Date: 2026-10-15
Status: Draft for review

## 1. Purpose

Doz is a clinical decision-support web app that calculates drug doses for patients of all ages (neonates to adults), with a cited, verifiable reference behind every number, warning and note. Target users are physicians and pharmacists, including psychiatrists.

It replaces the role of the earlier Saphira calculator (nameofstone.github.io/Saphira), which had no per-drug sources and several dosing errors. Doz must support every drug Saphira supports, corrected and referenced.

### Success criteria

- Every dose, cap, contraindication, warning and note in the data carries at least one reference, or is explicitly shown as "no reference".
- For every drug, the clinician can see which sources are present and which are missing.
- A dose is never calculated past a per-dose, daily or adult cap without the cap being applied and shown.
- Age/weight contraindications marked `block` stop the calculation.
- Data is plain JSON, one file per drug, validated in CI; adding a drug needs no code change.
- Search finds drugs and diseases in Persian and English, by name, brand, synonym, ICD-10 code or category.
- Runs on phones, tablets, desktops and large monitors; Persian (RTL, Vazirmatn) and English (LTR); light and dark themes; works offline.
- Deployed automatically to GitHub Pages at `https://cenaav.github.io/doz/`.

### Non-goals (v1)

- No backend, accounts, or patient data storage. Nothing the user enters leaves the device.
- No e-prescribing or EHR integration.
- No IV infusion-rate/drip calculator (may be added later as a regimen type).

## 2. Stack and deployment

- Nuxt 4 (Vue 3.5) in static generation mode (`nuxt generate`): every page is pre-rendered to real HTML at build time, so drug and disease pages are indexable by search engines and render before JS loads on phones.
- `@nuxtjs/i18n` with `prefix_except_default` strategy: Persian at `/doz/...`, English at `/doz/en/...`. Each language version is its own indexable page with `hreflang` links.
- Tailwind CSS 4 for styling: logical properties for RTL/LTR, `dark:` variant for themes, responsive breakpoints. No component library.
- `@vite-pwa/nuxt` for offline use.
- Fuse.js for fuzzy search (client side, index built at build time).
- Vitest for unit tests; Ajv for JSON Schema validation.
- Vazirmatn (self-hosted via `@fontsource-variable/vazirmatn`, so offline works) for Persian; system font stack for English.
- SEO: per-page `<title>`, description, canonical, `hreflang`, Open Graph; `sitemap.xml` and `robots.txt` generated at build.
- GitHub Actions on push to `main`: install → validate data → test → `nuxt generate` (`app.baseURL: '/doz/'`) → deploy `.output/public` to Pages.
- One-time manual step: repo Settings → Pages → Source = "GitHub Actions".

## 3. Data model

```
data/
  sources.json                  reference registry
  diseases.json                 conditions
  categories.json               drug categories
  drugs/<category>/<drug-id>.json   one file per drug
schema/
  source.schema.json
  disease.schema.json
  category.schema.json
  drug.schema.json
docs/DATA_GUIDE.md              how to add/edit data
```

At build time all drug files are loaded (`import.meta.glob`), every drug/disease/category route is pre-rendered, and a search index is emitted. No runtime fetch is required.

All human-readable text is bilingual: `{ "fa": "...", "en": "..." }`. A missing language falls back to the other with a visible marker.

### 3.1 Source (`sources.json`)

```json
{
  "id": "fda-amoxicillin",
  "type": "fda-label",
  "title": "Amoxicillin for oral suspension — Prescribing Information",
  "publisher": "U.S. FDA / DailyMed",
  "edition": "Revised 2024-03",
  "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=...",
  "accessed": "2026-10-15",
  "license": "public"
}
```

`type` is one of:

- `fda-label`: FDA prescribing information (DailyMed). Cited by section number.
- `ema-smpc`: EU Summary of Product Characteristics. Cited by section.
- `guideline`: published guideline/article (AAP, NICE, WHO, IDSA…). Cited by journal, year, volume and page.
- `licensed-reference`: the licensed reference obtained via the medical school. Cited by edition and page. Placeholder entry exists; filled when the license arrives.
- `ifda-leaflet`: Iranian product leaflet / IFDA listing, for Iran-only products.
- `textbook`: other books, cited by edition and page.

`license`: `public` | `licensed` | `pending`. Text quoted from `licensed` sources must stay within license terms; the schema allows citation only (no quoted text field).

### 3.2 Reference (`refs` arrays, used everywhere)

```json
{ "source": "fda-amoxicillin", "section": "2.2", "page": null, "note": { "en": "Pediatric dosing table" } }
```

- `source` must exist in `sources.json` (CI check).
- At least one of `section` or `page` is required.
- Optional `url` overrides the source URL (deep link).

### 3.3 Disease (`diseases.json`)

```json
{
  "id": "acute-otitis-media",
  "name": { "fa": "اوتیت مدیای حاد", "en": "Acute otitis media" },
  "synonyms": ["AOM", "عفونت گوش میانی"],
  "icd10": ["H66.9"],
  "specialty": "pediatrics"
}
```

### 3.4 Category (`categories.json`)

`id`, bilingual `name`, `icon`, `order`. Initial categories: antibiotics, analgesics-antipyretics, respiratory, gastrointestinal, antiparasitic, antifungal, antihistamines, psychiatry (with subgroups: ADHD, antidepressants, antipsychotics, mood stabilizers, anxiolytics/hypnotics), then cardiology, neurology/anticonvulsants, emergency, endocrine in later phases.

### 3.5 Drug (`drugs/<category>/<id>.json`)

```json
{
  "id": "amoxicillin",
  "schemaVersion": 1,
  "name": { "fa": "آموکسی‌سیلین", "en": "Amoxicillin" },
  "category": "antibiotics",
  "class": { "fa": "پنی‌سیلین", "en": "Aminopenicillin" },
  "brands": [{ "name": "Amoxil", "market": "US" }],
  "synonyms": ["amoxycillin", "آموکسی"],

  "formulations": [
    {
      "id": "susp-250-5",
      "form": "suspension",
      "route": "oral",
      "label": "250 mg / 5 mL",
      "concentration": { "amount": 250, "unit": "mg", "perVolumeMl": 5 },
      "components": null,
      "markets": ["IR", "US"],
      "refs": [ ... ]
    }
  ],

  "regimens": [
    {
      "id": "aom-high-dose",
      "disease": "acute-otitis-media",
      "label": { "fa": "...", "en": "High-dose AOM" },
      "population": { "minAge": { "value": 2, "unit": "month" }, "maxAge": null, "minWeightKg": null, "maxWeightKg": null },
      "type": "weightBased",
      "unit": "mg",
      "dose": { "perKgPerDay": 90, "dividedDoses": 2 },
      "limits": { "maxPerDose": 2000, "maxPerDay": 4000, "refs": [ ... ] },
      "durationDays": { "min": 5, "max": 10 },
      "allowedFormulations": ["susp-400-5", "susp-250-5"],
      "refs": [ ... ],
      "notes": [ { "text": { "fa": "...", "en": "..." }, "refs": [ ... ] } ]
    }
  ],

  "contraindications": [
    { "id": "...", "severity": "block", "rule": { "maxAge": { "value": 6, "unit": "month" } },
      "text": { "fa": "...", "en": "..." }, "refs": [ ... ] }
  ],
  "warnings": [ { "text": {...}, "refs": [...] } ],
  "renal": [ { "egfrBelow": 30, "text": {...}, "refs": [...] } ],
  "monitoring": [ { "text": {...}, "refs": [...] } ],
  "interactions": [ { "with": "...", "text": {...}, "refs": [...] } ],

  "review": { "status": "unverified", "reviewer": null, "date": null },

  "examples": [
    { "regimen": "aom-high-dose", "formulation": "susp-400-5",
      "input": { "ageMonths": 24, "weightKg": 12 },
      "expect": { "perDose": 540, "mlPerDose": 6.75, "mlPerDoseRounded": 6.8, "dosesPerDay": 2 } }
  ]
}
```

#### Regimen types

Dose numbers are in the regimen's `unit` (`mg`, `mcg`, `g`, `unit`, `mL`; default `mg`). A formulation's `concentration` always gives the amount of the dosed ingredient per volume (liquids) or per tablet/capsule.

| type | dose fields | used for |
|---|---|---|
| `weightBased` | `perKgPerDay` + `dividedDoses`, or `perKgPerDose` + `intervalHours` | most pediatric drugs; with `unit: "mL"` also volume-per-kg drugs (lactulose) |
| `fixed` | `perDose` + `dosesPerDay` | adult/fixed dosing |
| `ageBand` | `bands[]`: age range → `perDose`, `dosesPerDay` | cetirizine, nitazoxanide… |
| `titration` | per-day `start`, `increment`, `incrementEveryDays`, `targetMin`, `targetMax`, `max`, `dividedDoses`; optional `weightBands` | psychiatry (methylphenidate, risperidone, SSRIs…) |
| `bsa` | `perM2PerDay` + `dividedDoses` (needs height) | selected drugs |
| `loading` | `days[]`: day range → `perKgPerDay`, `maxPerDay` | azithromycin 5-day |
| `notCalculated` | `reason` (bilingual) + refs | codeine combos, OTC age-label drugs |

A regimen may define `weightBands` instead of a single dose (e.g. risperidone in autism irritability: <20 kg vs ≥20 kg).

#### Combination products

`components[]` lists each ingredient with its amount per volume. The regimen names a `doseComponent` (e.g. amoxicillin), and other components may have their own `limits` (e.g. clavulanate max mg/kg/day). The engine checks all component limits; this is what stops the high-dose co-amoxiclav + 4:1 formulation error.

## 4. Dose engine

Pure JS module `src/engine/`, no Vue imports.

`calculate({ drug, regimenId, formulationId, patient }) → Result`

`patient`: `ageDays` (derived from input in days/months/years), `weightKg`, optional `heightCm`, `serumCreatinine`, `pna`/`pma` for neonates.

Result:
- `status`: `ok` | `blocked` | `notCalculated` | `invalidInput`
- `perDose` (mg, mL rounded to measurable precision), `perDay`, `dosesPerDay`, `intervalHours`, `duration`, `schedule` (for titration/loading: step list)
- `capsApplied[]`: which limit clipped the dose, with refs
- `warnings[]`: triggered warnings, contraindications (`warn`), plausibility issues
- `blocks[]`: triggered `block` contraindications
- `refs[]`: all refs used for this result

Rules:
- Caps apply in order: per-dose → per-day → adult cap. Each applied cap is reported.
- Population check: patient must be inside regimen `population`; otherwise `blocked` with reason.
- Age bands are inclusive-lower / exclusive-upper on `ageDays` to avoid gaps (Saphira's 1.9→2 gap bug).
- mL rounding: <1 mL → 0.05 mL; 1–10 mL → 0.1 mL; >10 mL → 0.5 mL. The unrounded value is shown too.
- Plausibility: weight outside the age's rough 1st–99th WHO/CDC percentile range → warning (not block). Weight ≤ 0 or > 300 kg, or age < 0 or > 120 y → `invalidInput`.
- eGFR (bedside Schwartz for <18 y: 0.413 × height / SCr) is computed only if height and creatinine are given; renal rules then trigger.

## 5. Reference display

- Each number in a result has a citation chip; tapping it opens a sheet with source title, edition, section, page, link and access date.
- Each drug page has a **Reference status** table listing every source type relevant to that drug with ✅ present (with locator) or ❌ not present, plus clinical review status (⚠️ unverified / ✅ verified by X on date).
- Items with no refs (should not pass CI for doses, but may exist for descriptive text) show "No reference" in red.
- Unverified drugs show an "Unverified" badge in lists, on the drug page and on every result.

## 6. Search

- One search box on the home page and in the header.
- Index entries: drugs (name fa/en, brands, synonyms, class, category), diseases (name, synonyms, ICD-10), categories.
- Persian normalization before indexing and querying: Arabic ي/ك → ی/ک, remove tatweel and diacritics, ZWNJ/half-space → space, Persian/Arabic digits → Latin, lowercase.
- Fuse.js fuzzy match; results grouped by type (Drugs, Diseases, Categories).
- Disease page lists every drug with a regimen for it, linking straight into the calculator with that regimen preselected.

## 7. Pages

All routes exist in Persian (no prefix) and English (`/en` prefix) and are pre-rendered.

| route | content |
|---|---|
| `/` | search, categories grid, recent drugs (localStorage) |
| `/category/:id` | drug list |
| `/drug/:id` | drug info, safety, reference status (static) + calculator (interactive) |
| `/disease/:id` | related drugs and regimens |
| `/sources` | all sources; licensed-reference placeholder |
| `/about` | disclaimer, how to use, data policy, review status explanation |
| `/settings` | language, theme |

Layout: single column on phones; two columns ≥ 768 px (list + detail); three columns ≥ 1280 px (list + calculator + references). Max content width on very large screens with larger base font.

## 8. Safety and disclaimer

- First-run modal: Doz is a decision-support tool for qualified professionals, not a substitute for clinical judgment, official prescribing information or local guidelines; data is under review. User must tick "I understand" (stored in localStorage, re-asked when disclaimer version changes).
- Permanent short disclaimer under every result.
- No result is shown without its refs.
- Saphira errors explicitly fixed: co-amoxiclav clavulanate limit; missing adult caps (amoxicillin, co-amoxiclav, erythromycin, TMP-SMX, ketotifen, lactulose, metronidazole-giardia); azithromycin days 2–5 cap = 250 mg; fexofenadine 2–11 y = 30 mg BID; age-band gaps; age-based contraindications enforced in weight mode (age is always required); domperidone EMA restriction; theophylline cap; Corizan component/age checks; metronidazole/nitazoxanide recategorized as antiparasitic.

## 9. Quality gates (CI)

1. JSON Schema validation for every data file.
2. Referential integrity: every `source`, `disease`, `category`, `allowedFormulations` id exists.
3. Every regimen, contraindication and limit has ≥ 1 ref (CI fails otherwise).
4. Every drug has ≥ 1 `example` per calculable regimen; all examples pass the engine.
5. Engine unit tests (caps, bands, rounding, titration, loading, components, blocks).
6. Build.

## 10. Data entry policy

- FDA label citations are checked against the live DailyMed label at entry time; section numbers and revision date recorded.
- Guideline citations include journal, year, volume and page from the published article.
- Licensed-reference fields stay empty until the license is in place; the UI shows them as ❌.
- Nothing is cited from memory alone. If a value cannot be verified, it is not entered, or entered as `notCalculated` with the reason.
- Every drug starts as `review.status: "unverified"`; only a named clinical reviewer changes it.

## 11. Phases

1. App shell, engine, schema, CI, deploy, search, disclaimer, i18n, themes — with a handful of drugs to prove each regimen type.
2. All Saphira drugs (42), corrected and referenced.
3. Psychiatry (ADHD, antidepressants, antipsychotics, mood stabilizers, anxiolytics/hypnotics).
4. Further categories one by one (cardiology, anticonvulsants, emergency, endocrine, …).
5. Licensed reference integration when the license arrives; clinical review sign-off.

Each phase ends with tests green and a deploy.
