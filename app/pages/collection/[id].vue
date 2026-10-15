<script setup lang="ts">
const route = useRoute()
const collection = getCollection(route.params.id as string)
if (!collection) throw createError({ statusCode: 404, statusMessage: 'Collection not found', fatal: true })
const lt = useLocalText()
const ids = new Set(collection.drugs)
const drugs = catalog.filter((d) => ids.has(d.id))
usePageMeta(() => lt(collection.name), () => lt(collection.description ?? collection.name))
</script>
<template>
  <div class="space-y-4">
    <h1 class="text-xl font-bold">{{ collection!.icon }} {{ lt(collection!.name) }}</h1>
    <p v-if="collection!.description" class="text-sm text-slate-500">{{ lt(collection!.description) }}</p>
    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
      <DrugListItem v-for="d in drugs" :key="d.id" :drug="d" />
    </div>
  </div>
</template>
