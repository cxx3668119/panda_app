from __future__ import annotations
from app.models.app_user import AppUser

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import CalendarType, Gender
from app.models.bazi_profile import BaziProfile
from app.models.natal_reading import NatalReading
from app.repositories.db_support import build_profile_no, get_active_profile, get_or_create_demo_user
from app.repositories.memory_store import DISLAIMER_TEXT


class ProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_profile(self, user: AppUser) -> dict | None:
        profile = get_active_profile(self.db, user.id)
        if not profile:
            return None
        return self._to_profile_response(profile)

    def save_profile(self, payload: dict, user: AppUser) -> dict:
        profile = get_active_profile(self.db, user.id)
        birth_time = payload.get('birthTime') if not payload['birthTimeUnknown'] else None
        birth_date = datetime.strptime(payload['birthDate'], '%Y-%m-%d').date()
        if profile is None:
            profile = BaziProfile(
                user_id=user.id,
                profile_no=build_profile_no(user.user_no),
                gender=self._gender_to_db(payload['gender']),
                calendar_type=self._calendar_to_db(payload['calendarType']),
                birth_date=birth_date,
                birth_time=datetime.strptime(birth_time, '%H:%M').time() if birth_time else None,
                birth_time_unknown=payload['birthTimeUnknown'],
                birth_place_text=payload['birthPlace'],
                timezone=payload['timezone'],
                is_active=True,
                is_deleted=False,
            )
            self.db.add(profile)
            self.db.flush()
        else:
            profile.gender = self._gender_to_db(payload['gender'])
            profile.calendar_type = self._calendar_to_db(payload['calendarType'])
            profile.birth_date = birth_date
            profile.birth_time = datetime.strptime(birth_time, '%H:%M').time() if birth_time else None
            profile.birth_time_unknown = payload['birthTimeUnknown']
            profile.birth_place_text = payload['birthPlace']
            profile.timezone = payload['timezone']
        self._ensure_reading(user.id, profile.id)
        self.db.commit()
        self.db.refresh(profile)
        return self._to_profile_response(profile)

    def get_interpretation(self, user: AppUser) -> dict:
        profile = get_active_profile(self.db, user.id)
        if not profile:
            return {
                'summaryTitle': '请先完成建档',
                'personality': '',
                'strength': '',
                'risk': '',
                'advice': '',
                'fullContent': '',
                'disclaimer': DISLAIMER_TEXT,
            }
        reading = self.db.scalar(
            select(NatalReading)
            .where(
                NatalReading.user_id == user.id,
                NatalReading.profile_id == profile.id,
                NatalReading.is_deleted.is_(False),
            )
            .order_by(NatalReading.id.desc())
            .limit(1)
        )
        if not reading:
            self._ensure_reading(user.id, profile.id)
            self.db.commit()
            reading = self.db.scalar(
                select(NatalReading)
                .where(
                    NatalReading.user_id == user.id,
                    NatalReading.profile_id == profile.id,
                    NatalReading.is_deleted.is_(False),
                )
                .order_by(NatalReading.id.desc())
                .limit(1)
            )
        return {
            'summaryTitle': reading.summary_text or '稳中有冲劲的表达者',
            'personality': reading.personality_text or '',
            'strength': reading.strengths_text or '',
            'risk': reading.risks_text or '',
            'advice': reading.advice_text or '',
            'fullContent': (reading.content_json or {}).get('fullContent') or reading.summary_text or '',
            'disclaimer': reading.disclaimer_text or DISLAIMER_TEXT,
        }

    def _ensure_reading(self, user_id: int, profile_id: int) -> None:
        reading = self.db.scalar(
            select(NatalReading)
            .where(
                NatalReading.user_id == user_id,
                NatalReading.profile_id == profile_id,
                NatalReading.is_deleted.is_(False),
            )
            .limit(1)
        )
        if reading:
            return
        self.db.add(
            NatalReading(
                user_id=user_id,
                profile_id=profile_id,
                reading_no=f'reading-{uuid4().hex[:12]}',
                personality_text='你擅长把复杂问题拆开理解，对信息变化很敏感。',
                strengths_text='适合承担连接信息与组织共识的角色。',
                risks_text='在高压反馈下容易过度预演。',
                advice_text='先对齐目标，再推动动作。',
                summary_text='稳中有冲劲的表达者',
                disclaimer_text=DISLAIMER_TEXT,
                content_json={
                    'fullContent': '这份命盘解读偏向现代职场语境：你的优势是稳定识别关键变量、建立结构、推动对齐。',
                },
                status='ready',
                is_deleted=False,
            )
        )

    def _to_profile_response(self, profile: BaziProfile) -> dict:
        return {
            'calendarType': self._calendar_from_db(profile.calendar_type),
            'birthDate': profile.birth_date.isoformat(),
            'birthTime': profile.birth_time.strftime('%H:%M') if profile.birth_time else None,
            'birthTimeUnknown': profile.birth_time_unknown,
            'gender': self._gender_from_db(profile.gender),
            'birthPlace': profile.birth_place_text or '',
            'timezone': profile.timezone,
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
