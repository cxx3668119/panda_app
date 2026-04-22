from time import time

from app.core.exceptions import BusinessError
from app.repositories.chat_repository import ChatRepository
from app.repositories.memory_store import DISLAIMER_TEXT
from app.repositories.profile_repository import ProfileRepository
from app.schemas.chat import AskAiRequest, ChatMessageResponse, QuotaResponse


class ChatService:
    def __init__(self, repository: ChatRepository, profile_repository: ProfileRepository) -> None:
        self.repository = repository
        self.profile_repository = profile_repository

    def get_quota(self) -> QuotaResponse:
        return QuotaResponse(**self.repository.get_quota())

    def get_today_session(self) -> list[ChatMessageResponse]:
        return [ChatMessageResponse(**item) for item in self.repository.get_messages()]

    def ask(self, payload: AskAiRequest) -> ChatMessageResponse:
        profile = self.profile_repository.get_profile()
        if not profile:
            raise BusinessError('请先完成建档后再体验', status_code=400)
        if profile['birthTimeUnknown']:
            raise BusinessError('未知时辰暂不支持 AI 提问', status_code=400)

        quota = self.repository.get_quota()
        remain = quota['freeLimit'] - quota['freeUsed'] + quota['paidBalance']
        if remain <= 0:
            raise BusinessError('免费次数已用完，可购买更多提问次数', status_code=400)

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
                    'content': '当前不提供投资建议，请结合专业意见判断。',
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': True,
                }
            else:
                answer = {
                    'id': int(time() * 1000) + 1,
                    'role': 'assistant',
                    'content': f'结合你当天的上下文，问题“{payload.question}”更适合先做信息对齐，再决定是否推进。',
                    'disclaimer': DISLAIMER_TEXT,
                    'rejected': False,
                }
                if quota['freeUsed'] < quota['freeLimit']:
                    quota['freeUsed'] += 1
                elif quota['paidBalance'] > 0:
                    quota['paidBalance'] -= 1
                self.repository.update_quota(quota)

            saved_answer = self.repository.append_message(answer)
            self.repository.commit()
            return ChatMessageResponse(**saved_answer)
        except Exception:
            self.repository.rollback()
            raise
