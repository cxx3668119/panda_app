from __future__ import annotations

_system_prompt = (
    """你现在是一个紫薇八字大师，请推测该命局的前世与今生的因果。""".strip()
)
_continue_chat_system_prompt = """
你现在是一个紫薇八字大师。
要求：
1. 回答必须贴近用户当前问题，不要泛泛而谈。
2. 回答要结合上下文，而不是每次都重新从零开始。
3. 不使用宿命论、恐吓式表达、绝对化判断。
4. 不提供医疗、法律、投资等专业建议。
5. 如果问题过于敏感或越过边界，要给出克制的拒答或降级回应。
"""


def build_first_chat_prompt(record: dict) -> tuple[str, str]:
    system_prompt = _system_prompt
    user_prompt = f"""
        我的生辰时间是阳历{record.get('birthDate', '')}，出生时间是{record.get('birthTime', '')}，如果出生时间未知，请注明
        ，性別{record.get('gender', '')}，出生地{record.get('birthPlace', '')}，请帮我计算我的生辰八字，
        然后请推测该命局的前世与今生的因果。具体到今生的样貌和家庭还有情缘。
        可以关于事业，财运，身体健康，婚姻，家庭这些方面进行分析，但请不要直接说这些词，而是用更现代的语言来表达。
请严格返回一个合法 JSON 对象，并满足以下要求：
1. 只输出 JSON，不要输出任何解释文字
2. 不要输出 Markdown 或 ```json 代码块 
3. JSON 字段必须且只能包含：
summary: string，500字以内的命局总结
appearance: string，100字以内的外貌描述
family: string，100字以内的家庭描述
relationship: string，100字以内的感情与关系描述
career: string，100字以内的事业描述
wealth: string，100字以内的财富描述
health: string，100字以内的健康描述
timeline2020to2035: string，100字以内的阶段性节奏总结
suggestions: list[str]，推荐追问列表
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


def build_continue_chat_prompt(
    question: str,
    intro_summary: str,
    record: dict,
    recent_messages: list[dict],
) -> tuple[str, str]:
    system_prompt = _continue_chat_system_prompt

    history_lines = []
    for item in recent_messages:
        history_lines.append(
            f"- 角色：{item.get('role', '')}；内容：{item.get('content', '')}"
        )
    history_text = "\n".join(history_lines) if history_lines else "暂无历史消息"

    user_prompt = f"""
用户资料：
- 出生日期：{record.get('birthDate', '')}
- 出生时间：{record.get('birthTime', '')}
- 性别：{record.get('gender', '')}
- 出生地：{record.get('birthPlace', '')}
- 年龄：{record.get('age', '')}
- 生肖：{record.get('zodiac', '')}
- 星座：{record.get('horoscope', '')}
已生成的个人主题解读摘要：
{intro_summary}
最近消息历史：
{history_text}
用户当前问题：
{question}
        请基于之前的命局分析，给出详细解答，并严格按照以下JSON 格式返回结果。
   - answer: string
   - conclusion: string or null
   - reasoning: string or null
   - suggestion: string
   - riskLevel: string or null
   - rejected: bool 
返回示例：
{
  "answer": "……",
  "conclusion": "……",
  "reasoning": "……",
  "suggestion": "……",
  "riskLevel": "low",
  "rejected": false
}
    """.strip()
    return system_prompt, user_prompt
