from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AiChatMessage(Base):
    __tablename__ = 'ai_chat_message'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(BigInteger)
    role_type: Mapped[str] = mapped_column(String(16))
    question_category: Mapped[str | None] = mapped_column(String(64))
    content_text: Mapped[str] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(20), default='low')
    hit_sensitive_rule: Mapped[bool] = mapped_column(default=False)
    refusal_type: Mapped[str | None] = mapped_column(String(32))
    review_status: Mapped[str] = mapped_column(String(20), default='approved')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
