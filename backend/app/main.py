from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.account import router as account_router
from app.api.v1.ai_chat import router as ai_router
from app.api.v1.auth import router as auth_router
from app.api.v1.daily_fortune import router as daily_fortune_router
from app.api.v1.growth_archive import router as growth_archive_router
from app.api.v1.profile import router as profile_router
from app.api.v1.reminder import router as reminder_router
from app.api.v1.user_record import router as user_record_router

from app.core.config import settings
from app.core.exceptions import BusinessError


app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5173', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount('/uploads', StaticFiles(directory=settings.upload_dir), name='uploads')


@app.exception_handler(BusinessError)
async def handle_business_error(_: Request, exc: BusinessError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'message': exc.message,
            'data': None,
        },
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    first_error = exc.errors()[0] if exc.errors() else None
    message = first_error.get('msg', '请求参数校验失败') if first_error else '请求参数校验失败'
    return JSONResponse(
        status_code=422,
        content={
            'success': False,
            'message': message,
            'data': None,
        },
    )


@app.get('/health')
def health_check() -> dict:
    return {
        'success': True,
        'message': 'ok',
        'data': {
            'status': 'healthy',
        },
    }


app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(account_router, prefix=settings.api_prefix)
app.include_router(profile_router, prefix=settings.api_prefix)
app.include_router(daily_fortune_router, prefix=settings.api_prefix)
app.include_router(ai_router, prefix=settings.api_prefix)
app.include_router(growth_archive_router, prefix=settings.api_prefix)
app.include_router(reminder_router, prefix=settings.api_prefix)
app.include_router(user_record_router, prefix=settings.api_prefix)