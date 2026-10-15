<script setup lang="ts">
import type { Drug, SourceType } from '../../lib/types'
import { drugRefs, groupRefsByType } from '../../lib/data/refs'
const props = defineProps<{ drug: Drug }>()
const ALWAYS: SourceType[] = ['fda-label', 'guideline', 'licensed-reference', 'ifda-leaflet']
const grouped = computed(() => groupRefsByType(drugRefs(props.drug), sources))
const rows = computed(() => {
  const extra = [...grouped.value.keys()].filter((k) => !ALWAYS.includes(k))
  return [...ALWAYS, ...extra].map((type) => ({ type, refs: grouped.value.get(type) ?? [] }))
})
</script>
<template>
  <section class="card space-y-3">
    <h2 class="text-lg font-bold">📚 {{ $t('refStatus.title') }}</h2>
    <p class="text-xs text-slate-500">{{ $t('refStatus.help') }}</p>
    <ul class="divide-y divide-slate-200 dark:divide-slate-800">
      <li v-for="row in rows" :key="row.type" class="py-2">
        <div class="flex items-center justify-between gap-2">
          <span class="font-bold">{{ $t(`sourceTypes.${row.type}`) }}</span>
          <span :class="row.refs.length ? 'text-emerald-600' : 'text-red-600'" class="text-sm font-bold">{{ row.refs.length ? '✅ ' + $t('refStatus.present') : '❌ ' + $t('refStatus.absent') }}</span>
        </div>
        <RefChips v-if="row.refs.length" :refs="row.refs" class="mt-1" />
      </li>
      <li class="flex items-center justify-between gap-2 py-2">
        <span class="font-bold">{{ $t('refStatus.review') }}</span>
        <ReviewBadge :status="drug.review.status" />
      </li>
    </ul>
  </section>
</template>
