"""
로스팅 관련 스키마
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.bean import RoastProfile
from app.schemas.bean import Bean


class SingleOriginRoastingRequest(BaseModel):
    """싱글 오리진 로스팅 요청"""

    green_bean_id: int = Field(..., description="생두 ID")
    input_weight: float = Field(..., gt=0, description="생두 투입량 (kg)")
    output_weight: float = Field(..., ge=0, description="원두 생산량 (kg)")
    roast_profile: RoastProfile = Field(..., description="로스팅 프로필 (LIGHT/DARK)")
    notes: Optional[str] = Field(None, description="로스팅 노트")


class BlendRoastingRequest(BaseModel):
    """블렌드 로스팅 요청"""

    blend_id: int = Field(..., description="블렌드 ID")
    output_weight: float = Field(..., gt=0, description="원두 목표 생산량 (kg)")
    input_weight: Optional[float] = Field(None, gt=0, description="실제 투입량 (kg)")
    notes: Optional[str] = Field(None, description="로스팅 노트")


class RoastingResponse(BaseModel):
    """로스팅 결과 응답"""

    success: bool = True
    message: str
    roasted_bean: Bean
    batch_no: Optional[str] = Field(None, description="생산 배치 번호")
    loss_rate_percent: float = Field(..., description="손실률 (%)")
    production_cost: float = Field(..., description="생산 원가 (원/kg)")


from app.schemas.inventory_log import InventoryLog


class RoastingLogBase(BaseModel):
    """로스팅 로그 기본 스키마"""

    batch_no: str
    target_bean_id: int
    input_weight_total: float
    output_weight_total: float
    loss_rate: Optional[float] = None
    production_cost: Optional[float] = None
    notes: Optional[str] = None


class RoastingLogCreate(BaseModel):
    """로스팅 로그 생성 스키마"""
    batch_no: str
    target_bean_id: int
    input_weight_total: float
    output_weight_total: float
    loss_rate: Optional[float] = None
    production_cost: Optional[float] = None
    notes: Optional[str] = None


class RoastingLog(RoastingLogBase):
    """로스팅 로그 상세 스키마"""

    id: int
    roast_date: Optional[datetime] = None 
    created_at: Optional[datetime] = None
    target_bean: Optional[Bean] = None

    class Config:
        from_attributes = True


class RoastingLogDetail(RoastingLog):
    """로스팅 로그 상세 정보 (재고 로그 포함)"""
    inventory_logs: List[InventoryLog] = []

    class Config:
        from_attributes = True
