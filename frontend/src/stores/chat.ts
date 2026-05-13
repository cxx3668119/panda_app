import { defineStore } from 'pinia'
import { ref } from 'vue'
import { askAiStream, fetchTodaySession, streamIntro } from '@/api/chat'
import type { ChatMessage } from '@/types'

const DISCLAIMER_TEXT =
  '本内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议，请结合实际情况独立判断。'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const loading = ref(false)

  function touchMessages() {
    messages.value = [...messages.value]
  }

  async function loadSession() {
    messages.value = await fetchTodaySession()
  }

  async function streamIntroIfNeeded() {
    if (messages.value.length > 0) return

    loading.value = true
    const assistantMessage: ChatMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: '',
      disclaimer: undefined,
      rejected: false,
    }
    messages.value.push(assistantMessage)
    touchMessages()

    try {
      await streamIntro((chunk) => {
        assistantMessage.content += chunk
        touchMessages()
      })
      assistantMessage.disclaimer = DISCLAIMER_TEXT
      touchMessages()
    } catch (error) {
      messages.value.pop()
      touchMessages()
      throw error
    } finally {
      loading.value = false
    }
  }

  async function sendQuestion(question: string) {
    loading.value = true
    const rejectedLikely = question.includes('投资')
    messages.value.push({ id: Date.now(), role: 'user', content: question })

    const assistantMessage: ChatMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: '',
      disclaimer: undefined,
      rejected: false,
    }
    messages.value.push(assistantMessage)
    touchMessages()

    try {
      await askAiStream(question, (chunk) => {
        assistantMessage.content += chunk
        touchMessages()
      })

      assistantMessage.disclaimer = DISCLAIMER_TEXT
      assistantMessage.rejected = rejectedLikely
      touchMessages()
    } catch (error) {
      messages.value.pop()
      touchMessages()
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    messages,
    loading,
    loadSession,
    streamIntroIfNeeded,
    sendQuestion,
  }
})
