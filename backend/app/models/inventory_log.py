from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    IN = "IN"   # 일반 입고
    OUT = "OUT" # 일반 출고
    ADJUST = "ADJUST" # 재고 조정
    
    INBOUND = "INBOUND" # 구매 입고
    ROASTING_IN = "ROASTING_IN" # 로스팅 투입 (생두 차감)
    ROASTING_OUT = "ROASTING_OUT" # 로스팅 생산 (원두 증가)
    BLENDING_IN = "BLENDING_IN" # 블렌딩 투입 (원두 차감)
    BLENDING_OUT = "BLENDING_OUT" # 블렌딩 생산 (블렌드 증가)
    SALES = "SALES" # 판매 출고
    LOSS = "LOSS" # 손실 (폐기 등)

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False) # IN, OUT, ADJUST
    quantity_change = Column(Float, nullable=False) # 변동량 (+ 또는 -)
    current_quantity = Column(Float, nullable=False) # 변동 후 잔고
    reason = Column(Text, nullable=True) # 사유 (예: 로스팅 사용, 구매 입고)
    
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

    bean = relationship("Bean", back_populates="inventory_logs")
