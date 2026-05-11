from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReminderSendLog(Base):
    __tablename__ = 'reminder_send_log'
    __table_args__ = (
        Index('idx_reminder_send_log_user_time', 'user_id', 'plan_send_at'),
        Index('idx_reminder_send_log_status', 'send_status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    reminder_setting_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('reminder_setting.id', name='fk_reminder_send_log_setting'),
    )
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_reminder_send_log_user'))
    channel_type: Mapped[str] = mapped_column(String(20))
    plan_send_at: Mapped[datetime] = mapped_column(DateTime)
    actual_send_at: Mapped[datetime | None] = mapped_column(DateTime)
    send_status: Mapped[str] = mapped_column(String(20), default='pending')
    fail_reason: Mapped[str | None] = mapped_column(String(255))
    provider_message_id: Mapped[str | None] = mapped_column(String(128))
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
