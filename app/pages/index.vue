<script setup lang="ts">
import type { CatalogEntry } from '../../lib/types'
const { t } = useI18n()
const lt = useLocalText()
const localePath = useLocalePath()
const fmt = useFormatNumber()
useSeoMeta({ title: () => t('home.title'), description: () => t('home.description') })
const cats = categories.map((c) => ({ ...c, count: categoryCounts[c.id] ?? 0 })).filter((c) => c.count)
const recentDrugs = shallowRef<CatalogEntry[]>([])
// The catalog is only fetched when there are recent drugs to name, after the page has rendered.
onMounted(async () => {
  const ids: string[] = JSON.parse(localStorage.getItem('doz_recent') ?? '[]')
  if (!ids.length) return
  const { catalog } = await import('../utils/catalog')
  recentDrugs.value = ids.map((id) => catalog.find((d) => d.id === id)).filter((d): d is CatalogEntry => !!d)
})
</script>
<template>
  <div class="space-y-6">
    <section class="mx-auto max-w-3xl pt-4 text-center sm:pt-10">
      <h1 class="text-4xl font-black text-brand-600 sm:text-5xl dark:text-brand-400">Doz</h1>
      <p class="mt-2 text-slate-600 dark:text-slate-400">{{ $t('home.tagline') }}</p>
      <SearchBox class="mt-6" />
      <SafetyBanner class="mt-3" />
      <NuxtLink :to="localePath('/calculator')" class="mt-4 flex items-center justify-center gap-3 rounded-2xl bg-brand-600 px-4 py-4 text-white shadow hover:bg-brand-700">
        <span class="text-3xl">🧮</span>
        <span class="text-start"><b class="block text-lg">{{ $t('quick.cta') }}</b><span class="text-sm opacity-90">{{ $t('quick.ctaSub') }}</span></span>
      </NuxtLink>
    </section>
    <section v-if="recentDrugs.length" class="mx-auto max-w-3xl">
      <h2 class="mb-2 text-sm font-bold text-slate-500">{{ $t('home.recent') }}</h2>
      <div class="flex flex-wrap gap-2">
        <NuxtLink v-for="d in recentDrugs" :key="d.id" :to="localePath(`/drug/${d.id}`)" class="chip text-sm">{{ lt(d.name) }}</NuxtLink>
      </div>
    </section>
    <section>
      <h2 class="mb-3 text-base font-semibold">{{ $t('home.collections') }}</h2>
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <NuxtLink v-for="c in collections" :key="c.id" :to="localePath(`/collection/${c.id}`)" class="card hover:border-brand-400">
          <div class="text-2xl">{{ c.icon }}</div>
          <div class="mt-1 font-semibold">{{ lt(c.name) }}</div>
          <div class="text-sm text-slate-500">{{ $t('home.drugCount', { n: fmt(c.drugs.length) }) }}</div>
        </NuxtLink>
      </div>
    </section>
    <section>
      <h2 class="mb-1 text-base font-semibold">{{ $t('home.categories') }}</h2>
      <p class="mb-3 text-xs text-slate-500">{{ $t('category.atcNote') }}</p>
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-6">
        <NuxtLink v-for="c in cats" :key="c.id" :to="localePath(`/category/${c.id}`)" class="card hover:border-brand-400">
          <div class="text-2xl">{{ c.icon }}</div>
          <div class="mt-1 font-semibold">{{ lt(c.name) }}</div>
          <div class="text-sm text-slate-500">{{ $t('home.drugCount', { n: fmt(c.count) }) }}</div>
        </NuxtLink>
      </div>
    </section>
  </div>
</template>
