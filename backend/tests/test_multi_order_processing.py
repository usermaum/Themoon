"""
다중 주문 처리 로직 테스트

Mock OCR 데이터를 사용하여 주문별 그룹화 로직을 검증합니다.
"""
import json
from pathlib import Path

from app.services.ocr_service import OCRService


def test_post_process_ocr_result():
    """
    _post_process_ocr_result() 함수 테스트
    """
    # Mock OCR 응답 로드
    mock_file = Path(__file__).parent / "mock_multi_order_ocr_response.json"
    with open(mock_file, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    # OCRService 인스턴스 생성
    ocr_service = OCRService()

    # 후처리 실행
    result = ocr_service._post_process_ocr_result(mock_data.copy())

    # 검증
    print("=" * 80)
    print("🧪 다중 주문 처리 테스트 결과")
    print("=" * 80)

    assert result["has_multiple_orders"] is True, "has_multiple_orders should be True"
    print("✅ has_multiple_orders:", result["has_multiple_orders"])

    assert result["total_order_count"] == 3, "total_order_count should be 3"
    print("✅ total_order_count:", result["total_order_count"])

    assert len(result["order_groups"]) == 3, "order_groups should have 3 groups"
    print("✅ order_groups 개수:", len(result["order_groups"]))

    print("\n📦 주문 그룹 상세:")
    print("-" * 80)

    for idx, group in enumerate(result["order_groups"], 1):
        print(f"\n[주문 #{idx}]")
        print(f"  주문번호: {group['order_number']}")
        print(f"  주문날짜: {group['order_date']}")
        print(f"  품목 수: {len(group['items'])}")
        print(f"  소계: {group['subtotal']:,}원")

        assert group["order_date"] is not None, f"Order #{idx} should have order_date"
        assert len(group["items"]) > 0, f"Order #{idx} should have items"
        assert group["subtotal"] > 0, f"Order #{idx} should have subtotal"

        for item in group["items"]:
            print(f"    - {item['bean_name']} ({item['quantity']}{item['unit']})")
            assert (
                item["order_number"] == group["order_number"]
            ), "Item order_number should match group order_number"

    print("\n" + "=" * 80)
    print("✅ 모든 테스트 통과!")
    print("=" * 80)

    # 결과 샘플 JSON 저장
    output_file = Path(__file__).parent / "test_output_multi_order.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n📄 결과 저장: {output_file}")


if __name__ == "__main__":
    test_post_process_ocr_result()
