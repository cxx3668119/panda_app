from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.db_support import get_active_profile, get_or_create_demo_user
from app.schemas.auth import LoginResponse, LoginUser


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def send_code(self, email: str) -> dict:
        return {'success': True, 'message': f'验证码已发送至 {email}'}

    def login(self, email: str) -> LoginResponse:
        user = get_or_create_demo_user(self.db)
        profile = get_active_profile(self.db, user.id)
        self.db.commit()
        nickname = user.nickname or '今日宜推进'
        return LoginResponse(
            token='mock-token',
            user=LoginUser(email=email, nickname=nickname),
            hasProfile=profile is not None,
        )
