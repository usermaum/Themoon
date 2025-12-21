from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.services import bean_service
from app.services.blend_service import blend_service
from app.schemas.bean import Bean

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    대시보드 통계 통합 조회
    - 전체 원두 개수
    - 전체 블렌드 레시피 개수
    - 총 원두 재고량 (kg)
    - 재고 부족 원두 리스트 (Top 5)
    """
    
    # 병렬 처리가 가능하면 좋겠지만, 동기 DB 세션이므로 순차 실행
    # User Request: Show only Green Beans (Single Origin)
    total_beans = bean_service.get_beans_count(db, bean_types=["GREEN_BEAN"])
    total_blends = blend_service.get_blends_count(db)
    total_stock = bean_service.get_total_stock(db)
    low_stock_beans = bean_service.get_low_stock_beans(db, threshold=5.0, limit=5)
    low_stock_count = bean_service.count_low_stock_beans(db, threshold=5.0)
    
    # Explicitly convert ORM objects to Pydantic models
    low_stock_beans_data = [Bean.model_validate(b) for b in low_stock_beans]
    
    return {
        "total_beans": total_beans,
        "total_blends": total_blends,
        "total_stock_kg": total_stock,
        "low_stock_beans": low_stock_beans_data,
        "low_stock_count": low_stock_count
    }
