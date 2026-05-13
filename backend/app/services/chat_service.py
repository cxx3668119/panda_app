from time import time

from app.core.exceptions import BusinessError
from app.integrations.chat_generator import ChatGenerator
from app.repositories.chat_repository import ChatRepository
from app.repositories.memory_store import DISLAIMER_TEXT
from app.repositories.profile_repository import ProfileRepository
from app.schemas.chat import AskAiRequest, ChatMessageResponse, QuotaResponse


class ChatService:
    def __init__(
        self, repository: ChatRepository, profile_repository: ProfileRepository
    ) -> None:
        self.repository = repository
        self.profile_repository = profile_repository

    def get_quota(self) -> QuotaResponse:
        return QuotaResponse(**self.repository.get_quota())

    def get_today_session(self) -> list[ChatMessageResponse]:
        return [ChatMessageResponse(**item) for item in self.repository.get_messages()]

    def get_session(self) -> list[ChatMessageResponse]:
        return [ChatMessageResponse(**item) for item in self.repository.get_messages()]

    def ask(self, payload: AskAiRequest) -> ChatMessageResponse:
        profile = self.profile_repository.get_profile()
        if not profile:
            raise BusinessError('请先完成建档后再体验', status_code=400)
        if profile['birthTimeUnknown']:
            raise BusinessError('出生时辰未知时暂不支持 AI 提问', status_code=400)

        try:
            user_message = {
                'id': int(time() * 1000),
                'role': 'user',
                'content': payload.question,
                'disclaimer': None,
                'rejected': False,
            }
            self.repository.append_message(user_message)

            rejected = '投资' in payload.question
            if rejected:
                answer = {
                    'id': int(time() * 1000) + 1,
                    'role': 'assistant',
                    'content': '当前不提供投资建议，请结合专业意见独立判断。',
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': True,
                }
            else:
                answer = {
                    'id': int(time() * 1000) + 1,
                    'role': 'assistant',
                    'content': f'结合你当前的上下文，问题“{payload.question}”更适合先做信息对齐，再决定是否推进。',
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': False,
                }

            saved_answer = self.repository.append_message(answer)
            self.repository.commit()
            return ChatMessageResponse(**saved_answer)
        except Exception:
            self.repository.rollback()
            raise

    def ask_stream(self, payload: AskAiRequest):
        profile = self.profile_repository.get_profile()
        if not profile:
            raise BusinessError('请先完成建档后再体验', status_code=400)
        if profile['birthTimeUnknown']:
            raise BusinessError('出生时辰未知时暂不支持 AI 提问', status_code=400)

        user_message = {
            'id': int(time() * 1000),
            'role': 'user',
            'content': payload.question,
            'disclaimer': None,
            'rejected': False,
        }
        self.repository.append_message(user_message)

        rejected = '投资' in payload.question
        record = self.repository.get_current_record()
        recent_messages = self.repository.get_recent_messages()
        intro_summary = ''
        for item in recent_messages:
            if item['role'] == 'assistant' and item['content']:
                intro_summary = item['content']
                break

        generator = ChatGenerator()

        def stream_response():
            full_text_parts: list[str] = []
            try:
                if rejected:
                    answer_text = '当前不提供投资建议，请结合专业意见独立判断。'
                    full_text_parts.append(answer_text)
                    yield answer_text
                else:
                    for chunk in generator.stream_answer_text(
                        question=payload.question,
                        intro_summary=intro_summary,
                        record=record,
                        recent_messages=recent_messages,
                    ):
                        full_text_parts.append(chunk)
                        yield chunk

                answer = {
                    'id': int(time() * 1000) + 1,
                    'role': 'assistant',
                    'content': ''.join(full_text_parts),
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': rejected,
                }
                self.repository.append_message(answer)
                self.repository.commit()
            except Exception:
                self.repository.rollback()
                raise

        return stream_response()

    def intro_stream(self):
        record = self.repository.get_current_record()
        if not record:
            raise BusinessError('请先完成建档后再体验', status_code=400)

        recent_messages = self.repository.get_recent_messages()
        if recent_messages:
            def empty_stream():
                if False:
                    yield ''
            return empty_stream()

        generator = ChatGenerator()

        def stream_response():
            full_text_parts: list[str] = []
            try:
                for chunk in generator.stream_intro_text(record):
                    full_text_parts.append(chunk)
                    yield chunk

                answer = {
                    'id': int(time() * 1000) + 1,
                    'role': 'assistant',
                    'content': ''.join(full_text_parts),
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': False,
                }
                self.repository.append_message(answer)
                self.repository.commit()
            except Exception:
                self.repository.rollback()
                raise

        return stream_response()
