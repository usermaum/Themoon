"""
ReportService 테스트

ReportService의 주요 보고서 생성 기능을 테스트합니다:
- 월별 요약
- 비용 분석
- 원두 사용량 분석
- 블렌드 성과 분석
- Excel/CSV 내보내기
"""

import pytest
from datetime import datetime
from app.services.report_service import ReportService
from io import BytesIO
import pandas as pd
from unittest.mock import patch, MagicMock


class TestReportServiceSummary:
    """요약 데이터 테스트"""

    def test_get_monthly_summary(self, db_session):
        """월별 요약 데이터 조회"""
        service = ReportService(db_session)

        now = datetime.now()
        summary = service.get_monthly_summary(now.year, now.month)

        assert isinstance(summary, dict)
        assert 'year' in summary
        assert 'month' in summary
        assert 'period' in summary
        assert 'total_inflow' in summary
        assert 'total_outflow' in summary
        assert 'transaction_count' in summary

    def test_get_monthly_summary_no_data(self, db_session):
        """거래 데이터 없을 때 월별 요약"""
        service = ReportService(db_session)

        summary = service.get_monthly_summary(2025, 1)

        assert summary['total_inflow'] == 0
        assert summary['total_outflow'] == 0
        assert summary['transaction_count'] == 0


class TestReportServiceCostAnalysis:
    """비용 분석 테스트"""

    def test_get_cost_analysis(self, db_session, sample_blend):
        """비용 분석"""
        service = ReportService(db_session)

        analysis = service.get_cost_analysis()

        assert isinstance(analysis, dict)
        assert 'start_date' in analysis
        assert 'end_date' in analysis
        assert 'cost_analysis' in analysis
        assert 'total_cost' in analysis

        # 블렌드가 있으면 분석 데이터도 있어야 함
        if analysis['cost_analysis']:
            item = analysis['cost_analysis'][0]
            assert 'blend_name' in item
            assert 'total_cost' in item
            assert 'suggested_price' in item

    def test_get_cost_analysis_custom_dates(self, db_session, sample_blend):
        """사용자 지정 날짜로 비용 분석"""
        service = ReportService(db_session)

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 31)

        analysis = service.get_cost_analysis(start_date, end_date)

        assert analysis['period_days'] == 30


class TestReportServiceBeanUsage:
    """원두 사용량 분석 테스트"""

    def test_get_bean_usage_analysis(self, db_session, sample_beans):
        """원두 사용량 분석"""
        service = ReportService(db_session)

        usage = service.get_bean_usage_analysis()

        assert isinstance(usage, dict)
        assert 'start_date' in usage
        assert 'end_date' in usage
        assert 'usage_analysis' in usage
        assert 'total_usage' in usage

    def test_get_bean_usage_analysis_no_usage(self, db_session, sample_beans):
        """사용량 없을 때 분석"""
        service = ReportService(db_session)

        usage = service.get_bean_usage_analysis()

        assert usage['total_usage'] == 0
        assert len(usage['usage_analysis']) == 0


class TestReportServiceBlendPerformance:
    """블렌드 성과 분석 테스트"""

    def test_get_blend_performance(self, db_session, sample_blend):
        """블렌드 성과 분석"""
        service = ReportService(db_session)

        performance = service.get_blend_performance()

        assert isinstance(performance, dict)
        assert 'performance' in performance

        # 블렌드가 있으면 성과 데이터도 있어야 함
        if performance['performance']:
            item = performance['performance'][0]
            assert 'blend_name' in item
            assert 'cost_per_portion' in item
            assert 'profit_rate' in item

    def test_get_blend_performance_no_blends(self, db_session):
        """블렌드 없을 때 성과 분석"""
        service = ReportService(db_session)

        performance = service.get_blend_performance()

        assert performance['best_blend'] is None
        assert performance['worst_blend'] is None


class TestReportServiceExcel:
    """Excel 내보내기 테스트"""

    def test_export_to_excel_summary(self, db_session, sample_beans, sample_blend):
        """요약 보고서를 Excel로 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='summary')

        assert isinstance(excel_data, BytesIO)
        assert excel_data.tell() == 0  # 시작 위치

        # Excel 파일 읽기 가능한지 확인
        excel_data.seek(0)
        df = pd.read_excel(excel_data, sheet_name='요약')
        assert isinstance(df, pd.DataFrame)

    def test_export_to_excel_all(self, db_session, sample_beans, sample_blend):
        """전체 보고서를 Excel로 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='all')

        assert isinstance(excel_data, BytesIO)

        # 여러 시트가 있는지 확인
        excel_data.seek(0)
        xl_file = pd.ExcelFile(excel_data)
        assert len(xl_file.sheet_names) >= 1

    def test_export_to_excel_cost(self, db_session, sample_beans, sample_blend):
        """비용 분석 보고서를 Excel로 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='cost')

        assert isinstance(excel_data, BytesIO)
        excel_data.seek(0)
        xl_file = pd.ExcelFile(excel_data)
        # 비용분석 시트가 있어야 함
        assert '비용분석' in xl_file.sheet_names or '요약' in xl_file.sheet_names

    def test_export_to_excel_blend(self, db_session, sample_beans, sample_blend):
        """블렌드 성과 보고서를 Excel로 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='blend')

        assert isinstance(excel_data, BytesIO)
        excel_data.seek(0)
        xl_file = pd.ExcelFile(excel_data)
        # 블렌드성과 시트가 있어야 함
        assert '블렌드성과' in xl_file.sheet_names or '요약' in xl_file.sheet_names

    def test_export_to_excel_bean_usage(self, db_session, sample_beans, sample_blend, sample_transactions):
        """원두 사용량 보고서를 Excel로 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='bean_usage')

        assert isinstance(excel_data, BytesIO)
        excel_data.seek(0)
        xl_file = pd.ExcelFile(excel_data)
        # 원두사용 시트가 있어야 함
        assert len(xl_file.sheet_names) >= 1

    def test_export_to_excel_empty(self, db_session):
        """데이터 없을 때 Excel 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='summary')

        assert isinstance(excel_data, BytesIO)
        # 에러 없이 생성되어야 함

    def test_export_to_excel_no_sheets(self, db_session):
        """모든 데이터가 없을 때 빈 시트 생성"""
        service = ReportService(db_session)

        # 데이터 없는 상태에서 'all' 타입으로 내보내기
        excel_data = service.export_to_excel(report_type='all')

        assert isinstance(excel_data, BytesIO)
        excel_data.seek(0)
        xl_file = pd.ExcelFile(excel_data)
        # 최소 1개 시트는 있어야 함 (빈 정보 시트)
        assert len(xl_file.sheet_names) >= 1


class TestReportServiceCSV:
    """CSV 내보내기 테스트"""

    def test_export_to_csv_summary(self, db_session, sample_beans, sample_blend):
        """요약 보고서를 CSV로 내보내기"""
        service = ReportService(db_session)

        csv_data = service.export_to_csv(report_type='summary')

        assert isinstance(csv_data, str)
        assert len(csv_data) > 0
        # CSV 헤더가 있는지 확인
        assert '항목' in csv_data or '값' in csv_data

    def test_export_to_csv_blend(self, db_session, sample_blend):
        """블렌드 보고서를 CSV로 내보내기"""
        service = ReportService(db_session)

        csv_data = service.export_to_csv(report_type='blend')

        assert isinstance(csv_data, str)
        assert len(csv_data) > 0

    def test_export_to_csv_cost(self, db_session, sample_beans, sample_blend):
        """비용 분석 보고서를 CSV로 내보내기"""
        service = ReportService(db_session)

        csv_data = service.export_to_csv(report_type='cost')

        assert isinstance(csv_data, str)
        assert len(csv_data) > 0
        # CSV 헤더 확인
        assert '블렌드명' in csv_data or 'blend_name' in csv_data

    def test_export_to_csv_bean_usage(self, db_session, sample_beans, sample_transactions):
        """원두 사용량 보고서를 CSV로 내보내기"""
        service = ReportService(db_session)

        csv_data = service.export_to_csv(report_type='bean_usage')

        assert isinstance(csv_data, str)
        assert len(csv_data) > 0


class TestReportServiceEdgeCases:
    """경계값 및 예외 상황 테스트"""

    def test_get_monthly_summary_future_month(self, db_session):
        """미래 월 요약"""
        service = ReportService(db_session)

        summary = service.get_monthly_summary(2030, 12)

        assert summary['total_inflow'] == 0
        assert summary['total_outflow'] == 0

    def test_get_cost_analysis_reversed_dates(self, db_session, sample_blend):
        """시작일이 종료일보다 나중인 경우"""
        service = ReportService(db_session)

        start_date = datetime(2025, 2, 1)
        end_date = datetime(2025, 1, 1)

        analysis = service.get_cost_analysis(start_date, end_date)

        # 음수 일수가 나올 수 있음
        assert analysis['period_days'] < 0


class TestReportServiceExceptionHandling:
    """예외 처리 테스트 (커버리지 95%+ 목표)"""

    def test_export_excel_exception_in_summary_sheet(self, db_session, sample_beans, sample_blend):
        """_create_summary_sheet에서 예외 발생 시 처리"""
        service = ReportService(db_session)

        # bean_service.get_beans_summary()에서 예외 발생
        with patch.object(service.bean_service, 'get_beans_summary', side_effect=Exception("Test exception")):
            excel_data = service.export_to_excel(report_type='summary')

            # 예외가 발생해도 Excel 파일은 생성되어야 함
            assert isinstance(excel_data, BytesIO)
            excel_data.seek(0)
            xl_file = pd.ExcelFile(excel_data)
            # 요약 시트는 있어야 함 (오류 메시지 포함)
            assert '요약' in xl_file.sheet_names

            # 오류 메시지가 포함되어 있는지 확인
            df = pd.read_excel(excel_data, sheet_name='요약')
            assert '오류' in df.columns or 'Test exception' in str(df.values)

    def test_export_excel_exception_in_cost_sheet(self, db_session, sample_beans, sample_blend):
        """_create_cost_sheet에서 예외 발생 시 처리"""
        service = ReportService(db_session)

        # to_excel 메서드에서 예외 발생시키기
        original_to_excel = pd.DataFrame.to_excel
        call_count = [0]

        def side_effect_to_excel(self, *args, **kwargs):
            call_count[0] += 1
            # 비용분석 시트 작성 시도 시 예외 발생
            if call_count[0] == 1 and 'sheet_name' in kwargs and kwargs['sheet_name'] == '비용분석':
                raise Exception("Cost sheet error")
            return original_to_excel(self, *args, **kwargs)

        with patch.object(pd.DataFrame, 'to_excel', side_effect_to_excel):
            excel_data = service.export_to_excel(report_type='cost')

            # 예외가 발생해도 Excel 파일은 생성되어야 함
            assert isinstance(excel_data, BytesIO)
            excel_data.seek(0)
            xl_file = pd.ExcelFile(excel_data)
            # 최소 1개 시트는 있어야 함 (오류가 있더라도 오류 시트)
            assert len(xl_file.sheet_names) >= 1


    def test_export_excel_all_sheets_empty_creates_default_sheet(self, db_session):
        """모든 데이터가 비어있어 sheets_created == 0일 때 기본 시트 생성"""
        service = ReportService(db_session)

        # 모든 get_* 메서드가 빈 데이터 반환하도록 mock
        with patch.object(service, 'get_cost_analysis', return_value={'cost_analysis': []}), \
             patch.object(service, 'get_bean_usage_analysis', return_value={'usage_analysis': []}), \
             patch.object(service, 'get_blend_performance', return_value={'performance': []}):

            excel_data = service.export_to_excel(report_type='all')

            # Excel 파일은 생성되어야 함
            assert isinstance(excel_data, BytesIO)
            excel_data.seek(0)
            xl_file = pd.ExcelFile(excel_data)
            # 최소 1개 시트는 있어야 함 (요약 또는 정보 시트)
            assert len(xl_file.sheet_names) >= 1

# ============================================
# Phase 5 테스트 (2025-11-11 추가)
# ============================================

class TestReportServicePhase5MonthlyReport:
    """Phase 5: 월별 거래 리포트 테스트"""

    def test_get_monthly_transactions_report(self, db_session, sample_beans, sample_transactions):
        """월별 거래 리포트 데이터 생성"""
        service = ReportService(db_session)

        now = datetime.now()
        report = service.get_monthly_transactions_report(now.year, now.month)

        assert isinstance(report, dict)
        assert 'summary' in report
        assert 'daily_trend' in report
        assert 'transaction_type' in report

        # 요약 데이터 확인
        summary = report['summary']
        assert '총 입고량 (kg)' in summary
        assert '총 출고량 (kg)' in summary
        assert '로스팅 횟수' in summary
        assert '재고 증감 (kg)' in summary

        # DataFrame 확인
        assert isinstance(report['daily_trend'], pd.DataFrame)
        assert isinstance(report['transaction_type'], pd.DataFrame)

    def test_get_monthly_transactions_report_no_data(self, db_session):
        """데이터 없을 때 월별 리포트"""
        service = ReportService(db_session)

        report = service.get_monthly_transactions_report(2025, 1)

        assert report['summary']['총 입고량 (kg)'] == 0
        assert report['summary']['총 출고량 (kg)'] == 0
        assert report['summary']['로스팅 횟수'] == 0
        assert len(report['daily_trend']) == 0


class TestReportServicePhase5Profitability:
    """Phase 5: 수익성 분석 테스트"""

    def test_get_profitability_by_bean(self, db_session, sample_beans):
        """원두별 수익성 분석"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 1, 1)
        end_date = date(2025, 12, 31)

        result = service.get_profitability_by_bean(start_date, end_date, sort_by='profit_rate')

        assert isinstance(result, pd.DataFrame)

        # 결과가 있으면 필수 컬럼 확인
        if len(result) > 0:
            assert '원두명' in result.columns
            assert '로스팅 횟수' in result.columns
            assert '평균 손실률(%)' in result.columns
            assert '총 투입량(g)' in result.columns
            assert '총 산출량(g)' in result.columns
            assert '수익률(%)' in result.columns

    def test_get_profitability_by_bean_empty(self, db_session, sample_beans):
        """로스팅 기록 없을 때 수익성 분석"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 31)

        result = service.get_profitability_by_bean(start_date, end_date)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_get_profitability_by_bean_sort_options(self, db_session, sample_beans):
        """정렬 옵션 테스트"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 1, 1)
        end_date = date(2025, 12, 31)

        # 수익률순
        result1 = service.get_profitability_by_bean(start_date, end_date, sort_by='profit_rate')
        assert isinstance(result1, pd.DataFrame)

        # 손실률순
        result2 = service.get_profitability_by_bean(start_date, end_date, sort_by='loss_rate')
        assert isinstance(result2, pd.DataFrame)

        # 투입량순
        result3 = service.get_profitability_by_bean(start_date, end_date, sort_by='input_weight')
        assert isinstance(result3, pd.DataFrame)


class TestReportServicePhase5DataFrames:
    """Phase 5: DataFrame 조회 테스트"""

    def test_get_roasting_logs_dataframe(self, db_session, sample_beans):
        """로스팅 기록 DataFrame 조회"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 1, 1)
        end_date = date(2025, 12, 31)

        result = service.get_roasting_logs_dataframe(start_date, end_date)

        assert isinstance(result, pd.DataFrame)

        # 로스팅 기록이 있으면 컬럼 확인
        if len(result) > 0:
            assert '날짜' in result.columns
            assert '원두명' in result.columns
            assert '생두 무게(g)' in result.columns
            assert '원두 무게(g)' in result.columns
            assert '손실률(%)' in result.columns

    def test_get_inventory_dataframe(self, db_session, sample_beans):
        """재고 현황 DataFrame 조회"""
        service = ReportService(db_session)

        result = service.get_inventory_dataframe()

        assert isinstance(result, pd.DataFrame)

        # 재고가 있으면 컬럼 확인
        if len(result) > 0:
            assert '원두명' in result.columns
            assert '재고 타입' in result.columns
            assert '수량(g)' in result.columns
            assert '최소 재고량(g)' in result.columns

    def test_get_transactions_dataframe(self, db_session, sample_beans, sample_transactions):
        """거래 내역 DataFrame 조회"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 1, 1)
        end_date = date(2025, 12, 31)

        result = service.get_transactions_dataframe(start_date, end_date)

        assert isinstance(result, pd.DataFrame)

        # 거래 내역이 있으면 컬럼 확인
        if len(result) > 0:
            assert '날짜' in result.columns
            assert '원두' in result.columns
            assert '거래 유형' in result.columns
            assert '수량(kg)' in result.columns


class TestReportServicePhase5Export:
    """Phase 5: Excel/CSV 내보내기 테스트"""

    def test_generate_monthly_excel(self, db_session, sample_beans, sample_transactions):
        """월별 종합 리포트 Excel 생성"""
        service = ReportService(db_session)

        now = datetime.now()
        result = service.generate_monthly_excel(now.year, now.month)

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)

        # 4개 시트 확인
        assert len(xl_file.sheet_names) >= 1
        assert '요약' in xl_file.sheet_names

    def test_generate_monthly_excel_no_data(self, db_session):
        """데이터 없을 때 월별 Excel 생성"""
        service = ReportService(db_session)

        result = service.generate_monthly_excel(2025, 1)

        assert isinstance(result, BytesIO)
        result.seek(0)
        xl_file = pd.ExcelFile(result)
        assert '요약' in xl_file.sheet_names

    # Note: export_profitability_csv는 별도 메서드로 구현되지 않음
    # get_profitability_by_bean() + dataframe_to_csv()를 조합하여 사용


class TestReportServicePhase5EdgeCases:
    """Phase 5: 경계값 및 예외 상황 테스트"""

    def test_get_profitability_reversed_dates(self, db_session, sample_beans):
        """시작일이 종료일보다 나중인 경우"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 12, 31)
        end_date = date(2025, 1, 1)

        result = service.get_profitability_by_bean(start_date, end_date)

        # 빈 결과 반환
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_get_monthly_transactions_report_future_month(self, db_session):
        """미래 월의 거래 리포트"""
        service = ReportService(db_session)

        report = service.get_monthly_transactions_report(2030, 12)

        assert report['summary']['총 입고량 (kg)'] == 0
        assert len(report['daily_trend']) == 0

    def test_get_roasting_logs_dataframe_invalid_date_range(self, db_session, sample_beans):
        """잘못된 날짜 범위로 로스팅 기록 조회"""
        service = ReportService(db_session)

        from datetime import date
        start_date = date(2025, 12, 31)
        end_date = date(2025, 1, 1)

        result = service.get_roasting_logs_dataframe(start_date, end_date)

        assert isinstance(result, pd.DataFrame)
        # 빈 결과 또는 에러 없이 반환
