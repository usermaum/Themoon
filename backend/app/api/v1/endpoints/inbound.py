import logging
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inbound_document import InboundDocument
from app.repositories.inbound_repository import InboundRepository
from app.schemas.inbound import (
    InboundConfirmRequest,
    PaginatedInboundResponse,
)
from app.services.image_service import image_service
from app.services.ocr_service import OCRService
from app.services.inbound_service import inbound_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services (ocr_service is used here for streaming analysis)
ocr_service = OCRService()

import asyncio
import json

from fastapi.responses import StreamingResponse


@router.post("/analyze")
async def analyze_inbound_document(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    Analyze an inbound document (invoice) from a file upload or a URL.
    Returns a Server-Sent Events (SSE) stream with status updates.
    """

    # Eagerly read file content to prevent "I/O operation on closed file" error
    # because UploadFile is closed when the request handler exits, but the generator runs later.
    upload_file_bytes = None
    upload_filename = "unknown.jpg"
    upload_content_type = "image/jpeg"

    if file:
        upload_file_bytes = await file.read()
        upload_filename = file.filename
        upload_content_type = file.content_type or "image/jpeg"

    async def analyze_generator():
        image_bytes = None
        filename = "unknown.jpg"
        mime_type = "image/jpeg"

        try:
            # Step 1: Image Fetching
            yield json.dumps({"status": "progress", "message": "이미지를 가져오는 중..."}) + "\n"

            if upload_file_bytes:
                image_bytes = upload_file_bytes
                filename = upload_filename
                mime_type = upload_content_type
            elif url:
                yield json.dumps(
                    {"status": "progress", "message": "외부 URL에서 이미지 다운로드 중..."}
                ) + "\n"
                try:
                    # Google Drive Link Helper
                    import re

                    drive_pattern = r"(?:https?:\/\/)?(?:drive|docs)\.google\.com\/(?:file\/d\/|open\?id=|uc\?id=)([a-zA-Z0-9_-]+)"
                    match = re.search(drive_pattern, url)
                    fetch_url = url
                    if match:
                        file_id = match.group(1)
                        fetch_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                        yield json.dumps(
                            {"status": "progress", "message": "Google Drive 링크 변환 중..."}
                        ) + "\n"

                    async with httpx.AsyncClient() as client:
                        response = await client.get(fetch_url, follow_redirects=True)
                        response.raise_for_status()
                        image_bytes = response.content

                        # Try to extract filename
                        import cgi

                        content_disposition = response.headers.get("content-disposition")
                        if content_disposition:
                            try:
                                _, params = cgi.parse_header(content_disposition)
                                if "filename" in params:
                                    filename = params["filename"]
                                    if not any(
                                        filename.lower().endswith(ext)
                                        for ext in [".jpg", ".jpeg", ".png", ".webp"]
                                    ):
                                        filename += ".jpg"
                                else:
                                    filename = "gdrive_upload.jpg"
                            except:
                                filename = "gdrive_upload.jpg"
                        else:
                            filename = "gdrive_upload.jpg"

                        mime_type = response.headers.get("content-type", "image/jpeg")
                except Exception as e:
                    yield json.dumps(
                        {"status": "error", "message": f"이미지 다운로드 실패: {str(e)}"}
                    ) + "\n"
                    return
            else:
                yield json.dumps(
                    {"status": "error", "message": "파일 또는 URL을 제공해야 합니다."}
                ) + "\n"
                return

            if not image_bytes:
                yield json.dumps(
                    {"status": "error", "message": "이미지 데이터가 비어있습니다."}
                ) + "\n"
                return

            # Step 2: Validation
            yield json.dumps(
                {"status": "progress", "message": "이미지 보안 및 품질 검증 중..."}
            ) + "\n"
            is_valid, error_msg = image_service.validate_image(image_bytes, filename)
            if not is_valid:
                yield json.dumps(
                    {"status": "error", "message": f"유효하지 않은 이미지: {error_msg}"}
                ) + "\n"
                return

            # Step 3: Preprocessing
            yield json.dumps(
                {"status": "progress", "message": "OCR 최적화를 위한 전처리 중..."}
            ) + "\n"
            processed_image_bytes = image_bytes
            try:
                import io

                from PIL import Image

                # Explicit BytesIO to prevent premature GC/Closure
                with io.BytesIO(image_bytes) as buf:
                    with Image.open(buf) as img:
                        img.load()  # Force load data into memory
                        processed_img = image_service.preprocess_for_ocr(img)

                        output = io.BytesIO()
                        if processed_img.mode in ("RGBA", "LA"):
                            processed_img = processed_img.convert("RGB")
                        processed_img.save(output, format="JPEG", quality=95)
                        processed_image_bytes = output.getvalue()
                        mime_type = "image/jpeg"
            except Exception as e:
                logger.warning(f"Preprocessing failed: {e}", exc_info=True)
                # Continue with original

            # Step 4: OCR Analysis (Streaming from Service)
            ocr_result = None
            async for update in ocr_service.analyze_image_stream(processed_image_bytes, mime_type):
                if update["status"] == "complete":
                    ocr_result = update["data"]
                elif update["status"] == "error":
                    yield json.dumps({"status": "error", "message": update["message"]}) + "\n"
                    return
                else:
                    # Progress update from OCR Service
                    yield json.dumps(update) + "\n"

            if not ocr_result:
                yield json.dumps({"status": "error", "message": "OCR 분석 결과가 없습니다."}) + "\n"
                return

            if ocr_result.get("error") == "INVALID_DOCUMENT":
                yield json.dumps(
                    {"status": "error", "message": "INVALID_DOCUMENT: 명세서 형식이 아닙니다."}
                ) + "\n"
                return

            # Step 5: Save Image (Local Storage)
            yield json.dumps({"status": "progress", "message": "이미지 저장 중..."}) + "\n"
            image_data = None
            try:
                # Run sync S3/Local IO in thread to avoid blocking pipeline
                image_data = await asyncio.to_thread(
                    image_service.process_and_save, image_bytes, filename
                )
                drive_link = f"/static/uploads/inbound/{image_data['paths']['original']}"
            except Exception as e:
                yield json.dumps(
                    {"status": "error", "message": f"이미지 저장 실패: {str(e)}"}
                ) + "\n"
                return

            # Step 6: Post-processing (Bean Matching)
            yield json.dumps(
                {"status": "progress", "message": "생두 데이터베이스 매칭 중..."}
            ) + "\n"

            from app.schemas.inbound import (
                AdditionalInfo,
                AmountsInfo,
                DocumentInfo,
                ReceiverInfo,
                SupplierInfo,
                OCRResponse,
            )

            document_info = (
                DocumentInfo(**ocr_result.get("document_info", {}))
                if "document_info" in ocr_result
                else None
            )
            supplier_info = (
                SupplierInfo(**ocr_result.get("supplier", {})) if "supplier" in ocr_result else None
            )
            receiver_info = (
                ReceiverInfo(**ocr_result.get("receiver", {})) if "receiver" in ocr_result else None
            )
            amounts_info = (
                AmountsInfo(**ocr_result.get("amounts", {})) if "amounts" in ocr_result else None
            )
            additional_info = (
                AdditionalInfo(**ocr_result.get("additional_info", {}))
                if "additional_info" in ocr_result
                else None
            )

            items_with_match_info = []
            for item_data in ocr_result.get("items", []):
                bean_name = item_data.get("bean_name")
                # Use InboundService for matching
                matched_bean, match_field, match_method = inbound_service.match_bean_multi_field(bean_name, db)
                item_data["matched"] = matched_bean is not None
                item_data["match_field"] = match_field
                item_data["match_method"] = match_method
                item_data["bean_id"] = matched_bean.id if matched_bean else None
                items_with_match_info.append(item_data)

            final_response = OCRResponse(
                debug_raw_text=ocr_result.get("debug_raw_text"),
                document_info=document_info,
                supplier=supplier_info,
                receiver=receiver_info,
                amounts=amounts_info,
                items=items_with_match_info,
                additional_info=additional_info,
                has_multiple_orders=ocr_result.get("has_multiple_orders", False),
                total_order_count=ocr_result.get("total_order_count", 0),
                order_groups=ocr_result.get("order_groups", []),
                supplier_name=ocr_result.get("supplier", {}).get("name"),
                contract_number=ocr_result.get("document_info", {}).get("contract_number"),
                supplier_phone=ocr_result.get("supplier", {}).get("phone"),
                supplier_email=ocr_result.get("supplier", {}).get("email"),
                receiver_name=ocr_result.get("receiver", {}).get("name"),
                invoice_date=ocr_result.get("document_info", {}).get("invoice_date"),
                total_amount=ocr_result.get("amounts", {}).get("total_amount"),
                drive_link=drive_link,
                original_image_path=image_data["paths"].get("original") if image_data else None,
                webview_image_path=image_data["paths"].get("webview") if image_data else None,
                thumbnail_image_path=image_data["paths"].get("thumbnail") if image_data else None,
                image_width=image_data.get("width") if image_data else None,
                image_height=image_data.get("height") if image_data else None,
                file_size_bytes=image_data.get("file_size_bytes") if image_data else None,
            )

            # Final Success Yield
            yield json.dumps({"status": "complete", "data": final_response.dict()}) + "\n"

        except Exception as e:
            logger.error(f"Analysis Generator Error: {e}", exc_info=True)
            yield json.dumps({"status": "error", "message": f"서버 내부 오류: {str(e)}"}) + "\n"

    return StreamingResponse(analyze_generator(), media_type="application/x-ndjson")


@router.get("/list", response_model=PaginatedInboundResponse)
def get_inbound_list(
    page: int = 1,
    limit: int = 20,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    명세서 목록 조회 (Pagination & Filtering)
    """
    inbound_repo = InboundRepository(db)
    items, total = inbound_repo.get_list(
        skip=(page - 1) * limit,
        limit=limit,
        from_date=from_date,
        to_date=to_date,
        keyword=keyword
    )
    total_pages = (total + limit - 1) // limit

    return {"items": items, "total": total, "page": page, "size": limit, "total_pages": total_pages}


@router.get("/{document_id}")
def get_inbound_detail(document_id: int, db: Session = Depends(get_db)):
    """
    명세서 상세 정보 조회 (Document + Detail + Receiver + Items)
    """
    inbound_repo = InboundRepository(db)
    doc = inbound_repo.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"document": doc, "detail": doc.detail, "receiver": doc.receiver, "items": doc.items}


@router.get("/check-duplicate/{contract_number}")
def check_duplicate_contract_number(contract_number: str, db: Session = Depends(get_db)):
    """
    Check if a contract number already exists.
    Returns {"exists": true/false}
    """
    inbound_repo = InboundRepository(db)
    existing_doc = inbound_repo.get_document_by_contract_number(contract_number)

    if existing_doc:
        return {"exists": True, "detail": "⚠️ 이미 등록된 명세서(계약번호)입니다."}
    return {"exists": False, "detail": "사용 가능한 번호입니다."}


@router.post("/confirm", status_code=201)
def confirm_inbound(request: InboundConfirmRequest, db: Session = Depends(get_db)):
    """
    Saves the confirmed inbound data.
    Delegates logic to InboundService.
    """
    try:
        result = inbound_service.confirm_inbound(db, request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Inbound Confirm Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
