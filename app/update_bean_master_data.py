#!/usr/bin/env python3
"""
원두 마스터 데이터 업데이트 스크립트

마스터플랜 v2 - Phase 1, Task T1-2
마스터플랜에 정의된 원두 정보로 업데이트
"""

import sys
from sqlalchemy.orm import Session
from models.database import SessionLocal, Bean


# 마스터플랜 v2 - 원두 정보
MASTER_BEAN_DATA = {
    '마사이': {
        'country_name': '에티오피아',
        'country_code': 'Eth',
        'roast_level': 'W',  # White (Light)
        'price_per_kg': 5000.0,  # 에티오피아 평균
        'description': '풀문 블렌드 40% 구성'
    },
    'g4': {
        'country_name': '케냐',
        'country_code': 'K',
        'roast_level': 'W',
        'price_per_kg': 6000.0,  # 케냐 평균
        'description': '풀문 블렌드 10% + 뉴문 블렌드 10% 구성'
    },
    '브라질': {
        'country_name': '브라질',
        'country_code': 'Br',
        'roast_level': 'N',  # Normal
        'price_per_kg': 4700.0,  # 브라질 기준 (파젠다카르모)
        'description': '뉴문 블렌드 60% 구성'
    },
    '콜롬비아': {
        'country_name': '콜롬비아',
        'country_code': 'Co',
        'roast_level': 'W',
        'price_per_kg': 5900.0,  # 콜롬비아 기준 (후일라)
        'description': '뉴문 블렌드 30% 구성'
    }
}


def update_bean_master_data(db: Session):
    """
    원두 마스터 데이터 업데이트
    """
    print("="*80)
    print("🔧 원두 마스터 데이터 업데이트")
    print("="*80)

    updated_count = 0

    for bean_name, data in MASTER_BEAN_DATA.items():
        bean = db.query(Bean).filter(Bean.name == bean_name).first()

        if not bean:
            print(f"⚠️  원두 '{bean_name}' 찾을 수 없음")
            continue

        print(f"\n📝 업데이트 중: {bean_name} (ID: {bean.id}, no: {bean.no})")
        print(f"   변경 전: {bean.country_name or 'Unknown'} | {bean.roast_level} | ₩{bean.price_per_kg:,.0f}/kg")

        # 업데이트
        bean.country_name = data['country_name']
        bean.country_code = data['country_code']
        bean.roast_level = data['roast_level']
        bean.price_per_kg = data['price_per_kg']
        bean.description = data['description']

        print(f"   변경 후: {bean.country_name} | {bean.roast_level} | ₩{bean.price_per_kg:,.0f}/kg")
        print(f"   설명: {bean.description}")

        updated_count += 1

    return updated_count


def verify_master_beans(db: Session):
    """
    마스터플랜에 필요한 6개 원두 검증
    """
    print("\n" + "="*80)
    print("✅ 마스터플랜 필수 원두 검증 (6종)")
    print("="*80)

    required_beans = [
        ('마사이', '에티오피아', '풀문 40%'),
        ('안티구아', '과테말라', '풀문 40%'),
        ('모모라', '에티오피아', '풀문 10%'),
        ('g4', '케냐', '풀문 10% + 뉴문 10%'),
        ('브라질', '브라질', '뉴문 60%'),
        ('콜롬비아', '콜롬비아', '뉴문 30%')
    ]

    all_valid = True

    for bean_name, expected_country, usage in required_beans:
        bean = db.query(Bean).filter(Bean.name == bean_name).first()

        if not bean:
            print(f"❌ {bean_name}: 존재하지 않음")
            all_valid = False
            continue

        country_match = bean.country_name == expected_country
        has_price = bean.price_per_kg > 0

        status = "✅" if (country_match and has_price) else "⚠️"

        print(f"{status} {bean_name:10s} | {bean.country_name:15s} | {bean.roast_level} | ₩{bean.price_per_kg:>7,.0f}/kg | {usage}")

        if not country_match:
            print(f"   ⚠️  국가 불일치: {bean.country_name} != {expected_country}")
            all_valid = False

        if not has_price:
            print(f"   ⚠️  가격 미설정")
            all_valid = False

    print("\n" + "="*80)
    if all_valid:
        print("🎉 모든 필수 원두가 올바르게 설정되었습니다!")
    else:
        print("⚠️  일부 원두에 문제가 있습니다. 위의 내용을 확인하세요.")
    print("="*80)

    return all_valid


def main():
    """
    메인 실행
    """
    print("="*80)
    print("🚀 원두 마스터 데이터 업데이트 시작")
    print("="*80)
    print("마스터플랜 v2 - Phase 1, Task T1-2")
    print("업데이트 대상: 4개 원두 (마사이, g4, 브라질, 콜롬비아)")
    print("="*80)

    db = SessionLocal()

    try:
        # 1. 업데이트
        updated_count = update_bean_master_data(db)

        # 2. 커밋
        db.commit()
        print(f"\n✅ {updated_count}개 원두 업데이트 완료")

        # 3. 검증
        verify_master_beans(db)

        print("\n" + "="*80)
        print("🎉 T1-2 작업 완료!")
        print("="*80)

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
