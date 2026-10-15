import { describe, expect, test } from 'vitest'
import { calculate } from '../../lib/engine'
import { drug, susp, R, yr, mo } from './helpers'

const Y = (v: number) => ({ value: v, unit: 'year' as const })

describe('ageBand', () => {
  const d = drug([{ type: 'ageBand', dose: { bands: [
    { minAge: { value: 6, unit: 'month' }, maxAge: Y(2), perDose: 2.5, dosesPerDay: 1 },
    { minAge: Y(2), maxAge: Y(6), perDose: 2.5, dosesPerDay: 1 },
    { minAge: Y(6), maxAge: null, perDose: 10, dosesPerDay: 1, refs: R },
  ] } }], [susp('f', 5)])
  test.each([[1.95, 2.5], [2, 2.5], [5.99, 2.5], [6, 10], [40, 10]])('age %s → %s mg', (age, mg) => {
    expect(calculate(d, 'r0', 'f', { ageDays: yr(age), weightKg: age < 6 ? 14 : 30 }).perDose).toBe(mg)
  })
  test('below first band blocks', () => {
    expect(calculate(d, 'r0', 'f', { ageDays: mo(3), weightKg: 6 }).blocks[0].code).toBe('NO_AGE_BAND')
  })
})

describe('loading (azithromycin 5-day)', () => {
  const d = drug([{ type: 'loading', dose: { dividedDoses: 1, days: [
    { fromDay: 1, toDay: 1, perKgPerDay: 10, maxPerDay: 500 },
    { fromDay: 2, toDay: 5, perKgPerDay: 5, maxPerDay: 250 },
  ] } }], [susp('f', 200)])
  test('15 kg', () => {
    const r = calculate(d, 'r0', 'f', { ageDays: yr(4), weightKg: 15 })
    expect(r.schedule!.map((s) => s.perDay)).toEqual([150, 75])
    expect(r.schedule![0].mlPerDose).toBe(3.75)
  })
  test('60 kg caps each phase separately', () => {
    const r = calculate(d, 'r0', 'f', { ageDays: yr(15), weightKg: 60 })
    expect(r.schedule!.map((s) => s.perDay)).toEqual([500, 250])
    expect(r.schedule!.every((s) => s.capped)).toBe(true)
  })
})

describe('titration with weight bands (risperidone-like)', () => {
  const tab = { id: 't', form: 'tablet', route: 'oral', label: '0.5', concentration: { amount: 0.5, unit: 'mg' as const, perUnit: 'tablet' as const, scored: false }, markets: ['US'], refs: R }
  const d = drug([{ type: 'titration', dose: { dividedDoses: 1, weightBands: [
    { minWeightKg: 0, maxWeightKg: 20, start: 0.25, increment: 0.25, incrementEveryDays: 14, targetMin: 0.5, targetMax: 0.5, max: 1 },
    { minWeightKg: 20, maxWeightKg: null, start: 0.5, increment: 0.5, incrementEveryDays: 14, targetMin: 1, targetMax: 1, max: 2.5 },
  ] } }], [tab, susp('sol', 1, 1)])
  test('<20 kg band', () => {
    const r = calculate(d, 'r0', 'sol', { ageDays: yr(6), weightKg: 18 })
    expect(r.titration).toMatchObject({ start: 0.25, max: 1 }); expect(r.perDose).toBe(0.25); expect(r.mlPerDose).toBe(0.25)
  })
  test('unscored 0.5 mg tablet cannot give a 0.25 mg start dose', () => {
    expect(calculate(d, 'r0', 't', { ageDays: yr(6), weightKg: 18 }).blocks[0].code).toBe('TABLET_ROUNDING')
  })
  test('≥20 kg band', () => {
    expect(calculate(d, 'r0', 't', { ageDays: yr(9), weightKg: 20 }).titration!.start).toBe(0.5)
  })
})

describe('combination product limits (co-amoxiclav)', () => {
  const clavLimit = { maxPerKgPerDay: 10, refs: R }
  const f4 = susp('f4', 125, 5, { components: { amoxicillin: { name: { en: 'Amoxicillin' }, amount: 125, unit: 'mg' }, clavulanate: { name: { en: 'Clavulanate' }, amount: 31.25, unit: 'mg', limits: clavLimit } } })
  const f14 = susp('f14', 600, 5, { components: { amoxicillin: { name: { en: 'Amoxicillin' }, amount: 600, unit: 'mg' }, clavulanate: { name: { en: 'Clavulanate' }, amount: 42.9, unit: 'mg', limits: clavLimit } } })
  const d = drug([{ doseComponent: 'amoxicillin', dose: { perKgPerDay: 90, dividedDoses: 2 } }], [f4, f14])
  test('high dose with 4:1 blocked for clavulanate excess', () => {
    const r = calculate(d, 'r0', 'f4', { ageDays: yr(2), weightKg: 12 })
    expect(r.status).toBe('blocked'); expect(r.blocks[0].code).toBe('COMPONENT_LIMIT'); expect(r.perDose).toBeUndefined()
  })
  test('high dose with 14:1 ok', () => {
    expect(calculate(d, 'r0', 'f14', { ageDays: yr(2), weightKg: 12 })).toMatchObject({ status: 'ok', perDose: 540, mlPerDose: 4.5 })
  })
})

describe('notCalculated', () => {
  test('returns reason', () => {
    const d = drug([{ type: 'notCalculated', dose: { reason: { en: 'label is age-based OTC' } } }])
    expect(calculate(d, 'r0', 'f', { ageDays: yr(5), weightKg: 18 })).toMatchObject({ status: 'notCalculated', reason: { en: 'label is age-based OTC' } })
  })
})
