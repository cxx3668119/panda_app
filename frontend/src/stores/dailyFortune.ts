import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchFortuneHistory, fetchTodayFortune } from '@/api/daily'
import type { DailyFortuneData } from '@/types'

export const useDailyFortuneStore = defineStore('dailyFortune', () => {
  const today = ref<DailyFortuneData | null>(null)
  const history = ref<DailyFortuneData[]>([])

  async function loadToday() {
    today.value = await fetchTodayFortune()
  }

  async function loadHistory() {
    history.value = await fetchFortuneHistory()
  }

  return {
    today,
    history,
    loadToday,
    loadHistory
  }
})
