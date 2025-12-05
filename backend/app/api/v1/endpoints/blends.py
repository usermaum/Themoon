from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.blend import Blend, BlendCreate, BlendUpdate, BlendingProduction, BlendingResponse
from app.services.blend_service import blend_service

router = APIRouter()

@router.get("/", response_model=List[Blend])
def read_blends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    블렌드 목록 조회
    """
    blends = blend_service.get_blends(db, skip=skip, limit=limit)
    return blends

@router.post("/", response_model=Blend, status_code=status.HTTP_201_CREATED)
def create_blend(blend: BlendCreate, db: Session = Depends(get_db)):
    """
    새 블렌드 레시피 생성
    """
    return blend_service.create_blend(db, blend)

@router.get("/{blend_id}", response_model=Blend)
def read_blend(blend_id: int, db: Session = Depends(get_db)):
    """
    블렌드 상세 조회
    """
    db_blend = blend_service.get_blend(db, blend_id)
    if db_blend is None:
        raise HTTPException(status_code=404, detail="Blend not found")
    return db_blend

@router.put("/{blend_id}", response_model=Blend)
def update_blend(blend_id: int, blend_update: BlendUpdate, db: Session = Depends(get_db)):
    """
    블렌드 정보 수정
    """
    db_blend = blend_service.update_blend(db, blend_id, blend_update)
    if db_blend is None:
        raise HTTPException(status_code=404, detail="Blend not found")
    return db_blend

@router.delete("/{blend_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blend(blend_id: int, db: Session = Depends(get_db)):
    """
    블렌드 삭제
    """
    success = blend_service.delete_blend(db, blend_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blend not found")

@router.post("/{blend_id}/production", response_model=BlendingResponse)
def produce_blend(
    blend_id: int, 
    production_data: BlendingProduction, 
    db: Session = Depends(get_db)
):
    """
    블렌드 제품 생산 (재료 소모 -> 블렌드 재고 증가)
    """
    try:
        return blend_service.process_production(db, blend_id, production_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
