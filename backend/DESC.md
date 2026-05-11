# Backend AI Daily Fortune Guide

## 1. 目标

本文档用于指导当前项目把“今日日运”从静态查库逻辑，升级为标准化的 AI 生成链路。

目标链路：

`前端请求 -> 后端编排 -> 读取用户上下文 -> 调用模型 -> 校验结构化结果 -> 落库 -> 返回前端`

这条链路不是只服务于“今日日运”，后续做：

- AI 命盘解读
- 周报总结
- 问事 Agent
- 成长档案总结

都可以复用同一套工程方法。

---

## 2. 当前项目分层原则

### API Layer

接 HTTP 请求，不写复杂 AI 逻辑。

### Use Case / Service Layer

决定什么时候调用 AI，什么时候查缓存，什么时候落库。

### LLM Client Layer

只负责调模型，不夹业务。

### Prompt Layer

只负责组装 prompt。

### Schema Layer

负责结构化输出校验。

### Repository Layer

负责查库和存库。

### Eval / Logging Layer

负责记录效果、排查问题。

---

## 3. 第 0 步状态

当前 `daily_fortune` 链路已经完成从 `demo user` 切到 `current user`：

- `get_daily_fortune_service` 已通过 `get_current_user` 注入真实用户
- `DailyFortuneRepository` 已按 `self.user.id` 查询数据

这一步的意义是：后续 AI 生成必须绑定真实用户上下文，而不是 demo 数据。

---

## 4. 下一步开发顺序

建议严格按下面顺序做，不要跳步。

1. 先定义 AI 输出 Schema
2. 再封装 AI Client
3. 再写 Prompt Builder
4. 再写生成器 Service
5. 再接到 `DailyFortuneService`
6. 再补 Repository 写库能力
7. 再做错误处理和降级
8. 最后补日志和评估

---

## 5. 第 1 步：定义 AI 输出 Schema

### 目标

先定义“模型必须返回什么”，而不是先写 prompt。

### 原则

先有 schema，再有模型输出。

### 新建文件

- `backend/app/schemas/daily_fortune_generation.py`

### 推荐内容

```python
from pydantic import BaseModel, Field


class DailyFortuneGeneration(BaseModel):
    score: int = Field(ge=0, le=100)
    keywords: list[str]
    suitable: str
    caution: str
    actionAdvice: str
    summary: str
    detail: str
```

### 为什么这样做

- 防止模型缺字段
- 防止字段类型错乱
- 方便后续落库
- 方便以后做 Agent tool output schema

### 完成标准

- 模型输出可以被 `Pydantic` 成功校验
- 缺字段或类型错误时，程序能明确报错

---

## 6. 第 2 步：封装统一 AI Client

### 目标

把模型调用统一收口，避免业务代码到处直接调 SDK。

### 原则

业务代码不要直接依赖模型 SDK。

### 新建文件

- `backend/app/clients/ai_client.py`

### 这个文件只负责

- 读取 API Key / Base URL / Model
- 发起模型请求
- 返回原始结果

### 这个文件不要负责

- 用户判断
- prompt 拼接
- 数据库存储
- 业务异常兜底

### 推荐接口

```python
class AiClient:
    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        ...
```

### 需要补充的配置

建议在 `backend/app/core/config.py` 增加：

```python
ai_api_key: str = ''
ai_base_url: str | None = None
ai_model: str = 'gpt-4.1-mini'
daily_fortune_prompt_version: str = 'v1'
```

### 完成标准

- 切换模型只改 `AiClient` 和配置，不改业务层

---

## 7. 第 3 步：写 Prompt Builder

### 目标

把 prompt 当成独立资产管理，而不是塞在 service 里。

### 原则

Prompt 也是代码资产，需要可维护、可版本化。

### 新建文件

- `backend/app/prompts/daily_fortune_prompt.py`

### 输入内容建议

- 用户出生信息
- 性别
- 出生地
- 时区
- 是否已知时辰
- 命盘解读摘要
- 最近 3 到 7 天日运
- 当前日期

### 风格约束建议

- 语气克制
- 不绝对化
- 不宿命论
- 不恐吓
- 不给医疗/法律/投资建议
- 输出面向日常行动建议
- 语言尽量现代、清晰、职场化

### Prompt Builder 产出

- `system_prompt`
- `user_prompt`

### 完成标准

- prompt 文件独立可维护
- prompt 变更可追踪到版本号

---

## 8. 第 4 步：写生成器 Service

### 目标

把“prompt + 模型调用 + schema 校验”封装成一个可复用生成器。

### 原则

生成器是 AI feature 的核心，不直接混进业务 service。

### 新建文件

- `backend/app/services/daily_fortune_generator.py`

### 职责

1. 收集输入上下文
2. 组装 prompt
3. 调用 `AiClient`
4. 解析模型结果
5. 使用 `DailyFortuneGeneration` 校验
6. 返回结构化对象

### 推荐接口

```python
class DailyFortuneGenerator:
    def generate(
        self,
        profile: dict,
        interpretation: dict | None,
        recent_history: list[dict],
        target_date: str,
    ) -> DailyFortuneGeneration:
        ...
```

### 完成标准

- 独立调用生成器就能拿到结构化日运结果
- 模型格式错误时能明确失败

---

## 9. 第 5 步：接入主业务链路

### 目标

把 `DailyFortuneService.get_today()` 从“查库返回”升级为“查库优先，缺失时 AI 生成”。

### 当前文件

- `backend/app/services/daily_fortune_service.py`

### 目标逻辑

1. 获取当前用户
2. 获取当前 active profile
3. 查询今天是否已有日运
4. 如果有，直接返回
5. 如果没有，调用 generator 生成
6. 保存到数据库
7. 返回给前端

### 推荐伪代码

```python
def get_today(self) -> DailyFortuneResponse:
    profile = ...
    if not profile:
        return DailyFortuneResponse(...)

    existing = self.repository.find_today(...)
    if existing:
        return DailyFortuneResponse(**existing)

    generated = self.generator.generate(...)
    saved = self.repository.save_generated_fortune(...)
    return DailyFortuneResponse(**saved)
```

### 完成标准

- 前端第一次请求时会触发生成
- 同一天第二次请求直接走数据库

---

## 10. 第 6 步：补 Repository 写库能力

### 目标

让 Repository 只负责数据读写，不关心 AI 业务细节。

### 当前文件

- `backend/app/repositories/daily_fortune_repository.py`

### 建议新增方法

- `find_today(...)`
- `get_recent_history(...)`
- `save_generated_fortune(...)`

### 写库时建议存储的字段

- `fortune_date`
- `score`
- `keyword_tags`
- `favorable_text`
- `unfavorable_text`
- `advice_text`
- `summary_text`
- `detail_json`
- `generation_mode='llm'`
- `llm_model`
- `prompt_version`

### 完成标准

- 数据库中能看到 AI 生成的日运
- 同一用户同一天不重复生成多条

---

## 11. 第 7 步：错误处理与降级

### 目标

让接口在模型失败时仍然可用。

### 至少要处理的情况

- 用户未建档
- profile 信息不完整
- 模型超时
- 模型返回空结果
- 模型返回结构不合法
- 数据库存储失败

### 最小降级策略

当 AI 失败时，返回一版保守建议：

```python
{
    "date": "...",
    "score": 60,
    "scoreLabel": "保持观察",
    "keywords": ["观察", "留白"],
    "suitable": "适合先整理已有信息。",
    "caution": "避免在不确定时快速下结论。",
    "actionAdvice": "先观察，再推进。",
    "summary": "今天更适合稳住节奏。",
    "detail": "系统暂时无法生成完整日运，先给你一版保守建议。"
}
```

### 完成标准

- AI 出错时接口仍能返回可用结果
- 错误会被记录，不是静默失败

---

## 12. 第 8 步：日志与评估

### 目标

让这条 AI 链路可复盘、可优化。

### 最小日志字段建议

- `user_id`
- `profile_id`
- `target_date`
- `model_name`
- `prompt_version`
- `latency_ms`
- `success`
- `error_type`

### 最小评估方式

先手动准备 5 到 10 组样本，验证：

- 输出结构是否稳定
- 风格是否统一
- 是否过于模板化
- 是否出现越界表达
- 是否和用户上下文有关联

### 完成标准

- 可以定位“为什么这条日运生成得不好”
- 可以比较不同 prompt 版本效果

---

## 13. 推荐目录结构

建议逐步补成这样：

```text
backend/app/
  api/
  clients/
    ai_client.py
  prompts/
    daily_fortune_prompt.py
  repositories/
    daily_fortune_repository.py
  schemas/
    daily_fortune.py
    daily_fortune_generation.py
  services/
    daily_fortune_service.py
    daily_fortune_generator.py
```

---

## 14. 实操节奏建议

### 第一轮

- 完成 `daily_fortune_generation.py`
- 完成 `ai_client.py`
- 完成 `daily_fortune_prompt.py`
- 完成 `daily_fortune_generator.py`

目标：本地独立调通生成器

### 第二轮

- 改 `daily_fortune_service.py`
- 改 `daily_fortune_repository.py`

目标：前端打开“今日日运”时能触发 AI 生成并返回

### 第三轮

- 补错误处理
- 补日志
- 做 5 条样本评估

目标：这条链路具备基础工程化能力

---

## 15. 学习重点

这次开发你最该掌握的不是“怎么调一个模型”，而是下面这套思维：

1. 先定义输出 contract
2. 再封装模型调用
3. 再拆 prompt
4. 再做业务编排
5. 再做数据落地
6. 最后补观测与评估

这就是后续从 AI feature 走向 AI Agent 开发的底层方法。

