# AI八字算命助手 后端设计文档

## 1. 文档信息

| 版本号 | 创建日期 | 关联文档 | 状态 |
|--------|----------|----------|------|
| V1.0 | 2026-04-16 | docs/ai-bazi-assistant-prd.md、docs/requirements-clarification.md、docs/tech-stack.md | 初稿 |

## 2. 文档目标

本文档用于指导 AI八字算命助手 MVP 的后端设计与研发实现，明确系统架构、模块边界、接口职责、数据模型、Pydantic 模型设计、SQLAlchemy 实体建议、核心流程、内容安全与可观测性方案，为 FastAPI 技术栈下的开发落地提供统一基线。

## 3. 设计范围

### 3.1 首版范围
MVP 后端需支持以下能力：
- H5 邮箱验证码登录
- 微信小程序登录预留
- 命盘档案创建与修改
- 八字排盘与命盘解读生成
- 今日日运实时生成与历史查询
- AI问答与当日上下文拼装
- 免费次数控制与购买次数预埋
- 成长档案聚合
- 提醒设置管理
- 敏感词处理、风险分类、拒答与免责声明输出
- 埋点日志记录

### 3.2 暂不包含
- 完整支付回调链路
- 多人合盘
- 深度报告体系
- 社区内容
- 多命理体系扩展
- 复杂智能推荐引擎

## 4. 已确认的业务规则基线

### 4.1 平台与认证
- MVP 首发 H5，后续兼容微信小程序、Web
- H5 使用邮箱验证码登录
- 小程序使用微信登录
- 用户身份为命盘、日运、问答、成长档案、提醒设置的主索引

### 4.2 命盘与解读
- 建档为表单输入
- 支持“未知时辰”
- 用户可修改出生信息
- 修改后提升档案版本并重新生成解读
- 解读内容由 LLM 生成
- 解读结构固定
- 解读结果长文优先
- 解读需附“仅供参考/生成说明/免责声明”

### 4.3 日运与问答
- 今日日运按访问实时生成
- 同日内容固定
- 支持历史查询
- AI问答仅使用当天上下文
- 登录用户默认 3 次免费提问
- 免费次数用尽后走购买次数预埋能力
- 未知时辰用户不允许提问

### 4.4 风控规则
- 敏感词做兜底转换
- 投资类问题直接拒答
- 医疗、法律、投资等方向输出免责声明
- 回答语气保持克制、启发式、非绝对化

## 5. 技术架构设计

## 5.1 技术栈
- Web 框架：FastAPI
- ORM：SQLAlchemy
- 数据校验：Pydantic
- 数据库：MySQL（首选）
- 认证方式：JWT Bearer Token
- 缓存：Redis（建议）
- 异步任务：APScheduler + Redis 或 Celery（二选一，MVP 推荐 APScheduler + Redis）

## 5.2 分层架构建议

```text
API Layer
  └── 路由、鉴权、参数接收、统一响应
Service Layer
  └── 业务编排、规则控制、额度扣减、风险校验
Domain/Manager Layer
  └── 命盘计算、上下文组装、LLM Prompt 构造、提醒调度
Repository Layer
  └── 数据访问、查询封装、事务边界控制
Model Layer
  └── SQLAlchemy 实体
Schema Layer
  └── Pydantic 请求/响应模型
Infrastructure Layer
  └── JWT、Redis、消息/任务、LLM 客户端、邮件服务、微信服务
```

## 5.3 模块划分
- 认证中心
- 用户档案中心
- 命盘解读中心
- 日运中心
- AI问答中心
- 商业化中心
- 成长档案中心
- 提醒中心
- 风控中心
- 埋点与日志中心

## 6. 推荐目录结构

```text
app/
  api/
    v1/
      auth.py
      profile.py
      daily_fortune.py
      ai_chat.py
      quota.py
      growth_archive.py
      reminder.py
      user.py
  core/
    config.py
    security.py
    exceptions.py
    response.py
    enums.py
  models/
    user.py
    auth_code.py
    profile.py
    interpretation.py
    daily_fortune.py
    chat.py
    quota.py
    reminder.py
    event_log.py
  schemas/
    auth.py
    profile.py
    interpretation.py
    daily_fortune.py
    chat.py
    quota.py
    growth_archive.py
    reminder.py
    common.py
  services/
    auth_service.py
    profile_service.py
    bazi_service.py
    interpretation_service.py
    daily_fortune_service.py
    ai_chat_service.py
    quota_service.py
    growth_archive_service.py
    reminder_service.py
    risk_guard_service.py
    content_safety_service.py
    event_log_service.py
  repositories/
    user_repository.py
    profile_repository.py
    interpretation_repository.py
    daily_fortune_repository.py
    chat_repository.py
    quota_repository.py
    reminder_repository.py
  integrations/
    llm_client.py
    email_client.py
    wechat_client.py
    redis_client.py
  tasks/
    reminder_tasks.py
    archive_tasks.py
    event_tasks.py
  db/
    base.py
    session.py
```

## 7. 模块设计说明

### 7.1 认证中心

#### 职责
- 邮箱验证码发送
- 邮箱验证码登录
- 微信登录预留
- token 签发与解析
- 登录行为记录

#### 核心服务
- `AuthService`
- `EmailCodeService`
- `TokenService`
- `WechatAuthService`

#### 核心规则
- 验证码 5 分钟有效
- 同一邮箱 60 秒内限制重复发送
- 登录成功后补齐用户基础信息
- 首次登录自动创建问答次数账户和默认提醒设置

### 7.2 用户档案中心

#### 职责
- 创建/修改命盘档案
- 处理出生信息合法性
- 排盘结果写入
- 档案版本维护

#### 核心服务
- `ProfileService`
- `BaziCalculateService`
- `ProfileVersionService`

#### 核心规则
- 一个用户仅维护一份当前有效档案
- 修改出生信息后提高 `profile_version`
- 未知时辰标记写入档案
- 未知时辰不影响日运与解读，但影响问答权限

### 7.3 命盘解读中心

#### 职责
- 组装命盘解读 Prompt
- 调用 LLM 生成固定结构内容
- 存储摘要、分段内容、完整长文
- 附加免责声明

#### 核心服务
- `InterpretationService`
- `PromptBuilderService`
- `ContentSafetyService`

#### 核心规则
- 输出结构固定为：性格、优势、风险、建议、长文
- 用户修改档案后重新生成新版本内容
- 解读生成后固定存储，默认不提供“手动刷新生成”能力

### 7.4 日运中心

#### 职责
- 今日日运实时生成
- 历史日运查询
- 同日固定内容控制
- 分享数据输出预留

#### 核心服务
- `DailyFortuneService`
- `DailyPromptService`
- `FortuneCacheService`

#### 核心规则
- 首次访问某日页面时实时生成
- 若当日已生成则直接返回
- 同一天内容固定
- 支持按日期查询历史日运

### 7.5 AI问答中心

#### 职责
- 提问权限校验
- 免费/付费次数控制
- 当天上下文组装
- 风险问题识别
- 拒答与免责声明输出
- 会话消息持久化

#### 核心服务
- `AiChatService`
- `QuotaService`
- `ContextAssembleService`
- `RiskGuardService`

#### 核心规则
1. 校验是否已登录
2. 校验是否已建档
3. 校验是否未知时辰
4. 校验剩余次数
5. 执行敏感词处理与风险识别
6. 风险问题直接拒答
7. 正常问题基于当天上下文生成回答
8. 回答统一经过安全重写
9. 成功回答后扣减次数并落库

### 7.6 商业化中心

#### 职责
- 次数套餐查询
- 订单创建
- 支付成功后增加问答次数

#### 核心服务
- `QuotaPackageService`
- `QuotaOrderService`
- `PaymentCallbackService`

#### 核心规则
- MVP 先完成套餐和订单预埋
- 支付成功后增加 `paid_question_balance`
- 暂不实现完整第三方支付回调细节

### 7.7 成长档案中心

#### 职责
- 聚合历史日运
- 聚合历史提问摘要
- 提炼阶段关键词
- 统计连续访问天数

#### 核心服务
- `GrowthArchiveService`
- `TopicTagService`

#### 核心规则
- 首版以聚合展示为主
- 不做签到系统
- 不做复杂周总结自动生成

### 7.8 提醒中心

#### 职责
- 获取与更新提醒设置
- 调度提醒任务
- 为不同平台预留发送能力

#### 核心服务
- `ReminderService`
- `ReminderSchedulerService`

#### 核心规则
- 默认开启站内提醒
- 默认时间 09:00
- 首版不做频控降频

### 7.9 风控中心

#### 职责
- 敏感词替换
- 风险问题分类
- 模型输出绝对化表达校正
- 拒答策略统一输出

#### 核心服务
- `RiskGuardService`
- `SensitiveWordService`
- `ContentSafetyService`

## 8. 数据模型设计

以下模型与前面产出的表结构保持一致。

### 8.1 用户与认证
- `users`
- `email_verification_codes`

### 8.2 命盘与解读
- `user_profiles`
- `profile_interpretations`

### 8.3 日运与问答
- `daily_fortunes`
- `ai_chat_sessions`
- `ai_chat_messages`

### 8.4 商业化与额度
- `user_quota_accounts`
- `quota_order_packages`
- `quota_orders`

### 8.5 提醒与埋点
- `reminder_settings`
- `user_event_logs`

## 9. SQLAlchemy 实体设计建议

### 9.1 实体基类
建议统一抽象 `BaseModelMixin`：
- `id`
- `created_at`
- `updated_at`
- `deleted_at`（可选）

### 9.2 关键实体建议

#### User
核心字段：
- `id`
- `user_no`
- `platform`
- `login_type`
- `email`
- `wechat_openid`
- `nickname`
- `avatar_url`
- `status`
- `last_login_at`

#### UserProfile
核心字段：
- `user_id`
- `calendar_type`
- `birth_date`
- `birth_time`
- `birth_time_unknown`
- `gender`
- `birth_place`
- `timezone`
- `bazi_year_pillar`
- `bazi_month_pillar`
- `bazi_day_pillar`
- `bazi_hour_pillar`
- `profile_version`
- `latest_interpretation_id`

#### ProfileInterpretation
核心字段：
- `user_id`
- `profile_id`
- `generation_type`
- `content_version`
- `summary_title`
- `personality_content`
- `strength_content`
- `risk_content`
- `advice_content`
- `full_content`
- `disclaimer_text`
- `is_current`

#### DailyFortune
核心字段：
- `user_id`
- `profile_id`
- `fortune_date`
- `score_overall`
- `keyword_1~3`
- `suitable_content`
- `caution_content`
- `action_advice`
- `summary_content`
- `detail_content`
- `generation_status`

#### AiChatSession
核心字段：
- `user_id`
- `profile_id`
- `session_date`
- `source_type`
- `source_id`
- `context_scope`
- `question_count`
- `status`

#### AiChatMessage
核心字段：
- `session_id`
- `user_id`
- `message_role`
- `message_type`
- `content`
- `content_safe`
- `risk_level`
- `risk_type`
- `reject_flag`
- `disclaimer_text`

#### UserQuotaAccount
核心字段：
- `user_id`
- `free_question_limit`
- `free_question_used`
- `paid_question_balance`
- `total_question_used`

## 10. Pydantic 模型设计建议

## 10.1 通用模型
- `BaseResponse`
- `PageRequest`
- `PageResponse[T]`
- `TokenPayload`
- `UserIdentity`

## 10.2 认证模型
- `SendEmailCodeRequest`
- `EmailLoginRequest`
- `WechatLoginRequest`
- `LoginResponse`

### 字段建议
```text
SendEmailCodeRequest:
- email: EmailStr

EmailLoginRequest:
- email: EmailStr
- code: str
- platform: Literal['H5']
```

## 10.3 命盘模型
- `ProfileSaveRequest`
- `ProfileCurrentResponse`
- `BaziInfoVO`

### ProfileSaveRequest 字段建议
- `calendar_type`
- `birth_date`
- `birth_time`
- `birth_time_unknown`
- `gender`
- `birth_place`
- `timezone`

校验建议：
- `birth_time_unknown=True` 时允许 `birth_time=None`
- `birth_time_unknown=False` 时 `birth_time` 必填

## 10.4 解读模型
- `InterpretationResponse`
- `InterpretationSectionVO`

## 10.5 日运模型
- `DailyFortuneResponse`
- `DailyFortuneHistoryItem`
- `DailyFortuneHistoryResponse`

## 10.6 问答模型
- `AiQuotaResponse`
- `AiAskRequest`
- `AiAskResponse`
- `ChatSessionResponse`
- `ChatMessageVO`

### AiAskRequest 字段建议
- `source_type: Literal['PROFILE', 'DAILY_FORTUNE']`
- `source_id: int | None`
- `question: str`

校验建议：
- 问题长度限制 1~500
- 过滤纯空白字符串

## 10.7 提醒模型
- `ReminderSettingsResponse`
- `ReminderSettingsUpdateRequest`

## 10.8 成长档案模型
- `GrowthArchiveHomeResponse`
- `RecentQuestionVO`
- `TopicKeywordVO`

## 11. API 设计摘要

### 11.1 认证模块
- `POST /api/v1/auth/email/send-code`
- `POST /api/v1/auth/email/login`
- `POST /api/v1/auth/wechat/login`

### 11.2 命盘模块
- `POST /api/v1/profile/save`
- `GET /api/v1/profile/current`
- `GET /api/v1/profile/interpretation`

### 11.3 日运模块
- `GET /api/v1/daily-fortune/today`
- `GET /api/v1/daily-fortune/history`
- `GET /api/v1/daily-fortune/{fortuneDate}`

### 11.4 AI问答模块
- `GET /api/v1/ai/quota`
- `POST /api/v1/ai/chat/ask`
- `GET /api/v1/ai/chat/session/today`

### 11.5 商业化模块
- `GET /api/v1/quota/packages`
- `POST /api/v1/quota/orders/create`
- `GET /api/v1/quota/orders/{orderNo}`

### 11.6 成长与提醒模块
- `GET /api/v1/growth-archive/home`
- `GET /api/v1/reminder/settings`
- `POST /api/v1/reminder/settings`
- `POST /api/v1/user/delete-apply`

## 12. 统一错误码建议

| 错误码 | 含义 |
|--------|------|
| 0 | 成功 |
| 40001 | 参数校验失败 |
| 40002 | 登录状态失效 |
| 40003 | 验证码错误或过期 |
| 40004 | 访问过于频繁 |
| 40401 | 用户不存在 |
| 40402 | 命盘档案不存在 |
| 40901 | 当日内容已存在 |
| 41001 | 问题超出可回答范围 |
| 41002 | 未知时辰不可提问 |
| 41003 | 免费及付费次数已用尽 |
| 50000 | 系统异常 |
| 50001 | LLM 服务异常 |
| 50002 | 命盘生成失败 |
| 50003 | 日运生成失败 |

## 13. 核心流程设计

### 13.1 邮箱登录流程
```text
用户输入邮箱 -> 发送验证码 -> 校验验证码 -> 查询/创建用户 -> 签发 JWT -> 初始化默认数据 -> 返回登录结果
```

### 13.2 建档流程
```text
用户提交出生信息 -> Pydantic 校验 -> 写入 user_profiles -> 调用排盘服务 -> 保存四柱结果 -> 调用解读服务 -> 持久化解读 -> 返回档案结果
```

### 13.3 今日日运流程
```text
用户访问今日日运 -> 查询当日是否已有内容 -> 有则直接返回 -> 无则组装命盘+日期上下文 -> 调用生成服务 -> 风控处理 -> 落库 -> 返回结果
```

### 13.4 AI问答流程
```text
用户提问 -> 校验登录/建档/未知时辰/次数 -> 敏感词转换 -> 风险分类 ->
若高风险则拒答并返回免责声明 ->
否则组装当天上下文 -> 调用 LLM -> 安全重写 -> 落库会话与消息 -> 扣减次数 -> 返回回答
```

### 13.5 购买次数流程
```text
查询套餐 -> 创建订单 -> 支付成功回调（预留） -> 增加 paid_question_balance -> 返回最新额度
```

## 14. 风控与内容安全设计

## 14.1 输入侧校验
- 邮箱格式校验
- 出生日期合法性校验
- 出生时间格式校验
- 问题长度限制
- 特殊字符与空白处理

## 14.2 风险分类建议
- `INVESTMENT`
- `MEDICAL`
- `LEGAL`
- `EXTREME`
- `SENSITIVE_OTHER`

## 14.3 风险处理策略

| 风险类型 | 策略 |
|----------|------|
| INVESTMENT | 直接拒答 |
| MEDICAL | 不给专业判断，输出边界提示 |
| LEGAL | 不给专业判断，输出边界提示 |
| EXTREME | 强制拒答并记录高风险日志 |
| SENSITIVE_OTHER | 视场景给弱化建议或拒答 |

## 14.4 统一免责声明模板
```text
本内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议，请结合实际情况独立判断。
```

## 14.5 输出重写规则
- 去除“绝对、注定、必须、一定”等高风险词
- 将结论式表达改写为倾向式建议
- 补充“结合实际情况判断”的收口

## 15. 缓存、事务与并发控制建议

### 15.1 缓存建议
- 邮箱验证码存 Redis
- 用户 token 黑名单可存 Redis
- 当日日运可加 Redis 热缓存
- 套餐列表可短期缓存

### 15.2 事务建议
以下场景需事务保护：
- 建档 + 排盘结果写入 + 档案版本更新
- 问答成功后消息落库 + 次数扣减
- 支付回调成功后订单更新 + 次数到账

### 15.3 并发控制建议
- 日运生成需使用用户 + 日期维度幂等锁
- 问答扣减次数建议使用行级锁或原子更新
- 验证码发送要做频控与重复发送保护

## 16. 日志与埋点设计

### 16.1 业务日志重点
- 登录成功/失败
- 建档成功/失败
- 命盘解读生成耗时
- 日运生成耗时
- AI问答调用耗时
- 风险命中类型
- 次数扣减前后余额
- 提醒设置变更

### 16.2 埋点事件建议
- `view_home`
- `click_start_profile`
- `submit_birth_info`
- `profile_created`
- `view_profile_result`
- `view_daily_fortune`
- `ask_ai_question`
- `receive_ai_answer`
- `enable_reminder`
- `revisit_next_day`
- `share_result`

### 16.3 日志脱敏建议
- 邮箱做部分脱敏
- 出生信息不打印完整明文
- 敏感问题文本默认不直接写业务日志
- 风控日志记录分类结果和摘要，不落完整原文

## 17. 可观测性与监控建议

### 17.1 核心指标
- 验证码发送成功率
- 登录成功率
- 建档成功率
- 解读生成成功率
- 今日日运生成成功率
- AI回答成功率
- 风险拒答率
- 免费次数耗尽转化率

### 17.2 性能指标
- 登录接口 P95
- 建档接口 P95
- 日运接口 P95
- AI问答首字响应时间
- LLM 平均耗时

### 17.3 告警建议
- LLM 服务失败率异常
- 日运生成失败率异常
- 验证码服务失败率异常
- Redis 不可用
- 数据库连接池耗尽

## 18. 后端研发落地建议

### 18.1 优先实现顺序
1. 认证中心
2. 用户档案中心
3. 命盘解读中心
4. 日运中心
5. AI问答中心
6. 风控中心
7. 成长档案中心
8. 提醒中心
9. 商业化预埋

### 18.2 代码职责边界建议
- `api` 只负责入参、出参与调用 service
- `service` 负责业务编排
- `repository` 负责数据库交互
- `integrations` 负责 LLM、邮件、微信、缓存等外部能力
- `schemas` 只描述数据结构，不承载业务逻辑

### 18.3 首版关键实现顺序
- 先打通邮箱登录 -> 建档 -> 解读 -> 今日日运闭环
- 再加 AI问答次数控制与风险拒答
- 最后补成长档案、提醒设置与商业化预埋

## 19. 验收标准

| 模块 | 验收标准 |
|------|----------|
| 认证 | H5 可完成验证码登录，返回稳定 token |
| 建档 | 用户可成功创建与更新命盘档案，未知时辰路径可用 |
| 解读 | 可生成固定结构的长文解读并成功存储 |
| 日运 | 首次访问实时生成，同日重复访问返回同一结果 |
| AI问答 | 可校验额度、识别未知时辰、限制当天上下文并进行风险拒答 |
| 成长档案 | 可聚合历史日运、问题摘要与关键词 |
| 提醒设置 | 可读取与更新提醒设置 |
| 日志与风控 | 风险分类、免责声明、关键日志均可正常产出 |

## 20. 结论

MVP 后端设计的核心是围绕“身份、命盘、日运、问答、次数、风控”建立一条稳定可扩展的数据与服务链路。FastAPI + SQLAlchemy + Pydantic 的组合足以支撑首版快速交付；在实现上应优先保证幂等、风险控制、内容一致性和日志可观测性，并为后续小程序接入、支付完善、留存增强与商业化扩展预留清晰边界。
