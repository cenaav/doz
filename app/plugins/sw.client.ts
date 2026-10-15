// Registers the PWA service worker for offline use. The @vite-pwa/nuxt auto-registration
// did not register on the statically generated pages, so we do it here.
export default defineNuxtPlugin(() => {
  if (import.meta.dev || !('serviceWorker' in navigator)) return
  const base = useRuntimeConfig().app.baseURL
  // When a new deploy's service worker takes over, reload once so the user never keeps seeing an old cached page.
  const hadController = !!navigator.serviceWorker.controller
  let reloaded = false
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!hadController || reloaded) return
    reloaded = true
    location.reload()
  })
  const register = () => navigator.serviceWorker.register(`${base}sw.js`, { scope: base }).then((r) => r.update()).catch(() => {})
  // Wait until the page is loaded and idle so precaching never competes with the first render.
  const idle = () => ('requestIdleCallback' in window ? requestIdleCallback(register, { timeout: 10000 }) : setTimeout(register, 5000))
  if (document.readyState === 'complete') idle()
  else window.addEventListener('load', idle, { once: true })
})
