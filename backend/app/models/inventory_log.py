from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class InventoryChangeType(str, enum.Enum):
    """재고 변동 유형"""
    PURCHASE = "PURCHASE"             # 구매 입고
    ROASTING_INPUT = "ROASTING_INPUT" # 로스팅 투입 (차감)
    ROASTING_OUTPUT = "ROASTING_OUTPUT"# 로스팅 생산 (증가)
    SALES = "SALES"                   # 판매 출고
    LOSS = "LOSS"                     # 손실/폐기
    ADJUSTMENT = "ADJUSTMENT"         # 재고 조정 (실사 반영)
    BLENDING_INPUT = "BLENDING_INPUT" # 블렌딩 투입

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    
    # 변동 유형 (Enum)
    change_type = Column(Enum(InventoryChangeType), nullable=False) 
    
    change_amount = Column(Float, nullable=False, comment="변동량") # +: 증가, -: 감소
    current_quantity = Column(Float, nullable=False, comment="변동 후 잔고")
    
    notes = Column(Text, nullable=True, comment="비고/사유")
    related_id = Column(Integer, nullable=True, comment="관련 ID (로스팅ID 등)")
    
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

    # Relationships
    bean = relationship("app.models.bean.Bean", back_populates="inventory_logs")
    
    inbound_document_id = Column(Integer, ForeignKey("inbound_documents.id"), nullable=True)
    inbound_document = relationship("app.models.inbound_document.InboundDocument", back_populates="inventory_logs")

