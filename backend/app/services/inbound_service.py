import logging
import re
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.bean import Bean, BeanType
from app.models.inventory_log import InventoryChangeType
from app.repositories.inbound_repository import InboundRepository
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory_log import InventoryLogCreate
from app.schemas.inbound import InboundConfirmRequest, InboundConfirmResponse

logger = logging.getLogger(__name__)

class InboundService:
    def __init__(self):
        # Repositories are initialized per request usually, but here we can pass DB session to methods
        pass

    def match_bean_multi_field(self, bean_name: str, db: Session) -> tuple[Bean | None, str, str]:
        """
        다중 필드로 생두 매칭 시도 (대소문자 무시)
        """
        if not bean_name:
            return None, "new", "new"

        # 1. Exact match 시도 (Bean.name)
        bean = db.query(Bean).filter(Bean.name == bean_name).first()
        if bean:
            return bean, "name", "exact"

        # 2. Exact match 시도 (Bean.name_en)
        bean = db.query(Bean).filter(Bean.name_en == bean_name).first()
        if bean:
            return bean, "name_en", "exact"

        # 3. Exact match 시도 (Bean.name_ko)
        bean = db.query(Bean).filter(Bean.name_ko == bean_name).first()
        if bean:
            return bean, "name_ko", "exact"

        # 4. Case-insensitive match 시도 (Bean.name)
        bean = db.query(Bean).filter(func.lower(Bean.name) == bean_name.lower()).first()
        if bean:
            return bean, "name", "case_insensitive"

        # 5. Case-insensitive match 시도 (Bean.name_en)
        bean = db.query(Bean).filter(func.lower(Bean.name_en) == bean_name.lower()).first()
        if bean:
            return bean, "name_en", "case_insensitive"

        # 6. Case-insensitive match 시도 (Bean.name_ko)
        bean = db.query(Bean).filter(func.lower(Bean.name_ko) == bean_name.lower()).first()
        if bean:
            return bean, "name_ko", "case_insensitive"

        return None, "new", "new"

    def confirm_inbound(self, db: Session, request: InboundConfirmRequest) -> dict:
        inbound_repo = InboundRepository(db)
        inventory_repo = InventoryRepository(db)

        # 0. Check Duplicate Check
        if request.document.contract_number:
            existing_doc = inbound_repo.get_document_by_contract_number(request.document.contract_number)
            if existing_doc:
                raise ValueError(f"Duplicate Contract Number: {request.document.contract_number}")

        # 1. Manage Supplier
        supplier_id = request.document.supplier_id
        if not supplier_id and request.document.supplier_name:
            supplier = inbound_repo.get_supplier_by_name(request.document.supplier_name)
            if not supplier:
                # Create New Supplier
                supplier = inbound_repo.create_supplier({
                    "name": request.document.supplier_name,
                    "contact_phone": request.document.supplier_phone,
                    "contact_email": request.document.supplier_email,
                    "representative_name": request.document.receiver_name or ""
                })
            supplier_id = supplier.id

        # 2. Create Document
        doc_data = request.document.dict(exclude={"supplier_phone", "supplier_email"})
        doc_data["supplier_id"] = supplier_id
        doc_data["processing_status"] = "completed"
        
        new_doc = inbound_repo.create_document(doc_data)

        # 2-1. Create Document Detail
        if request.document_info or request.supplier or request.amounts or request.additional_info:
            detail_data = {"inbound_document_id": new_doc.id}
            
            if request.document_info:
                detail_data.update({
                    "document_number": request.document_info.document_number,
                    "issue_date": request.document_info.issue_date,
                    "delivery_date": request.document_info.delivery_date,
                    "payment_due_date": request.document_info.payment_due_date,
                    "invoice_type": request.document_info.invoice_type
                })
            
            if request.supplier:
                detail_data.update({
                    "supplier_business_number": request.supplier.business_number,
                    "supplier_address": request.supplier.address,
                    "supplier_phone": request.supplier.phone,
                    "supplier_fax": request.supplier.fax,
                    "supplier_email": request.supplier.email,
                    "supplier_representative": request.supplier.representative,
                    "supplier_contact_person": request.supplier.contact_person,
                    "supplier_contact_phone": request.supplier.contact_phone
                })
                
            if request.amounts:
                detail_data.update({
                    "subtotal": request.amounts.subtotal,
                    "tax_amount": request.amounts.tax_amount,
                    "grand_total": request.amounts.grand_total or request.amounts.total_amount,
                    "currency": request.amounts.currency
                })
                
            if request.additional_info:
                detail_data.update({
                    "payment_terms": request.additional_info.payment_terms,
                    "shipping_method": request.additional_info.shipping_method,
                    "notes": request.additional_info.notes,
                    "remarks": request.additional_info.remarks
                })
            
            inbound_repo.create_detail(detail_data)

        # 2-2. Create Receiver
        if request.receiver:
            inbound_repo.create_receiver({
                "inbound_document_id": new_doc.id,
                "name": request.receiver.name,
                "business_number": request.receiver.business_number,
                "address": request.receiver.address,
                "phone": request.receiver.phone,
                "contact_person": request.receiver.contact_person,
            })

        # 3. Process Items
        for idx, item in enumerate(request.items):
            bean_name = item.bean_name
            quantity = item.quantity or 0.0

            # Find Bean (다중 필드 매칭)
            bean, match_field, match_method = self.match_bean_multi_field(bean_name, db)

            if not bean:
                logger.info(f"Creating new bean: {bean_name} (no match found)")
                # Bean Creation should ideally be in BeanRepository, but for now using DB directly or assuming simple
                # Let's use DB session directly here as it's a specific 'create on fly' logic
                bean = Bean(
                    name=bean_name,
                    name_en=bean_name,
                    quantity_kg=0.0,
                    origin=item.origin or "Unknown",
                    type=BeanType.GREEN_BEAN,
                )
                db.add(bean)
                db.flush()
            else:
                logger.info(
                    f"Matched bean: {bean_name} -> {bean.name} (ID: {bean.id}, field: {match_field})"
                )

            # Create Inventory Log (using InventoryRepository mostly, but need specific fields)
            # InventoryLogService uses InventoryRepository. Here we are inside InboundService.
            # We can use InventoryRepository directly.
            
            log = InventoryLogCreate(
                bean_id=bean.id,
                change_type=InventoryChangeType.PURCHASE.value,
                change_amount=quantity,
                inbound_document_id=new_doc.id,
                notes=f"Inbound from {new_doc.supplier_name} (Contract: {new_doc.contract_number or 'N/A'})"
            )
            
            # Using InventoryRepository to create log and update stock
            # Note: InventoryRepository.create_log handles stock update
            inventory_repo.create_log(log)

            # Create InboundItem
            inbound_repo.create_item({
                "inbound_document_id": new_doc.id,
                "item_order": idx,
                "bean_name": item.bean_name,
                "specification": item.specification,
                "unit": item.unit,
                "quantity": item.quantity,
                "remaining_quantity": item.quantity,
                "origin": item.origin,
                "unit_price": item.unit_price,
                "supply_amount": item.amount,
                "tax_amount": None,
                "notes": item.note,
                "order_number": item.order_number,
                "bean_id": bean.id # Link to the matched bean
            })

        db.commit()
        return {"status": "success", "document_id": new_doc.id, "supplier_id": supplier_id}

inbound_service = InboundService()
