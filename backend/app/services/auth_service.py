from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    def login(self, payload: LoginRequest) -> LoginResponse:
        return self.repository.login(str(payload.email), payload.password)

    def register(self, payload: RegisterRequest) -> LoginResponse:
        return self.repository.register(
            nickname=payload.nickname,
            email=str(payload.email),
            password=payload.password,
            timezone=payload.timezone,
            mobile=payload.mobile,
        )
