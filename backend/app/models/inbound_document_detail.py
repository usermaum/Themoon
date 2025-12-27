from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.timezone import get_kst_now


class InboundDocumentDetail(Base):
    """인바운드 문서 상세 정보 (OCR 추출 데이터)"""

    __tablename__ = "inbound_document_details"

    id = Column(Integer, primary_key=True, index=True)
    inbound_document_id = Column(
        Integer, ForeignKey("inbound_documents.id"), nullable=False, unique=True
    )

    # 문서 정보
    document_number = Column(String, nullable=True, comment="문서번호")
    issue_date = Column(String, nullable=True, comment="발행일 (YYYY-MM-DD)")
    delivery_date = Column(String, nullable=True, comment="납품일 (YYYY-MM-DD)")
    payment_due_date = Column(String, nullable=True, comment="지급기한 (YYYY-MM-DD)")
    invoice_type = Column(String, nullable=True, comment="명세서 종류 (GSC, HACIELO, STANDARD)")

    # 공급자 상세 정보
    supplier_business_number = Column(String, nullable=True, comment="공급자 사업자등록번호")
    supplier_address = Column(Text, nullable=True, comment="공급자 주소")
    supplier_phone = Column(String, nullable=True, comment="공급자 대표 전화")
    supplier_fax = Column(String, nullable=True, comment="공급자 팩스")
    supplier_email = Column(String, nullable=True, comment="공급자 이메일")
    supplier_representative = Column(String, nullable=True, comment="공급자 대표자명")
    supplier_contact_person = Column(String, nullable=True, comment="공급자 담당자명")
    supplier_contact_phone = Column(String, nullable=True, comment="공급자 담당자 전화")

    # 금액 상세 정보
    subtotal = Column(Float, nullable=True, comment="공급가액")
    tax_amount = Column(Float, nullable=True, comment="세액")
    grand_total = Column(Float, nullable=True, comment="총합계")
    currency = Column(String, nullable=True, default="KRW", comment="통화")

    # 추가 정보
    payment_terms = Column(Text, nullable=True, comment="결제조건")
    shipping_method = Column(String, nullable=True, comment="배송방법")
    notes = Column(Text, nullable=True, comment="비고")
    remarks = Column(Text, nullable=True, comment="특이사항")

    created_at = Column(DateTime(timezone=True), default=get_kst_now)
    updated_at = Column(DateTime(timezone=True), default=get_kst_now, onupdate=get_kst_now)

    # Relationships
    inbound_document = relationship(
        "app.models.inbound_document.InboundDocument", back_populates="detail"
    )
