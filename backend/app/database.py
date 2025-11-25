"""
데이터베이스 연결 설정

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/models/database.py
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# PostgreSQL URL이 postgres://로 시작하면 postgresql://로 변경
# (일부 오래된 라이브러리 호환성 문제)
database_url = settings.DATABASE_URL
print(f"🔗 Original DATABASE_URL: {database_url[:50]}...")  # 보안을 위해 일부만 출력

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    print(f"✅ Converted to: postgresql://...")

# SQLite인 경우 connect_args 추가
connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    print("📁 Using SQLite database")
elif database_url.startswith("postgresql"):
    print("🐘 Using PostgreSQL database")

# SQLAlchemy 엔진 생성
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # 연결 상태 확인
    echo=False,  # SQL 로그 (개발 시 True)
    connect_args=connect_args,
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
