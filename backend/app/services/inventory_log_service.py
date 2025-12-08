from sqlalchemy.orm import Session
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.bean import Bean
from app.schemas.inventory_log import InventoryLogCreate
from typing import List, Optional

class InventoryLogService:
    def get_logs(
        self,
        db: Session,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[InventoryLog]:
        query = db.query(InventoryLog)
        if bean_id:
            query = query.filter(InventoryLog.bean_id == bean_id)
        if change_types:
            query = query.filter(InventoryLog.change_type.in_(change_types))
        return query.order_by(InventoryLog.created_at.desc()).offset(skip).limit(limit).all()

    def get_logs_count(
        self,
        db: Session,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None
    ) -> int:
        """입출고 기록 총 개수 조회"""
        query = db.query(InventoryLog)
        if bean_id:
            query = query.filter(InventoryLog.bean_id == bean_id)
        if change_types:
            query = query.filter(InventoryLog.change_type.in_(change_types))
        return query.count()

    def create_log(self, db: Session, log: InventoryLogCreate) -> InventoryLog:
        # Bean의 현재 재고량 가져오기
        bean = db.query(Bean).filter(Bean.id == log.bean_id).first()
        if not bean:
            raise ValueError("Bean not found")
        
        # 재고량 업데이트
        new_quantity = bean.quantity_kg + log.change_amount
        if new_quantity < 0:
            raise ValueError("Insufficient inventory")
        
        bean.quantity_kg = new_quantity
        
        # 로그 생성
        db_log = InventoryLog(
            bean_id=log.bean_id,
            change_type=log.change_type,
            change_amount=log.change_amount,
            current_quantity=new_quantity,
            notes=log.notes
        )
        
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    def update_log(self, db: Session, log_id: int, change_amount: float, notes: Optional[str] = None) -> Optional[InventoryLog]:
        # 기존 로그 조회
        db_log = db.query(InventoryLog).filter(InventoryLog.id == log_id).first()
        if not db_log:
            return None
        
        # 원두 조회
        bean = db.query(Bean).filter(Bean.id == db_log.bean_id).first()
        if not bean:
            raise ValueError("Bean not found")
        
        # 기존 변경량 되돌리기
        bean.quantity_kg -= db_log.change_amount
        
        # 새 변경량 적용
        new_quantity = bean.quantity_kg + change_amount
        if new_quantity < 0:
            raise ValueError("Insufficient inventory")
        
        bean.quantity_kg = new_quantity
        
        # 로그 업데이트
        db_log.change_amount = change_amount
        db_log.current_quantity = new_quantity
        if notes is not None:
            db_log.notes = notes
        
        db.commit()
        db.refresh(db_log)
        return db_log

    def delete_log(self, db: Session, log_id: int) -> bool:
        # 기존 로그 조회
        db_log = db.query(InventoryLog).filter(InventoryLog.id == log_id).first()
        if not db_log:
            return False
        
        # 원두 조회
        bean = db.query(Bean).filter(Bean.id == db_log.bean_id).first()
        if not bean:
            raise ValueError("Bean not found")
        
        # 변경량 되돌리기
        new_quantity = bean.quantity_kg - db_log.change_amount
        if new_quantity < 0:
            raise ValueError("Cannot delete: would result in negative inventory")
        
        bean.quantity_kg = new_quantity
        
        # 로그 삭제
        db.delete(db_log)
        db.commit()
        return True

inventory_log_service = InventoryLogService()
