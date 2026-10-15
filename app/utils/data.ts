import type { CatalogEntry, Category, Disease, Drug, Source } from '../../lib/types'
import sourcesJson from '../../data/sources.json'
import diseasesJson from '../../data/diseases.json'
import categoriesJson from '../../data/categories.json'
import catalogJson from '../generated/catalog.json'

export const sources = sourcesJson as Source[]
export const diseases = diseasesJson as Disease[]
export const categories = (categoriesJson as Category[]).slice().sort((a, b) => a.order - b.order)
export const catalog = catalogJson as CatalogEntry[]

export const getSource = (id: string) => sources.find((s) => s.id === id)
export const getDisease = (id: string) => diseases.find((d) => d.id === id)
export const getCategory = (id: string) => categories.find((c) => c.id === id)

const drugLoaders = import.meta.glob<Drug>('../../data/drugs/**/*.json', { import: 'default' })
export async function loadDrug(id: string): Promise<Drug | null> {
  const key = Object.keys(drugLoaders).find((k) => k.endsWith(`/${id}.json`))
  return key ? await drugLoaders[key]() : null
}
