export type Lang = 'fa' | 'en'
export type I18nText = Partial<Record<Lang, string>>
export type AgeUnit = 'day' | 'week' | 'month' | 'year'
export interface Age { value: number; unit: AgeUnit }

export interface Ref {
  source: string
  section?: string | null
  page?: string | null
  url?: string
  note?: I18nText
}

export type SourceType = 'fda-label' | 'ema-smpc' | 'uk-smpc' | 'guideline' | 'licensed-reference' | 'ifda-leaflet' | 'textbook'
export interface Source {
  id: string
  type: SourceType
  short: string
  title: string
  publisher?: string
  edition?: string
  year?: number
  citation?: string
  url?: string
  accessed?: string
  license: 'public' | 'licensed' | 'pending'
}

export interface Range { minAge?: Age | null; maxAge?: Age | null; minWeightKg?: number | null; maxWeightKg?: number | null }

export type DoseUnit = 'mg' | 'mcg' | 'g' | 'unit' | 'mL'
export interface Concentration { amount: number; unit: DoseUnit; perVolumeMl?: number; perUnit?: 'tablet' | 'capsule' | 'sachet'; scored?: boolean }
export interface Limits { maxPerDose?: number; maxPerDay?: number; maxPerKgPerDose?: number; maxPerKgPerDay?: number; refs: Ref[] }
export interface Component { name: I18nText; amount: number; unit: DoseUnit; limits?: Limits }
export interface Formulation {
  id: string
  form: string
  route: string
  label: string
  concentration: Concentration
  components?: Record<string, Component> | null
  markets: string[]
  refs: Ref[]
}
export interface Note { text: I18nText; refs: Ref[] }

export interface AgeBandRow { minAge: Age; maxAge: Age | null; perDose: number; dosesPerDay: number; refs?: Ref[] }
export interface LoadingDay { fromDay: number; toDay: number; perKgPerDay: number; maxPerDay?: number }
export interface TitrationSteps { start: number; increment?: number; incrementEveryDays?: number; targetMin?: number; targetMax?: number; max: number }
export type RegimenType = 'weightBased' | 'fixed' | 'ageBand' | 'bsa' | 'loading' | 'titration' | 'notCalculated'
export interface Regimen {
  id: string
  disease: string
  label: I18nText
  population: Range
  type: RegimenType
  unit?: DoseUnit
  dose: {
    perKgPerDay?: number
    perKgPerDayMax?: number
    perKgPerDose?: number
    perKgPerDoseMax?: number
    dividedDoses?: number
    intervalHours?: number
    perDose?: number
    perDoseMax?: number
    dosesPerDay?: number
    perM2PerDay?: number
    bands?: AgeBandRow[]
    days?: LoadingDay[]
    titration?: TitrationSteps
    weightBands?: (TitrationSteps & { minWeightKg: number; maxWeightKg: number | null })[]
    reason?: I18nText
  }
  doseComponent?: string
  limits?: Limits
  durationDays?: { min: number; max: number } | null
  allowedFormulations?: string[]
  refs: Ref[]
  notes?: Note[]
}

export interface Contraindication { id: string; severity: 'block' | 'warn'; rule?: Range; text: I18nText; refs: Ref[] }
export interface RenalRule { egfrBelow: number; severity: 'block' | 'warn'; text: I18nText; refs: Ref[] }
export interface Example {
  regimen: string
  formulation: string
  input: { ageDays?: number; ageMonths?: number; ageYears?: number; weightKg: number; heightCm?: number; scrMgDl?: number }
  expect: Partial<Record<'status' | 'perDose' | 'perDay' | 'dosesPerDay' | 'mlPerDose' | 'mlPerDoseRounded' | 'tabletsPerDoseRounded' | 'upperPerDose' | 'upperPerDay' | 'upperMlPerDose' | 'upperMlPerDoseRounded', number | string>>
}
export interface Drug {
  id: string
  schemaVersion: 1
  name: I18nText
  category: string
  class?: I18nText
  brands: { name: string; market: string }[]
  synonyms: string[]
  formulations: Formulation[]
  regimens: Regimen[]
  contraindications: Contraindication[]
  warnings: Note[]
  renal: RenalRule[]
  monitoring: Note[]
  interactions: (Note & { with: string })[]
  review: { status: 'unverified' | 'verified'; reviewer: string | null; date: string | null }
  examples: Example[]
}
export interface Disease {
  id: string
  name: I18nText
  synonyms: string[]
  icd10: string[]
  specialty: string
  description?: Note
  symptoms?: { items: I18nText[]; refs: Ref[] }
}
export interface Category { id: string; name: I18nText; icon: string; order: number }
export interface CatalogEntry {
  id: string
  category: string
  name: I18nText
  class?: I18nText
  brands: string[]
  synonyms: string[]
  reviewStatus: 'unverified' | 'verified'
  regimens: { id: string; disease: string; label: I18nText }[]
}
export interface DataSet { sources: Source[]; diseases: Disease[]; categories: Category[]; drugs: { path: string; drug: Drug }[] }
