<script setup lang="ts">
import type { Ref as DataRef } from '../../lib/types'
const props = defineProps<{ refs?: DataRef[] }>()
const { open } = useRefSheet()
const label = (r: DataRef) => {
  const s = getSource(r.source)
  return `${s?.short ?? r.source}${r.section ? ` §${r.section}` : ''}${r.page ? ` p.${r.page}` : ''}`
}
</script>
<template>
  <span class="inline-flex flex-wrap gap-1 align-middle">
    <span v-if="!props.refs?.length" class="rounded-md bg-red-100 px-1.5 py-0.5 text-xs font-bold text-red-700 dark:bg-red-900/50 dark:text-red-200">{{ $t('refs.none') }}</span>
    <button v-for="(r, i) in props.refs" :key="i" type="button" class="chip ltr" @click="open(r)">{{ label(r) }}</button>
  </span>
</template>
