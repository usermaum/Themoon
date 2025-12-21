from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timezone import get_kst_now

class InboundItem(Base):
    """인바운드 문서 품목 상세 정보 (OCR 추출 데이터)"""
    __tablename__ = "inbound_items"

    id = Column(Integer, primary_key=True, index=True)
    inbound_document_id = Column(Integer, ForeignKey("inbound_documents.id"), nullable=False)
    item_order = Column(Integer, nullable=False, default=0, comment="품목 순서")

    # 품목 기본 정보
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=True, comment="원두 ID (매칭된 경우)")
    bean_name = Column(String, nullable=True, comment="품목명")
    specification = Column(String, nullable=True, comment="규격")
    unit = Column(String, nullable=True, default="kg", comment="단위 (kg, g, etc.)")
    quantity = Column(Float, nullable=True, comment="수량")
    origin = Column(String, nullable=True, comment="원산지")

    # 금액 정보
    unit_price = Column(Float, nullable=True, comment="단가")
    supply_amount = Column(Float, nullable=True, comment="공급가액")
    tax_amount = Column(Float, nullable=True, comment="세액")

    # 추가 정보
    notes = Column(Text, nullable=True, comment="비고")

    created_at = Column(DateTime(timezone=True), default=get_kst_now)
    updated_at = Column(DateTime(timezone=True), default=get_kst_now, onupdate=get_kst_now)

    # Relationships
    inbound_document = relationship("app.models.inbound_document.InboundDocument", back_populates="items")
    bean = relationship("app.models.bean.Bean", foreign_keys=[bean_id])
