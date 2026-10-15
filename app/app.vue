<script setup lang="ts">
const head = useLocaleHead()
const { t } = useI18n()
// Site-wide link-preview tags; each page sets its own title and description with usePageMeta.
const ogImage = 'https://doz.amonproject.com/og-image.jpg'
useSeoMeta({
  ogSiteName: 'Doz',
  ogType: 'website',
  ogImage,
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogImageType: 'image/jpeg',
  ogImageAlt: () => t('home.tagline'),
  twitterCard: 'summary_large_image',
  twitterImage: ogImage,
  twitterImageAlt: () => t('home.tagline'),
  ogTitle: () => t('home.title') + ' | Doz',
  ogDescription: () => t('home.description'),
  twitterTitle: () => t('home.title') + ' | Doz',
  twitterDescription: () => t('home.description'),
})
useHead(() => ({
  htmlAttrs: head.value.htmlAttrs,
  link: head.value.link,
  meta: head.value.meta,
  titleTemplate: (t?: string) => (t ? `${t} | Doz` : 'Doz'),
}))
</script>

<template>
  <NuxtPwaManifest />
  <NuxtPwaAssets />
  <NuxtLayout><NuxtPage /></NuxtLayout>
</template>
