# doz
Doz is a source-referenced drug dose calculator that helps physicians prescribe accurately for children and patients of all ages. Choose a drug, indication, age and weight to get the dose, frequency and exact volume, with maximum-dose limits, safety checks and a cited reference for every result.

**Live:** https://doz.amonproject.com (Cloudflare) · mirror: https://cenaav.github.io/doz/

> ⚠️ Doz is a decision-support tool for qualified healthcare professionals. It does not replace clinical judgment, official prescribing information or local guidelines. The data is under clinical review; drugs marked "Unverified" have not been signed off yet. Always check a dose against the original source before prescribing.

## Features

- Dose by drug, disease, age and weight: per dose, per day, interval, duration, and the exact volume or tablet count for the chosen product.
- A citation chip on every dose, limit, warning and note, opening the source, section or page, edition and link.
- A reference status table on each drug page showing which sources (FDA label, published guideline, licensed reference, Iranian leaflet) are present ✅ or missing ❌, plus the clinical review status.
- Per-dose and daily limits applied and shown; age contraindications block the calculation; formulation restrictions (e.g. ES-600 only for 90 mg/kg); warnings for implausible weight for age; renal rules from bedside Schwartz eGFR.
- Regimen types: weight-based, fixed, age bands, BSA, loading schedules and titration (psychiatry).
- Search across drugs, brands, diseases, synonyms and ICD-10 codes in Persian and English, tolerant of typos and Arabic/Persian letter variants.
- Persian (RTL, Vazirmatn) and English; light and dark themes; responsive from small phones to large monitors.
- Installable PWA: the app shell is cached after the first visit and every page you open stays available offline. No accounts and no server: patient inputs never leave the device.
- Every page is pre-rendered, so drug and disease pages are indexable by search engines.

## Development

Requires Node 24.

```bash
npm install
npm run dev        # http://localhost:3000
npm test           # engine, search and data tests (incl. every drug's worked examples)
npm run generate   # validate data, build catalog and pre-render the static site to .output/public
```

Stack: Nuxt 4 (static generation), Vue 3, Tailwind CSS 4, @nuxtjs/i18n, @vite-pwa/nuxt, MiniSearch, Ajv, Vitest.

```
lib/        dose engine, search, data validation (plain TypeScript, no Vue)
data/       sources, diseases, categories and one JSON file per drug
schema/     JSON Schemas for the data
app/        Nuxt app (pages, components)
i18n/       Persian and English UI strings
docs/       data guide, design spec, implementation plan
```

## Data

All drug data is JSON in `data/`. To add or update a drug, follow **[docs/DATA_GUIDE.md](docs/DATA_GUIDE.md)**. Every value must cite a source that was opened and checked; CI rejects data with missing references, unknown sources or failing worked examples.

Design: [docs/superpowers/specs/2026-10-15-doz-design.md](docs/superpowers/specs/2026-10-15-doz-design.md)

## Deployment

**Cloudflare (main site, doz.amonproject.com):** `npm run deploy:cf` builds the site and uploads `.output/public` as static assets to the `doz` Worker (`wrangler.jsonc`). Requires `npx wrangler login` once. `public/_headers` gives hashed `/_nuxt/` files a one-year cache.

**GitHub Pages (mirror):** 
Every push to `main` runs data validation, tests and the static build, then publishes to GitHub Pages (`.github/workflows/deploy.yml`). One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
