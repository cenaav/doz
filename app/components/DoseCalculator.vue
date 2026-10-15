<script setup lang="ts">
import type { AgeUnit, Drug } from '../../lib/types'
import { calculate, needsWeight } from '../../lib/engine'
import { toDays } from '../../lib/engine/age'
const props = defineProps<{ drug: Drug; regimenIds?: string[] }>()
const regimens = computed(() => (props.regimenIds ? props.drug.regimens.filter((r) => props.regimenIds!.includes(r.id)) : props.drug.regimens))
const route = useRoute()
const lt = useLocalText()
const localePath = useLocalePath()

const regimenFromQuery = () => {
  const q = route.query.regimen
  return typeof q === 'string' && regimens.value.some((r) => r.id === q) ? q : null
}
const regimenId = ref(regimenFromQuery() ?? regimens.value[0].id)
// Pre-rendered HTML is built without the query string, so apply ?regimen= again after hydration.
onMounted(() => {
  const q = regimenFromQuery()
  if (q) regimenId.value = q
})
watch(regimens, (rs) => { if (!rs.some((r) => r.id === regimenId.value)) regimenId.value = rs[0].id })
const regimen = computed(() => regimens.value.find((r) => r.id === regimenId.value) ?? regimens.value[0])
const weightNeeded = computed(() => needsWeight(props.drug, regimen.value))
const formulations = computed(() => props.drug.formulations.filter((f) => !regimen.value.allowedFormulations || regimen.value.allowedFormulations.includes(f.id)))
const formulationId = ref('')
watch(formulations, (fs) => { if (!fs.some((f) => f.id === formulationId.value)) formulationId.value = fs[0]?.id ?? '' }, { immediate: true })

const ageText = ref(''); const ageUnit = ref<AgeUnit>('year')
const weightText = ref(''); const heightText = ref(''); const scrText = ref('')
const showRenal = ref(false)
const age = computed(() => parseNumber(ageText.value))
const weight = computed(() => parseNumber(weightText.value))

const result = computed(() => {
  if (regimen.value.type === 'notCalculated' || age.value == null) return null
  if (weight.value == null && (weightNeeded.value || weightText.value)) return null
  return calculate(props.drug, regimen.value.id, formulationId.value, {
    ageDays: toDays({ value: age.value, unit: ageUnit.value }),
    weightKg: weight.value ?? undefined,
    heightCm: parseNumber(heightText.value) ?? undefined,
    scrMgDl: parseNumber(scrText.value) ?? undefined,
  })
})
const disease = computed(() => getDisease(regimen.value.disease))
const groups = computed(() => {
  const by = new Map<string, typeof props.drug.regimens>()
  for (const r of regimens.value) by.set(r.disease, [...(by.get(r.disease) ?? []), r])
  return [...by].map(([id, regimens]) => ({ id, name: lt(getDisease(id)?.name), regimens }))
})
</script>
<template>
  <section class="card space-y-4">
    <h2 class="card-title !mb-0">🧮 {{ $t('calc.title') }}</h2>

    <label class="block space-y-1">
      <span class="text-sm font-medium">{{ $t('calc.regimen') }}</span>
      <select v-model="regimenId" class="input">
        <optgroup v-for="g in groups" :key="g.id" :label="g.name">
          <option v-for="r in g.regimens" :key="r.id" :value="r.id">{{ lt(r.label) }}</option>
        </optgroup>
      </select>
    </label>
    <p class="text-xs text-slate-500">
      <NuxtLink v-if="disease" :to="localePath(`/disease/${disease.id}`)" class="underline">{{ lt(disease.name) }}</NuxtLink>
      · {{ $t('calc.regimenRefs') }} <RefChips :refs="regimen.refs" />
    </p>
    <ul v-if="regimen.notes?.length" class="space-y-1 text-sm">
      <li v-for="(n, i) in regimen.notes" :key="i">• {{ lt(n.text) }} <RefChips :refs="n.refs" /></li>
    </ul>

    <div v-if="regimen.type === 'notCalculated'" class="rounded-xl border border-amber-300 bg-amber-50 p-3 text-sm dark:border-amber-800 dark:bg-amber-950">
      ⛔ {{ lt(regimen.dose.reason) }} <RefChips :refs="regimen.refs" />
    </div>

    <template v-else>
      <label class="block space-y-1">
        <span class="text-sm font-medium">{{ $t('calc.formulation') }}</span>
        <select v-model="formulationId" class="input ltr">
          <option v-for="f in formulations" :key="f.id" :value="f.id">{{ f.label }} ({{ $t(`forms.${f.form}`) }})</option>
        </select>
      </label>
      <div class="grid grid-cols-2 gap-3">
        <label class="block space-y-1">
          <span class="text-sm font-medium">{{ $t('calc.age') }} *</span>
          <div class="flex gap-1">
            <input v-model="ageText" class="input min-w-0" inputmode="decimal" :placeholder="$t('calc.agePh')" />
            <select v-model="ageUnit" class="input w-auto px-2">
              <option v-for="u in ['day', 'week', 'month', 'year']" :key="u" :value="u">{{ $t(`units.${u}`) }}</option>
            </select>
          </div>
        </label>
        <label class="block space-y-1">
          <span class="text-sm font-medium">{{ $t('calc.weight') }} {{ weightNeeded ? '*' : `(${$t('calc.optionalShort')})` }}</span>
          <input v-model="weightText" class="input" inputmode="decimal" :placeholder="$t('calc.weightPh')" />
        </label>
      </div>
      <button type="button" class="btn-ghost" @click="showRenal = !showRenal">{{ showRenal ? '▾' : '▸' }} {{ $t('calc.optional') }}</button>
      <div v-if="showRenal" class="grid grid-cols-2 gap-3">
        <label class="block space-y-1"><span class="text-sm">{{ $t('calc.height') }}</span><input v-model="heightText" class="input" inputmode="decimal" /></label>
        <label class="block space-y-1"><span class="text-sm">{{ $t('calc.scr') }}</span><input v-model="scrText" class="input" inputmode="decimal" /></label>
      </div>
      <p v-if="ageText && age == null" class="text-sm text-red-600">{{ $t('calc.badNumber', { field: $t('calc.age') }) }}</p>
      <p v-if="weightText && weight == null" class="text-sm text-red-600">{{ $t('calc.badNumber', { field: $t('calc.weight') }) }}</p>
      <DoseResult v-if="result" :result="result" :drug="drug" />
      <p v-else class="text-sm text-slate-500">{{ weightNeeded ? $t('calc.enterInputs') : $t('calc.enterAge') }}</p>
    </template>
  </section>
</template>
