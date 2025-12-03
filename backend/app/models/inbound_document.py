from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class InboundStatus(str, enum.Enum):
    PENDING = "PENDING"     # 처리 대기 (업로드 직후)
    VERIFIED = "VERIFIED"   # 검증 완료 (OCR 확인 및 수정 완료)
    CONFIRMED = "CONFIRMED" # 입고 확정 (재고 반영 완료)

class InboundDocument(Base):
    """입고 문서 모델 (영수증/견적서)"""
    __tablename__ = "inbound_documents"

    id = Column(Integer, primary_key=True, index=True)
    
    file_path = Column(String(500), nullable=False, comment="파일 경로")
    upload_date = Column(DateTime(timezone=True), server_default=func.current_timestamp(), comment="업로드 일시")
    
    invoice_number = Column(String(100), nullable=True, comment="명세서 고유번호")
    supplier_name = Column(String(100), nullable=True, comment="공급처명")
    
    status = Column(Enum(InboundStatus), default=InboundStatus.PENDING, comment="상태")
    
    raw_ocr_data = Column(JSON, nullable=True, comment="OCR 추출 원본 데이터")
    
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<InboundDocument(id={self.id}, status='{self.status}')>"
