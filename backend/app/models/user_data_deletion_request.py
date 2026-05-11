from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserDataDeletionRequest(Base):
    __tablename__ = 'user_data_deletion_request'
    __table_args__ = (
        UniqueConstraint('request_no', name='request_no'),
        Index('idx_user_data_deletion_request_user', 'user_id'),
        Index('idx_user_data_deletion_request_status', 'request_status'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('app_user.id', name='fk_user_data_deletion_request_user'),
    )
    request_no: Mapped[str] = mapped_column(String(32))
    request_status: Mapped[str] = mapped_column(String(20), default='pending')
    request_reason: Mapped[str | None] = mapped_column(String(255))
    submitted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    approved_at: Mapped[datetime | None] = mapped_column(DateTime)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime)
    execution_result: Mapped[str | None] = mapped_column(String(20))
    execution_note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
