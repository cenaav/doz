import type { Age, AgeUnit, Range } from '../types'
import type { Patient } from './index'

const DAYS: Record<AgeUnit, number> = { day: 1, week: 7, month: 30.4375, year: 365.25 }
export const toDays = (a: Age) => a.value * DAYS[a.unit]

export function ageDaysFrom(i: { ageDays?: number; ageMonths?: number; ageYears?: number }): number {
  if (i.ageDays != null) return i.ageDays
  if (i.ageMonths != null) return i.ageMonths * DAYS.month
  return (i.ageYears ?? NaN) * DAYS.year
}

export function inRange(p: Patient, r: Range): boolean {
  if (r.minAge && p.ageDays < toDays(r.minAge)) return false
  if (r.maxAge && p.ageDays >= toDays(r.maxAge)) return false
  if (r.minWeightKg != null && (p.weightKg == null || p.weightKg < r.minWeightKg)) return false
  if (r.maxWeightKg != null && (p.weightKg == null || p.weightKg > r.maxWeightKg)) return false
  return true
}
