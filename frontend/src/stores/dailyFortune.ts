import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchFortuneHistory, fetchTodayFortune } from '@/api/daily'
import type { DailyFortuneData } from '@/types'

export const useDailyFortuneStore = defineStore('dailyFortune', () => {
  const today = ref<DailyFortuneData | null>(null)
  const history = ref<DailyFortuneData[]>([])
  const loadingToday = ref(false)
  const todayError = ref('')

  async function loadToday() {
    loadingToday.value = true
    todayError.value = ''

    try {
      today.value = await fetchTodayFortune()
      return today.value
    } catch (error) {
      todayError.value =
        error instanceof Error ? error.message : '今日运势获取失败，请稍后重试'
      throw error
    } finally {
      loadingToday.value = false
    }
  }

  async function loadHistory() {
    history.value = await fetchFortuneHistory()
  }

  return {
    today,
    history,
    loadingToday,
    todayError,
    loadToday,
    loadHistory
  }
})
