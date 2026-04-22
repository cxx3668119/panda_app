from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AiChatSession(Base):
    __tablename__ = 'ai_chat_session'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    profile_id: Mapped[int] = mapped_column(BigInteger)
    session_no: Mapped[str] = mapped_column(String(32), unique=True)
    session_date: Mapped[date] = mapped_column(Date)
    topic: Mapped[str | None] = mapped_column(String(64))
    context_scope: Mapped[str] = mapped_column(String(20), default='today')
    question_count: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(20), default='active')
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
