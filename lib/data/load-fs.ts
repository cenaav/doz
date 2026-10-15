import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import type { DataSet, Drug } from '../types'

const readJson = (p: string) => JSON.parse(readFileSync(p, 'utf8'))

function walk(dir: string): string[] {
  return readdirSync(dir).flatMap((f) => {
    const p = join(dir, f)
    return statSync(p).isDirectory() ? walk(p) : p.endsWith('.json') ? [p] : []
  })
}

export function loadDataSet(root: string): DataSet {
  const dataDir = join(root, 'data')
  return {
    sources: readJson(join(dataDir, 'sources.json')),
    diseases: readJson(join(dataDir, 'diseases.json')),
    categories: readJson(join(dataDir, 'categories.json')),
    collections: existsSync(join(dataDir, 'collections.json')) ? readJson(join(dataDir, 'collections.json')) : [],
    drugs: walk(join(dataDir, 'drugs'))
      .sort()
      .map((p) => ({ path: relative(dataDir, p), drug: readJson(p) as Drug })),
  }
}
