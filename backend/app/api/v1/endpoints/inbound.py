from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional, List
import httpx
import logging
import os
import uuid
from app.services.ocr_service import OCRService
from app.services.image_service import image_service
from app.schemas.inbound import OCRResponse, AnalyzeUrlRequest, PaginatedInboundResponse
from app.config import settings
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import or_
from app.models.inbound_document import InboundDocument
from app.models.inbound_document_detail import InboundDocumentDetail
from app.models.inbound_receiver import InboundReceiver
from app.models.inbound_item import InboundItem
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.bean import Bean, BeanType
from app.models.supplier import Supplier
from app.schemas.inbound import InboundConfirmRequest

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
ocr_service = OCRService()

# === 생두 매칭 헬퍼 함수 ===
def match_bean_multi_field(bean_name: str, db: Session) -> tuple[Bean | None, str, str]:
    """
    다중 필드로 생두 매칭 시도 (대소문자 무시)

    Args:
        bean_name: OCR에서 추출한 생두명
        db: DB 세션

    Returns:
        (매칭된 Bean 객체 또는 None, 매칭 필드, 매칭 방법)
        - Bean: 매칭된 생두 객체 (없으면 None)
        - match_field: "name", "name_en", "name_ko", "new"
        - match_method: "exact", "case_insensitive", "new"
    """
    if not bean_name:
        return None, "new", "new"

    from sqlalchemy import func

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

    # 7. 매칭 실패
    return None, "new", "new"

@router.post("/analyze", response_model=OCRResponse)
async def analyze_inbound_document(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Analyze an inbound document (invoice) from a file upload or a URL.
    1. Uploads the image to Google Drive (Inbound Folder).
    2. Performs OCR using Gemini.
    3. Returns structured data + Drive Link.
    """
    image_bytes = None
    filename = "unknown.jpg"
    mime_type = "image/jpeg"

    # 1. Get Image Data
    if file:
        image_bytes = await file.read()
        filename = file.filename
        mime_type = file.content_type or "image/jpeg"
    elif url:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                image_bytes = response.content
                filename = "url_import.jpg" # Generate a better name if possible
                mime_type = response.headers.get("content-type", "image/jpeg")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Must provide either 'file' or 'url'")

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image data")

    # 1. Security Validation
    is_valid, error_msg = image_service.validate_image(image_bytes, filename)
    if not is_valid:
        logger.warning(f"Image validation failed: {filename} - {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)

    # 3. Perform OCR (Validate first)
    try:
        ocr_result = ocr_service.analyze_image(image_bytes, mime_type)
        if ocr_result.get("error") == "INVALID_DOCUMENT":
            logger.warning(f"Invalid document detected: {filename}")
            raise HTTPException(
                status_code=400, 
                detail="INVALID_DOCUMENT"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR Analysis Failed: {e}")
        if "GEMINI_QUOTA_EXCEEDED" in str(e):
             raise HTTPException(
                status_code=429, 
                detail="Google Gemini API Quota Exceeded. Please try again later (approx. 1 min)."
            )
        raise HTTPException(status_code=500, detail=f"OCR Analysis Failed: {str(e)}")

    # 2. Process and Save to Local Storage (Tiered)
    image_data = None
    try:
        image_data = image_service.process_and_save(image_bytes, filename)
        drive_link = f"/static/uploads/inbound/{image_data['paths']['original']}"
        logger.info(f"Image processed and saved: {image_data['paths']}")
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        # Fallback to simple save if needed, or raise error. 
        # For now, we prefer raising error to ensure data integrity.
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

    # 4. Merge Results (새로운 구조화된 데이터 + 하위 호환성)
    from app.schemas.inbound import (
        DocumentInfo, SupplierInfo, ReceiverInfo,
        AmountsInfo, AdditionalInfo
    )

    # 새로운 구조화된 데이터 생성
    document_info = DocumentInfo(**ocr_result.get("document_info", {})) if "document_info" in ocr_result else None
    supplier_info = SupplierInfo(**ocr_result.get("supplier", {})) if "supplier" in ocr_result else None
    receiver_info = ReceiverInfo(**ocr_result.get("receiver", {})) if "receiver" in ocr_result else None
    amounts_info = AmountsInfo(**ocr_result.get("amounts", {})) if "amounts" in ocr_result else None
    additional_info = AdditionalInfo(**ocr_result.get("additional_info", {})) if "additional_info" in ocr_result else None

    # 5. 각 아이템에 대해 생두 매칭 시도 (NEW)
    items_with_match_info = []
    for item_data in ocr_result.get("items", []):
        bean_name = item_data.get("bean_name")

        # 매칭 시도
        matched_bean, match_field, match_method = match_bean_multi_field(bean_name, db)

        # 매칭 정보 추가
        item_data["matched"] = matched_bean is not None
        item_data["match_field"] = match_field
        item_data["match_method"] = match_method
        item_data["bean_id"] = matched_bean.id if matched_bean else None

        items_with_match_info.append(item_data)

    response = OCRResponse(
        # 디버그 텍스트
        debug_raw_text=ocr_result.get("debug_raw_text"),

        # 새로운 구조화된 데이터
        document_info=document_info,
        supplier=supplier_info,
        receiver=receiver_info,
        amounts=amounts_info,
        items=items_with_match_info,  # 매칭 정보가 포함된 아이템
        additional_info=additional_info,

        # 하위 호환성 (기존 필드)
        supplier_name=ocr_result.get("supplier", {}).get("name"),
        contract_number=ocr_result.get("document_info", {}).get("contract_number"),
        supplier_phone=ocr_result.get("supplier", {}).get("phone"),
        supplier_email=ocr_result.get("supplier", {}).get("email"),
        receiver_name=ocr_result.get("receiver", {}).get("name"),
        invoice_date=ocr_result.get("document_info", {}).get("invoice_date"),
        total_amount=ocr_result.get("amounts", {}).get("total_amount"),

        # 메타 정보 (Tiered Storage)
        drive_link=drive_link,
        original_image_path=image_data['paths'].get('original') if image_data else None,
        webview_image_path=image_data['paths'].get('webview') if image_data else None,
        thumbnail_image_path=image_data['paths'].get('thumbnail') if image_data else None,
        image_width=image_data.get('width') if image_data else None,
        image_height=image_data.get('height') if image_data else None,
        file_size_bytes=image_data.get('file_size_bytes') if image_data else None
    )

    return response

@router.get("/list", response_model=PaginatedInboundResponse)
def get_inbound_list(
    page: int = 1,
    limit: int = 20,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    명세서 목록 조회 (Pagination & Filtering)
    """
    query = db.query(InboundDocument)

    # Filtering
    if from_date:
        query = query.filter(InboundDocument.invoice_date >= from_date)
    if to_date:
        query = query.filter(InboundDocument.invoice_date <= to_date)
    
    if keyword:
        # Search in Contract Number or Supplier Name
        query = query.filter(
            or_(
                InboundDocument.contract_number.ilike(f"%{keyword}%"),
                InboundDocument.supplier_name.ilike(f"%{keyword}%")
            )
        )

    # Sorting (Latest first)
    query = query.order_by(InboundDocument.created_at.desc())

    # Pagination
    total = query.count()
    total_pages = (total + limit - 1) // limit
    
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": limit,
        "total_pages": total_pages
    }

@router.get("/check-duplicate/{contract_number}")

@router.get("/check-duplicate/{contract_number}")
def check_duplicate_contract_number(contract_number: str, db: Session = Depends(get_db)):
    """
    Check if a contract number already exists.
    Returns {"exists": true/false}
    """
    existing_doc = db.query(InboundDocument).filter(
        InboundDocument.contract_number == contract_number
    ).first()
    
    if existing_doc:
        return {"exists": True, "detail": "⚠️ 이미 등록된 명세서(계약번호)입니다."}
    return {"exists": False, "detail": "사용 가능한 번호입니다."}

# --- Save Endpoint ---


@router.post("/confirm", status_code=201)
def confirm_inbound(
    request: InboundConfirmRequest,
    db: Session = Depends(get_db)
):
    """
    Saves the confirmed inbound data:
    1. Check for Duplicate Contract Number.
    2. Manage Supplier (Find existing or Create new).
    3. Create InboundDocument record.
    4. Create InventoryLog records for each item.
    5. Update Bean quantity.
    """
    # 0. Check Duplicate Check
    if request.document.contract_number:
        # Check strict match on contract_number
        existing_doc = db.query(InboundDocument).filter(
            InboundDocument.contract_number == request.document.contract_number
        ).first()
        if existing_doc:
             raise HTTPException(status_code=400, detail=f"Duplicate Contract Number: {request.document.contract_number}")

    # 1. Manage Supplier
    supplier_id = request.document.supplier_id
    if not supplier_id and request.document.supplier_name:
        # Try to find by name
        supplier = db.query(Supplier).filter(Supplier.name == request.document.supplier_name).first()
        if not supplier:
            # Create New Supplier
            supplier = Supplier(
                name=request.document.supplier_name,
                contact_phone=request.document.supplier_phone,
                contact_email=request.document.supplier_email,
                representative_name=request.document.receiver_name or "" # Fallback or separate field?
            )
            db.add(supplier)
            db.flush() # Get ID
        
        # If supplier exists, we could update info, but let's skip for safety.
        supplier_id = supplier.id

    # 2. Create Document
    doc_data = request.document.dict(exclude={'supplier_phone', 'supplier_email'})
    doc_data['supplier_id'] = supplier_id

    new_doc = InboundDocument(**doc_data)
    db.add(new_doc)
    db.flush() # Get ID

    # 2-1. Create Document Detail (NEW - Option B)
    if request.document_info or request.supplier or request.amounts or request.additional_info:
        detail_data = {}

        # Document info
        if request.document_info:
            detail_data['document_number'] = request.document_info.document_number
            detail_data['issue_date'] = request.document_info.issue_date
            detail_data['delivery_date'] = request.document_info.delivery_date
            detail_data['payment_due_date'] = request.document_info.payment_due_date
            detail_data['invoice_type'] = request.document_info.invoice_type

        # Supplier detailed info
        if request.supplier:
            detail_data['supplier_business_number'] = request.supplier.business_number
            detail_data['supplier_address'] = request.supplier.address
            detail_data['supplier_phone'] = request.supplier.phone
            detail_data['supplier_fax'] = request.supplier.fax
            detail_data['supplier_email'] = request.supplier.email
            detail_data['supplier_representative'] = request.supplier.representative
            detail_data['supplier_contact_person'] = request.supplier.contact_person
            detail_data['supplier_contact_phone'] = request.supplier.contact_phone

        # Amount details
        if request.amounts:
            detail_data['subtotal'] = request.amounts.subtotal
            detail_data['tax_amount'] = request.amounts.tax_amount
            detail_data['grand_total'] = request.amounts.grand_total or request.amounts.total_amount
            detail_data['currency'] = request.amounts.currency

        # Additional info
        if request.additional_info:
            detail_data['payment_terms'] = request.additional_info.payment_terms
            detail_data['shipping_method'] = request.additional_info.shipping_method
            detail_data['notes'] = request.additional_info.notes
            detail_data['remarks'] = request.additional_info.remarks

        detail = InboundDocumentDetail(
            inbound_document_id=new_doc.id,
            **detail_data
        )
        db.add(detail)

    # 2-2. Create Receiver (NEW - Option B)
    if request.receiver:
        receiver = InboundReceiver(
            inbound_document_id=new_doc.id,
            name=request.receiver.name,
            business_number=request.receiver.business_number,
            address=request.receiver.address,
            phone=request.receiver.phone,
            contact_person=request.receiver.contact_person
        )
        db.add(receiver)

    # 3. Process Items
    for idx, item in enumerate(request.items):
        bean_name = item.bean_name
        quantity = item.quantity or 0.0

        # Find Bean (다중 필드 매칭)
        bean, match_field, match_method = match_bean_multi_field(bean_name, db)

        if not bean:
            # Auto-create bean if missing
            logger.info(f"Creating new bean: {bean_name} (no match found)")
            bean = Bean(
                name=bean_name,
                name_en=bean_name,  # OCR 결과를 영문명으로 저장
                quantity_kg=0.0,
                origin=item.origin or "Unknown",
                type=BeanType.GREEN_BEAN
            )
            db.add(bean)
            db.flush()
        else:
            logger.info(f"Matched bean: {bean_name} → {bean.name} (ID: {bean.id}, field: {match_field})")

        # Create Log (기존 로직 유지)
        log = InventoryLog(
            bean_id=bean.id,
            change_type=InventoryChangeType.PURCHASE,
            change_amount=quantity,
            current_quantity=bean.quantity_kg + quantity,
            inbound_document_id=new_doc.id,
            notes=f"Inbound from {new_doc.supplier_name} (Contract: {new_doc.contract_number or 'N/A'})"
        )
        db.add(log)

        # Update Bean Quantity
        bean.quantity_kg += quantity

        # Create InboundItem (NEW - Option B)
        inbound_item = InboundItem(
            inbound_document_id=new_doc.id,
            item_order=idx,
            bean_name=item.bean_name,
            specification=item.specification,
            unit=item.unit,
            quantity=item.quantity,
            remaining_quantity=item.quantity,  # FIFO Initial State
            origin=item.origin,
            unit_price=item.unit_price,
            supply_amount=item.amount,  # OCRItem.amount maps to supply_amount
            tax_amount=None,  # Not provided in OCRItem
            notes=item.note
        )
        db.add(inbound_item)
    
    db.commit()
    return {"status": "success", "document_id": new_doc.id, "supplier_id": supplier_id}
