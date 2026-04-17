from fastapi import Header

from app.core.config import settings
from app.core.exceptions import BusinessError


async def get_current_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    prefix = 'Bearer '
    if not authorization.startswith(prefix):
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    token = authorization[len(prefix):]
    if token != settings.mock_token:
        raise BusinessError('登录状态已失效，请重新登录', status_code=401)
    return token
