from __future__ import annotations

import json
from datetime import date

from sqlalchemy import MetaData, Table, select
from sqlalchemy.orm import Session

from app.clients.ai_client import AiClient
from app.core.config import settings
from app.models.app_user import AppUser
from app.models.daily_fortune import DailyFortune
from app.models.user_record import UserRecord
from app.prompts.daily_fortune_prompt import build_daily_fortune_prompt
from app.repositories.db_support import (
    get_bound_user_record,
    get_bound_user_record_id,
    today_local,
)
from app.schemas.daily_fortune_generation import DailyFortuneGeneration


class DailyFortuneRepository:
    def __init__(self, db: Session, user: AppUser) -> None:
        self.db = db
        self.user = user

    def get_today(self) -> dict:
        record_id = self.get_bound_user_record_id()
        if not record_id:
            return self._empty_response("请先绑定个人档案并生成运势。")

        existing = self.find_today()
        if existing:
            return existing

        record_info = self.build_generation_context()
        if not record_info:
            return self._empty_response("未找到可用的个人档案信息。")

        system_prompt, user_prompt = build_daily_fortune_prompt(
            record=record_info,
            interpretation_summary="",
            recent_history=[],
            target_date=date.today().isoformat(),
        )

        generated = AiClient().generate_text(system_prompt, user_prompt)
        print("generated raw repr:", repr(generated))

        data = self._parse_generated_json(generated)
        result = DailyFortuneGeneration(**data)
        return self.save_generated_fortune(result)

    def get_history(self) -> list[dict]:
        record_id = self.get_bound_user_record_id()
        if not record_id:
            return []

        fortunes = self.db.scalars(
            select(DailyFortune)
            .where(
                DailyFortune.user_id == self.user.id,
                DailyFortune.record_id == record_id,
                DailyFortune.is_deleted.is_(False),
            )
            .order_by(DailyFortune.fortune_date.desc(), DailyFortune.id.desc())
            .limit(30)
        ).all()
        return [self._to_response(item) for item in fortunes]

    def get_bound_user_record_id(self) -> int | None:
        return get_bound_user_record_id(self.db, self.user.id)

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
            "timezone": self.user.timezone or "Asia/Shanghai",
            "age": record.age,
            "zodiac": record.zodiac,
            "horoscope": record.horoscope,
            "birthZodiacSign": record.birth_zodiac_sign,
        }

    def save_generated_fortune(self, result: DailyFortuneGeneration) -> dict:
        record_id = self.get_bound_user_record_id()
        if not record_id:
            raise ValueError("bound user record missing")

        payload = {
            "user_id": self.user.id,
            "record_id": record_id,
            "fortune_date": today_local(),
            "score": result.score,
            "keyword_tags": ",".join(result.keywords),
            "favorable_text": result.suitable,
            "unfavorable_text": result.caution,
            "advice_text": result.actionAdvice,
            "summary_text": result.summary,
            "detail_json": {"detail": result.detail},
            "generation_mode": "llm",
            "llm_model": settings.ai_model,
            "prompt_version": settings.daily_fortune_prompt_version,
            "review_status": "approved",
            "risk_level": "low",
            "is_fixed": True,
            "is_deleted": False,
            "deleted_at": None,
        }

        daily_fortune_table = Table(
            "daily_fortune",
            MetaData(),
            autoload_with=self.db.get_bind(),
        )

        # 兼容本地仍存在 profile_id 的半迁移数据库。
        if "profile_id" in daily_fortune_table.c:
            payload["profile_id"] = record_id

        insert_payload = {
            key: value for key, value in payload.items() if key in daily_fortune_table.c
        }
        result_proxy = self.db.execute(daily_fortune_table.insert().values(**insert_payload))
        self.db.commit()

        fortune_id = result_proxy.lastrowid
        fortune = self.db.get(DailyFortune, fortune_id) if fortune_id else None
        if not fortune:
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
            raise ValueError("saved daily fortune not found")

        return self._to_response(fortune)

    def _empty_response(self, action_advice: str) -> dict:
        return {
            "date": today_local().isoformat(),
            "score": 0,
            "scoreLabel": "暂无数据",
            "keywords": [],
            "suitable": "暂无数据",
            "caution": "暂无数据",
            "actionAdvice": action_advice,
            "summary": "今天暂无运势数据。",
            "detail": "请先完成档案绑定后再查看今日日运。",
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
        return [item.strip() for item in value.split(",") if item.strip()]

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

        return json.loads(text[start : end + 1])
