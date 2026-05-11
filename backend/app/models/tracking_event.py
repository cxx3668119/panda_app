from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrackingEvent(Base):
    __tablename__ = 'tracking_event'
    __table_args__ = (
        Index('idx_tracking_event_user_time', 'user_id', 'event_time'),
        Index('idx_tracking_event_name_time', 'event_name', 'event_time'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey('app_user.id', name='fk_tracking_event_user'),
    )
    profile_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey('bazi_profile.id', name='fk_tracking_event_profile'),
    )
    session_no: Mapped[str | None] = mapped_column(String(64))
    event_name: Mapped[str] = mapped_column(String(64))
    event_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    page_name: Mapped[str | None] = mapped_column(String(64))
    device_type: Mapped[str | None] = mapped_column(String(32))
    platform_type: Mapped[str | None] = mapped_column(String(32))
    event_props: Mapped[dict | None] = mapped_column(JSON)
    is_sensitive: Mapped[bool] = mapped_column(default=False)
    props_masked: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
