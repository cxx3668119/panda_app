<template>
  <div class="hero-card">
    <div class="row space-between">
      <div>
        <div class="muted">{{ data.date }}</div>
        <h2 class="page-title" style="font-size: 24px">{{ data.scoreLabel }}</h2>
      </div>
      <div class="score">{{ data.score }}</div>
    </div>
    <div class="tag-list mt-16">
      <span v-for="keyword in data.keywords" :key="keyword" class="tag">{{ keyword }}</span>
    </div>
    <p class="page-subtitle mt-16">{{ data.summary }}</p>
  </div>
</template>

<script setup lang="ts">
import type { DailyFortuneData } from '@/types'

defineProps<{
  data: DailyFortuneData
}>()
</script>
