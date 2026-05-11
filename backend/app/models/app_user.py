from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AppUser(Base):
    __tablename__ = 'app_user'
    __table_args__ = (
        Index('idx_app_user_mobile', 'mobile'),
        Index('idx_app_user_openid', 'wechat_openid'),
        Index('idx_app_user_status', 'status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_no: Mapped[str] = mapped_column(String(32), unique=True)
    login_type: Mapped[str] = mapped_column(String(20))
    mobile: Mapped[str | None] = mapped_column(String(32))
    mobile_masked: Mapped[str | None] = mapped_column(String(32))
    wechat_openid: Mapped[str | None] = mapped_column(String(128))
    nickname: Mapped[str | None] = mapped_column(String(64))
    gender: Mapped[str | None] = mapped_column(String(16))
    email: Mapped[str | None] = mapped_column(String(128))
    password_hash: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(255))
    session_token: Mapped[str | None] = mapped_column(String(128))
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Shanghai')
    status: Mapped[str] = mapped_column(String(20), default='active')
    register_source: Mapped[str | None] = mapped_column(String(32))
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    bound_record_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    password_updated_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
