<template>
  <main class="page" v-if="today">
    <h1 class="page-title">今日日运</h1>
    <p class="page-subtitle">你的每日状态会按当天上下文固定生成，适合反复查看与回顾。</p>

    <DailyFortuneCard :data="today" />
    <DailyFortuneDetail class="mt-20" :data="today" />

    <div class="actions mt-20">
      <RouterLink class="primary-btn" to="/ai/chat">发起 AI 提问</RouterLink>
      <button class="ghost-btn" type="button">分享（预埋）</button>
      <RouterLink class="secondary-btn" to="/daily/history">查看历史日运</RouterLink>
    </div>

    <BottomNav />
  </main>

  <main v-else class="page">
    <LoadingState text="正在生成今日日运..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import DailyFortuneCard from '@/components/daily/DailyFortuneCard.vue'
import DailyFortuneDetail from '@/components/daily/DailyFortuneDetail.vue'
import { useDailyFortuneStore } from '@/stores/dailyFortune'

const dailyFortuneStore = useDailyFortuneStore()
const today = computed(() => dailyFortuneStore.today)

onMounted(async () => {
  if (!dailyFortuneStore.today) {
    await dailyFortuneStore.loadToday()
  }
})
</script>
