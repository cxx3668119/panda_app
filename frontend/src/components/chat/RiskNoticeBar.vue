<template>
  <div class="context-bar">
    {{ text }}
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>
