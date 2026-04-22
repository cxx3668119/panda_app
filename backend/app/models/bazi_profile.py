from datetime import date, datetime, time

from sqlalchemy import BigInteger, Date, DateTime, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BaziProfile(Base):
    __tablename__ = 'bazi_profile'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    profile_no: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str | None] = mapped_column(String(64))
    gender: Mapped[str] = mapped_column(String(16))
    calendar_type: Mapped[str] = mapped_column(String(16), default='solar')
    birth_date: Mapped[date] = mapped_column(Date)
    birth_time: Mapped[time | None] = mapped_column(Time)
    birth_time_unknown: Mapped[bool] = mapped_column(default=False)
    birth_place_text: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Shanghai')
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
