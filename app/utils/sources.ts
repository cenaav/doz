import type { Source } from '../../lib/types'
import sourcesJson from '../../data/sources.json'

export const sources = sourcesJson as Source[]
export const getSource = (id: string) => sources.find((s) => s.id === id)
