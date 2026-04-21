<template>
  <div class="surface-card grid gap-3">
    <div
      v-for="message in messages"
      :key="message.id"
      :class="message.role === 'user'
        ? 'ml-auto max-w-[88%] rounded-[24px] bg-accent px-4 py-3 text-sm leading-7 text-white shadow-glow'
        : 'max-w-[88%] rounded-[24px] bg-cream px-4 py-3 text-sm leading-7 text-ink'"
    >
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
