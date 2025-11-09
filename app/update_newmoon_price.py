#!/usr/bin/env python3
"""
뉴문 블렌딩 판매가 업데이트

마스터플랜 v2 - Phase 1 후속 작업
뉴문 블렌딩 판매가를 ₩4,000 → ₩15,000으로 조정
"""

import sys
from sqlalchemy.orm import Session
from models.database import SessionLocal, Blend


def update_newmoon_price(db: Session, new_price: float = 15000.0):
    """
    뉴문 블렌딩 판매가 업데이트

    Args:
        db: 데이터베이스 세션
        new_price: 새 판매가 (기본값: 15,000원)
    """
    print("=" * 80)
    print("🔧 뉴문 블렌딩 판매가 업데이트")
    print("=" * 80)

    # 뉴문 블렌드 조회
    blend = db.query(Blend).filter(Blend.name == '뉴문 블렌딩').first()

    if not blend:
        print("❌ 뉴문 블렌딩을 찾을 수 없습니다.")
        return False

    print(f"\n📊 블렌드 정보:")
    print(f"   ID: {blend.id}")
    print(f"   이름: {blend.name}")
    print(f"   타입: {blend.blend_type}")
    print(f"   기존 판매가: ₩{blend.suggested_price:,.0f}")
    print(f"   새 판매가: ₩{new_price:,.0f}")

    # 가격 변경
    old_price = blend.suggested_price
    blend.suggested_price = new_price

    price_change = new_price - old_price
    change_percent = (price_change / old_price * 100) if old_price > 0 else 0

    print(f"\n📈 변경사항:")
    print(f"   가격 변화: ₩{price_change:+,.0f} ({change_percent:+.1f}%)")

    return True


def calculate_margin(db: Session):
    """
    뉴문 블렌딩 마진 계산 (마스터플랜 공식)
    """
    from models.database import BlendRecipe, Bean

    print("\n" + "=" * 80)
    print("💰 뉴문 블렌딩 원가 및 마진 계산")
    print("=" * 80)

    LOSS_RATE = 0.17  # 17% 손실률

    blend = db.query(Blend).filter(Blend.name == '뉴문 블렌딩').first()

    if not blend:
        return

    recipes = db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()

    # 1. 혼합 원가 계산
    blend_cost_before_loss = 0
    print(f"\n📊 원가 구성:")
    for recipe in recipes:
        bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
        component_cost = bean.price_per_kg * (recipe.ratio / 100.0)
        blend_cost_before_loss += component_cost
        print(f"   {bean.name:10s}: ₩{bean.price_per_kg:>6,}/kg × {recipe.ratio:>4.0f}% = ₩{component_cost:>6,.0f}/kg")

    # 2. 손실률 반영
    blend_cost_after_loss = blend_cost_before_loss / (1 - LOSS_RATE)

    print(f"\n📐 원가 계산:")
    print(f"   혼합 원가 (손실 전): ₩{blend_cost_before_loss:,.0f}/kg")
    print(f"   최종 원가 (손실 17% 반영): ₩{blend_cost_after_loss:,.0f}/kg")

    # 3. 마진 계산
    selling_price = blend.suggested_price
    margin = selling_price - blend_cost_after_loss
    margin_rate = (margin / selling_price * 100) if selling_price > 0 else 0

    print(f"\n💵 수익성 분석:")
    print(f"   판매가: ₩{selling_price:,.0f}/kg")
    print(f"   마진: ₩{margin:,.0f}/kg ({margin_rate:.1f}%)")

    if margin > 0:
        print(f"   ✅ 수익 구조 정상")
    else:
        print(f"   ⚠️  손실 발생 중")

    print("=" * 80)


def main():
    """
    메인 실행
    """
    print("=" * 80)
    print("🚀 뉴문 블렌딩 판매가 업데이트 시작")
    print("=" * 80)

    db = SessionLocal()

    try:
        # 1. 판매가 업데이트
        success = update_newmoon_price(db, new_price=15000.0)

        if not success:
            print("\n❌ 업데이트 실패")
            sys.exit(1)

        # 2. 커밋
        db.commit()
        print(f"\n✅ 판매가 업데이트 완료")

        # 3. 마진 계산
        calculate_margin(db)

        print("\n" + "=" * 80)
        print("🎉 작업 완료!")
        print("=" * 80)

    except Exception as e:
        db.rollback()
        print(f"\n❌ 오류 발생: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
