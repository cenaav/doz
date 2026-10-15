import type { DoseUnit, Limits } from '../types'
import type { CapHit } from './index'

export function applyLimits(perDose: number, dosesPerDay: number, weightKg: number, limits: Limits | undefined, unit: DoseUnit) {
  const hits: CapHit[] = []
  if (!limits) return { perDose, perDay: perDose * dosesPerDay, hits }
  const hit = (kind: CapHit['kind'], limit: number) => hits.push({ kind, limit, unit, refs: limits.refs })
  const doseCaps: [CapHit['kind'], number | undefined][] = [
    ['maxPerKgPerDose', limits.maxPerKgPerDose != null ? limits.maxPerKgPerDose * weightKg : undefined],
    ['maxPerDose', limits.maxPerDose],
  ]
  for (const [kind, cap] of doseCaps) if (cap != null && perDose > cap) { perDose = cap; hit(kind, cap) }
  let perDay = perDose * dosesPerDay
  const dayCaps: [CapHit['kind'], number | undefined][] = [
    ['maxPerKgPerDay', limits.maxPerKgPerDay != null ? limits.maxPerKgPerDay * weightKg : undefined],
    ['maxPerDay', limits.maxPerDay],
  ]
  for (const [kind, cap] of dayCaps) if (cap != null && perDay > cap) { perDay = cap; perDose = cap / dosesPerDay; hit(kind, cap) }
  return { perDose, perDay, hits }
}
