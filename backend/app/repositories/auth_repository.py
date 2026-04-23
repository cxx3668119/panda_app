from __future__ import annotations

from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BusinessError
from app.core.passwords import hash_password, verify_password
from app.core.tokens import generate_session_token
from app.models.app_user import AppUser
from app.repositories.account_repository import ensure_account_columns
from app.repositories.db_support import get_active_profile, get_or_create_demo_user
from app.schemas.auth import LoginResponse, LoginUser


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        ensure_account_columns(self.db)

    def login(self, email: str, password: str) -> LoginResponse:
        self._ensure_demo_user_account()
        user = self.db.scalar(select(AppUser).where(AppUser.email == email))
        if not user or not verify_password(password, user.password_hash):
            raise BusinessError('邮箱或密码错误', status_code=401)
        user.session_token = generate_session_token()
        profile = get_active_profile(self.db, user.id)
        self.db.commit()
        self.db.refresh(user)
        return self._build_login_response(user, profile is not None)

    def register(self, nickname: str, email: str, password: str, timezone: str, mobile: str | None) -> LoginResponse:
        self._ensure_demo_user_account()
        conditions = [AppUser.email == email]
        if mobile:
            conditions.append(AppUser.mobile == mobile)
        conflict = self.db.scalar(select(AppUser).where(or_(*conditions)))
        if conflict:
            raise BusinessError('邮箱或手机号已被其他账号使用', status_code=400)
        user = AppUser(
            user_no=f'user-{uuid4().hex[:12]}',
            login_type='mobile',
            nickname=nickname,
            email=email,
            mobile=mobile,
            password_hash=hash_password(password),
            session_token=generate_session_token(),
            timezone=timezone,
            status='active',
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self._build_login_response(user, False)

    def _build_login_response(self, user: AppUser, has_profile: bool) -> LoginResponse:
        return LoginResponse(
            token=user.session_token or '',
            user=LoginUser(
                id=user.id,
                email=user.email or settings.demo_email,
                nickname=user.nickname or settings.demo_nickname,
                mobile=user.mobile,
                timezone=user.timezone,
                avatarUrl=user.avatar_url,
                status=user.status,
            ),
            hasProfile=has_profile,
        )

    def _ensure_demo_user_account(self) -> None:
        user = get_or_create_demo_user(self.db)
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
            self.db.commit()
