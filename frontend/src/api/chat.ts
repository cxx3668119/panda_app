import { ApiError, get, getApiBaseUrl, getAuthToken, post } from '@/api/client'
import type { ChatMessage, QuotaData } from '@/types'

function waitForPaint() {
  return new Promise<void>((resolve) => {
    if (typeof requestAnimationFrame === 'function') {
      requestAnimationFrame(() => resolve())
      return
    }
    setTimeout(() => resolve(), 0)
  })
}

function createSseReader(onChunk: (chunk: string) => void) {
  const decoder = new TextDecoder('utf-8')
  let buffer = ''

  return {
    async push(value: Uint8Array) {
      buffer += decoder.decode(value, { stream: true })
      let chunkHandled = false

      while (true) {
        const separatorIndex = buffer.indexOf('\n\n')
        if (separatorIndex === -1) break

        const rawEvent = buffer.slice(0, separatorIndex).trim()
        buffer = buffer.slice(separatorIndex + 2)

        if (!rawEvent) continue

        const dataLine = rawEvent.split('\n').find((line) => line.startsWith('data: '))
        if (!dataLine) continue

        try {
          const payload = JSON.parse(dataLine.slice(6)) as { type: string; content: string }
          if (payload.type === 'delta' && payload.content) {
            onChunk(payload.content)
            chunkHandled = true
          }
        } catch {
          // ignore malformed event chunk
        }
      }

      if (chunkHandled) {
        await waitForPaint()
      }
    },
  }
}

export async function fetchQuota() {
  return get<QuotaData>('/ai/quota')
}

export async function fetchTodaySession() {
  return get<ChatMessage[]>('/ai/chat/session')
}

export async function askAi(question: string): Promise<ChatMessage> {
  return post<ChatMessage>('/ai/chat/ask', { question })
}

export async function streamIntro(onChunk: (chunk: string) => void) {
  const token = getAuthToken()
  const response = await fetch(`${getApiBaseUrl()}/ai/chat/intro/stream`, {
    method: 'GET',
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })

  if (!response.ok) {
    let message = '请求失败，请稍后重试'
    try {
      const result = await response.json()
      message = result?.message || message
    } catch {
      try {
        const text = await response.text()
        if (text) message = text
      } catch {
        // ignore
      }
    }
    throw new ApiError(message, response.status)
  }

  const reader = response.body?.getReader()
  if (!reader) {
    throw new ApiError('流式响应不可用，请稍后重试', response.status)
  }

  const sseReader = createSseReader(onChunk)
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    if (value) await sseReader.push(value)
  }
}

export async function askAiStream(question: string, onChunk: (chunk: string) => void) {
  const token = getAuthToken()
  const response = await fetch(`${getApiBaseUrl()}/ai/chat/ask/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ question }),
  })

  if (!response.ok) {
    let message = '请求失败，请稍后重试'
    try {
      const result = await response.json()
      message = result?.message || message
    } catch {
      try {
        const text = await response.text()
        if (text) message = text
      } catch {
        // ignore
      }
    }
    throw new ApiError(message, response.status)
  }

  const reader = response.body?.getReader()
  if (!reader) {
    throw new ApiError('流式响应不可用，请稍后重试', response.status)
  }

  const sseReader = createSseReader(onChunk)
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    if (value) await sseReader.push(value)
  }
}
