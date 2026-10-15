import { expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'
import { validateDataSet } from '../../lib/data/validate'
const root = join(__dirname, '../..')
test('repository data is valid', () => expect(validateDataSet(loadDataSet(root), root)).toEqual([]))
