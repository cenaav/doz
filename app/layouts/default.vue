<template>
  <div class="flex min-h-dvh flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <AppHeader />
    <main class="mx-auto w-full max-w-screen-2xl flex-1 px-3 py-4 sm:px-4 lg:px-6">
      <slot />
    </main>
    <footer class="border-t border-slate-200 px-4 py-3 text-center text-xs leading-6 text-slate-500 dark:border-slate-800">
      {{ $t('disclaimer.short') }}
    </footer>
    <RefSheet />
    <DisclaimerModal />
  </div>
</template>
