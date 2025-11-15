#!/usr/bin/env python3
"""
원두 정보 검증 및 수정

전체 원두 데이터의 정확성을 검증하고 문제를 수정합니다.
- 디카페 가격 설정
- 중복 원두 정리
- 정보 완성도 확인
"""

import sys
from sqlalchemy.orm import Session
from models.database import SessionLocal, Bean


# 원두 정보 업데이트 (가격, 설명 등)
BEAN_UPDATES = {
    # 디카페 원두 가격 설정
    '디카페 SDM': {
        'price_per_kg': 7500.0,  # 디카페는 일반보다 1.5배 정도
        'description': '에티오피아 디카페 (Swiss Decaf Method)'
    },
    '디카페 SM': {
        'price_per_kg': 8000.0,
        'description': '콜롬비아 디카페 (Sugarcane Method)'
    },
    '스위스워터': {
        'price_per_kg': 7000.0,
        'description': '브라질 디카페 (Swiss Water Process)'
    },
    # 기존 원두 정보 보완
    '예가체프': {
        'description': '에티오피아 대표 스페셜티 - 플로럴, 시트러스 향'
    },
    '코케허니': {
        'description': '에티오피아 내추럴 프로세스 - 달콤하고 과일 풍미'
    },
    '우라가': {
        'description': '에티오피아 워시드 - 깔끔하고 밝은 산미'
    },
    'AA FAQ': {
        'description': '케냐 최고 등급 - 강한 산미와 베리 향'
    },
    '키린야가': {
        'description': '케냐 피베리 - 진한 바디감과 와인 같은 향'
    },
    '후일라': {
        'description': '콜롬비아 대표 지역 - 균형잡힌 맛과 초콜릿 향'
    },
    '안티구아': {
        'description': '과테말라 화산토 재배 - 스모키하고 풍부한 바디'
    },
    '엘탄케': {
        'description': '코스타리카 레드허니 - 달콤하고 깔끔한 산미'
    },
    '파젠다카르모': {
        'description': '브라질 대표 농장 - 견과류, 초콜릿 향'
    },
    '마사이': {
        'description': '풀문 블렌드 40% 구성 - 플로럴, 밝은 산미'
    },
    'g4': {
        'description': '풀문 10% + 뉴문 10% 구성 - 베리, 와인 향'
    }
}


# 중복 원두 처리 규칙
DUPLICATE_RULES = {
    # '브라질' (no 16)을 유지, '파젠다카르모' (no 10)는 별도 유지
    # '콜롬비아' (no 17)를 유지, '후일라' (no 7)는 별도 유지
    # 중복이 아니라 서로 다른 원두로 간주
}


def verify_bean(bean: Bean) -> list:
    """
    원두 정보 검증

    Returns:
        문제점 리스트
    """
    issues = []

    # 가격 체크
    if bean.price_per_kg == 0:
        issues.append(f"⚠️  가격 미설정 (0원)")

    # 국가 정보 체크
    if not bean.country_name or bean.country_name == 'Unknown':
        issues.append(f"⚠️  국가 정보 없음")

    # 로스팅 레벨 체크
    if not bean.roast_level:
        issues.append(f"⚠️  로스팅 레벨 없음")

    # 설명 체크
    if not bean.description:
        issues.append(f"ℹ️  설명 없음")

    return issues


def update_bean_info(db: Session, bean: Bean, updates: dict) -> bool:
    """
    원두 정보 업데이트
    """
    updated = False

    if 'price_per_kg' in updates and bean.price_per_kg != updates['price_per_kg']:
        old_price = bean.price_per_kg
        bean.price_per_kg = updates['price_per_kg']
        print(f"      가격: ₩{old_price:,.0f} → ₩{updates['price_per_kg']:,.0f}")
        updated = True

    if 'description' in updates and bean.description != updates['description']:
        bean.description = updates['description']
        print(f"      설명: {updates['description'][:50]}...")
        updated = True

    if 'country_name' in updates and bean.country_name != updates['country_name']:
        bean.country_name = updates['country_name']
        print(f"      국가: {updates['country_name']}")
        updated = True

    if 'roast_level' in updates and bean.roast_level != updates['roast_level']:
        bean.roast_level = updates['roast_level']
        print(f"      레벨: {updates['roast_level']}")
        updated = True

    return updated


def main():
    """
    메인 실행
    """
    print("=" * 80)
    print("🔍 원두 정보 검증 및 수정")
    print("=" * 80)

    db = SessionLocal()

    try:
        # 1. 전체 원두 조회
        beans = db.query(Bean).order_by(Bean.no).all()
        print(f"\n총 {len(beans)}종 원두 검증 중...\n")

        # 2. 검증 및 수정
        total_issues = 0
        total_updates = 0

        for bean in beans:
            print(f"{bean.no:2d}. {bean.name:20s} | {bean.country_name:15s} | {bean.roast_level:3s} | ₩{bean.price_per_kg:>7,.0f}/kg")

            # 검증
            issues = verify_bean(bean)
            if issues:
                total_issues += len(issues)
                for issue in issues:
                    print(f"   {issue}")

            # 수정
            if bean.name in BEAN_UPDATES:
                if update_bean_info(db, bean, BEAN_UPDATES[bean.name]):
                    total_updates += 1
                    print(f"   ✅ 정보 업데이트됨")

            print()

        # 3. 커밋
        if total_updates > 0:
            db.commit()
            print(f"✅ {total_updates}개 원두 정보 업데이트 완료")
        else:
            print(f"ℹ️  업데이트 필요 없음")

        # 4. 최종 검증
        print("\n" + "=" * 80)
        print("📊 최종 검증 결과")
        print("=" * 80)

        beans = db.query(Bean).order_by(Bean.no).all()
        perfect_count = 0

        for bean in beans:
            issues = verify_bean(bean)
            if not issues:
                perfect_count += 1
            else:
                print(f"❌ {bean.name}: {', '.join(issues)}")

        print(f"\n✅ 완벽한 원두: {perfect_count}/{len(beans)}종")
        print(f"⚠️  문제 있는 원두: {len(beans) - perfect_count}종")

        print("\n" + "=" * 80)
        print("🎉 원두 정보 검증 완료!")
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
