"""
애플리케이션 설정

환경 변수 기반 설정 관리
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
import json


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
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """JSON 문자열 또는 리스트를 파싱"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(',')]
        return v

    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
