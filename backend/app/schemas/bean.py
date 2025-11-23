"""
Bean 스키마 - 원두 정보 요청/응답 검증

Pydantic 모델을 사용한 데이터 검증 및 직렬화
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BeanBase(BaseModel):
    """Bean 공통 필드"""
    
    name: str = Field(..., min_length=1, max_length=100, description="원두명")
    origin: Optional[str] = Field(None, max_length=100, description="원산지")
    variety: Optional[str] = Field(None, max_length=50, description="품종")
    processing_method: Optional[str] = Field(None, max_length=50, description="가공 방식")
    purchase_date: Optional[date] = Field(None, description="구매일")
    purchase_price_per_kg: Optional[float] = Field(None, ge=0, description="kg당 구매 가격")
    quantity_kg: Optional[float] = Field(None, ge=0, description="재고량 (kg)")
    roast_level: Optional[str] = Field(None, max_length=20, description="로스팅 단계")
    notes: Optional[str] = Field(None, description="메모")


class BeanCreate(BeanBase):
    """Bean 생성 요청"""
    pass


class BeanUpdate(BaseModel):
    """Bean 수정 요청 - 모든 필드 선택적"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="원두명")
    origin: Optional[str] = Field(None, max_length=100, description="원산지")
    variety: Optional[str] = Field(None, max_length=50, description="품종")
    processing_method: Optional[str] = Field(None, max_length=50, description="가공 방식")
    purchase_date: Optional[date] = Field(None, description="구매일")
    purchase_price_per_kg: Optional[float] = Field(None, ge=0, description="kg당 구매 가격")
    quantity_kg: Optional[float] = Field(None, ge=0, description="재고량 (kg)")
    roast_level: Optional[str] = Field(None, max_length=20, description="로스팅 단계")
    notes: Optional[str] = Field(None, description="메모")


class Bean(BeanBase):
    """Bean 응답 - DB 정보 포함"""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
