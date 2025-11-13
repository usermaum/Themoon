"""
Invoice 서비스

거래 명세서 이미지 처리 및 입고 확정 관리
"""

from typing import Dict, List, Optional
from datetime import datetime, date
import os
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import desc
import sys

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.invoice import Invoice, InvoiceItem
from models.database import Bean, Inventory, Transaction
from utils.image_utils import convert_uploaded_file_to_image, save_image

# Invoice 상태 (문자열로 직접 정의)
class InvoiceStatus:
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class InvoiceService:
    """
    Invoice 서비스

    거래 명세서 이미지 처리, 저장, 입고 확정을 관리합니다.
    """

    def __init__(self, db: Session):
        """
        Args:
            db: SQLAlchemy Session
        """
        self.db = db

    def process_invoice_image(
        self,
        uploaded_file,
        ocr_service: 'OCRService'
    ) -> Dict:
        """
        거래 명세서 이미지 전체 처리 파이프라인

        1. 이미지 변환 (UploadedFile → PIL Image)
        2. OCR 수행
        3. 데이터 파싱
        4. 원두 매칭
        5. 결과 반환

        Args:
            uploaded_file: Streamlit UploadedFile 객체
            ocr_service: OCRService 인스턴스

        Returns:
            {
                'image': PIL.Image,
                'ocr_text': str,
                'invoice_type': str,
                'invoice_data': Dict,
                'items': List[Dict],
                'confidence': float,
                'warnings': List[str],
                'matched_beans': Dict[str, Tuple[Bean, float]]
            }
        """
        # 1. 이미지 변환
        image = convert_uploaded_file_to_image(uploaded_file)

        # 2. OCR 처리
        ocr_result = ocr_service.process_image(image, preprocess=True)

        parsed_data = ocr_result['parsed_data']
        invoice_type = parsed_data.get('invoice_type', 'UNKNOWN')

        # 3. 원두 매칭 (items 또는 단일 원두)
        matched_beans = {}

        if invoice_type == 'GSC':
            # GSC: 다중 원두 매칭
            for item in parsed_data.get('items', []):
                bean_name = item.get('bean_name', '')
                if bean_name and bean_name not in matched_beans:
                    matched_bean, score = ocr_service.match_bean_to_db(bean_name)
                    matched_beans[bean_name] = (matched_bean, score)

        else:
            # 기본 타입: 단일 원두 매칭
            bean_name = parsed_data.get('bean_name', '')
            if bean_name:
                matched_bean, score = ocr_service.match_bean_to_db(bean_name)
                matched_beans[bean_name] = (matched_bean, score)

        # 4. 결과 반환
        return {
            'image': image,
            'ocr_text': ocr_result['ocr_text'],
            'invoice_type': invoice_type,
            'invoice_data': parsed_data,
            'items': parsed_data.get('items', []),
            'confidence': ocr_result['confidence'],
            'warnings': ocr_result['warnings'],
            'matched_beans': matched_beans,
            'timestamp': ocr_result['timestamp']
        }

    def save_invoice(
        self,
        invoice_data: Dict,
        items: List[Dict],
        image: Image.Image,
        ocr_text: str,
        confidence: float
    ) -> Invoice:
        """
        Invoice 및 InvoiceItem 저장

        Args:
            invoice_data: 거래 명세서 메타데이터
            items: 명세서 항목 리스트
            image: PIL Image 객체
            ocr_text: OCR 원본 텍스트
            confidence: 신뢰도 점수

        Returns:
            저장된 Invoice 객체
        """
        # 1. 이미지 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"invoice_{timestamp}.png"
        image_path = os.path.join('data', 'invoices', image_filename)

        save_image(image, image_path)

        # 2. Invoice 생성
        invoice = Invoice(
            image_path=image_path,
            supplier=invoice_data.get('supplier', 'UNKNOWN'),
            invoice_date=invoice_data.get('invoice_date', date.today()),
            total_amount=invoice_data.get('total_amount', 0.0),
            status=InvoiceStatus.PENDING,
            confidence_score=confidence,
            ocr_raw_text=ocr_text,
            invoice_type=invoice_data.get('invoice_type', 'UNKNOWN'),
            contract_number=invoice_data.get('contract_number'),
            total_weight=invoice_data.get('total_weight')
        )

        self.db.add(invoice)
        self.db.flush()  # invoice.id 생성

        # 3. InvoiceItem 생성
        for item in items:
            # 원두 매칭 (bean_id 설정)
            bean_id = None
            bean_name_raw = item.get('bean_name', '')

            # Bean 조회 시도 (정확한 이름 또는 유사도 매칭)
            if bean_name_raw:
                # 먼저 정확한 이름으로 조회
                bean = self.db.query(Bean).filter(
                    Bean.name == bean_name_raw,
                    Bean.is_active == True
                ).first()

                if bean:
                    bean_id = bean.id

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                bean_id=bean_id,
                bean_name_raw=bean_name_raw,
                quantity=item.get('quantity', 0),
                unit_price=item.get('unit_price', 0.0),
                amount=item.get('amount', 0.0),
                weight=item.get('weight', 0.0),
                spec=item.get('spec'),
                origin=item.get('origin'),
                notes=item.get('notes'),
                confidence_score=item.get('confidence_score', confidence)
            )

            self.db.add(invoice_item)

        self.db.commit()
        self.db.refresh(invoice)

        return invoice

    def confirm_invoice(self, invoice_id: int) -> None:
        """
        입고 확정

        1. Invoice 상태를 COMPLETED로 변경
        2. InvoiceItem 별로 Inventory 및 Transaction 생성

        Args:
            invoice_id: Invoice ID

        Raises:
            ValueError: Invoice를 찾을 수 없거나 이미 처리됨
        """
        # 1. Invoice 조회
        invoice = self.db.query(Invoice).filter(
            Invoice.id == invoice_id
        ).first()

        if not invoice:
            raise ValueError(f"Invoice를 찾을 수 없습니다: {invoice_id}")

        if invoice.status == InvoiceStatus.COMPLETED:
            raise ValueError(f"이미 입고 확정된 Invoice입니다: {invoice_id}")

        # 2. InvoiceItem 처리
        for item in invoice.items:
            if not item.bean_id:
                # bean_id가 없으면 입고 불가 (수동 매칭 필요)
                continue

            # 2-1. Inventory 생성 (원두 입고)
            inventory = Inventory(
                bean_id=item.bean_id,
                inventory_type="RAW_BEAN",  # 문자열로 직접 사용
                quantity=item.weight,  # kg 단위
                cost_per_kg=item.unit_price,
                notes=f"거래 명세서 입고 (Invoice #{invoice_id})",
                created_at=invoice.invoice_date or datetime.now()
            )

            self.db.add(inventory)
            self.db.flush()  # inventory.id 생성

            # 2-2. Transaction 생성 (입고 거래)
            transaction = Transaction(
                bean_id=item.bean_id,
                transaction_type="PURCHASE",  # 문자열로 직접 사용
                quantity=item.weight,
                unit_price=item.unit_price,
                total_amount=item.amount,
                transaction_date=invoice.invoice_date or datetime.now(),
                supplier=invoice.supplier,
                notes=f"거래 명세서 자동 입고 (Invoice #{invoice_id})",
                invoice_item_id=item.id
            )

            self.db.add(transaction)

        # 3. Invoice 상태 변경
        invoice.status = InvoiceStatus.COMPLETED
        invoice.confirmed_at = datetime.now()

        self.db.commit()

    def update_invoice_status(
        self,
        invoice_id: int,
        status: str
    ) -> Invoice:
        """
        Invoice 상태 변경

        Args:
            invoice_id: Invoice ID
            status: 새로운 상태

        Returns:
            업데이트된 Invoice 객체

        Raises:
            ValueError: Invoice를 찾을 수 없음
        """
        invoice = self.db.query(Invoice).filter(
            Invoice.id == invoice_id
        ).first()

        if not invoice:
            raise ValueError(f"Invoice를 찾을 수 없습니다: {invoice_id}")

        invoice.status = status

        if status == InvoiceStatus.COMPLETED:
            invoice.confirmed_at = datetime.now()
        elif status == InvoiceStatus.FAILED:
            invoice.confirmed_at = None

        self.db.commit()
        self.db.refresh(invoice)

        return invoice

    def get_invoice_history(
        self,
        limit: int = 20,
        status: Optional[str] = None
    ) -> List[Invoice]:
        """
        최근 처리 내역 조회

        Args:
            limit: 조회 개수 (기본값: 20)
            status: 상태 필터 (None이면 전체)

        Returns:
            Invoice 리스트 (최신순)
        """
        query = self.db.query(Invoice)

        if status:
            query = query.filter(Invoice.status == status)

        invoices = query.order_by(
            desc(Invoice.created_at)
        ).limit(limit).all()

        return invoices

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Invoice 상세 조회

        Args:
            invoice_id: Invoice ID

        Returns:
            Invoice 객체 (없으면 None)
        """
        return self.db.query(Invoice).filter(
            Invoice.id == invoice_id
        ).first()

    def delete_invoice(self, invoice_id: int) -> None:
        """
        Invoice 삭제 (PENDING 상태만 가능)

        Args:
            invoice_id: Invoice ID

        Raises:
            ValueError: Invoice를 찾을 수 없거나 삭제 불가 상태
        """
        invoice = self.get_invoice_by_id(invoice_id)

        if not invoice:
            raise ValueError(f"Invoice를 찾을 수 없습니다: {invoice_id}")

        if invoice.status != InvoiceStatus.PENDING:
            raise ValueError(f"PENDING 상태의 Invoice만 삭제 가능합니다")

        # 이미지 파일 삭제 (옵션)
        if invoice.image_path and os.path.exists(invoice.image_path):
            try:
                os.remove(invoice.image_path)
            except Exception:
                pass  # 파일 삭제 실패해도 DB는 삭제

        # Invoice 삭제 (cascade로 InvoiceItem도 자동 삭제)
        self.db.delete(invoice)
        self.db.commit()
