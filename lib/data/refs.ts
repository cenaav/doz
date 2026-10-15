import type { Drug, Ref, Source, SourceType } from '../types'

export function collectRefs(node: unknown, out: Ref[] = []): Ref[] {
  if (Array.isArray(node)) node.forEach((n) => collectRefs(n, out))
  else if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (k === 'refs' && Array.isArray(v)) out.push(...(v as Ref[]))
      else collectRefs(v, out)
    }
  }
  return out
}

export function refKey(r: Ref): string {
  return `${r.source}|${r.section ?? ''}|${r.page ?? ''}`
}

export function uniqueRefs(refs: Ref[]): Ref[] {
  const seen = new Set<string>()
  return refs.filter((r) => (seen.has(refKey(r)) ? false : (seen.add(refKey(r)), true)))
}

export function groupRefsByType(refs: Ref[], sources: Source[]): Map<SourceType, Ref[]> {
  const byId = new Map(sources.map((s) => [s.id, s]))
  const map = new Map<SourceType, Ref[]>()
  for (const r of uniqueRefs(refs)) {
    const s = byId.get(r.source)
    if (!s) continue
    map.set(s.type, [...(map.get(s.type) ?? []), r])
  }
  return map
}

export function drugRefs(drug: Drug): Ref[] {
  return uniqueRefs(collectRefs(drug))
}
