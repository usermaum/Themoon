from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional, List
import httpx
import logging
import os
import uuid
from app.services.google_drive_service import GoogleDriveService
from app.services.ocr_service import OCRService
from app.schemas.inbound import OCRResponse, AnalyzeUrlRequest
from app.config import settings
from sqlalchemy.orm import Session
from app.database import get_db
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
drive_service = GoogleDriveService()
ocr_service = OCRService()

@router.post("/analyze", response_model=OCRResponse)
async def analyze_inbound_document(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None)
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

    # 2. Save to Local Storage (Instead of Google Drive)
    drive_link = None
    try:
        # Create directory if not exists
        upload_dir = os.path.join("static", "uploads", "inbound")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(image_bytes)
            
        # Generate URL (Assuming backend is running on localhost:8000 or using relative path)
        # We store relative path or full URL. Frontend usually needs full URL to load image.
        # But for portability, relative path is better, and frontend adds base URL.
        # However, `drive_link` field expects a full URL usually.
        # Let's return the full URL based on settings or request.base_url?
        # For simplicity MVP: http://localhost:8000/static/uploads/inbound/...
        # But better: /static/uploads/inbound/... and let frontend handle base.
        drive_link = f"/static/uploads/inbound/{unique_filename}"
        
        logger.info(f"Image saved locally at: {file_path}")

    except Exception as e:
        logger.error(f"Local File Save Failed: {e}")
        # Continue with OCR even if save fails? No, if we can't save locally, something is wrong.
        # But strictly speaking OCR can run without saving.
        # Let's warn and continue?
        logger.warning(f"Continuing without Local Save due to error: {e}")

    # 3. Perform OCR
    try:
        ocr_result = ocr_service.analyze_image(image_bytes, mime_type)
    except Exception as e:
        logger.error(f"OCR Analysis Failed: {e}")
        raise HTTPException(status_code=500, detail=f"OCR Analysis Failed: {str(e)}")

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

    response = OCRResponse(
        # 디버그 텍스트
        debug_raw_text=ocr_result.get("debug_raw_text"),

        # 새로운 구조화된 데이터
        document_info=document_info,
        supplier=supplier_info,
        receiver=receiver_info,
        amounts=amounts_info,
        items=ocr_result.get("items", []),
        additional_info=additional_info,

        # 하위 호환성 (기존 필드)
        supplier_name=ocr_result.get("supplier", {}).get("name"),
        contract_number=ocr_result.get("document_info", {}).get("contract_number"),
        supplier_phone=ocr_result.get("supplier", {}).get("phone"),
        supplier_email=ocr_result.get("supplier", {}).get("email"),
        receiver_name=ocr_result.get("receiver", {}).get("name"),
        invoice_date=ocr_result.get("document_info", {}).get("invoice_date"),
        total_amount=ocr_result.get("amounts", {}).get("total_amount"),

        # 메타 정보
        drive_link=drive_link
    )

    return response

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

        # Find Bean
        bean = db.query(Bean).filter(Bean.name == bean_name).first()
        if not bean:
            # Auto-create bean if missing
            bean = Bean(name=bean_name, quantity_kg=0.0, origin="Unknown", type=BeanType.GREEN_BEAN)
            db.add(bean)
            db.flush()

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
            origin=item.origin,
            unit_price=item.unit_price,
            supply_amount=item.amount,  # OCRItem.amount maps to supply_amount
            tax_amount=None,  # Not provided in OCRItem
            notes=item.note
        )
        db.add(inbound_item)
    
    db.commit()
    return {"status": "success", "document_id": new_doc.id, "supplier_id": supplier_id}
