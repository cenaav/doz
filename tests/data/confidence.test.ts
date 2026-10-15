import { describe, expect, test } from 'vitest'
import { buildCatalog } from '../../lib/data/catalog'
import { drugConfidence } from '../../lib/data/refs'
import type { Drug, Source } from '../../lib/types'

const sources: Source[] = [
  { id: 'fda', type: 'fda-label', short: 'FDA', title: 'x', license: 'public', url: 'https://x' },
  { id: 'web', type: 'secondary-web', short: 'Web', title: 'y', license: 'public', url: 'https://y' },
]
const R = (s: string) => [{ source: s, section: '1' }]
const mk = (doseSrc: string, extra: Partial<Drug> = {}): Drug => ({
  id: 'd', schemaVersion: 1, name: { en: 'D' }, category: 'c', brands: [], synonyms: [],
  formulations: [{ id: 'f', form: 'syrup', route: 'oral', label: 'f', concentration: { amount: 1, unit: 'mg', perVolumeMl: 1 }, markets: ['IR'], refs: R(doseSrc) }],
  regimens: [{ id: 'r', disease: 'x', label: { en: 'r' }, population: {}, type: 'fixed', dose: { perDose: 1, dosesPerDay: 1 }, refs: R(doseSrc) }],
  contraindications: [], warnings: [], renal: [], monitoring: [], interactions: [],
  review: { status: 'unverified', reviewer: null, date: null }, examples: [], ...extra,
})

describe('drug confidence', () => {
  test('primary sources → high', () => expect(drugConfidence(mk('fda'), sources)).toBe('high'))
  test('any regimen or formulation backed only by secondary web → low', () => expect(drugConfidence(mk('web'), sources)).toBe('low'))
  test('catalog carries confidence and markets', () => {
    const [c] = buildCatalog([mk('web')], sources)
    expect(c.confidence).toBe('low'); expect(c.markets).toEqual(['IR'])
  })
})
