from app.core.exceptions import BusinessError
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import InterpretationResponse, ProfileResponse, ProfileSaveRequest


class ProfileService:
    def __init__(self, repository: ProfileRepository) -> None:
        self.repository = repository

    def get_current_profile(self) -> ProfileResponse | None:
        profile = self.repository.get_profile()
        return ProfileResponse(**profile) if profile else None

    def save_profile(self, payload: ProfileSaveRequest) -> ProfileResponse:
        if not payload.birthTimeUnknown and not payload.birthTime:
            raise BusinessError('已知时辰时必须填写出生时辰', status_code=400)
        saved = self.repository.save_profile(payload.model_dump())
        return ProfileResponse(**saved)

    def get_interpretation(self) -> InterpretationResponse:
        return InterpretationResponse(**self.repository.get_interpretation())
