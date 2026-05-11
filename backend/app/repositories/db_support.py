from __future__ import annotations

from datetime import date
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.passwords import hash_password
from app.models.app_user import AppUser
from app.models.bazi_profile import BaziProfile
from app.models.user_record import UserRecord


def get_or_create_demo_user(db: Session) -> AppUser:
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
        login_type="mobile",
        nickname=settings.demo_nickname,
        email=settings.demo_email,
        password_hash=hash_password(settings.demo_password),
        session_token=settings.mock_token,
        timezone="Asia/Shanghai",
        status="active",
    )
    db.add(user)
    db.flush()
    return user


def get_active_profile(db: Session, user_id: int) -> BaziProfile | None:
    return db.scalar(
        select(BaziProfile)
        .where(
            BaziProfile.user_id == user_id,
            BaziProfile.active_record_id.is_not(None),
            BaziProfile.is_active.is_(True),
            BaziProfile.is_deleted.is_(False),
        )
        .order_by(BaziProfile.id.desc())
        .limit(1)
    )


def get_bound_user_record_id(db: Session, user_id: int) -> int | None:
    return db.scalar(
        select(AppUser.bound_record_id)
        .where(
            AppUser.id == user_id,
            AppUser.status == "active",
        )
        .limit(1)
    )


def get_bound_user_record(db: Session, user_id: int) -> UserRecord | None:
    record_id = get_bound_user_record_id(db, user_id)
    if not record_id:
        return None
    return db.scalar(
        select(UserRecord)
        .where(
            UserRecord.id == record_id,
            UserRecord.user_id == user_id,
            UserRecord.is_deleted.is_(False),
        )
        .limit(1)
    )


def build_profile_no(user_no: str) -> str:
    return f"{user_no}-{uuid4().hex[:12]}"


def today_local() -> date:
    return date.today()
