<template>
  <div class="card">
    <h3 class="section-title">快捷问题</h3>
    <div class="actions">
      <button v-for="item in questions" :key="item" class="ghost-btn" @click="$emit('select', item)">
        {{ item }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  questions: string[]
}>()

defineEmits<{
  (e: 'select', value: string): void
}>()
</script>
