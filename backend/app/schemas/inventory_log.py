from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class InventoryLogBase(BaseModel):
    bean_id: int
    change_type: str  # "PURCHASE", "ROASTING_INPUT", "ROASTING_OUTPUT", "SALES", "LOSS", "ADJUSTMENT", "BLENDING_INPUT"
    change_amount: float  # +: 증가, -: 감소
    notes: Optional[str] = None


class BeanSimple(BaseModel):
    name: str
    id: int

    class Config:
        from_attributes = True


class InventoryLogCreate(InventoryLogBase):
    pass


class InventoryLog(InventoryLogBase):
    id: int
    current_quantity: float
    created_at: datetime
    bean: Optional[BeanSimple] = None

    class Config:
        from_attributes = True


class InventoryLogListResponse(BaseModel):
    """입출고 기록 목록 응답 (페이징 지원)"""

    items: List[InventoryLog]
    total: int
    page: int
    size: int
    pages: int
