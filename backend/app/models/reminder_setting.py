from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReminderSetting(Base):
    __tablename__ = 'reminder_setting'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    channel_type: Mapped[str] = mapped_column(String(20))
    reminder_time: Mapped[str] = mapped_column(String(8), default='09:00')
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Shanghai')
    frequency_type: Mapped[str] = mapped_column(String(20), default='daily')
    is_enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
