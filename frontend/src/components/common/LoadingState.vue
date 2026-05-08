<template>
  <div class="surface-card panda-panel flex items-center gap-4 text-sm leading-7 text-muted">
    <img alt="熊猫等待中" class="h-14 w-14 rounded-[20px] border border-line/70 bg-white/80 p-2 shadow-soft" src="/panda-badge.png" />
    <div>
      <div class="font-sans text-sm font-semibold text-ink/90">熊猫正在整理今日内容</div>
      <div>{{ text }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>
