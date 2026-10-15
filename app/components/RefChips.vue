<script setup lang="ts">
import type { Ref as DataRef } from '../../lib/types'
const props = defineProps<{ refs?: DataRef[] }>()
const { open } = useRefSheet()
const href = (r: DataRef) => r.url || getSource(r.source)?.url
const label = (r: DataRef) => {
  const s = getSource(r.source)
  return `${s?.short ?? r.source}${r.section ? ` §${r.section}` : ''}${r.page ? ` p.${r.page}` : ''}`
}
</script>
<template>
  <span class="inline-flex flex-wrap gap-1 align-middle">
    <span v-if="!props.refs?.length" class="rounded-md bg-red-100 px-1.5 py-0.5 text-xs font-bold text-red-700 dark:bg-red-900/50 dark:text-red-200">{{ $t('refs.none') }}</span>
    <span v-for="(r, i) in props.refs" :key="i" class="inline-flex items-stretch">
      <button type="button" class="chip ltr rounded-e-none" @click="open(r)">{{ label(r) }}</button>
      <a v-if="href(r)" :href="href(r)" target="_blank" rel="noopener noreferrer" class="chip rounded-s-none border-s-0 px-1" :aria-label="$t('refs.open')" :title="$t('refs.open')">↗</a>
    </span>
  </span>
</template>
