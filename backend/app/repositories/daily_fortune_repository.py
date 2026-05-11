from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date
from app.models.app_user import AppUser
from app.models.daily_fortune import DailyFortune
from app.models.user_record import UserRecord
from app.repositories.db_support import (
    get_bound_user_record,
    get_bound_user_record_id,
    today_local,
)
from app.clients.ai_client import AiClient
from app.prompts.daily_fortune_prompt import build_daily_fortune_prompt
from app.schemas.daily_fortune_generation import DailyFortuneGeneration

class DailyFortuneRepository:
    def __init__(self, db: Session, user: AppUser) -> None:
        self.db = db
        self.user = user

    def get_today(self) -> dict:
        user = self.user
        client = AiClient()
        record_id = self.get_bound_user_record_id()
        if not record_id:
            return {
                "date": today_local().isoformat(),
                "score": 0,
                "scoreLabel": "暂无数据",
                "keywords": [],
                "suitable": "暂无数据",
                "caution": "暂无数据",
                "actionAdvice": "请先绑定个人档案并生成运势。",
                "summary": "今天暂无运势数据。",
                "detail": "请先绑定个人档案后再查看今日日运。",
            }

        existing = self.find_today()
        if existing:
            return existing
        record_info = self.build_generation_context()
        if not record_info:
            return {
                "date": today_local().isoformat(),
                "score": 0,
                "scoreLabel": "暂无数据",
                "keywords": [],
                "suitable": "暂无数据",
                "caution": "暂无数据",
                "actionAdvice": "请先绑定个人档案并生成运势。",
                "summary": "今天暂无运势数据。",
                "detail": "请先绑定个人档案后再查看今日日运。",
            }

        system_prompt, user_prompt = build_daily_fortune_prompt(
            record_info, "", [], date.today().isoformat()
        )
        generated = client.generate_text(system_prompt, user_prompt)
        print("generated raw repr:", repr(generated))
        data = self._parse_generated_json(generated)
        result = DailyFortuneGeneration(**data)
        print("Generated fortune parsed:", result.model_dump())
        return {
            "date": today_local().isoformat(),
            "score": result.score,
            "scoreLabel": self._score_label(result.score),
            "keywords": result.keywords,
            "suitable": result.suitable,
            "caution": result.caution,
            "actionAdvice": result.actionAdvice,
            "summary": result.summary,
            "detail": result.detail,
        }

    def get_history(self) -> list[dict]:
        user = self.user
        record_id = self.get_bound_user_record_id()
        if not record_id:
            return []
        fortunes = self.db.scalars(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == user.id,
                DailyFortune.record_id == record_id,
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.fortune_date.desc(), DailyFortune.id.desc())
            .limit(30)
        ).all()
        return [self._to_response(item) for item in fortunes]

    def get_bound_user_record_id(self):
        record_id = get_bound_user_record_id(self.db, self.user.id)
        return record_id

    def get_bound_user_record(self) -> UserRecord | None:
        return get_bound_user_record(self.db, self.user.id)

    def find_today(self) -> dict | None:
        record_id = self.get_bound_user_record_id()
        if not record_id:
            return None
        fortune = self.db.scalar(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == self.user.id,
                DailyFortune.record_id == record_id,
                DailyFortune.fortune_date == today_local(),
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.id.desc())
            .limit(1)
        )
        if not fortune:
            return None
        return self._to_response(fortune)

    def build_generation_context(self) -> dict | None:
        record = self.get_bound_user_record()
        if not record:
            return None
        return {
            "name": record.name,
            "birthDate": record.birthday.date().isoformat(),
            "birthTime": record.birthday.strftime("%H:%M"),
            "birthTimeUnknown": False,
            "gender": record.gender,
            "birthPlace": record.birthplace or "",
            "timezone": self.user.timezone,
            "age": record.age,
            "zodiac": record.zodiac,
            "horoscope": record.horoscope,
            "birthZodiacSign": record.birth_zodiac_sign,
        }

    def _to_response(self, fortune: DailyFortune) -> dict:
        detail_json = fortune.detail_json or {}
        detail_text = (
            detail_json.get("detail") if isinstance(detail_json, dict) else None
        )
        if not detail_text and detail_json:
            detail_text = json.dumps(detail_json, ensure_ascii=False)
        score = fortune.score or 0
        return {
            "date": fortune.fortune_date.isoformat(),
            "score": score,
            "scoreLabel": self._score_label(score),
            "keywords": self._split_keywords(fortune.keyword_tags),
            "suitable": fortune.favorable_text or "",
            "caution": fortune.unfavorable_text or "",
            "actionAdvice": fortune.advice_text or "",
            "summary": fortune.summary_text or "",
            "detail": detail_text or fortune.summary_text or "",
        }

    def _split_keywords(self, value: str | None) -> list[str]:
        if not value:
            return []
        return [
            item.strip() for item in value.replace("，", ",").split(",") if item.strip()
        ]

    def _score_label(self, score: int) -> str:
        if score >= 80:
            return "顺势沟通"
        if score >= 70:
            return "稳定推进"
        if score >= 60:
            return "收束整理"
        return "保持观察"

    def _parse_generated_json(self, generated: str) -> dict:
        if not generated or not generated.strip():
            raise ValueError("AI 返回为空")

        text = generated.strip()
        if text.startswith("```json"):
            text = text.removeprefix("```json").strip()
        if text.startswith("```"):
            text = text.removeprefix("```").strip()
        if text.endswith("```"):
            text = text[:-3].strip()

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError(f"AI 未返回合法 JSON: {generated}")

        json_text = text[start : end + 1]
        return json.loads(json_text)
