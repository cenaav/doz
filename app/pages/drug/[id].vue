<script setup lang="ts">
const route = useRoute()
const id = route.params.id as string
const { data: drug } = await useAsyncData(`drug-${id}`, () => loadDrug(id))
if (!drug.value) throw createError({ statusCode: 404, statusMessage: 'Drug not found', fatal: true })
const lt = useLocalText()
const { t, locale } = useI18n()
useSeoMeta({
  title: () => `${lt(drug.value!.name)}${locale.value === 'fa' ? ` (${drug.value!.name.en})` : ''} — ${t('drug.doseTitle')}`,
  description: () => t('drug.description', { name: lt(drug.value!.name) }),
})
onMounted(() => {
  const list: string[] = JSON.parse(localStorage.getItem('doz_recent') ?? '[]')
  localStorage.setItem('doz_recent', JSON.stringify([id, ...list.filter((x) => x !== id)].slice(0, 8)))
})
</script>
<template>
  <!-- Fixed order on every drug page: header, then calculator beside safety, then references beside similar drugs. -->
  <div v-if="drug" class="space-y-4">
    <DrugHeader :drug="drug" />
    <div class="grid items-start gap-4 lg:grid-cols-2">
      <DoseCalculator :drug="drug" />
      <DrugSafety :drug="drug" />
    </div>
    <div class="grid gap-4 lg:grid-cols-2">
      <ReferenceStatus :drug="drug" class="h-full" />
      <SimilarDrugs :drug="drug" class="h-full" />
    </div>
  </div>
</template>
