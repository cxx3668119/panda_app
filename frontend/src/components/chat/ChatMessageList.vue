<template>
  <div class="card list">
    <div v-for="message in messages" :key="message.id" class="chat-bubble" :class="message.role === 'user' ? 'user' : 'assistant'">
      <div>{{ message.content }}</div>
      <div v-if="message.disclaimer" class="helper-text mt-16">{{ message.disclaimer }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/types'

defineProps<{
  messages: ChatMessage[]
}>()
</script>
