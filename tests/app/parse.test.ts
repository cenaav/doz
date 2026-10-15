import { expect, test } from 'vitest'
import { parseNumber } from '../../app/utils/parse'

test.each([
  ['12', 12],
  ['۱۲٫۵', 12.5],
  ['١٢,٥', 12.5],
  ['3.5', 3.5],
  [' 7 ', 7],
  ['', null],
  ['abc', null],
  ['1.2.3', null],
])('%s → %s', (s, n) => expect(parseNumber(s)).toBe(n))
