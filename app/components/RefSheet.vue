<script setup lang="ts">
const { current, close } = useRefSheet()
const lt = useLocalText()
const source = computed(() => (current.value ? getSource(current.value.source) : undefined))
</script>
<template>
  <div v-if="current" class="fixed inset-0 z-50 flex items-end justify-center bg-black/50 sm:items-center" @click.self="close">
    <div class="card w-full max-w-lg rounded-b-none sm:rounded-2xl" role="dialog" aria-modal="true">
      <div class="mb-3 flex items-start justify-between gap-3">
        <h2 class="text-base font-semibold">{{ $t('refs.title') }}</h2>
        <button class="btn-ghost" :aria-label="$t('common.close')" @click="close">✕</button>
      </div>
      <dl v-if="source" class="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1.5 text-sm">
        <dt class="text-slate-500">{{ $t('refs.source') }}</dt><dd class="ltr text-start">{{ source.title }}</dd>
        <template v-if="source.publisher"><dt class="text-slate-500">{{ $t('refs.publisher') }}</dt><dd class="ltr text-start">{{ source.publisher }}</dd></template>
        <template v-if="source.citation"><dt class="text-slate-500">{{ $t('refs.citation') }}</dt><dd class="ltr text-start">{{ source.citation }}</dd></template>
        <template v-if="source.edition"><dt class="text-slate-500">{{ $t('refs.edition') }}</dt><dd class="ltr text-start">{{ source.edition }}</dd></template>
        <template v-if="current.section"><dt class="text-slate-500">{{ $t('refs.section') }}</dt><dd class="ltr text-start font-bold">{{ current.section }}</dd></template>
        <template v-if="current.page"><dt class="text-slate-500">{{ $t('refs.page') }}</dt><dd class="ltr text-start font-bold">{{ current.page }}</dd></template>
        <template v-if="current.note"><dt class="text-slate-500">{{ $t('refs.note') }}</dt><dd>{{ lt(current.note) }}</dd></template>
        <template v-if="source.accessed"><dt class="text-slate-500">{{ $t('refs.accessed') }}</dt><dd class="ltr text-start">{{ source.accessed }}</dd></template>
        <dt class="text-slate-500">{{ $t('refs.license') }}</dt><dd>{{ $t(`refs.licenses.${source.license}`) }}</dd>
      </dl>
      <p v-else class="text-red-600">{{ $t('refs.unknown') }}</p>
      <a v-if="current.url || source?.url" :href="current.url || source?.url" target="_blank" rel="noopener noreferrer" class="btn mt-4 w-full">{{ $t('refs.open') }} ↗</a>
    </div>
  </div>
</template>
