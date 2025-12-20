from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timezone import get_kst_now

class InboundReceiver(Base):
    """인바운드 문서 공급받는자 정보 (OCR 추출 데이터)"""
    __tablename__ = "inbound_receivers"

    id = Column(Integer, primary_key=True, index=True)
    inbound_document_id = Column(Integer, ForeignKey("inbound_documents.id"), nullable=False, unique=True)

    # 공급받는자 기본 정보
    name = Column(String, nullable=True, comment="공급받는자명 (default: The Moon Coffee)")
    business_number = Column(String, nullable=True, comment="사업자등록번호")
    address = Column(Text, nullable=True, comment="주소")
    phone = Column(String, nullable=True, comment="전화번호")
    contact_person = Column(String, nullable=True, comment="담당자명")

    created_at = Column(DateTime(timezone=True), default=get_kst_now)
    updated_at = Column(DateTime(timezone=True), default=get_kst_now, onupdate=get_kst_now)

    # Relationships
    inbound_document = relationship("app.models.inbound_document.InboundDocument", back_populates="receiver")
