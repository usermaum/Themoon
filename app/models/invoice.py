"""
거래 명세서 이미지 자동 입고 기능 - 데이터베이스 모델
Invoice, InvoiceItem, InvoiceLearning 모델 정의
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Invoice(Base):
    """
    거래 명세서 모델

    이미지 업로드 시 생성되며, OCR로 추출된 정보와 메타데이터 저장
    """
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(Text, nullable=False)  # 이미지 파일 경로 (예: data/invoices/20251112_143022_예가체프.jpg)
    supplier = Column(String(200), nullable=True)  # 공급업체 (예: "GSC GREEN COFFEE", "HACIELO")
    invoice_date = Column(Date, nullable=False)  # 거래일자
    total_amount = Column(Float, nullable=True)  # 총액 (원)
    status = Column(String(20), default="COMPLETED")  # 상태: PENDING, COMPLETED, FAILED
    confidence_score = Column(Float, nullable=True)  # 신뢰도 (0~100)
    ocr_raw_text = Column(Text, nullable=True)  # OCR 원본 텍스트 (디버깅 및 재처리용)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Invoice(id={self.id}, supplier={self.supplier}, date={self.invoice_date}, status={self.status})>"


class InvoiceItem(Base):
    """
    명세서 항목 모델 (다중 원두 지원)

    하나의 거래 명세서(Invoice)에 여러 개의 원두 항목이 포함될 수 있음
    """
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    bean_id = Column(Integer, ForeignKey("beans.id", ondelete="SET NULL"), nullable=True)  # 매칭된 원두 (없으면 NULL)
    bean_name_raw = Column(Text, nullable=False)  # OCR로 추출한 원두명 (원본, 예: "Colombia Supreme Hulls")
    quantity = Column(Float, nullable=False)  # 수량 (kg)
    unit_price = Column(Float, nullable=True)  # 단가 (원/kg)
    amount = Column(Float, nullable=True)  # 금액 (수량 * 단가, 원)
    origin = Column(String(100), nullable=True)  # 원산지 (예: "Ethiopia", "Colombia")
    notes = Column(Text, nullable=True)  # 비고 (사용자가 추가한 메모)
    confidence_score = Column(Float, nullable=True)  # 항목별 신뢰도 (0~100)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    invoice = relationship("Invoice", back_populates="items")
    bean = relationship("Bean")  # Bean 모델과 관계 (database.py에 정의됨)
    learning_data = relationship("InvoiceLearning", back_populates="invoice_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InvoiceItem(id={self.id}, invoice_id={self.invoice_id}, bean={self.bean_name_raw}, qty={self.quantity}kg)>"


class InvoiceLearning(Base):
    """
    학습 데이터 모델

    사용자가 OCR 결과를 수정한 내역을 저장하여
    향후 동일한 오류 발생 시 자동으로 제안할 수 있도록 학습
    """
    __tablename__ = "invoice_learning"

    id = Column(Integer, primary_key=True, index=True)
    invoice_item_id = Column(Integer, ForeignKey("invoice_items.id", ondelete="CASCADE"), nullable=False)
    ocr_text = Column(Text, nullable=False)  # OCR이 인식한 텍스트 (예: "에티오피아예가체프")
    corrected_value = Column(Text, nullable=False)  # 사용자가 수정한 값 (예: "에티오피아 예가체프 G1")
    field_name = Column(String(50), nullable=False)  # 필드명 (bean_name, quantity, unit_price, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    invoice_item = relationship("InvoiceItem", back_populates="learning_data")

    def __repr__(self):
        return f"<InvoiceLearning(id={self.id}, field={self.field_name}, ocr={self.ocr_text[:20]}...)>"
