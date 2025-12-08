"""
Bean API 엔드포인트

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/pages/BeanManagement.py
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.database import get_db
from app.schemas.bean import Bean, BeanCreate, BeanUpdate, BeanListResponse
from app.services import bean_service

router = APIRouter()


@router.get("/", response_model=BeanListResponse)
def read_beans(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    search: Optional[str] = Query(None, description="검색어 (이름, 원산지, 품종)"),
    type: Optional[List[str]] = Query(None, description="원두 유형 필터 (GREEN_BEAN, ROASTED_BEAN, BLEND_BEAN)"),
    db: Session = Depends(get_db)
):
    """원두 목록 조회"""
    print(f"DEBUG: Received type filter: {type}") # Debug log
    skip = (page - 1) * size
    beans = bean_service.get_beans(db, skip=skip, limit=size, search=search, bean_types=type)
    total = bean_service.get_beans_count(db, search=search, bean_types=type)
    pages = math.ceil(total / size) if size > 0 else 0
    
    return BeanListResponse(
        items=beans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{bean_id}", response_model=Bean)
def read_bean(bean_id: int, db: Session = Depends(get_db)):
    """원두 상세 조회"""
    bean = bean_service.get_bean(db, bean_id=bean_id)
    if bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return bean


@router.post("/", response_model=Bean, status_code=201)
def create_bean(bean: BeanCreate, db: Session = Depends(get_db)):
    """새 원두 등록"""
    return bean_service.create_bean(db=db, bean=bean)


@router.put("/{bean_id}", response_model=Bean)
def update_bean(bean_id: int, bean: BeanUpdate, db: Session = Depends(get_db)):
    """원두 정보 수정"""
    updated_bean = bean_service.update_bean(db, bean_id=bean_id, bean=bean)
    if updated_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return updated_bean


@router.delete("/{bean_id}", status_code=204)
def delete_bean(bean_id: int, db: Session = Depends(get_db)):
    """원두 삭제"""
    success = bean_service.delete_bean(db, bean_id=bean_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bean not found")


@router.get("/stats/count", response_model=dict)
def get_beans_count(db: Session = Depends(get_db)):
    """전체 원두 개수 조회"""
    count = bean_service.get_beans_count(db)
    return {"count": count}


@router.patch("/{bean_id}/quantity", response_model=Bean)
def update_bean_quantity(
    bean_id: int,
    quantity_change: float = Query(..., description="재고 변경량 (kg, 음수 가능)"),
    db: Session = Depends(get_db)
):
    """원두 재고량 조정"""
    updated_bean = bean_service.update_bean_quantity(
        db, bean_id=bean_id, quantity_change=quantity_change
    )
    if updated_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return updated_bean
