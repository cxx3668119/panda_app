from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RiskAuditLog(Base):
    __tablename__ = 'risk_audit_log'
    __table_args__ = (
        Index('idx_risk_audit_log_biz', 'biz_type', 'biz_id'),
        Index('idx_risk_audit_log_user', 'user_id'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    biz_type: Mapped[str] = mapped_column(String(32))
    biz_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int | None] = mapped_column(BigInteger)
    risk_level: Mapped[str] = mapped_column(String(20))
    rule_code: Mapped[str | None] = mapped_column(String(64))
    rule_name: Mapped[str | None] = mapped_column(String(128))
    hit_text: Mapped[str | None] = mapped_column(Text)
    action_type: Mapped[str] = mapped_column(String(20))
    audit_result: Mapped[str] = mapped_column(String(20))
    reviewer: Mapped[str | None] = mapped_column(String(64))
    review_note: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
