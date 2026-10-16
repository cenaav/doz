import { describe, expect, test } from 'vitest'
import { pickDrugs } from '../../lib/search/pick'
import type { CatalogEntry } from '../../lib/types'

const entry = (id: string, en: string, fa: string, extra: Partial<CatalogEntry> = {}): CatalogEntry =>
  ({ id, category: 'c', name: { en, fa }, brands: [], synonyms: [], reviewStatus: 'unverified', regimens: [], ...extra }) as CatalogEntry

const list = [
  entry('amoxicillin', 'Amoxicillin', 'آموکسی‌سیلین', { brands: ['Amoxil'] }),
  entry('amoxicillin-clavulanate', 'Amoxicillin + clavulanate', 'کوآموکسی‌کلاو', { brands: ['Augmentin'] }),
  entry('acetaminophen', 'Acetaminophen', 'استامینوفن', { synonyms: ['paracetamol', 'تب بر'] }),
  entry('cefixime', 'Cefixime', 'سفیکسیم'),
]
const ids = (q: string) => pickDrugs(list, q).map((d) => d.id)

describe('pickDrugs', () => {
  test('empty query returns everything', () => expect(ids('')).toHaveLength(4))
  test('English prefix ranks the name match first', () => expect(ids('amox')[0]).toBe('amoxicillin'))
  test('part of a name matches', () => expect(ids('clav')).toEqual(['amoxicillin-clavulanate']))
  test('Persian partial name', () => expect(ids('سفیک')).toEqual(['cefixime']))
  test('Persian without the half-space', () => expect(ids('آموکسی سیلین')).toContain('amoxicillin'))
  test('brand name', () => expect(ids('augmentin')).toEqual(['amoxicillin-clavulanate']))
  test('synonym', () => expect(ids('paracetamol')).toEqual(['acetaminophen']))
  test('Arabic yeh/kaf typed', () => expect(ids('سفيكسيم')).toEqual(['cefixime']))
  test('one-letter typo still finds the drug', () => expect(ids('cefixine')).toEqual(['cefixime']))
  test('typo is not used when exact matches exist', () => expect(ids('amoxicillin')).not.toContain('cefixime'))
  test('nonsense finds nothing', () => expect(ids('zzzzqq')).toEqual([]))
})
