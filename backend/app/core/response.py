from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = True
    message: str = 'ok'
    data: object | None = None


def ok(data: object | None = None, message: str = 'ok') -> ApiResponse:
    return ApiResponse(success=True, message=message, data=data)
