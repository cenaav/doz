<script setup lang="ts">
import type { CatalogEntry } from '../../lib/types'
defineProps<{ drug: CatalogEntry }>()
const lt = useLocalText()
const { locale } = useI18n()
const localePath = useLocalePath()
</script>
<template>
  <NuxtLink :to="localePath(`/drug/${drug.id}`)" class="card flex items-center justify-between gap-3 hover:border-brand-400">
    <div>
      <div class="font-bold">{{ lt(drug.name) }}</div>
      <div class="text-start text-sm text-slate-500">{{ locale === 'fa' ? drug.name.en : drug.name.fa }}<span v-if="drug.brands.length" class="ltr"> · {{ drug.brands.slice(0, 3).join(', ') }}</span></div>
    </div>
    <div class="flex shrink-0 flex-col items-end gap-1">
      <ReviewBadge :status="drug.reviewStatus" small />
      <span v-if="drug.confidence === 'low'" class="rounded-full bg-red-600 px-2 py-0.5 text-[10px] font-bold text-white">⚠ {{ $t('confidence.short') }}</span>
      <MarketBadges :markets="drug.markets" small />
    </div>
  </NuxtLink>
</template>
