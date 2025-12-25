from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.inbound_document import InboundDocument
from app.models.inbound_item import InboundItem
from app.schemas.inbound import InboundDocumentCreate
from app.repositories.base_repository import BaseRepository


class InboundRepository(BaseRepository[InboundDocument, InboundDocumentCreate, dict]):
    def __init__(self, db: Session):
        super().__init__(InboundDocument, db)

    def get_document_with_items(self, document_id: int) -> Optional[InboundDocument]:
        return self.db.query(InboundDocument).filter(InboundDocument.id == document_id).first()

    def get_fifo_candidates(self, bean_id: int) -> List[InboundItem]:
        """잔여 재고가 있는 입고 항목을 오래된 순서대로 조회 (FIFO)"""
        return (
            self.db.query(InboundItem)
            .filter(InboundItem.bean_id == bean_id, InboundItem.remaining_quantity > 0)
            .order_by(asc(InboundItem.created_at))
            .all()
        )

    def update_item_remaining_quantity(self, item_id: int, new_quantity: float) -> Optional[InboundItem]:
        item = self.db.query(InboundItem).filter(InboundItem.id == item_id).first()
        if item:
            item.remaining_quantity = new_quantity
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
        return item
