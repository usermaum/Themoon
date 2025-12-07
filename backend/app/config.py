"""
애플리케이션 설정

환경 변수 기반 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import Optional
import json
import os


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 애플리케이션
    APP_NAME: str = "TheMoon API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # 데이터베이스 (개발용 SQLite)
    DATABASE_URL: str = "sqlite:///./themoon.db"

    # PostgreSQL 사용 시 (프로덕션):
    # DATABASE_URL: str = "postgresql://user:password@localhost/themoon"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3500"]

    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    CONTEXT7_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # CORS origins를 문자열에서 리스트로 변환 (Render.com 환경변수 처리)
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS")
        if cors_origins and isinstance(cors_origins, str):
            try:
                self.BACKEND_CORS_ORIGINS = json.loads(cors_origins)
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 단일 origin으로 처리
                self.BACKEND_CORS_ORIGINS = [cors_origins]


settings = Settings()
