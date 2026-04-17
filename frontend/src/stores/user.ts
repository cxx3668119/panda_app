import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { clearAuthStorage, TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from '@/api/client'
import { loginByEmail } from '@/api/auth'
import type { LoginUser } from '@/types'

function readStoredUser(): LoginUser | null {
  const raw = localStorage.getItem(USER_STORAGE_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as LoginUser
  } catch {
    localStorage.removeItem(USER_STORAGE_KEY)
    return null
  }
}

export const useUserStore = defineStore('user', () => {
  const storedUser = readStoredUser()
  const token = ref(localStorage.getItem(TOKEN_STORAGE_KEY) || '')
  const email = ref(storedUser?.email || '')
  const nickname = ref(storedUser?.nickname || '')
  const isLoggedIn = computed(() => !!token.value)

  async function login(emailValue: string, code: string) {
    const result = await loginByEmail({ email: emailValue, code })
    token.value = result.token
    email.value = result.user.email
    nickname.value = result.user.nickname
    localStorage.setItem(TOKEN_STORAGE_KEY, result.token)
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(result.user))
    return result
  }

  function logout() {
    token.value = ''
    email.value = ''
    nickname.value = ''
    clearAuthStorage()
  }

  return {
    token,
    email,
    nickname,
    isLoggedIn,
    login,
    logout
  }
})
