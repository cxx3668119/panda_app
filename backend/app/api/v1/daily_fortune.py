from fastapi import APIRouter, Depends
from app.models.app_user import AppUser

from app.api.dependencies import get_daily_fortune_service
from app.core.response import ok
from app.services.daily_fortune_service import DailyFortuneService
from app.core.security import get_current_user

router = APIRouter(prefix="/daily-fortune", tags=["daily-fortune"])


@router.get("/today")
def get_today(
    # user: AppUser = Depends(get_current_user),
    service: DailyFortuneService = Depends(get_daily_fortune_service),
):
    return ok(service.get_today().model_dump())


@router.get("/history")
def get_history(
    service: DailyFortuneService = Depends(get_daily_fortune_service),
):
    return ok([item.model_dump() for item in service.get_history()])
