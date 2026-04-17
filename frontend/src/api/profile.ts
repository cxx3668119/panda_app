import { get } from '@/api/client'
import type { InterpretationData } from '@/types'

export async function fetchInterpretation() {
  return get<InterpretationData>('/profile/interpretation')
}
