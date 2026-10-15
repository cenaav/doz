import type { CatalogEntry, Drug, Source } from '../types'
import { drugConfidence } from './refs'

export function buildCatalog(drugs: Drug[], sources: Source[] = []): CatalogEntry[] {
  return drugs
    .map((d) => ({
      id: d.id,
      category: d.category,
      name: d.name,
      class: d.class,
      brands: d.brands.map((b) => b.name),
      synonyms: d.synonyms,
      reviewStatus: d.review.status,
      confidence: drugConfidence(d, sources),
      markets: [...new Set(d.formulations.flatMap((f) => f.markets))],
      regimens: d.regimens.map((r) => ({ id: r.id, disease: r.disease, label: r.label, type: r.type })),
    }))
    .sort((a, b) => (a.name.en ?? a.id).localeCompare(b.name.en ?? b.id))
}
