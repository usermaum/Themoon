from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.blend import Blend as BlendModel
from app.schemas.blend import Blend, BlendCreate, BlendUpdate

router = APIRouter()

@router.get("/", response_model=List[Blend])
def get_blends(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    모든 블렌드 목록 조회
    - search: 이름 검색
    """
    query = db.query(BlendModel)
    
    if search:
        query = query.filter(BlendModel.name.ilike(f"%{search}%"))
        
    return query.offset(skip).limit(limit).all()

@router.get("/{blend_id}", response_model=Blend)
def get_blend(blend_id: int, db: Session = Depends(get_db)):
    """
    특정 블렌드 조회
    """
    blend = db.query(BlendModel).filter(BlendModel.id == blend_id).first()
    if not blend:
        raise HTTPException(status_code=404, detail="Blend not found")
    return blend

@router.post("/", response_model=Blend)
def create_blend(blend_in: BlendCreate, db: Session = Depends(get_db)):
    """
    새 블렌드 생성
    """
    # JSON 직렬화 가능한 형태로 recipe 저장
    recipe_data = [item.dict() for item in blend_in.recipe]
    
    db_blend = BlendModel(
        name=blend_in.name,
        description=blend_in.description,
        recipe=recipe_data,
        target_roast_level=blend_in.target_roast_level,
        notes=blend_in.notes
    )
    db.add(db_blend)
    db.commit()
    db.refresh(db_blend)
    return db_blend

@router.put("/{blend_id}", response_model=Blend)
def update_blend(blend_id: int, blend_in: BlendUpdate, db: Session = Depends(get_db)):
    """
    블렌드 정보 수정
    """
    db_blend = db.query(BlendModel).filter(BlendModel.id == blend_id).first()
    if not db_blend:
        raise HTTPException(status_code=404, detail="Blend not found")
    
    update_data = blend_in.dict(exclude_unset=True)
    
    if "recipe" in update_data and update_data["recipe"]:
        update_data["recipe"] = [item.dict() for item in update_data["recipe"]]
        
    for field, value in update_data.items():
        setattr(db_blend, field, value)
        
    db.add(db_blend)
    db.commit()
    db.refresh(db_blend)
    return db_blend

@router.delete("/{blend_id}")
def delete_blend(blend_id: int, db: Session = Depends(get_db)):
    """
    블렌드 삭제
    """
    db_blend = db.query(BlendModel).filter(BlendModel.id == blend_id).first()
    if not db_blend:
        raise HTTPException(status_code=404, detail="Blend not found")
    
    db.delete(db_blend)
    db.commit()
    return {"success": True, "message": "Blend deleted successfully"}
