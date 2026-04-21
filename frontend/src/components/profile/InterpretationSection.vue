<template>
  <div class="surface-card space-y-3">
    <h3 class="section-title">{{ title }}</h3>
    <p class="text-sm leading-7 text-ink/85 sm:text-base">{{ content }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  content: string
}>()
</script>
