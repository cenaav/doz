<script setup lang="ts">
import type { CatalogEntry, Drug } from '../../lib/types'
const { t } = useI18n()
const fmt = useFormatNumber()
const lt = useLocalText()
const localePath = useLocalePath()
usePageMeta(() => t('quick.title'), () => t('quick.description'))

type Mode = 'weight' | 'age'
const MODE_TYPES: Record<Mode, string[]> = { weight: ['weightBased', 'bsa', 'loading', 'weightBand'], age: ['ageBand', 'fixed', 'titration'] }
const mode = ref<Mode>('weight')
const category = ref<string | null>(null)
const drugId = ref('')

const inMode = (type: string) => MODE_TYPES[mode.value].includes(type)
const drugsInMode = computed(() => catalog.filter((d) => d.regimens.some((r) => inMode(r.type))))
const cats = computed(() => categories.filter((c) => drugsInMode.value.some((d) => d.category === c.id)))
const list = computed<CatalogEntry[]>(() =>
  drugsInMode.value.filter((d) => !category.value || d.category === category.value).sort((a, b) => lt(a.name).localeCompare(lt(b.name))),
)
watch([mode, category], () => {
  if (!list.value.some((d) => d.id === drugId.value)) drugId.value = ''
})

// Loaded on the client only. useAsyncData with a fixed key returned the prerendered (empty) value
// after in-app navigation, so selecting a drug showed nothing.
const drug = shallowRef<Drug | null>(null)
watch(drugId, async (id) => {
  const loaded = id ? await loadDrug(id) : null
  if (drugId.value === id) drug.value = loaded
})
const regimenIds = computed(() => drug.value?.regimens.filter((r) => inMode(r.type)).map((r) => r.id) ?? [])
const doseCupRef = [{ source: 'fda-childrens-tylenol', section: 'Directions', note: { fa: 'فقط از پیمانه مخصوص همراه دارو استفاده شود', en: 'Use only the enclosed dosing cup; do not use any other dosing device' } }]
</script>

<template>
  <div class="mx-auto max-w-3xl space-y-4">
    <h1 class="text-center text-xl font-black">🧮 {{ $t('quick.title') }}</h1>

    <div class="flex items-start gap-2 rounded-2xl border border-red-200 bg-red-50 p-3 text-sm leading-7 text-red-800 dark:border-red-900 dark:bg-red-950/60 dark:text-red-200">
      <span class="text-lg">🛡️</span>
      <p><b>{{ $t('quick.safetyTitle') }}</b> {{ $t('quick.safety') }} <RefChips :refs="doseCupRef" /></p>
    </div>

    <div class="grid grid-cols-2 gap-1 rounded-2xl bg-slate-100 p-1 dark:bg-slate-800" role="tablist">
      <button v-for="m in (['weight', 'age'] as const)" :key="m" type="button" role="tab" :aria-selected="mode === m"
        class="rounded-xl py-2.5 text-sm font-bold transition"
        :class="mode === m ? 'bg-white text-brand-700 shadow dark:bg-slate-900 dark:text-brand-300' : 'text-slate-600 dark:text-slate-300'"
        @click="mode = m">
        {{ m === 'weight' ? '⚖️' : '🧒' }} {{ $t(`quick.mode.${m}`) }}
      </button>
    </div>
    <p class="text-center text-xs text-slate-500">{{ $t(`quick.modeHelp.${mode}`) }}</p>

    <div class="grid grid-cols-2 gap-2 sm:grid-cols-3">
      <button type="button" class="rounded-xl border px-3 py-2 text-sm font-bold"
        :class="!category ? 'border-brand-600 bg-brand-600 text-white' : 'border-slate-300 dark:border-slate-700'" @click="category = null">
        {{ $t('quick.allCategories') }}
      </button>
      <button v-for="c in cats" :key="c.id" type="button" class="rounded-xl border px-3 py-2 text-sm font-bold"
        :class="category === c.id ? 'border-brand-600 bg-brand-600 text-white' : 'border-slate-300 dark:border-slate-700'" @click="category = c.id">
        {{ c.icon }} {{ lt(c.name) }}
      </button>
    </div>

    <label class="block space-y-1">
      <span class="text-sm font-bold">💊 {{ $t('quick.selectDrug') }} <span class="font-normal text-slate-500">({{ $t('quick.count', { n: fmt(list.length) }) }})</span></span>
      <select v-model="drugId" class="input">
        <option value="">{{ $t('quick.selectDrugPh') }}</option>
        <option v-for="d in list" :key="d.id" :value="d.id">{{ lt(d.name) }} — {{ d.name.en }}</option>
      </select>
      <span class="block text-xs leading-5 text-slate-500">{{ $t('quick.notListed') }}</span>
    </label>

    <template v-if="drug && regimenIds.length">
      <DoseCalculator :key="`${drug.id}-${mode}`" :drug="drug" :regimen-ids="regimenIds" />
      <NuxtLink :to="localePath(`/drug/${drug.id}`)" class="btn-ghost w-full justify-center border border-slate-300 dark:border-slate-700">
        📚 {{ $t('quick.fullPage') }}
      </NuxtLink>
    </template>
  </div>
</template>
