<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Security</div>
      <h1 class="page-title">修改密码</h1>
      <p class="page-subtitle">修改完成后，请使用新密码重新登录账号。</p>
    </section>

    <section class="surface-card space-y-6">
      <ErrorRetryBox v-if="error">{{ error }}</ErrorRetryBox>
      <div v-else-if="success" class="info-box">{{ success }}</div>

      <div class="grid gap-4">
        <div class="grid gap-2">
          <label class="field-label">当前密码</label>
          <input v-model="currentPassword" type="password" class="field-input" placeholder="请输入当前密码" />
        </div>
        <div class="grid gap-2">
          <label class="field-label">新密码</label>
          <input v-model="newPassword" type="password" class="field-input" placeholder="请输入新密码" />
        </div>
        <div class="grid gap-2">
          <label class="field-label">确认新密码</label>
          <input v-model="confirmPassword" type="password" class="field-input" placeholder="请再次输入新密码" />
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="btn-primary" :disabled="saving" @click="handleSubmit">{{ saving ? '提交中...' : '确认修改' }}</button>
        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ErrorRetryBox from '@/components/common/ErrorRetryBox.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const saving = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  error.value = ''
  success.value = ''
  if (!currentPassword.value.trim()) {
    error.value = '请输入当前密码'
    return
  }
  if (newPassword.value.trim().length < 6) {
    error.value = '新密码长度不能少于6位'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    error.value = '两次输入的新密码不一致'
    return
  }

  try {
    saving.value = true
    await userStore.updatePassword(currentPassword.value, newPassword.value)
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    success.value = '密码修改成功'
  } catch (err) {
    error.value = err instanceof Error ? err.message : '修改失败，请稍后重试'
  } finally {
    saving.value = false
  }
}
</script>
