<template>
  <main v-if="today" class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Daily reading</div>
      <h1 class="page-title">今日运势</h1>
      <p class="page-subtitle">你的每日状态会按当天上下文固定生成，适合反复查看与回顾。</p>
    </section>

    <DailyFortuneCard :data="today" />
    <DailyFortuneDetail class="mt-6" :data="today" />

    <div class="mt-6 flex flex-wrap gap-3">
      <RouterLink class="btn-primary" to="/ai/chat">发起 AI 提问</RouterLink>
      <!-- <button class="btn-ghost" type="button">分享（预埋）</button> -->
      <RouterLink class="btn-secondary" to="/daily/history">查看历史日运</RouterLink>
    </div>

    <BottomNav />
  </main>

  <main v-else class="page-shell">
    <LoadingState text="正在生成今日运势..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import DailyFortuneCard from '@/components/daily/DailyFortuneCard.vue'
import DailyFortuneDetail from '@/components/daily/DailyFortuneDetail.vue'
import { useDailyFortuneStore } from '@/stores/dailyFortune'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const dailyFortuneStore = useDailyFortuneStore()
const today = computed(() => dailyFortuneStore.today)

onMounted(async () => {
  if (!dailyFortuneStore.today) {
    await dailyFortuneStore.loadToday()
  }
  console.log(userStore);
  
})
</script>
