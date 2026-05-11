from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.app_user import AppUser

from app.core.enums import ReminderChannel
from app.models.reminder_setting import ReminderSetting
from app.repositories.db_support import get_or_create_demo_user


class ReminderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_settings(self, user: AppUser) -> dict:
        setting = self.db.scalar(
            select(ReminderSetting)
            .where(ReminderSetting.user_id == user.id, ReminderSetting.channel_type == 'in_app')
            .order_by(ReminderSetting.id.desc())
            .limit(1)
        )
        if not setting:
            return {
                'enabled': True,
                'channel': ReminderChannel.IN_APP,
                'time': '09:00',
                'timezone': user.timezone,
            }
        return self._to_response(setting)

    def save_settings(self, payload: dict, user: AppUser) -> dict:
        setting = self.db.scalar(
            select(ReminderSetting)
            .where(ReminderSetting.user_id == user.id, ReminderSetting.channel_type == 'in_app')
            .order_by(ReminderSetting.id.desc())
            .limit(1)
        )
        if setting is None:
            setting = ReminderSetting(
                user_id=user.id,
                channel_type='in_app',
                reminder_time=payload['time'],
                timezone=payload['timezone'],
                frequency_type='daily',
                is_enabled=payload['enabled'],
            )
            self.db.add(setting)
        else:
            setting.reminder_time = payload['time']
            setting.timezone = payload['timezone']
            setting.is_enabled = payload['enabled']
        self.db.commit()
        self.db.refresh(setting)
        return self._to_response(setting)

    def _to_response(self, setting: ReminderSetting) -> dict:
        return {
            'enabled': setting.is_enabled,
            'channel': ReminderChannel.IN_APP,
            'time': setting.reminder_time,
            'timezone': setting.timezone,
        }
