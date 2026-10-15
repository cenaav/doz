<script setup lang="ts">
import type { Drug, DrugLink } from '../../lib/types'
const props = defineProps<{ drug: Drug }>()
const lt = useLocalText()
// Main reference services are always listed, so a missing one shows as "none" instead of disappearing.
const MAIN: DrugLink['kind'][] = ['fda', 'dailymed', 'medlineplus', 'who-atc', 'darooyab']
const rows = computed(() => {
  const links = props.drug.links ?? []
  const extra = links.filter((l) => !MAIN.includes(l.kind))
  return [...MAIN.map((kind) => ({ kind, items: links.filter((l) => l.kind === kind) })), ...extra.map((l) => ({ kind: l.kind, items: [l] }))]
})
</script>
<template>
  <section id="links" class="card scroll-mt-20 space-y-3">
    <h2 class="card-title !mb-0">🔗 {{ $t('links.title') }}</h2>
    <ul class="divide-y divide-slate-200 text-sm dark:divide-slate-800">
      <li v-for="row in rows" :key="row.kind + row.items.map((i) => i.url).join()" class="flex flex-wrap items-center justify-between gap-2 py-2">
        <span>{{ $t(`links.${row.kind}`) }}</span>
        <span v-if="row.items.length" class="flex flex-wrap gap-1">
          <a v-for="l in row.items" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="chip ltr">{{ l.label ?? $t(`links.open`) }}</a>
        </span>
        <span v-else class="font-medium text-red-600">❌ {{ $t('links.none') }}</span>
      </li>
    </ul>
    <div v-if="drug.iran" id="iran" class="scroll-mt-20 space-y-1 border-t border-slate-100 pt-2 dark:border-slate-800">
      <h3 class="text-sm font-semibold">🇮🇷 {{ $t(`iran.${drug.iran.status}`) }} <RefChips :refs="drug.iran.refs" /></h3>
      <p class="text-xs text-slate-500">{{ $t(`iran.help.${drug.iran.status}`) }}</p>
      <ul v-if="drug.iran.forms?.length" class="space-y-0.5 text-xs">
        <li v-for="f in drug.iran.forms" :key="f.code"><span class="ltr font-mono">{{ f.code }}</span> · <span class="ltr">{{ f.en }}</span><span v-if="f.fa"> · {{ f.fa }}</span></li>
      </ul>
    </div>
  </section>
</template>
