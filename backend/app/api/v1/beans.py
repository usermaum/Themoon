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
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    search: Optional[str] = Query(None, description="검색어 (이름, 원산지, 품종)"),
    type: List[str] = Query([], description="원두 유형 필터 (GREEN_BEAN, ROASTED_BEAN, BLEND_BEAN)"),
    origin: Optional[str] = Query(None, description="원산지 필터 (예: Blend)"),
    exclude_blend: bool = Query(False, description="블렌드 제외 (원두 탭용)"),
    db: Session = Depends(get_db)
):
    """원두 목록 조회 (페이징 및 필터 지원)"""
    # 빈 리스트를 None으로 변환 (bean_service에서 None일 때만 필터 미적용)
    bean_types = type if type else None

    # skip/limit 계산
    skip = (page - 1) * size

    # 데이터 조회
    items = bean_service.get_beans(db, skip=skip, limit=size, search=search, bean_types=bean_types, origin=origin, exclude_blend=exclude_blend)
    total = bean_service.get_beans_count(db, search=search, bean_types=bean_types, origin=origin, exclude_blend=exclude_blend)
    pages = (total + size - 1) // size if size > 0 else 0

    return BeanListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

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
