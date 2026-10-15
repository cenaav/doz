<script setup lang="ts">
import type { Drug } from '../../lib/types'
const props = defineProps<{ drug: Drug }>()
const lt = useLocalText()
const localePath = useLocalePath()
const diseaseIds = new Set(props.drug.regimens.map((r) => r.disease))
const others = catalog.filter((d) => d.id !== props.drug.id)
const sameClass = others.filter((d) => props.drug.class?.en && d.class?.en === props.drug.class.en)
const sameDisease = others.filter((d) => !sameClass.includes(d) && d.regimens.some((r) => diseaseIds.has(r.disease)))
</script>

<template>
  <section v-if="sameClass.length || sameDisease.length" class="card space-y-3">
    <h2 class="card-title !mb-0">🔗 {{ $t('drug.similar') }}</h2>
    <div v-for="[label, list] in ([['sameClass', sameClass], ['sameDisease', sameDisease]] as const)" :key="label">
      <template v-if="list.length">
        <h3 class="mb-1 text-xs font-medium text-slate-500">{{ $t(`drug.${label}`) }}</h3>
        <div class="flex flex-wrap gap-2">
          <NuxtLink v-for="d in list" :key="d.id" :to="localePath(`/drug/${d.id}`)" class="chip text-sm">{{ lt(d.name) }}</NuxtLink>
        </div>
      </template>
    </div>
  </section>
</template>
