from pydantic import BaseModel, field_validator
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

    @field_validator('description', 'target_roast_level', 'notes', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v

class BlendCreate(BlendBase):
    pass

class BlendUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    recipe: Optional[List[BlendRecipeItem]] = None
    target_roast_level: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('name', 'description', 'target_roast_level', 'notes', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v

class Blend(BlendBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
