#!/usr/bin/env python3
"""
데이터 검증 스크립트

현재 데이터베이스의 상태를 확인하고 검증합니다.
- beans 테이블: 13종 원두 확인
- blends 테이블: 풀문, 뉴문 확인
- blend_recipes: 혼합률(%) 확인
- roasting_logs: 실제 데이터 확인
- cost_settings: 원가 정보 확인
"""

import sys
from pathlib import Path

# 프로젝트 루트 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.models.database import get_db, Bean, Blend, BlendRecipe, RoastingLog, CostSetting
from sqlalchemy import func
from datetime import datetime

def print_section(title):
    """섹션 타이틀 출력"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def validate_beans(db):
    """원두 테이블 검증"""
    print_section("1. BEANS 테이블 검증")

    beans = db.query(Bean).all()
    bean_count = len(beans)

    print(f"✅ 총 원두 개수: {bean_count}개")

    if bean_count == 0:
        print("⚠️  경고: 원두 데이터가 없습니다!")
        return False

    print(f"\n{'No':<5} {'원두명':<15} {'국가':<15} {'가격(원/kg)':<15} {'상태':<10}")
    print("-" * 65)

    has_issues = False
    for bean in beans:
        price_status = "✅" if bean.price_per_kg > 0 else "⚠️ 가격 0"
        status_icon = "✅" if bean.status == 'active' else "⚠️"

        print(f"{bean.id:<5} {bean.name:<15} {bean.country_code or 'N/A':<15} "
              f"{bean.price_per_kg:>12,.0f} {status_icon} {bean.status:<10}")

        if bean.price_per_kg <= 0:
            has_issues = True

    if bean_count < 13:
        print(f"\n⚠️  경고: 예상 13종 원두 중 {bean_count}개만 등록됨")
        has_issues = True
    elif bean_count == 13:
        print(f"\n✅ 13종 원두 모두 등록 완료")
    else:
        print(f"\n✅ 13종 초과 ({bean_count}개) 등록됨")

    return not has_issues

def validate_blends(db):
    """블렌드 테이블 검증"""
    print_section("2. BLENDS 테이블 검증")

    blends = db.query(Blend).all()
    blend_count = len(blends)

    print(f"✅ 총 블렌드 개수: {blend_count}개")

    if blend_count == 0:
        print("⚠️  경고: 블렌드 데이터가 없습니다!")
        return False

    print(f"\n{'ID':<5} {'블렌드명':<15} {'블렌드타입':<12} {'판매가(원)':<15} {'상태':<10}")
    print("-" * 65)

    has_issues = False
    fullmoon_found = False
    newmoon_found = False

    for blend in blends:
        price_status = "✅" if blend.suggested_price and blend.suggested_price > 0 else "⚠️ 가격 0"

        print(f"{blend.id:<5} {blend.name:<15} {blend.blend_type or 'N/A':<12} "
              f"{blend.suggested_price or 0:>12,.0f} {blend.status:<10}")

        if blend.name and ("풀문" in blend.name or "Full" in blend.name):
            fullmoon_found = True
        if blend.name and ("뉴문" in blend.name or "New" in blend.name):
            newmoon_found = True

        if not blend.suggested_price or blend.suggested_price <= 0:
            print(f"   ⚠️  판매가가 설정되지 않음")
            has_issues = True

    print(f"\n{'풀문 블렌드':<20}: {'✅ 발견' if fullmoon_found else '❌ 미발견'}")
    print(f"{'뉴문 블렌드':<20}: {'✅ 발견' if newmoon_found else '❌ 미발견'}")

    if not fullmoon_found or not newmoon_found:
        has_issues = True

    return not has_issues

def validate_blend_recipes(db):
    """블렌드 레시피 검증"""
    print_section("3. BLEND_RECIPES 테이블 검증")

    blends = db.query(Blend).all()

    if not blends:
        print("⚠️  블렌드가 없어서 레시피를 검증할 수 없습니다.")
        return False

    has_issues = False

    for blend in blends:
        recipes = db.query(BlendRecipe).filter(
            BlendRecipe.blend_id == blend.id
        ).all()

        print(f"\n🔹 {blend.name} (ID: {blend.id})")
        print(f"{'원두명':<15} {'포션/비율':<12}")
        print("-" * 35)

        if not recipes:
            print("⚠️  레시피가 없습니다!")
            has_issues = True
            continue

        total_ratio = 0
        for recipe in recipes:
            bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
            bean_name = bean.name if bean else f"Unknown (ID:{recipe.bean_id})"

            # ratio 필드가 있으면 사용, 없으면 portion_count 사용
            ratio_value = recipe.ratio if hasattr(recipe, 'ratio') and recipe.ratio else recipe.portion_count or 0

            print(f"{bean_name:<15} {ratio_value:>8.1f}")

            total_ratio += ratio_value

        print(f"\n{'합계':<15} {total_ratio:>8.1f}")

        # 100에 가까운지 확인 (혼합률인 경우)
        if 90 <= total_ratio <= 110:
            if abs(total_ratio - 100.0) > 0.1:
                print(f"⚠️  경고: 혼합률 합계가 100%가 아님 (현재: {total_ratio:.1f}%)")
                has_issues = True
            else:
                print(f"✅ 혼합률 합계 100% 정상")
        else:
            print(f"✅ 레시피 합계: {total_ratio:.1f}")

    return not has_issues

def validate_roasting_logs(db):
    """로스팅 기록 검증"""
    print_section("4. ROASTING_LOGS 테이블 검증")

    total_logs = db.query(RoastingLog).count()

    print(f"✅ 총 로스팅 기록: {total_logs}개")

    if total_logs == 0:
        print("⚠️  경고: 로스팅 기록이 없습니다!")
        print("   Phase 1 T1-1 (마이그레이션) 작업이 필요합니다.")
        return False

    # 월별 통계
    monthly_stats = db.query(
        RoastingLog.roasting_month,
        func.count(RoastingLog.id).label('count'),
        func.sum(RoastingLog.raw_weight_kg).label('total_raw'),
        func.sum(RoastingLog.roasted_weight_kg).label('total_roasted'),
        func.avg(RoastingLog.loss_rate_percent).label('avg_loss_rate')
    ).group_by(RoastingLog.roasting_month).order_by(RoastingLog.roasting_month).all()

    print(f"\n{'월':<10} {'기록수':<10} {'생두량(kg)':<15} {'로스팅량(kg)':<15} {'평균손실률(%)':<15}")
    print("-" * 70)

    has_issues = False
    for stat in monthly_stats:
        month, count, total_raw, total_roasted, avg_loss = stat

        print(f"{month:<10} {count:<10} {total_raw:>12,.1f} {total_roasted:>12,.1f} {avg_loss:>12.2f}")

        if avg_loss < 15 or avg_loss > 20:
            print(f"   ⚠️  평균 손실률 {avg_loss:.1f}%는 비정상 범위 (정상: 15~20%)")
            has_issues = True

    # 이상치 확인
    abnormal_logs = db.query(RoastingLog).filter(
        (RoastingLog.loss_rate_percent < 15) | (RoastingLog.loss_rate_percent > 20)
    ).count()

    if abnormal_logs > 0:
        print(f"\n⚠️  손실률 이상치: {abnormal_logs}개 레코드 (15% 미만 또는 20% 초과)")
        has_issues = True
    else:
        print(f"\n✅ 모든 레코드의 손실률 정상 범위 (15~20%)")

    # NULL 값 확인
    null_checks = {
        'raw_weight_kg': db.query(RoastingLog).filter(RoastingLog.raw_weight_kg == None).count(),
        'roasted_weight_kg': db.query(RoastingLog).filter(RoastingLog.roasted_weight_kg == None).count(),
        'roasting_date': db.query(RoastingLog).filter(RoastingLog.roasting_date == None).count(),
    }

    null_found = False
    for field, count in null_checks.items():
        if count > 0:
            print(f"⚠️  {field} NULL 값: {count}개")
            null_found = True
            has_issues = True

    if not null_found:
        print(f"✅ 필수 필드 NULL 값 없음")

    return not has_issues

def validate_cost_settings(db):
    """원가 설정 검증"""
    print_section("5. COST_SETTINGS 테이블 검증")

    settings = db.query(CostSetting).all()
    setting_count = len(settings)

    print(f"✅ 총 설정 개수: {setting_count}개")

    if setting_count == 0:
        print("⚠️  경고: 원가 설정이 없습니다!")
        return False

    print(f"\n{'설정명':<30} {'값':<20}")
    print("-" * 55)

    for setting in settings:
        print(f"{setting.parameter_name:<30} {setting.value:<20}")

    return True

def generate_summary_report(results):
    """검증 결과 요약"""
    print_section("📊 검증 결과 요약")

    checks = {
        'Beans (원두)': results['beans'],
        'Blends (블렌드)': results['blends'],
        'Blend Recipes (레시피)': results['blend_recipes'],
        'Roasting Logs (로스팅 기록)': results['roasting_logs'],
        'Cost Settings (원가 설정)': results['cost_settings'],
    }

    passed = sum(1 for v in checks.values() if v)
    total = len(checks)

    print(f"\n{'검증 항목':<35} {'결과':<10}")
    print("-" * 50)

    for name, status in checks.items():
        status_icon = "✅ 통과" if status else "❌ 실패"
        print(f"{name:<35} {status_icon}")

    print(f"\n{'='*50}")
    print(f"전체 결과: {passed}/{total} 통과 ({passed/total*100:.0f}%)")
    print(f"{'='*50}\n")

    if passed == total:
        print("✅ 모든 검증 통과! 데이터 상태 양호합니다.")
        return True
    else:
        print("⚠️  일부 검증 실패. 위의 경고를 확인하세요.")
        return False

def main():
    """메인 함수"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         The Moon Drip BAR - 데이터 검증 스크립트          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"\n실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    db = next(get_db())

    try:
        results = {
            'beans': validate_beans(db),
            'blends': validate_blends(db),
            'blend_recipes': validate_blend_recipes(db),
            'roasting_logs': validate_roasting_logs(db),
            'cost_settings': validate_cost_settings(db),
        }

        all_passed = generate_summary_report(results)

        # 종료 코드
        sys.exit(0 if all_passed else 1)

    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
    finally:
        db.close()

if __name__ == "__main__":
    main()
