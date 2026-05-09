export interface UserAccount {
  id: number
  email: string
  nickname: string
  mobile: string | null
  timezone: string
  avatarUrl: string | null
  status: string
}

export interface UserRecord {
  id: number
  name: string
  birthday: string
  gender: string
  birthZodiacSign: string
  birthplace: string
  age: number
  zodiac: string
  horoscope: string
}

export interface LoginResponse {
  token: string
  user: UserAccount
  hasProfile: boolean
}

export interface RegisterPayload {
  nickname: string
  email: string
  password: string
  timezone: string
  mobile: string | null
}

export interface UserProfile {
  calendarType: 'SOLAR' | 'LUNAR'
  birthDate: string
  birthTime: string | null
  birthTimeUnknown: boolean
  gender: 'MALE' | 'FEMALE'
  birthPlace: string
  timezone: string
}

export interface InterpretationData {
  summaryTitle: string
  personality: string
  strength: string
  risk: string
  advice: string
  fullContent: string
  disclaimer: string
}

export interface DailyFortuneData {
  date: string
  score: number
  scoreLabel: string
  keywords: string[]
  suitable: string
  caution: string
  actionAdvice: string
  summary: string
  detail: string
}

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  disclaimer?: string
  rejected?: boolean
}

export interface QuotaData {
  freeLimit: number
  freeUsed: number
  paidBalance: number
}

export interface GrowthArchiveData {
  summary: string
  recentQuestions: string[]
  keywords: string[]
  streakDays: number
  recentFortunes: Array<{ date: string; summary: string; score: number }>
}

export interface ReminderSettings {
  enabled: boolean
  channel: 'IN_APP'
  time: string
  timezone: string
}

export interface AccountUpdatePayload {
  nickname: string
  email: string
  mobile: string | null
  timezone: string
}

export interface ChangePasswordPayload {
  currentPassword: string
  newPassword: string
}
