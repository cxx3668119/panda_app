from pydantic import BaseModel
from datetime import datetime

class UserRecordCreateRequest(BaseModel):
    name: str
    birthday: datetime
    gender: str
    birthplace: str | None = None

class UserRecordResponse(BaseModel):
    id: int
    name: str
    birthday: datetime
    gender: str
    birthZodiacSign: str
    birthplace: str | None
    age: int
    zodiac: str
    horoscope: str
