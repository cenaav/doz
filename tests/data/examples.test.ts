import { describe, expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'
import { calculate } from '../../lib/engine'
import { ageDaysFrom } from '../../lib/engine/age'

const ds = loadDataSet(join(__dirname, '../..'))
for (const { drug } of ds.drugs.filter((d) => d.drug.examples.length)) {
  describe(drug.id, () => {
    drug.examples.forEach((ex, i) => {
      test(`example ${i + 1}: ${ex.regimen} / ${ex.formulation}`, () => {
        const r = calculate(drug, ex.regimen, ex.formulation, { ...ex.input, ageDays: ageDaysFrom(ex.input) })
        for (const [k, v] of Object.entries(ex.expect)) {
          const actual = k.startsWith('upper') ? (r.upper as any)?.[k[5].toLowerCase() + k.slice(6)] : (r as any)[k]
          if (typeof v === 'number') expect(actual, k).toBeCloseTo(v, 2)
          else expect(actual, k).toBe(v)
        }
      })
    })
  })
}
