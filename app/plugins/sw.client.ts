// Registers the PWA service worker for offline use. The @vite-pwa/nuxt auto-registration
// did not register on the statically generated pages, so we do it here.
export default defineNuxtPlugin(() => {
  if (import.meta.dev || !('serviceWorker' in navigator)) return
  const base = useRuntimeConfig().app.baseURL
  const register = () => navigator.serviceWorker.register(`${base}sw.js`, { scope: base }).catch(() => {})
  if (document.readyState === 'complete') register()
  else window.addEventListener('load', register, { once: true })
})
