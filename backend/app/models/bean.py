"""
Bean 모델 - 원두 정보 관리

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/models/bean.py
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


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
    
    # 구매 정보
    purchase_date = Column(Date, comment="구매일")
    purchase_price_per_kg = Column(Float, comment="kg당 구매 가격")
    quantity_kg = Column(Float, default=0.0, comment="재고량 (kg)")
    
    # 로스팅 정보
    roast_level = Column(String(20), comment="로스팅 단계 (Light, Medium, Dark)")
    
    # 추가 정보
    notes = Column(Text, comment="메모")
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inventory_logs = relationship("InventoryLog", back_populates="bean", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bean(id={self.id}, name='{self.name}', origin='{self.origin}')>"
