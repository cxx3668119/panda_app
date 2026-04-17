from pydantic import BaseModel


class DailyFortuneResponse(BaseModel):
    date: str
    score: int
    scoreLabel: str
    keywords: list[str]
    suitable: str
    caution: str
    actionAdvice: str
    summary: str
    detail: str
