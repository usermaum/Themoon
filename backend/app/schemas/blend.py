from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class BlendRecipeItem(BaseModel):
    """블렌드 레시피 아이템 (원두 ID 및 비율)"""

    bean_id: int
    ratio: float  # 0.0 ~ 1.0 (비율)


class BlendBase(BaseModel):
    """블렌드 기본 스키마"""

    name: str
    description: Optional[str] = None
    recipe: List[BlendRecipeItem]
    target_roast_level: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("description", "target_roast_level", "notes", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class BlendCreate(BlendBase):
    """블렌드 생성 스키마"""

    pass


class BlendUpdate(BaseModel):
    """블렌드 수정 스키마"""

    name: Optional[str] = None
    description: Optional[str] = None
    recipe: Optional[List[BlendRecipeItem]] = None
    target_roast_level: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("name", "description", "target_roast_level", "notes", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class Blend(BlendBase):
    """블렌드 응답 스키마"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
