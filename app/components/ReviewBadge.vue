<script setup lang="ts">
defineProps<{ status: 'verified' | 'unverified'; small?: boolean }>()
</script>
<template>
  <span class="inline-flex shrink-0 items-center rounded-full font-bold"
    :class="[small ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs',
      status === 'verified' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200' : 'bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200']">
    {{ status === 'verified' ? '✓ ' + $t('review.verified') : '⚠ ' + $t('review.unverified') }}
  </span>
</template>
