from pydantic import BaseModel, field_validator

from app.core.enums import CalendarType, Gender


class ProfileSaveRequest(BaseModel):
    calendarType: CalendarType
    birthDate: str
    birthTime: str | None
    birthTimeUnknown: bool
    gender: Gender
    birthPlace: str
    timezone: str

    @field_validator('birthTime')
    @classmethod
    def validate_birth_time(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip() or None


class ProfileResponse(ProfileSaveRequest):
    pass


class InterpretationResponse(BaseModel):
    summaryTitle: str
    personality: str
    strength: str
    risk: str
    advice: str
    fullContent: str
    disclaimer: str
