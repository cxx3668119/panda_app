<template>
  <div class="surface-card space-y-4">
    <h3 class="section-title">快捷问题</h3>
    <div class="flex flex-wrap gap-3">
      <button
        v-for="item in questions"
        :key="item"
        class="btn-ghost text-left"
        @click="$emit('select', item)"
      >
        {{ item }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  questions: string[];
}>();

defineEmits<{
  (e: "select", value: string): void;
}>();
</script>
