"""
데이터베이스 기본 설정
SQLAlchemy Base, Engine, Session 관리
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 프로젝트 루트 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# data 디렉토리가 없으면 생성 (Streamlit Cloud 대응)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, "roasting_data.db")

# 데이터베이스 URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 클래스
Base = declarative_base()

def init_db():
    """데이터베이스 테이블 생성"""
    # 모든 모델이 임포트된 상태에서 호출되어야 함
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료")

def get_db():
    """DB 세션 반환 (의존성 주입용)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db():
    """데이터베이스 초기화 (개발용)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 초기화 완료")
