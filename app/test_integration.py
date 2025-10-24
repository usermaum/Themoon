"""
통합 테스트 스크립트
애플리케이션의 모든 구성 요소가 올바르게 작동하는지 검증
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════════════════════════════════════════
# 테스트 결과 출력 헬퍼
# ═══════════════════════════════════════════════════════════════════════════════

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name):
        self.passed += 1
        print(f"✅ {test_name}")

    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"❌ {test_name}: {error}")

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "="*70)
        print(f"📊 테스트 결과: {self.passed}/{total} 통과")
        print("="*70)
        if self.errors:
            print("\n❌ 실패한 테스트:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        return self.failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# Test 1: 모듈 임포트 확인
# ═══════════════════════════════════════════════════════════════════════════════

def test_imports():
    """모든 필수 모듈이 임포트 가능한지 확인"""
    print("\n🔍 Test 1: 모듈 임포트 확인")
    print("-" * 70)

    result = TestResult()

    # 핵심 라이브러리
    try:
        import streamlit as st
        result.add_pass("Streamlit 임포트")
    except Exception as e:
        result.add_fail("Streamlit 임포트", str(e))

    try:
        import pandas as pd
        result.add_pass("Pandas 임포트")
    except Exception as e:
        result.add_fail("Pandas 임포트", str(e))

    try:
        import plotly.graph_objects as go
        result.add_pass("Plotly 임포트")
    except Exception as e:
        result.add_fail("Plotly 임포트", str(e))

    try:
        import sqlalchemy
        result.add_pass("SQLAlchemy 임포트")
    except Exception as e:
        result.add_fail("SQLAlchemy 임포트", str(e))

    try:
        import openpyxl
        result.add_pass("openpyxl 임포트")
    except Exception as e:
        result.add_fail("openpyxl 임포트", str(e))

    # 프로젝트 모듈
    try:
        from models import SessionLocal, init_db
        result.add_pass("Models 임포트")
    except Exception as e:
        result.add_fail("Models 임포트", str(e))

    try:
        from services.bean_service import BeanService
        result.add_pass("BeanService 임포트")
    except Exception as e:
        result.add_fail("BeanService 임포트", str(e))

    try:
        from services.blend_service import BlendService
        result.add_pass("BlendService 임포트")
    except Exception as e:
        result.add_fail("BlendService 임포트", str(e))

    try:
        from services.report_service import ReportService
        result.add_pass("ReportService 임포트")
    except Exception as e:
        result.add_fail("ReportService 임포트", str(e))

    try:
        from services.excel_service import ExcelService
        result.add_pass("ExcelService 임포트")
    except Exception as e:
        result.add_fail("ExcelService 임포트", str(e))

    try:
        from services.analytics_service import AnalyticsService
        result.add_pass("AnalyticsService 임포트")
    except Exception as e:
        result.add_fail("AnalyticsService 임포트", str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 2: 데이터베이스 연결 및 초기화
# ═══════════════════════════════════════════════════════════════════════════════

def test_database():
    """데이터베이스 연결 및 기본 기능 확인"""
    print("\n🔍 Test 2: 데이터베이스 연결 및 초기화")
    print("-" * 70)

    result = TestResult()

    try:
        from models import SessionLocal, init_db, Bean, Blend

        # 데이터베이스 연결
        try:
            db = SessionLocal()
            result.add_pass("데이터베이스 연결")
        except Exception as e:
            result.add_fail("데이터베이스 연결", str(e))
            return result

        # 테이블 확인
        try:
            bean_count = db.query(Bean).count()
            result.add_pass(f"Bean 테이블 확인 ({bean_count}개)")
        except Exception as e:
            result.add_fail("Bean 테이블 확인", str(e))

        try:
            blend_count = db.query(Blend).count()
            result.add_pass(f"Blend 테이블 확인 ({blend_count}개)")
        except Exception as e:
            result.add_fail("Blend 테이블 확인", str(e))

        # 데이터 조회
        try:
            beans = db.query(Bean).filter(Bean.status == "active").all()
            result.add_pass(f"원두 조회 ({len(beans)}종 활성)")
        except Exception as e:
            result.add_fail("원두 조회", str(e))

        try:
            blends = db.query(Blend).filter(Blend.status == "active").all()
            result.add_pass(f"블렌드 조회 ({len(blends)}개 활성)")
        except Exception as e:
            result.add_fail("블렌드 조회", str(e))

        db.close()

    except Exception as e:
        result.add_fail("데이터베이스 테스트", str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 3: 서비스 기능 확인
# ═══════════════════════════════════════════════════════════════════════════════

def test_services():
    """각 서비스의 기본 기능 확인"""
    print("\n🔍 Test 3: 서비스 기능 확인")
    print("-" * 70)

    result = TestResult()

    try:
        from models import SessionLocal
        from services.bean_service import BeanService
        from services.blend_service import BlendService
        from services.report_service import ReportService
        from services.excel_service import ExcelService
        from services.analytics_service import AnalyticsService

        db = SessionLocal()

        # BeanService 테스트
        try:
            bean_service = BeanService(db)
            summary = bean_service.get_beans_summary()
            result.add_pass(f"BeanService.get_beans_summary() ({summary['total_beans']}종)")
        except Exception as e:
            result.add_fail("BeanService 테스트", str(e))

        # BlendService 테스트
        try:
            blend_service = BlendService(db)
            summary = blend_service.get_blends_summary()
            result.add_pass(f"BlendService.get_blends_summary() ({summary['total_blends']}개)")
        except Exception as e:
            result.add_fail("BlendService 테스트", str(e))

        # ReportService 테스트
        try:
            report_service = ReportService(db)
            monthly = report_service.get_monthly_summary(datetime.now().year, datetime.now().month)
            result.add_pass(f"ReportService.get_monthly_summary() ({monthly['transaction_count']}건)")
        except Exception as e:
            result.add_fail("ReportService 테스트", str(e))

        # ExcelService 테스트
        try:
            excel_service = ExcelService(db)
            result.add_pass("ExcelService 인스턴스화")
        except Exception as e:
            result.add_fail("ExcelService 테스트", str(e))

        # AnalyticsService 테스트
        try:
            analytics_service = AnalyticsService(db)
            trend = analytics_service.get_monthly_trend(3)
            result.add_pass(f"AnalyticsService.get_monthly_trend() ({len(trend)}개월)")
        except Exception as e:
            result.add_fail("AnalyticsService 테스트", str(e))

        db.close()

    except Exception as e:
        result.add_fail("서비스 테스트", str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 4: 페이지 파일 확인
# ═══════════════════════════════════════════════════════════════════════════════

def test_pages():
    """모든 페이지 파일이 존재하는지 확인"""
    print("\n🔍 Test 4: 페이지 파일 확인")
    print("-" * 70)

    result = TestResult()

    pages = [
        "pages/1_대시보드.py",
        "pages/2_원두관리.py",
        "pages/3_블렌딩관리.py",
        "pages/4_분석.py",
        "pages/5_재고관리.py",
        "pages/6_보고서.py",
        "pages/7_설정.py",
        "pages/8_Excel동기화.py",
        "pages/9_고급분석.py"
    ]

    for page in pages:
        page_path = os.path.join(os.path.dirname(__file__), page)
        if os.path.exists(page_path):
            with open(page_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            result.add_pass(f"{page} ({lines} lines)")
        else:
            result.add_fail(f"{page} 찾기", "파일 없음")

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 5: 데이터 무결성 확인
# ═══════════════════════════════════════════════════════════════════════════════

def test_data_integrity():
    """데이터 무결성 검증"""
    print("\n🔍 Test 5: 데이터 무결성 확인")
    print("-" * 70)

    result = TestResult()

    try:
        from models import SessionLocal, Bean, Blend, Inventory

        db = SessionLocal()

        # 원두 데이터
        try:
            beans = db.query(Bean).filter(Bean.status == "active").all()
            invalid_beans = [b for b in beans if not b.name or not b.roast_level]
            if not invalid_beans:
                result.add_pass(f"원두 데이터 무결성 ({len(beans)}종 정상)")
            else:
                result.add_fail("원두 데이터", f"{len(invalid_beans)}개 손상")
        except Exception as e:
            result.add_fail("원두 데이터 확인", str(e))

        # 블렌드 데이터
        try:
            blends = db.query(Blend).filter(Blend.status == "active").all()
            invalid_blends = [b for b in blends if not b.name or not b.blend_type]
            if not invalid_blends:
                result.add_pass(f"블렌드 데이터 무결성 ({len(blends)}개 정상)")
            else:
                result.add_fail("블렌드 데이터", f"{len(invalid_blends)}개 손상")
        except Exception as e:
            result.add_fail("블렌드 데이터 확인", str(e))

        # 재고 데이터
        try:
            inventory = db.query(Inventory).all()
            invalid_inv = [i for i in inventory if i.quantity_kg < 0]
            if not invalid_inv:
                result.add_pass(f"재고 데이터 무결성 ({len(inventory)}개 정상)")
            else:
                result.add_fail("재고 데이터", f"{len(invalid_inv)}개 음수")
        except Exception as e:
            result.add_fail("재고 데이터 확인", str(e))

        db.close()

    except Exception as e:
        result.add_fail("데이터 무결성 테스트", str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 6: 원가 계산 검증
# ═══════════════════════════════════════════════════════════════════════════════

def test_cost_calculation():
    """원가 계산 기능 검증"""
    print("\n🔍 Test 6: 원가 계산 검증")
    print("-" * 70)

    result = TestResult()

    try:
        from models import SessionLocal
        from services.blend_service import BlendService

        db = SessionLocal()
        blend_service = BlendService(db)

        blends = blend_service.get_active_blends()

        if not blends:
            result.add_fail("블렌드 조회", "활성 블렌드 없음")
            db.close()
            return result

        for blend in blends:
            try:
                cost_info = blend_service.calculate_blend_cost(blend.id)
                if cost_info and 'cost_per_portion' in cost_info:
                    if cost_info['cost_per_portion'] > 0:
                        result.add_pass(f"{blend.name} 원가 계산 (₩{cost_info['cost_per_portion']:,.0f})")
                    else:
                        result.add_fail(f"{blend.name} 원가", "원가가 0 이하")
                else:
                    result.add_fail(f"{blend.name} 원가", "계산 실패")
            except Exception as e:
                result.add_fail(f"{blend.name} 원가 계산", str(e))

        db.close()

    except Exception as e:
        result.add_fail("원가 계산 테스트", str(e))

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Test 7: 파일 크기 및 구조 확인
# ═══════════════════════════════════════════════════════════════════════════════

def test_project_structure():
    """프로젝트 구조 및 파일 크기 확인"""
    print("\n🔍 Test 7: 프로젝트 구조 확인")
    print("-" * 70)

    result = TestResult()

    # 주요 파일 확인
    files_to_check = {
        "app.py": "메인 앱",
        "models/__init__.py": "ORM 모델",
        "models/database.py": "데이터베이스",
        "services/bean_service.py": "원두 서비스",
        "services/blend_service.py": "블렌드 서비스",
        "services/report_service.py": "보고서 서비스",
        "services/excel_service.py": "Excel 서비스",
        "services/analytics_service.py": "분석 서비스",
        "utils/constants.py": "상수 정의"
    }

    app_dir = os.path.dirname(os.path.abspath(__file__))
    total_lines = 0

    for file_path, description in files_to_check.items():
        full_path = os.path.join(app_dir, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                result.add_pass(f"{description} ({lines} lines)")
            except Exception as e:
                result.add_fail(f"{file_path} 읽기", str(e))
        else:
            result.add_fail(f"{description}", f"{file_path} 없음")

    result.add_pass(f"총 코드: {total_lines:,} lines")

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# 메인 테스트 실행
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """모든 테스트 실행"""
    print("\n" + "="*70)
    print("🧪 통합 테스트 시작")
    print("="*70)
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    all_results = []

    # 각 테스트 실행
    all_results.append(test_imports())
    all_results.append(test_database())
    all_results.append(test_services())
    all_results.append(test_pages())
    all_results.append(test_data_integrity())
    all_results.append(test_cost_calculation())
    all_results.append(test_project_structure())

    # 최종 결과
    print("\n" + "="*70)
    print("📊 최종 테스트 결과")
    print("="*70)

    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed

    print(f"\n✅ 통과: {total_passed}")
    print(f"❌ 실패: {total_failed}")
    print(f"📊 총계: {total_tests}")

    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"🎯 성공률: {success_rate:.1f}%")

    print(f"\n완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if total_failed == 0:
        print("\n🎉 모든 테스트 통과! 애플리케이션은 정상입니다.")
        return 0
    else:
        print(f"\n⚠️ {total_failed}개의 테스트 실패. 위의 오류를 수정하세요.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
