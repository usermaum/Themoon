from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.roasting import RoastingCreate, RoastingResponse, RoastingLogResponse
from app.models.roasting_log import RoastingLog
from app.services import roasting_service

router = APIRouter()

@router.post("/", response_model=RoastingResponse)
def create_roasting(
    roasting_data: RoastingCreate,
    db: Session = Depends(get_db)
):
    """
    로스팅 실행 (생두 소모 -> 원두 생성)
    - 생두 재고 차감 (ROASTING_IN)
    - 원두 재고 증가 (ROASTING_OUT)
    - 로스팅 로그 기록
    - 원가 계산 및 업데이트
    """
    try:
        return roasting_service.process_roasting(db, roasting_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[RoastingLogResponse])
def get_roasting_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    로스팅 이력 조회
    """
    logs = db.query(RoastingLog).order_by(RoastingLog.roast_date.desc()).limit(limit).all()
    
    return [
        RoastingLogResponse(
            id=log.id,
            green_bean_id=log.green_bean_id,
            green_bean_name=log.green_bean.name if log.green_bean else "Unknown",
            roasted_bean_id=log.roasted_bean_id,
            roasted_bean_name=log.roasted_bean.name if log.roasted_bean else "Unknown",
            input_quantity=log.input_quantity,
            output_quantity=log.output_quantity,
            loss_rate=log.loss_rate,
            roast_date=log.roast_date.isoformat() if log.roast_date else "",
            note=log.note
        ) for log in logs
    ]
