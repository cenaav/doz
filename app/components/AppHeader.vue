<script setup lang="ts">
const localePath = useLocalePath()
const route = useRoute()
const isHome = computed(() => route.path.replace(/\/$/, '') === localePath('/').replace(/\/$/, ''))
</script>
<template>
  <header class="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-900/90">
    <div class="mx-auto flex max-w-screen-2xl items-center gap-2 px-3 py-2 sm:px-4 lg:px-6">
      <NuxtLink :to="localePath('/')" class="text-xl font-black text-brand-600 dark:text-brand-400">Doz</NuxtLink>
      <SearchBox v-if="!isHome" compact class="mx-2 hidden max-w-xl flex-1 md:block" />
      <nav class="ms-auto flex items-center gap-0.5">
        <NuxtLink v-if="!isHome" :to="localePath('/')" class="btn-ghost md:hidden" :aria-label="$t('search.placeholder')">🔍</NuxtLink>
        <NuxtLink :to="localePath('/sources')" class="btn-ghost hidden sm:inline-flex">{{ $t('nav.sources') }}</NuxtLink>
        <NuxtLink :to="localePath('/about')" class="btn-ghost">{{ $t('nav.about') }}</NuxtLink>
        <LangSwitch />
        <ThemeToggle />
      </nav>
    </div>
  </header>
</template>
