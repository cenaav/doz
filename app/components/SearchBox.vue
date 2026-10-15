<script setup lang="ts">
defineProps<{ compact?: boolean }>()
const q = ref('')
const focused = ref(false)
const { search } = useSearch()
const lt = useLocalText()
const localePath = useLocalePath()
const results = computed(() => search(q.value))
const empty = computed(() => !results.value.drugs.length && !results.value.diseases.length && !results.value.categories.length)
function blur() { setTimeout(() => (focused.value = false), 150) }
</script>
<template>
  <div class="relative" role="search">
    <input v-model="q" type="search" class="input" :class="compact ? 'py-1.5 text-sm' : 'py-3 text-lg'"
      :placeholder="$t('search.placeholder')" :aria-label="$t('search.placeholder')" autocomplete="off"
      @focus="focused = true" @blur="blur" />
    <div v-if="focused && q.trim()" class="card absolute inset-x-0 top-full z-40 mt-1 max-h-[70dvh] space-y-3 overflow-auto p-2 text-start">
      <p v-if="empty" class="p-2 text-sm text-slate-500">{{ $t('search.noResults') }}</p>
      <section v-if="results.drugs.length">
        <h3 class="px-2 text-xs font-bold uppercase text-slate-500">{{ $t('search.drugs') }}</h3>
        <NuxtLink v-for="d in results.drugs" :key="d.id" :to="localePath(`/drug/${d.id}`)" class="flex items-center justify-between gap-2 rounded-lg px-2 py-2 hover:bg-slate-100 dark:hover:bg-slate-800">
          <span><b>{{ lt(d.name) }}</b> <span class="ltr text-sm text-slate-500">{{ d.name.en }}</span></span>
          <ReviewBadge :status="d.reviewStatus" small />
        </NuxtLink>
      </section>
      <section v-if="results.diseases.length">
        <h3 class="px-2 text-xs font-bold uppercase text-slate-500">{{ $t('search.diseases') }}</h3>
        <NuxtLink v-for="d in results.diseases" :key="d.id" :to="localePath(`/disease/${d.id}`)" class="block rounded-lg px-2 py-2 hover:bg-slate-100 dark:hover:bg-slate-800">
          {{ lt(d.name) }} <span class="ltr text-xs text-slate-500">{{ d.icd10.join(', ') }}</span>
        </NuxtLink>
      </section>
      <section v-if="results.categories.length">
        <h3 class="px-2 text-xs font-bold uppercase text-slate-500">{{ $t('search.categories') }}</h3>
        <NuxtLink v-for="c in results.categories" :key="c.id" :to="localePath(`/category/${c.id}`)" class="block rounded-lg px-2 py-2 hover:bg-slate-100 dark:hover:bg-slate-800">
          {{ c.icon }} {{ lt(c.name) }}
        </NuxtLink>
      </section>
    </div>
  </div>
</template>
