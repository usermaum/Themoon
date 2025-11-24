from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventoryLogBase(BaseModel):
    bean_id: int
    transaction_type: str  # "IN", "OUT", "ADJUST"
    quantity_change: float
    reason: Optional[str] = None

class InventoryLogCreate(InventoryLogBase):
    pass

class InventoryLog(InventoryLogBase):
    id: int
    current_quantity: float
    created_at: datetime

    class Config:
        from_attributes = True
