<template>
  <div class="surface-hero space-y-3">
    <div class="eyebrow">命盘摘要</div>
    <h2 class="font-serif text-3xl leading-tight text-ink sm:text-[2rem]">{{ title }}</h2>
    <p class="max-w-2xl text-sm leading-7 text-muted sm:text-base">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
