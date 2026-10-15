<script setup lang="ts">
const { locale } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const other = computed(() => (locale.value === 'fa' ? 'en' : 'fa'))
</script>
<template>
  <NuxtLink :to="switchLocalePath(other)" class="icon-btn"
    :aria-label="$t('settings.language')" :title="$t('settings.language')"><span :class="other === 'fa' ? 'block text-xs' : 'block translate-y-px'">{{ other === 'fa' ? 'فا' : 'EN' }}</span></NuxtLink>
</template>
