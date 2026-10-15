<script setup lang="ts">
const mode = useColorMode()
const order = ['system', 'light', 'dark'] as const
const icon = { system: '🖥️', light: '☀️', dark: '🌙' }
function next() { mode.preference = order[(order.indexOf(mode.preference as any) + 1) % order.length] }
</script>
<template>
  <ClientOnly>
    <button class="btn-ghost" :aria-label="$t('settings.theme')" :title="$t(`settings.themes.${mode.preference}`)" @click="next">
      {{ icon[mode.preference as keyof typeof icon] }}
    </button>
    <template #fallback><span class="btn-ghost">🖥️</span></template>
  </ClientOnly>
</template>
