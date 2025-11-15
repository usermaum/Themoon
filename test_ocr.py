#!/usr/bin/env python3
"""
OCR 종합 테스트 스크립트
- GSC 타입 인식
- 날짜/금액 파싱
- 항목 인식
- 신뢰도 측정
"""

import sys
from PIL import Image
from app.models.database import get_db
from app.services.ocr_service import OCRService
from app.services.learning_service import LearningService

def test_image(image_path: str):
    """이미지 OCR 테스트"""
    print(f"\n{'='*80}")
    print(f"테스트 이미지: {image_path}")
    print(f"{'='*80}\n")

    # DB 세션 및 서비스 초기화
    db = next(get_db())
    learning_service = LearningService(db)
    ocr_service = OCRService(db, learning_service)

    # 이미지 로드
    try:
        image = Image.open(image_path)
        print(f"✅ 이미지 로드 성공: {image.size}")
    except Exception as e:
        print(f"❌ 이미지 로드 실패: {e}")
        return

    # OCR 처리 (전처리 적용)
    print("\n🔍 OCR 처리 중 (전처리 적용)...")
    try:
        result = ocr_service.process_image(image, preprocess=True)

        if result.get('success'):
            print("✅ OCR 처리 성공!\n")

            # 1. 명세서 타입
            print(f"📋 명세서 타입: {result.get('invoice_type', 'Unknown')}")

            # 2. 추출된 데이터
            print(f"\n📅 날짜: {result.get('date', 'None')}")
            print(f"💰 총 금액: {result.get('total_amount', 'None')}")

            # 3. 항목 리스트
            items = result.get('items', [])
            print(f"\n📦 항목 개수: {len(items)}개")
            for i, item in enumerate(items, 1):
                print(f"\n  항목 {i}:")
                print(f"    - 원두명: {item.get('bean_name', 'None')}")
                print(f"    - 수량: {item.get('quantity', 'None')}")
                print(f"    - 단가: {item.get('unit_price', 'None')}")
                print(f"    - 금액: {item.get('amount', 'None')}")

            # 4. 신뢰도 점수
            confidence = result.get('confidence', {})
            print(f"\n📊 신뢰도 점수:")
            print(f"  - 타입: {confidence.get('type', 0):.1f}%")
            print(f"  - 날짜: {confidence.get('date', 0):.1f}%")
            print(f"  - 금액: {confidence.get('amount', 0):.1f}%")
            print(f"  - 항목: {confidence.get('items', 0):.1f}%")
            print(f"  - 전체: {confidence.get('overall', 0):.1f}%")

            # 5. OCR 원본 텍스트 (처음 500자)
            ocr_text = result.get('ocr_text', '')
            print(f"\n📝 OCR 원본 텍스트 (처음 500자):")
            print("-" * 80)
            print(ocr_text[:500])
            if len(ocr_text) > 500:
                print(f"... (총 {len(ocr_text)}자)")
            print("-" * 80)

        else:
            print(f"❌ OCR 처리 실패: {result.get('error', 'Unknown error')}")
            print(f"\n전체 결과:")
            print(result)

    except Exception as e:
        print(f"❌ OCR 처리 중 오류: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    # 테스트할 이미지
    test_images = [
        "images/coffee_bean_receiving_Specification/IMG_1650.PNG",
        "images/coffee_bean_receiving_Specification/IMG_1651.PNG",
    ]

    # 커맨드라인 인자가 있으면 사용
    if len(sys.argv) > 1:
        test_images = sys.argv[1:]

    for img_path in test_images:
        test_image(img_path)
        print("\n")
