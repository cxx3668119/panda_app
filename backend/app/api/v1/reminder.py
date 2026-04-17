from fastapi import APIRouter, Depends

from app.core.response import ok
from app.core.security import get_current_token
from app.schemas.reminder import ReminderSettingsUpdateRequest
from app.services.reminder_service import ReminderService

router = APIRouter(prefix='/reminder', tags=['reminder'])
service = ReminderService()


@router.get('/settings')
def get_settings(_: str = Depends(get_current_token)):
    return ok(service.get_settings().model_dump())


@router.post('/settings')
def save_settings(payload: ReminderSettingsUpdateRequest, _: str = Depends(get_current_token)):
    return ok(service.save_settings(payload).model_dump())
