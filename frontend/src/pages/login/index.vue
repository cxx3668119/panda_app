<template>
  <main class="page-shell">
    <section class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
      <div class="page-hero pt-2 lg:pt-10">
        <div class="eyebrow">Bazi companion</div>
        <h1 class="page-title">AI 八字算命助手</h1>
        <p class="page-subtitle">先用邮箱验证码登录，开始你的命盘解读、今日日运与陪伴式问答体验。</p>
      </div>

      <div class="space-y-4">
        <AuthEmailForm
          :email="email"
          :code="code"
          @update:email="email = $event"
          @update:code="code = $event"
          @send-code="handleSendCode"
          @submit="handleLogin"
        />

        <ErrorRetryBox v-if="error">
          {{ error }}
        </ErrorRetryBox>
        <LoadingState v-else-if="loading" text="正在登录..." />

        <DisclaimerBlock text="本产品内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议。" />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthEmailForm from '@/components/auth/AuthEmailForm.vue'
import DisclaimerBlock from '@/components/common/DisclaimerBlock.vue'
import ErrorRetryBox from '@/components/common/ErrorRetryBox.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { sendEmailCode } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const email = ref('demo@example.com')
const code = ref('123456')
const loading = ref(false)
const error = ref('')

async function handleSendCode() {
  error.value = ''
  if (!email.value.trim() || !/.+@.+\..+/.test(email.value)) {
    error.value = '请输入有效邮箱地址'
    return
  }

  try {
    loading.value = true
    await sendEmailCode(email.value)
  } catch {
    error.value = '验证码发送失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

async function handleLogin() {
  error.value = ''
  if (!email.value.trim() || !/.+@.+\..+/.test(email.value)) {
    error.value = '请输入有效邮箱地址'
    return
  }
  if (!code.value.trim()) {
    error.value = '请输入验证码'
    return
  }

  try {
    loading.value = true
    const result = await userStore.login(email.value, code.value)
    router.push(result.hasProfile ? '/daily' : '/profile/create')
  } catch {
    error.value = '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
