from datetime import date, datetime, time

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Integer, JSON, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BaziProfile(Base):
    __tablename__ = 'bazi_profile'
    __table_args__ = (
        Index('idx_bazi_profile_user', 'user_id'),
        Index('idx_bazi_profile_user_active', 'user_id', 'is_active'),
        Index('idx_bazi_profile_deleted', 'is_deleted'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('app_user.id', name='fk_bazi_profile_user'))
    profile_no: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str | None] = mapped_column(String(64))
    gender: Mapped[str] = mapped_column(String(16))
    calendar_type: Mapped[str] = mapped_column(String(16), default='solar')
    birth_date: Mapped[date] = mapped_column(Date)
    birth_time: Mapped[time | None] = mapped_column(Time)
    birth_time_unknown: Mapped[bool] = mapped_column(default=False)
    birth_country: Mapped[str | None] = mapped_column(String(64))
    birth_province: Mapped[str | None] = mapped_column(String(64))
    birth_city: Mapped[str | None] = mapped_column(String(64))
    birth_place_text: Mapped[str | None] = mapped_column(String(255))
    birth_place_masked: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Shanghai')
    birth_date_encrypted: Mapped[str | None] = mapped_column(Text)
    birth_time_encrypted: Mapped[str | None] = mapped_column(Text)
    birth_place_encrypted: Mapped[str | None] = mapped_column(Text)
    bazi_chart_json: Mapped[dict | None] = mapped_column(JSON)
    chart_source: Mapped[str | None] = mapped_column(String(32))
    chart_version: Mapped[str | None] = mapped_column(String(32))
    version_no: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
