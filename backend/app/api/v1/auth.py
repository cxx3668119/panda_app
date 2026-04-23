from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.core.response import ok
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return ok(service.login(payload).model_dump())


@router.post('/register')
def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    return ok(service.register(payload).model_dump())
