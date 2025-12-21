from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.database import get_db
from app.services import cost_service, stats_service
from app.models.bean import Bean

router = APIRouter()

@router.get("/cost/fifo/{bean_id}")
def get_fifo_cost(
    bean_id: int, 
    quantity: float = Query(..., gt=0, description="Quantity to calculate cost for"),
    db: Session = Depends(get_db)
):
    """
    Calculate FIFO cost for a specific bean and quantity.
    """
    try:
        cost = cost_service.calculate_fifo_cost(db, bean_id, quantity)
        return {"bean_id": bean_id, "quantity": quantity, "fifo_avg_cost": cost}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/supplier")
def get_supplier_statistics(db: Session = Depends(get_db)):
    """
    Get total purchase stats by supplier.
    """
    return stats_service.get_supplier_stats(db)

@router.get("/stats/buying/monthly")
def get_buying_trends(
    months: int = Query(12, description="Number of months to look back"),
    db: Session = Depends(get_db)
):
    """
    Get monthly buying total amounts.
    """
    return stats_service.get_monthly_buying_stats(db, months)

@router.get("/stats/item/trends")
def get_item_trends(
    bean_name: str = Query(..., description="Bean name to search for"),
    db: Session = Depends(get_db)
):
    """
    Get price history for a specific item.
    """
    return stats_service.get_item_price_trends(db, bean_name)
