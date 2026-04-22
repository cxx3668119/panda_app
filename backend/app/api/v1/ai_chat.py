from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.core.response import ok
from app.core.security import get_current_token
from app.schemas.chat import AskAiRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix='/ai', tags=['ai'])


@router.get('/quota')
def get_quota(_: str = Depends(get_current_token), service: ChatService = Depends(get_chat_service)):
    return ok(service.get_quota().model_dump())


@router.get('/chat/session/today')
def get_today_session(_: str = Depends(get_current_token), service: ChatService = Depends(get_chat_service)):
    return ok([item.model_dump() for item in service.get_today_session()])


@router.post('/chat/ask')
def ask_ai(
    payload: AskAiRequest,
    _: str = Depends(get_current_token),
    service: ChatService = Depends(get_chat_service),
):
    return ok(service.ask(payload).model_dump())
