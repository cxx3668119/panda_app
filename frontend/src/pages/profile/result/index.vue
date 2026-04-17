<template>
  <main class="page" v-if="interpretation && profile">
    <InterpretationSummaryCard :title="interpretation.summaryTitle" :description="interpretation.advice" />

    <div class="actions mt-20">
      <RouterLink class="secondary-btn" to="/daily">查看今日日运</RouterLink>
      <RouterLink class="ghost-btn" to="/profile/create">修改出生信息</RouterLink>
      <RouterLink class="primary-btn" :to="profile.birthTimeUnknown ? '/profile/create' : '/ai/chat'">
        {{ profile.birthTimeUnknown ? '补充时辰后提问' : '去 AI 提问' }}
      </RouterLink>
    </div>

    <ErrorRetryBox v-if="profile.birthTimeUnknown" class="mt-16">
      未知时辰暂不支持 AI 提问，请补充时辰后再使用互动问答。
    </ErrorRetryBox>

    <InterpretationSection class="mt-20" title="性格特征" :content="interpretation.personality" />
    <InterpretationSection class="mt-16" title="优势能力" :content="interpretation.strength" />
    <InterpretationSection class="mt-16" title="风险提醒" :content="interpretation.risk" />
    <InterpretationSection class="mt-16" title="成长建议" :content="interpretation.advice" />
    <InterpretationSection class="mt-16" title="长文解读" :content="interpretation.fullContent" />
    <DisclaimerBlock class="mt-20" :text="interpretation.disclaimer" />
    <BottomNav />
  </main>

  <main v-else class="page">
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
