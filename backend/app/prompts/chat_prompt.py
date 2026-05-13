from __future__ import annotations


def _base_system_prompt() -> str:
    return (
        '你是一位风格克制、表达清晰的命理主题解读助手。'
        '你的任务是基于用户的出生信息，生成面向自我探索与娱乐陪伴场景的内容。'
        '不要使用宿命论、恐吓式表达或绝对化判断。'
        '不要提供医疗、法律、投资等专业建议。'
    )


def _continue_system_prompt() -> str:
    return (
        '你是一位风格克制、表达清晰的命理问答助手。'
        '回答必须贴近用户当前问题，并结合已有上下文。'
        '不要使用宿命论、恐吓式表达或绝对化判断。'
        '不要提供医疗、法律、投资等专业建议。'
        '如果问题过于敏感或越过边界，要给出克制的拒答或降级回应。'
    )


def _record_block(record) -> str:
    return (
        f'- 出生时间：{record.birthday}\n'
        f'- 性别：{record.gender}\n'
        f'- 出生地：{record.birthplace}\n'
        f'- 年龄：{record.age}\n'
        f'- 生肖：{record.zodiac}\n'
        f'- 星座：{record.horoscope}'
    )


def _recent_history_block(recent_messages: list[dict]) -> str:
    if not recent_messages:
        return '暂无历史消息'

    lines: list[str] = []
    for item in recent_messages:
        lines.append(f"- 角色：{item.get('role', '')}；内容：{item.get('content', '')}")
    return '\n'.join(lines)


def build_first_chat_prompt(record) -> tuple[str, str]:
    system_prompt = _base_system_prompt()
    user_prompt = f"""
请根据以下用户资料，生成一份个人主题解读。

用户资料：
{_record_block(record)}

请严格返回一个合法 JSON 对象，并满足以下要求：
1. 只输出 JSON，不要输出任何解释文字。
2. 不要输出 Markdown 或 ```json 代码块。
3. JSON 字段必须且只能包含：
   - summary: string，100 字以内的整体命局与人生主题总结
   - appearance: string，100 字以内的外在气质描述
   - family: string，100 字以内的家庭与成长环境描述
   - relationship: string，100 字以内的关系与情感模式描述
   - career: string，100 字以内的事业方向描述
   - wealth: string，100 字以内的财富节奏描述
   - health: string，100 字以内的健康提醒描述
   - timeline2020to2035: string，100 字以内的阶段节奏总结
   - suggestions: list[str]，推荐追问列表

返回示例：
{{
  "summary": "这是一段整体命局与人生主题的概括。",
  "appearance": "这是一段关于外在气质与给人印象的描述。",
  "family": "这是一段关于家庭与成长环境影响的描述。",
  "relationship": "这是一段关于感情与关系模式的描述。",
  "career": "这是一段关于事业方向与职场特征的描述。",
  "wealth": "这是一段关于财富节奏与资源积累方式的描述。",
  "health": "这是一段关于身体状态与健康提醒的描述。",
  "timeline2020to2035": "这是一段关于 2020-2035 阶段节奏的总结。",
  "suggestions": [
    "我更适合什么样的事业路径？",
    "我在感情里最需要注意什么？",
    "未来几年我最该把握的重点是什么？"
  ]
}}
""".strip()
    return system_prompt, user_prompt


def build_first_chat_stream_prompt(record) -> tuple[str, str]:
    system_prompt = _base_system_prompt()
    user_prompt = f"""
请根据以下用户资料，直接写一段适合作为聊天页开场白的个人主题解读正文。

用户资料：
{_record_block(record)}

要求：
1. 直接输出自然语言正文，不要输出 JSON。
2. 不要输出标题、字段名、Markdown 或代码块。
3. 控制在 3 到 5 段，总长度适中，适合在聊天页直接阅读。
4. 语气温和、清晰，像一位有经验的顾问在做第一轮解读。
5. 结尾顺势给出 3 个可以继续追问的方向，但不要写成 JSON 列表。
""".strip()
    return system_prompt, user_prompt


def build_continue_chat_prompt(
    question: str,
    intro_summary: str,
    record,
    recent_messages: list[dict],
) -> tuple[str, str]:
    system_prompt = _continue_system_prompt()
    user_prompt = f"""
请基于以下上下文，回答用户的追问。

用户资料：
{_record_block(record)}

已生成的个人主题解读摘要：
{intro_summary}

最近消息历史：
{_recent_history_block(recent_messages)}

用户当前问题：
{question}

请严格返回一个合法 JSON 对象，并满足以下要求：
1. 只输出 JSON，不要输出任何解释文字。
2. 不要输出 Markdown 或 ```json 代码块。
3. JSON 字段必须且只能包含：
   - answer: string
   - conclusion: string or null
   - reasoning: string or null
   - suggestion: string
   - riskLevel: string or null
   - rejected: bool

返回示例：
{{
  "answer": "这是回答内容，要求自然流畅，适合直接回复给用户。",
  "conclusion": "这是一句对当前问题的总结性结论，如果无法明确给出可返回 null。",
  "reasoning": "这是对回答依据的解释，用来说明为什么得出这个判断，如果无法明确给出可返回 null。",
  "suggestion": "这是一条给用户的可执行建议，要求具体可行。",
  "riskLevel": "low",
  "rejected": false
}}
""".strip()
    return system_prompt, user_prompt


def build_continue_chat_stream_prompt(
    question: str,
    intro_summary: str,
    record,
    recent_messages: list[dict],
) -> tuple[str, str]:
    system_prompt = _continue_system_prompt()
    user_prompt = f"""
请基于以下上下文，直接回答用户当前问题。

用户资料：
{_record_block(record)}

已生成的个人主题解读摘要：
{intro_summary}

最近消息历史：
{_recent_history_block(recent_messages)}

用户当前问题：
{question}

要求：
1. 直接输出自然语言正文，不要输出 JSON。
2. 不要输出标题、字段名、Markdown 或代码块。
3. 回答要像聊天中的直接回复，语气自然、清晰、克制。
4. 先给结论，再给简要解释，最后给一条可执行建议。
""".strip()
    return system_prompt, user_prompt
