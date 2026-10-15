import { describe, expect, test } from 'vitest'
import { createSearch } from '../../lib/search'
import type { CatalogEntry, Category, Disease } from '../../lib/types'

const entry = (id: string, en: string, fa: string, extra: Partial<CatalogEntry> = {}): CatalogEntry =>
  ({ id, category: 'c', name: { en, fa }, brands: [], synonyms: [], reviewStatus: 'unverified', regimens: [], ...extra })

const diseases: Disease[] = [
  { id: 'acute-otitis-media', name: { en: 'Acute otitis media', fa: 'اوتیت مدیای حاد' }, synonyms: ['AOM', 'عفونت گوش میانی'], icd10: ['H66.90'], specialty: 'peds',
    symptoms: { items: [{ en: 'Ear pain', fa: 'گوش درد' }, { en: 'Fever', fa: 'تب' }, { en: 'Irritability in infants', fa: 'بی‌قراری در شیرخوار' }], refs: [{ source: 's', section: 'Symptoms' }] } },
  { id: 'allergic-rhinitis', name: { en: 'Allergic rhinitis', fa: 'رینیت آلرژیک' }, synonyms: ['hay fever'], icd10: ['J30.9'], specialty: 'allergy',
    symptoms: { items: [{ en: 'Sneezing', fa: 'عطسه' }, { en: 'Runny nose', fa: 'آبریزش بینی' }, { en: 'Itchy eyes', fa: 'خارش چشم' }], refs: [{ source: 's', section: 'Symptoms' }] } },
]
const categories: Category[] = [{ id: 'antibiotics', name: { en: 'Antibiotics', fa: 'آنتی‌بیوتیک‌ها' }, icon: '💊', order: 1 }]
const catalog = [
  entry('amoxicillin', 'Amoxicillin', 'آموکسی‌سیلین', { brands: ['Amoxil'], class: { en: 'Aminopenicillin', fa: 'آمینوپنی‌سیلین' },
    regimens: [{ id: 'aom', disease: 'acute-otitis-media', label: { en: 'Acute otitis media — high dose', fa: 'اوتیت مدیا — دوز بالا' } }] }),
  entry('cetirizine', 'Cetirizine', 'ستیریزین', { class: { en: 'Second-generation antihistamine', fa: 'آنتی‌هیستامین نسل دوم' },
    regimens: [{ id: 'ar', disease: 'allergic-rhinitis', label: { en: 'Allergic rhinitis', fa: 'رینیت آلرژیک' } }] }),
]
const s = createSearch(catalog, diseases, categories)

describe('full-text search', () => {
  test('symptom finds the disease (Persian)', () => expect(s('گوش درد').diseases[0].id).toBe('acute-otitis-media'))
  test('symptom finds the disease (English, other word order)', () => expect(s('nose runny').diseases[0].id).toBe('allergic-rhinitis'))
  test('symptom also finds drugs that treat that disease', () => expect(s('sneezing').drugs.map((d) => d.id)).toContain('cetirizine'))
  test('partial word (prefix)', () => expect(s('amox').drugs[0].id).toBe('amoxicillin'))
  test('partial Persian word', () => expect(s('آموکس').drugs[0].id).toBe('amoxicillin'))
  test('typo', () => expect(s('cetirizin').drugs[0].id).toBe('cetirizine'))
  test('drug class word', () => expect(s('antihistamine').drugs[0].id).toBe('cetirizine'))
  test('disease name finds its drugs', () => expect(s('otitis').drugs.map((d) => d.id)).toContain('amoxicillin'))
  test('multi-word mixed query', () => expect(s('ear pain fever').diseases[0].id).toBe('acute-otitis-media'))
  test('matched symptom is reported for display', () => expect(s('عطسه').diseases[0].matched).toContain('عطسه'))
  test('ZWNJ / Arabic ya insensitive', () => expect(s('بي قراري').diseases[0].id).toBe('acute-otitis-media'))
  test('empty query', () => expect(s('  ')).toEqual({ drugs: [], diseases: [], categories: [] }))
})
