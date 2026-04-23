from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'AI八字算命助手 Backend'
    api_prefix: str = '/api/v1'
    mock_token: str = 'mock-token'
    database_url: str = 'mysql+pymysql://root:88888888@127.0.0.1:3306/panda_app?charset=utf8mb4'
    demo_user_no: str = 'demo-user'
    demo_nickname: str = '今日宜推进'
    demo_email: str = 'demo@example.com'
    demo_password: str = '123456'
    free_chat_limit: int = 3
    upload_dir: str = 'uploads'
    avatar_dir: str = 'uploads/avatars'
    avatar_max_bytes: int = 2 * 1024 * 1024


settings = Settings()
