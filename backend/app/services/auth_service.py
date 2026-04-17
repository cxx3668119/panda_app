from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import EmailLoginRequest, LoginResponse, SendEmailCodeRequest


class AuthService:
    def __init__(self) -> None:
        self.repository = AuthRepository()

    def send_email_code(self, payload: SendEmailCodeRequest) -> dict:
        return self.repository.send_code(str(payload.email))

    def login_by_email(self, payload: EmailLoginRequest) -> LoginResponse:
        return self.repository.login(str(payload.email))
