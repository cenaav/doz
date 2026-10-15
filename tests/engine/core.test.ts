import { describe, expect, test } from 'vitest'
import { calculate } from '../../lib/engine'
import { inRange, toDays } from '../../lib/engine/age'
import { roundMl, roundTablets } from '../../lib/engine/rounding'
import { schwartzEgfr, mostellerBsa } from '../../lib/engine/renal'
import { drug, susp, R, yr, mo } from './helpers'

describe('age', () => {
  test('units', () => { expect(toDays({ value: 2, unit: 'year' })).toBe(730.5); expect(toDays({ value: 24, unit: 'month' })).toBe(730.5) })
  test('upper bound exclusive, lower inclusive', () => {
    const r = { minAge: { value: 6, unit: 'month' as const }, maxAge: { value: 2, unit: 'year' as const } }
    expect(inRange({ ageDays: mo(6), weightKg: 8 }, r)).toBe(true)
    expect(inRange({ ageDays: yr(2), weightKg: 12 }, r)).toBe(false)
    expect(inRange({ ageDays: yr(1.999), weightKg: 12 }, r)).toBe(true)
  })
  test('maxWeightKg is inclusive (labels say "≤ 40 kg")', () => {
    expect(inRange({ ageDays: yr(5), weightKg: 40 }, { maxWeightKg: 40 })).toBe(true)
    expect(inRange({ ageDays: yr(5), weightKg: 40.1 }, { maxWeightKg: 40 })).toBe(false)
  })
})

describe('rounding', () => {
  test('mL steps', () => {
    expect(roundMl(0.37)).toBe(0.35)
    expect(roundMl(6.75)).toBe(6.8)
    expect(roundMl(12.3)).toBe(12.5)
  })
  test('tablets', () => { expect(roundTablets(0.74, true)).toBe(0.5); expect(roundTablets(0.74, false)).toBe(1) })
})

describe('weightBased', () => {
  const amox = drug([{ dose: { perKgPerDay: 90, dividedDoses: 2 }, limits: { maxPerDose: 2000, maxPerDay: 4000, refs: R } }])
  test('12 kg', () => {
    const r = calculate(amox, 'r0', 'f', { ageDays: yr(2), weightKg: 12 })
    expect(r).toMatchObject({ status: 'ok', perDose: 540, perDay: 1080, dosesPerDay: 2, intervalHours: 12, mlPerDose: 6.75, mlPerDoseRounded: 6.8 })
    expect(r.capsApplied).toEqual([])
  })
  test('adult weight is capped and reported', () => {
    const r = calculate(amox, 'r0', 'f', { ageDays: yr(15), weightKg: 60 })
    expect(r.perDose).toBe(2000); expect(r.perDay).toBe(4000)
    expect(r.capsApplied.map((c) => c.kind)).toEqual(['maxPerDose'])
  })
  test('per-kg-per-dose with interval', () => {
    const d = drug([{ dose: { perKgPerDose: 15, intervalHours: 6 }, limits: { maxPerKgPerDay: 75, maxPerDay: 4000, refs: R } }], [susp('f', 160)])
    const r = calculate(d, 'r0', 'f', { ageDays: yr(3), weightKg: 14 })
    expect(r).toMatchObject({ perDose: 210, dosesPerDay: 4, perDay: 840, mlPerDose: 6.56, mlPerDoseRounded: 6.6 })
  })
  test('daily cap divides back to per dose', () => {
    const d = drug([{ dose: { perKgPerDay: 40, dividedDoses: 4 }, limits: { maxPerDay: 2000, refs: R } }])
    const r = calculate(d, 'r0', 'f', { ageDays: yr(16), weightKg: 70 })
    expect(r.perDay).toBe(2000); expect(r.perDose).toBe(500); expect(r.capsApplied[0].kind).toBe('maxPerDay')
  })
  test('mL unit (volume per kg)', () => {
    const d = drug([{ unit: 'mL', dose: { perKgPerDay: 1.5, dividedDoses: 1 } }], [{ ...susp('f', 10), concentration: { amount: 10, unit: 'g', perVolumeMl: 15 } }])
    expect(calculate(d, 'r0', 'f', { ageDays: yr(2), weightKg: 10 })).toMatchObject({ perDose: 15, mlPerDose: 15, mlPerDoseRounded: 15 })
  })
})

describe('fixed and bsa', () => {
  test('fixed', () => {
    expect(calculate(drug([{ type: 'fixed', dose: { perDose: 200, dosesPerDay: 2 } }]), 'r0', 'f', { ageDays: yr(10), weightKg: 30 }))
      .toMatchObject({ perDose: 200, perDay: 400, mlPerDose: 2.5 })
  })
  test('bsa needs height', () => {
    const d = drug([{ type: 'bsa', dose: { perM2PerDay: 100, dividedDoses: 2 } }])
    expect(calculate(d, 'r0', 'f', { ageDays: yr(10), weightKg: 30 }).status).toBe('invalidInput')
    const r = calculate(d, 'r0', 'f', { ageDays: yr(10), weightKg: 30, heightCm: 140 })
    expect(r.bsa).toBeCloseTo(mostellerBsa(140, 30), 3); expect(r.perDay).toBeCloseTo(108.01, 1)
  })
})

describe('input validation and safety', () => {
  const d = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }])
  test.each([0, -1, 301, NaN])('weight %s invalid', (w) => expect(calculate(d, 'r0', 'f', { ageDays: yr(2), weightKg: w }).status).toBe('invalidInput'))
  test.each([-1, yr(121), NaN])('age %s invalid', (a) => expect(calculate(d, 'r0', 'f', { ageDays: a, weightKg: 10 }).status).toBe('invalidInput'))
  test('implausible weight warns, still calculates', () => {
    const r = calculate(d, 'r0', 'f', { ageDays: yr(2), weightKg: 60 })
    expect(r.status).toBe('ok'); expect(r.warnings.map((w) => w.code)).toContain('WEIGHT_IMPLAUSIBLE')
  })
  test('outside population blocks', () => {
    const p = drug([{ population: { minAge: { value: 2, unit: 'month' } }, dose: { perKgPerDay: 30, dividedDoses: 3 } }])
    const r = calculate(p, 'r0', 'f', { ageDays: mo(1), weightKg: 4 })
    expect(r.status).toBe('blocked'); expect(r.blocks[0].code).toBe('OUTSIDE_POPULATION'); expect(r.perDose).toBeUndefined()
  })
  test('block contraindication stops calculation', () => {
    const c = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }], undefined, {
      contraindications: [{ id: 'infant', severity: 'block', rule: { maxAge: { value: 6, unit: 'month' } }, text: { en: 'no' }, refs: R }],
    })
    expect(calculate(c, 'r0', 'f', { ageDays: mo(3), weightKg: 6 }).status).toBe('blocked')
    expect(calculate(c, 'r0', 'f', { ageDays: mo(7), weightKg: 8 }).status).toBe('ok')
  })
  test('contraindication without rule is informational only', () => {
    const c = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }], undefined, {
      contraindications: [{ id: 'allergy', severity: 'block', text: { en: 'beta-lactam allergy' }, refs: R }],
    })
    const r = calculate(c, 'r0', 'f', { ageDays: yr(3), weightKg: 14 })
    expect(r.status).toBe('ok'); expect(r.blocks).toEqual([])
  })
  test('warn contraindication adds warning', () => {
    const c = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }], undefined, {
      contraindications: [{ id: 'w', severity: 'warn', rule: { maxAge: { value: 2, unit: 'year' } }, text: { en: 'careful' }, refs: R }],
    })
    expect(calculate(c, 'r0', 'f', { ageDays: yr(1), weightKg: 10 }).warnings.map((w) => w.code)).toContain('CONTRAINDICATION')
  })
  test('formulation not allowed blocks', () => {
    const c = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 }, allowedFormulations: ['g'] }], [susp('f', 400), susp('g', 600)])
    expect(calculate(c, 'r0', 'f', { ageDays: yr(2), weightKg: 12 }).blocks[0].code).toBe('FORMULATION_NOT_ALLOWED')
  })
  test('renal rule from Schwartz eGFR', () => {
    expect(schwartzEgfr(100, 1)).toBeCloseTo(41.3, 1)
    const c = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }], undefined, { renal: [{ egfrBelow: 50, severity: 'warn', text: { en: 'adjust' }, refs: R }] })
    const r = calculate(c, 'r0', 'f', { ageDays: yr(5), weightKg: 18, heightCm: 100, scrMgDl: 1 })
    expect(r.egfr).toBeCloseTo(41.3, 1); expect(r.warnings.map((w) => w.code)).toContain('RENAL')
  })
  test('tablet output', () => {
    const tab = { id: 't', form: 'tablet', route: 'oral', label: '250', concentration: { amount: 250, unit: 'mg' as const, perUnit: 'tablet' as const, scored: true }, markets: ['IR'], refs: R }
    const r = calculate(drug([{ type: 'fixed', dose: { perDose: 375, dosesPerDay: 2 } }], [tab]), 'r0', 't', { ageDays: yr(12), weightKg: 40 })
    expect(r).toMatchObject({ tabletsPerDose: 1.5, tabletsPerDoseRounded: 1.5 }); expect(r.mlPerDose).toBeUndefined()
  })
  test('tablet strength that cannot deliver the dose (>10% off) blocks instead of showing a rounded count', () => {
    const cap = { id: 'c', form: 'capsule', route: 'oral', label: '500', concentration: { amount: 500, unit: 'mg' as const, perUnit: 'capsule' as const }, markets: ['IR'], refs: R }
    const r = calculate(drug([{ dose: { perKgPerDay: 45, dividedDoses: 2 } }], [cap]), 'r0', 'c', { ageDays: yr(2), weightKg: 12 })
    expect(r.status).toBe('blocked'); expect(r.blocks[0].code).toBe('TABLET_ROUNDING'); expect(r.tabletsPerDoseRounded).toBeUndefined()
  })
  test('refs collected from regimen, limits and formulation', () => {
    const r = calculate(drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }]), 'r0', 'f', { ageDays: yr(2), weightKg: 12 })
    expect(r.refs.length).toBeGreaterThan(0)
  })
})

describe('weight optional when the regimen does not need it', () => {
  const ab = drug([{ type: 'ageBand', dose: { bands: [{ minAge: { value: 2, unit: 'year' }, maxAge: null, perDose: 5, dosesPerDay: 1 }] } }], [susp('f', 5)])
  test('ageBand without weight calculates', () => {
    expect(calculate(ab, 'r0', 'f', { ageDays: yr(4) })).toMatchObject({ status: 'ok', perDose: 5, mlPerDose: 5 })
  })
  test('weight-based regimen without weight is invalid input', () => {
    const wb = drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }])
    expect(calculate(wb, 'r0', 'f', { ageDays: yr(4) }).blocks[0].code).toBe('NEED_WEIGHT')
  })
  test('population with weight limits needs weight', () => {
    const pw = drug([{ type: 'fixed', population: { minWeightKg: 40 }, dose: { perDose: 500, dosesPerDay: 2 } }])
    expect(calculate(pw, 'r0', 'f', { ageDays: yr(30) }).blocks[0].code).toBe('NEED_WEIGHT')
  })
})
