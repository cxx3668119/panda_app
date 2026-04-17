from pydantic import BaseModel


class GrowthArchiveResponse(BaseModel):
    summary: str
    recentQuestions: list[str]
    keywords: list[str]
    streakDays: int
    recentFortunes: list[dict[str, str | int]]
