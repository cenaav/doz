<script setup lang="ts">
import type { Ref as DataRef } from '../../lib/types'
const props = defineProps<{ refs?: DataRef[] }>()
const href = (r: DataRef) => r.url || getSource(r.source)?.url
const where = (r: DataRef) => [r.section, r.page ? `p. ${r.page}` : ''].filter(Boolean).join(' · ')
const title = (r: DataRef) => {
  const s = getSource(r.source)
  return [s?.title, s?.edition, where(r)].filter(Boolean).join('\n')
}
</script>
<template>
  <span class="inline-flex flex-wrap items-center gap-1 align-middle">
    <span v-if="!props.refs?.length" class="rounded-md bg-red-100 px-1.5 py-0.5 text-xs font-bold text-red-700 dark:bg-red-900/50 dark:text-red-200">{{ $t('refs.none') }}</span>
    <component :is="href(r) ? 'a' : 'span'" v-for="(r, i) in props.refs" :key="i" class="chip ltr !inline max-w-full text-start leading-6 [box-decoration-break:clone]"
      :href="href(r)" :target="href(r) ? '_blank' : undefined" :rel="href(r) ? 'noopener noreferrer' : undefined" :title="title(r)">
      <span class="font-semibold">{{ getSource(r.source)?.short ?? r.source }}</span>
      <span v-if="where(r)" class="opacity-75"> · {{ where(r) }}</span>
    </component>
  </span>
</template>
