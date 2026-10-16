import { normalize } from './normalize'
import type { CatalogEntry } from '../types'

// Ranks drugs for the type-ahead picker. Every query word must appear in the drug's names, brands or
// synonyms (spaces and half-spaces ignored). Name starts rank above name contains, which rank above
// brand/synonym hits. If nothing matches, words of 4+ letters may differ by one letter (typos).
const squash = (s: string) => normalize(s).replace(/[\s\-+/()]/g, '')

function within1(a: string, b: string): boolean {
  if (Math.abs(a.length - b.length) > 1) return false
  let i = 0, j = 0, edits = 0
  while (i < a.length && j < b.length) {
    if (a[i] === b[j]) { i++; j++; continue }
    if (++edits > 1) return false
    if (a.length > b.length) i++
    else if (a.length < b.length) j++
    else { i++; j++ }
  }
  return edits + (a.length - i) + (b.length - j) <= 1
}

export function pickDrugs<T extends CatalogEntry>(list: T[], query: string): T[] {
  const words = normalize(query).split(' ').filter(Boolean).map(squash).filter(Boolean)
  if (!words.length) return list
  const rows = list.map((d) => {
    const names = [d.name.fa, d.name.en].map(squash)
    const other = [...d.brands, ...d.synonyms].map(squash)
    return { d, names, all: [...names, ...other] }
  })
  const score = (r: (typeof rows)[number]) => {
    if (!words.every((w) => r.all.some((h) => h.includes(w)))) return -1
    const w = words[0]
    if (r.names.some((h) => h.startsWith(w))) return 3
    if (r.names.some((h) => h.includes(w))) return 2
    return 1
  }
  const hits = rows.map((r) => ({ r, s: score(r) })).filter((x) => x.s > 0)
  if (hits.length) return hits.sort((a, b) => b.s - a.s).map((x) => x.r.d)
  // Typo fallback: each word of 4+ letters is within one edit of some name/brand prefix of the same length.
  return rows
    .filter((r) => words.every((w) => w.length >= 4 && r.all.some((h) => within1(w, h.slice(0, w.length)) || within1(w, h.slice(0, w.length + 1)))))
    .map((r) => r.d)
}
