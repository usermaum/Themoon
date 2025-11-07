#!/usr/bin/env python3
"""
로스팅 데이터 마이그레이션 스크립트

마스터플랜 v2 - Phase 1, Task T1-1
2개월분 테스트 로스팅 데이터 생성 및 DB 삽입
"""

import sys
from datetime import date
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine
from models import Base, Bean, RoastingLog

# 블렌드 데이터 (Sheet1 (2)에서 추출)
BLEND_DATA = {
    'full_moon': {
        'total_roasted_per_month': 11000,  # 22,000 / 2개월
        'beans': [
            {'name': '마사이', 'ratio': 0.4, 'roasted_per_month': 4400},
            {'name': '안티구아', 'ratio': 0.4, 'roasted_per_month': 4400},
            {'name': '모모라', 'ratio': 0.1, 'roasted_per_month': 1100},
            {'name': 'g4', 'ratio': 0.1, 'roasted_per_month': 1100}
        ]
    },
    'new_moon': {
        'total_roasted_per_month': 2000,  # 4,000 / 2개월
        'beans': [
            {'name': '브라질', 'ratio': 0.6, 'roasted_per_month': 1200},
            {'name': '콜롬비아', 'ratio': 0.3, 'roasted_per_month': 600},
            {'name': 'g4', 'ratio': 0.1, 'roasted_per_month': 200}
        ]
    }
}

# 2개월 데이터
MONTHS = ['2025-09', '2025-10']

# 손실률 17% (0.83 = 1 - 0.17)
LOSS_RATE = 0.17
ROASTING_EFFICIENCY = 1 - LOSS_RATE  # 0.83


def calculate_raw_weight(roasted_weight_kg: float) -> float:
    """
    로스팅량으로부터 생두량 계산
    생두량 = 로스팅량 / 0.83
    """
    return round(roasted_weight_kg / ROASTING_EFFICIENCY, 2)


def calculate_loss_rate(raw_weight_kg: float, roasted_weight_kg: float) -> float:
    """
    손실률 계산
    손실률 = (생두량 - 로스팅량) / 생두량 * 100
    """
    return round((raw_weight_kg - roasted_weight_kg) / raw_weight_kg * 100, 2)


def get_or_create_bean(db: Session, bean_name: str) -> Bean:
    """
    원두 조회 또는 생성
    """
    bean = db.query(Bean).filter(Bean.name == bean_name).first()
    if not bean:
        # 기존 beans에서 최대 no 값 찾기
        max_no = db.query(Bean.no).order_by(Bean.no.desc()).first()
        next_no = (max_no[0] + 1) if max_no else 1

        # 새 원두 생성 (기본 정보)
        bean = Bean(
            no=next_no,
            name=bean_name,
            country_name='Unknown',  # 추후 업데이트
            roast_level='N',  # 기본값
            price_per_kg=10000.0,  # 기본 가격 (추후 업데이트)
            status='active'
        )
        db.add(bean)
        db.flush()
        print(f"  ✅ 새 원두 생성: {bean_name} (ID: {bean.id}, no: {next_no})")
    return bean


def clear_roasting_logs(db: Session):
    """
    기존 roasting_logs 데이터 삭제
    """
    count = db.query(RoastingLog).count()
    if count > 0:
        print(f"⚠️  기존 roasting_logs 데이터 {count}개 삭제 중...")
        db.query(RoastingLog).delete()
        db.commit()
        print(f"✅ 삭제 완료")
    else:
        print("ℹ️  기존 roasting_logs 데이터 없음")


def generate_roasting_data(db: Session):
    """
    2개월분 로스팅 데이터 생성
    """
    total_records = 0

    for month_idx, month in enumerate(MONTHS):
        print(f"\n📅 {month} 데이터 생성 중...")
        roasting_date = date.fromisoformat(f"{month}-15")  # 매월 15일로 설정
        roasting_month = month  # YYYY-MM 형식

        # 풀문 블렌드
        print(f"  🌕 풀문 블렌드:")
        for bean_info in BLEND_DATA['full_moon']['beans']:
            bean_name = bean_info['name']
            roasted_kg = bean_info['roasted_per_month']
            raw_kg = calculate_raw_weight(roasted_kg)
            loss_rate = calculate_loss_rate(raw_kg, roasted_kg)

            bean = get_or_create_bean(db, bean_name)

            log = RoastingLog(
                bean_id=bean.id,
                raw_weight_kg=raw_kg,
                roasted_weight_kg=roasted_kg,
                loss_rate_percent=loss_rate,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=loss_rate - 17.0,
                roasting_date=roasting_date,
                roasting_month=roasting_month,
                notes=f"풀문 블렌드 ({bean_info['ratio']*100:.0f}%) - 테스트 데이터"
            )
            db.add(log)
            total_records += 1

            print(f"     {bean_name}: 생두 {raw_kg}kg → 로스팅 {roasted_kg}kg (손실률 {loss_rate}%)")

        # 뉴문 블렌드
        print(f"  🌑 뉴문 블렌드:")
        for bean_info in BLEND_DATA['new_moon']['beans']:
            bean_name = bean_info['name']

            # g4는 이미 풀문에서 추가되었으므로 건너뛰기 (같은 날짜)
            if bean_name == 'g4':
                continue

            roasted_kg = bean_info['roasted_per_month']
            raw_kg = calculate_raw_weight(roasted_kg)
            loss_rate = calculate_loss_rate(raw_kg, roasted_kg)

            bean = get_or_create_bean(db, bean_name)

            log = RoastingLog(
                bean_id=bean.id,
                raw_weight_kg=raw_kg,
                roasted_weight_kg=roasted_kg,
                loss_rate_percent=loss_rate,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=loss_rate - 17.0,
                roasting_date=roasting_date,
                roasting_month=roasting_month,
                notes=f"뉴문 블렌드 ({bean_info['ratio']*100:.0f}%) - 테스트 데이터"
            )
            db.add(log)
            total_records += 1

            print(f"     {bean_name}: 생두 {raw_kg}kg → 로스팅 {roasted_kg}kg (손실률 {loss_rate}%)")

        # g4는 풀문+뉴문 합계
        print(f"  📊 g4 (풀문 + 뉴문 합계):")
        full_moon_g4 = next(b for b in BLEND_DATA['full_moon']['beans'] if b['name'] == 'g4')
        new_moon_g4 = next(b for b in BLEND_DATA['new_moon']['beans'] if b['name'] == 'g4')

        g4_roasted_kg = full_moon_g4['roasted_per_month'] + new_moon_g4['roasted_per_month']
        g4_raw_kg = calculate_raw_weight(g4_roasted_kg)
        g4_loss_rate = calculate_loss_rate(g4_raw_kg, g4_roasted_kg)

        g4_bean = get_or_create_bean(db, 'g4')

        g4_log = RoastingLog(
            bean_id=g4_bean.id,
            raw_weight_kg=g4_raw_kg,
            roasted_weight_kg=g4_roasted_kg,
            loss_rate_percent=g4_loss_rate,
            expected_loss_rate_percent=17.0,
            loss_variance_percent=g4_loss_rate - 17.0,
            roasting_date=roasting_date,
            roasting_month=roasting_month,
            notes=f"풀문 블렌드 (10%) + 뉴문 블렌드 (10%) - 테스트 데이터"
        )
        db.add(g4_log)
        total_records += 1

        print(f"     g4: 생두 {g4_raw_kg}kg → 로스팅 {g4_roasted_kg}kg (손실률 {g4_loss_rate}%)")

    return total_records


def validate_data(db: Session):
    """
    마이그레이션 후 데이터 검증
    """
    print("\n" + "="*80)
    print("🔍 데이터 검증 중...")
    print("="*80)

    # 1. 레코드 수 확인
    total_count = db.query(RoastingLog).count()
    print(f"\n1️⃣ 레코드 수: {total_count}개")
    expected_count = len(MONTHS) * 6  # 2개월 * (풀문 4개 + 뉴문 2개)
    if total_count == expected_count:
        print(f"   ✅ 예상 레코드 수와 일치 ({expected_count}개)")
    else:
        print(f"   ⚠️  예상 레코드 수 불일치: 예상 {expected_count}개, 실제 {total_count}개")

    # 2. 월별 집계
    print(f"\n2️⃣ 월별 집계:")
    for month in MONTHS:
        month_logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_date >= date.fromisoformat(f"{month}-01"),
            RoastingLog.roasting_date < date.fromisoformat(f"{month}-28")
        ).all()

        total_raw = sum(log.raw_weight_kg for log in month_logs)
        total_roasted = sum(log.roasted_weight_kg for log in month_logs)
        avg_loss_rate = (total_raw - total_roasted) / total_raw * 100 if total_raw > 0 else 0

        print(f"   {month}: {len(month_logs)}개 레코드")
        print(f"      생두량: {total_raw:.2f}kg")
        print(f"      로스팅량: {total_roasted:.2f}kg")
        print(f"      손실률: {avg_loss_rate:.2f}%")

        if abs(avg_loss_rate - 17.0) < 0.5:
            print(f"      ✅ 손실률이 목표(17%) 범위 내")
        else:
            print(f"      ⚠️  손실률이 목표(17%)를 벗어남")

    # 3. 원두별 집계
    print(f"\n3️⃣ 원두별 집계:")
    unique_bean_ids = db.query(RoastingLog.bean_id).distinct().all()
    for (bean_id,) in unique_bean_ids:
        bean = db.query(Bean).filter(Bean.id == bean_id).first()
        bean_logs = db.query(RoastingLog).filter(RoastingLog.bean_id == bean_id).all()
        total_raw = sum(log.raw_weight_kg for log in bean_logs)
        total_roasted = sum(log.roasted_weight_kg for log in bean_logs)

        print(f"   {bean.name}: 생두 {total_raw:.2f}kg → 로스팅 {total_roasted:.2f}kg ({len(bean_logs)}건)")

    # 4. 총 합계
    print(f"\n4️⃣ 전체 합계:")
    all_logs = db.query(RoastingLog).all()
    grand_total_raw = sum(log.raw_weight_kg for log in all_logs)
    grand_total_roasted = sum(log.roasted_weight_kg for log in all_logs)
    grand_avg_loss_rate = (grand_total_raw - grand_total_roasted) / grand_total_raw * 100

    print(f"   총 생두량: {grand_total_raw:.2f}kg")
    print(f"   총 로스팅량: {grand_total_roasted:.2f}kg")
    print(f"   평균 손실률: {grand_avg_loss_rate:.2f}%")

    # 마스터플랜 목표와 비교
    expected_total_raw = 31325.3  # 마스터플랜 명시
    expected_total_roasted = 26000  # 마스터플랜 명시

    print(f"\n5️⃣ 마스터플랜 목표 대비:")
    print(f"   목표 생두량: {expected_total_raw}kg (실제: {grand_total_raw:.2f}kg)")
    print(f"   목표 로스팅량: {expected_total_roasted}kg (실제: {grand_total_roasted:.2f}kg)")

    raw_diff = abs(grand_total_raw - expected_total_raw) / expected_total_raw * 100
    roasted_diff = abs(grand_total_roasted - expected_total_roasted) / expected_total_roasted * 100

    if raw_diff < 1 and roasted_diff < 1:
        print(f"   ✅ 목표와 1% 이내로 일치")
    else:
        print(f"   ⚠️  생두량 차이: {raw_diff:.1f}%, 로스팅량 차이: {roasted_diff:.1f}%")

    print("\n" + "="*80)


def main():
    """
    메인 마이그레이션 프로세스
    """
    print("="*80)
    print("🚀 로스팅 데이터 마이그레이션 시작")
    print("="*80)
    print(f"마스터플랜 v2 - Phase 1, Task T1-1")
    print(f"2개월분 테스트 데이터 생성 (2025-09, 2025-10)")
    print("="*80)

    # 데이터베이스 연결
    db = SessionLocal()

    try:
        # 1. 기존 데이터 삭제
        print("\n📋 Step 1: 기존 데이터 삭제")
        clear_roasting_logs(db)

        # 2. 테스트 데이터 생성
        print("\n📋 Step 2: 테스트 데이터 생성")
        total_records = generate_roasting_data(db)

        # 3. 커밋
        db.commit()
        print(f"\n✅ 총 {total_records}개 레코드 생성 완료")

        # 4. 검증
        validate_data(db)

        print("\n" + "="*80)
        print("🎉 마이그레이션 성공!")
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
