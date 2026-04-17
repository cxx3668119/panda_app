<template>
  <main class="page" v-if="quota">
    <h1 class="page-title">AI 问答</h1>
    <p class="page-subtitle">基于当天命盘与日运上下文，为你提供克制、启发式的建议。</p>

    <RiskNoticeBar text="当前回答仅结合你当天的命盘与日运上下文生成。" />
    <QuestionQuotaBar class="mt-16" :remain="remainCount" :quota="quota" />
    <QuestionQuickActions class="mt-16" :questions="quickQuestions" @select="question = $event" />
    <ChatMessageList class="mt-16" :messages="messages" />

    <div class="card chat-input mt-16">
      <textarea v-model="question" rows="4" placeholder="请输入你今天最想追问的问题"></textarea>
      <div class="actions">
        <button class="primary-btn" :disabled="chatStore.loading" @click="handleSend">发送问题</button>
      </div>
    </div>

    <PurchaseQuotaModal v-if="remainCount <= 0" class="mt-16" />
    <DisclaimerBlock class="mt-16" text="高风险方向会触发边界提示；投资类问题会直接拒答。" />
    <BottomNav />
  </main>

  <main v-else class="page">
    <LoadingState text="正在加载当日问答上下文..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import DisclaimerBlock from '@/components/common/DisclaimerBlock.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import ChatMessageList from '@/components/chat/ChatMessageList.vue'
import PurchaseQuotaModal from '@/components/chat/PurchaseQuotaModal.vue'
import QuestionQuickActions from '@/components/chat/QuestionQuickActions.vue'
import QuestionQuotaBar from '@/components/chat/QuestionQuotaBar.vue'
import RiskNoticeBar from '@/components/chat/RiskNoticeBar.vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const question = ref('')
const quickQuestions = [
  '今天适合做需求汇报吗？',
  '今天适合推进跨团队协作吗？',
  '我今天更适合沟通还是独立思考？',
  '今天适合做关键决策吗？'
]

const quota = computed(() => chatStore.quota)
const remainCount = computed(() => chatStore.remainCount)
const messages = computed(() => chatStore.messages)

onMounted(async () => {
  if (!chatStore.quota || !chatStore.messages.length) {
    await chatStore.loadSession()
  }
})

async function handleSend() {
  if (!question.value.trim()) return
  if (remainCount.value <= 0) return

  const currentQuestion = question.value.trim()
  question.value = ''
  await chatStore.sendQuestion(currentQuestion)
}
</script>
