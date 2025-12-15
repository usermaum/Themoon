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
    bean_types: Optional[List[str]] = None,
    origin: Optional[str] = None,
    exclude_blend: bool = False
) -> List[Bean]:
    """원두 목록 조회 (페이징 및 검색 지원)"""
    query = db.query(Bean)

    if search:
        query = query.filter(
            (Bean.name.contains(search)) |
            (Bean.name_ko.contains(search)) |
            (Bean.name_en.contains(search)) |
            (Bean.origin.contains(search)) |
            (Bean.origin_ko.contains(search)) |
            (Bean.origin_en.contains(search)) |
            (Bean.variety.contains(search))
        )

    if bean_types:
        query = query.filter(Bean.type.in_(bean_types))

    if origin:
        query = query.filter(Bean.origin == origin)

    if exclude_blend:
        query = query.filter(Bean.origin != 'Blend')

    return query.offset(skip).limit(limit).all()


def create_bean(db: Session, bean: BeanCreate) -> Bean:
    """새 원두 등록"""
    db_bean = Bean(**bean.model_dump())
    db.add(db_bean)
    db.commit()
    db.refresh(db_bean)
    return db_bean


def update_bean(db: Session, bean_id: int, bean: BeanUpdate) -> Optional[Bean]:
    """원두 정보 수정"""
    db_bean = get_bean(db, bean_id)
    if not db_bean:
        return None
    
    # 제공된 필드만 업데이트
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


def get_beans_count(db: Session, search: Optional[str] = None, bean_types: Optional[List[str]] = None, origin: Optional[str] = None, exclude_blend: bool = False) -> int:
    """전체 원두 개수 조회 (필터 포함)"""
    query = db.query(Bean)

    if search:
        query = query.filter(
            (Bean.name.contains(search)) |
            (Bean.name_ko.contains(search)) |
            (Bean.name_en.contains(search)) |
            (Bean.origin.contains(search)) |
            (Bean.origin_ko.contains(search)) |
            (Bean.origin_en.contains(search)) |
            (Bean.variety.contains(search))
        )

    if bean_types:
        query = query.filter(Bean.type.in_(bean_types))

    if origin:
        query = query.filter(Bean.origin == origin)

    if exclude_blend:
        query = query.filter(Bean.origin != 'Blend')

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
