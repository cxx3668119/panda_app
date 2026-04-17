from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = 'AI八字算命助手 Backend'
    api_prefix: str = '/api/v1'
    mock_token: str = 'mock-token'


settings = Settings()
