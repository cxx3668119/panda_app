from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import CalendarType, Gender
from app.core.record_utils import calculate_age, calculate_horoscope, calculate_zodiac
from app.models.app_user import AppUser
from app.models.bazi_profile import BaziProfile
from app.models.natal_reading import NatalReading
from app.models.user_record import UserRecord
from app.repositories.db_support import (
    build_profile_no,
    get_bound_or_latest_user_record,
    get_profile_by_record_id,
)
from app.repositories.memory_store import DISLAIMER_TEXT


class ProfileRepository:
    def __init__(self, db: Session, user: AppUser) -> None:
        self.db = db
        self.user = user

    def get_profile(self) -> dict | None:
        record = self._get_current_record()
        if not record:
            return None
        profile = get_profile_by_record_id(self.db, self.user.id, record.id)
        return self._to_profile_response(record, profile)

    def save_profile(self, payload: dict) -> dict:
        record = self._upsert_record(payload)
        profile = self._upsert_profile(record, payload)
        self._ensure_reading(profile.id)
        self.db.commit()
        self.db.refresh(record)
        self.db.refresh(profile)
        return self._to_profile_response(record, profile)

    def get_interpretation(self) -> dict:
        record = self._get_current_record()
        if not record:
            return {
                "summaryTitle": "请先完成建档",
                "personality": "",
                "strength": "",
                "risk": "",
                "advice": "",
                "fullContent": "",
                "disclaimer": DISLAIMER_TEXT,
            }

        profile = self._ensure_profile_for_record(record)
        reading = self.db.scalar(
            select(NatalReading)
            .where(
                NatalReading.user_id == self.user.id,
                NatalReading.profile_id == profile.id,
                NatalReading.is_deleted.is_(False),
            )
            .order_by(NatalReading.id.desc())
            .limit(1)
        )
        if not reading:
            self._ensure_reading(profile.id)
            self.db.commit()
            reading = self.db.scalar(
                select(NatalReading)
                .where(
                    NatalReading.user_id == self.user.id,
                    NatalReading.profile_id == profile.id,
                    NatalReading.is_deleted.is_(False),
                )
                .order_by(NatalReading.id.desc())
                .limit(1)
            )

        return {
            "summaryTitle": reading.summary_text or "稳中有冲劲的表达者",
            "personality": reading.personality_text or "",
            "strength": reading.strengths_text or "",
            "risk": reading.risks_text or "",
            "advice": reading.advice_text or "",
            "fullContent": (reading.content_json or {}).get("fullContent") or reading.summary_text or "",
            "disclaimer": reading.disclaimer_text or DISLAIMER_TEXT,
        }

    def _get_current_record(self) -> UserRecord | None:
        return get_bound_or_latest_user_record(self.db, self.user.id)

    def _upsert_record(self, payload: dict) -> UserRecord:
        birth_time_unknown = payload["birthTimeUnknown"]
        birth_time = payload.get("birthTime") if not birth_time_unknown else None
        birthday = datetime.strptime(payload["birthDate"], "%Y-%m-%d")
        if birth_time:
            time_part = datetime.strptime(birth_time, "%H:%M").time()
            birthday = birthday.replace(hour=time_part.hour, minute=time_part.minute)

        zodiac = calculate_zodiac(birthday)
        record = self._get_current_record()
        if record is None:
            record = UserRecord(
                user_id=self.user.id,
                name=self.user.nickname or "默认档案",
                birthday=birthday,
                gender=self._gender_to_db(payload["gender"]),
                birthplace=payload["birthPlace"],
                age=calculate_age(birthday),
                zodiac=zodiac,
                horoscope=calculate_horoscope(birthday),
                birth_zodiac_sign=zodiac,
                is_deleted=False,
            )
            self.db.add(record)
            self.db.flush()
            self.user.bound_record_id = record.id
            self.user.timezone = payload["timezone"]
            return record

        record.birthday = birthday
        record.gender = self._gender_to_db(payload["gender"])
        record.birthplace = payload["birthPlace"]
        record.age = calculate_age(birthday)
        record.zodiac = zodiac
        record.horoscope = calculate_horoscope(birthday)
        record.birth_zodiac_sign = zodiac
        if not self.user.bound_record_id:
            self.user.bound_record_id = record.id
        self.user.timezone = payload["timezone"]
        return record

    def _ensure_profile_for_record(self, record: UserRecord) -> BaziProfile:
        profile = get_profile_by_record_id(self.db, self.user.id, record.id)
        if profile:
            return profile

        profile = BaziProfile(
            user_id=self.user.id,
            active_record_id=record.id,
            profile_no=build_profile_no(self.user.user_no),
            name=record.name,
            gender=str(record.gender).lower(),
            calendar_type=self._calendar_to_db(CalendarType.SOLAR),
            birth_date=record.birthday.date(),
            birth_time=record.birthday.time(),
            birth_time_unknown=False,
            birth_place_text=record.birthplace,
            timezone=self.user.timezone,
            is_active=True,
            is_deleted=False,
        )
        self.db.add(profile)
        self.db.flush()
        return profile

    def _upsert_profile(self, record: UserRecord, payload: dict) -> BaziProfile:
        profile = self._ensure_profile_for_record(record)
        birth_time = payload.get("birthTime") if not payload["birthTimeUnknown"] else None
        profile.active_record_id = record.id
        profile.name = record.name
        profile.gender = self._gender_to_db(payload["gender"])
        profile.calendar_type = self._calendar_to_db(payload["calendarType"])
        profile.birth_date = record.birthday.date()
        profile.birth_time = datetime.strptime(birth_time, "%H:%M").time() if birth_time else None
        profile.birth_time_unknown = payload["birthTimeUnknown"]
        profile.birth_place_text = payload["birthPlace"]
        profile.timezone = payload["timezone"]
        profile.is_active = True
        profile.is_deleted = False
        return profile

    def _ensure_reading(self, profile_id: int) -> None:
        reading = self.db.scalar(
            select(NatalReading)
            .where(
                NatalReading.user_id == self.user.id,
                NatalReading.profile_id == profile_id,
                NatalReading.is_deleted.is_(False),
            )
            .limit(1)
        )
        if reading:
            return

        self.db.add(
            NatalReading(
                user_id=self.user.id,
                profile_id=profile_id,
                reading_no=f"reading-{uuid4().hex[:12]}",
                personality_text="你擅长把复杂问题拆开理解，对信息变化很敏感。",
                strengths_text="适合承担连接信息与组织共识的角色。",
                risks_text="在高压反馈下容易过度预演。",
                advice_text="先对齐目标，再推动动作。",
                summary_text="稳中有冲劲的表达者",
                disclaimer_text=DISLAIMER_TEXT,
                content_json={
                    "fullContent": "这份命盘解读偏向现代职场语境：你的优势是稳定识别关键变量、建立结构、推动对齐。",
                },
                status="ready",
                is_deleted=False,
            )
        )

    def _to_profile_response(self, record: UserRecord, profile: BaziProfile | None) -> dict:
        return {
            "calendarType": self._calendar_from_db(profile.calendar_type if profile else "solar"),
            "birthDate": record.birthday.date().isoformat(),
            "birthTime": None if profile and profile.birth_time_unknown else record.birthday.strftime("%H:%M"),
            "birthTimeUnknown": profile.birth_time_unknown if profile else False,
            "gender": self._gender_from_db(str(record.gender)),
            "birthPlace": record.birthplace or "",
            "timezone": profile.timezone if profile and profile.timezone else self.user.timezone,
        }

    def _calendar_to_db(self, value: CalendarType | str) -> str:
        raw = value.value if isinstance(value, CalendarType) else str(value)
        return raw.lower()

    def _calendar_from_db(self, value: str) -> CalendarType:
        return CalendarType(value.upper())

    def _gender_to_db(self, value: Gender | str) -> str:
        raw = value.value if isinstance(value, Gender) else str(value)
        return raw.lower()

    def _gender_from_db(self, value: str) -> Gender:
        return Gender(value.upper())
