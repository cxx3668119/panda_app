from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BusinessError
from app.core.passwords import hash_password, verify_password
from app.models.app_user import AppUser


class AccountRepository:
    def __init__(self, db: Session, user: AppUser) -> None:
        self.db = db
        self.user = user

    def get_me(self) -> dict:
        return self._to_response(self.user)

    def update_me(self, payload: dict) -> dict:
        conditions = [AppUser.email == payload['email']]
        mobile = payload.get('mobile')
        if mobile:
            conditions.append(AppUser.mobile == mobile)
        conflict = self.db.scalar(
            select(AppUser).where(AppUser.id != self.user.id, or_(*conditions))
        )
        if conflict:
            raise BusinessError('邮箱或手机号已被其他账号使用', status_code=400)
        self.user.nickname = payload['nickname']
        self.user.email = payload['email']
        self.user.mobile = mobile
        self.user.timezone = payload['timezone']
        self.db.commit()
        self.db.refresh(self.user)
        return self._to_response(self.user)

    def change_password(self, current_password: str, new_password: str) -> None:
        if not verify_password(current_password, self.user.password_hash):
            raise BusinessError('当前密码不正确', status_code=400)
        self.user.password_hash = hash_password(new_password)
        self.user.password_updated_at = datetime.utcnow()
        self.db.commit()

    def save_avatar(self, filename: str) -> dict:
        self.user.avatar_url = f'/uploads/avatars/{filename}'
        self.db.commit()
        self.db.refresh(self.user)
        return self._to_response(self.user)

    def _to_response(self, user: AppUser) -> dict:
        return {
            'id': user.id,
            'email': user.email or settings.demo_email,
            'nickname': user.nickname or settings.demo_nickname,
            'mobile': user.mobile,
            'timezone': user.timezone,
            'avatarUrl': user.avatar_url,
            'status': user.status,
        }
