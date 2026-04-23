from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountInfoResponse, AccountUpdateRequest, ChangePasswordRequest


class AccountService:
    def __init__(self, repository: AccountRepository) -> None:
        self.repository = repository

    def get_me(self) -> AccountInfoResponse:
        return AccountInfoResponse(**self.repository.get_me())

    def update_me(self, payload: AccountUpdateRequest) -> AccountInfoResponse:
        return AccountInfoResponse(**self.repository.update_me(payload.model_dump()))

    def change_password(self, payload: ChangePasswordRequest) -> None:
        self.repository.change_password(payload.currentPassword, payload.newPassword)

    def upload_avatar(self, filename: str) -> AccountInfoResponse:
        return AccountInfoResponse(**self.repository.save_avatar(filename))
