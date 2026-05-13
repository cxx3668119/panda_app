from __future__ import annotations


def build_daily_fortune_prompt(
    record: dict,
    interpretation_summary: str,
    recent_history: list[dict],
    target_date: str,
) -> tuple[str, str]:
    system_prompt = """
你是一名风格克制、表达清晰的 AI 日运解读助手。

你的任务是基于用户资料、长期画像摘要和最近日运历史，
生成一份面向日常陪伴场景的今日日运建议。

要求：
1. 语气温和、克制、清晰，不使用宿命论、恐吓式表达。
2. 不提供医疗、法律、投资等专业建议。
3. 输出内容更像“趋势提醒 + 行动建议”，而不是绝对判断。
4. 尽量使用现代语言，减少命理术语堆砌。
5. 只返回一个合法 JSON 对象，不要输出额外解释、标题或 Markdown 代码块。
""".strip()

    history_lines = []
    for item in recent_history:
        history_lines.append(
            f"- 日期：{item.get('date', '')}；摘要：{item.get('summary', '')}；分数：{item.get('score', '')}"
        )
    history_text = "\n".join(history_lines) if history_lines else "无历史日运数据"

    user_prompt = f"""
请为用户生成 {target_date} 的今日日运。

用户资料：
- 姓名：{record.get('name', '')}
- 出生日期：{record.get('birthDate', '')}
- 出生时间：{record.get('birthTime', '')}
- 时辰未知：{record.get('birthTimeUnknown', False)}
- 性别：{record.get('gender', '')}
- 出生地：{record.get('birthPlace', '')}
- 时区：{record.get('timezone', '')}
- 年龄：{record.get('age', '')}
- 生肖：{record.get('zodiac', '')}
- 星座：{record.get('horoscope', '')}

长期画像摘要：
{interpretation_summary or '暂无长期画像摘要'}

最近日运历史：
{history_text}

请严格返回一个合法 JSON 对象，并满足以下要求：
1. 只输出 JSON，不要输出任何解释文字
2. 不要输出 Markdown 或 ```json 代码块
3. JSON 字段必须且只能包含：
   - score: int，范围 0-100
   - keywords: string[]，2 到 5 个关键词
   - suitable: string
   - caution: string
   - actionAdvice: string
   - summary: string
   - detail: string

返回示例：
{{
  "score": 78,
  "keywords": ["聚焦", "表达", "判断"],
  "suitable": "适合推进沟通与信息对齐。",
  "caution": "避免在信息不足时做过度承诺。",
  "actionAdvice": "先给结论，再补过程。",
  "summary": "今天更适合稳步推进，而不是强行突破。",
  "detail": "今天的状态偏向清晰判断和稳定表达，适合处理中短周期任务。"
}}
""".strip()

    return system_prompt, user_prompt
