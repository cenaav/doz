<script setup lang="ts">
import type { Drug } from '../../lib/types'
import type { Result, Msg } from '../../lib/engine'
import { drugConfidence } from '../../lib/data/refs'
const props = defineProps<{ result: Result; drug: Drug }>()
const lt = useLocalText()
const { t } = useI18n()
const fmt = useFormatNumber()
const u = computed(() => t(`units.dose.${props.result.unit}`))
const lowConfidence = computed(() => drugConfidence(props.drug, sources) === 'low')
const msg = (m: Msg) => (m.text ? lt(m.text) : t(`engine.${m.code}`, m.params ?? {}))
</script>
<template>
  <div class="space-y-3" aria-live="polite">
    <ConfidenceBanner v-if="lowConfidence" compact />
    <div v-if="result.status === 'invalidInput' || result.status === 'blocked'" class="rounded-xl border border-red-300 bg-red-50 p-3 dark:border-red-800 dark:bg-red-950">
      <p class="font-semibold text-red-700 dark:text-red-300">⛔ {{ $t(`calc.status.${result.status}`) }}</p>
      <ul class="mt-1 space-y-1 text-sm">
        <li v-for="(b, i) in result.blocks" :key="i">• {{ msg(b) }} <span v-if="b.code !== 'CONTRAINDICATION' && b.code !== 'RENAL' && b.text">({{ $t(`engine.${b.code}`, b.params ?? {}) }})</span> <RefChips v-if="b.refs" :refs="b.refs" /></li>
      </ul>
    </div>

    <div v-else-if="result.status === 'notCalculated'" class="rounded-xl border border-amber-300 bg-amber-50 p-3 text-sm dark:border-amber-800 dark:bg-amber-950">⛔ {{ lt(result.reason) }}</div>

    <div v-else-if="result.perMin != null" class="rounded-2xl bg-brand-50 p-4 dark:bg-brand-900/30">
      <p class="text-sm text-slate-600 dark:text-slate-300">{{ $t('calc.pumpRate') }}</p>
      <p v-if="result.mlPerHour != null" class="text-2xl font-bold text-brand-700 dark:text-brand-300">
        {{ fmt(result.mlPerHour) }}<template v-if="result.upper?.mlPerHour != null"> – {{ fmt(result.upper.mlPerHour) }}</template> {{ $t('units.mlPerHour') }}
      </p>
      <p class="mt-1 text-sm">= {{ fmt(result.perMin) }}<template v-if="result.upper?.perMin != null"> – {{ fmt(result.upper.perMin) }}</template> {{ u }}/min</p>
      <p class="mt-1 text-xs text-slate-500">{{ $t('calc.infusionNote') }}</p>
    </div>

    <template v-else>
      <div class="rounded-2xl bg-brand-50 p-4 dark:bg-brand-900/30">
        <p class="text-sm text-slate-600 dark:text-slate-300">{{ $t('calc.perDose') }}</p>
        <p class="text-2xl font-bold text-brand-700 dark:text-brand-300">
          <template v-if="result.mlPerDoseRounded != null">{{ fmt(result.mlPerDoseRounded) }}<template v-if="result.upper"> – {{ fmt(result.upper.mlPerDoseRounded) }}</template> {{ $t('units.ml') }}</template>
          <template v-else-if="result.tabletsPerDoseRounded != null">{{ fmt(result.tabletsPerDoseRounded) }}<template v-if="result.upper"> – {{ fmt(result.upper.tabletsPerDoseRounded) }}</template> {{ $t(`units.${result.tabletUnit}`) }}</template>
          <template v-else>{{ fmt(result.perDose) }}<template v-if="result.upper"> – {{ fmt(result.upper.perDose) }}</template> {{ u }}</template>
        </p>
        <p v-if="result.mlPerDoseRounded == null && result.tabletsPerDoseRounded == null" class="mt-1 text-sm text-slate-500">{{ $t('calc.vialNote') }}</p>
        <p v-else class="mt-1 text-sm">
          = {{ fmt(result.perDose) }}<template v-if="result.upper"> – {{ fmt(result.upper.perDose) }}</template> {{ u }}
          <span v-if="result.mlPerDose != null && result.mlPerDose !== result.mlPerDoseRounded" class="text-slate-500">({{ $t('calc.exact') }}: {{ fmt(result.mlPerDose) }} {{ $t('units.ml') }})</span>
          <span v-if="result.tabletsPerDose != null && result.tabletsPerDose !== result.tabletsPerDoseRounded" class="text-slate-500">({{ $t('calc.exact') }}: {{ fmt(result.tabletsPerDose) }})</span>
        </p>
        <p class="mt-2 font-medium">{{ $t('calc.every', { h: fmt(result.intervalHours), n: fmt(result.dosesPerDay) }) }}</p>
        <p class="text-sm">{{ $t('calc.perDay') }}: {{ fmt(result.perDay) }}<template v-if="result.upper"> – {{ fmt(result.upper.perDay) }}</template> {{ u }}<span v-if="result.mlPerDay != null"> ({{ fmt(result.mlPerDay) }}<template v-if="result.upper?.mlPerDay != null"> – {{ fmt(result.upper.mlPerDay) }}</template> {{ $t('units.ml') }})</span></p>
        <p v-if="result.durationDays" class="text-sm">{{ $t('calc.duration', { min: fmt(result.durationDays.min), max: fmt(result.durationDays.max) }) }}</p>
        <p v-if="result.bsa" class="text-sm">BSA: {{ fmt(result.bsa) }} m²</p>
        <p v-if="result.egfr" class="text-sm">eGFR (bedside Schwartz): {{ fmt(result.egfr) }}</p>
      </div>

      <table v-if="result.schedule" class="w-full text-sm">
        <thead><tr class="text-slate-500"><th class="text-start">{{ $t('calc.days') }}</th><th class="text-start">{{ $t('calc.perDose') }}</th><th class="text-start">{{ $t('calc.perDay') }}</th></tr></thead>
        <tbody>
          <tr v-for="s in result.schedule" :key="s.fromDay" class="border-t border-slate-200 dark:border-slate-800">
            <td>{{ s.fromDay === s.toDay ? fmt(s.fromDay) : `${fmt(s.fromDay)}–${fmt(s.toDay)}` }}</td>
            <td><b v-if="s.mlPerDoseRounded != null">{{ fmt(s.mlPerDoseRounded) }} {{ $t('units.ml') }}</b> ({{ fmt(s.perDose) }} {{ u }})</td>
            <td>{{ fmt(s.perDay) }} {{ u }} <span v-if="s.capped" class="text-amber-600">⚑ {{ $t('calc.capped') }}</span></td>
          </tr>
        </tbody>
      </table>

      <div v-if="result.titration" class="rounded-xl border border-slate-200 p-3 text-sm dark:border-slate-800">
        <p class="font-semibold">{{ $t('calc.titration') }}</p>
        <p>{{ $t('calc.tStart', { d: fmt(result.titration.start), u }) }}</p>
        <p v-if="result.titration.increment">{{ $t('calc.tIncrement', { d: fmt(result.titration.increment), every: fmt(result.titration.incrementEveryDays), u }) }}</p>
        <p v-if="result.titration.targetMin && result.titration.targetMin === result.titration.targetMax">{{ $t('calc.tTargetOne', { d: fmt(result.titration.targetMin), u }) }}</p>
        <p v-else-if="result.titration.targetMin">{{ $t('calc.tTarget', { min: fmt(result.titration.targetMin), max: fmt(result.titration.targetMax), u }) }}</p>
        <p class="font-semibold">{{ $t('calc.tMax', { d: fmt(result.titration.max), u }) }}</p>
      </div>

      <p v-if="result.upper" class="text-xs text-slate-500">{{ $t('calc.rangeNote') }}</p>
      <ul v-if="[...result.capsApplied, ...(result.upper?.capsApplied ?? [])].length" class="space-y-1 rounded-xl border border-amber-300 bg-amber-50 p-3 text-sm dark:border-amber-800 dark:bg-amber-950">
        <li v-for="(c, i) in [...result.capsApplied, ...(result.upper?.capsApplied ?? [])]" :key="i">🛡️ {{ $t(`calc.cap.${c.kind}`, { v: fmt(c.limit), u }) }} <RefChips :refs="c.refs" /></li>
      </ul>
    </template>

    <ul v-if="result.warnings.length" class="space-y-1 rounded-xl border border-amber-300 bg-amber-50 p-3 text-sm dark:border-amber-800 dark:bg-amber-950">
      <li v-for="(w, i) in result.warnings" :key="i">⚠️ {{ msg(w) }} <RefChips v-if="w.refs" :refs="w.refs" /></li>
    </ul>

    <div class="text-sm"><span class="font-medium">{{ $t('calc.refsUsed') }}:</span> <RefChips :refs="result.refs" /></div>
    <p v-if="drug.review.status !== 'verified'" class="text-xs font-bold text-amber-700 dark:text-amber-300">⚠ {{ $t('review.unverifiedResult') }}</p>
    <p class="text-xs text-slate-500">{{ $t('disclaimer.short') }}</p>
  </div>
</template>
