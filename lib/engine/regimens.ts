import type { Drug, Regimen } from '../types'
import { toDays } from './age'
import type { Msg, Patient, ScheduleStep, TitrationPlan } from './index'

export interface BaseDose {
  perDose?: number; dosesPerDay?: number
  schedule?: Omit<ScheduleStep, 'mlPerDose' | 'mlPerDoseRounded'>[]
  titration?: TitrationPlan
  bsa?: number
  error?: Msg
  extraRefs?: Drug['regimens'][number]['refs']
}

export function baseDose(reg: Regimen, p: Patient): BaseDose {
  const d = reg.dose
  switch (reg.type) {
    case 'weightBased':
      if (d.perKgPerDay != null) return { perDose: (d.perKgPerDay * p.weightKg) / d.dividedDoses!, dosesPerDay: d.dividedDoses }
      return { perDose: d.perKgPerDose! * p.weightKg, dosesPerDay: 24 / d.intervalHours! }
    case 'fixed':
      return { perDose: d.perDose, dosesPerDay: d.dosesPerDay }
    case 'bsa': {
      if (!p.heightCm) return { error: { code: 'NEED_HEIGHT' } }
      const bsa = Math.sqrt((p.heightCm * p.weightKg) / 3600)
      return { perDose: (d.perM2PerDay! * bsa) / d.dividedDoses!, dosesPerDay: d.dividedDoses, bsa }
    }
    case 'ageBand': {
      const b = d.bands!.find((x) => p.ageDays >= toDays(x.minAge) && (!x.maxAge || p.ageDays < toDays(x.maxAge)))
      if (!b) return { error: { code: 'NO_AGE_BAND' } }
      return { perDose: b.perDose, dosesPerDay: b.dosesPerDay, extraRefs: b.refs }
    }
    case 'loading': {
      const n = d.dividedDoses!
      const schedule = d.days!.map((x) => {
        const raw = x.perKgPerDay * p.weightKg
        const perDay = x.maxPerDay != null ? Math.min(raw, x.maxPerDay) : raw
        return { fromDay: x.fromDay, toDay: x.toDay, perDay, perDose: perDay / n, capped: perDay < raw }
      })
      return { perDose: schedule[0].perDose, dosesPerDay: n, schedule }
    }
    case 'titration': {
      const steps = d.titration ?? d.weightBands!.find((w) => p.weightKg >= w.minWeightKg && (w.maxWeightKg == null || p.weightKg < w.maxWeightKg))
      if (!steps) return { error: { code: 'NO_WEIGHT_BAND' } }
      const n = d.dividedDoses!
      const { start, increment, incrementEveryDays, targetMin, targetMax, max } = steps
      return { perDose: start / n, dosesPerDay: n, titration: { start, increment, incrementEveryDays, targetMin, targetMax, max, dividedDoses: n } }
    }
    default:
      return {}
  }
}
