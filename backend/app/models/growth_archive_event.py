from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GrowthArchiveEvent(Base):
    __tablename__ = 'growth_archive_event'
    __table_args__ = (
        Index('idx_growth_archive_event_user_date', 'user_id', 'event_date'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_growth_archive_event_user'))
    profile_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey('bazi_profile.id', name='fk_growth_archive_event_profile'),
    )
    event_type: Mapped[str] = mapped_column(String(32))
    event_date: Mapped[date] = mapped_column(Date)
    title: Mapped[str] = mapped_column(String(128))
    content_text: Mapped[str | None] = mapped_column(Text)
    ext_json: Mapped[dict | None] = mapped_column(JSON)
    source_type: Mapped[str | None] = mapped_column(String(32))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
