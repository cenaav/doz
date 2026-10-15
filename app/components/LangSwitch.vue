<script setup lang="ts">
const { locale } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const other = computed(() => (locale.value === 'fa' ? 'en' : 'fa'))
</script>
<template>
  <NuxtLink :to="switchLocalePath(other)" class="btn-ghost font-bold" :aria-label="$t('settings.language')">
    {{ other === 'fa' ? 'فا' : 'EN' }}
  </NuxtLink>
</template>
