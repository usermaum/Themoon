from sqlalchemy.orm import Session
from app.models.blend import Blend
from app.schemas.blend import BlendCreate, BlendUpdate
from typing import List, Optional

class BlendService:
    def get_blends(self, db: Session, skip: int = 0, limit: int = 100) -> List[Blend]:
        return db.query(Blend).offset(skip).limit(limit).all()

    def get_blend(self, db: Session, blend_id: int) -> Optional[Blend]:
        return db.query(Blend).filter(Blend.id == blend_id).first()

    def create_blend(self, db: Session, blend: BlendCreate) -> Blend:
        # Pydantic 모델을 dict로 변환하되, recipe 리스트 내부의 객체도 dict로 변환해야 함
        blend_data = blend.model_dump()
        # recipe는 이미 list of dict 형태이거나 JSON 호환 타입이어야 함
        
        db_blend = Blend(**blend_data)
        db.add(db_blend)
        db.commit()
        db.refresh(db_blend)
        return db_blend

    def update_blend(self, db: Session, blend_id: int, blend_update: BlendUpdate) -> Optional[Blend]:
        db_blend = self.get_blend(db, blend_id)
        if not db_blend:
            return None
        
        update_data = blend_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_blend, key, value)
            
        db.commit()
        db.refresh(db_blend)
        return db_blend

    def delete_blend(self, db: Session, blend_id: int) -> bool:
        db_blend = self.get_blend(db, blend_id)
        if not db_blend:
            return False
        
        db.delete(db_blend)
        db.commit()
        return True

blend_service = BlendService()
