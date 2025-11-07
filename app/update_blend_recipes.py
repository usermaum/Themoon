#!/usr/bin/env python3
"""
블렌드 레시피 업데이트 스크립트

마스터플랜 v2 - Phase 1, Task T1-3
마스터플랜에 정의된 블렌드 레시피로 업데이트
"""

import sys
from sqlalchemy.orm import Session
from models.database import SessionLocal, Blend, BlendRecipe, Bean


# 마스터플랜 v2 - 블렌드 레시피
MASTER_BLEND_RECIPES = {
    '풀문 블렌드': {
        'blend_type': '풀문',
        'suggested_price': 22000.0,
        'description': '마사이 40% + 안티구아 40% + 모모라 10% + g4 10%',
        'recipes': [
            {'bean_name': '마사이', 'portion_count': 4, 'ratio': 40.0},
            {'bean_name': '안티구아', 'portion_count': 4, 'ratio': 40.0},
            {'bean_name': '모모라', 'portion_count': 1, 'ratio': 10.0},
            {'bean_name': 'g4', 'portion_count': 1, 'ratio': 10.0}
        ]
    },
    '뉴문 블렌딩': {
        'blend_type': '뉴문',
        'suggested_price': 4000.0,
        'description': '브라질 60% + 콜롬비아 30% + g4 10%',
        'recipes': [
            {'bean_name': '브라질', 'portion_count': 6, 'ratio': 60.0},
            {'bean_name': '콜롬비아', 'portion_count': 3, 'ratio': 30.0},
            {'bean_name': 'g4', 'portion_count': 1, 'ratio': 10.0}
        ]
    }
}


def update_blend_recipe(db: Session, blend_name: str, recipe_data: dict):
    """
    블렌드 레시피 업데이트
    """
    print(f"\n🔧 업데이트 중: {blend_name}")
    print("=" * 80)

    # 블렌드 조회
    blend = db.query(Blend).filter(Blend.name == blend_name).first()

    if not blend:
        print(f"  ⚠️  블렌드 '{blend_name}' 찾을 수 없음")
        return False

    print(f"  블렌드 ID: {blend.id}")
    print(f"  기존 판매가: ₩{blend.suggested_price:,.0f}")
    print(f"  새 판매가: ₩{recipe_data['suggested_price']:,.0f}")

    # 판매가 및 설명 업데이트
    blend.suggested_price = recipe_data['suggested_price']
    blend.description = recipe_data['description']
    blend.total_portion = sum(r['portion_count'] for r in recipe_data['recipes'])

    # 기존 레시피 삭제
    old_recipes = db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()
    print(f"\n  📝 기존 레시피 삭제: {len(old_recipes)}개")
    for old_recipe in old_recipes:
        db.delete(old_recipe)

    # 새 레시피 추가
    print(f"  ✅ 새 레시피 추가:")
    for recipe_info in recipe_data['recipes']:
        bean_name = recipe_info['bean_name']
        bean = db.query(Bean).filter(Bean.name == bean_name).first()

        if not bean:
            print(f"    ⚠️  원두 '{bean_name}' 찾을 수 없음")
            continue

        new_recipe = BlendRecipe(
            blend_id=blend.id,
            bean_id=bean.id,
            portion_count=recipe_info['portion_count'],
            ratio=recipe_info['ratio']
        )
        db.add(new_recipe)

        print(f"    - {bean_name:10s}: {recipe_info['portion_count']}포션 ({recipe_info['ratio']:.0f}%)")

    return True


def verify_blend_recipes(db: Session):
    """
    블렌드 레시피 검증
    """
    print("\n" + "=" * 80)
    print("✅ 블렌드 레시피 검증")
    print("=" * 80)

    all_valid = True

    for blend_name, recipe_data in MASTER_BLEND_RECIPES.items():
        blend = db.query(Blend).filter(Blend.name == blend_name).first()

        if not blend:
            print(f"❌ {blend_name}: 블렌드 존재하지 않음")
            all_valid = False
            continue

        print(f"\n📊 {blend_name} (ID: {blend.id})")
        print(f"   판매가: ₩{blend.suggested_price:,.0f}")
        print(f"   설명: {blend.description}")
        print(f"   레시피:")

        recipes = db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()

        total_ratio = 0
        for recipe in recipes:
            bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
            print(f"     - {bean.name:10s}: {recipe.portion_count}포션 ({recipe.ratio:.0f}%) | ₩{bean.price_per_kg:,.0f}/kg")
            total_ratio += recipe.ratio

        # 비율 합계 검증
        if abs(total_ratio - 100.0) < 0.01:
            print(f"   ✅ 비율 합계: {total_ratio:.0f}%")
        else:
            print(f"   ❌ 비율 합계 오류: {total_ratio:.0f}% (100%이어야 함)")
            all_valid = False

    print("\n" + "=" * 80)
    if all_valid:
        print("🎉 모든 블렌드 레시피가 올바르게 설정되었습니다!")
    else:
        print("⚠️  일부 블렌드에 문제가 있습니다.")
    print("=" * 80)

    return all_valid


def calculate_blend_cost(db: Session):
    """
    블렌드 원가 계산 (마스터플랜 공식 적용)
    """
    print("\n" + "=" * 80)
    print("💰 블렌드 원가 계산 (마스터플랜 공식)")
    print("=" * 80)

    LOSS_RATE = 0.17  # 17% 손실률

    for blend_name in MASTER_BLEND_RECIPES.keys():
        blend = db.query(Blend).filter(Blend.name == blend_name).first()

        if not blend:
            continue

        print(f"\n📊 {blend_name}")

        recipes = db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()

        # 1. 혼합 비중별 원가 계산
        blend_cost_before_loss = 0
        for recipe in recipes:
            bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
            bean_cost = bean.price_per_kg * (recipe.ratio / 100.0)
            blend_cost_before_loss += bean_cost
            print(f"   {bean.name:10s}: ₩{bean.price_per_kg:>6,.0f}/kg × {recipe.ratio:>4.0f}% = ₩{bean_cost:>6,.0f}/kg")

        # 2. 손실률 반영 (최종 원가)
        blend_cost_after_loss = blend_cost_before_loss / (1 - LOSS_RATE)

        print(f"\n   혼합 원가 (손실 전): ₩{blend_cost_before_loss:,.0f}/kg")
        print(f"   최종 원가 (손실 17% 반영): ₩{blend_cost_after_loss:,.0f}/kg")

        # 3. 수익성 계산
        selling_price = blend.suggested_price
        margin = selling_price - blend_cost_after_loss
        margin_rate = (margin / selling_price) * 100 if selling_price > 0 else 0

        print(f"   판매가: ₩{selling_price:,.0f}/kg")
        print(f"   마진: ₩{margin:,.0f}/kg ({margin_rate:.1f}%)")

    print("\n" + "=" * 80)


def main():
    """
    메인 실행
    """
    print("=" * 80)
    print("🚀 블렌드 레시피 업데이트 시작")
    print("=" * 80)
    print("마스터플랜 v2 - Phase 1, Task T1-3")
    print("업데이트 대상: 2개 블렌드 (풀문 블렌드, 뉴문 블렌딩)")
    print("=" * 80)

    db = SessionLocal()

    try:
        # 1. 레시피 업데이트
        for blend_name, recipe_data in MASTER_BLEND_RECIPES.items():
            update_blend_recipe(db, blend_name, recipe_data)

        # 2. 커밋
        db.commit()
        print(f"\n✅ 블렌드 레시피 업데이트 완료")

        # 3. 검증
        verify_blend_recipes(db)

        # 4. 원가 계산
        calculate_blend_cost(db)

        print("\n" + "=" * 80)
        print("🎉 T1-3 작업 완료!")
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
