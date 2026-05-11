from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NatalReading(Base):
    __tablename__ = 'natal_reading'
    __table_args__ = (
        Index('idx_natal_reading_user_profile', 'user_id', 'profile_id'),
        Index('idx_natal_reading_generated_at', 'generated_at'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_natal_reading_user'))
    profile_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('bazi_profile.id', name='fk_natal_reading_profile'))
    reading_no: Mapped[str] = mapped_column(String(32), unique=True)
    content_mode: Mapped[str] = mapped_column(String(16), default='plain')
    generation_mode: Mapped[str] = mapped_column(String(16), default='hybrid')
    personality_text: Mapped[str | None] = mapped_column(Text)
    strengths_text: Mapped[str | None] = mapped_column(Text)
    risks_text: Mapped[str | None] = mapped_column(Text)
    advice_text: Mapped[str | None] = mapped_column(Text)
    summary_text: Mapped[str | None] = mapped_column(Text)
    disclaimer_text: Mapped[str | None] = mapped_column(String(500))
    content_json: Mapped[dict | None] = mapped_column(JSON)
    llm_model: Mapped[str | None] = mapped_column(String(64))
    prompt_version: Mapped[str | None] = mapped_column(String(32))
    review_status: Mapped[str] = mapped_column(String(20), default='approved')
    risk_level: Mapped[str] = mapped_column(String(20), default='low')
    status: Mapped[str] = mapped_column(String(20), default='ready')
    generated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
