import { mkdirSync, writeFileSync } from 'node:fs'
import { loadDataSet } from '../lib/data/load-fs'
import { buildCatalog, resolveCollections } from '../lib/data/catalog'

const SITE = 'https://doz.amonproject.com'
const ds = loadDataSet(process.cwd())
const catalog = buildCatalog(ds.drugs.map((d) => d.drug), ds.sources)
const collections = resolveCollections(ds.collections ?? [], ds.drugs.map((d) => d.drug))
const paths = [
  '/',
  '/sources',
  '/about',
  '/settings',
  '/diseases',
  '/calculator',
  ...ds.categories.map((c) => `/category/${c.id}`),
  ...collections.map((c) => `/collection/${c.id}`),
  ...catalog.map((d) => `/drug/${d.id}`),
  ...ds.diseases.map((d) => `/disease/${d.id}`),
]
const routes = paths.flatMap((p) => [p, p === '/' ? '/en' : `/en${p}`])
mkdirSync('app/generated', { recursive: true })
writeFileSync('app/generated/catalog.json', JSON.stringify(catalog))
writeFileSync('app/generated/routes.json', JSON.stringify(routes))
writeFileSync('app/generated/collections.json', JSON.stringify(collections))
const counts = Object.fromEntries(ds.categories.map((c) => [c.id, catalog.filter((d) => d.category === c.id).length]))
writeFileSync('app/generated/category-counts.json', JSON.stringify(counts))
const urls = routes.map((r) => `<url><loc>${SITE}${r}</loc></url>`).join('')
writeFileSync('public/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`)
console.log(`✓ catalog: ${catalog.length} drugs, ${routes.length} routes`)
