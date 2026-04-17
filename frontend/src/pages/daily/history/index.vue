<template>
  <main class="page">
    <h1 class="page-title">历史日运</h1>
    <p class="page-subtitle">按日期回顾每日状态与建议，当前版本为只读查看。</p>

    <div v-if="history.length" class="list">
      <div v-for="item in history" :key="item.date" class="card">
        <div class="row space-between">
          <div>
            <div class="muted">{{ item.date }}</div>
            <div class="section-title" style="margin: 4px 0 0">{{ item.scoreLabel }}</div>
          </div>
          <div class="score" style="font-size: 32px">{{ item.score }}</div>
        </div>
        <p class="page-subtitle mt-16">{{ item.summary }}</p>
        <div class="tag-list">
          <span v-for="keyword in item.keywords" :key="keyword" class="tag">{{ keyword }}</span>
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
