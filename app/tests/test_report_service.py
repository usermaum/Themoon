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

    def test_export_to_excel_empty(self, db_session):
        """데이터 없을 때 Excel 내보내기"""
        service = ReportService(db_session)

        excel_data = service.export_to_excel(report_type='summary')

        assert isinstance(excel_data, BytesIO)
        # 에러 없이 생성되어야 함


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
