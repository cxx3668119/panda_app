from pydantic import BaseModel, Field


class ChatIntroGeneration(BaseModel):
    summary: str = Field(
        description="首屏总览摘要，用 1 到 2 句话概括用户当前最核心的命理主题与整体基调。"
    )
    appearance: str = Field(
        description="外在气质或给人的第一印象解读，用于描述用户整体形象、气场或表征倾向。"
    )
    family: str = Field(
        description="家庭与成长环境相关的解读，用于描述原生家庭氛围、成长课题或家庭影响。"
    )
    relationship: str = Field(
        description="感情与关系模式解读，用于描述亲密关系倾向、情缘课题或相处风格。"
    )
    career: str = Field(
        description="事业方向与工作节奏解读，用于描述用户更适合的发展方式、职场特点或事业趋势。"
    )
    wealth: str = Field(
        description="财富与资源获取方式解读，用于描述财运节奏、风险点或更适合的资源积累路径。"
    )
    health: str = Field(
        description="身体状态与健康提醒，用于给出日常状态观察和保守型健康建议，不提供医疗结论。"
    )
    timeline2020to2035: str = Field(
        description="2020 到 2035 年的阶段性节奏总结，用于概括重要阶段变化，而不是逐年硬性断言。"
    )
    suggestions: list[str] = Field(
        description="推荐追问列表，给前端直接渲染为快捷问题，帮助用户围绕首屏解读继续追问。"
    )


class ChatAnswerGeneration(BaseModel):
    answer: str = Field(description="本次 AI 提问的主回答内容，直接面向用户展示。")
    conclusion: str = Field(description="一句话结论，用于快速概括这次问题的核心判断。")
    reasoning: str = Field(
        description="回答依据说明，用于解释为什么得出这个结论，强调上下文和判断逻辑。"
    )
    suggestion: str = Field(
        description="可执行建议，给用户一条更具体、可落地的下一步行动方向。"
    )
    riskLevel: str = Field(
        description="风险等级标记，用于标识本次问题或回答是否涉及较高风险场景，例如 low、medium、high。"
    )
    rejected: bool = Field(
        description="是否触发拒答或降级处理。为 true 时表示问题越过产品边界或命中敏感规则。"
    )
