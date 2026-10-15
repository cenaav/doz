<script setup lang="ts">
import type { Drug, Population } from '../../lib/types'
const props = defineProps<{ drug: Drug }>()
const POPS: Population[] = ['pregnancy', 'lactation', 'pediatric', 'geriatric', 'reproductive']
const ICON: Record<Population, string> = { pregnancy: '🤰', lactation: '🤱', pediatric: '👶', geriatric: '👴', reproductive: '⚥' }
const pops = computed(() => POPS.filter((p) => props.drug.populations?.[p]).map((p) => ({ p, note: props.drug.populations![p]! })))
const blocks = computed(() => props.drug.contraindications.length)
const interactions = computed(() => props.drug.interactions.length)
</script>
<template>
  <!-- One-line summary tags; each links to the section with the full text and its source. -->
  <div class="flex flex-wrap items-center gap-1.5 text-xs">
    <a v-for="{ p, note } in pops" :key="p" :href="`#pop-${p}`" class="inline-flex items-center gap-1">
      <span>{{ ICON[p] }} {{ $t(`pop.${p}`) }}:</span><PopLevelBadge :level="note.level" />
    </a>
    <a v-if="drug.iran" href="#iran" class="inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 font-semibold"
      :class="drug.iran.status === 'not-found' ? 'border-slate-300 text-slate-600 dark:border-slate-600 dark:text-slate-300' : 'border-emerald-300 bg-emerald-50 text-emerald-800 dark:border-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-200'">
      🇮🇷 {{ $t(`iran.${drug.iran.status}`) }}
    </a>
    <a v-if="blocks" href="#safety" class="rounded-md border border-red-300 bg-red-50 px-1.5 py-0.5 font-semibold text-red-800 dark:border-red-700 dark:bg-red-950/60 dark:text-red-200">⛔ {{ $t('tags.contra', { n: blocks }) }}</a>
    <a v-if="interactions" href="#safety" class="rounded-md border border-amber-300 bg-amber-50 px-1.5 py-0.5 font-semibold text-amber-800 dark:border-amber-700 dark:bg-amber-900/40 dark:text-amber-200">⚠️ {{ $t('tags.interactions', { n: interactions }) }}</a>
    <a v-if="drug.usApproval" href="#links" class="inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 font-semibold"
      :class="drug.usApproval.kind === 'unapproved' || drug.usApproval.kind === 'dietary supplement' ? 'border-red-300 bg-red-50 text-red-800 dark:border-red-700 dark:bg-red-950/60 dark:text-red-200' : 'border-blue-300 bg-blue-50 text-blue-800 dark:border-blue-700 dark:bg-blue-900/40 dark:text-blue-200'">
      🇺🇸 {{ $t(`usApproval.${drug.usApproval.kind}`) }}<span v-if="drug.usApproval.id" class="ltr">&nbsp;{{ drug.usApproval.id }}</span>
    </a>
    <a v-for="code in drug.atc ?? []" :key="code" :href="`https://atcddd.fhi.no/atc_ddd_index/?code=${code}`" target="_blank" rel="noopener" class="chip ltr">ATC {{ code }}</a>
  </div>
</template>
