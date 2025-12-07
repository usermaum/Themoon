from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class BlendRecipeItem(BaseModel):
    bean_id: int
    ratio: float  # 0.0 ~ 1.0 (비율)

class BlendBase(BaseModel):
    name: str
    description: Optional[str] = None
    recipe: List[BlendRecipeItem]
    target_roast_level: Optional[str] = None
    notes: Optional[str] = None

class BlendCreate(BlendBase):
    pass

class BlendUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    recipe: Optional[List[BlendRecipeItem]] = None
    target_roast_level: Optional[str] = None
    notes: Optional[str] = None

class Blend(BlendBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
