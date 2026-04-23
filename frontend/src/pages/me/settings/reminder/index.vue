<template>
  <main v-if="form" class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Reminder settings</div>
      <h1 class="page-title">提醒设置</h1>
      <p class="page-subtitle">在“我的”里管理你的日运提醒节奏，当前版本默认支持站内提醒。</p>
    </section>

    <section class="surface-card space-y-6">
      <div class="flex items-start justify-between gap-4 rounded-[24px] border border-line/70 bg-white/65 p-4">
        <div class="space-y-1">
          <div class="section-title">开启提醒</div>
          <div class="text-sm leading-6 text-muted">默认提醒时间为每天 09:00</div>
        </div>
        <label class="relative inline-flex cursor-pointer items-center">
          <input v-model="form.enabled" type="checkbox" class="peer sr-only" />
          <span class="h-7 w-12 rounded-full bg-line transition peer-checked:bg-accent"></span>
          <span class="absolute left-1 h-5 w-5 rounded-full bg-white shadow-sm transition peer-checked:translate-x-5"></span>
        </label>
      </div>

      <div class="space-y-2">
        <label class="field-label">提醒渠道</label>
        <input :value="form.channel" disabled class="field-input" />
      </div>

      <div class="space-y-2">
        <label class="field-label">提醒时间</label>
        <input v-model="form.time" type="time" class="field-input" />
      </div>

      <div class="space-y-2">
        <label class="field-label">时区</label>
        <input v-model="form.timezone" class="field-input" />
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="btn-primary" @click="handleSave">保存设置</button>
        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div>
    </section>
  </main>

  <main v-else class="page-shell">
    <LoadingState text="正在加载提醒设置..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import LoadingState from '@/components/common/LoadingState.vue'
import { useReminderStore } from '@/stores/growth'
import type { ReminderSettings } from '@/types'

const reminderStore = useReminderStore()
const form = ref<ReminderSettings | null>(null)

const settings = computed(() => reminderStore.settings)

onMounted(async () => {
  if (!reminderStore.settings) {
    await reminderStore.loadSettings()
  }
  form.value = settings.value ? { ...settings.value } : null
})

async function handleSave() {
  if (!form.value) return
  await reminderStore.saveSettings(form.value)
  form.value = settings.value ? { ...settings.value } : null
}
</script>
