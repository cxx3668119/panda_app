<template>
  <main class="page-shell" v-if="archive">
    <section class="page-hero">
      <div class="eyebrow">Growth archive</div>
      <h1 class="page-title">成长档案</h1>
      <p class="page-subtitle">聚合你最近的日运与提问轨迹，帮助你回看关注主题。</p>
    </section>

    <section class="surface-hero">
      <div class="eyebrow">阶段总结</div>
      <p class="mt-4 text-base leading-7 text-ink/85 sm:text-lg">{{ archive.summary }}</p>
    </section>

    <section class="mt-6 grid gap-4 sm:grid-cols-2">
      <div class="surface-card">
        <div class="eyebrow">连续访问</div>
        <div class="mt-3 text-4xl font-serif text-ink">{{ archive.streakDays }}</div>
      </div>
      <div class="surface-card">
        <div class="eyebrow">关注关键词</div>
        <div class="mt-3 text-2xl font-semibold tracking-tight text-ink">{{ archive.keywords.length }} 个</div>
      </div>
    </section>

    <section class="surface-card mt-6">
      <h3 class="section-title">最近提问</h3>
      <div class="mt-4 space-y-3">
        <div
          v-for="item in archive.recentQuestions"
          :key="item"
          class="rounded-2xl border border-line/70 bg-white/70 px-4 py-3 text-sm leading-6 text-ink/85"
        >
          {{ item }}
        </div>
      </div>
    </section>

    <section class="surface-card mt-6">
      <h3 class="section-title">关注主题</h3>
      <div class="mt-4 flex flex-wrap gap-2.5">
        <span v-for="item in archive.keywords" :key="item" class="chip">{{ item }}</span>
      </div>
    </section>

    <section class="surface-card mt-6">
      <h3 class="section-title">最近日运</h3>
      <div class="mt-4 space-y-3">
        <div
          v-for="item in archive.recentFortunes"
          :key="item.date"
          class="rounded-[22px] border border-line/70 bg-white/70 p-4"
        >
          <div class="flex items-center justify-between gap-3">
            <strong class="text-sm font-semibold text-ink">{{ item.date }}</strong>
            <span class="chip">{{ item.score }}</span>
          </div>
          <div class="mt-3 text-sm leading-6 text-muted">{{ item.summary }}</div>
        </div>
      </div>
    </section>

    <BottomNav />
  </main>

  <main v-else class="page-shell">
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
