from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class InboundItem(BaseModel):
    name: str
    quantity: Optional[float] = 0.0
    unit_price: Optional[float] = 0.0
    total_price: Optional[float] = 0.0
    
    # 매칭된 원두 ID (선택 사항, 프론트에서 매칭 후 전송)
    matched_bean_id: Optional[int] = None
    matched_bean_name: Optional[str] = None
    match_score: Optional[int] = 0

class InboundResponse(BaseModel):
    """OCR 분석 결과 응답"""
    supplier_name: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None # YYYY-MM-DD string
    total_amount: Optional[float] = 0.0
    items: List[InboundItem] = []
    
    # 임시 파일 ID 또는 경로 (확정 시 사용)
    temp_file_path: str

class InboundConfirmRequest(BaseModel):
    """입고 확정 요청"""
    temp_file_path: str
    supplier_name: Optional[str] = None
    invoice_number: Optional[str] = None
    items: List[InboundItem]
