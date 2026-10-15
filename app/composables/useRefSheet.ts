import type { Ref as DataRef } from '../../lib/types'
export function useRefSheet() {
  const current = useState<DataRef | null>('ref-sheet', () => null)
  return { current, open: (r: DataRef) => (current.value = r), close: () => (current.value = null) }
}
