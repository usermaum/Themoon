"""
데이터베이스 설정 및 초기화
SQLAlchemy ORM 기반 DB 관리
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import sys

# 프로젝트 루트 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "Data", "roasting_data.db")

# 데이터베이스 URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # True로 설정하면 SQL 쿼리 출력
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 클래스
Base = declarative_base()

# ═══════════════════════════════════════════════════════════════
# ORM 모델 정의
# ═══════════════════════════════════════════════════════════════

class Bean(Base):
    """원두 모델"""
    __tablename__ = "beans"

    id = Column(Integer, primary_key=True, index=True)
    no = Column(Integer, unique=True, nullable=False)  # 1~13
    country_code = Column(String(10), nullable=True)
    country_name = Column(String(50), nullable=True)
    name = Column(String(100), nullable=False, unique=True)
    roast_level = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    price_per_kg = Column(Float, default=0.0)
    status = Column(String(20), default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    inventory = relationship("Inventory", back_populates="bean", cascade="all, delete-orphan")
    blend_recipes = relationship("BlendRecipe", back_populates="bean", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bean(no={self.no}, name={self.name}, roast={self.roast_level})>"


class Blend(Base):
    """블렌드 모델"""
    __tablename__ = "blends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    blend_type = Column(String(20), nullable=False)  # 풀문, 뉴문, 시즈널
    description = Column(Text, nullable=True)
    total_portion = Column(Integer, default=0)
    suggested_price = Column(Float, default=0.0)
    status = Column(String(20), default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    recipes = relationship("BlendRecipe", back_populates="blend", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="blend", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Blend(name={self.name}, type={self.blend_type})>"


class BlendRecipe(Base):
    """블렌드 구성 (다대다)"""
    __tablename__ = "blend_recipes"

    id = Column(Integer, primary_key=True, index=True)
    blend_id = Column(Integer, ForeignKey("blends.id"), nullable=False)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    portion_count = Column(Integer, nullable=False)  # 포션 개수
    ratio = Column(Float, default=0.0)  # 비율 (%)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    blend = relationship("Blend", back_populates="recipes")
    bean = relationship("Bean", back_populates="blend_recipes")

    def __repr__(self):
        return f"<BlendRecipe(blend_id={self.blend_id}, bean_id={self.bean_id}, portion={self.portion_count})>"


class Inventory(Base):
    """재고 관리"""
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), unique=True, nullable=False)
    quantity_kg = Column(Float, default=0.0)  # 현재 재고 (kg)
    min_quantity_kg = Column(Float, default=5.0)  # 최소 재고
    max_quantity_kg = Column(Float, default=50.0)  # 최대 재고
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    bean = relationship("Bean", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory(bean_id={self.bean_id}, qty={self.quantity_kg}kg)>"


class Transaction(Base):
    """거래 기록 (판매/사용)"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    blend_id = Column(Integer, ForeignKey("blends.id"), nullable=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=True)
    transaction_type = Column(String(20), nullable=False)  # 판매, 사용, 입고
    quantity_kg = Column(Float, nullable=False)
    price_per_unit = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    user_id = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    blend = relationship("Blend", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(type={self.transaction_type}, qty={self.quantity_kg}, amount={self.total_amount})>"


class CostSetting(Base):
    """비용 설정"""
    __tablename__ = "cost_settings"

    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String(100), unique=True, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CostSetting({self.parameter_name}={self.value})>"


class RoastingLog(Base):
    """로스팅 기록"""
    __tablename__ = "roasting_logs"

    id = Column(Integer, primary_key=True, index=True)
    raw_weight_kg = Column(Float, nullable=False)  # 생두 투입량
    roasted_weight_kg = Column(Float, nullable=False)  # 로스팅 후 무게
    loss_rate_percent = Column(Float, nullable=False)  # 손실률 (자동 계산)
    expected_loss_rate_percent = Column(Float, default=17.0)  # 예상 손실률
    loss_variance_percent = Column(Float, nullable=True)  # 손실률 편차

    roasting_date = Column(Date, nullable=False)  # 로스팅 날짜
    roasting_month = Column(String(7), nullable=True)  # YYYY-MM

    notes = Column(Text, nullable=True)  # 로스팅 노트
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<RoastingLog(date={self.roasting_date}, raw={self.raw_weight_kg}kg, loss={self.loss_rate_percent}%)>"


# ═══════════════════════════════════════════════════════════════
# DB 초기화 함수
# ═══════════════════════════════════════════════════════════════

def init_db():
    """데이터베이스 테이블 생성"""
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


def check_db_exists() -> bool:
    """데이터베이스 존재 여부 확인"""
    return os.path.exists(DATABASE_PATH)


if __name__ == "__main__":
    init_db()
    print(f"📁 DB 위치: {DATABASE_PATH}")
    print(f"🔗 DB URL: {DATABASE_URL}")
