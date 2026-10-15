import { createSearch } from '../../lib/search'
let fn: ReturnType<typeof createSearch> | null = null
export function useSearch() {
  fn ??= createSearch(catalog, diseases, categories)
  return { search: fn }
}
