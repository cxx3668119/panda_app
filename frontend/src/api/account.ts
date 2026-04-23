import { get, patch, postForm } from '@/api/client'
import type { AccountUpdatePayload, UserAccount } from '@/types'

export async function fetchMe() {
  return get<UserAccount>('/account/me')
}

export async function updateMe(payload: AccountUpdatePayload) {
  return patch<UserAccount>('/account/me', payload)
}

export async function uploadAvatar(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return postForm<UserAccount>('/account/avatar', formData)
}
