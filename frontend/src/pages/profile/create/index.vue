<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Create profile</div>
      <h1 class="page-title">创建你的命盘档案</h1>
      <p class="page-subtitle">填写基础出生信息后，即可生成首份命盘解读。</p>
    </section>

    <ProfileForm v-model="form" @submit="handleSubmit" />

    <div class="mt-4 space-y-4">
      <ErrorRetryBox v-if="error">
        {{ error }}
      </ErrorRetryBox>
      <LoadingState v-else-if="loading" text="正在生成命盘解读..." />
      <DisclaimerBlock text="出生时辰不确定也可以继续体验，但 AI 提问能力会受限。" />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ProfileForm from '@/components/profile/ProfileForm.vue'
import DisclaimerBlock from '@/components/common/DisclaimerBlock.vue'
import ErrorRetryBox from '@/components/common/ErrorRetryBox.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useProfileStore } from '@/stores/profile'
import type { UserProfile } from '@/types'

const router = useRouter()
const profileStore = useProfileStore()

const form = ref<UserProfile>({
  calendarType: 'SOLAR',
  birthDate: '1998-08-18',
  birthTime: '09:30',
  birthTimeUnknown: false,
  gender: 'FEMALE',
  birthPlace: '杭州',
  timezone: 'Asia/Shanghai'
})
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''

  if (!form.value.birthDate) {
    error.value = '请选择出生日期'
    return
  }
  if (!form.value.gender) {
    error.value = '请选择性别'
    return
  }
  if (!form.value.birthTimeUnknown && !form.value.birthTime) {
    error.value = '请选择出生时间，或开启未知时辰'
    return
  }

  try {
    loading.value = true
    await profileStore.submitProfile(form.value)
    router.push('/profile/result')
  } catch {
    error.value = '建档失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
