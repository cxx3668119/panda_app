<template>
  <div class="surface-card text-sm leading-7 text-muted">{{ text }}</div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>
