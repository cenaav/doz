import type { Msg, Patient } from './index'

// [ageYears, minKg, maxKg]; linear interpolation between rows. Heuristic for typo detection only.
const BOUNDS: [number, number, number][] = [
  [0, 1.7, 5.3], [0.5, 4.7, 11.5], [1, 6, 14.4], [2, 7.7, 17.8], [3, 8.9, 21.3], [5, 11.5, 28.2],
  [8, 15.7, 42.6], [10, 18.7, 55.2], [12, 23, 71.3], [15, 31.5, 92], [18, 35.7, 109],
]

export function plausibilityWarnings(p: Patient & { weightKg: number }): Msg[] {
  const y = p.ageDays / 365.25
  if (y >= 18) return []
  const i = BOUNDS.findIndex(([a]) => a > y)
  const [a0, lo0, hi0] = BOUNDS[i - 1]
  const [a1, lo1, hi1] = BOUNDS[i]
  const t = (y - a0) / (a1 - a0)
  const lo = lo0 + t * (lo1 - lo0)
  const hi = hi0 + t * (hi1 - hi0)
  return p.weightKg < lo || p.weightKg > hi
    ? [{ code: 'WEIGHT_IMPLAUSIBLE', params: { min: Math.round(lo * 10) / 10, max: Math.round(hi * 10) / 10 } }]
    : []
}
