import type { CatalogEntry, Collection, Drug, Source } from '../types'
import { toDays } from '../engine/age'
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
      atc: d.atc ?? [],
      regimens: d.regimens.map((r) => ({ id: r.id, disease: r.disease, label: r.label, type: r.type })),
    }))
    .sort((a, b) => (a.name.en ?? a.id).localeCompare(b.name.en ?? b.id))
}

/** True when any calculable regimen covers patients under 18 years. */
export function hasPediatricDose(d: Drug): boolean {
  const adult = toDays({ value: 18, unit: 'year' })
  return d.regimens.some((r) => r.type !== 'notCalculated' && (!r.population.minAge || toDays(r.population.minAge) < adult))
}

/** Collections with their drug lists resolved (curated ids plus, when asked, every drug with a child dose). */
export function resolveCollections(collections: Collection[], drugs: Drug[]): Collection[] {
  return collections.map((c) => ({
    ...c,
    drugs: [...new Set([...c.drugs, ...(c.pediatricAuto ? drugs.filter(hasPediatricDose).map((d) => d.id) : [])])],
  }))
}
