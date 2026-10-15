import { describe, expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'

// The engine matches a weight band as min < weight ≤ max, so bands must be contiguous
// (each min equals the previous max) and the first band must start below the regimen's minimum weight.
const ds = loadDataSet(join(__dirname, '../..'))

describe('weight bands leave no weight without a dose', () => {
  for (const { drug } of ds.drugs) {
    for (const reg of drug.regimens) {
      if (reg.type !== 'weightBand') continue
      test(`${drug.id}/${reg.id}`, () => {
        const bands = [...reg.dose.weightBands!].sort((a, b) => a.minWeightKg - b.minWeightKg)
        for (let i = 1; i < bands.length; i++) expect(bands[i].minWeightKg, `band ${i} start`).toBe(bands[i - 1].maxWeightKg)
        const popMin = reg.population.minWeightKg
        if (popMin != null) expect(bands[0].minWeightKg, 'first band start').toBeLessThan(popMin)
      })
    }
  }
})
