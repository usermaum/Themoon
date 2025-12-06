"""
로스팅 API 엔드포인트
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.roasting import SingleOriginRoastingRequest, RoastingResponse
from app.services import roasting_service

router = APIRouter()

@router.post("/single-origin", response_model=RoastingResponse)
def roast_single_origin(
    request: SingleOriginRoastingRequest,
    db: Session = Depends(get_db)
):
    """
    싱글 오리진 로스팅 기록
    - 생두 재고 차감 -> 원두 재고 생성/증가 -> 재고 로그 기록
    """
    try:
        roasted_bean = roasting_service.create_single_origin_roasting(
            db=db,
            green_bean_id=request.green_bean_id,
            input_weight=request.input_weight,
            output_weight=request.output_weight,
            roast_profile=request.roast_profile,
            notes=request.notes
        )
        
        # 손실률 계산
        loss_rate = 0.0
        if request.input_weight > 0:
            loss_rate = (request.input_weight - request.output_weight) / request.input_weight * 100
            
        return RoastingResponse(
            message="Single origin roasting logged successfully",
            roasted_bean=roasted_bean,
            loss_rate_percent=round(loss_rate, 2),
            production_cost=round(roasted_bean.cost_price, 2)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
