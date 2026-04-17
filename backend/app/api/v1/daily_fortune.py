from fastapi import APIRouter, Depends

from app.core.response import ok
from app.core.security import get_current_token
from app.services.daily_fortune_service import DailyFortuneService

router = APIRouter(prefix='/daily-fortune', tags=['daily-fortune'])
service = DailyFortuneService()


@router.get('/today')
def get_today(_: str = Depends(get_current_token)):
    return ok(service.get_today().model_dump())


@router.get('/history')
def get_history(_: str = Depends(get_current_token)):
    return ok([item.model_dump() for item in service.get_history()])
