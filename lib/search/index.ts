import Fuse from 'fuse.js'
import type { CatalogEntry, Category, Disease } from '../types'
import { normalize } from './normalize'

export interface SearchResults { drugs: CatalogEntry[]; diseases: Disease[]; categories: Category[] }
type Doc = { kind: 'drug' | 'disease' | 'category'; i: number; terms: string[] }
const terms = (xs: (string | undefined)[]) => xs.filter((x): x is string => !!x).map(normalize)

export function createSearch(catalog: CatalogEntry[], diseases: Disease[], categories: Category[]) {
  const docs: Doc[] = [
    ...catalog.map((d, i) => ({ kind: 'drug' as const, i, terms: terms([d.name.fa, d.name.en, d.class?.fa, d.class?.en, ...d.brands, ...d.synonyms]) })),
    ...diseases.map((d, i) => ({ kind: 'disease' as const, i, terms: terms([d.name.fa, d.name.en, ...d.synonyms, ...d.icd10]) })),
    ...categories.map((c, i) => ({ kind: 'category' as const, i, terms: terms([c.name.fa, c.name.en]) })),
  ]
  const fuse = new Fuse(docs, { keys: ['terms'], threshold: 0.35, ignoreLocation: true })
  return (q: string, limit = 8): SearchResults => {
    const res: SearchResults = { drugs: [], diseases: [], categories: [] }
    const nq = normalize(q)
    if (!nq) return res
    for (const { item } of fuse.search(nq)) {
      if (item.kind === 'drug' && res.drugs.length < limit) res.drugs.push(catalog[item.i])
      if (item.kind === 'disease' && res.diseases.length < limit) res.diseases.push(diseases[item.i])
      if (item.kind === 'category' && res.categories.length < limit) res.categories.push(categories[item.i])
    }
    return res
  }
}
