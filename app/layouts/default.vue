<script setup lang="ts">
const localePath = useLocalePath()
const route = useRoute()
const isHome = computed(() => route.path.replace(/\/$/, '') === localePath('/').replace(/\/$/, ''))
const { current } = useRefSheet()
</script>

<template>
  <div class="flex min-h-dvh flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <AppHeader />
    <main class="mx-auto w-full max-w-screen-2xl flex-1 px-3 py-4 sm:px-4 lg:px-6">
      <SafetyBanner v-if="!isHome" class="mb-4" />
      <slot />
    </main>
    <footer class="space-y-1 border-t border-slate-200 px-4 py-4 text-center text-xs leading-6 text-slate-500 dark:border-slate-800">
      <p>
        {{ $t('disclaimer.short') }}
        <NuxtLink :to="localePath('/about')" class="ms-1 underline">{{ $t('nav.about') }}</NuxtLink> ·
        <NuxtLink :to="localePath('/sources')" class="underline">{{ $t('nav.sources') }}</NuxtLink>
      </p>
      <p>
        {{ $t('footer.inspired') }}
        <a href="https://nameofstone.github.io/Saphira/" target="_blank" rel="noopener" class="underline">Saphira</a>{{ $t('footer.inspiredTail') }}
      </p>
      <p>
        {{ $t('footer.contact') }}
        <a href="https://t.me/cenaav" target="_blank" rel="noopener" class="ltr font-medium text-brand-700 underline dark:text-brand-300">@cenaav</a>
      </p>
    </footer>
    <LazyRefSheet v-if="current" />
    <DisclaimerModal />
  </div>
</template>
