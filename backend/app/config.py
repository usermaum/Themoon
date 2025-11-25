"""
애플리케이션 설정

환경 변수 기반 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import Optional, Union
import json


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 애플리케이션
    APP_NAME: str = "TheMoon API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # 데이터베이스
    # 환경 변수에서 DATABASE_URL을 읽음 (Render가 자동 제공)
    # 없으면 개발용 SQLite 사용
    DATABASE_URL: str = "sqlite:///./themoon.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # CORS
    # 환경 변수에서 JSON 문자열 또는 리스트로 받음
    # 예: BACKEND_CORS_ORIGINS='["http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: Union[str, list[str]] = ["http://localhost:3000"]

    def get_cors_origins(self) -> list[str]:
        """CORS origins를 리스트로 반환"""
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            try:
                return json.loads(self.BACKEND_CORS_ORIGINS)
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 단일 문자열로 처리
                return [self.BACKEND_CORS_ORIGINS]
        return self.BACKEND_CORS_ORIGINS

    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
