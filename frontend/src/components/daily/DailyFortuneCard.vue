<template>
  <div class="surface-hero space-y-5">
    <div class="flex items-start justify-between gap-4">
      <div class="space-y-2">
        <div class="eyebrow">{{ data.date }}</div>
        <h2 class="font-serif text-3xl leading-tight text-ink sm:text-[2rem]">{{ data.scoreLabel }}</h2>
      </div>
      <div class="font-sans text-5xl font-semibold leading-none text-accent">{{ data.score }}</div>
    </div>
    <div class="flex flex-wrap gap-2">
      <span v-for="keyword in data.keywords" :key="keyword" class="chip">{{ keyword }}</span>
    </div>
    <p class="max-w-2xl text-sm leading-7 text-muted sm:text-base">{{ data.summary }}</p>
  </div>
</template>

<script setup lang="ts">
import type { DailyFortuneData } from '@/types'

defineProps<{
  data: DailyFortuneData
}>()
</script>
