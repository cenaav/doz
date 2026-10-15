import type { CatalogEntry, Drug } from '../types'

export function buildCatalog(drugs: Drug[]): CatalogEntry[] {
  return drugs
    .map((d) => ({
      id: d.id,
      category: d.category,
      name: d.name,
      class: d.class,
      brands: d.brands.map((b) => b.name),
      synonyms: d.synonyms,
      reviewStatus: d.review.status,
      regimens: d.regimens.map((r) => ({ id: r.id, disease: r.disease, label: r.label })),
    }))
    .sort((a, b) => (a.name.en ?? a.id).localeCompare(b.name.en ?? b.id))
}
