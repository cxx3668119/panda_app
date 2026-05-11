from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        password = value.strip()
        if not password:
            raise ValueError('密码不能为空')
        return password


class LoginUser(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    mobile: str | None = None
    timezone: str
    avatarUrl: str | None = None
    status: str


class LoginResponse(BaseModel):
    token: str
    user: LoginUser
    hasProfile: bool


class AccountInfoResponse(LoginUser):
    pass


class AccountUpdateRequest(BaseModel):
    nickname: str
    email: EmailStr
    mobile: str | None = None
    timezone: str

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        nickname = value.strip()
        if not nickname:
            raise ValueError('昵称不能为空')
        if len(nickname) > 32:
            raise ValueError('昵称长度不能超过32个字符')
        return nickname

    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, value: str | None) -> str | None:
        if value is None:
            return None
        mobile = value.strip()
        return mobile or None

    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        timezone = value.strip()
        if not timezone:
            raise ValueError('时区不能为空')
        return timezone


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str

    @field_validator('currentPassword', 'newPassword')
    @classmethod
    def validate_password_fields(cls, value: str) -> str:
        password = value.strip()
        if len(password) < 6:
            raise ValueError('密码长度不能少于6位')
        return password


class SetCurrentRecordRequest(BaseModel):
    recordId: int