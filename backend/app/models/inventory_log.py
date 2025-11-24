from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    IN = "IN"   # 입고
    OUT = "OUT" # 출고
    ADJUST = "ADJUST" # 조정 (재고 실사 등)

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    transaction_type = Column(String, nullable=False) # IN, OUT, ADJUST
    quantity_change = Column(Float, nullable=False) # 변동량 (+ 또는 -)
    current_quantity = Column(Float, nullable=False) # 변동 후 잔고
    reason = Column(String, nullable=True) # 사유 (예: 로스팅 사용, 구매 입고)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bean = relationship("Bean", back_populates="inventory_logs")
