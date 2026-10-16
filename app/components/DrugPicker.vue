<script setup lang="ts">
import type { CatalogEntry } from '../../lib/types'
import { pickDrugs } from '../../lib/search/pick'
// Type-ahead drug picker: one field that is both the search box and the dropdown.
const props = defineProps<{ drugs: CatalogEntry[] }>()
const model = defineModel<string>({ required: true })
const lt = useLocalText()
const q = ref('')
const open = ref(false)
const active = ref(0)
const listEl = ref<HTMLElement | null>(null)
const uid = useId()

const selected = computed(() => props.drugs.find((d) => d.id === model.value) ?? null)
const matches = computed(() => pickDrugs(props.drugs, q.value))
// Show the chosen drug in the field when the list is closed.
watch([selected, open], () => { if (!open.value) q.value = selected.value ? lt(selected.value.name) : '' }, { immediate: true })
watch(q, () => (active.value = 0))

function choose(d: CatalogEntry) {
  model.value = d.id
  open.value = false
}
function onFocus(e: FocusEvent) {
  open.value = true
  ;(e.target as HTMLInputElement).select()
}
function onInput() {
  open.value = true
}
function onBlur() {
  setTimeout(() => (open.value = false), 120)
}
function clear() {
  model.value = ''
  q.value = ''
  open.value = true
}
function move(step: number) {
  if (!open.value) { open.value = true; return }
  const n = matches.value.length
  if (!n) return
  active.value = (active.value + step + n) % n
  nextTick(() => listEl.value?.querySelector<HTMLElement>(`[data-i="${active.value}"]`)?.scrollIntoView({ block: 'nearest' }))
}
function enter() {
  const d = matches.value[active.value]
  if (open.value && d) choose(d)
}
</script>

<template>
  <div class="relative">
    <div class="relative">
      <span class="pointer-events-none absolute inset-y-0 start-3 flex items-center text-slate-400" aria-hidden="true">🔍</span>
      <input v-model="q" type="text" class="input ps-10 pe-10" role="combobox" autocomplete="off" :aria-expanded="open" :aria-controls="`${uid}-list`"
        :aria-activedescendant="open && matches.length ? `${uid}-${active}` : undefined" :placeholder="$t('quick.searchDrugPh')"
        @focus="onFocus" @input="onInput" @blur="onBlur" @keydown.down.prevent="move(1)" @keydown.up.prevent="move(-1)"
        @keydown.enter.prevent="enter" @keydown.esc="open = false" />
      <button v-if="q" type="button" class="absolute inset-y-0 end-2 my-auto h-7 w-7 rounded-full text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800"
        :aria-label="$t('quick.clear')" @mousedown.prevent @click="clear">✕</button>
    </div>
    <ul v-show="open" :id="`${uid}-list`" ref="listEl" role="listbox"
      class="card absolute inset-x-0 top-full z-40 mt-1 max-h-80 overflow-auto p-1">
      <li v-if="!matches.length" class="px-3 py-3 text-sm text-slate-500">{{ $t('quick.noMatch') }}</li>
      <li v-for="(d, i) in matches" :id="`${uid}-${i}`" :key="d.id" :data-i="i" role="option" :aria-selected="d.id === model"
        class="flex cursor-pointer items-baseline justify-between gap-3 rounded-lg px-3 py-2"
        :class="i === active ? 'bg-brand-50 dark:bg-brand-900/40' : 'hover:bg-slate-50 dark:hover:bg-slate-800'"
        @mousedown.prevent="choose(d)" @mousemove="active = i">
        <span class="font-semibold" :class="d.id === model && 'text-brand-700 dark:text-brand-300'">{{ lt(d.name) }}</span>
        <span class="ltr truncate text-xs text-slate-500">{{ d.name.en }}</span>
      </li>
    </ul>
  </div>
</template>
