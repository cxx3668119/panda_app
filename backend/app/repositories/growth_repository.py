from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_user import AppUser
from app.models.daily_fortune import DailyFortune
from app.models.growth_archive_event import GrowthArchiveEvent


class GrowthRepository:
    def __init__(self, db: Session, user: AppUser) -> None:
        self.db = db
        self.user = user

    def get_archive(self) -> dict:
        events = self.db.scalars(
            select(GrowthArchiveEvent)
            .where(
                GrowthArchiveEvent.user_id == self.user.id,
                GrowthArchiveEvent.is_deleted.is_(False),
            )
            .order_by(GrowthArchiveEvent.event_date.desc(), GrowthArchiveEvent.id.desc())
            .limit(20)
        ).all()
        fortunes = self.db.scalars(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == self.user.id,
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.fortune_date.desc(), DailyFortune.id.desc())
            .limit(7)
        ).all()
        recent_questions = [item.title for item in events if item.event_type == "qa_summary"][:5]
        keyword_counter: Counter[str] = Counter()
        for item in events:
            ext = item.ext_json or {}
            for keyword in ext.get("keywords", []):
                if keyword:
                    keyword_counter[str(keyword)] += 1
        if not keyword_counter:
            for fortune in fortunes:
                for keyword in self._split_keywords(fortune.keyword_tags):
                    keyword_counter[keyword] += 1
        streak_days = 0
        prev_day = None
        for fortune in fortunes:
            if prev_day is None or (prev_day - fortune.fortune_date).days == 1:
                streak_days += 1
                prev_day = fortune.fortune_date
            else:
                break
        summary = events[0].content_text if events else "最近暂时无成长档案数据。"
        recent_fortunes = [
            {
                "date": item.fortune_date.isoformat(),
                "summary": item.summary_text or "",
                "score": item.score or 0,
            }
            for item in fortunes[:3]
        ]
        return {
            "summary": summary,
            "recentQuestions": recent_questions,
            "keywords": [item for item, _ in keyword_counter.most_common(3)],
            "streakDays": streak_days,
            "recentFortunes": recent_fortunes,
        }

    def _split_keywords(self, value: str | None) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in value.replace("，", ",").split(",") if item.strip()]
