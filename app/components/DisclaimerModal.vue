<script setup lang="ts">
const VERSION = '1'
const show = ref(false)
const agreed = ref(false)
onMounted(() => { show.value = localStorage.getItem('doz_disclaimer') !== VERSION })
function accept() { localStorage.setItem('doz_disclaimer', VERSION); show.value = false }
</script>
<template>
  <div v-if="show" class="fixed inset-0 z-[60] grid place-items-center bg-black/60 p-4" role="dialog" aria-modal="true" aria-labelledby="disclaimer-title">
    <div class="card max-h-[90dvh] w-full max-w-lg space-y-3 overflow-auto">
      <h2 id="disclaimer-title" class="text-xl font-black text-red-700 dark:text-red-400">⚠️ {{ $t('disclaimer.title') }}</h2>
      <p v-for="i in 4" :key="i" class="text-sm leading-7">{{ $t(`disclaimer.p${i}`) }}</p>
      <label class="flex items-start gap-2 text-sm font-bold">
        <input v-model="agreed" type="checkbox" class="mt-1 size-4 accent-brand-600" />
        <span>{{ $t('disclaimer.agree') }}</span>
      </label>
      <button class="btn w-full" :disabled="!agreed" @click="accept">{{ $t('disclaimer.continue') }}</button>
    </div>
  </div>
</template>
