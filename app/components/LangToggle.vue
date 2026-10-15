<script setup lang="ts">
const { locale } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const other = computed(() => (locale.value === 'fa' ? 'en' : 'fa'))
</script>
<template>
  <NuxtLink :to="switchLocalePath(other)" class="grid size-8 place-items-center rounded-full border border-slate-300 text-[11px] font-semibold text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
    :aria-label="$t('settings.language')" :title="$t('settings.language')">{{ other === 'fa' ? 'فا' : 'EN' }}</NuxtLink>
</template>
