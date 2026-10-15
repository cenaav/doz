import type { Drug, Regimen, Formulation } from '../../lib/types'
export const R = [{ source: 's', section: '1' }]
export const susp = (id: string, amount: number, perVolumeMl = 5, extra: Partial<Formulation> = {}): Formulation =>
  ({ id, form: 'suspension', route: 'oral', label: id, concentration: { amount, unit: 'mg', perVolumeMl }, markets: ['IR'], refs: R, ...extra })
export function drug(regimens: Partial<Regimen>[], formulations: Formulation[] = [susp('f', 400)], extra: Partial<Drug> = {}): Drug {
  return {
    id: 'd', schemaVersion: 1, name: { en: 'D' }, category: 'c', brands: [], synonyms: [],
    formulations,
    regimens: regimens.map((r, i) => ({ id: `r${i}`, disease: 'x', label: { en: 'r' }, population: {}, type: 'weightBased', dose: {}, refs: R, ...r }) as Regimen),
    contraindications: [], warnings: [], renal: [], monitoring: [], interactions: [],
    review: { status: 'unverified', reviewer: null, date: null }, examples: [], ...extra,
  }
}
export const yr = (y: number) => y * 365.25
export const mo = (m: number) => m * 30.4375
