from pydantic import BaseModel, Field
from typing import Optional

class RoastingCreate(BaseModel):
    green_bean_id: int = Field(..., description="생두 ID")
    roasted_bean_id: Optional[int] = Field(None, description="원두 ID (기존 원두에 추가할 경우)")
    new_bean_name: Optional[str] = Field(None, description="새 원두 이름 (새로 생성할 경우)")
    input_amount: float = Field(..., gt=0, description="투입량 (kg)")
    output_amount: float = Field(..., gt=0, description="생산량 (kg)")
    roast_level: str = Field("Medium", description="로스팅 단계")

class RoastingResponse(BaseModel):
    transaction_id_in: int
    transaction_id_out: int
    loss_rate: float
    cost_price: float
