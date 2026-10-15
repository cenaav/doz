import { describe, expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'
import { validateDataSet } from '../../lib/data/validate'
import type { DataSet } from '../../lib/types'

const repo = join(__dirname, '../..')
const fixture = () => loadDataSet(join(__dirname, 'fixtures/valid'))
const errorsOf = (mut: (ds: DataSet) => void) => {
  const ds = fixture()
  mut(ds)
  return validateDataSet(ds, repo)
}

describe('validateDataSet', () => {
  test('valid fixture passes', () => expect(validateDataSet(fixture(), repo)).toEqual([]))
  test('regimen without refs fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [] }).join()).toMatch(/refs/)
  })
  test('ref without section or page fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [{ source: 'fda-x' }] }).length).toBeGreaterThan(0)
  })
  test('page must be a page number, not a table label', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [{ source: 'fda-x', page: 'Table 1' }] }).join()).toMatch(/page/)
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [{ source: 'fda-x', page: 'e964' }] })).toEqual([])
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [{ source: 'fda-x', page: '39-44' }] })).toEqual([])
  })
  test('disease symptoms with refs pass', () => {
    expect(errorsOf((ds) => { ds.diseases[0].symptoms = { items: [{ en: 'Fever' }], refs: [{ source: 'fda-x', section: 'Symptoms' }] } })).toEqual([])
  })
  test('disease symptoms without refs fail', () => {
    expect(errorsOf((ds) => { ds.diseases[0].symptoms = { items: [{ en: 'Fever' }], refs: [] } }).length).toBeGreaterThan(0)
  })
  test('disease symptoms with unknown source fail', () => {
    expect(errorsOf((ds) => { ds.diseases[0].symptoms = { items: [{ en: 'Fever' }], refs: [{ source: 'nope', section: 'x' }] } }).join()).toMatch(/unknown source nope/)
  })
  test('source without online link fails (unless license pending)', () => {
    expect(errorsOf((ds) => { delete (ds.sources[0] as any).url }).join()).toMatch(/fda-x.*url|url.*fda-x/)
    expect(errorsOf((ds) => { delete (ds.sources[0] as any).url; ds.sources[0].license = 'pending' })).toEqual([])
  })
  test('unknown source fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].refs = [{ source: 'nope', section: '1' }] }).join()).toMatch(/unknown source nope/)
  })
  test('unknown disease fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].disease = 'nope' }).join()).toMatch(/unknown disease/)
  })
  test('calculable regimen without example fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.examples = [] }).join()).toMatch(/has no example/)
  })
  test('unit mismatch fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.regimens[0].unit = 'mcg' }).join()).toMatch(/unit mcg/)
  })
  test('typo field fails (additionalProperties)', () => {
    expect(errorsOf((ds) => { (ds.drugs[0].drug as any).warnigns = [] }).length).toBeGreaterThan(0)
  })
  test('wrong folder fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].path = 'drugs/other/test-drug.json' }).join()).toMatch(/must be at/)
  })
  test('verified without reviewer fails', () => {
    expect(errorsOf((ds) => { ds.drugs[0].drug.review.status = 'verified' }).join()).toMatch(/reviewer/)
  })
})
