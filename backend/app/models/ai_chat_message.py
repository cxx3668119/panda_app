from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AiChatMessage(Base):
    __tablename__ = 'ai_chat_message'
    __table_args__ = (
        Index('idx_ai_chat_message_session', 'session_id', 'id'),
        Index('idx_ai_chat_message_category', 'question_category'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('ai_chat_session.id', name='fk_ai_chat_message_session'),
    )
    role_type: Mapped[str] = mapped_column(String(16))
    question_category: Mapped[str | None] = mapped_column(String(64))
    content_text: Mapped[str] = mapped_column(Text)
    content_masked: Mapped[str | None] = mapped_column(Text)
    content_encrypted: Mapped[str | None] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(20), default='low')
    hit_sensitive_rule: Mapped[bool] = mapped_column(default=False)
    refusal_type: Mapped[str | None] = mapped_column(String(32))
    review_status: Mapped[str] = mapped_column(String(20), default='approved')
    token_input: Mapped[int | None] = mapped_column(Integer)
    token_output: Mapped[int | None] = mapped_column(Integer)
    model_name: Mapped[str | None] = mapped_column(String(64))
    prompt_version: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
