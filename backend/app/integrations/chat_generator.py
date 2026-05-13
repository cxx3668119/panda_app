from app.schemas.chat_generation import (
    ChatIntroGeneration,
    ChatAnswerGeneration,
)
from app.prompts.chat_prompt import build_first_chat_prompt, build_continue_chat_prompt
from app.clients.ai_client import AiClient
import json


class ChatGenerator:
    def __init__(self):
        self.ai_client = AiClient()

    def generate_intro(self, record: dict) -> ChatIntroGeneration:
        system_prompt, user_prompt = build_first_chat_prompt(record)
        generated = self.ai_client.generate_text(system_prompt, user_prompt)
        print("generated raw repr:", repr(generated))
        data = self._parse_generated_json(generated)
        return ChatIntroGeneration(**data)

    def generate_answer(
        self,
        question: str,
        intro_summary: str,
        record: dict,
        recent_messages: list[dict],
    ) -> ChatAnswerGeneration:
        system_prompt, user_prompt = build_continue_chat_prompt(
            question=question,
            intro_summary=intro_summary,
            record=record,
            recent_messages=recent_messages,
        )
        generated = self.ai_client.generate_text(system_prompt, user_prompt)
        print("generated raw repr:", repr(generated))
        data = self._parse_generated_json(generated)
        return ChatAnswerGeneration(**data)

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
