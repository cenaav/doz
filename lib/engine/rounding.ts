export const r2 = (x: number) => Math.round(x * 100) / 100
const snap = (x: number, step: number) => r2(Math.round(Number((x / step).toFixed(6))) * step)
export function roundMl(ml: number): number {
  return snap(ml, ml < 1 ? 0.05 : ml <= 10 ? 0.1 : 0.5)
}
export function roundTablets(n: number, scored: boolean): number {
  return scored ? snap(n, 0.5) : Math.round(n)
}
