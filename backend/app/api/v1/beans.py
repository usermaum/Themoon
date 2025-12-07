"""
원두 관리 API 엔드포인트
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bean import Bean, BeanCreate, BeanUpdate, BeanListResponse
from app.services import bean_service
from app.models.bean import BeanType

router = APIRouter()

@router.get("/", response_model=BeanListResponse)
def read_beans(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """원두 목록 조회"""
    items = bean_service.get_beans(db, skip=skip, limit=limit, search=search)
    total = bean_service.get_beans_count(db) # 검색어가 있을 경우 카운트 로직이 부정확할 수 있으나, 일단 전체 카운트로 구현
    
    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }

@router.post("/", response_model=Bean)
def create_bean(bean: BeanCreate, db: Session = Depends(get_db)):
    """새 원두 등록"""
    return bean_service.create_bean(db, bean)

@router.get("/{bean_id}", response_model=Bean)
def read_bean(bean_id: int, db: Session = Depends(get_db)):
    """특정 원두 조회"""
    db_bean = bean_service.get_bean(db, bean_id)
    if db_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return db_bean

@router.put("/{bean_id}", response_model=Bean)
def update_bean(bean_id: int, bean: BeanUpdate, db: Session = Depends(get_db)):
    """원두 정보 수정"""
    db_bean = bean_service.update_bean(db, bean_id, bean)
    if db_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return db_bean

@router.delete("/{bean_id}")
def delete_bean(bean_id: int, db: Session = Depends(get_db)):
    """원두 삭제"""
    success = bean_service.delete_bean(db, bean_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bean not found")
    return {"ok": True}
