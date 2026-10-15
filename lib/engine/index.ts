import type { DoseUnit, Drug, I18nText, Ref } from '../types'
import { uniqueRefs } from '../data/refs'
import { inRange } from './age'
import { applyLimits } from './caps'
import { plausibilityWarnings } from './plausibility'
import { baseDose } from './regimens'
import { schwartzEgfr } from './renal'
import { r2, roundMl, roundTablets } from './rounding'

export interface Patient { ageDays: number; weightKg?: number; heightCm?: number; scrMgDl?: number }
export interface Msg { code: string; text?: I18nText; refs?: Ref[]; params?: Record<string, string | number> }
export interface CapHit { kind: 'maxPerKgPerDose' | 'maxPerDose' | 'maxPerKgPerDay' | 'maxPerDay'; limit: number; unit: DoseUnit; refs: Ref[] }
export interface ScheduleStep { fromDay: number; toDay: number; perDay: number; perDose: number; mlPerDose?: number; mlPerDoseRounded?: number; capped: boolean }
export interface TitrationPlan { start: number; increment?: number; incrementEveryDays?: number; targetMin?: number; targetMax?: number; max: number; dividedDoses: number }
export interface Result {
  status: 'ok' | 'blocked' | 'notCalculated' | 'invalidInput'
  unit: DoseUnit
  perDose?: number; perDay?: number; dosesPerDay?: number; intervalHours?: number
  mlPerDose?: number; mlPerDoseRounded?: number; mlPerDay?: number
  tabletsPerDose?: number; tabletsPerDoseRounded?: number; tabletUnit?: string
  durationDays?: { min: number; max: number } | null
  schedule?: ScheduleStep[]; titration?: TitrationPlan
  capsApplied: CapHit[]; warnings: Msg[]; blocks: Msg[]; refs: Ref[]
  egfr?: number; bsa?: number; reason?: I18nText
  /** Upper end of a dose range, when the source gives one. */
  upper?: Pick<Result, 'perDose' | 'perDay' | 'mlPerDose' | 'mlPerDoseRounded' | 'mlPerDay' | 'tabletsPerDose' | 'tabletsPerDoseRounded' | 'capsApplied'>
}

const MAX_AGE_DAYS = 120 * 365.25

/** Calculates a dose; when the regimen gives a range, `upper` holds the result for the top of the range. */
export function calculate(drug: Drug, regimenId: string, formulationId: string, p: Patient): Result {
  const res = calculateOne(drug, regimenId, formulationId, p)
  const reg = drug.regimens.find((r) => r.id === regimenId)
  const d = reg?.dose
  if (res.status !== 'ok' || !reg || !d || (d.perKgPerDayMax == null && d.perKgPerDoseMax == null && d.perDoseMax == null)) return res
  const upperDose = {
    ...d,
    perKgPerDay: d.perKgPerDayMax ?? d.perKgPerDay,
    perKgPerDose: d.perKgPerDoseMax ?? d.perKgPerDose,
    perDose: d.perDoseMax ?? d.perDose,
  }
  const hi = calculateOne({ ...drug, regimens: drug.regimens.map((r) => (r === reg ? { ...r, dose: upperDose } : r)) }, regimenId, formulationId, p)
  if (hi.status !== 'ok') return { ...res, warnings: [...res.warnings, ...hi.blocks] }
  const { perDose, perDay, mlPerDose, mlPerDoseRounded, mlPerDay, tabletsPerDose, tabletsPerDoseRounded, capsApplied } = hi
  return { ...res, upper: { perDose, perDay, mlPerDose, mlPerDoseRounded, mlPerDay, tabletsPerDose, tabletsPerDoseRounded, capsApplied } }
}

function calculateOne(drug: Drug, regimenId: string, formulationId: string, p: Patient): Result {
  const reg = drug.regimens.find((r) => r.id === regimenId)
  const form = drug.formulations.find((f) => f.id === formulationId)
  const unit = reg?.unit ?? 'mg'
  const res: Result = { status: 'ok', unit, capsApplied: [], warnings: [], blocks: [], refs: [] }
  const invalid = (code: string): Result => ({ ...res, status: 'invalidInput', blocks: [{ code }] })

  if (!reg) return invalid('UNKNOWN_REGIMEN')
  if (!form) return invalid('UNKNOWN_FORMULATION')
  if (p.weightKg == null) {
    if (needsWeight(drug, reg)) return invalid('NEED_WEIGHT')
  } else if (!Number.isFinite(p.weightKg) || p.weightKg <= 0 || p.weightKg > 300) return invalid('INVALID_WEIGHT')
  if (!Number.isFinite(p.ageDays) || p.ageDays < 0 || p.ageDays > MAX_AGE_DAYS) return invalid('INVALID_AGE')

  const refs: Ref[] = [...reg.refs, ...form.refs]
  if (p.weightKg != null) res.warnings.push(...plausibilityWarnings(p as Patient & { weightKg: number }))

  for (const c of drug.contraindications) {
    if (!c.rule || !inRange(p, c.rule)) continue
    const msg = { code: 'CONTRAINDICATION', text: c.text, refs: c.refs }
    ;(c.severity === 'block' ? res.blocks : res.warnings).push(msg)
    refs.push(...c.refs)
  }
  if (p.heightCm && p.scrMgDl) {
    if (p.ageDays < 18 * 365.25) {
      res.egfr = r2(schwartzEgfr(p.heightCm, p.scrMgDl))
      for (const rr of drug.renal) {
        if (res.egfr >= rr.egfrBelow) continue
        ;(rr.severity === 'block' ? res.blocks : res.warnings).push({ code: 'RENAL', text: rr.text, refs: rr.refs, params: { egfr: res.egfr } })
        refs.push(...rr.refs)
      }
    } else res.warnings.push({ code: 'EGFR_ADULT_NOT_COMPUTED' })
  }
  if (reg.allowedFormulations && !reg.allowedFormulations.includes(form.id)) res.blocks.push({ code: 'FORMULATION_NOT_ALLOWED', refs: reg.refs })
  if (!inRange(p, reg.population)) res.blocks.push({ code: 'OUTSIDE_POPULATION', refs: reg.refs })

  const done = (status: Result['status']): Result => ({ ...res, status, refs: uniqueRefs(refs) })
  if (res.blocks.length) return done('blocked')
  if (reg.type === 'notCalculated') return { ...done('notCalculated'), reason: reg.dose.reason }

  const base = baseDose(reg, p)
  if (base.error) {
    if (base.error.code === 'NEED_HEIGHT') return invalid('NEED_HEIGHT')
    res.blocks.push({ ...base.error, refs: reg.refs })
    return done('blocked')
  }
  if (base.extraRefs) refs.push(...base.extraRefs)
  if (reg.limits) refs.push(...reg.limits.refs)

  const n = base.dosesPerDay!
  const capped = applyLimits(base.perDose!, n, p.weightKg ?? 0, reg.limits, unit)
  res.capsApplied = capped.hits
  res.perDose = r2(capped.perDose)
  res.perDay = r2(capped.perDay)
  res.dosesPerDay = r2(n)
  res.intervalHours = r2(reg.dose.intervalHours ?? 24 / n)
  res.durationDays = reg.durationDays ?? null
  res.bsa = base.bsa
  res.titration = base.titration

  // other-ingredient limits for combination products
  if (form.components && reg.doseComponent) {
    for (const [key, comp] of Object.entries(form.components)) {
      if (key === reg.doseComponent || !comp.limits) continue
      const compPerDay = (capped.perDay * comp.amount) / form.concentration.amount
      const l = comp.limits
      const over = (l.maxPerKgPerDay != null && p.weightKg != null && compPerDay > l.maxPerKgPerDay * p.weightKg) || (l.maxPerDay != null && compPerDay > l.maxPerDay)
      if (over) {
        res.blocks.push({ code: 'COMPONENT_LIMIT', text: comp.name, refs: l.refs, params: { perDay: r2(compPerDay), unit: comp.unit } })
        refs.push(...l.refs)
      }
    }
    if (res.blocks.length) {
      const { perDose, perDay, dosesPerDay, intervalHours, ...rest } = res
      return { ...rest, status: 'blocked', refs: uniqueRefs(refs) }
    }
  }

  const c = form.concentration
  const toMl = (amount: number) => (unit === 'mL' ? amount : (amount * c.perVolumeMl!) / c.amount)
  if (c.perVolumeMl != null || unit === 'mL') {
    res.mlPerDose = r2(toMl(capped.perDose))
    res.mlPerDoseRounded = roundMl(toMl(capped.perDose))
    res.mlPerDay = r2(toMl(capped.perDay))
    res.schedule = base.schedule?.map((s) => ({ ...s, perDay: r2(s.perDay), perDose: r2(s.perDose), mlPerDose: r2(toMl(s.perDose)), mlPerDoseRounded: roundMl(toMl(s.perDose)) }))
  } else {
    const t = capped.perDose / c.amount
    const rounded = roundTablets(t, !!c.scored)
    // A strength that cannot deliver the dose within 10% must not be shown as a dose.
    if (rounded === 0 || Math.abs(rounded - t) / t > 0.1) {
      res.blocks.push({ code: 'TABLET_ROUNDING', params: { exact: r2(t), rounded } })
      const { perDose, perDay, dosesPerDay, intervalHours, ...rest } = res
      return { ...rest, status: 'blocked', refs: uniqueRefs(refs) }
    }
    res.tabletsPerDose = r2(t)
    res.tabletsPerDoseRounded = rounded
    res.tabletUnit = c.perUnit
    res.schedule = base.schedule?.map((s) => ({ ...s, perDay: r2(s.perDay), perDose: r2(s.perDose) }))
  }
  return done('ok')
}

/** True when the dose, its limits, its population or a contraindication depends on body weight. */
export function needsWeight(drug: Drug, reg: Drug['regimens'][number]): boolean {
  if (['weightBased', 'bsa', 'loading'].includes(reg.type) || reg.dose.weightBands) return true
  const hasW = (r?: { minWeightKg?: number | null; maxWeightKg?: number | null }) => r?.minWeightKg != null || r?.maxWeightKg != null
  if (hasW(reg.population) || drug.contraindications.some((c) => hasW(c.rule))) return true
  return reg.limits?.maxPerKgPerDay != null || reg.limits?.maxPerKgPerDose != null
}
