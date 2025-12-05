"""
Bean 스키마 - 원두 정보 요청/응답 검증

Pydantic 모델을 사용한 데이터 검증 및 직렬화
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.models.bean import BeanType, RoastProfile


class BeanBase(BaseModel):
    """Bean 공통 필드"""

    name: str = Field(..., min_length=1, max_length=100, description="원두명")
    
    # Phase 2: Type & Profile
    type: Optional[BeanType] = Field(default=BeanType.GREEN_BEAN, description="원두 유형")
    roast_profile: Optional[RoastProfile] = Field(None, description="로스팅 프로필")
    
    origin: Optional[str] = Field(None, max_length=100, description="원산지")
    variety: Optional[str] = Field(None, max_length=50, description="품종")
    processing_method: Optional[str] = Field(None, max_length=50, description="가공 방식")
    
    purchase_date: Optional[date] = Field(None, description="구매일")
    purchase_price_per_kg: Optional[float] = Field(None, ge=0, description="kg당 구매 가격")
    
    cost_price: Optional[float] = Field(None, ge=0, description="생산 원가 (kg당)")
    quantity_kg: Optional[float] = Field(None, ge=0, description="재고량 (kg)")
    
    parent_bean_id: Optional[int] = Field(None, description="상위 생두 ID")
    
    notes: Optional[str] = Field(None, description="메모")

    @field_validator('origin', 'variety', 'processing_method', 'notes', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """빈 문자열을 None으로 변환"""
        if v == '':
            return None
        return v


class BeanCreate(BeanBase):
    """Bean 생성 요청"""
    pass


class BeanUpdate(BaseModel):
    """Bean 수정 요청 - 모든 필드 선택적"""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="원두명")
    type: Optional[BeanType] = Field(None, description="원두 유형")
    roast_profile: Optional[RoastProfile] = Field(None, description="로스팅 프로필")
    
    origin: Optional[str] = Field(None, max_length=100, description="원산지")
    variety: Optional[str] = Field(None, max_length=50, description="품종")
    processing_method: Optional[str] = Field(None, max_length=50, description="가공 방식")
    purchase_date: Optional[date] = Field(None, description="구매일")
    purchase_price_per_kg: Optional[float] = Field(None, ge=0, description="kg당 구매 가격")
    cost_price: Optional[float] = Field(None, ge=0, description="생산 원가 (kg당)")
    quantity_kg: Optional[float] = Field(None, ge=0, description="재고량 (kg)")
    parent_bean_id: Optional[int] = Field(None, description="상위 생두 ID")
    notes: Optional[str] = Field(None, description="메모")

    @field_validator('name', 'origin', 'variety', 'processing_method', 'notes', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """빈 문자열을 None으로 변환"""
        if v == '':
            return None
        return v


class Bean(BeanBase):
    """Bean 응답 - DB 정보 포함"""
    
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class BeanListResponse(BaseModel):
    """Bean 목록 응답 (페이지네이션 정보 포함)"""
    
    items: list[Bean]
    total: int
    page: int
    size: int
    pages: int
