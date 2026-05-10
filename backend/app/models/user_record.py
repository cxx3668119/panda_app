from datetime import  datetime

from sqlalchemy import BigInteger, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRecord(Base):
    __tablename__ = 'user_record'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)

    name: Mapped[str] = mapped_column(String(64))
    birthday: Mapped[datetime] = mapped_column(DateTime)
    gender: Mapped[str] = mapped_column(String(16))
    birthplace: Mapped[str | None] = mapped_column(String(255))

    age: Mapped[int] = mapped_column(Integer)
    zodiac: Mapped[str] = mapped_column(String(16))
    horoscope: Mapped[str] = mapped_column(String(16))
    birth_zodiac_sign: Mapped[str] = mapped_column(String(16))

    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
