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
          if (typeof v === 'number') expect((r as any)[k], k).toBeCloseTo(v, 2)
          else expect((r as any)[k], k).toBe(v)
        }
      })
    })
  })
}
