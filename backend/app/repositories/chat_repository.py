from __future__ import annotations

from datetime import datetime
from time import time
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.app_user import AppUser

from app.core.config import settings
from app.models.ai_chat_message import AiChatMessage
from app.models.ai_chat_session import AiChatSession
from app.repositories.db_support import get_active_profile, get_or_create_demo_user, today_local


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_quota(self, user: AppUser) -> dict:
        profile = get_active_profile(self.db, user.id)
        if not profile:
            return {
                'freeLimit': settings.free_chat_limit,
                'freeUsed': 0,
                'paidBalance': 0,
            }
        session = self._get_or_create_today_session(user.id, profile.id)
        user_message_count = self.db.scalar(
            select(func.count(AiChatMessage.id)).where(
                AiChatMessage.session_id == session.id,
                AiChatMessage.role_type == 'user',
            )
        ) or 0
        return {
            'freeLimit': settings.free_chat_limit,
            'freeUsed': int(user_message_count),
            'paidBalance': 0,
        }

    def get_messages(self, user: AppUser) -> list[dict]:
        profile = get_active_profile(self.db, user.id)
        if not profile:
            return []
        session = self._get_or_create_today_session(user.id, profile.id)
        messages = self.db.scalars(
            select(AiChatMessage)
            .where(AiChatMessage.session_id == session.id)
            .order_by(AiChatMessage.id.asc())
        ).all()
        return [self._to_response(item) for item in messages]

    def append_message(self, payload: dict, user: AppUser) -> dict:
        profile = get_active_profile(self.db, user.id)
        if not profile:
            raise ValueError('profile missing')
        session = self._get_or_create_today_session(user.id, profile.id)
        message = AiChatMessage(
            session_id=session.id,
            role_type=payload['role'],
            content_text=payload['content'],
            risk_level='medium' if payload.get('rejected') else 'low',
            hit_sensitive_rule=bool(payload.get('rejected')),
            refusal_type='investment' if payload.get('rejected') else None,
            review_status='approved',
        )
        self.db.add(message)
        self.db.flush()
        if payload['role'] == 'user':
            session.question_count += 1
            self.db.flush()
        return self._to_response(message)

    def update_quota(self, payload: dict) -> dict:
        return payload

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def get_today_profile(self, user: AppUser):
        return get_active_profile(self.db, user.id)

    def _get_or_create_today_session(self, user_id: int, profile_id: int) -> AiChatSession:
        session = self.db.scalar(
            select(AiChatSession)
            .where(
                AiChatSession.user_id == user_id,
                AiChatSession.profile_id == profile_id,
                AiChatSession.session_date == today_local(),
                AiChatSession.is_deleted.is_(False),
            )
            .order_by(AiChatSession.id.desc())
            .limit(1)
        )
        if session:
            return session
        session = AiChatSession(
            user_id=user_id,
            profile_id=profile_id,
            session_no=f'session-{uuid4().hex[:12]}',
            session_date=today_local(),
            context_scope='today',
            question_count=0,
            status='active',
            is_deleted=False,
        )
        self.db.add(session)
        self.db.flush()
        return session

    def _to_response(self, message: AiChatMessage) -> dict:
        return {
            'id': int(message.id if message.id is not None else int(time() * 1000)),
            'role': message.role_type,
            'content': message.content_text,
            'disclaimer': None if message.role_type == 'user' else '本内容仅供娱乐陪伴和自我探索参考，不构成医疗、法律、投资等专业建议，请结合实际情况独立判断。',
            'rejected': bool(message.hit_sensitive_rule) if message.role_type == 'assistant' else False,
        }
