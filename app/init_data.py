"""
데이터베이스 초기화 및 기본 데이터 로드
프로젝트 시작 시 한 번만 실행
"""

import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.database import init_db, SessionLocal, CostSetting
from services.bean_service import BeanService
from services.blend_service import BlendService
from utils.constants import DEFAULT_COST_SETTINGS
from datetime import datetime

def init_database():
    """데이터베이스 전체 초기화"""
    print("\n" + "="*70)
    print("🚀 데이터베이스 초기화 시작")
    print("="*70)

    # 1. 테이블 생성
    print("\n1️⃣  데이터베이스 테이블 생성 중...")
    init_db()

    # 2. 세션 생성
    db = SessionLocal()

    # 3. 원두 데이터 로드
    print("\n2️⃣  기본 원두 데이터 로드 중... (13종)")
    bean_service = BeanService(db)
    bean_count = bean_service.init_default_beans()
    print(f"   ✅ {bean_count}개 원두 로드 완료")

    # 원두 요약
    bean_summary = bean_service.get_beans_summary()
    print(f"\n   📊 원두 요약:")
    print(f"   - 총 원두: {bean_summary['total_beans']}종")
    print(f"   - 로스팅 레벨 분포:")
    for level, count in bean_summary['by_roast_level'].items():
        print(f"     • {level}: {count}개")

    # 4. 블렌드 데이터 로드
    print("\n3️⃣  기본 블렌드 데이터 로드 중... (7개)")
    blend_service = BlendService(db)
    blend_count = blend_service.init_default_blends()
    print(f"   ✅ {blend_count}개 블렌드 로드 완료")

    # 블렌드 요약
    blend_summary = blend_service.get_blends_summary()
    print(f"\n   📊 블렌드 요약:")
    print(f"   - 총 블렌드: {blend_summary['total_blends']}개")
    print(f"   - 타입별 분포:")
    for blend_type, count in blend_summary['by_type'].items():
        print(f"     • {blend_type}: {count}개")

    # 5. 비용 설정 로드
    print("\n4️⃣  기본 비용 설정 로드 중...")
    for param_name, value in DEFAULT_COST_SETTINGS.items():
        existing = db.query(CostSetting).filter(
            CostSetting.parameter_name == param_name
        ).first()

        if not existing:
            setting = CostSetting(
                parameter_name=param_name,
                value=value,
                description=f"Default {param_name}",
                updated_at=datetime.utcnow()
            )
            db.add(setting)

    db.commit()
    print(f"   ✅ {len(DEFAULT_COST_SETTINGS)}개 비용 설정 로드 완료")

    # 6. 블렌드별 원가 계산 예시
    print("\n5️⃣  블렌드별 원가 계산:")
    active_blends = blend_service.get_active_blends()
    for blend in active_blends:
        if blend.total_portion > 0:  # 레시피가 있는 것만
            cost_info = blend_service.calculate_blend_cost(blend.id)
            if cost_info:
                print(f"\n   🎨 {cost_info['blend_name']} ({cost_info['blend_type']})")
                print(f"   - 포션: {cost_info['total_portion']}개")
                print(f"   - 포션당 원가: ₩{cost_info['cost_per_portion']:,.0f}")
                print(f"   - 제안 판매가: ₩{cost_info['suggested_price']:,.0f}")
                print(f"   - 예상 이익: ₩{cost_info['profit_margin']:,.0f}")

    db.close()

    print("\n" + "="*70)
    print("✅ 데이터베이스 초기화 완료!")
    print("="*70 + "\n")

    return True


def verify_database():
    """데이터베이스 검증"""
    print("\n" + "="*70)
    print("🔍 데이터베이스 검증")
    print("="*70)

    db = SessionLocal()

    from models.database import Bean, Blend, Inventory

    # 1. 원두 검증
    bean_count = db.query(Bean).filter(Bean.status == "active").count()
    print(f"\n✅ 활성 원두: {bean_count}종")

    # 2. 블렌드 검증
    blend_count = db.query(Blend).filter(Blend.status == "active").count()
    print(f"✅ 활성 블렌드: {blend_count}개")

    # 3. 재고 검증
    inventory_count = db.query(Inventory).count()
    print(f"✅ 재고 기록: {inventory_count}개")

    db.close()

    print("\n" + "="*70 + "\n")

    return True


if __name__ == "__main__":
    # 데이터베이스 초기화
    init_database()

    # 데이터베이스 검증
    verify_database()

    print("🎉 모든 준비가 완료되었습니다!")
    print("📝 app/app.py를 실행하여 Streamlit 앱을 시작하세요")
    print("   명령어: streamlit run app/app.py\n")
