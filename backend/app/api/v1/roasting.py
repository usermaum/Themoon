"""
로스팅 API 엔드포인트
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.roasting import (
    BlendRoastingRequest,
    RoastingLog,
    RoastingLogDetail,
    RoastingResponse,
    RoastingResponse,
    SingleOriginRoastingRequest,
)
from app.schemas.analytics import RoastingStatsResponse
from typing import Optional
from datetime import date
from fastapi import Query

from app.services.roasting_service import RoastingService
from app.services.bean_service import BeanService
from app.services.inventory_service import InventoryService
from app.repositories.bean_repository import BeanRepository
from app.repositories.inbound_repository import InboundRepository
from app.repositories.inventory_log_repository import InventoryLogRepository
from app.repositories.blend_repository import BlendRepository
from app.repositories.roasting_log_repository import RoastingLogRepository

router = APIRouter()


def get_roasting_service(db: Session = Depends(get_db)) -> RoastingService:
    bean_repo = BeanRepository(db)
    inbound_repo = InboundRepository(db)
    inventory_log_repo = InventoryLogRepository(db)
    blend_repo = BlendRepository(db)
    roasting_log_repo = RoastingLogRepository(db)

    bean_service = BeanService(bean_repo)
    inventory_service = InventoryService(inbound_repo, inventory_log_repo)
    
    return RoastingService(bean_service, inventory_service, blend_repo, roasting_log_repo)


@router.post("/single-origin", response_model=RoastingResponse)
def roast_single_origin(
    request: SingleOriginRoastingRequest,
    service: RoastingService = Depends(get_roasting_service),
):
    """
    싱글 오리진 로스팅 기록
    - 생두 재고 차감 -> 원두 재고 생성/증가 -> 재고 로그 기록
    """
    try:
        roasted_bean, batch_no = service.create_single_origin_roasting(
            green_bean_id=request.green_bean_id,
            input_weight=request.input_weight,
            output_weight=request.output_weight,
            roast_profile=request.roast_profile,
            notes=request.notes,
        )

        # 손실률 계산
        loss_rate = 0.0
        if request.input_weight > 0:
            loss_rate = (request.input_weight - request.output_weight) / request.input_weight * 100

        return RoastingResponse(
            message="Single origin roasting logged successfully",
            roasted_bean=roasted_bean,
            batch_no=batch_no,
            loss_rate_percent=round(loss_rate, 2),
            production_cost=round(roasted_bean.cost_price, 2),
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/blend", response_model=RoastingResponse)
def roast_blend(
    request: BlendRoastingRequest,
    service: RoastingService = Depends(get_roasting_service),
):
    """
    블렌드 로스팅 기록
    """
    try:
        roasted_bean, batch_no = service.create_blend_roasting(
            blend_id=request.blend_id,
            output_weight=request.output_weight,
            input_weight=request.input_weight,
            notes=request.notes,
        )

        loss_rate = 0.0
        if request.input_weight and request.input_weight > 0:
            loss_rate = (request.input_weight - request.output_weight) / request.input_weight * 100

        return RoastingResponse(
            message="Blend roasting logged successfully",
            roasted_bean=roasted_bean,
            batch_no=batch_no,
            loss_rate_percent=round(loss_rate, 2),
            production_cost=round(roasted_bean.cost_price, 2) if roasted_bean.cost_price else 0.0,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        # 디버깅을 위해 에러 상세 출력
        print(f"Error in roast_blend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=list[RoastingLog])
def get_roasting_history(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="조회 시작일"),
    end_date: Optional[date] = Query(None, description="조회 종료일"),
    bean_id: Optional[int] = Query(None, description="생두 ID 필터"),
    bean_type: Optional[str] = Query(None, description="원두 유형 필터 (GREEN_BEAN, BLEND_BEAN)"),
    db: Session = Depends(get_db),
):
    """로스팅 이력 조회"""
    repo = RoastingLogRepository(db)
    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "bean_id": bean_id,
        "bean_type": bean_type
    }
    return repo.get_multi(skip=skip, limit=limit, filters=filters)


@router.get("/{log_id}", response_model=RoastingLogDetail)
def get_roasting_log(
    log_id: int,
    db: Session = Depends(get_db),
):
    """특정 로스팅 배치 상세 조회"""
    repo = RoastingLogRepository(db)
    log = repo.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Roasting log not found")
    return log


@router.get("/dashboard/stats", response_model=RoastingStatsResponse)
def get_roasting_stats(
    start_date: Optional[date] = Query(None, description="조회 시작일"),
    end_date: Optional[date] = Query(None, description="조회 종료일"),
    service: RoastingService = Depends(get_roasting_service),
):
    """
    로스팅 대시보드 통계 조회
    - 총생산량, 비용, 손실률 요약
    - 일별 생산 차트 데이터
    - 원두별 사용 비중
    """
    try:
        return service.get_analytics_summary(start_date, end_date)
    except Exception as e:
        print(f"Error in stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
