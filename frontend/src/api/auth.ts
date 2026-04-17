import { get, post } from '@/api/client'
import type { LoginResponse, UserProfile } from '@/types'

export async function sendEmailCode(email: string) {
  return post<{ success: true; message: string }>('/auth/email/send-code', { email })
}

export async function loginByEmail(payload: { email: string; code: string }) {
  return post<LoginResponse>('/auth/email/login', payload)
}

export async function saveProfile(profile: UserProfile) {
  return post<UserProfile>('/profile/save', profile)
}

export async function fetchCurrentProfile() {
  return get<UserProfile | null>('/profile/current')
}
