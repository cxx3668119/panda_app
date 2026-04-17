<template>
  <div class="card">
    <h3 class="section-title">邮箱验证码登录</h3>
    <div class="field">
      <label>邮箱</label>
      <input :value="email" type="email" placeholder="请输入邮箱" @input="$emit('update:email', ($event.target as HTMLInputElement).value)" />
    </div>
    <div class="field mt-16">
      <label>验证码</label>
      <input :value="code" placeholder="请输入验证码" @input="$emit('update:code', ($event.target as HTMLInputElement).value)" />
    </div>
    <div class="actions mt-16">
      <button class="secondary-btn" @click="$emit('send-code')">获取验证码</button>
      <button class="primary-btn" @click="$emit('submit')">登录</button>
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
