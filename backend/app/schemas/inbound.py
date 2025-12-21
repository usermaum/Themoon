from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- OCR/Analysis Schemas ---

class DocumentInfo(BaseModel):
    """문서 정보"""
    document_number: Optional[str] = None
    contract_number: Optional[str] = None
    issue_date: Optional[str] = None
    invoice_date: Optional[str] = None
    delivery_date: Optional[str] = None
    payment_due_date: Optional[str] = None
    invoice_type: Optional[str] = None

class SupplierInfo(BaseModel):
    """공급자 정보"""
    name: Optional[str] = None
    business_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    representative: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None

class ReceiverInfo(BaseModel):
    """수신자 정보"""
    name: Optional[str] = None
    business_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None

class AmountsInfo(BaseModel):
    """금액 정보"""
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    grand_total: Optional[float] = None
    currency: Optional[str] = None

class OCRItem(BaseModel):
    """품목 정보 (확장)"""
    item_number: Optional[str] = None
    bean_name: Optional[str] = None
    bean_name_kr: Optional[str] = None
    specification: Optional[str] = None
    origin: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    note: Optional[str] = None

    # 매칭 상태 정보 (NEW)
    matched: Optional[bool] = None  # 기존 생두와 매칭 여부
    match_field: Optional[str] = None  # 매칭된 필드: "name", "name_en", "name_ko", "new"
    match_method: Optional[str] = None  # 매칭 방법: "exact", "new"
    bean_id: Optional[int] = None  # 매칭된 생두 ID (matched=True일 때)

class AdditionalInfo(BaseModel):
    """추가 정보"""
    payment_terms: Optional[str] = None
    shipping_method: Optional[str] = None
    notes: Optional[str] = None
    remarks: Optional[str] = None

class OCRResponse(BaseModel):
    """OCR 분석 결과 (전체 명세서 데이터)"""
    # 디버그 원본 텍스트
    debug_raw_text: Optional[str] = None

    # 구조화된 데이터
    document_info: Optional[DocumentInfo] = None
    supplier: Optional[SupplierInfo] = None
    receiver: Optional[ReceiverInfo] = None
    amounts: Optional[AmountsInfo] = None
    items: List[OCRItem] = []
    additional_info: Optional[AdditionalInfo] = None

    # 기존 호환성 유지 (deprecated, 하위 호환성)
    supplier_name: Optional[str] = None
    contract_number: Optional[str] = None
    supplier_phone: Optional[str] = None
    supplier_email: Optional[str] = None
    receiver_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None

    # 메타 정보
    drive_link: Optional[str] = None

# --- Inbound Document DB Schemas ---
class InboundDocumentBase(BaseModel):
    supplier_name: Optional[str] = None
    contract_number: Optional[str] = None
    supplier_id: Optional[int] = None
    receiver_name: Optional[str] = None
    
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    image_url: Optional[str] = None
    drive_file_id: Optional[str] = None
    notes: Optional[str] = None

class InboundDocumentCreate(InboundDocumentBase):
    # Extra fields for Supplier creation/update
    supplier_phone: Optional[str] = None
    supplier_email: Optional[str] = None

class InboundDocument(InboundDocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Request Schemas ---
class AnalyzeUrlRequest(BaseModel):
    url: str

class InboundConfirmRequest(BaseModel):
    # Data to save to DB (Log + Document)
    document: InboundDocumentCreate
    items: List[OCRItem] # Validated list of items

    # New: Full OCR data for detailed storage (Option B redesign)
    document_info: Optional[DocumentInfo] = None
    supplier: Optional[SupplierInfo] = None
    receiver: Optional[ReceiverInfo] = None
    amounts: Optional[AmountsInfo] = None
    additional_info: Optional[AdditionalInfo] = None
