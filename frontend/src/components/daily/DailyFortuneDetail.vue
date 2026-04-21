<template>
  <div class="surface-card space-y-4">
    <h3 class="section-title">今日详细建议</h3>
    <div class="grid gap-3">
      <div class="rounded-2xl bg-cream px-4 py-4 text-sm leading-7 text-ink"><strong>宜做：</strong>{{ data.suitable }}</div>
      <div class="rounded-2xl bg-cream px-4 py-4 text-sm leading-7 text-ink"><strong>谨慎：</strong>{{ data.caution }}</div>
      <div class="rounded-2xl bg-cream px-4 py-4 text-sm leading-7 text-ink"><strong>行动建议：</strong>{{ data.actionAdvice }}</div>
      <div class="rounded-2xl bg-cream px-4 py-4 text-sm leading-7 text-ink"><strong>长文详情：</strong>{{ data.detail }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DailyFortuneData } from '@/types'

defineProps<{
  data: DailyFortuneData
}>()
</script>
