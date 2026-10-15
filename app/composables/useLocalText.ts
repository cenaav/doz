import type { I18nText, Lang } from '../../lib/types'
export function useLocalText() {
  const { locale } = useI18n()
  return (t?: I18nText | null) => {
    if (!t) return ''
    const l = locale.value as Lang
    return t[l] ?? t[l === 'fa' ? 'en' : 'fa'] ?? ''
  }
}
