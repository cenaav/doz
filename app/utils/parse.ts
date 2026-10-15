import { normalize } from '../../lib/search/normalize'

/** Parses a user-typed number, accepting Persian/Arabic digits and decimal separators. */
export function parseNumber(s: string): number | null {
  const t = normalize(s).replace(/[٫,]/g, '.')
  if (!/^\d+(\.\d+)?$/.test(t)) return null
  return Number(t)
}
