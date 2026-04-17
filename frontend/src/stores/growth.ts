import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchGrowthArchive, fetchReminderSettings, saveReminderSettings } from '@/api/growth'
import type { GrowthArchiveData, ReminderSettings } from '@/types'

export const useGrowthStore = defineStore('growth', () => {
  const archive = ref<GrowthArchiveData | null>(null)

  async function loadArchive() {
    archive.value = await fetchGrowthArchive()
  }

  return {
    archive,
    loadArchive
  }
})

export const useReminderStore = defineStore('reminder', () => {
  const settings = ref<ReminderSettings | null>(null)

  async function loadSettings() {
    settings.value = await fetchReminderSettings()
  }

  async function saveSettings(payload: ReminderSettings) {
    settings.value = await saveReminderSettings(payload)
  }

  return {
    settings,
    loadSettings,
    saveSettings
  }
})
