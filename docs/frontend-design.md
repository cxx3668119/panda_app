# AI八字算命助手 前端设计文档

## 1. 文档信息

| 版本号 | 创建日期 | 关联文档 | 状态 |
|--------|----------|----------|------|
| V1.0 | 2026-04-16 | docs/ai-bazi-assistant-prd.md、docs/requirements-clarification.md | 初稿 |

## 2. 文档目标

本文档用于指导 AI八字算命助手 MVP 的前端设计与研发实现，明确页面信息架构、核心交互、组件拆分、状态管理、接口对接、异常处理与埋点方案，确保 H5 首发版本可以高效落地，并兼容后续微信小程序扩展。

## 3. 设计范围

### 3.1 首版范围
MVP 前端需覆盖以下功能：
- 邮箱验证码登录（H5）
- 八字建档
- 首份命盘解读
- 今日日运查看
- AI追问互动
- 成长档案
- 提醒设置
- 次数不足后的购买引导弹层

### 3.2 暂不包含
- 多人合盘
- 深度年度报告
- 社区内容广场
- 多命理体系扩展
- 复杂支付流程页
- 签到系统
- 智能提醒降频策略

## 4. 已确认的业务规则基线

### 4.1 平台与登录
- MVP 首发平台：H5
- 后续支持：微信小程序、Web
- H5 登录方式：邮箱验证码登录
- 小程序登录方式：微信授权登录
- 首版不做游客态核心体验，核心功能依赖登录身份承接数据

### 4.2 建档与解读
- 建档方式：表单输入
- 必填字段：出生日期、性别
- 可选增强字段：出生时间、出生地、时区、公历/农历切换
- 支持“未知时辰”
- 用户可修改出生信息
- 未知时辰用户可以建档、查看命盘解读、查看日运
- 未知时辰用户不允许使用 AI 提问
- 命盘解读由 LLM 生成
- 解读结构固定，需包含性格、优势、风险、建议、长文解读
- 需明确展示“仅供参考/生成说明/免责声明”

### 4.3 日运与问答
- 今日日运按用户访问实时生成
- 同一天内容固定，不允许刷新出不同结果
- 支持历史日运查看
- 支持分享能力
- AI问答仅结合当天上下文
- 页面需明确提示“当前回答仅结合当天上下文”
- 登录用户默认 3 次免费提问
- 超出免费次数后进入购买引导

### 4.4 风控与提示
- 敏感词需做兜底转换
- 投资类问题直接拒答
- 医疗、法律、投资等高风险方向需展示免责声明
- 输出语气保持克制、启发式、非绝对化

## 5. 页面信息架构

```text
启动页/落地页
  └── 登录页
        └── 建档页
              └── 命盘解读页
                    └── 首页/今日日运页
                          ├── AI问答页
                          ├── 历史日运页
                          ├── 成长档案页
                          └── 提醒设置页
```

### 5.1 一级导航建议
MVP 建议采用底部 Tab + 功能跳转的轻量结构：
- 首页（日运）
- 成长档案
- 我的/设置

说明：
- 命盘解读页不建议放入底部 Tab，作为建档后的关键承接页与“我的命盘”二级入口存在。
- AI问答页由命盘解读页和日运页双入口进入。

## 6. 页面级功能设计

### 6.1 登录页

#### 页面目标
完成 H5 邮箱验证码登录，建立用户身份，承接建档与后续数据留存。

#### 页面元素
- Logo / 产品价值主张
- 邮箱输入框
- 验证码输入框
- 获取验证码按钮
- 登录按钮
- 用户协议入口
- 隐私政策入口
- 免责声明入口

#### 交互规则
- 邮箱输入实时校验格式
- 点击“获取验证码”后开始 60 秒倒计时
- 验证码 5 分钟有效
- 登录成功后：
  - 若未建档，跳转建档页
  - 若已建档，进入今日日运首页

#### 异常处理
- 邮箱格式错误：输入框下方提示
- 验证码错误/过期：toast 提示并保留邮箱
- 网络异常：支持重试

#### 埋点建议
- `view_login`
- `click_send_code`
- `send_code_success`
- `send_code_fail`
- `login_success`
- `login_fail`

### 6.2 建档页

#### 页面目标
让用户在 1 分钟内完成命盘创建，并快速进入首份解读。

#### 页面元素
- 出生日期选择器
- 出生时间选择器
- 未知时辰开关
- 性别选择
- 出生地输入
- 时区选择
- 公历/农历切换
- 提交按钮
- 建档说明

#### 交互规则
- 默认使用公历
- 开启“未知时辰”后，出生时间选择器禁用
- 开启“未知时辰”后展示提示：
  - 会影响部分解读精度
  - 不可使用 AI 提问功能
- 提交前做字段完整性校验
- 成功后跳转命盘解读页

#### 页面文案提示建议
- “出生时辰不确定也可以先体验，但部分互动能力会受限。”
- “内容仅供娱乐陪伴和自我探索参考。”

#### 埋点建议
- `view_profile_form`
- `change_birth_date`
- `change_birth_time`
- `switch_birth_time_unknown`
- `submit_birth_info`
- `profile_created`
- `profile_create_fail`

### 6.3 命盘解读页

#### 页面目标
承接用户首次价值感知，建立“专属感 + 可读性 + 可继续探索”的第一印象。

#### 页面结构
1. 顶部摘要卡片
2. 性格特征模块
3. 优势能力模块
4. 风险提醒模块
5. 成长建议模块
6. 长文解读模块
7. 免责声明模块
8. 底部行动区

#### 底部行动区
- 查看今日日运
- 去 AI 提问
- 修改出生信息

#### 交互规则
- 首屏先展示摘要和核心四模块
- 长文默认折叠，支持“展开全文”
- 若为未知时辰用户：
  - “去 AI 提问”按钮置灰
  - 点击后弹出能力限制说明
- 修改出生信息后需重新生成解读，并提示旧内容已失效

#### 埋点建议
- `view_profile_result`
- `expand_full_interpretation`
- `click_go_daily_fortune`
- `click_go_ai_chat`
- `click_edit_profile`

### 6.4 首页 / 今日日运页

#### 页面目标
提供用户每日高频打开的核心内容，形成连续使用习惯。

#### 页面结构
1. 今日日期与状态区
2. 状态评分卡片
3. 关键词标签
4. 宜做事项
5. 谨慎事项
6. 行动建议
7. 一句话提醒
8. 长文详情区
9. 操作区

#### 操作区
- 发起 AI 提问
- 分享
- 查看历史日运

#### 交互规则
- 页面首次进入触发今日日运请求
- 若后台未生成，则展示 loading 态
- 生成成功后当日内容固定
- 下拉刷新只刷新展示状态，不改变内容
- 支持跳转历史日运页
- 支持分享按钮预埋

#### 状态呈现建议
- 评分使用数值 + 标签并存，如：`78 / 稳定推进`
- 关键词使用 2~3 个标签展示
- 卡片摘要优先，长文放详情区

#### 埋点建议
- `view_daily_fortune`
- `view_daily_detail`
- `click_daily_share`
- `click_daily_history`
- `click_daily_ask_ai`

### 6.5 历史日运页

#### 页面目标
承接成长档案和用户回顾需求，形成历史沉淀。

#### 页面元素
- 日期列表
- 每日摘要
- 每日评分
- 详情跳转

#### 交互规则
- 默认按日期倒序展示
- 支持分页加载
- 点击进入指定日期日运详情
- 同日详情使用只读模式

#### 埋点建议
- `view_daily_history`
- `click_history_item`

### 6.6 AI问答页

#### 页面目标
基于命盘和当日上下文，为用户提供可追问、克制、个性化的启发式建议。

#### 页面元素
- 顶部上下文提示条
- 剩余次数展示
- 预设问题快捷入口
- 对话消息流
- 输入框
- 发送按钮
- 风险免责声明区

#### 顶部提示文案
- “当前回答仅结合你当天的命盘与日运上下文生成。”

#### 预设问题建议
- 今天适合做需求汇报吗？
- 今天适合推进跨团队协作吗？
- 我今天更适合沟通还是独立思考？
- 今天适合做关键决策吗？

#### 交互规则
- 未知时辰用户不可进入提问
- 次数不足时：
  - 输入框可见但发送后弹出购买引导更自然
  - 或直接禁用发送并展示购买 CTA
- 提问发送后展示流式等待态/打字态
- 回答返回后附加免责声明
- 风险问题直接展示拒答卡片
- 同一会话只保留当天上下文，不展示历史跨天会话

#### 风险问题处理
- 投资类：直接拒答
- 医疗/法律：给边界提示 + 免责声明
- 命中敏感词：展示“问题已调整表达后处理”或直接拒绝

#### 埋点建议
- `view_ai_chat`
- `click_quick_question`
- `ask_ai_question`
- `receive_ai_answer`
- `ai_question_rejected`
- `quota_exhausted`
- `click_buy_quota`

### 6.7 成长档案页

#### 页面目标
展示历史沉淀，增强长期陪伴感。

#### 页面结构
1. 阶段总结卡片
2. 最近日运记录
3. 最近提问记录
4. 关注主题关键词
5. 连续访问天数

#### 交互规则
- 首版不做复杂图表
- 首版不做签到模块
- 最近提问记录仅展示摘要，不直接暴露敏感长文本
- 主题关键词点击后可筛选历史提问/日运

#### 埋点建议
- `view_growth_archive`
- `click_recent_question`
- `click_topic_keyword`

### 6.8 提醒设置页

#### 页面目标
让用户开启和管理日运提醒，服务次日回访。

#### 页面元素
- 提醒总开关
- 提醒渠道选择
- 提醒时间选择
- 时区设置
- 提醒说明文案

#### 交互规则
- 默认开启站内提醒
- 默认时间为 09:00
- 首版不做自动降频
- 若在 H5 环境提醒能力有限，可展示“站内提醒/消息订阅待平台支持”说明

#### 埋点建议
- `view_reminder_settings`
- `enable_reminder`
- `disable_reminder`
- `change_reminder_time`

## 7. 组件拆分设计

### 7.1 基础业务组件
- `AuthEmailForm`：邮箱登录表单
- `ProfileForm`：建档表单
- `InterpretationSummaryCard`：命盘解读摘要卡片
- `InterpretationSection`：解读分段模块
- `DailyFortuneCard`：日运主卡片
- `DailyFortuneDetail`：日运长文详情
- `QuestionQuotaBar`：问答剩余额度条
- `QuestionQuickActions`：快捷问题入口
- `ChatMessageList`：对话消息列表
- `RiskNoticeBar`：风险与上下文提示条
- `HistoryFortuneList`：历史日运列表
- `GrowthKeywordPanel`：关键词面板
- `ReminderForm`：提醒设置表单
- `PurchaseQuotaModal`：购买次数弹层

### 7.2 通用组件
- `EmptyState`
- `LoadingState`
- `ErrorRetryBox`
- `SectionHeader`
- `DisclaimerBlock`
- `ActionFooterBar`

## 8. 状态管理设计

### 8.1 Store 划分建议
- `useUserStore`
  - 用户信息
  - token
  - 登录态
- `useProfileStore`
  - 命盘档案
  - 解读结果
  - 是否未知时辰
- `useDailyFortuneStore`
  - 今日日运
  - 历史日运列表
- `useChatStore`
  - 当日会话
  - 消息列表
  - 输入态/加载态
- `useQuotaStore`
  - 免费次数
  - 已用次数
  - 付费剩余次数
- `useReminderStore`
  - 提醒开关
  - 提醒时间
  - 提醒渠道

### 8.2 本地缓存建议
本地缓存建议只保存：
- token
- 用户基础信息
- 最近一次建档表单草稿
- 今日日运最后一次展示快照

不建议明文缓存：
- 完整出生信息
- 风险问题文本
- 敏感问答长文本

## 9. 接口对接清单

### 9.1 认证接口
- `POST /api/v1/auth/email/send-code`
- `POST /api/v1/auth/email/login`
- `POST /api/v1/auth/wechat/login`

### 9.2 命盘与解读接口
- `POST /api/v1/profile/save`
- `GET /api/v1/profile/current`
- `GET /api/v1/profile/interpretation`

### 9.3 日运接口
- `GET /api/v1/daily-fortune/today`
- `GET /api/v1/daily-fortune/history`
- `GET /api/v1/daily-fortune/{fortuneDate}`

### 9.4 AI问答接口
- `GET /api/v1/ai/quota`
- `POST /api/v1/ai/chat/ask`
- `GET /api/v1/ai/chat/session/today`

### 9.5 商业化接口
- `GET /api/v1/quota/packages`
- `POST /api/v1/quota/orders/create`
- `GET /api/v1/quota/orders/{orderNo}`

### 9.6 成长与提醒接口
- `GET /api/v1/growth-archive/home`
- `GET /api/v1/reminder/settings`
- `POST /api/v1/reminder/settings`
- `POST /api/v1/user/delete-apply`

## 10. 页面状态与异常处理设计

### 10.1 通用状态
- 初始加载态
- 空状态
- 错误态
- 网络异常态
- 登录失效态

### 10.2 关键异常场景

| 场景 | 处理方式 | 用户提示 |
|------|----------|----------|
| token 失效 | 清理登录态并跳登录页 | 登录状态已失效，请重新登录 |
| 未建档访问核心页 | 强制跳转建档页 | 请先完成建档后再体验 |
| 未知时辰进入提问 | 弹出限制弹窗 | 未知时辰暂不支持 AI 提问 |
| 免费次数用尽 | 弹购买引导 | 免费次数已用完，可购买更多提问次数 |
| 投资类问题 | 直接拒答卡片 | 当前不提供投资建议，请结合专业意见判断 |
| 日运未生成 | loading + 重试 | 今日运势正在生成中，请稍后刷新 |
| 分享失败 | toast 提示 | 当前分享失败，请稍后重试 |

## 11. 视觉与内容表达建议

### 11.1 内容风格
- 现代语言表达，不使用大量传统术语堆砌
- 用“倾向、提醒、建议、观察角度”替代绝对判断
- 首屏信息密度高但结构清晰
- 弱化“宿命感”，强化“陪伴感”和“参考感”

### 11.2 页面节奏
- 建档页强调低门槛
- 解读页强调专属感
- 日运页强调高频打开
- AI问答页强调互动感
- 成长档案页强调沉淀感

## 12. 埋点方案建议

### 12.1 核心漏斗埋点
1. `view_home`
2. `click_start_profile`
3. `submit_birth_info`
4. `profile_created`
5. `view_profile_result`
6. `view_daily_fortune`
7. `ask_ai_question`
8. `enable_reminder`
9. `revisit_next_day`

### 12.2 关键属性建议
- `platform`
- `source_page`
- `has_birth_time`
- `birth_time_unknown`
- `question_topic`
- `question_length`
- `quota_type`（free/paid）
- `risk_type`
- `reminder_channel`

## 13. 前端研发建议

### 13.1 页面目录建议
```text
src/pages/login
src/pages/profile/create
src/pages/profile/result
src/pages/daily/index
src/pages/daily/history
src/pages/ai/chat
src/pages/growth/archive
src/pages/settings/reminder
```

### 13.2 组件目录建议
```text
src/components/auth
src/components/profile
src/components/daily
src/components/chat
src/components/growth
src/components/common
```

### 13.3 公共能力建议
- 统一请求封装
- 统一错误码处理
- 统一登录失效拦截
- 统一免责声明组件
- 统一埋点上报方法

## 14. 验收标准

| 模块 | 验收标准 |
|------|----------|
| 登录 | 用户可完成邮箱验证码登录，并正确进入建档或首页 |
| 建档 | 用户可在 1 分钟内完成建档，未知时辰路径可正常提交 |
| 命盘解读 | 结构化内容完整展示，长文可展开，免责声明可见 |
| 今日日运 | 首次访问可生成并展示内容，同日刷新不变更 |
| AI问答 | 当天上下文提示明确，未知时辰不可提问，风险问题可拒答 |
| 成长档案 | 可展示历史日运、最近提问、关键词与连续访问天数 |
| 提醒设置 | 用户可开启/关闭提醒并修改提醒时间 |

## 15. 结论

MVP 前端设计应围绕“低门槛建档、首屏感知价值、日运驱动留存、问答增强互动、成长档案承接沉淀”展开。页面与组件设计应优先保证 H5 首发体验顺畅，并在状态管理、接口抽象和交互提示上预留小程序扩展能力，为后续留存增强版与商业化版本打下基础。
