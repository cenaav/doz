import { loadDataSet } from '../lib/data/load-fs'
import { validateDataSet } from '../lib/data/validate'

const root = process.cwd()
const errors = validateDataSet(loadDataSet(root), root)
if (errors.length) {
  console.error(`✗ ${errors.length} data error(s):\n` + errors.map((e) => `  - ${e}`).join('\n'))
  process.exit(1)
}
console.log('✓ data valid')
