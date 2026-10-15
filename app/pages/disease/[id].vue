<script setup lang="ts">
const route = useRoute()
const disease = getDisease(route.params.id as string)
if (!disease) throw createError({ statusCode: 404, statusMessage: 'Disease not found', fatal: true })
const lt = useLocalText()
const localePath = useLocalePath()
const { t } = useI18n()
const rows = catalog.flatMap((d) => d.regimens.filter((r) => r.disease === disease.id).map((r) => ({ drug: d, regimen: r })))
useSeoMeta({ title: () => lt(disease.name), description: () => t('disease.description', { name: lt(disease.name) }) })
</script>
<template>
  <div class="space-y-4">
    <h1 class="text-xl font-bold">{{ lt(disease!.name) }}</h1>
    <p class="ltr text-start text-sm text-slate-500">{{ disease!.name.en }} · ICD-10: {{ disease!.icd10.join(', ') }}</p>
    <section v-if="disease!.description" class="card">
      <p class="leading-7">{{ lt(disease!.description.text) }} <RefChips :refs="disease!.description.refs" /></p>
    </section>
    <section v-if="disease!.symptoms" class="card">
      <h2 class="mb-2 font-semibold">{{ $t('diseases.symptoms') }}</h2>
      <ul class="grid gap-1 text-sm sm:grid-cols-2">
        <li v-for="(s, i) in disease!.symptoms.items" :key="i">• {{ lt(s) }}</li>
      </ul>
      <p class="mt-2 text-xs"><RefChips :refs="disease!.symptoms.refs" /></p>
    </section>
    <h2 class="font-semibold">{{ $t('diseases.drugs') }}</h2>
    <p v-if="!rows.length" class="text-slate-500">{{ $t('disease.empty') }}</p>
    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      <NuxtLink v-for="row in rows" :key="row.drug.id + row.regimen.id" :to="localePath({ path: `/drug/${row.drug.id}`, query: { regimen: row.regimen.id } })" class="card hover:border-brand-400">
        <div class="flex items-center justify-between gap-2"><b>{{ lt(row.drug.name) }}</b><ReviewBadge :status="row.drug.reviewStatus" small /></div>
        <p class="text-sm text-slate-600 dark:text-slate-400">{{ lt(row.regimen.label) }}</p>
      </NuxtLink>
    </div>
  </div>
</template>
