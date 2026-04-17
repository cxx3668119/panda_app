from app.repositories.growth_repository import GrowthRepository
from app.schemas.growth_archive import GrowthArchiveResponse


class GrowthArchiveService:
    def __init__(self) -> None:
        self.repository = GrowthRepository()

    def get_home(self) -> GrowthArchiveResponse:
        return GrowthArchiveResponse(**self.repository.get_archive())
