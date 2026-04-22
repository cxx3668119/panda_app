from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.core.response import ok
from app.schemas.auth import EmailLoginRequest, SendEmailCodeRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/email/send-code')
def send_email_code(payload: SendEmailCodeRequest, service: AuthService = Depends(get_auth_service)):
    return ok(service.send_email_code(payload))


@router.post('/email/login')
def login_by_email(payload: EmailLoginRequest, service: AuthService = Depends(get_auth_service)):
    return ok(service.login_by_email(payload).model_dump())
