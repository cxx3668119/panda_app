<template>
  <div class="hero-card">
    <div class="muted">命盘摘要</div>
    <h2 class="page-title" style="font-size: 24px">{{ title }}</h2>
    <p class="page-subtitle">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
