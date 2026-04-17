from datetime import date

from pydantic import BaseModel, EmailStr


class SendEmailCodeRequest(BaseModel):
    email: EmailStr


class EmailLoginRequest(BaseModel):
    email: EmailStr
    code: str


class LoginUser(BaseModel):
    email: EmailStr
    nickname: str


class LoginResponse(BaseModel):
    token: str
    user: LoginUser
    hasProfile: bool
