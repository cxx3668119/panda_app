import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_chat_service
from app.core.response import ok
from app.core.security import get_current_token
from app.schemas.chat import AskAiRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix='/ai', tags=['ai'])


def _sse_event(event_type: str, content: str = '') -> str:
    return f"data: {json.dumps({'type': event_type, 'content': content}, ensure_ascii=False)}\n\n"


def _wrap_sse(stream):
    yield _sse_event('start', '')
    for chunk in stream:
        yield _sse_event('delta', chunk)
    yield _sse_event('done', '')


@router.get('/quota')
def get_quota(_: str = Depends(get_current_token), service: ChatService = Depends(get_chat_service)):
    return ok(service.get_quota().model_dump())


@router.get('/chat/session')
def get_session(_: str = Depends(get_current_token), service: ChatService = Depends(get_chat_service)):
    return ok([item.model_dump() for item in service.get_session()])


@router.get('/chat/session/today')
def get_today_session(_: str = Depends(get_current_token), service: ChatService = Depends(get_chat_service)):
    return ok([item.model_dump() for item in service.get_today_session()])


@router.get('/chat/intro/stream')
def get_intro_stream(
    _: str = Depends(get_current_token),
    service: ChatService = Depends(get_chat_service),
):
    return StreamingResponse(
        _wrap_sse(service.intro_stream()),
        media_type='text/event-stream; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
        },
    )


@router.post('/chat/ask')
def ask_ai(
    payload: AskAiRequest,
    _: str = Depends(get_current_token),
    service: ChatService = Depends(get_chat_service),
):
    return ok(service.ask(payload).model_dump())


@router.post('/chat/ask/stream')
def ask_ai_stream(
    payload: AskAiRequest,
    _: str = Depends(get_current_token),
    service: ChatService = Depends(get_chat_service),
):
    return StreamingResponse(
        _wrap_sse(service.ask_stream(payload)),
        media_type='text/event-stream; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
        },
    )
