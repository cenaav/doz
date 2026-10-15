<script setup lang="ts">
import type { PopLevel } from '../../lib/types'
defineProps<{ level: PopLevel }>()
const STYLE: Record<PopLevel, string> = {
  ok: 'border-emerald-300 bg-emerald-50 text-emerald-800 dark:border-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-200',
  caution: 'border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-700 dark:bg-amber-900/40 dark:text-amber-200',
  avoid: 'border-orange-400 bg-orange-50 text-orange-800 dark:border-orange-700 dark:bg-orange-900/40 dark:text-orange-200',
  contraindicated: 'border-red-400 bg-red-50 text-red-800 dark:border-red-700 dark:bg-red-950/60 dark:text-red-200',
  'not-established': 'border-slate-300 bg-slate-50 text-slate-700 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200',
  'no-data': 'border-slate-300 bg-slate-50 text-slate-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-400',
}
</script>
<template>
  <span class="inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-semibold" :class="STYLE[level]">{{ $t(`pop.level.${level}`) }}</span>
</template>
