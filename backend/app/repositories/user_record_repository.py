from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_record import UserRecord
from datetime import datetime
class UserRecordRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        name: str,
        birthday: datetime,
        gender: str,
        birthplace: str | None,
        age: int,
        zodiac: str,
        horoscope: str,
        birth_zodiac_sign: str,
    ) -> UserRecord:
        record = UserRecord(
            user_id=user_id,
            name=name,
            birthday=birthday,
            gender=gender,
            birthplace=birthplace,
            age=age,
            zodiac=zodiac,
            horoscope=horoscope,
            birth_zodiac_sign=birth_zodiac_sign,
            is_deleted=False,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_by_user(self, user_id: int) -> list[UserRecord]:
        return list(
            self.db.scalars(
                select(UserRecord)
                .where(
                    UserRecord.user_id == user_id,
                    UserRecord.is_deleted.is_(False),
                )
                .order_by(UserRecord.id.desc())
            ).all()
        )
