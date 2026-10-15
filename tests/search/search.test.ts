import { describe, expect, test } from 'vitest'
import { normalize } from '../../lib/search/normalize'
import { createSearch } from '../../lib/search'
import type { CatalogEntry } from '../../lib/types'

const entry = (id: string, en: string, fa: string, extra: Partial<CatalogEntry> = {}): CatalogEntry =>
  ({ id, category: 'c', name: { en, fa }, brands: [], synonyms: [], reviewStatus: 'unverified', regimens: [], ...extra })

describe('normalize', () => {
  test('Arabic letters → Persian', () => expect(normalize('كلي')).toBe(normalize('کلی')))
  test('ZWNJ → space', () => expect(normalize('آموکسی‌سیلین')).toBe('اموکسی سیلین'))
  test('digits', () => expect(normalize('۱۲٣')).toBe('123'))
  test('case and spaces', () => expect(normalize('  AmoX  ')).toBe('amox'))
})

describe('createSearch', () => {
  const s = createSearch(
    [entry('amoxicillin', 'Amoxicillin', 'آموکسی‌سیلین', { brands: ['Amoxil'] }), entry('cetirizine', 'Cetirizine', 'ستیریزین')],
    [{ id: 'acute-otitis-media', name: { en: 'Acute otitis media', fa: 'اوتیت مدیای حاد' }, synonyms: ['AOM'], icd10: ['H66.9'], specialty: 'peds' }],
    [{ id: 'antibiotics', name: { en: 'Antibiotics', fa: 'آنتی‌بیوتیک‌ها' }, icon: '💊', order: 1 }],
  )
  test('English name', () => expect(s('amox').drugs[0].id).toBe('amoxicillin'))
  test('typo', () => expect(s('amoxicilin').drugs[0].id).toBe('amoxicillin'))
  test('Persian with Arabic ya and no ZWNJ', () => expect(s('اموکسي سيلين').drugs[0].id).toBe('amoxicillin'))
  test('brand', () => expect(s('amoxil').drugs[0].id).toBe('amoxicillin'))
  test('disease synonym', () => expect(s('AOM').diseases[0].id).toBe('acute-otitis-media'))
  test('ICD-10', () => expect(s('H66').diseases[0].id).toBe('acute-otitis-media'))
  test('category', () => expect(s('آنتی بیوتیک').categories[0].id).toBe('antibiotics'))
  test('empty query', () => expect(s('  ')).toEqual({ drugs: [], diseases: [], categories: [] }))
})
