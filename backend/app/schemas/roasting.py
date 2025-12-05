from pydantic import BaseModel, Field
from typing import Optional
from app.models.bean import RoastProfile

class RoastingCreate(BaseModel):
    green_bean_id: int = Field(..., description="생두 ID")
    roasted_bean_id: Optional[int] = Field(None, description="원두 ID (기존 원두에 추가할 경우)")
    new_bean_name: Optional[str] = Field(None, description="새 원두 이름 (새로 생성할 경우)")
    input_amount: float = Field(..., gt=0, description="투입량 (kg)")
    output_amount: float = Field(..., gt=0, description="생산량 (kg)")
    roast_profile: RoastProfile = Field(RoastProfile.MEDIUM, description="로스팅 프로필 (Light, Medium, Dark)")
    note: Optional[str] = Field(None, description="메모")

class RoastingResponse(BaseModel):
    roasting_log_id: int
    loss_rate: float
    cost_price: float
    roasted_bean_id: int

class RoastingLogResponse(BaseModel):
    id: int
    green_bean_id: int
    green_bean_name: str
    roasted_bean_id: int
    roasted_bean_name: str
    input_quantity: float
    output_quantity: float
    loss_rate: float
    roast_date: str
    note: Optional[str] = None
    
    class Config:
        from_attributes = True
