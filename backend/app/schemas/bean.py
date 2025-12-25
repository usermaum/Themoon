"""
Bean 스키마 - 원두 정보 요청/응답 검증

Ref: Documents/Planning/Themoon_Rostings_v2.md
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.bean import BeanType, RoastProfile


class BeanBase(BaseModel):
    """Bean 공통 필드"""

    name: str = Field(..., min_length=1, max_length=100, description="품목명")
    type: BeanType = Field(default=BeanType.GREEN_BEAN, description="품목 유형")
    sku: Optional[str] = Field(None, description="SKU 코드")

    # 다국어 정보
    name_ko: Optional[str] = Field(None, description="품목명(한글)")
    name_en: Optional[str] = Field(None, description="품목명(영문)")

    # 생두 정보
    origin: Optional[str] = Field(None, max_length=100, description="원산지")
    origin_ko: Optional[str] = Field(None, description="원산지(한글)")
    origin_en: Optional[str] = Field(None, description="원산지(영문)")

    variety: Optional[str] = Field(None, max_length=50, description="품종")
    grade: Optional[str] = Field(None, max_length=50, description="등급")
    processing_method: Optional[str] = Field(None, max_length=50, description="가공 방식")

    # 원두 정보
    roast_profile: Optional[RoastProfile] = Field(None, description="로스팅 프로필")
    parent_bean_id: Optional[int] = Field(None, description="원재료 생두 ID")

    # 재고 및 가격
    quantity_kg: float = Field(default=0.0, ge=0, description="현재 재고량 (kg)")
    avg_price: float = Field(default=0.0, ge=0, description="평균 단가 (매입가/생산원가)")
    purchase_price_per_kg: Optional[float] = Field(None, ge=0, description="최근 매입가")
    cost_price: Optional[float] = Field(None, ge=0, description="생산 원가")

    # 메타 데이터
    description: Optional[str] = Field(None, description="설명")
    notes: Optional[str] = Field(None, description="메모")

    # 로스팅 정보
    expected_loss_rate: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="예상 로스팅 손실률"
    )

    @field_validator(
        "origin", "variety", "grade", "processing_method", "description", "notes", mode="before"
    )
    @classmethod
    def empty_str_to_none(cls, v):
        """빈 문자열을 None으로 변환"""
        if v == "":
            return None
        return v


class BeanCreate(BeanBase):
    """Bean 생성 요청"""

    pass


class BeanUpdate(BaseModel):
    """Bean 수정 요청"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[BeanType] = Field(None)
    sku: Optional[str] = Field(None)

    name_ko: Optional[str] = Field(None)
    name_en: Optional[str] = Field(None)

    origin: Optional[str] = Field(None)
    origin_ko: Optional[str] = Field(None)
    origin_en: Optional[str] = Field(None)

    variety: Optional[str] = Field(None)
    grade: Optional[str] = Field(None)
    processing_method: Optional[str] = Field(None)

    roast_profile: Optional[RoastProfile] = Field(None)
    parent_bean_id: Optional[int] = Field(None)

    quantity_kg: Optional[float] = Field(None, ge=0)
    avg_price: Optional[float] = Field(None, ge=0)
    purchase_price_per_kg: Optional[float] = Field(None, ge=0)
    cost_price: Optional[float] = Field(None, ge=0)

    description: Optional[str] = Field(None)

    notes: Optional[str] = Field(None)

    expected_loss_rate: Optional[float] = Field(None, ge=0.0, le=1.0)

    @field_validator(
        "origin", "variety", "grade", "processing_method", "description", "notes", mode="before"
    )
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class Bean(BeanBase):
    """Bean 응답 - DB 정보 포함"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BeanListResponse(BaseModel):
    """Bean 목록 응답"""

    items: List[Bean]
    total: int
    page: int
    size: int
    pages: int
