<script setup lang="ts">
// Follows the system theme until the user taps; then switches between light and dark.
const mode = useColorMode()
const isDark = computed(() => mode.value === 'dark')
const toggle = () => (mode.preference = isDark.value ? 'light' : 'dark')
</script>
<template>
  <ClientOnly>
    <button type="button" class="icon-btn text-base"
      :aria-label="$t('settings.theme')" :title="$t(`settings.themes.${isDark ? 'light' : 'dark'}`)" @click="toggle">{{ isDark ? '☀️' : '🌙' }}</button>
    <template #fallback><span class="icon-btn" /></template>
  </ClientOnly>
</template>
