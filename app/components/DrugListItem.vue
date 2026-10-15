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
    <ReviewBadge :status="drug.reviewStatus" small />
  </NuxtLink>
</template>
