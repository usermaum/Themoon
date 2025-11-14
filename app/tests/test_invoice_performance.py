"""
거래 명세서 이미지 입고 성능 테스트

이미지 크기별 처리 시간 측정
"""

import pytest
import time
from PIL import Image, ImageDraw, ImageFont
import io
import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.ocr_service import OCRService
from services.invoice_service import InvoiceService
from services.learning_service import LearningService


@pytest.fixture
def db():
    """테스트용 DB 세션"""
    session = SessionLocal()
    yield session
    session.close()


def create_test_image_with_text(width, height, text="TEST INVOICE"):
    """
    텍스트가 포함된 테스트 이미지 생성

    Args:
        width: 이미지 너비
        height: 이미지 높이
        text: 이미지에 추가할 텍스트

    Returns:
        PIL.Image
    """
    # 흰색 배경 이미지
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # 텍스트 추가 (간단한 텍스트, 폰트 없이)
    draw.text((50, 50), text, fill='black')
    draw.text((50, 100), "공급업체: GSC GREEN COFFEE", fill='black')
    draw.text((50, 150), "날짜: 2025-11-14", fill='black')
    draw.text((50, 200), "원두명: 에티오피아 예가체프 G1", fill='black')
    draw.text((50, 250), "수량: 10kg", fill='black')
    draw.text((50, 300), "단가: 20,000원", fill='black')

    return img


class TestInvoicePerformance:
    """성능 테스트"""

    def test_image_processing_performance_small(self, db):
        """소형 이미지 처리 성능 (800x600)"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # 소형 이미지 생성 (800x600)
        img = create_test_image_with_text(800, 600)

        start_time = time.time()
        result = invoice_service.process_invoice_image(img, ocr_service)
        end_time = time.time()

        processing_time = end_time - start_time

        print(f"\n소형 이미지 (800x600) 처리 시간: {processing_time:.2f}초")
        assert result is not None
        assert processing_time < 10.0  # 10초 이내

    def test_image_processing_performance_medium(self, db):
        """중형 이미지 처리 성능 (1600x1200)"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # 중형 이미지 생성 (1600x1200)
        img = create_test_image_with_text(1600, 1200)

        start_time = time.time()
        result = invoice_service.process_invoice_image(img, ocr_service)
        end_time = time.time()

        processing_time = end_time - start_time

        print(f"\n중형 이미지 (1600x1200) 처리 시간: {processing_time:.2f}초")
        assert result is not None
        assert processing_time < 15.0  # 15초 이내

    def test_image_processing_performance_large(self, db):
        """대형 이미지 처리 성능 (3200x2400)"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)
        invoice_service = InvoiceService(db, learning_service=learning_service)

        # 대형 이미지 생성 (3200x2400)
        img = create_test_image_with_text(3200, 2400)

        start_time = time.time()
        result = invoice_service.process_invoice_image(img, ocr_service)
        end_time = time.time()

        processing_time = end_time - start_time

        print(f"\n대형 이미지 (3200x2400) 처리 시간: {processing_time:.2f}초")
        assert result is not None
        assert processing_time < 30.0  # 30초 이내

    def test_ocr_extraction_performance(self, db):
        """OCR 텍스트 추출 성능"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)

        # 테스트 이미지 생성
        img = create_test_image_with_text(1600, 1200)

        # 이미지를 numpy array로 변환
        import numpy as np
        img_array = np.array(img)

        start_time = time.time()
        text = ocr_service.extract_text_from_image(img_array)
        end_time = time.time()

        processing_time = end_time - start_time

        print(f"\nOCR 텍스트 추출 시간: {processing_time:.2f}초")
        print(f"추출된 텍스트 길이: {len(text)} 문자")

        assert text is not None
        assert processing_time < 10.0  # 10초 이내

    def test_parsing_performance(self, db):
        """텍스트 파싱 성능"""
        learning_service = LearningService(db)
        ocr_service = OCRService(db, learning_service=learning_service)

        # 테스트 텍스트 (GSC 명세서 시뮬레이션)
        test_text = """
        GSC GREEN COFFEE
        거래 명세서

        공급업체: GSC GREEN COFFEE
        계약번호: GSC-2025-001
        날짜: 2025-11-14

        No. 품명 규격 수량 단가 공급가액
        1 에티오피아 예가체프 G1 10kg 20,000 200,000
        2 콜롬비아 수프리모 AA 15kg 18,000 270,000
        3 브라질 산토스 No.2 20kg 15,000 300,000

        합계: 770,000원
        """

        start_time = time.time()
        result = ocr_service.parse_invoice_data(test_text)
        end_time = time.time()

        processing_time = end_time - start_time

        print(f"\n텍스트 파싱 시간: {processing_time:.2f}초")
        print(f"파싱 결과: {result.get('invoice_type', 'UNKNOWN')}")

        assert result is not None
        assert processing_time < 1.0  # 1초 이내


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
