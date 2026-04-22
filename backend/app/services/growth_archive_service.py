from app.repositories.growth_repository import GrowthRepository
from app.schemas.growth_archive import GrowthArchiveResponse


class GrowthArchiveService:
    def __init__(self, repository: GrowthRepository) -> None:
        self.repository = repository

    def get_home(self) -> GrowthArchiveResponse:
        return GrowthArchiveResponse(**self.repository.get_archive())
