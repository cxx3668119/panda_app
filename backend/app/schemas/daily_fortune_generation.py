from pydantic import BaseModel, Field


class DailyFortuneGeneration(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description="今日日运综合分，范围 0 到 100，分数越高表示当天整体状态越适合主动推进。",
    )
    keywords: list[str] = Field(
        min_length=2,
        max_length=5,
        description="今日日运关键词列表，建议 2 到 5 个短词，用于概括当天的核心状态或行动主题。",
    )

    suitable: str = Field(
        description="适合做的事情，描述当天更适宜推进的方向、场景或行为。"
    )
    caution: str = Field(
        description="需要谨慎的事情，描述当天不宜冒进或需要注意的风险点。"
    )
    actionAdvice: str = Field(
        description="行动建议，给用户一条可直接执行的具体建议，强调可操作性。"
    )
    summary: str = Field(
        description="今日日运摘要，用一句话概括当天的整体节奏和建议方向。"
    )
    detail: str = Field(
        description="今日日运详细解读，对当天状态、适合场景和注意事项进行更完整说明。"
    )
