"""
테스트 로스팅 데이터 생성 스크립트

계절성 패턴을 반영한 1년치 테스트 데이터를 생성합니다.
"""

import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, RoastingLog, Bean


# ═══════════════════════════════════════════════════════════════
# 설정
# ═══════════════════════════════════════════════════════════════

# 계절성 패턴 (월별 손실률 조정값, %)
SEASONAL_PATTERN = {
    1: -1.5,   # 1월: 겨울, 건조, 손실률 낮음
    2: -1.0,   # 2월
    3: 0.0,    # 3월: 봄, 정상
    4: +0.5,   # 4월
    5: +1.0,   # 5월
    6: +2.0,   # 6월: 여름 시작, 습도 증가
    7: +3.5,   # 7월: 여름 최고
    8: +3.0,   # 8월
    9: +1.0,   # 9월: 가을
    10: 0.0,   # 10월: 정상
    11: -0.5,  # 11월
    12: -1.5,  # 12월: 겨울
}

# 기본 손실률
BASE_LOSS_RATE = 17.0

# 정규 분포 표준편차
STD_DEV = 1.5

# 생성할 데이터 개수
DATA_COUNT = 100

# 날짜 범위
START_DATE = datetime(2024, 1, 1).date()
END_DATE = datetime(2025, 11, 8).date()

# 원두 ID 범위 (1~17)
BEAN_ID_MIN = 1
BEAN_ID_MAX = 17


# ═══════════════════════════════════════════════════════════════
# 데이터 생성 함수
# ═══════════════════════════════════════════════════════════════

def generate_random_date(start: datetime.date, end: datetime.date) -> datetime.date:
    """지정된 범위 내에서 랜덤 날짜 생성"""
    days_between = (end - start).days
    random_days = random.randint(0, days_between)
    return start + timedelta(days=random_days)


def calculate_loss_rate(month: int) -> float:
    """
    계절성을 반영한 손실률 계산

    Args:
        month: 월 (1~12)

    Returns:
        손실률 (%)
    """
    seasonal_adjustment = SEASONAL_PATTERN.get(month, 0.0)
    base_with_seasonal = BASE_LOSS_RATE + seasonal_adjustment

    # 정규 분포 노이즈 추가
    noise = random.gauss(0, STD_DEV)

    loss_rate = base_with_seasonal + noise

    # 손실률 범위 제한 (10% ~ 25%)
    loss_rate = max(10.0, min(25.0, loss_rate))

    return round(loss_rate, 2)


def generate_test_roasting_records(db: Session, count: int = DATA_COUNT) -> list:
    """
    테스트 로스팅 기록 생성

    Args:
        db: SQLAlchemy 세션
        count: 생성할 레코드 개수

    Returns:
        생성된 RoastingLog 객체 리스트
    """
    print(f"🔄 {count}개의 테스트 로스팅 데이터 생성 중...")

    records = []

    for i in range(count):
        # 1. 랜덤 날짜 생성
        roasting_date = generate_random_date(START_DATE, END_DATE)

        # 2. 랜덤 원두 선택 (1~17)
        bean_id = random.randint(BEAN_ID_MIN, BEAN_ID_MAX)

        # 3. 계절성 반영 손실률 계산
        month = roasting_date.month
        loss_rate = calculate_loss_rate(month)

        # 4. 생두 투입량 (10kg ~ 50kg 랜덤)
        raw_weight = round(random.uniform(10.0, 50.0), 2)

        # 5. 로스팅 후 무게 계산
        roasted_weight = round(raw_weight * (1 - loss_rate / 100), 2)

        # 6. 예상 손실률 (17%) 및 편차
        expected_loss_rate = BASE_LOSS_RATE
        loss_variance = round(loss_rate - expected_loss_rate, 2)

        # 7. RoastingLog 객체 생성
        roasting_log = RoastingLog(
            bean_id=bean_id,
            raw_weight_kg=raw_weight,
            roasted_weight_kg=roasted_weight,
            loss_rate_percent=loss_rate,
            expected_loss_rate_percent=expected_loss_rate,
            loss_variance_percent=loss_variance,
            roasting_date=roasting_date,
            roasting_month=roasting_date.strftime("%Y-%m"),
            notes=f"테스트 데이터 (계절성 반영: {month}월)"
        )

        records.append(roasting_log)

        # 진행률 표시
        if (i + 1) % 10 == 0:
            print(f"  ✓ {i + 1}/{count} 생성 완료...")

    return records


def insert_test_data(db: Session, records: list) -> int:
    """
    테스트 데이터 DB 삽입

    Args:
        db: SQLAlchemy 세션
        records: RoastingLog 객체 리스트

    Returns:
        삽입된 레코드 개수
    """
    print(f"\n💾 데이터베이스에 {len(records)}개 레코드 삽입 중...")

    try:
        db.add_all(records)
        db.commit()
        print(f"✅ {len(records)}개 레코드 삽입 완료!")
        return len(records)

    except Exception as e:
        db.rollback()
        print(f"❌ 삽입 실패: {e}")
        return 0


def verify_data(db: Session):
    """생성된 데이터 검증"""
    print("\n📊 데이터 검증 중...")

    # 총 레코드 수
    total_count = db.query(RoastingLog).count()
    print(f"  총 로스팅 기록: {total_count}개")

    # 테스트 데이터 수
    test_count = db.query(RoastingLog).filter(
        RoastingLog.notes.like("%테스트 데이터%")
    ).count()
    print(f"  테스트 데이터: {test_count}개")

    # 월별 분포
    from sqlalchemy import func
    monthly_dist = db.query(
        func.substr(RoastingLog.roasting_month, 6, 2).label('month'),
        func.count(RoastingLog.id).label('count'),
        func.avg(RoastingLog.loss_rate_percent).label('avg_loss')
    ).filter(
        RoastingLog.notes.like("%테스트 데이터%")
    ).group_by('month').order_by('month').all()

    print("\n  월별 분포 및 평균 손실률:")
    for month, count, avg_loss in monthly_dist:
        seasonal = SEASONAL_PATTERN.get(int(month), 0)
        print(f"    {month}월: {count:2d}건, 평균 {avg_loss:5.2f}% (기대: {BASE_LOSS_RATE + seasonal:.2f}%)")

    # 원두별 분포
    bean_dist = db.query(
        Bean.name,
        func.count(RoastingLog.id).label('count')
    ).join(
        RoastingLog, RoastingLog.bean_id == Bean.id
    ).filter(
        RoastingLog.notes.like("%테스트 데이터%")
    ).group_by(Bean.name).order_by(func.count(RoastingLog.id).desc()).all()

    print(f"\n  원두별 분포 (상위 5개):")
    for bean_name, count in bean_dist[:5]:
        print(f"    {bean_name}: {count}건")


# ═══════════════════════════════════════════════════════════════
# 메인 실행
# ═══════════════════════════════════════════════════════════════

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("테스트 로스팅 데이터 생성 스크립트")
    print("=" * 60)
    print(f"\n설정:")
    print(f"  데이터 개수: {DATA_COUNT}개")
    print(f"  날짜 범위: {START_DATE} ~ {END_DATE}")
    print(f"  기본 손실률: {BASE_LOSS_RATE}%")
    print(f"  표준편차: {STD_DEV}%")
    print(f"  계절성 패턴: 여름(+3.5%), 겨울(-1.5%)\n")

    # 사용자 확인
    confirm = input("⚠️  기존 테스트 데이터가 있다면 중복됩니다. 계속하시겠습니까? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ 취소되었습니다.")
        return

    # DB 세션 생성
    db = SessionLocal()

    try:
        # 1. 테스트 데이터 생성
        records = generate_test_roasting_records(db, DATA_COUNT)

        # 2. DB 삽입
        inserted_count = insert_test_data(db, records)

        if inserted_count > 0:
            # 3. 검증
            verify_data(db)

        print("\n" + "=" * 60)
        print("✅ 작업 완료!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    main()
