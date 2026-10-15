import type { Category, Drug } from '../../lib/types'
import categoriesJson from '../../data/categories.json'
import categoryCountsJson from '../generated/category-counts.json'

// Large datasets live in their own modules (catalog.ts, sources.ts, diseases.ts) so pages
// that do not need them, like the home page, do not download them.
export const categories = (categoriesJson as Category[]).slice().sort((a, b) => a.order - b.order)
export const categoryCounts = categoryCountsJson as Record<string, number>
export const getCategory = (id: string) => categories.find((c) => c.id === id)

const drugLoaders = import.meta.glob<Drug>('../../data/drugs/**/*.json', { import: 'default' })
export async function loadDrug(id: string): Promise<Drug | null> {
  const key = Object.keys(drugLoaders).find((k) => k.endsWith(`/${id}.json`))
  return key ? await drugLoaders[key]() : null
}
