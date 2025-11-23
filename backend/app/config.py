"""
애플리케이션 설정

환경 변수를 통한 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 기본 설정
    PROJECT_NAME: str = "TheMoon API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 데이터베이스
    DATABASE_URL: str = "postgresql://themoon:password@localhost:5432/themoon_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
