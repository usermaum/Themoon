"""
Invoice 서비스

거래 명세서 이미지 처리 및 입고 확정 관리
"""

from typing import Dict, List, Optional, TYPE_CHECKING
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

# Type hints only (순환 참조 방지)
if TYPE_CHECKING:
    from services.learning_service import LearningService

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

    def __init__(self, db: Session, learning_service: Optional['LearningService'] = None):
        """
        Args:
            db: SQLAlchemy Session
            learning_service: LearningService 인스턴스 (학습 기능 사용 시)
        """
        self.db = db
        self.learning_service = learning_service

    def process_invoice_image(
        self,
        uploaded_file,
        claude_ocr_service
    ) -> Dict:
        """
        거래 명세서 이미지 전체 처리 파이프라인 (Claude API 사용)

        1. 이미지 변환 (UploadedFile → PIL Image)
        2. Claude API로 OCR + 파싱
        3. 원두 매칭
        4. 결과 반환

        Args:
            uploaded_file: Streamlit UploadedFile 객체
            claude_ocr_service: ClaudeOCRService 인스턴스

        Returns:
            {
                'image': PIL.Image,
                'ocr_text': str,
                'invoice_type': str,
                'invoice_data': Dict,
                'items': List[Dict],
                'confidence': float,
                'warnings': List[str],
                'matched_beans': Dict[str, Tuple[Bean, float]],
                'timestamp': str
            }
        """
        # 1. 이미지 변환
        image = convert_uploaded_file_to_image(uploaded_file)

        # 2. Claude API로 OCR + 파싱
        claude_result = claude_ocr_service.process_invoice(image)

        invoice_type = claude_result.get('invoice_type', 'UNKNOWN')
        invoice_data = claude_result.get('invoice_data', {})
        items = claude_result.get('items', [])

        # 3. 원두 매칭
        matched_beans = {}

        if invoice_type == 'GSC':
            # GSC: 다중 원두 매칭
            for item in items:
                bean_name = item.get('bean_name', '')
                if bean_name and bean_name not in matched_beans:
                    # DB에서 유사한 원두 찾기
                    matched_bean, score = self._match_bean_to_db(bean_name)
                    matched_beans[bean_name] = (matched_bean, score)

        else:
            # 기본 타입: 단일 원두 매칭
            bean_name = invoice_data.get('bean_name', '')
            if bean_name:
                matched_bean, score = self._match_bean_to_db(bean_name)
                matched_beans[bean_name] = (matched_bean, score)

        # 4. 결과 반환
        return {
            'image': image,
            'ocr_text': claude_result.get('ocr_text', ''),
            'invoice_type': invoice_type,
            'invoice_data': invoice_data,
            'items': items,
            'confidence': claude_result.get('confidence', 95.0),
            'warnings': claude_result.get('warnings', []),
            'matched_beans': matched_beans,
            'timestamp': claude_result.get('timestamp', '')
        }

    def _match_bean_to_db(self, bean_name: str):
        """
        원두명을 DB에서 매칭 (유사도 기반)

        Args:
            bean_name: 추출된 원두명

        Returns:
            (matched_bean, score) tuple
        """
        from difflib import SequenceMatcher

        all_beans = self.db.query(Bean).filter(Bean.status == 'active').all()

        if not all_beans:
            return (None, 0.0)

        # 유사도 계산
        best_match = None
        best_score = 0.0

        for bean in all_beans:
            score = SequenceMatcher(None, bean_name.lower(), bean.name.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = bean

        # 70% 이상 유사하면 매칭으로 간주
        if best_score >= 0.7:
            return (best_match, best_score)
        else:
            return (None, 0.0)

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
            ocr_raw_text=ocr_text
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
                    Bean.status == 'active'
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

            # 2-1. Inventory 조회 또는 생성
            inventory = self.db.query(Inventory).filter(
                Inventory.bean_id == item.bean_id,
                Inventory.inventory_type == "RAW_BEAN"
            ).first()

            if not inventory:
                # 재고 없으면 새로 생성
                inventory = Inventory(
                    bean_id=item.bean_id,
                    inventory_type="RAW_BEAN",
                    quantity_kg=0.0
                )
                self.db.add(inventory)
                self.db.flush()

            # 재고 수량 증가
            inventory.quantity_kg += item.quantity

            # 2-2. Transaction 생성 (입고 거래)
            notes_text = f"거래 명세서 자동 입고 (Invoice #{invoice_id})"
            if invoice.supplier:
                notes_text += f" - {invoice.supplier}"

            transaction = Transaction(
                bean_id=item.bean_id,
                transaction_type="PURCHASE",
                inventory_type="RAW_BEAN",
                quantity_kg=item.quantity,
                price_per_unit=item.unit_price,
                total_amount=item.amount,
                notes=notes_text,
                invoice_item_id=item.id
            )

            self.db.add(transaction)

        # 3. Invoice 상태 변경
        invoice.status = InvoiceStatus.COMPLETED

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

    def save_user_corrections(
        self,
        corrections: List[Dict]
    ) -> int:
        """
        사용자 수정 내역 일괄 저장

        UI에서 사용자가 OCR 결과를 수정한 경우,
        그 수정 내역을 InvoiceLearning 테이블에 저장합니다.

        Args:
            corrections: 수정 내역 리스트
                [
                    {
                        'invoice_item_id': int,
                        'field_name': str,
                        'ocr_value': str,
                        'corrected_value': str
                    },
                    ...
                ]

        Returns:
            저장된 수정 내역 개수

        Raises:
            ValueError: learning_service가 없는 경우
        """
        if not self.learning_service:
            raise ValueError("LearningService가 설정되지 않았습니다")

        if not corrections:
            return 0

        # 학습 서비스를 통해 일괄 저장
        saved_items = self.learning_service.batch_save_corrections(corrections)

        return len(saved_items)
