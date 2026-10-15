import { describe, expect, test } from 'vitest'
import { join } from 'node:path'
import { loadDataSet } from '../../lib/data/load-fs'
import { buildCatalog } from '../../lib/data/catalog'
import { createSearch } from '../../lib/search'

const ds = loadDataSet(join(__dirname, '../..'))
const s = createSearch(buildCatalog(ds.drugs.map((d) => d.drug), ds.sources), ds.diseases, ds.categories)

describe('search over the real data set', () => {
  test('English drug name', () => expect(s('cephalexin').drugs[0]?.id).toBe('cephalexin'))
  test('Persian partial drug name', () => expect(s('سفال').drugs.map((d) => d.id)).toContain('cephalexin'))
  test('Persian symptom → disease', () => expect(s('گوش درد').diseases.map((d) => d.id)).toContain('acute-otitis-media'))
  test('English symptom → disease', () => expect(s('ear pain').diseases.map((d) => d.id)).toContain('acute-otitis-media'))
  test('symptom → drugs', () => expect(s('wheezing').drugs.map((d) => d.id)).toContain('theophylline'))
  test('bloody diarrhea (Persian)', () => expect(s('اسهال خونی').diseases.map((d) => d.id)).toContain('shigellosis'))
})
