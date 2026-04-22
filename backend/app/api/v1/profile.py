from fastapi import APIRouter, Depends

from app.api.dependencies import get_profile_service
from app.core.response import ok
from app.core.security import get_current_token
from app.schemas.profile import ProfileSaveRequest
from app.services.profile_service import ProfileService

router = APIRouter(prefix='/profile', tags=['profile'])


@router.post('/save')
def save_profile(
    payload: ProfileSaveRequest,
    _: str = Depends(get_current_token),
    service: ProfileService = Depends(get_profile_service),
):
    return ok(service.save_profile(payload).model_dump())


@router.get('/current')
def get_current_profile(
    _: str = Depends(get_current_token),
    service: ProfileService = Depends(get_profile_service),
):
    profile = service.get_current_profile()
    return ok(profile.model_dump() if profile else None)


@router.get('/interpretation')
def get_interpretation(
    _: str = Depends(get_current_token),
    service: ProfileService = Depends(get_profile_service),
):
    return ok(service.get_interpretation().model_dump())
