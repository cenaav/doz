<script setup lang="ts">
defineProps<{ markets: string[]; small?: boolean }>()
const STYLE: Record<string, string> = {
  IR: 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-900/50 dark:text-emerald-200 dark:border-emerald-700',
  US: 'bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/50 dark:text-blue-200 dark:border-blue-700',
  GB: 'bg-purple-100 text-purple-800 border-purple-300 dark:bg-purple-900/50 dark:text-purple-200 dark:border-purple-700',
  UN: 'bg-sky-100 text-sky-800 border-sky-300 dark:bg-sky-900/50 dark:text-sky-200 dark:border-sky-700',
}
const FLAG: Record<string, string> = { IR: '🇮🇷', US: '🇺🇸', GB: '🇬🇧', UN: '🌐' }
</script>

<template>
  <span class="inline-flex flex-wrap gap-1 align-middle">
    <span v-for="m in markets" :key="m" class="inline-flex items-center gap-0.5 rounded-full border font-bold"
      :class="[STYLE[m] ?? 'border-slate-300 bg-slate-100 text-slate-700', small ? 'px-1.5 text-[10px]' : 'px-2 py-0.5 text-xs']"
      :title="$t(`markets.${m}`, m)">
      {{ FLAG[m] ?? '' }} {{ $t(`markets.${m}`, m) }}
    </span>
  </span>
</template>
