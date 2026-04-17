<template>
  <main class="page" v-if="archive">
    <h1 class="page-title">成长档案</h1>
    <p class="page-subtitle">聚合你最近的日运与提问轨迹，帮助你回看关注主题。</p>

    <div class="hero-card">
      <div class="muted">阶段总结</div>
      <p class="mt-16">{{ archive.summary }}</p>
    </div>

    <div class="stats-grid mt-20">
      <div class="stat-card">
        <div class="muted">连续访问</div>
        <div class="score" style="font-size: 30px">{{ archive.streakDays }}</div>
      </div>
      <div class="stat-card">
        <div class="muted">关注关键词</div>
        <div class="section-title" style="margin: 8px 0 0">{{ archive.keywords.length }} 个</div>
      </div>
    </div>

    <div class="card mt-20">
      <h3 class="section-title">最近提问</h3>
      <div class="list">
        <div v-for="item in archive.recentQuestions" :key="item" class="list-item">{{ item }}</div>
      </div>
    </div>

    <div class="card mt-20">
      <h3 class="section-title">关注主题</h3>
      <div class="tag-list">
        <span v-for="item in archive.keywords" :key="item" class="tag">{{ item }}</span>
      </div>
    </div>

    <div class="card mt-20">
      <h3 class="section-title">最近日运</h3>
      <div class="list">
        <div v-for="item in archive.recentFortunes" :key="item.date" class="list-item">
          <div class="row space-between">
            <strong>{{ item.date }}</strong>
            <span>{{ item.score }}</span>
          </div>
          <div class="muted mt-16">{{ item.summary }}</div>
        </div>
      </div>
    </div>

    <BottomNav />
  </main>

  <main v-else class="page">
    <LoadingState text="正在加载成长档案..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useGrowthStore } from '@/stores/growth'

const growthStore = useGrowthStore()
const archive = computed(() => growthStore.archive)

onMounted(async () => {
  if (!growthStore.archive) {
    await growthStore.loadArchive()
  }
})
</script>
