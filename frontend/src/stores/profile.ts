import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchCurrentProfile, saveProfile } from '@/api/auth'
import { fetchInterpretation } from '@/api/profile'
import type { InterpretationData, UserProfile } from '@/types'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref<UserProfile | null>(null)
  const interpretation = ref<InterpretationData | null>(null)

  async function loadProfile() {
    profile.value = await fetchCurrentProfile()
    interpretation.value = await fetchInterpretation()
  }

  async function submitProfile(payload: UserProfile) {
    profile.value = await saveProfile(payload)
    interpretation.value = await fetchInterpretation()
  }

  return {
    profile,
    interpretation,
    loadProfile,
    submitProfile
  }
})
