from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.bean import Bean
from app.models.inventory_log import InventoryLog
from app.schemas.inventory_log import InventoryLogCreate
from app.repositories.inventory_repository import InventoryRepository


class InventoryLogService:
    def get_logs(
        self,
        db: Session,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[InventoryLog]:
        repo = InventoryRepository(db)
        return repo.get_logs(bean_id, change_types, search, skip, limit)

    def get_logs_count(
        self,
        db: Session,
        bean_id: Optional[int] = None,
        change_types: Optional[List[str]] = None,
        search: Optional[str] = None,
    ) -> int:
        repo = InventoryRepository(db)
        return repo.count_logs(bean_id, change_types, search)

    def create_log(self, db: Session, log: InventoryLogCreate) -> InventoryLog:
        repo = InventoryRepository(db)
        
        # Bean의 현재 재고량 가져오기
        bean = repo.get_bean(log.bean_id)
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
            notes=log.notes,
        )

        return repo.create_log(db_log)

    def update_log(
        self, db: Session, log_id: int, change_amount: float, notes: Optional[str] = None
    ) -> Optional[InventoryLog]:
        repo = InventoryRepository(db)
        
        # 기존 로그 조회
        db_log = repo.get_log(log_id)
        if not db_log:
            return None

        # 원두 조회
        bean = repo.get_bean(db_log.bean_id)
        if not bean:
            raise ValueError("Bean not found")

        # 기존 변경량 되돌리기
        bean.quantity_kg -= db_log.change_amount

        # 새 변경량 적용
        new_quantity = bean.quantity_kg + change_amount
        if new_quantity < 0:
            raise ValueError("Insufficient inventory")

        bean.quantity_kg = new_quantity

        # 로그 업데이트 (This part remains in service as it modifies object state before commit)
        # However, repository's save method isn't explicitly used for update in SQLAlchemy usually unless using specific pattern.
        # But we need to commit. We can add a method to repo or just use db.commit() here if we want strict repo pattern we'd verify.
        # Given the repo `create_log` does commit, let's add `update_log` or `commit` to repo.
        # For now, let's keep direct object modification and use a repo method to save/commit.
        
        db_log.change_amount = change_amount
        db_log.current_quantity = new_quantity
        if notes is not None:
            db_log.notes = notes

        # Using implicit commit for now or adding a save method to repo.
        # Let's use `repo.db.commit()` effectively via a repo wrapper method if strictly following pattern,
        # but the request was to isolate query logic.
        repo.db.commit()
        repo.db.refresh(db_log)
        return db_log

    def delete_log(self, db: Session, log_id: int) -> bool:
        repo = InventoryRepository(db)
        
        # 기존 로그 조회
        db_log = repo.get_log(log_id)
        if not db_log:
            return False

        # 원두 조회
        bean = repo.get_bean(db_log.bean_id)
        if not bean:
            raise ValueError("Bean not found")

        # 변경량 되돌리기
        new_quantity = bean.quantity_kg - db_log.change_amount
        if new_quantity < 0:
            raise ValueError("Cannot delete: would result in negative inventory")

        bean.quantity_kg = new_quantity

        # 로그 삭제
        repo.delete_log(db_log)
        return True


inventory_log_service = InventoryLogService()
