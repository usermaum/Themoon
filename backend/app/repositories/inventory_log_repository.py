from sqlalchemy.orm import Session
from app.models.inventory_log import InventoryLog
from app.schemas.inventory_log import InventoryLogCreate
from app.repositories.base_repository import BaseRepository


class InventoryLogRepository(BaseRepository[InventoryLog, InventoryLogCreate, dict]):
    def __init__(self, db: Session):
        super().__init__(InventoryLog, db)
