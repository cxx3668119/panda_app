<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Archive</div>
      <h1 class="page-title">历史日运</h1>
      <p class="page-subtitle">按日期回顾每日状态与建议，当前版本为只读查看。</p>
    </section>

    <div v-if="history.length" class="grid gap-4">
      <div v-for="item in history" :key="item.date" class="surface-card space-y-4">
        <div class="flex items-start justify-between gap-4">
          <div class="space-y-1">
            <div class="eyebrow">{{ item.date }}</div>
            <div class="section-title !mb-0">{{ item.scoreLabel }}</div>
          </div>
          <div class="font-sans text-4xl font-semibold leading-none text-accent">{{ item.score }}</div>
        </div>
        <p class="text-sm leading-7 text-muted sm:text-base">{{ item.summary }}</p>
        <div class="flex flex-wrap gap-2">
          <span v-for="keyword in item.keywords" :key="keyword" class="chip">{{ keyword }}</span>
        </div>
      </div>
    </div>

    <LoadingState v-else text="正在加载历史日运..." />
    <BottomNav />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useDailyFortuneStore } from '@/stores/dailyFortune'

const dailyFortuneStore = useDailyFortuneStore()
const history = computed(() => dailyFortuneStore.history)

onMounted(async () => {
  if (!dailyFortuneStore.history.length) {
    await dailyFortuneStore.loadHistory()
  }
})
</script>
