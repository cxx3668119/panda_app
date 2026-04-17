<template>
  <div class="card muted">{{ text }}</div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>
