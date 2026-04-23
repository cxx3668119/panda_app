import { get, post } from '@/api/client'
import type { ChangePasswordPayload, LoginResponse, RegisterPayload, UserProfile } from '@/types'

export async function login(payload: { email: string; password: string }) {
  return post<LoginResponse>('/auth/login', payload)
}

export async function register(payload: RegisterPayload) {
  return post<LoginResponse>('/auth/register', payload)
}

export async function saveProfile(profile: UserProfile) {
  return post<UserProfile>('/profile/save', profile)
}

export async function fetchCurrentProfile() {
  return get<UserProfile | null>('/profile/current')
}

export async function changePassword(payload: ChangePasswordPayload) {
  return post<{ success: true }>('/account/change-password', payload)
}
