from app.repositories.daily_fortune_repository import DailyFortuneRepository
from app.schemas.daily_fortune import DailyFortuneResponse
from app.core.exceptions import BusinessError


class DailyFortuneService:
    def __init__(self, repository: DailyFortuneRepository) -> None:
        self.repository = repository

    def get_today(self) -> DailyFortuneResponse:
        user = self.repository.user
        record_id = self.repository.get_bound_user_record_id()
        if not record_id:
            raise BusinessError("请绑定个人档案", status_code=400)
        existing = self.repository.find_today()
        if existing:
            return DailyFortuneResponse(**existing)
        # context = self.repository.build_generation_context()
        return DailyFortuneResponse(**self.repository.get_today())

    def get_history(self) -> list[DailyFortuneResponse]:
        return [DailyFortuneResponse(**item) for item in self.repository.get_history()]
