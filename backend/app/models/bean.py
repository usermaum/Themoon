"""
Bean 모델 - 원두 정보 관리

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/models/bean.py
"""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from app.database import Base


class BeanType(str, enum.Enum):
    GREEN_BEAN = "GREEN_BEAN"
    ROASTED_BEAN = "ROASTED_BEAN"
    BLEND = "BLEND"


class RoastProfile(str, enum.Enum):
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    DARK = "DARK"


class Bean(Base):
    """원두 정보 모델"""
    
    __tablename__ = "beans"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    name = Column(String(100), nullable=False, index=True, comment="원두명")
    origin = Column(String(100), comment="원산지")
    variety = Column(String(50), comment="품종 (Arabica, Robusta 등)")
    processing_method = Column(String(50), comment="가공 방식 (Washed, Natural, Honey 등)")
    
    # 구분 (Phase 2)
    type = Column(Enum(BeanType), default=BeanType.GREEN_BEAN, comment="원두 유형")
    
    # 구매 정보 (생두용)
    purchase_date = Column(Date, comment="구매일")
    purchase_price_per_kg = Column(Float, comment="kg당 구매 가격")
    
    # 생산 정보 (원두용)
    cost_price = Column(Float, default=0.0, comment="생산 원가 (kg당)")
    
    # 재고
    quantity_kg = Column(Float, default=0.0, comment="재고량 (kg)")
    
    # 로스팅 정보 (원두용)
    # roast_level deprecated in favor of roast_profile
    roast_profile = Column(Enum(RoastProfile), nullable=True, comment="로스팅 프로필")
    
    # 관계 (원두는 생두로부터 파생됨)
    parent_bean_id = Column(Integer, ForeignKey('beans.id'), nullable=True, comment="생두 ID")
    children = relationship("Bean", backref=backref('parent_bean', remote_side=[id]))
    
    # 추가 정보
    notes = Column(Text, comment="메모")
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    # Relationships
    inventory_logs = relationship("InventoryLog", back_populates="bean", cascade="all, delete-orphan")
    
    @property
    def recipe(self):
        """Legacy compatibility for Blend Schema"""
        return getattr(self, 'recipes', [])
    
    def __repr__(self):
        return f"<Bean(id={self.id}, name='{self.name}', type='{self.type}', quantity={self.quantity_kg})>"
