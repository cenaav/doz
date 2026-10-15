import { existsSync, readFileSync } from 'node:fs'
import tailwindcss from '@tailwindcss/vite'

const base = process.env.NUXT_APP_BASE_URL || '/'

// Precache only the hashed app assets and icons. HTML and payloads are cached at runtime (network first),
// so after a deploy the browser never shows an old page that points at deleted files.
type PrecacheEntry = { url: string; revision: string | null; size: number }
const precacheAssets = async (entries: PrecacheEntry[]) => ({
  manifest: entries.filter((e) => !e.url.endsWith('.html') && !e.url.endsWith('_payload.json')),
  warnings: [],
})
const routes: string[] = existsSync('app/generated/routes.json')
  ? JSON.parse(readFileSync('app/generated/routes.json', 'utf8'))
  : []

export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  ssr: true,
  modules: ['@nuxtjs/i18n', '@nuxtjs/color-mode', '@vite-pwa/nuxt'],
  css: ['~/assets/css/main.css'],
  vite: { plugins: [tailwindcss()] },
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/svg+xml', href: `${base}icon.svg` }],
      meta: [{ name: 'theme-color', content: '#0f766e' }],
    },
  },
  colorMode: { classSuffix: '', preference: 'system', fallback: 'light', storageKey: 'doz_theme' },
  i18n: {
    strategy: 'prefix_except_default',
    defaultLocale: 'fa',
    baseUrl: 'https://doz.amonproject.com',
    locales: [
      { code: 'fa', language: 'fa-IR', dir: 'rtl', name: 'فارسی', file: 'fa.json' },
      { code: 'en', language: 'en-US', dir: 'ltr', name: 'English', file: 'en.json' },
    ],
    detectBrowserLanguage: false,
  },
  pwa: {
    registerType: 'autoUpdate',
    injectRegister: false,
    client: { registerPlugin: false },
    pwaAssets: { config: true },
    manifest: {
      name: 'Doz',
      short_name: 'Doz',
      description: 'Source-referenced drug dose calculator',
      lang: 'fa',
      dir: 'rtl',
      theme_color: '#0f766e',
      background_color: '#ffffff',
      start_url: base,
      scope: base,
      display: 'standalone',
    },
    workbox: {
      globPatterns: ['_nuxt/**/*.{js,css,woff2}', '*.{png,svg,ico}'],
      runtimeCaching: [
        { urlPattern: ({ request }) => request.mode === 'navigate', handler: 'NetworkFirst', options: { cacheName: 'doz-pages', networkTimeoutSeconds: 4 } },
        { urlPattern: /_payload\.json/, handler: 'NetworkFirst', options: { cacheName: 'doz-payloads', networkTimeoutSeconds: 4 } },
        { urlPattern: /\/_i18n\//, handler: 'NetworkFirst', options: { cacheName: 'doz-i18n', networkTimeoutSeconds: 4 } },
      ],
      navigateFallback: undefined,
      manifestTransforms: [precacheAssets],
      clientsClaim: true,
      skipWaiting: true,
    },
  },
  nitro: { prerender: { crawlLinks: true, failOnError: true, routes: ['/', '/en', ...routes] } },
})
