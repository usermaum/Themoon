from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InventoryLogBase(BaseModel):
    bean_id: int
    change_type: str  # "PURCHASE", "ROASTING_INPUT", "ROASTING_OUTPUT", "SALES", "LOSS", "ADJUSTMENT", "BLENDING_INPUT"
    change_amount: float  # +: 증가, -: 감소
    notes: Optional[str] = None

class InventoryLogCreate(InventoryLogBase):
    pass

class InventoryLog(InventoryLogBase):
    id: int
    current_quantity: float
    created_at: datetime

    class Config:
        from_attributes = True

class InventoryLogListResponse(BaseModel):
    """입출고 기록 목록 응답 (페이징 지원)"""
    items: List[InventoryLog]
    total: int
    page: int
    size: int
    pages: int
