from __future__ import annotations

from datetime import date
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.passwords import hash_password
from app.models.app_user import AppUser
from app.models.bazi_profile import BaziProfile
from app.repositories.account_repository import ensure_account_columns


def get_or_create_demo_user(db: Session) -> AppUser:
    ensure_account_columns(db)
    user = db.scalar(select(AppUser).where(AppUser.user_no == settings.demo_user_no))
    if user:
        changed = False
        if not user.email:
            user.email = settings.demo_email
            changed = True
        if not user.password_hash:
            user.password_hash = hash_password(settings.demo_password)
            changed = True
        if not user.session_token:
            user.session_token = settings.mock_token
            changed = True
        if changed:
            db.commit()
            db.refresh(user)
        return user
    user = AppUser(
        user_no=settings.demo_user_no,
        login_type='mobile',
        nickname=settings.demo_nickname,
        email=settings.demo_email,
        password_hash=hash_password(settings.demo_password),
        session_token=settings.mock_token,
        timezone='Asia/Shanghai',
        status='active',
    )
    db.add(user)
    db.flush()
    return user


def get_active_profile(db: Session, user_id: int) -> BaziProfile | None:
    return db.scalar(
        select(BaziProfile)
        .where(BaziProfile.user_id == user_id, BaziProfile.is_active.is_(True), BaziProfile.is_deleted.is_(False))
        .order_by(BaziProfile.id.desc())
        .limit(1)
    )


def build_profile_no(user_no: str) -> str:
    return f'{user_no}-{uuid4().hex[:12]}'


def today_local() -> date:
    return date.today()
