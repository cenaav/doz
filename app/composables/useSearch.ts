import type { createSearch } from '../../lib/search'
type SearchFn = ReturnType<typeof createSearch>
let loading: Promise<SearchFn> | null = null

/** Loads the catalog and builds the search index on first use, so pages render without them. */
export function loadSearch(): Promise<SearchFn> {
  loading ??= Promise.all([import('../../lib/search'), import('../utils/catalog'), import('../utils/diseases')])
    .then(([s, c, d]) => s.createSearch(c.catalog, d.diseases, categories))
  return loading
}

export function useSearch() {
  const search = shallowRef<SearchFn | null>(null)
  const load = () => loadSearch().then((fn) => (search.value = fn))
  return { search, load }
}
