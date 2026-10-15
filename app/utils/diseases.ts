import type { Disease } from '../../lib/types'
import diseasesJson from '../../data/diseases.json'

export const diseases = diseasesJson as Disease[]
export const getDisease = (id: string) => diseases.find((d) => d.id === id)
