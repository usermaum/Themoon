"""
데이터베이스 연결 설정

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/models/database.py
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLAlchemy 엔진 생성
# SQLite와 PostgreSQL 모두 지원
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # 연결 상태 확인
    echo=settings.DEBUG,  # SQL 로그 (디버그 모드에서만)
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성

    FastAPI dependency로 사용:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
