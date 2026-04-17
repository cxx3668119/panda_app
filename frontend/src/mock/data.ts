import type {
  DailyFortuneData,
  GrowthArchiveData,
  InterpretationData,
  QuotaData,
  ReminderSettings,
  UserProfile,
  ChatMessage
} from '@/types'

export const mockProfile: UserProfile = {
  calendarType: 'SOLAR',
  birthDate: '1998-08-18',
  birthTime: '09:30',
  birthTimeUnknown: false,
  gender: 'FEMALE',
  birthPlace: '杭州',
  timezone: 'Asia/Shanghai'
}

export const mockInterpretation: InterpretationData = {
  summaryTitle: '稳中有冲劲的表达者',
  personality: '你擅长把复杂问题拆开理解，对信息变化很敏感，既能共情他人也能快速捕捉风险。',
  strength: '在跨团队协作、需求梳理和节奏推进上有较强优势，适合承担连接信息与组织共识的角色。',
  risk: '当外部反馈不稳定时，容易过早自我归因，导致沟通前过度预演和内耗。',
  advice: '把“先对齐目标，再推动动作”作为日常节奏，会比直接推进更省力。',
  fullContent: '这份命盘解读偏向现代职场语境：你的优势不是单点爆发，而是稳定识别关键变量、建立结构、推动对齐。高压场景下，你可能一边追求效率，一边又在意表达是否足够周全，因此会在关键节点上花较多时间做心理准备。更适合你的成长策略不是无限提速，而是建立一套可复用的沟通模版和复盘机制，让你的判断力沉淀成稳定能力。',
  disclaimer: '本内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议，请结合实际情况独立判断。'
}

export const mockDailyFortune: DailyFortuneData = {
  date: '2026-04-16',
  score: 78,
  scoreLabel: '稳定推进',
  keywords: ['聚焦', '对齐', '留白'],
  suitable: '适合整理需求表达、推进已有共识的事项。',
  caution: '不宜在信息不充分时做过度承诺。',
  actionAdvice: '重要沟通先给结论，再补过程，会更容易获得支持。',
  summary: '今天更适合稳步推进，而不是强行突破。',
  detail: '你的当天状态更偏“清晰判断 + 稳定表达”。适合处理中短周期任务、需求汇报和跨团队同步。若临时插入新变量，建议先确认优先级，再决定是否接住。'
}

export const mockHistory: DailyFortuneData[] = [
  mockDailyFortune,
  { ...mockDailyFortune, date: '2026-04-15', score: 74, scoreLabel: '收束整理', keywords: ['回顾', '判断', '取舍'], summary: '适合做复盘与取舍。', detail: '昨天的重心更偏整理和决策。' },
  { ...mockDailyFortune, date: '2026-04-14', score: 82, scoreLabel: '顺势沟通', keywords: ['表达', '连接', '推进'], summary: '适合做重点沟通。', detail: '前天更适合做对外表达。' }
]

export const mockQuota: QuotaData = {
  freeLimit: 3,
  freeUsed: 1,
  paidBalance: 0
}

export const mockChatMessages: ChatMessage[] = [
  {
    id: 1,
    role: 'assistant',
    content: '当前回答仅结合你当天的命盘与日运上下文生成。今天更适合做信息对齐和稳步推进。',
    disclaimer: mockInterpretation.disclaimer
  }
]

export const mockGrowthArchive: GrowthArchiveData = {
  summary: '最近一周你更关注沟通节奏、需求汇报和决策压力，整体状态偏理性推进型。',
  recentQuestions: ['今天适合做需求汇报吗？', '我更适合沟通还是独立思考？'],
  keywords: ['需求汇报', '跨团队协作', '节奏管理'],
  streakDays: 4,
  recentFortunes: mockHistory.map((item) => ({ date: item.date, summary: item.summary, score: item.score }))
}

export const mockReminderSettings: ReminderSettings = {
  enabled: true,
  channel: 'IN_APP',
  time: '09:00',
  timezone: 'Asia/Shanghai'
}
