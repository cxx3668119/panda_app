from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, JSON, SmallInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DailyFortune(Base):
    __tablename__ = 'daily_fortune'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    profile_id: Mapped[int] = mapped_column(BigInteger)
    fortune_date: Mapped[date] = mapped_column(Date)
    score: Mapped[int | None] = mapped_column(SmallInteger)
    keyword_tags: Mapped[str | None] = mapped_column(String(255))
    favorable_text: Mapped[str | None] = mapped_column(Text)
    unfavorable_text: Mapped[str | None] = mapped_column(Text)
    advice_text: Mapped[str | None] = mapped_column(Text)
    summary_text: Mapped[str | None] = mapped_column(Text)
    detail_json: Mapped[dict | None] = mapped_column(JSON)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
