<script setup lang="ts">
const route = useRoute()
const category = getCategory(route.params.id as string)
if (!category) throw createError({ statusCode: 404, statusMessage: 'Category not found', fatal: true })
const lt = useLocalText()
const { t } = useI18n()
const drugs = catalog.filter((d) => d.category === category.id)
useSeoMeta({ title: () => lt(category.name), description: () => t('category.description', { name: lt(category.name) }) })
</script>
<template>
  <div class="space-y-4">
    <h1 class="text-xl font-bold">{{ category!.icon }} {{ lt(category!.name) }}</h1>
    <p v-if="!drugs.length" class="text-slate-500">{{ $t('category.empty') }}</p>
    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
      <DrugListItem v-for="d in drugs" :key="d.id" :drug="d" />
    </div>
  </div>
</template>
