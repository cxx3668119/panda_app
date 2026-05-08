<template>
  <main v-if="form" class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Account profile</div>
      <h1 class="page-title">账号信息</h1>
      <p class="page-subtitle">维护昵称、邮箱、手机号和时区。</p>
    </section>

    <section class="surface-card space-y-6">
      <div class="flex items-center gap-4 rounded-[24px] border border-line/70 bg-white/70 p-4">
        <img
          :src="userStore.user?.avatarUrl || '/panda-badge.png'"
          alt="头像预览"
          class="h-20 w-20 rounded-[28px] border border-line/70 bg-white/85 object-cover p-1 shadow-soft"
        />
        <div class="text-sm leading-6 text-muted">当前环境暂未启用头像上传，账号资料可先正常维护。</div>
      </div>

      <ErrorRetryBox v-if="error">{{ error }}</ErrorRetryBox>
      <div v-else-if="success" class="info-box">{{ success }}</div>

      <div class="grid gap-4">
        <div class="grid gap-2">
          <label class="field-label">昵称</label>
          <input v-model="form.nickname" class="field-input" maxlength="32" placeholder="请输入昵称" />
        </div>
        <div class="grid gap-2">
          <label class="field-label">邮箱</label>
          <input v-model="form.email" type="email" class="field-input" placeholder="请输入邮箱" />
        </div>
        <div class="grid gap-2">
          <label class="field-label">手机号</label>
          <input v-model="mobileValue" class="field-input" placeholder="请输入手机号" />
        </div>
        <div class="grid gap-2">
          <label class="field-label">时区</label>
          <input v-model="form.timezone" class="field-input" placeholder="如 Asia/Shanghai" />
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="btn-primary" :disabled="saving" @click="handleSave">{{ saving ? '保存中...' : '保存信息' }}</button>
        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div>
    </section>
  </main>

  <main v-else class="page-shell">
    <LoadingState text="正在加载账号信息..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import ErrorRetryBox from '@/components/common/ErrorRetryBox.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useUserStore } from '@/stores/user'
import type { AccountUpdatePayload } from '@/types'

const userStore = useUserStore()
const form = ref<AccountUpdatePayload | null>(null)
const saving = ref(false)
const error = ref('')
const success = ref('')

const mobileValue = computed({
  get: () => form.value?.mobile || '',
  set: (value: string) => {
    if (!form.value) return
    form.value.mobile = value
  }
})

onMounted(async () => {
  if (!userStore.user) {
    await userStore.loadMe()
  }
  if (!userStore.user) return
  form.value = {
    nickname: userStore.user.nickname,
    email: userStore.user.email,
    mobile: userStore.user.mobile,
    timezone: userStore.user.timezone
  }
})

async function handleSave() {
  if (!form.value) return
  error.value = ''
  success.value = ''
  if (!form.value.nickname.trim()) {
    error.value = '请输入昵称'
    return
  }
  if (!/.+@.+\..+/.test(form.value.email)) {
    error.value = '请输入有效邮箱地址'
    return
  }
  if (!form.value.timezone.trim()) {
    error.value = '请输入时区'
    return
  }

  try {
    saving.value = true
    const result = await userStore.updateMe({
      ...form.value,
      nickname: form.value.nickname.trim(),
      email: form.value.email.trim(),
      mobile: form.value.mobile?.trim() || null,
      timezone: form.value.timezone.trim()
    })
    form.value = {
      nickname: result.nickname,
      email: result.email,
      mobile: result.mobile,
      timezone: result.timezone
    }
    success.value = '账号信息已更新'
  } catch (err) {
    error.value = err instanceof Error ? err.message : '保存失败，请稍后重试'
  } finally {
    saving.value = false
  }
}
</script>
