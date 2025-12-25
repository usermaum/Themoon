from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.inventory_log import InventoryLog, InventoryLogCreate, InventoryLogListResponse
from app.services.inventory_log_service import inventory_log_service

router = APIRouter()


@router.get("/", response_model=InventoryLogListResponse)
def read_inventory_logs(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    bean_id: Optional[int] = Query(None, description="원두 ID 필터"),
    change_type: List[str] = Query([], description="변동 유형 필터 (PURCHASE, SALES 등)"),
    search: Optional[str] = Query(None, description="검색어 (원두 이름/원산지)"),
    db: Session = Depends(get_db),
):
    """
    재고 입출고 기록 조회 (페이징 지원)
    - bean_id: 특정 원두의 기록만 조회
    - change_type: 변동 유형으로 필터링 (입고/출고 탭용)
    - search: 원두 이름/원산지 검색
    """
    # skip/limit 계산
    skip = (page - 1) * size

    # 빈 리스트를 None으로 변환
    change_types = change_type if change_type else None

    # 데이터 조회
    logs = inventory_log_service.get_logs(
        db, bean_id=bean_id, change_types=change_types, search=search, skip=skip, limit=size
    )
    total = inventory_log_service.get_logs_count(
        db, bean_id=bean_id, change_types=change_types, search=search
    )
    pages = (total + size - 1) // size if size > 0 else 0

    # Explicit conversation
    logs_data = [InventoryLog.model_validate(log) for log in logs]

    return InventoryLogListResponse(items=logs_data, total=total, page=page, size=size, pages=pages)


@router.post("/", response_model=InventoryLog, status_code=status.HTTP_201_CREATED)
def create_inventory_log(log: InventoryLogCreate, db: Session = Depends(get_db)):
    """
    재고 입출고 기록 생성
    - transaction_type: "IN" (입고), "OUT" (출고), "ADJUST" (조정)
    - quantity_change: 양수(입고), 음수(출고)
    """
    try:
        new_log = inventory_log_service.create_log(db, log)
        return InventoryLog.model_validate(new_log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{log_id}", response_model=InventoryLog)
def update_inventory_log(
    log_id: int, change_amount: float, notes: Optional[str] = None, db: Session = Depends(get_db)
):
    """
    재고 입출고 기록 수정
    """
    try:
        updated_log = inventory_log_service.update_log(db, log_id, change_amount, notes)
        if not updated_log:
            raise HTTPException(status_code=404, detail="Inventory log not found")
        return InventoryLog.model_validate(updated_log)
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
