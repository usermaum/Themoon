from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.database import get_db
from app.models.bean import Bean
from app.models.inventory_log import InventoryLog

router = APIRouter()

@router.get("/stats")
def get_inventory_stats(db: Session = Depends(get_db)):
    """
    전체 재고 통계 조회
    """
    total_beans = db.query(func.count(Bean.id)).scalar()
    total_weight = db.query(func.sum(Bean.quantity_kg)).scalar() or 0.0
    
    # Total Value = Sum(quantity * cost_price)
    # Optimized to use SQL aggregation
    total_value = db.query(func.sum(func.coalesce(Bean.quantity_kg, 0) * func.coalesce(Bean.cost_price, 0))).scalar() or 0.0
    
    return {
        "total_beans": total_beans,
        "total_weight": round(total_weight, 2),
        "total_value": round(total_value, 0)
    }

@router.get("/low-stock")
def get_low_stock_beans(threshold: float = 5.0, db: Session = Depends(get_db)):
    """
    재고 부족 알림 (기본 5kg 미만)
    """
    beans = db.query(Bean).filter(Bean.quantity_kg < threshold).all()
    return [{
        "id": b.id,
        "name": b.name,
        "quantity_kg": b.quantity_kg,
        "threshold": threshold
    } for b in beans]

@router.get("/recent-activity")
def get_recent_activity(limit: int = 5, db: Session = Depends(get_db)):
    """
    최근 재고 변동 이력
    """
    logs = db.query(InventoryLog).order_by(InventoryLog.created_at.desc()).limit(limit).all()
    
    return [{
        "id": log.id,
        "bean_name": log.bean.name,
        "type": log.transaction_type,
        "amount": log.quantity_change,
        "date": log.created_at
    } for log in logs]
