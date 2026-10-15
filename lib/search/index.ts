import MiniSearch from 'minisearch'
import type { CatalogEntry, Category, Disease, I18nText } from '../types'
import { normalize } from './normalize'

type Hit<T> = T & { matched: string[] }
export interface SearchResults { drugs: Hit<CatalogEntry>[]; diseases: Hit<Disease>[]; categories: Hit<Category>[] }

interface Doc { id: string; kind: 'drug' | 'disease' | 'category'; i: number; name: string; alt: string; body: string }
const both = (t?: I18nText) => [t?.fa, t?.en].filter(Boolean).join(' ')

/** Full-text search over drugs, diseases (incl. symptoms) and categories, Persian/English, prefix + fuzzy. */
export function createSearch(catalog: CatalogEntry[], diseases: Disease[], categories: Category[]) {
  const diseaseById = new Map(diseases.map((d) => [d.id, d]))
  const docs: Doc[] = [
    ...catalog.map((d, i) => {
      const treats = [...new Set(d.regimens.map((r) => r.disease))].map((id) => diseaseById.get(id))
      return {
        id: `drug:${d.id}`, kind: 'drug' as const, i,
        name: [both(d.name), ...d.brands, ...d.synonyms].join(' '),
        alt: both(d.class),
        body: [
          ...d.regimens.map((r) => both(r.label)),
          ...treats.flatMap((x) => (x ? [both(x.name), ...x.synonyms, ...(x.symptoms?.items.map(both) ?? [])] : [])),
        ].join(' '),
      }
    }),
    ...diseases.map((d, i) => ({
      id: `disease:${d.id}`, kind: 'disease' as const, i,
      name: [both(d.name), ...d.synonyms, ...d.icd10].join(' '),
      alt: (d.symptoms?.items ?? []).map(both).join(' '),
      body: both(d.description?.text),
    })),
    ...categories.map((c, i) => ({ id: `category:${c.id}`, kind: 'category' as const, i, name: both(c.name), alt: '', body: '' })),
  ]
  const ms = new MiniSearch<Doc>({
    fields: ['name', 'alt', 'body'],
    storeFields: ['kind', 'i'],
    tokenize: (text) => normalize(text).split(/[^\p{L}\p{N}.]+/u).filter(Boolean),
    processTerm: (term) => normalize(term) || null,
    searchOptions: {
      boost: { name: 4, alt: 2, body: 1 },
      prefix: true,
      fuzzy: (term) => (term.length > 4 ? 0.2 : term.length > 3 ? 1 : 0),
      combineWith: 'OR',
    },
  })
  ms.addAll(docs)

  return (q: string, limit = 8): SearchResults => {
    const res: SearchResults = { drugs: [], diseases: [], categories: [] }
    if (!normalize(q)) return res
    // Prefer documents matching every word; fall back to any word.
    let hits = ms.search(q, { combineWith: 'AND' })
    if (!hits.length) hits = ms.search(q)
    for (const h of hits) {
      const doc = docs.find((d) => d.id === h.id)!
      const matched = matchedPhrases(doc, h.terms)
      if (doc.kind === 'drug' && res.drugs.length < limit) res.drugs.push({ ...catalog[doc.i], matched })
      if (doc.kind === 'disease' && res.diseases.length < limit) res.diseases.push({ ...diseases[doc.i], matched })
      if (doc.kind === 'category' && res.categories.length < limit) res.categories.push({ ...categories[doc.i], matched })
    }
    return res
  }

  function matchedPhrases(doc: Doc, terms: string[]): string[] {
    if (doc.kind !== 'disease') return []
    const d = diseases[doc.i]
    return (d.symptoms?.items ?? [])
      .flatMap((t) => [t.fa, t.en].filter((x): x is string => !!x))
      .filter((p) => terms.some((term) => normalize(p).split(' ').includes(term)))
  }
}
