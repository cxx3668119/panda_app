from pydantic import BaseModel

from app.core.enums import ReminderChannel


class ReminderSettingsResponse(BaseModel):
    enabled: bool
    channel: ReminderChannel
    time: str
    timezone: str


class ReminderSettingsUpdateRequest(ReminderSettingsResponse):
    pass
