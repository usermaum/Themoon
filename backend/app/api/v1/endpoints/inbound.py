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

    # 4. Merge Results
    response = OCRResponse(
        supplier_name=ocr_result.get("supplier_name"),
        invoice_date=ocr_result.get("invoice_date"),
        total_amount=ocr_result.get("total_amount"),
        items=ocr_result.get("items", []),
        drive_link=drive_link
    )

    return response

# --- Save Endpoint ---
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inbound_document import InboundDocument
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.bean import Bean, BeanType
from app.schemas.inbound import InboundConfirmRequest

@router.post("/confirm", status_code=201)
def confirm_inbound(
    request: InboundConfirmRequest,
    db: Session = Depends(get_db)
):
    """
    Saves the confirmed inbound data:
    1. Create InboundDocument record.
    2. Create InventoryLog records for each item.
    3. Update Bean current_quantity.
    """
    # 1. Create Document
    doc_data = request.document.dict()
    new_doc = InboundDocument(**doc_data)
    db.add(new_doc)
    db.flush() # Get ID

    # 2. Process Items
    for item in request.items:
        bean_name = item.bean_name
        quantity = item.quantity
        
        # Find Bean
        bean = db.query(Bean).filter(Bean.name == bean_name).first()
        if not bean:
            # Auto-create bean if missing (Simple logic for Inbound ease)
            bean = Bean(name=bean_name, quantity_kg=0.0, origin="Unknown", type=BeanType.GREEN_BEAN)
            db.add(bean)
            db.flush()
        
        # Create Log
        log = InventoryLog(
            bean_id=bean.id,
            change_type=InventoryChangeType.PURCHASE,
            change_amount=quantity,
            current_quantity=bean.quantity_kg + quantity,
            inbound_document_id=new_doc.id,
            notes=f"Inbound from {new_doc.supplier_name}"
        )
        # Update Bean Quantity
        bean.quantity_kg += quantity
        
        db.add(log)
    
    db.commit()
    return {"status": "success", "document_id": new_doc.id}
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inbound_document import InboundDocument
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.bean import Bean
from app.schemas.inbound import InboundConfirmRequest

@router.post("/confirm", status_code=201)
def confirm_inbound(
    request: InboundConfirmRequest,
    db: Session = Depends(get_db)
):
    """
    Saves the confirmed inbound data:
    1. Create InboundDocument record.
    2. Create InventoryLog records for each item.
    3. Update Bean current_quantity (calculated via specific logic or relying on logs). 
       (InventoryLog trigger or service logic usually handles quantity updates, but here we might need to be explicit if no triggers exist)
    """
    # 1. Create Document
    doc_data = request.document.dict()
    new_doc = InboundDocument(**doc_data)
    db.add(new_doc)
    db.flush() # Get ID

    # 2. Process Items
    for item in request.items:
        # Find Bean (by name fuzzy match or exact? Frontend sends bean_id or name? 
        # The schema implies we are sending raw OCR items. We need to Map them to Bean IDs.
        # Ideally Frontend should allow selecting the Bean ID for each item.
        # But for now let's assume the frontend sends 'bean_name' and we try to find it, or we need to update Frontend to allow Bean Selection.
        
        # Checking schema: request.items is List[dict]. 
        # We need to clarify if frontend sends bean_id. 
        # Code view of `frontend/.../page.tsx` shows Inputs for `bean_name`.
        # Realistically, we need `bean_id` to link to InventoryLog.
        # For this MVP/Restoration, if we don't have bean_id, we can't create InventoryLog correctly linked to a Bean.
        # Logic: Try to find bean by name. If not found, create new? Or fail?
        # User requirement says "Automagically register". 
        # Let's try to find bean by name.
        
        bean_name = item.get('bean_name')
        quantity = float(item.get('quantity', 0))
        
        bean = db.query(Bean).filter(Bean.name == bean_name).first()
        if not bean:
            # Option: Create new bean if not exists?
            # Or skip?
            # Let's create a placeholder bean or error? 
            # Better: Create if missing to ensure flow doesn't break.
            bean = Bean(name=bean_name, remain_amount=0, origin="Unknown", type="Green") # Default values
            db.add(bean)
            db.flush()
        
        # Create Log
        log = InventoryLog(
            bean_id=bean.id,
            change_type=InventoryChangeType.PURCHASE,
            change_amount=quantity,
            current_quantity=bean.remain_amount + quantity, # Simple logic
            inbound_document_id=new_doc.id,
            notes=f"Inbound from {new_doc.supplier_name}"
        )
        # Update Bean Quantity (Manual update as no triggers guaranteed)
        bean.remain_amount += quantity
        
        db.add(log)
    
    db.commit()
    return {"status": "success", "document_id": new_doc.id}
