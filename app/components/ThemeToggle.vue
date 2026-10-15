<script setup lang="ts">
// Follows the system theme until the user taps; then switches between light and dark.
const mode = useColorMode()
const isDark = computed(() => mode.value === 'dark')
const toggle = () => (mode.preference = isDark.value ? 'light' : 'dark')
</script>
<template>
  <ClientOnly>
    <button type="button" class="grid size-8 place-items-center rounded-full text-base hover:bg-slate-100 dark:hover:bg-slate-800"
      :aria-label="$t('settings.theme')" :title="$t(`settings.themes.${isDark ? 'light' : 'dark'}`)" @click="toggle">{{ isDark ? '☀️' : '🌙' }}</button>
    <template #fallback><span class="size-8" /></template>
  </ClientOnly>
</template>
