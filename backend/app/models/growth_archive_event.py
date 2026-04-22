from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GrowthArchiveEvent(Base):
    __tablename__ = 'growth_archive_event'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    profile_id: Mapped[int | None] = mapped_column(BigInteger)
    event_type: Mapped[str] = mapped_column(String(32))
    event_date: Mapped[date] = mapped_column(Date)
    title: Mapped[str] = mapped_column(String(128))
    content_text: Mapped[str | None] = mapped_column(Text)
    ext_json: Mapped[dict | None] = mapped_column(JSON)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
