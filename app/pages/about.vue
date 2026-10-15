<script setup lang="ts">
const { t } = useI18n()
useSeoMeta({ title: () => t('about.title'), description: () => t('about.description') })
const sections = ['what', 'refs', 'review', 'privacy', 'contrib'] as const
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-4">
    <h1 class="text-xl font-bold">{{ $t('about.title') }}</h1>
    <section class="card space-y-2 border-red-300 dark:border-red-800">
      <h2 class="text-base font-semibold text-red-700 dark:text-red-400">⚠️ {{ $t('disclaimer.title') }}</h2>
      <p v-for="i in 4" :key="i" class="leading-7">{{ $t(`disclaimer.p${i}`) }}</p>
    </section>
    <section class="card space-y-2">
      <h2 class="text-base font-semibold">{{ $t('about.howTitle') }}</h2>
      <ol class="list-decimal space-y-1 ps-5 leading-7">
        <li v-for="i in 5" :key="i">{{ $t(`about.how${i}`) }}</li>
      </ol>
    </section>
    <section v-for="s in sections" :key="s" class="card space-y-2">
      <h2 class="text-base font-semibold">{{ $t(`about.${s}Title`) }}</h2>
      <p class="leading-7">{{ $t(`about.${s}Body`) }}</p>
    </section>
  </div>
</template>
