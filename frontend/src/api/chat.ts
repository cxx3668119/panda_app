import { get, post } from '@/api/client'
import type { ChatMessage, QuotaData } from '@/types'

export async function fetchQuota() {
  return get<QuotaData>('/ai/quota')
}

export async function fetchTodaySession() {
  return get<ChatMessage[]>('/ai/chat/session/today')
}

export async function askAi(question: string): Promise<ChatMessage> {
  return post<ChatMessage>('/ai/chat/ask', { question })
}
