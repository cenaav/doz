<script setup lang="ts">
import type { Drug, Population } from '../../lib/types'
const props = defineProps<{ drug: Drug }>()
const lt = useLocalText()
const POPS: Population[] = ['pregnancy', 'lactation', 'pediatric', 'geriatric', 'reproductive']
const ICON: Record<Population, string> = { pregnancy: '🤰', lactation: '🤱', pediatric: '👶', geriatric: '👴', reproductive: '⚥' }
</script>
<template>
  <section class="card space-y-3">
    <h2 class="card-title !mb-0">👥 {{ $t('pop.title') }}</h2>
    <ul class="space-y-3 text-sm">
      <li v-for="p in POPS" :id="`pop-${p}`" :key="p" class="scroll-mt-20">
        <div class="flex flex-wrap items-center gap-2">
          <span class="font-semibold">{{ ICON[p] }} {{ $t(`pop.${p}`) }}</span>
          <PopLevelBadge :level="drug.populations?.[p]?.level ?? 'no-data'" />
        </div>
        <template v-if="drug.populations?.[p]">
          <p class="mt-1">{{ lt(drug.populations[p]!.text) }} <RefChips :refs="drug.populations[p]!.refs" /></p>
          <blockquote v-if="drug.populations[p]!.quote" dir="auto" class="mt-1 border-s-2 border-slate-300 ps-2 text-start text-xs italic text-slate-500 dark:border-slate-600">“{{ drug.populations[p]!.quote }}”</blockquote>
        </template>
        <p v-else class="mt-1 text-slate-500">{{ $t('pop.none') }}</p>
      </li>
    </ul>
  </section>
</template>
