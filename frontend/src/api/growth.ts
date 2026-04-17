import { get, post } from '@/api/client'
import type { GrowthArchiveData, ReminderSettings } from '@/types'

export async function fetchGrowthArchive() {
  return get<GrowthArchiveData>('/growth-archive/home')
}

export async function fetchReminderSettings() {
  return get<ReminderSettings>('/reminder/settings')
}

export async function saveReminderSettings(payload: ReminderSettings) {
  return post<ReminderSettings>('/reminder/settings', payload)
}
