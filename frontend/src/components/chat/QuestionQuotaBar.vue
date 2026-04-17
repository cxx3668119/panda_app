<template>
  <div class="card">
    <div class="row space-between">
      <div>
        <div class="muted">剩余提问次数</div>
        <div class="score" style="font-size: 28px">{{ remain }}</div>
      </div>
      <div class="muted">免费 {{ quota.freeLimit - quota.freeUsed }} / 付费 {{ quota.paidBalance }}</div>
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
