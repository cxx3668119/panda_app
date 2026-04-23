from datetime import datetime

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BusinessError
from app.db.session import get_db
from app.models.app_user import AppUser
from app.repositories.account_repository import ensure_account_columns
from app.repositories.db_support import get_or_create_demo_user


async def get_current_token(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> str:
    if not authorization:
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    prefix = 'Bearer '
    if not authorization.startswith(prefix):
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    token = authorization[len(prefix):]
    ensure_account_columns(db)
    if token == settings.mock_token:
        user = get_or_create_demo_user(db)
        if user.session_token != settings.mock_token:
            user.session_token = settings.mock_token
            db.commit()
        return token
    user = db.scalar(select(AppUser).where(AppUser.session_token == token))
    if not user:
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    return token


async def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> AppUser:
    await get_current_token(authorization, db)
    token = authorization[len('Bearer '):]
    user = db.scalar(select(AppUser).where(AppUser.session_token == token))
    if user:
        return user
    ensure_account_columns(db)
    demo_user = get_or_create_demo_user(db)
    if demo_user.session_token != settings.mock_token:
        demo_user.session_token = settings.mock_token
        if not demo_user.email:
            demo_user.email = settings.demo_email
        db.commit()
    return demo_user
