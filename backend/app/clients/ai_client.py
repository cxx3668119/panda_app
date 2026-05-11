import json

from openai import OpenAI
from app.core.config import settings


class AiClient:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
        )
        self.model = settings.ai_model

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        try:
            print(
                "AI response dump:",
                json.dumps(response.model_dump(), ensure_ascii=True),
            )
        except Exception as exc:
            print("AI response dump failed:", repr(exc))

        content = response.choices[0].message.content
        try:
            print("AI extracted content repr:", ascii(content))
        except Exception as exc:
            print("AI content debug failed:", repr(exc))
        return content.strip() if content else ""
