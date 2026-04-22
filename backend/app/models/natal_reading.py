from datetime import datetime

from sqlalchemy import BigInteger, DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NatalReading(Base):
    __tablename__ = 'natal_reading'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    profile_id: Mapped[int] = mapped_column(BigInteger)
    reading_no: Mapped[str] = mapped_column(String(32), unique=True)
    personality_text: Mapped[str | None] = mapped_column(Text)
    strengths_text: Mapped[str | None] = mapped_column(Text)
    risks_text: Mapped[str | None] = mapped_column(Text)
    advice_text: Mapped[str | None] = mapped_column(Text)
    summary_text: Mapped[str | None] = mapped_column(Text)
    disclaimer_text: Mapped[str | None] = mapped_column(String(500))
    content_json: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default='ready')
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
