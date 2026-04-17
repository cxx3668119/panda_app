import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { askAi, fetchQuota, fetchTodaySession } from '@/api/chat'
import type { ChatMessage, QuotaData } from '@/types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const quota = ref<QuotaData | null>(null)
  const loading = ref(false)

  const remainCount = computed(() => {
    if (!quota.value) return 0
    return quota.value.freeLimit - quota.value.freeUsed + quota.value.paidBalance
  })

  async function loadSession() {
    messages.value = await fetchTodaySession()
    quota.value = await fetchQuota()
  }

  async function sendQuestion(question: string) {
    loading.value = true
    messages.value.push({ id: Date.now(), role: 'user', content: question })
    const answer = await askAi(question)
    messages.value.push(answer)
    if (quota.value && !answer.rejected) {
      if (quota.value.freeUsed < quota.value.freeLimit) {
        quota.value.freeUsed += 1
      } else if (quota.value.paidBalance > 0) {
        quota.value.paidBalance -= 1
      }
    }
    loading.value = false
  }

  return {
    messages,
    quota,
    loading,
    remainCount,
    loadSession,
    sendQuestion
  }
})
