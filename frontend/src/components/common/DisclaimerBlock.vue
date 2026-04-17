<template>
  <div class="disclaimer">
    {{ text }}
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>
