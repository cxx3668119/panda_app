<template>
  <div class="section-card">
    <h3 class="section-title">今日详细建议</h3>
    <div class="list">
      <div class="list-item"><strong>宜做：</strong>{{ data.suitable }}</div>
      <div class="list-item"><strong>谨慎：</strong>{{ data.caution }}</div>
      <div class="list-item"><strong>行动建议：</strong>{{ data.actionAdvice }}</div>
      <div class="list-item"><strong>长文详情：</strong>{{ data.detail }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DailyFortuneData } from '@/types'

defineProps<{
  data: DailyFortuneData
}>()
</script>
