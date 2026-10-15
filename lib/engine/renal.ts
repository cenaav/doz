export const schwartzEgfr = (heightCm: number, scrMgDl: number) => (0.413 * heightCm) / scrMgDl
export const mostellerBsa = (heightCm: number, weightKg: number) => Math.sqrt((heightCm * weightKg) / 3600)
