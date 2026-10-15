<script setup lang="ts">
import type { CatalogEntry } from '../../../lib/types'
const route = useRoute()
const category = getCategory(route.params.id as string)
if (!category) throw createError({ statusCode: 404, statusMessage: 'Category not found', fatal: true })
const lt = useLocalText()
const { t } = useI18n()
const drugs = catalog.filter((d) => d.category === category.id)
// Drugs are listed under their WHO ATC therapeutic subgroup (level 2), e.g. J01 antibacterials.
const groups = computed(() => {
  const map = new Map<string, CatalogEntry[]>()
  for (const d of drugs) {
    const code = d.atc[0]?.slice(0, 3) ?? ''
    map.set(code, [...(map.get(code) ?? []), d])
  }
  return [...map.entries()].sort(([a], [b]) => (a || 'ZZZ').localeCompare(b || 'ZZZ')).map(([code, list]) => ({ code, group: getAtcGroup(code), list }))
})
useSeoMeta({ title: () => lt(category.name), description: () => t('category.description', { name: lt(category.name) }) })
</script>
<template>
  <div class="space-y-5">
    <h1 class="text-xl font-bold">{{ category!.icon }} {{ lt(category!.name) }} <span class="ltr text-sm font-normal text-slate-500">ATC {{ category!.atc }}</span></h1>
    <p class="text-sm text-slate-500">{{ $t('category.atcNote') }}</p>
    <p v-if="!drugs.length" class="text-slate-500">{{ $t('category.empty') }}</p>
    <section v-for="g in groups" :key="g.code" class="space-y-2">
      <h2 class="text-base font-semibold">
        <span v-if="g.code" class="ltr me-1 text-slate-500">{{ g.code }}</span>{{ g.group ? lt(g.group.name) : $t('category.noAtc') }}
      </h2>
      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        <DrugListItem v-for="d in g.list" :key="d.id" :drug="d" />
      </div>
    </section>
  </div>
</template>
