import { describe, expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'
import { calculate, type Result } from '../../lib/engine'
import type { Age, Range } from '../../lib/types'

// Runs every calculable regimen of every drug with every allowed formulation over a spread of
// patients, and checks invariants that must hold for any result the calculator shows.
const ds = loadDataSet(join(__dirname, '../..'))
const YEAR = 365.25
// Typical weights for age (rough growth-chart medians), plus light and heavy adults.
const patients = [
  { ageDays: 10, weightKg: 3.5 },
  { ageDays: 0.5 * YEAR, weightKg: 7.5 },
  { ageDays: 1 * YEAR, weightKg: 10 },
  { ageDays: 3 * YEAR, weightKg: 14 },
  { ageDays: 6 * YEAR, weightKg: 20 },
  { ageDays: 10 * YEAR, weightKg: 32 },
  { ageDays: 14 * YEAR, weightKg: 50 },
  { ageDays: 30 * YEAR, weightKg: 45 },
  { ageDays: 40 * YEAR, weightKg: 70 },
  { ageDays: 50 * YEAR, weightKg: 120 },
  { ageDays: 80 * YEAR, weightKg: 60 },
]

// Rough median weight for an age, used to place a patient inside a regimen's own age range.
const weightFor = (years: number) => (years < 1 ? 3.5 + years * 6 : years < 13 ? 2 * years + 8 : years < 18 ? 4 * years - 6 : 70)
// Rough median height, only used by body-surface-area regimens.
const heightFor = (years: number) => (years < 1 ? 50 + years * 25 : years < 13 ? 75 + 6 * (years - 1) : 165)
const toYears = (a?: Age | null) => (a ? (a.value * { day: 1, week: 7, month: 30.4375, year: YEAR }[a.unit]) / YEAR : undefined)
function insidePatient(pop: Range) {
  const lo = toYears(pop.minAge) ?? 0
  const hi = toYears(pop.maxAge) ?? Math.max(lo + 1, 60)
  const years = (lo + hi) / 2
  let w = weightFor(years)
  if (pop.minWeightKg != null) w = Math.max(w, pop.minWeightKg)
  if (pop.maxWeightKg != null) w = Math.min(w, pop.maxWeightKg)
  if (pop.minWeightKg != null && pop.maxWeightKg != null) w = (pop.minWeightKg + pop.maxWeightKg) / 2
  return { ageDays: years * YEAR, weightKg: w }
}

const numbers = (r: Result) =>
  [r.perDose, r.perDay, r.mlPerDose, r.mlPerDoseRounded, r.mlPerDay, r.tabletsPerDose, r.tabletsPerDoseRounded, r.upper?.perDose, r.upper?.perDay].filter((n) => n != null) as number[]

const neverDosed: string[] = []
for (const { drug } of ds.drugs) {
  const regimens = drug.regimens.filter((r) => r.type !== 'notCalculated')
  if (!regimens.length) continue
  describe(drug.id, () => {
    for (const reg of regimens) {
      const forms = drug.formulations.filter((f) => !reg.allowedFormulations || reg.allowedFormulations.includes(f.id))
      test(`${reg.id}: ${forms.length} formulation(s) × ${patients.length} patients`, () => {
        expect(forms.length, 'regimen has no usable formulation').toBeGreaterThan(0)
        let okCount = 0
        for (const f of forms) {
          for (const p of [...patients, insidePatient(reg.population)]) {
            const r = calculate(drug, reg.id, f.id, { ...p, heightCm: heightFor(p.ageDays / YEAR) })
            const where = `${f.id} age ${(p.ageDays / YEAR).toFixed(1)}y ${p.weightKg}kg`
            expect(['ok', 'blocked', 'notCalculated', 'invalidInput'], where).toContain(r.status)
            for (const n of numbers(r)) {
              expect(Number.isFinite(n), `${where}: non-finite number`).toBe(true)
              expect(n, `${where}: negative number`).toBeGreaterThanOrEqual(0)
            }
            if (r.status !== 'ok') continue
            okCount++
            expect(r.perDose, `${where}: ok without dose`).toBeGreaterThan(0)
            const l = reg.limits
            const eps = 1e-6
            if (l?.maxPerDose != null) expect(r.perDose!, `${where}: over maxPerDose`).toBeLessThanOrEqual(l.maxPerDose + eps)
            if (l?.maxPerDay != null && r.perDay != null) expect(r.perDay, `${where}: over maxPerDay`).toBeLessThanOrEqual(l.maxPerDay + eps)
            if (l?.maxPerKgPerDose != null) expect(r.perDose!, `${where}: over maxPerKgPerDose`).toBeLessThanOrEqual(l.maxPerKgPerDose * p.weightKg + eps)
            if (l?.maxPerKgPerDay != null && r.perDay != null) expect(r.perDay, `${where}: over maxPerKgPerDay`).toBeLessThanOrEqual(l.maxPerKgPerDay * p.weightKg + eps)
            // A liquid dose must convert to the volume the label concentration gives.
            const c = f.concentration
            if (c.perVolumeMl && r.mlPerDose != null && r.unit === c.unit && !reg.doseComponent) {
              expect(r.mlPerDose, `${where}: mL does not match concentration`).toBeCloseTo((r.perDose! * c.perVolumeMl) / c.amount, 1)
            }
            // A tablet result must not be more than 10% away from the exact dose.
            if (r.tabletsPerDose != null && r.tabletsPerDoseRounded != null && r.tabletsPerDose > 0) {
              expect(Math.abs(r.tabletsPerDoseRounded - r.tabletsPerDose) / r.tabletsPerDose, `${where}: tablet rounding > 10%`).toBeLessThanOrEqual(0.1 + eps)
            }
          }
        }
        // Each calculable regimen must give a dose for at least one realistic patient, unless every
        // block is a deliberate safety stop (no strength gives the dose within 10%, or outside the label's range).
        if (!okCount) {
          const codes = new Set(forms.flatMap((f) => [...patients, insidePatient(reg.population)].flatMap((p) => calculate(drug, reg.id, f.id, { ...p, heightCm: heightFor(p.ageDays / YEAR) }).blocks.map((b) => b.code))))
          expect([...codes].filter((c) => !['TABLET_ROUNDING', 'OUTSIDE_POPULATION', 'CONTRAINDICATION'].includes(c)), 'no dose for any patient').toEqual([])
          neverDosed.push(`${drug.id}/${reg.id}`)
        }
      })
    }
  })
}

// Regimens the calculator can never dose with the strengths on file; listed so they stay visible.
test('regimens blocked for every patient by tablet strength', () => {
  expect(neverDosed.length).toBeLessThan(20)
})
