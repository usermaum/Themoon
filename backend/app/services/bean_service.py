"""
Bean CRUD 서비스

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/services/bean_service.py
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.bean import Bean
from app.schemas.bean import BeanCreate, BeanUpdate


def get_bean(db: Session, bean_id: int) -> Optional[Bean]:
    """ID로 원두 조회"""
    return db.query(Bean).filter(Bean.id == bean_id).first()


def get_beans(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    roast_level: Optional[str] = None,
    bean_type: Optional[str] = None
) -> List[Bean]:
    """원두 목록 조회 (페이징, 검색, 필터링 지원)"""
    query = db.query(Bean)
    
    if search:
        query = query.filter(
            (Bean.name.contains(search)) |
            (Bean.origin.contains(search)) |
            (Bean.variety.contains(search))
        )
    
    # Phase 2: Filter by Bean Type (Green/Roasted)
    if bean_type:
        query = query.filter(Bean.type == bean_type)
        
    # Legacy Support (mapped to new fields)
    if roast_level:
        if roast_level == "Green":
            query = query.filter(Bean.type == "GREEN_BEAN")
        elif roast_level == "Roasted":
            query = query.filter(Bean.type == "ROASTED_BEAN")
        else:
            # Map roast_level string to RoastProfile enum if possible
            # Assuming 'Medium' -> 'MEDIUM', 'Dark' -> 'DARK'
            try:
                uppercase_level = roast_level.upper()
                query = query.filter(Bean.roast_profile == uppercase_level)
            except:
                pass 
    
    return query.offset(skip).limit(limit).all()


def create_bean(db: Session, bean: BeanCreate) -> Bean:
    """원두 생성"""
    db_bean = Bean(
        name=bean.name,
        type=bean.type,
        roast_profile=bean.roast_profile,
        origin=bean.origin,
        variety=bean.variety,
        processing_method=bean.processing_method,
        purchase_date=bean.purchase_date,
        purchase_price_per_kg=bean.purchase_price_per_kg,
        cost_price=bean.cost_price or bean.purchase_price_per_kg or 0.0,
        quantity_kg=bean.quantity_kg or 0.0,
        parent_bean_id=bean.parent_bean_id,
        notes=bean.notes
    )
    db.add(db_bean)
    db.commit()
    db.refresh(db_bean)
    return db_bean


def update_bean(db: Session, bean_id: int, bean: BeanUpdate) -> Optional[Bean]:
    """원두 수정"""
    db_bean = get_bean(db, bean_id)
    if not db_bean:
        return None
    
    update_data = bean.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bean, field, value)
    
    db.commit()
    db.refresh(db_bean)
    return db_bean


def delete_bean(db: Session, bean_id: int) -> bool:
    """원두 삭제"""
    db_bean = get_bean(db, bean_id)
    if not db_bean:
        return False
    
    db.delete(db_bean)
    db.commit()
    return True


def get_beans_count(
    db: Session,
    search: Optional[str] = None,
    roast_level: Optional[str] = None,
    bean_type: Optional[str] = None
) -> int:
    """원두 개수 조회 (검색 및 필터링 지원)"""
    query = db.query(Bean)
    
    if search:
        query = query.filter(
            (Bean.name.contains(search)) |
            (Bean.origin.contains(search)) |
            (Bean.variety.contains(search))
        )
    
    if bean_type:
        query = query.filter(Bean.type == bean_type)
    
    if roast_level:
        if roast_level == "Green":
            query = query.filter(Bean.type == "GREEN_BEAN")
        elif roast_level == "Roasted":
            query = query.filter(Bean.type == "ROASTED_BEAN")
        else:
            try:
                uppercase_level = roast_level.upper()
                query = query.filter(Bean.roast_profile == uppercase_level)
            except:
                pass
            
    return query.count()


def update_bean_quantity(
    db: Session,
    bean_id: int,
    quantity_change: float
) -> Optional[Bean]:
    """원두 재고량 조정 (로스팅 등으로 인한 감소/증가)"""
    db_bean = get_bean(db, bean_id)
    if not db_bean:
        return None
    
    db_bean.quantity_kg += quantity_change
    if db_bean.quantity_kg < 0:
        db_bean.quantity_kg = 0
    
    db.commit()
    db.refresh(db_bean)
    return db_bean
