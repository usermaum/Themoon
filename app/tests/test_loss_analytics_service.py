"""
test_loss_analytics_service.py: LossAnalyticsService 테스트

손실률 예측 및 계절성 분석 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.loss_analytics_service import LossAnalyticsService
from app.models.database import RoastingLog
from datetime import date, timedelta


class TestLossAnalyticsService:
    """LossAnalyticsService 테스트 클래스"""

    def test_calculate_seasonal_index_normal(self, db_session):
        """계절 지수 계산 - 정상 케이스"""
        # 1월과 7월 데이터 생성 (계절성 차이)
        # 1월: 낮은 손실률 (15%)
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.5,  # 15% 손실
                loss_rate_percent=15.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=-2.0,
                roasting_date=date(2024, 1, 10 + i),
                roasting_month="2024-01"
            )
            db_session.add(log)

        # 7월: 높은 손실률 (20%)
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.0,  # 20% 손실
                loss_rate_percent=20.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=3.0,
                roasting_date=date(2024, 7, 10 + i),
                roasting_month="2024-07"
            )
            db_session.add(log)

        db_session.commit()

        # 계절 지수 계산
        seasonal_index = LossAnalyticsService.calculate_seasonal_index(db_session)

        # 검증
        assert '01' in seasonal_index
        assert '07' in seasonal_index

        # 1월은 평균보다 낮아야 함 (계절 지수 < 1.0)
        assert seasonal_index['01'] < 1.0

        # 7월은 평균보다 높아야 함 (계절 지수 > 1.0)
        assert seasonal_index['07'] > 1.0

        # 전체 평균 = (15*10 + 20*10) / 20 = 17.5
        # 1월 지수 = 15 / 17.5 ≈ 0.857
        assert 0.85 <= seasonal_index['01'] <= 0.87

        # 7월 지수 = 20 / 17.5 ≈ 1.143
        assert 1.14 <= seasonal_index['07'] <= 1.15

    def test_calculate_seasonal_index_no_data(self, db_session):
        """계절 지수 계산 - 데이터 없음"""
        seasonal_index = LossAnalyticsService.calculate_seasonal_index(db_session)

        # 빈 dict 반환
        assert seasonal_index == {}

    def test_predict_loss_rate_summer(self, db_session):
        """손실률 예측 - 여름철 (높은 손실률)"""
        # 테스트 데이터 준비 (최근 30개)
        # 평균 17% 손실률로 30개 생성
        for i in range(30):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=29-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        # 7월 계절 지수 설정 (1.15)
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.0,
                loss_rate_percent=19.5,  # 17 * 1.15
                expected_loss_rate_percent=17.0,
                loss_variance_percent=2.5,
                roasting_date=date(2024, 7, 10 + i),
                roasting_month="2024-07"
            )
            db_session.add(log)

        db_session.commit()

        # 계절 지수 먼저 계산
        LossAnalyticsService.calculate_seasonal_index(db_session)

        # 7월(months_ahead에 맞춰 조정 필요) 예측
        # 현재 월을 고려하여 months_ahead 계산
        current_month = date.today().month
        months_to_july = (7 - current_month) % 12
        if months_to_july == 0:
            months_to_july = 12  # 다음 해 7월

        prediction = LossAnalyticsService.predict_loss_rate(
            db_session,
            bean_id=1,
            months_ahead=months_to_july
        )

        # 검증
        assert prediction['bean_id'] == 1
        assert prediction['current_avg_loss_rate'] == 17.0
        assert 'predicted_loss_rate' in prediction
        assert 'confidence_interval_lower' in prediction
        assert 'confidence_interval_upper' in prediction
        assert prediction['model_type'] == 'moving_average_with_seasonality'
        assert prediction['data_points_used'] == 30

        # 예측값이 현재 평균보다 높아야 함 (계절 지수 > 1.0)
        assert prediction['predicted_loss_rate'] > prediction['current_avg_loss_rate']

    def test_predict_loss_rate_winter(self, db_session):
        """손실률 예측 - 겨울철 (낮은 손실률)"""
        # 테스트 데이터 준비
        for i in range(30):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=29-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        # 1월 계절 지수 설정 (0.88)
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.5,
                loss_rate_percent=15.0,  # 17 * 0.88
                expected_loss_rate_percent=17.0,
                loss_variance_percent=-2.0,
                roasting_date=date(2024, 1, 10 + i),
                roasting_month="2024-01"
            )
            db_session.add(log)

        db_session.commit()

        # 계절 지수 계산
        LossAnalyticsService.calculate_seasonal_index(db_session)

        # 1월 예측
        current_month = date.today().month
        months_to_january = (1 - current_month) % 12
        if months_to_january == 0:
            months_to_january = 12  # 다음 해 1월

        prediction = LossAnalyticsService.predict_loss_rate(
            db_session,
            bean_id=1,
            months_ahead=months_to_january
        )

        # 검증
        assert prediction['bean_id'] == 1
        assert 'predicted_loss_rate' in prediction

        # 예측값이 현재 평균보다 낮아야 함 (계절 지수 < 1.0)
        assert prediction['predicted_loss_rate'] < prediction['current_avg_loss_rate']

    def test_predict_loss_rate_insufficient_data(self, db_session):
        """손실률 예측 - 데이터 부족 (예외 발생)"""
        # 데이터 3개만 생성 (최소 5개 필요)
        for i in range(3):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=2-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        db_session.commit()

        # 예외 발생 확인
        with pytest.raises(ValueError) as exc_info:
            LossAnalyticsService.predict_loss_rate(db_session, bean_id=1)

        assert "데이터가 부족합니다" in str(exc_info.value)

    def test_confidence_interval_coverage(self, db_session):
        """신뢰구간 포함 여부 검증"""
        # 평균 17%, 표준편차 1.5%로 30개 데이터 생성
        import random
        random.seed(42)

        for i in range(30):
            loss_rate = 17.0 + random.gauss(0, 1.5)
            loss_rate = max(10.0, min(25.0, loss_rate))  # 10~25% 제한
            roasted_weight = 10.0 * (1 - loss_rate / 100)

            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=round(roasted_weight, 2),
                loss_rate_percent=round(loss_rate, 2),
                expected_loss_rate_percent=17.0,
                loss_variance_percent=round(loss_rate - 17.0, 2),
                roasting_date=date.today() - timedelta(days=29-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        # 계절 지수용 데이터
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date(2024, 6, 10 + i),
                roasting_month="2024-06"
            )
            db_session.add(log)

        db_session.commit()

        # 계절 지수 계산
        LossAnalyticsService.calculate_seasonal_index(db_session)

        # 예측
        prediction = LossAnalyticsService.predict_loss_rate(db_session, bean_id=1)

        # 신뢰구간 검증
        assert prediction['confidence_interval_lower'] < prediction['predicted_loss_rate']
        assert prediction['predicted_loss_rate'] < prediction['confidence_interval_upper']

        # 신뢰구간 범위 검증 (95% CI = ±2σ)
        # 범위가 합리적인지 확인 (너무 좁거나 넓지 않은지)
        ci_width = (
            prediction['confidence_interval_upper'] -
            prediction['confidence_interval_lower']
        )
        assert 2.0 < ci_width < 10.0  # 2% ~ 10% 범위

    def test_get_monthly_forecast(self, db_session):
        """3개월 예측"""
        # 테스트 데이터 준비
        for i in range(30):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=29-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        # 계절 지수용 월별 데이터
        for month in range(1, 13):
            for i in range(3):
                log = RoastingLog(
                    bean_id=1,
                    raw_weight_kg=10.0,
                    roasted_weight_kg=8.3,
                    loss_rate_percent=17.0,
                    expected_loss_rate_percent=17.0,
                    loss_variance_percent=0.0,
                    roasting_date=date(2024, month, 1 + i),
                    roasting_month=f"2024-{month:02d}"
                )
                db_session.add(log)

        db_session.commit()

        # 3개월 예측
        forecasts = LossAnalyticsService.get_monthly_forecast(db_session, months=3)

        # 검증
        assert len(forecasts) == 3
        assert all('predicted_loss_rate' in f for f in forecasts)
        assert all('prediction_month' in f for f in forecasts)

    def test_cache_functionality(self, db_session):
        """캐시 기능 검증"""
        # 데이터 생성
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=9-i),
                roasting_month=date.today().strftime("%Y-%m")
            )
            db_session.add(log)

        db_session.commit()

        # 캐시 초기화
        LossAnalyticsService.clear_cache()
        assert LossAnalyticsService._seasonal_index_cache is None

        # 첫 번째 호출 (캐시 생성)
        index1 = LossAnalyticsService.get_seasonal_index(db_session)
        assert LossAnalyticsService._seasonal_index_cache is not None

        # 두 번째 호출 (캐시 사용)
        index2 = LossAnalyticsService.get_seasonal_index(db_session)
        assert index1 == index2

        # 강제 갱신
        index3 = LossAnalyticsService.get_seasonal_index(db_session, force_refresh=True)
        assert index3 == index1  # 데이터가 같으므로 결과 동일

        # 캐시 초기화
        LossAnalyticsService.clear_cache()
        assert LossAnalyticsService._seasonal_index_cache is None
