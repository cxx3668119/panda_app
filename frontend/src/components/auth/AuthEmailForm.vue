<template>
  <div class="surface-card panda-panel space-y-5">
    <div class="flex items-start justify-between gap-3">
      <div class="space-y-2">
        <div class="eyebrow">Welcome back</div>
        <h3 class="section-title">邮箱验证码登录</h3>
      </div>
      <img alt="熊猫徽章" class="h-12 w-12 rounded-2xl border border-line/70 bg-white/85 p-2 shadow-soft" src="/panda-badge.svg" />
    </div>

    <div class="grid gap-4">
      <div class="grid gap-2">
        <label class="field-label">邮箱</label>
        <input class="field-input" :value="email" type="email" placeholder="请输入邮箱" @input="$emit('update:email', ($event.target as HTMLInputElement).value)" />
      </div>
      <div class="grid gap-2">
        <label class="field-label">验证码</label>
        <input class="field-input" :value="code" placeholder="请输入验证码" @input="$emit('update:code', ($event.target as HTMLInputElement).value)" />
      </div>
    </div>

    <div class="flex flex-wrap gap-3">
      <button class="btn-secondary" @click="$emit('send-code')">获取验证码</button>
      <button class="btn-primary" @click="$emit('submit')">登录</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  email: string
  code: string
}>()

defineEmits<{
  (e: 'update:email', value: string): void
  (e: 'update:code', value: string): void
  (e: 'send-code'): void
  (e: 'submit'): void
}>()
</script>
