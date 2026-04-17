from app.repositories.daily_fortune_repository import DailyFortuneRepository
from app.schemas.daily_fortune import DailyFortuneResponse


class DailyFortuneService:
    def __init__(self) -> None:
        self.repository = DailyFortuneRepository()

    def get_today(self) -> DailyFortuneResponse:
        return DailyFortuneResponse(**self.repository.get_today())

    def get_history(self) -> list[DailyFortuneResponse]:
        return [DailyFortuneResponse(**item) for item in self.repository.get_history()]
