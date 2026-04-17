import { get } from '@/api/client'
import type { DailyFortuneData } from '@/types'

export async function fetchTodayFortune() {
  return get<DailyFortuneData>('/daily-fortune/today')
}

export async function fetchFortuneHistory() {
  return get<DailyFortuneData[]>('/daily-fortune/history')
}
