<script setup lang="ts">
import type { Drug } from '../../lib/types'
import { drugConfidence } from '../../lib/data/refs'
const props = defineProps<{ drug: Drug }>()
const lt = useLocalText()
const { locale } = useI18n()
const localePath = useLocalePath()
const cat = getCategory(props.drug.category)
const markets = [...new Set(props.drug.formulations.flatMap((f) => f.markets))]
const lowConfidence = drugConfidence(props.drug, sources) === 'low'
</script>
<template>
  <section class="card space-y-2">
    <div class="flex flex-wrap items-start justify-between gap-2">
      <div>
        <h1 class="text-xl font-bold">{{ lt(drug.name) }}</h1>
        <p class="text-start text-sm text-slate-500">{{ locale === 'fa' ? drug.name.en : drug.name.fa }}</p>
      </div>
      <ReviewBadge :status="drug.review.status" />
    </div>
    <p class="text-sm">
      <NuxtLink v-if="cat" :to="localePath(`/category/${cat.id}`)" class="chip">{{ cat.icon }} {{ lt(cat.name) }}</NuxtLink>
      <span v-if="drug.class" class="ms-2 text-slate-600 dark:text-slate-400">{{ lt(drug.class) }}</span>
    </p>
    <p class="text-sm"><span class="text-slate-500">{{ $t('markets.label') }}:</span> <MarketBadges :markets="markets" /></p>
    <ConfidenceBanner v-if="lowConfidence" />
    <p v-if="drug.brands.length" class="ltr text-start text-sm text-slate-500">{{ drug.brands.map((b) => `${b.name} (${b.market})`).join(' · ') }}</p>
    <p v-if="drug.review.status === 'verified'" class="text-xs text-emerald-700 dark:text-emerald-300">{{ $t('review.by', { name: drug.review.reviewer, date: drug.review.date }) }}</p>
  </section>
</template>
