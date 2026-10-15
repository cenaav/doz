<script setup lang="ts">
const { t, locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const mode = useColorMode()
useSeoMeta({ title: () => t('settings.title') })
const themes = ['system', 'light', 'dark'] as const
function showDisclaimer() {
  localStorage.removeItem('doz_disclaimer')
  location.reload()
}
</script>

<template>
  <div class="mx-auto max-w-xl space-y-4">
    <h1 class="text-xl font-bold">{{ $t('settings.title') }}</h1>
    <section class="card space-y-2">
      <h2 class="font-semibold">{{ $t('settings.language') }}</h2>
      <div class="flex gap-2">
        <NuxtLink v-for="l in locales" :key="l.code" :to="switchLocalePath(l.code)" class="btn-ghost border border-slate-300 dark:border-slate-700"
          :class="{ 'border-brand-500 font-bold text-brand-700 dark:text-brand-300': l.code === locale }">{{ l.name }}</NuxtLink>
      </div>
    </section>
    <section class="card space-y-2">
      <h2 class="font-semibold">{{ $t('settings.theme') }}</h2>
      <ClientOnly>
        <div class="flex gap-2">
          <button v-for="th in themes" :key="th" type="button" class="btn-ghost border border-slate-300 dark:border-slate-700"
            :class="{ 'border-brand-500 font-bold text-brand-700 dark:text-brand-300': mode.preference === th }" @click="mode.preference = th">
            {{ $t(`settings.themes.${th}`) }}
          </button>
        </div>
      </ClientOnly>
    </section>
    <section class="card">
      <button type="button" class="btn-ghost" @click="showDisclaimer">⚠️ {{ $t('settings.showDisclaimer') }}</button>
    </section>
  </div>
</template>
