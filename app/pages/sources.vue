<script setup lang="ts">
const { t } = useI18n()
useSeoMeta({ title: () => t('sources.title'), description: () => t('sources.description') })
const types = ['fda-label', 'ema-smpc', 'guideline', 'licensed-reference', 'ifda-leaflet', 'textbook'] as const
</script>
<template>
  <div class="mx-auto max-w-4xl space-y-4">
    <h1 class="text-2xl font-black">{{ $t('sources.title') }}</h1>
    <p class="text-sm leading-7">{{ $t('sources.policy') }}</p>
    <section v-for="type in types" :key="type" class="card">
      <h2 class="mb-2 font-bold">{{ $t(`sourceTypes.${type}`) }}</h2>
      <ul v-if="sources.some((s) => s.type === type)" class="space-y-2 text-sm">
        <li v-for="s in sources.filter((x) => x.type === type)" :key="s.id" class="ltr text-start">
          <b>{{ s.short }}</b> — {{ s.title }}<span v-if="s.citation">. {{ s.citation }}</span><span v-if="s.edition"> ({{ s.edition }})</span>
          <a v-if="s.url" :href="s.url" target="_blank" rel="noopener noreferrer" class="ms-1 text-brand-600 underline">↗</a>
          <span class="ms-1 text-xs text-slate-500">[{{ $t(`refs.licenses.${s.license}`) }}]</span>
        </li>
      </ul>
      <p v-else class="text-sm text-slate-500">{{ $t('sources.noneOfType') }}</p>
    </section>
  </div>
</template>
