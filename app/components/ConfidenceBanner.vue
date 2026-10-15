<script setup lang="ts">
defineProps<{ compact?: boolean }>()
</script>

<template>
  <div class="rounded-xl border-2 border-red-400 bg-red-50 p-3 text-red-800 dark:border-red-700 dark:bg-red-950/70 dark:text-red-200" role="alert">
    <p class="font-semibold">⚠️ {{ $t('confidence.title') }}</p>
    <p v-if="!compact" class="mt-1 text-sm leading-7">{{ $t('confidence.body') }}</p>
  </div>
</template>
