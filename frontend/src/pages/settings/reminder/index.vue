<template>
  <main class="page" v-if="form">
    <h1 class="page-title">提醒设置</h1>
    <p class="page-subtitle">管理你的日运提醒节奏，当前版本默认支持站内提醒。</p>

    <div class="card">
      <div class="switch-row">
        <div>
          <div class="section-title" style="margin-bottom: 4px">开启提醒</div>
          <div class="muted">默认提醒时间为每天 09:00</div>
        </div>
        <input v-model="form.enabled" type="checkbox" />
      </div>

      <div class="field mt-16">
        <label>提醒渠道</label>
        <input :value="form.channel" disabled />
      </div>

      <div class="field mt-16">
        <label>提醒时间</label>
        <input v-model="form.time" type="time" />
      </div>

      <div class="field mt-16">
        <label>时区</label>
        <input v-model="form.timezone" />
      </div>

      <div class="actions mt-16">
        <button class="primary-btn" @click="handleSave">保存设置</button>
      </div>
    </div>

    <DisclaimerBlock class="mt-20" text="H5 首版先展示站内提醒能力，更多消息订阅方式待平台支持。" />
    <BottomNav />
  </main>

  <main v-else class="page">
    <LoadingState text="正在加载提醒设置..." />
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import BottomNav from '@/components/common/BottomNav.vue'
import DisclaimerBlock from '@/components/common/DisclaimerBlock.vue'
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
