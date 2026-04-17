from fastapi import APIRouter

from app.core.response import ok
from app.schemas.auth import EmailLoginRequest, SendEmailCodeRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])
service = AuthService()


@router.post('/email/send-code')
def send_email_code(payload: SendEmailCodeRequest):
    return ok(service.send_email_code(payload))


@router.post('/email/login')
def login_by_email(payload: EmailLoginRequest):
    return ok(service.login_by_email(payload).model_dump())
