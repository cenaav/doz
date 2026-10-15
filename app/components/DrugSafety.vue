<script setup lang="ts">
import type { Drug } from '../../lib/types'
defineProps<{ drug: Drug }>()
const lt = useLocalText()
</script>
<template>
  <section id="safety" class="card scroll-mt-20 space-y-4">
    <h2 class="card-title !mb-0">🛡️ {{ $t('safety.title') }}</h2>
    <div v-if="drug.contraindications.length">
      <h3 class="mb-1 text-sm font-semibold text-red-700 dark:text-red-400">{{ $t('safety.contraindications') }}</h3>
      <ul class="space-y-1 text-sm">
        <li v-for="c in drug.contraindications" :key="c.id">{{ c.severity === 'block' ? '⛔' : '⚠️' }} {{ lt(c.text) }} <RefChips :refs="c.refs" /></li>
      </ul>
    </div>
    <div v-for="sec in (['warnings', 'monitoring', 'interactions'] as const)" :key="sec">
      <template v-if="drug[sec].length">
        <h3 class="mb-1 text-sm font-semibold">{{ $t(`safety.${sec}`) }}</h3>
        <ul class="space-y-1 text-sm"><li v-for="(n, i) in drug[sec]" :key="i">• {{ lt(n.text) }} <RefChips :refs="n.refs" /></li></ul>
      </template>
    </div>
    <div v-if="drug.renal.length">
      <h3 class="mb-1 text-sm font-semibold">{{ $t('safety.renal') }}</h3>
      <ul class="space-y-1 text-sm"><li v-for="(r, i) in drug.renal" :key="i">• eGFR &lt; {{ r.egfrBelow }}: {{ lt(r.text) }} <RefChips :refs="r.refs" /></li></ul>
    </div>
    <div>
      <h3 class="mb-1 text-sm font-semibold">{{ $t('safety.formulations') }}</h3>
      <ul class="space-y-1 text-sm"><li v-for="f in drug.formulations" :key="f.id"><span class="ltr">{{ f.label }}</span> — {{ $t(`forms.${f.form}`) }} <MarketBadges :markets="f.markets" small /> <RefChips :refs="f.refs" /></li></ul>
    </div>
  </section>
</template>
