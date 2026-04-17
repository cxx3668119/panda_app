from app.repositories.memory_store import clone, state
from app.schemas.auth import LoginResponse, LoginUser


class AuthRepository:
    def send_code(self, email: str) -> dict:
        return {'success': True, 'message': f'验证码已发送至 {email}'}

    def login(self, email: str) -> LoginResponse:
        state['user']['email'] = email
        return LoginResponse(
            token=state['user']['token'],
            user=LoginUser(email=email, nickname=state['user']['nickname']),
            hasProfile=state['profile'] is not None
        )
