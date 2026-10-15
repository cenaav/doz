<script setup lang="ts">
const { t } = useI18n()
const lt = useLocalText()
const localePath = useLocalePath()
const fmt = useFormatNumber()
useSeoMeta({ title: () => t('home.title'), description: () => t('home.description') })
const cats = categories.map((c) => ({ ...c, count: catalog.filter((d) => d.category === c.id).length }))
const recent = ref<string[]>([])
onMounted(() => { recent.value = JSON.parse(localStorage.getItem('doz_recent') ?? '[]') })
const recentDrugs = computed(() => recent.value.map((id) => catalog.find((d) => d.id === id)).filter((d) => !!d))
</script>
<template>
  <div class="space-y-6">
    <section class="mx-auto max-w-3xl pt-4 text-center sm:pt-10">
      <h1 class="text-4xl font-black text-brand-600 sm:text-5xl dark:text-brand-400">Doz</h1>
      <p class="mt-2 text-slate-600 dark:text-slate-400">{{ $t('home.tagline') }}</p>
      <SearchBox class="mt-6" />
    </section>
    <section v-if="recentDrugs.length" class="mx-auto max-w-3xl">
      <h2 class="mb-2 text-sm font-bold text-slate-500">{{ $t('home.recent') }}</h2>
      <div class="flex flex-wrap gap-2">
        <NuxtLink v-for="d in recentDrugs" :key="d!.id" :to="localePath(`/drug/${d!.id}`)" class="chip text-sm">{{ lt(d!.name) }}</NuxtLink>
      </div>
    </section>
    <section>
      <h2 class="mb-3 text-lg font-bold">{{ $t('home.categories') }}</h2>
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-6">
        <NuxtLink v-for="c in cats" :key="c.id" :to="localePath(`/category/${c.id}`)" class="card hover:border-brand-400">
          <div class="text-2xl">{{ c.icon }}</div>
          <div class="mt-1 font-bold">{{ lt(c.name) }}</div>
          <div class="text-sm text-slate-500">{{ $t('home.drugCount', { n: fmt(c.count) }) }}</div>
        </NuxtLink>
      </div>
    </section>
  </div>
</template>
