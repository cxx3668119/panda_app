<template>
  <div class="surface-card grid gap-3">
    <div
      v-for="message in messages"
      :key="message.id"
      :class="message.role === 'user'
        ? 'ml-auto max-w-[88%] rounded-[24px] bg-accent px-4 py-3 text-sm leading-7 text-white shadow-glow'
        : 'max-w-[88%] rounded-[24px] border border-line/80 bg-cream px-4 py-3 text-sm leading-7 text-ink shadow-soft'"
    >
      <div v-if="message.role !== 'user'" class="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-muted">
        <img alt="熊猫助手" class="h-6 w-6 rounded-full border border-line/70 bg-white/80 p-1" src="/panda-badge.png" />
        Panda guide
      </div>
      <div>{{ message.content }}</div>
      <div v-if="message.disclaimer" :class="message.role === 'user' ? 'mt-3 text-xs text-white/80' : 'mt-3 text-xs text-muted'">
        {{ message.disclaimer }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/types'

defineProps<{
  messages: ChatMessage[]
}>()
</script>
