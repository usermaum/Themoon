from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.inventory_log import InventoryLog, InventoryLogCreate
from app.services.inventory_log_service import inventory_log_service

router = APIRouter()

@router.get("/", response_model=List[InventoryLog])
def read_inventory_logs(
    bean_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    재고 입출고 기록 조회
    bean_id를 지정하면 해당 원두의 기록만 조회
    """
    logs = inventory_log_service.get_logs(db, bean_id=bean_id, skip=skip, limit=limit)
    return logs

@router.post("/", response_model=InventoryLog, status_code=status.HTTP_201_CREATED)
def create_inventory_log(log: InventoryLogCreate, db: Session = Depends(get_db)):
    """
    재고 입출고 기록 생성
    - transaction_type: "IN" (입고), "OUT" (출고), "ADJUST" (조정)
    - quantity_change: 양수(입고), 음수(출고)
    """
    try:
        return inventory_log_service.create_log(db, log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{log_id}", response_model=InventoryLog)
def update_inventory_log(
    log_id: int,
    change_amount: float,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    재고 입출고 기록 수정
    """
    try:
        updated_log = inventory_log_service.update_log(db, log_id, change_amount, notes)
        if not updated_log:
            raise HTTPException(status_code=404, detail="Inventory log not found")
        return updated_log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_log(log_id: int, db: Session = Depends(get_db)):
    """
    재고 입출고 기록 삭제
    """
    try:
        success = inventory_log_service.delete_log(db, log_id)
        if not success:
            raise HTTPException(status_code=404, detail="Inventory log not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
