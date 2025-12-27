"""
애플리케이션 설정

환경 변수 기반 설정 관리
"""

import json
import os
from typing import Optional

from pydantic_settings import BaseSettings

# 프로젝트 디렉토리 경로 (모듈 레벨에서 정의)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ROOT_DIR = os.path.dirname(_BASE_DIR)


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 애플리케이션
    APP_NAME: str = "TheMoon API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # 데이터베이스 (개발용 SQLite) - 절대 경로 사용
    DATABASE_URL: str = f"sqlite:///{os.path.join(_ROOT_DIR, 'themoon.db')}"

    # PostgreSQL 사용 시 (프로덕션):
    # DATABASE_URL: str = "postgresql://user:password@localhost/themoon"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3500"]

    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    CONTEXT7_API_KEY: Optional[str] = None

    # Image Processing Settings
    IMAGE_UPLOAD_BASE_DIR: str = "static/uploads/inbound"
    IMAGE_MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    IMAGE_MIN_FREE_DISK_SPACE_GB: int = 5  # 최소 여유 공간

    # Image Quality Profiles
    IMAGE_ORIGINAL_MAX_SIZE: tuple[int, int] = (1600, 2400)
    IMAGE_ORIGINAL_QUALITY: int = 95
    IMAGE_WEBVIEW_MAX_SIZE: tuple[int, int] = (1200, 1800)
    IMAGE_WEBVIEW_QUALITY: int = 85
    IMAGE_THUMBNAIL_MAX_SIZE: tuple[int, int] = (400, 400)
    IMAGE_THUMBNAIL_QUALITY: int = 75

    # Logging
    LOG_FILE_PATH: str = os.path.join(_ROOT_DIR, "logs", "themoon_backend.log")
    FRONTEND_LOG_FILE_PATH: str = os.path.join(_ROOT_DIR, "logs", "themoon_frontend.log")
    MEMO_FILE_PATH: str = os.path.join(_ROOT_DIR, "logs", "dev_memos.json")
    FRONTEND_CACHE_DIR: str = os.path.join(_ROOT_DIR, "frontend", ".next", "cache")

    class Config:
        # 프로젝트 루트의 .env 파일 사용 (모노레포 구조)
        env_file = os.path.join(_ROOT_DIR, ".env")
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
