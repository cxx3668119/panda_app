from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_fortune import DailyFortune
from app.repositories.db_support import get_active_profile, get_or_create_demo_user, today_local


class DailyFortuneRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_today(self) -> dict:
        user = get_or_create_demo_user(self.db)
        profile = get_active_profile(self.db, user.id)
        fortune = self.db.scalar(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == user.id,
                DailyFortune.profile_id == (profile.id if profile else -1),
                DailyFortune.fortune_date == today_local(),
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.id.desc())
            .limit(1)
        )
        if fortune:
            return self._to_response(fortune)
        return {
            'date': today_local().isoformat(),
            'score': 0,
            'scoreLabel': '暂无数据',
            'keywords': [],
            'suitable': '暂无数据',
            'caution': '暂无数据',
            'actionAdvice': '请先完成建档并生成运势。',
            'summary': '今天暂无运势数据。',
            'detail': '今天暂无运势数据。',
        }

    def get_history(self) -> list[dict]:
        user = get_or_create_demo_user(self.db)
        profile = get_active_profile(self.db, user.id)
        if not profile:
            return []
        fortunes = self.db.scalars(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == user.id,
                DailyFortune.profile_id == profile.id,
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.fortune_date.desc(), DailyFortune.id.desc())
            .limit(30)
        ).all()
        return [self._to_response(item) for item in fortunes]

    def _to_response(self, fortune: DailyFortune) -> dict:
        detail_json = fortune.detail_json or {}
        detail_text = detail_json.get('detail') if isinstance(detail_json, dict) else None
        if not detail_text and detail_json:
            detail_text = json.dumps(detail_json, ensure_ascii=False)
        score = fortune.score or 0
        return {
            'date': fortune.fortune_date.isoformat(),
            'score': score,
            'scoreLabel': self._score_label(score),
            'keywords': self._split_keywords(fortune.keyword_tags),
            'suitable': fortune.favorable_text or '',
            'caution': fortune.unfavorable_text or '',
            'actionAdvice': fortune.advice_text or '',
            'summary': fortune.summary_text or '',
            'detail': detail_text or fortune.summary_text or '',
        }

    def _split_keywords(self, value: str | None) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in value.replace('，', ',').split(',') if item.strip()]

    def _score_label(self, score: int) -> str:
        if score >= 80:
            return '顺势沟通'
        if score >= 70:
            return '稳定推进'
        if score >= 60:
            return '收束整理'
        return '保持观察'
