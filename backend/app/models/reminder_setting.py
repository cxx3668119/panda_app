from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReminderSetting(Base):
    __tablename__ = 'reminder_setting'
    __table_args__ = (
        UniqueConstraint('user_id', 'channel_type', name='uk_reminder_setting'),
        Index('idx_reminder_setting_user_enabled', 'user_id', 'is_enabled'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_reminder_setting_user'))
    channel_type: Mapped[str] = mapped_column(String(20))
    reminder_time: Mapped[str] = mapped_column(String(8), default='09:00')
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Shanghai')
    frequency_type: Mapped[str] = mapped_column(String(20), default='daily')
    is_enabled: Mapped[bool] = mapped_column(default=True)
    quiet_days: Mapped[int] = mapped_column(Integer, default=0)
    last_sent_at: Mapped[datetime | None] = mapped_column(DateTime)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
