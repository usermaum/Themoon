"""
AnalyticsService 테스트

AnalyticsService의 주요 분석 기능을 테스트합니다:
- 월별 트렌드 분석
- 재고 예측
- ROI 분석
- 성능 지표
"""

import pytest
from datetime import datetime, timedelta
from app.services.analytics_service import AnalyticsService
from app.models.database import Transaction, Inventory


@pytest.fixture
def sample_transactions(db_session, sample_beans):
    """샘플 거래 데이터 생성"""
    transactions = []

    # 입고 거래
    for i in range(5):
        trans = Transaction(
            bean_id=sample_beans[0].id,
            transaction_type='입고',
            quantity_kg=10.0,
            price_per_unit=5500,
            total_amount=55000,
            created_at=datetime.now() - timedelta(days=30-i)
        )
        db_session.add(trans)
        transactions.append(trans)

    # 사용 거래
    for i in range(5):
        trans = Transaction(
            bean_id=sample_beans[0].id,
            transaction_type='사용',
            quantity_kg=2.0,
            price_per_unit=5500,
            total_amount=11000,
            created_at=datetime.now() - timedelta(days=20-i)
        )
        db_session.add(trans)
        transactions.append(trans)

    db_session.commit()

    for trans in transactions:
        db_session.refresh(trans)

    return transactions


@pytest.fixture
def sample_inventory(db_session, sample_beans):
    """샘플 재고 데이터"""
    inventories = []

    for bean in sample_beans:
        inv = Inventory(
            bean_id=bean.id,
            quantity_kg=20.0,
            min_quantity_kg=5.0,
            max_quantity_kg=50.0
        )
        db_session.add(inv)
        inventories.append(inv)

    db_session.commit()

    for inv in inventories:
        db_session.refresh(inv)

    return inventories


class TestAnalyticsServiceTrend:
    """트렌드 분석 테스트"""

    def test_get_monthly_trend(self, db_session, sample_transactions):
        """월별 거래 추이 분석"""
        service = AnalyticsService(db_session)

        trend_data = service.get_monthly_trend(months=3)

        assert isinstance(trend_data, list)
        assert len(trend_data) >= 1

        # 첫 번째 항목 구조 확인
        if trend_data:
            item = trend_data[0]
            assert 'period' in item
            assert 'month_name' in item
            assert 'inflow' in item
            assert 'outflow' in item
            assert 'net_change' in item

    def test_get_monthly_trend_empty(self, db_session):
        """거래 데이터 없을 때"""
        service = AnalyticsService(db_session)

        trend_data = service.get_monthly_trend(months=1)

        assert isinstance(trend_data, list)
        # 데이터가 없어도 기간은 반환됨
        assert len(trend_data) >= 1

        # 모든 값이 0이어야 함
        if trend_data:
            assert trend_data[0]['inflow'] == 0
            assert trend_data[0]['outflow'] == 0


class TestAnalyticsServiceProjection:
    """예측 분석 테스트"""

    def test_get_inventory_projection(self, db_session, sample_beans, sample_inventory, sample_transactions):
        """재고 예측"""
        service = AnalyticsService(db_session)

        projections = service.get_inventory_projection(days=30)

        assert isinstance(projections, list)
        assert len(projections) > 0

        # 첫 번째 항목 구조 확인
        proj = projections[0]
        assert 'bean_name' in proj
        assert 'current_quantity' in proj
        assert 'daily_usage' in proj
        assert 'projected_quantity' in proj

    def test_get_inventory_projection_no_usage(self, db_session, sample_beans, sample_inventory):
        """사용량 없을 때 재고 예측"""
        service = AnalyticsService(db_session)

        projections = service.get_inventory_projection(days=30)

        # 재고는 있지만 사용량이 없으면 daily_usage가 0
        if projections:
            assert all(p['daily_usage'] == 0 for p in projections)


class TestAnalyticsServiceROI:
    """ROI 분석 테스트"""

    def test_get_roi_analysis(self, db_session, sample_blend):
        """ROI 분석"""
        service = AnalyticsService(db_session)

        roi_data = service.get_roi_analysis()

        assert isinstance(roi_data, dict)
        assert 'roi_data' in roi_data
        assert 'average_roi' in roi_data

        # 블렌드가 있으면 ROI 데이터가 있어야 함
        if roi_data['roi_data']:
            item = roi_data['roi_data'][0]
            assert 'blend_name' in item
            assert 'total_cost' in item
            assert 'total_revenue' in item
            assert 'roi_percent' in item

    def test_get_roi_analysis_no_blends(self, db_session):
        """블렌드 없을 때 ROI 분석"""
        service = AnalyticsService(db_session)

        roi_data = service.get_roi_analysis()

        assert roi_data['average_roi'] == 0
        assert roi_data['best_roi'] is None
        assert roi_data['worst_roi'] is None


class TestAnalyticsServiceMetrics:
    """성능 지표 테스트"""

    def test_get_performance_metrics(self, db_session, sample_beans, sample_blend, sample_transactions):
        """성능 지표 조회"""
        service = AnalyticsService(db_session)

        metrics = service.get_performance_metrics()

        assert isinstance(metrics, dict)
        assert 'total_transactions' in metrics
        assert 'active_beans' in metrics
        assert 'active_blends' in metrics
        assert 'monthly_usage' in metrics
        assert 'monthly_revenue' in metrics

    def test_get_performance_metrics_empty(self, db_session):
        """데이터 없을 때 성능 지표"""
        service = AnalyticsService(db_session)

        metrics = service.get_performance_metrics()

        assert metrics['total_transactions'] == 0
        assert metrics['active_beans'] == 0
        assert metrics['monthly_usage'] == 0


class TestAnalyticsServiceForecast:
    """예측 테스트"""

    def test_get_usage_forecast(self, db_session, sample_transactions):
        """사용량 예측"""
        service = AnalyticsService(db_session)

        forecast_data = service.get_usage_forecast(days=30)

        assert isinstance(forecast_data, dict)
        assert 'avg_daily_usage' in forecast_data
        assert 'forecast' in forecast_data

        # 30일 예측
        assert len(forecast_data['forecast']) == 30

        # 첫 번째 항목 구조 확인
        if forecast_data['forecast']:
            item = forecast_data['forecast'][0]
            assert 'date' in item
            assert 'projected_usage' in item
            assert 'cumulative_usage' in item

    def test_get_usage_forecast_no_data(self, db_session):
        """거래 데이터 없을 때 예측"""
        service = AnalyticsService(db_session)

        forecast_data = service.get_usage_forecast(days=10)

        assert forecast_data['avg_daily_usage'] == 0
        assert len(forecast_data['forecast']) == 10


class TestAnalyticsServiceEfficiency:
    """효율성 분석 테스트"""

    def test_get_bean_efficiency(self, db_session, sample_beans, sample_transactions):
        """원두별 효율성 분석"""
        service = AnalyticsService(db_session)

        efficiency_data = service.get_bean_efficiency()

        assert isinstance(efficiency_data, dict)
        assert 'efficiency' in efficiency_data

        # 효율성 데이터 구조 확인
        if efficiency_data['efficiency']:
            item = efficiency_data['efficiency'][0]
            assert 'bean_name' in item
            assert 'price_per_kg' in item
            assert 'usage_count' in item
            assert 'usage_quantity' in item

    def test_get_bean_efficiency_no_usage(self, db_session, sample_beans):
        """사용량 없을 때 효율성 분석"""
        service = AnalyticsService(db_session)

        efficiency_data = service.get_bean_efficiency()

        # 원두는 있지만 사용량이 없으면 모두 0
        if efficiency_data['efficiency']:
            assert all(e['usage_count'] == 0 for e in efficiency_data['efficiency'])


class TestAnalyticsServiceComparison:
    """비교 분석 테스트"""

    def test_get_comparison_analysis(self, db_session, sample_blend):
        """블렌드 간 비교 분석"""
        service = AnalyticsService(db_session)

        comparison = service.get_comparison_analysis()

        assert isinstance(comparison, dict)
        assert 'comparison' in comparison

        # 비교 데이터 구조 확인
        if comparison['comparison']:
            item = comparison['comparison'][0]
            assert 'blend_name' in item
            assert 'cost_per_portion' in item
            assert 'selling_price' in item
            assert 'profit_rate' in item

    def test_get_comparison_analysis_no_blends(self, db_session):
        """블렌드 없을 때 비교 분석"""
        service = AnalyticsService(db_session)

        comparison = service.get_comparison_analysis()

        assert comparison['highest_profit'] is None
        assert comparison['highest_ratio'] is None
