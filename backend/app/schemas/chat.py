from pydantic import BaseModel, field_validator


class QuotaResponse(BaseModel):
    freeLimit: int
    freeUsed: int
    paidBalance: int


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    disclaimer: str | None = None
    rejected: bool | None = None


class AskAiRequest(BaseModel):
    question: str

    @field_validator('question')
    @classmethod
    def validate_question(cls, value: str) -> str:
        question = value.strip()
        if not question:
            raise ValueError('问题不能为空')
        if len(question) > 500:
            raise ValueError('问题长度不能超过500个字符')
        return question
