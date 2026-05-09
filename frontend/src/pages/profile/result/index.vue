<template>
  <main v-if="interpretation && profile" class="page-shell">
    <InterpretationSummaryCard :title="interpretation.summaryTitle" :description="interpretation.advice" />

    <div class="mt-6 flex flex-wrap gap-3">
      <RouterLink class="btn-secondary" to="/daily">查看今日运势</RouterLink>
      <RouterLink class="btn-ghost" to="/profile/create">修改出生信息</RouterLink>
      <RouterLink class="btn-primary" :to="profile.birthTimeUnknown ? '/profile/create' : '/ai/chat'">
        {{ profile.birthTimeUnknown ? '补充时辰后提问' : '去 AI 提问' }}
      </RouterLink>
    </div>

    <ErrorRetryBox v-if="profile.birthTimeUnknown" class="mt-4">
      未知时辰暂不支持 AI 提问，请补充时辰后再使用互动问答。
    </ErrorRetryBox>

    <InterpretationSection class="mt-6" title="性格特征" :content="interpretation.personality" />
    <InterpretationSection class="mt-4" title="优势能力" :content="interpretation.strength" />
    <InterpretationSection class="mt-4" title="风险提醒" :content="interpretation.risk" />
    <InterpretationSection class="mt-4" title="成长建议" :content="interpretation.advice" />
    <InterpretationSection class="mt-4" title="长文解读" :content="interpretation.fullContent" />
    <div class="mt-6">
      <DisclaimerBlock :text="interpretation.disclaimer" />
    </div>
    <BottomNav />
  </main>

  <main v-else class="page-shell">
    <LoadingState text="正在加载命盘解读..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import DisclaimerBlock from '@/components/common/DisclaimerBlock.vue'
import ErrorRetryBox from '@/components/common/ErrorRetryBox.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import InterpretationSection from '@/components/profile/InterpretationSection.vue'
import InterpretationSummaryCard from '@/components/profile/InterpretationSummaryCard.vue'
import { useProfileStore } from '@/stores/profile'

const profileStore = useProfileStore()

const profile = computed(() => profileStore.profile)
const interpretation = computed(() => profileStore.interpretation)

onMounted(async () => {
  if (!profileStore.profile || !profileStore.interpretation) {
    await profileStore.loadProfile()
  }
})
</script>
