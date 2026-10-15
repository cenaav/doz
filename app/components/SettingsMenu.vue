<script setup lang="ts">
const { locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const localePath = useLocalePath()
const mode = useColorMode()
const open = ref(false)
const themes = [
  { id: 'system', icon: '🖥️' },
  { id: 'light', icon: '☀️' },
  { id: 'dark', icon: '🌙' },
] as const
const route = useRoute()
watch(() => route.fullPath, () => (open.value = false))
</script>
<template>
  <div class="relative">
    <button type="button" class="btn-ghost" :aria-expanded="open" :aria-label="$t('settings.title')" @click="open = !open">
      ⚙️ <span class="hidden sm:inline">{{ $t('settings.title') }}</span>
    </button>
    <div v-if="open" class="fixed inset-0 z-40" @click="open = false" />
    <div v-if="open" class="card absolute end-0 top-full z-50 mt-2 w-64 space-y-3 p-3">
      <div>
        <p class="mb-1 text-xs text-slate-500">{{ $t('settings.language') }}</p>
        <div class="grid grid-cols-2 gap-1 rounded-xl bg-slate-100 p-1 dark:bg-slate-800">
          <NuxtLink v-for="l in locales" :key="l.code" :to="switchLocalePath(l.code)" class="rounded-lg px-2 py-1.5 text-center text-sm"
            :class="l.code === locale ? 'bg-white font-semibold text-brand-700 shadow-sm dark:bg-slate-950 dark:text-brand-300' : 'text-slate-600 dark:text-slate-300'">{{ l.name }}</NuxtLink>
        </div>
      </div>
      <div>
        <p class="mb-1 text-xs text-slate-500">{{ $t('settings.theme') }}</p>
        <ClientOnly>
          <div class="grid grid-cols-3 gap-1 rounded-xl bg-slate-100 p-1 dark:bg-slate-800">
            <button v-for="th in themes" :key="th.id" type="button" class="rounded-lg px-1 py-1.5 text-sm"
              :class="mode.preference === th.id ? 'bg-white font-semibold text-brand-700 shadow-sm dark:bg-slate-950 dark:text-brand-300' : 'text-slate-600 dark:text-slate-300'"
              @click="mode.preference = th.id">{{ th.icon }} {{ $t(`settings.themes.${th.id}`) }}</button>
          </div>
        </ClientOnly>
      </div>
      <NuxtLink :to="localePath('/settings')" class="block text-xs text-slate-500 underline">{{ $t('settings.more') }}</NuxtLink>
    </div>
  </div>
</template>
