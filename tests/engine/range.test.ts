import { describe, expect, test } from 'vitest'
import { calculate } from '../../lib/engine'
import { drug, susp, R, yr } from './helpers'

describe('dose ranges', () => {
  test('perKgPerDay range returns lower dose plus upper bound', () => {
    const d = drug([{ dose: { perKgPerDay: 25, perKgPerDayMax: 50, dividedDoses: 4 } }], [susp('f', 250)])
    const r = calculate(d, 'r0', 'f', { ageDays: yr(4), weightKg: 16 })
    expect(r).toMatchObject({ status: 'ok', perDose: 100, perDay: 400, mlPerDose: 2 })
    expect(r.upper).toMatchObject({ perDose: 200, perDay: 800, mlPerDose: 4, mlPerDoseRounded: 4 })
  })
  test('perKgPerDose range', () => {
    const d = drug([{ dose: { perKgPerDose: 5, perKgPerDoseMax: 10, intervalHours: 6 } }], [susp('f', 100)])
    const r = calculate(d, 'r0', 'f', { ageDays: yr(1), weightKg: 10 })
    expect(r.perDose).toBe(50); expect(r.upper?.perDose).toBe(100)
  })
  test('caps apply to the upper bound and are reported there', () => {
    const d = drug([{ dose: { perKgPerDay: 25, perKgPerDayMax: 50, dividedDoses: 2 }, limits: { maxPerDay: 1000, refs: R } }], [susp('f', 250)])
    const r = calculate(d, 'r0', 'f', { ageDays: yr(10), weightKg: 30 })
    expect(r.perDay).toBe(750); expect(r.capsApplied).toEqual([])
    expect(r.upper?.perDay).toBe(1000); expect(r.upper?.capsApplied.map((c) => c.kind)).toEqual(['maxPerDay'])
  })
  test('no range → no upper', () => {
    const r = calculate(drug([{ dose: { perKgPerDay: 30, dividedDoses: 3 } }]), 'r0', 'f', { ageDays: yr(3), weightKg: 14 })
    expect(r.upper).toBeUndefined()
  })
  test('fixed dose range (perDoseMax)', () => {
    const r = calculate(drug([{ type: 'fixed', dose: { perDose: 250, perDoseMax: 500, dosesPerDay: 4 } }], [susp('f', 250)]), 'r0', 'f', { ageDays: yr(30), weightKg: 70 })
    expect(r.perDose).toBe(250); expect(r.upper?.perDose).toBe(500)
  })
})
