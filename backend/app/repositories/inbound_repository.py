from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc
from app.models.inbound_document import InboundDocument
from app.models.inbound_item import InboundItem
from app.models.inbound_document_detail import InboundDocumentDetail
from app.models.inbound_receiver import InboundReceiver
from app.models.supplier import Supplier
from app.schemas.inbound import InboundDocumentCreate

class InboundRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_document(self, document_id: int) -> Optional[InboundDocument]:
        return self.db.query(InboundDocument).filter(InboundDocument.id == document_id).first()
    
    def get_document_with_items(self, document_id: int) -> Optional[InboundDocument]:
        return self.db.query(InboundDocument).filter(InboundDocument.id == document_id).first()

    def get_document_by_contract_number(self, contract_number: str) -> Optional[InboundDocument]:
        return self.db.query(InboundDocument).filter(InboundDocument.contract_number == contract_number).first()
    
    def get_supplier_by_name(self, name: str) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.name == name).first()

    def create_supplier(self, supplier_data: dict) -> Supplier:
        supplier = Supplier(**supplier_data)
        self.db.add(supplier)
        self.db.flush()
        return supplier

    def create_document(self, doc_data: dict) -> InboundDocument:
        new_doc = InboundDocument(**doc_data)
        self.db.add(new_doc)
        self.db.flush()
        return new_doc

    def create_detail(self, detail_data: dict) -> InboundDocumentDetail:
        detail = InboundDocumentDetail(**detail_data)
        self.db.add(detail)
        return detail

    def create_receiver(self, receiver_data: dict) -> InboundReceiver:
        receiver = InboundReceiver(**receiver_data)
        self.db.add(receiver)
        return receiver

    def create_item(self, item_data: dict) -> InboundItem:
        item = InboundItem(**item_data)
        self.db.add(item)
        return item
    
    def get_fifo_candidates(self, bean_id: int) -> List[InboundItem]:
        """잔여 재고가 있는 입고 항목을 오래된 순서대로 조회 (FIFO)"""
        return (
            self.db.query(InboundItem)
            .filter(InboundItem.bean_id == bean_id, InboundItem.remaining_quantity > 0)
            .order_by(asc(InboundItem.created_at))
            .all()
        )

    def update_item_remaining_quantity(self, item_id: int, new_quantity: float) -> Optional[InboundItem]:
        """입고 품목 재고 수량 업데이트"""
        item = self.db.query(InboundItem).filter(InboundItem.id == item_id).first()
        if item:
            item.remaining_quantity = new_quantity
            self.db.add(item)
            self.db.flush() # Commit is handled by Service
        return item

    def get_list(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> tuple[List[InboundDocument], int]:
        query = self.db.query(InboundDocument)

        if from_date:
            query = query.filter(InboundDocument.invoice_date >= from_date)
        if to_date:
            query = query.filter(InboundDocument.invoice_date <= to_date)
        
        if keyword:
            query = query.filter(
                or_(
                    InboundDocument.contract_number.ilike(f"%{keyword}%"),
                    InboundDocument.supplier_name.ilike(f"%{keyword}%"),
                )
            )
        
        total = query.count()
        query = query.order_by(InboundDocument.created_at.desc())
        items = query.offset(skip).limit(limit).all()
        
        return items, total
