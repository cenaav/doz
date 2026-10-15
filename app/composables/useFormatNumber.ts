/** Formats numbers in the active locale's digits (Persian digits in fa). */
export function useFormatNumber() {
  const { locale } = useI18n()
  return (n?: number | null) =>
    n == null ? '—' : new Intl.NumberFormat(locale.value === 'fa' ? 'fa-IR' : 'en-US', { maximumFractionDigits: 2 }).format(n)
}
