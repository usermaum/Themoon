"""
Bean API 엔드포인트
"""
import math
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.bean import Bean, BeanCreate, BeanListResponse, BeanUpdate, BeanType
from app.services.bean_service import BeanService
from app.repositories.bean_repository import BeanRepository

router = APIRouter()

def get_bean_service(db: Session = Depends(get_db)) -> BeanService:
    repository = BeanRepository(db)
    return BeanService(repository)

@router.get("/", response_model=BeanListResponse)
def read_beans(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    search: Optional[str] = Query(None, description="검색어 (이름, 원산지, 품종)"),
    type: List[str] = Query(
        [], description="원두 유형 필터 (GREEN_BEAN, ROASTED_BEAN, BLEND_BEAN)"
    ),
    service: BeanService = Depends(get_bean_service),
):
    """원두 목록 조회"""
    bean_types = type if type else None
    skip = (page - 1) * size
    
    beans = service.get_beans(skip=skip, limit=size, search=search, bean_types=bean_types)
    total = service.get_beans_count(search=search, bean_types=bean_types)
    
    pages = math.ceil(total / size) if size > 0 else 0
    beans_data = [Bean.model_validate(b) for b in beans]

    return BeanListResponse(items=beans_data, total=total, page=page, size=size, pages=pages)


@router.get("/{bean_id}", response_model=Bean)
def read_bean(bean_id: int, service: BeanService = Depends(get_bean_service)):
    """원두 상세 조회"""
    bean = service.get_bean(bean_id=bean_id)
    if bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return Bean.model_validate(bean)


@router.post("/", response_model=Bean, status_code=201)
def create_bean(bean: BeanCreate, service: BeanService = Depends(get_bean_service)):
    """새 원두 등록"""
    new_bean = service.create_bean(bean=bean)
    return Bean.model_validate(new_bean)


@router.put("/{bean_id}", response_model=Bean)
def update_bean(bean_id: int, bean: BeanUpdate, service: BeanService = Depends(get_bean_service)):
    """원두 정보 수정"""
    updated_bean = service.update_bean(bean_id=bean_id, bean=bean)
    if updated_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return Bean.model_validate(updated_bean)


@router.delete("/{bean_id}", status_code=204)
def delete_bean(bean_id: int, service: BeanService = Depends(get_bean_service)):
    """원두 삭제"""
    success = service.delete_bean(bean_id=bean_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bean not found")


@router.get("/stats/count", response_model=dict)
def get_beans_count(service: BeanService = Depends(get_bean_service)):
    """전체 원두 개수 조회"""
    count = service.get_beans_count()
    return {"count": count}


@router.patch("/{bean_id}/quantity", response_model=Bean)
def update_bean_quantity(
    bean_id: int,
    quantity_change: float = Query(..., description="재고 변경량 (kg, 음수 가능)"),
    service: BeanService = Depends(get_bean_service),
):
    """원두 재고량 조정"""
    updated_bean = service.update_bean_quantity(
        bean_id=bean_id, quantity_change=quantity_change
    )
    if updated_bean is None:
        raise HTTPException(status_code=404, detail="Bean not found")
    return Bean.model_validate(updated_bean)


@router.get("/meta/origins", response_model=List[str])
def get_unique_origins(service: BeanService = Depends(get_bean_service)):
    """등록된 모든 원두의 고유 원산지 목록 조회"""
    return service.get_unique_origins()


@router.get("/meta/varieties", response_model=List[str])
def get_unique_varieties(service: BeanService = Depends(get_bean_service)):
    """등록된 모든 원두의 고유 품종 목록 조회"""
    return service.get_unique_varieties()


@router.post("/check-batch", response_model=List[dict])
def check_beans_batch(names: List[str] = Body(...), service: BeanService = Depends(get_bean_service)):
    """
    여러 원두 이름에 대해 DB 존재 여부 확인
    """
    return service.check_existing_beans(names)
