<script setup lang="ts">
const head = useLocaleHead()
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
