<template>
  <div class="surface-card">
    <div class="flex items-start justify-between gap-4">
      <div class="space-y-1">
        <div class="eyebrow">剩余提问次数</div>
        <div class="font-sans text-4xl font-semibold leading-none text-accent">{{ remain }}</div>
      </div>
      <div class="text-right text-sm leading-6 text-muted">免费 {{ quota.freeLimit - quota.freeUsed }} / 付费 {{ quota.paidBalance }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { QuotaData } from '@/types'

defineProps<{
  remain: number
  quota: QuotaData
}>()
</script>
