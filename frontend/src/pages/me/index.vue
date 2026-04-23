<template>
  <main v-if="user" class="page-shell">
    <section class="surface-hero panda-panel">
      <div class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-4">
          <img
            :src="avatarSrc"
            alt="用户头像"
            class="h-20 w-20 rounded-[28px] border border-line/70 bg-white/85 object-cover p-1 shadow-soft"
          />
          <div class="space-y-2">
            <div class="eyebrow">My account</div>
            <div>
              <h1 class="page-title !max-w-none !text-3xl sm:!text-4xl">{{ user.nickname }}</h1>
              <p class="page-subtitle">{{ user.email }}</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <span class="chip">{{ statusText }}</span>
              <span class="chip">{{ user.timezone }}</span>
            </div>
          </div>
        </div>
        <RouterLink class="btn-secondary" to="/me/account">编辑账号信息</RouterLink>
      </div>
    </section>

    <section class="mt-6 grid gap-4">
      <RouterLink class="surface-card flex items-center justify-between gap-4" to="/me/account">
        <div class="space-y-1">
          <div class="section-title">账号信息</div>
          <div class="text-sm leading-6 text-muted">维护昵称、邮箱、手机号和时区，并更新头像。</div>
        </div>
        <span class="text-xl text-muted">›</span>
      </RouterLink>

      <RouterLink class="surface-card flex items-center justify-between gap-4" to="/me/password">
        <div class="space-y-1">
          <div class="section-title">修改密码</div>
          <div class="text-sm leading-6 text-muted">更新登录密码，后续使用新密码重新登录。</div>
        </div>
        <span class="text-xl text-muted">›</span>
      </RouterLink>

      <RouterLink class="surface-card flex items-center justify-between gap-4" to="/me/settings/reminder">
        <div class="space-y-1">
          <div class="section-title">提醒设置</div>
          <div class="text-sm leading-6 text-muted">管理日运提醒开关、时间和时区。</div>
        </div>
        <span class="text-xl text-muted">›</span>
      </RouterLink>
    </section>

    <section class="mt-6 surface-card space-y-4">
      <div>
        <div class="section-title">账号概览</div>
        <div class="mt-3 grid gap-3 sm:grid-cols-2">
          <div class="rounded-2xl border border-line/70 bg-white/70 px-4 py-3">
            <div class="text-xs text-muted">手机号</div>
            <div class="mt-1 text-sm text-ink">{{ user.mobile || '未填写' }}</div>
          </div>
          <div class="rounded-2xl border border-line/70 bg-white/70 px-4 py-3">
            <div class="text-xs text-muted">账号状态</div>
            <div class="mt-1 text-sm text-ink">{{ statusText }}</div>
          </div>
        </div>
      </div>

      <button class="btn-ghost w-full sm:w-auto" type="button" @click="handleLogout">退出登录</button>
    </section>

    <BottomNav />
  </main>

  <main v-else class="page-shell">
    <LoadingState text="正在加载我的主页..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/common/BottomNav.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)
const avatarSrc = computed(() => user.value?.avatarUrl || '/panda-badge.svg')
const statusText = computed(() => (user.value?.status === 'active' ? '账号正常' : user.value?.status || '未知状态'))

onMounted(async () => {
  if (!userStore.user) {
    await userStore.loadMe()
  }
})

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>
