<script setup lang="ts">
const { t } = useI18n()
const lt = useLocalText()
const localePath = useLocalePath()
const fmt = useFormatNumber()
useSeoMeta({ title: () => t('diseases.title'), description: () => t('diseases.description') })
const rows = computed(() =>
  diseases
    .map((d) => ({ d, n: catalog.reduce((a, c) => a + c.regimens.filter((r) => r.disease === d.id).length, 0) }))
    .sort((a, b) => lt(a.d.name).localeCompare(lt(b.d.name))),
)
</script>

<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-black">{{ $t('diseases.title') }}</h1>
    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
      <NuxtLink v-for="{ d, n } in rows" :key="d.id" :to="localePath(`/disease/${d.id}`)" class="card hover:border-brand-400">
        <div class="font-bold">{{ lt(d.name) }}</div>
        <div class="ltr text-start text-xs text-slate-500">{{ d.icd10.join(', ') }}</div>
        <p v-if="d.symptoms" class="mt-1 line-clamp-2 text-sm text-slate-600 dark:text-slate-400">{{ d.symptoms.items.map((s) => lt(s)).join('، ') }}</p>
        <p class="mt-1 text-xs text-brand-700 dark:text-brand-300">{{ $t('diseases.count', { n: fmt(n) }) }}</p>
      </NuxtLink>
    </div>
  </div>
</template>
