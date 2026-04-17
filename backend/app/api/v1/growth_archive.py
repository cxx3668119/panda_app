from fastapi import APIRouter, Depends

from app.core.response import ok
from app.core.security import get_current_token
from app.services.growth_archive_service import GrowthArchiveService

router = APIRouter(prefix='/growth-archive', tags=['growth-archive'])
service = GrowthArchiveService()


@router.get('/home')
def get_home(_: str = Depends(get_current_token)):
    return ok(service.get_home().model_dump())
