from app.repositories.reminder_repository import ReminderRepository
from app.schemas.reminder import ReminderSettingsResponse, ReminderSettingsUpdateRequest


class ReminderService:
    def __init__(self, repository: ReminderRepository) -> None:
        self.repository = repository

    def get_settings(self) -> ReminderSettingsResponse:
        return ReminderSettingsResponse(**self.repository.get_settings())

    def save_settings(
        self, payload: ReminderSettingsUpdateRequest
    ) -> ReminderSettingsResponse:
        return ReminderSettingsResponse(
            **self.repository.save_settings(payload.model_dump())
        )
