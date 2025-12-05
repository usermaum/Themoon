from pydantic import BaseModel, Field, field_validator
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

    @field_validator('recipe', mode='before')
    @classmethod
    def transform_recipes(cls, v):
        # If v is a list of SQLAlchemy objects (Recipe model)
        if v and isinstance(v, list) and not isinstance(v[0], dict) and hasattr(v[0], 'ingredient_bean_id'):
            return [
                {"bean_id": r.ingredient_bean_id, "ratio": r.ratio_percent / 100.0}
                for r in v
            ]
        return v

class BlendingProduction(BaseModel):
    amount: float = Field(..., gt=0, description="생산량 (kg)")
    note: Optional[str] = Field(None, description="메모")

class BlendingResponse(BaseModel):
    transaction_ids: List[int]
    cost_price: float
    produced_amount: float
