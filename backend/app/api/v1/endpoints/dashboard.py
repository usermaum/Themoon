from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.bean import Bean
from app.services import bean_service
from app.services.blend_service import blend_service

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

    # Dependency Injection (Manual for now, normally use Depends)
    from app.repositories.bean_repository import BeanRepository
    from app.services.bean_service import BeanService

    bean_repo = BeanRepository(db)
    bean_svc = BeanService(bean_repo)

    # User Request: Show only Green Beans (Single Origin)
    # Service methods use self.repository.db, so we don't pass db here
    total_beans = bean_svc.get_beans_count(bean_types=["GREEN_BEAN"])
    total_blends = blend_service.get_blends_count(db) # BlendService seems to still be module-level or old style?
    total_stock = bean_svc.get_total_stock()
    low_stock_beans = bean_svc.get_low_stock_beans(threshold=5.0, limit=5)
    low_stock_count = bean_svc.count_low_stock_beans(threshold=5.0)

    # Explicitly convert ORM objects to Pydantic models
    low_stock_beans_data = [Bean.model_validate(b) for b in low_stock_beans]

    return {
        "total_beans": total_beans,
        "total_blends": total_blends,
        "total_stock_kg": total_stock,
        "low_stock_beans": low_stock_beans_data,
        "low_stock_count": low_stock_count,
    }
