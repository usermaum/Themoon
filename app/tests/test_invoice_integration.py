"""
거래 명세서 이미지 입고 통합 테스트

전체 워크플로우 E2E 테스트:
1. 이미지 업로드 → OCR 분석 → 파싱 → 입고 → DB 검증
"""

import pytest
import sys
import os
from datetime import date
from PIL import Image
import io

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from models.database import Bean, Inventory, Transaction
from models.invoice import Invoice, InvoiceItem, InvoiceLearning
from services.ocr_service import OCRService
from services.invoice_service import InvoiceService
from services.learning_service import LearningService


@pytest.fixture
def db():
    """테스트용 DB 세션"""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def setup_test_bean(db):
    """테스트용 원두 생성"""
    # 기존 원두 조회 (No. 1~13 중 하나 사용)
    bean = db.query(Bean).filter(Bean.no == 1).first()

    if not bean:
        # 새 원두 생성 (테스트용)
        max_no = db.query(Bean).count()
        bean = Bean(
            no=max_no + 1,
            name="테스트 원두",
            roast_level="MEDIUM",
            status="active",
            price_per_kg=20000.0
        )
        db.add(bean)
        db.commit()
        db.refresh(bean)

    yield bean


@pytest.fixture
def create_test_image():
    """테스트용 더미 이미지 생성"""
    # 100x100 흰색 이미지 생성
    img = Image.new('RGB', (100, 100), color='white')

    # BytesIO로 변환 (UploadedFile 시뮬레이션)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img


class TestInvoiceIntegration:
    """거래 명세서 이미지 입고 통합 테스트"""

    def test_service_initialization(self, db):
        """서비스 초기화 테스트"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        assert learning_service is not None
        assert ocr_service is not None
        assert invoice_service is not None
        assert ocr_service.learning_service is learning_service
        assert invoice_service.learning_service is learning_service

    def test_ocr_parsing(self, db):
        """OCR 파싱 테스트 (기본 텍스트)"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)

        # 테스트 텍스트
        test_text = """
        거래 명세서
        공급자: GSC
        날짜: 2025-11-13
        원두명: 예가체프 G1
        수량: 10kg
        단가: 20,000원
        """

        # 파싱 테스트
        result = ocr_service.parse_invoice_data(test_text)

        assert result is not None
        assert 'invoice_type' in result

    def test_invoice_save_and_confirm(self, db, setup_test_bean, create_test_image):
        """Invoice 저장 및 입고 확정 테스트"""
        learning_service = LearningService(db)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # Invoice 데이터 준비
        invoice_data = {
            'supplier': 'TEST_SUPPLIER',
            'invoice_date': date.today(),
            'total_amount': 200000.0
        }

        items = [
            {
                'bean_name': setup_test_bean.name,
                'quantity': 10.0,
                'unit_price': 20000.0,
                'amount': 200000.0,
                'notes': 'G1',
                'bean_id': setup_test_bean.id
            }
        ]

        # Invoice 저장
        invoice = invoice_service.save_invoice(
            invoice_data=invoice_data,
            items=items,
            image=create_test_image,
            ocr_text="TEST OCR TEXT",
            confidence=85.0
        )

        assert invoice is not None
        assert invoice.id is not None
        assert invoice.status == "PENDING"
        assert len(invoice.items) == 1
        assert invoice.items[0].bean_id == setup_test_bean.id

        # 입고 확정
        invoice_service.confirm_invoice(invoice.id)

        # 확정 후 검증
        db.refresh(invoice)
        assert invoice.status == "COMPLETED"

        # Inventory 업데이트 확인
        inventory = db.query(Inventory).filter(
            Inventory.bean_id == setup_test_bean.id,
            Inventory.inventory_type == "RAW_BEAN"
        ).first()

        assert inventory is not None
        assert inventory.quantity_kg >= 10.0

        # Transaction 생성 확인
        transaction = db.query(Transaction).filter(
            Transaction.bean_id == setup_test_bean.id,
            Transaction.invoice_item_id == invoice.items[0].id
        ).first()

        assert transaction is not None
        assert transaction.quantity_kg == 10.0
        assert transaction.price_per_unit == 20000.0
        assert transaction.transaction_type == "PURCHASE"

    def test_learning_workflow(self, db, setup_test_bean, create_test_image):
        """학습 기능 워크플로우 테스트"""
        learning_service = LearningService(db)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # Invoice 저장
        invoice_data = {
            'supplier': 'TEST_SUPPLIER',
            'invoice_date': date.today(),
            'total_amount': 200000.0
        }

        items = [
            {
                'bean_name': setup_test_bean.name,
                'quantity': 10.0,
                'unit_price': 20000.0,
                'amount': 200000.0,
                'bean_id': setup_test_bean.id
            }
        ]

        invoice = invoice_service.save_invoice(
            invoice_data=invoice_data,
            items=items,
            image=create_test_image,
            ocr_text="TEST",
            confidence=80.0
        )

        # 사용자 수정 내역 저장
        corrections = [
            {
                'invoice_item_id': invoice.items[0].id,
                'field_name': 'bean_name',
                'ocr_value': '테스트원두',
                'corrected_value': setup_test_bean.name
            },
            {
                'invoice_item_id': invoice.items[0].id,
                'field_name': 'quantity',
                'ocr_value': '9.5',
                'corrected_value': '10.0'
            }
        ]

        saved_count = invoice_service.save_user_corrections(corrections)

        assert saved_count == 2

        # 학습 데이터 조회
        learning_data = learning_service.get_learning_data()
        assert len(learning_data) >= 2

        # 학습 통계 조회
        stats = learning_service.get_correction_stats()
        assert stats['total_corrections'] >= 2
        assert 'bean_name' in stats['by_field']
        assert 'quantity' in stats['by_field']

    def test_invoice_history(self, db):
        """Invoice 처리 내역 조회 테스트"""
        learning_service = LearningService(db)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # 전체 내역 조회
        invoices = invoice_service.get_invoice_history(limit=10)
        assert invoices is not None

        # PENDING 상태 필터링
        pending_invoices = invoice_service.get_invoice_history(
            limit=10,
            status="PENDING"
        )
        assert pending_invoices is not None
        for invoice in pending_invoices:
            assert invoice.status == "PENDING"

    def test_parse_invoice_data_with_learning(self, db):
        """학습 데이터 기반 파싱 테스트"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)

        test_text = """
        거래 명세서
        원두명: 예가체프
        수량: 10kg
        """

        # 학습 데이터 없이 파싱
        result = ocr_service.parse_invoice_data_with_learning(test_text)
        assert result is not None
        assert 'invoice_type' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
