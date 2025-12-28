from typing import List, Optional
from sqlalchemy.orm import Session, contains_eager
from app.models.bean import Bean
from app.models.inventory_log import InventoryLog

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_logs(
        self,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[InventoryLog]:
        query = self.db.query(InventoryLog).join(Bean)

        if bean_id:
            query = query.filter(InventoryLog.bean_id == bean_id)
        if change_types:
            query = query.filter(InventoryLog.change_type.in_(change_types))
        if search:
            query = query.filter(
                (Bean.name.contains(search))
                | (Bean.name_ko.contains(search))
                | (Bean.name_en.contains(search))
                | (Bean.origin.contains(search))
                | (Bean.origin_ko.contains(search))
            )

        return (
            query.options(contains_eager(InventoryLog.bean))
            .order_by(InventoryLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_logs(
        self,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None,
        search: Optional[str] = None,
    ) -> int:
        query = self.db.query(InventoryLog).join(Bean)

        if bean_id:
            query = query.filter(InventoryLog.bean_id == bean_id)
        if change_types:
            query = query.filter(InventoryLog.change_type.in_(change_types))
        if search:
            query = query.filter(
                (Bean.name.contains(search))
                | (Bean.name_ko.contains(search))
                | (Bean.name_en.contains(search))
                | (Bean.origin.contains(search))
                | (Bean.origin_ko.contains(search))
            )

        return query.count()

    def get_bean(self, bean_id: int) -> Optional[Bean]:
        return self.db.query(Bean).filter(Bean.id == bean_id).first()

    def get_log(self, log_id: int) -> Optional[InventoryLog]:
        return self.db.query(InventoryLog).filter(InventoryLog.id == log_id).first()

    def create_log(self, log: InventoryLog) -> InventoryLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def delete_log(self, log: InventoryLog):
        self.db.delete(log)
        self.db.commit()
