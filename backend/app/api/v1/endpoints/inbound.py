from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ocr_service import ocr_service
from app.schemas.inbound import InboundResponse, InboundConfirmRequest
from app.models.inbound_document import InboundDocument, InboundStatus
from app.models.inventory_log import InventoryLog, TransactionType
from app.models.bean import Bean
import shutil
import os
import uuid
from datetime import datetime
from app.utils.matching import find_best_match

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=InboundResponse)
async def upload_inbound_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    영수증/견적서 이미지를 업로드하고 OCR로 데이터를 추출합니다.
    """
    # 1. 파일 저장
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    # 2. OCR 수행
    try:
        ocr_data = await ocr_service.extract_receipt_data(content, mime_type=file.content_type)
    except Exception as e:
        # OCR 실패 시에도 파일은 저장하고 빈 데이터 리턴 (또는 에러 처리)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

    # 3. Fuzzy Matching
    all_beans = db.query(Bean).all()
    bean_map = {b.name: b.id for b in all_beans}
    bean_names = list(bean_map.keys())

    if "items" in ocr_data:
        for item in ocr_data["items"]:
            name = item.get("name")
            if name:
                match, score = find_best_match(name, bean_names)
                if match:
                    item["matched_bean_id"] = bean_map[match]
                    item["matched_bean_name"] = match
                    item["match_score"] = score

    # 4. 응답 생성
    return InboundResponse(
        supplier_name=ocr_data.get("supplier_name"),
        invoice_number=ocr_data.get("invoice_number"),
        date=ocr_data.get("date"),
        total_amount=ocr_data.get("total_amount"),
        items=ocr_data.get("items", []),
        temp_file_path=file_path
    )

@router.post("/confirm")
async def confirm_inbound(request: InboundConfirmRequest, db: Session = Depends(get_db)):
    """
    입고 내역을 확정하고 재고에 반영합니다.
    """
    # 1. 중복 확인 (같은 공급처, 같은 명세서 번호)
    if request.invoice_number and request.supplier_name:
        existing_doc = db.query(InboundDocument).filter(
            InboundDocument.invoice_number == request.invoice_number,
            InboundDocument.supplier_name == request.supplier_name,
            InboundDocument.status == InboundStatus.CONFIRMED
        ).first()
        
        if existing_doc:
            raise HTTPException(status_code=400, detail=f"이미 등록된 명세서입니다. (번호: {request.invoice_number})")

    # 2. InboundDocument 생성
    inbound_doc = InboundDocument(
        file_path=request.temp_file_path,
        status=InboundStatus.CONFIRMED,
        invoice_number=request.invoice_number,
        supplier_name=request.supplier_name,
        raw_ocr_data=request.model_dump(mode='json') # 요청 데이터 전체를 저장
    )
    db.add(inbound_doc)
    db.flush() # ID 생성을 위해 flush

    # 2. 각 항목별 재고 처리
    for item in request.items:
        if not item.matched_bean_id:
            continue # 매칭되지 않은 항목은 스킵 (또는 에러 처리)
            
        bean = db.query(Bean).filter(Bean.id == item.matched_bean_id).first()
        if not bean:
            continue
            
        # 평균 단가 갱신 (가중 평균)
        # 기존 재고 가치 + 신규 입고 가치 / 총 재고량 (bean.quantity_kg는 이미 증가된 상태)
        current_value = (bean.quantity_kg - item.quantity) * (bean.cost_price or 0.0)
        new_value = item.quantity * (item.unit_price or 0.0)
        
        if bean.quantity_kg > 0:
            bean.cost_price = (current_value + new_value) / bean.quantity_kg
        
        # InventoryLog 생성
        log = InventoryLog(
            bean_id=bean.id,
            transaction_type=TransactionType.INBOUND,
            quantity_change=item.quantity,
            current_quantity=bean.quantity_kg,
            reason=f"Inbound from {request.supplier_name or 'Unknown'}"
        )
        # Note: Cost price is updated on Bean, separate log for cost history not in current model schema except via Bean updates? 
        # Plan says Transaction has cost_price. I will check model update next. 
        # For now, align with current model.
        db.add(log)
    
    db.commit()
    return {"message": "Inbound confirmed successfully", "document_id": inbound_doc.id}
