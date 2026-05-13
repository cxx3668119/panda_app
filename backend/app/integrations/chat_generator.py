from app.schemas.chat_generation import ChatAnswerGeneration, ChatIntroGeneration
from app.prompts.chat_prompt import (
    build_continue_chat_prompt,
    build_continue_chat_stream_prompt,
    build_first_chat_prompt,
    build_first_chat_stream_prompt,
)
from app.clients.ai_client import AiClient
import json


class ChatGenerator:
    def __init__(self):
        self.ai_client = AiClient()

    def generate_intro(self, record) -> ChatIntroGeneration:
        system_prompt, user_prompt = build_first_chat_prompt(record)
        generated = self.ai_client.generate_text(system_prompt, user_prompt)
        data = self._parse_generated_json(generated)
        return ChatIntroGeneration(**data)

    def stream_intro_text(self, record):
        system_prompt, user_prompt = build_first_chat_stream_prompt(record)
        for chunk in self.ai_client.stream_text(system_prompt, user_prompt):
            yield chunk

    def generate_answer(
        self,
        question: str,
        intro_summary: str,
        record,
        recent_messages: list[dict],
    ) -> ChatAnswerGeneration:
        system_prompt, user_prompt = build_continue_chat_prompt(
            question=question,
            intro_summary=intro_summary,
            record=record,
            recent_messages=recent_messages,
        )
        generated = self.ai_client.generate_text(system_prompt, user_prompt)
        data = self._parse_generated_json(generated)
        return ChatAnswerGeneration(**data)

    def stream_answer_text(
        self,
        question: str,
        intro_summary: str,
        record,
        recent_messages: list[dict],
    ):
        system_prompt, user_prompt = build_continue_chat_stream_prompt(
            question=question,
            intro_summary=intro_summary,
            record=record,
            recent_messages=recent_messages,
        )
        for chunk in self.ai_client.stream_text(system_prompt, user_prompt):
            yield chunk

    def _parse_generated_json(self, generated: str) -> dict:
        if not generated or not generated.strip():
            raise ValueError('AI 返回为空')

        text = generated.strip()

        if text.startswith('```json'):
            text = text.removeprefix('```json').strip()
        if text.startswith('```'):
            text = text.removeprefix('```').strip()
        if text.endswith('```'):
            text = text[:-3].strip()

        start = text.find('{')
        end = text.rfind('}')
        if start == -1 or end == -1 or end < start:
            raise ValueError(f'AI 未返回合法 JSON: {generated}')

        return json.loads(text[start : end + 1])
