"""
Analytics Schemas
데이터 분석 및 시각화를 위한 공통 스키마 정의
Ref: Documents/Planning/Implementation_Roasting_v2.md
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class DailyProductionStats(BaseModel):
    """일별 생산량 통계"""
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    total_weight: float = Field(..., description="총 생산량 (kg)")
    batch_count: int = Field(..., description="생산 배치 수")

class BeanUsageStats(BaseModel):
    """원두 사용량 통계 (파이 차트용)"""
    bean_type: str = Field(..., description="원두 유형 (블렌드/싱글)")
    bean_name: str = Field(..., description="원두 이름")
    total_output: float = Field(..., description="총 생산량 (kg)")
    percentage: float = Field(..., description="비중 (%)")

class LossRateStats(BaseModel):
    """손실률 통계 (스캐터/라인 차트용)"""
    batch_no: str 
    roast_date: str
    bean_name: str
    loss_rate: float

class RoastingStatsResponse(BaseModel):
    """로스팅 대시보드 데이터 응답"""
    overview: dict = Field(..., description="KPI 요약 (총생산량, 비용 등)")
    daily_production: List[DailyProductionStats]
    bean_usage: List[BeanUsageStats]
    recent_loss_rates: List[LossRateStats]
