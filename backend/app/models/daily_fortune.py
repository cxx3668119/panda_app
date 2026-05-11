from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, JSON, SmallInteger, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DailyFortune(Base):
    __tablename__ = 'daily_fortune'
    __table_args__ = (
        UniqueConstraint('user_id', 'record_id', 'fortune_date', name='uk_daily_fortune'),
        Index('idx_daily_fortune_record_date', 'record_id', 'fortune_date'),
        Index('idx_daily_fortune_user_date', 'user_id', 'fortune_date'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_daily_fortune_user'))
    record_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user_record.id', name='fk_daily_fortune_record'))
    fortune_date: Mapped[date] = mapped_column(Date)
    score: Mapped[int | None] = mapped_column(SmallInteger)
    keyword_tags: Mapped[str | None] = mapped_column(String(255))
    favorable_text: Mapped[str | None] = mapped_column(Text)
    unfavorable_text: Mapped[str | None] = mapped_column(Text)
    advice_text: Mapped[str | None] = mapped_column(Text)
    summary_text: Mapped[str | None] = mapped_column(Text)
    detail_json: Mapped[dict | None] = mapped_column(JSON)
    generation_mode: Mapped[str] = mapped_column(String(16), default='hybrid')
    llm_model: Mapped[str | None] = mapped_column(String(64))
    prompt_version: Mapped[str | None] = mapped_column(String(32))
    review_status: Mapped[str] = mapped_column(String(20), default='approved')
    risk_level: Mapped[str] = mapped_column(String(20), default='low')
    is_fixed: Mapped[bool] = mapped_column(default=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
