from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

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

    # 로스팅 통계 필드 (고도화)
    brand = Column(String(100), nullable=True)  # 브랜드 (예: "산타바바라", "스페셜티")
    avg_loss_rate = Column(Float, nullable=True)  # 평균 손실률 (%) - 자동 계산
    std_loss_rate = Column(Float, nullable=True)  # 손실률 표준편차 (%) - 자동 계산
    total_roasted_count = Column(Integer, default=0)  # 총 로스팅 횟수
    last_roasted_date = Column(Date, nullable=True)  # 마지막 로스팅 날짜

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    inventory = relationship("Inventory", back_populates="bean", cascade="all, delete-orphan")
    blend_recipes = relationship("BlendRecipe", back_populates="bean", cascade="all, delete-orphan")
    price_history = relationship("BeanPriceHistory", back_populates="bean", cascade="all, delete-orphan")
    # RoastingLog와의 관계는 RoastingLog 측에서 backref로 설정됨

    def __repr__(self):
        return f"<Bean(no={self.no}, name={self.name}, roast={self.roast_level})>"


class BeanPriceHistory(Base):
    """원두 가격 변경 이력"""
    __tablename__ = "bean_price_history"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    change_reason = Column(Text, nullable=True)  # 변경 사유 (선택사항)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    bean = relationship("Bean", back_populates="price_history")

    def __repr__(self):
        return f"<BeanPriceHistory(bean_id={self.bean_id}, {self.old_price}→{self.new_price})>"
