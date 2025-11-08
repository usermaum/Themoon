"""
test_loss_rate_analyzer.py: LossRateAnalyzer 테스트

손실률 이상 탐지 및 분석 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.loss_rate_analyzer import LossRateAnalyzer
from app.services.roasting_service import RoastingService
from app.models.database import RoastingLog, LossRateWarning
from datetime import date, timedelta


class TestLossRateAnalyzer:
    """LossRateAnalyzer 테스트 클래스"""

    def test_analyze_loss_rate_trend_normal(self, db_session):
        """트렌드 분석 - 정상 상태"""
        # 정상 범위의 로스팅 기록 생성 (손실률 16~18%)
        for i in range(10):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.2 + (i % 3) * 0.1,  # 16~18% 손실
                roasting_date=date.today() - timedelta(days=i)
            )

        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)

        assert trend['data_count'] == 10
        assert 'avg_loss_rate' in trend
        assert 'median_loss_rate' in trend
        assert 'std_deviation' in trend
        assert trend['status'] in ['NORMAL', 'ATTENTION']  # 정상 또는 주의

    def test_analyze_loss_rate_trend_no_data(self, db_session):
        """트렌드 분석 - 데이터 없음"""
        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)

        assert trend['data_count'] == 0
        assert trend['status'] == 'NO_DATA'

    def test_analyze_loss_rate_trend_critical(self, db_session):
        """트렌드 분석 - 심각 상태 (이상치 다수)"""
        # 이상치 많은 기록 생성
        for i in range(10):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실 (이상치)
                roasting_date=date.today() - timedelta(days=i),
                expected_loss_rate=17.0
            )

        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)

        assert trend['data_count'] == 10
        assert trend['anomalies_count'] >= 5
        assert trend['status'] == 'CRITICAL'

    def test_get_recent_warnings(self, db_session):
        """최근 미해결 경고 조회"""
        # 이상치 발생시켜 경고 생성
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실
                roasting_date=date.today() - timedelta(days=i),
                expected_loss_rate=17.0
            )

        warnings = LossRateAnalyzer.get_recent_warnings(db_session, limit=10)

        assert len(warnings) >= 3
        assert all('severity' in w for w in warnings)
        assert all('variance' in w for w in warnings)

    def test_get_recent_warnings_empty(self, db_session):
        """최근 경고 없음"""
        warnings = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(warnings) == 0

    def test_resolve_warning(self, db_session):
        """경고 해결 처리"""
        # 경고 생성
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 생성된 경고 확인
        warning = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).first()

        assert warning is not None
        assert warning.is_resolved is False

        # 경고 해결
        resolved = LossRateAnalyzer.resolve_warning(
            db=db_session,
            warning_id=warning.id,
            notes='문제 해결됨'
        )

        assert resolved.is_resolved is True
        assert resolved.resolution_notes == '문제 해결됨'
        assert resolved.resolved_at is not None

    def test_resolve_nonexistent_warning(self, db_session):
        """존재하지 않는 경고 해결 - 예외 발생"""
        with pytest.raises(ValueError) as exc_info:
            LossRateAnalyzer.resolve_warning(
                db=db_session,
                warning_id=999
            )

        assert "경고를 찾을 수 없습니다" in str(exc_info.value)

    def test_get_monthly_summary(self, db_session):
        """월별 요약"""
        month = date.today().strftime('%Y-%m')

        # 월별 기록 생성
        for i in range(5):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today()
            )

        summary = LossRateAnalyzer.get_monthly_summary(db_session, month)

        assert summary['data_count'] == 5
        assert 'avg_loss_rate' in summary
        assert 'std_deviation' in summary
        assert 'anomalies_count' in summary

    def test_get_monthly_summary_no_data(self, db_session):
        """월별 요약 - 데이터 없음"""
        summary = LossRateAnalyzer.get_monthly_summary(db_session, '2020-01')

        assert summary['data_count'] == 0
        assert summary['status'] == 'NO_DATA'

    def test_detect_continuous_anomalies(self, db_session):
        """연속 이상 탐지"""
        # 4일 연속 이상 발생
        for i in range(4):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실
                roasting_date=date.today() - timedelta(days=3-i),
                expected_loss_rate=17.0
            )

        anomalies = LossRateAnalyzer.detect_continuous_anomalies(
            db=db_session,
            threshold=2  # 2회 연속 이상
        )

        assert len(anomalies) > 0

    def test_detect_continuous_anomalies_none(self, db_session):
        """연속 이상 없음"""
        # 정상 기록만 생성
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,  # 17% 손실
                roasting_date=date.today() - timedelta(days=i)
            )

        anomalies = LossRateAnalyzer.detect_continuous_anomalies(
            db=db_session,
            threshold=3
        )

        assert len(anomalies) == 0

    def test_get_severity_distribution(self, db_session):
        """심각도별 분포"""
        # 다양한 심각도의 이상치 생성
        # WARNING 수준 (4% 편차)
        for i in range(2):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.9,  # 21% 손실 (4% 편차)
                roasting_date=date.today() - timedelta(days=i),
                expected_loss_rate=17.0
            )

        # CRITICAL 수준 (13% 편차)
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실 (13% 편차)
                roasting_date=date.today() - timedelta(days=i+10),
                expected_loss_rate=17.0
            )

        dist = LossRateAnalyzer.get_severity_distribution(db_session, days=30)

        assert 'severity_distribution' in dist
        assert 'WARNING' in dist['severity_distribution'] or 'CRITICAL' in dist['severity_distribution']
        assert dist['total_warnings'] >= 5

    def test_get_severity_distribution_no_warnings(self, db_session):
        """심각도별 분포 - 경고 없음"""
        # 정상 기록만 생성
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today() - timedelta(days=i)
            )

        dist = LossRateAnalyzer.get_severity_distribution(db_session, days=30)

        assert dist['total_warnings'] == 0
        assert dist['critical_ratio'] == 0

    def test_get_loss_rate_by_bean_normal(self, db_session):
        """원두별 손실률 분석 - 정상 케이스 (충분한 데이터)"""
        # Bean ID 1, 2, 3에 대해 각각 10개씩 로스팅 기록 생성
        from app.models.database import RoastingLog, Bean

        # Bean 레코드 먼저 생성
        bean1 = Bean(id=1, no=1, name="테스트원두A", roast_level="MEDIUM", price_per_kg=20000)
        bean2 = Bean(id=2, no=2, name="테스트원두B", roast_level="MEDIUM", price_per_kg=18000)
        bean3 = Bean(id=3, no=3, name="테스트원두C", roast_level="DARK", price_per_kg=15000)
        db_session.add_all([bean1, bean2, bean3])
        db_session.commit()

        # Bean 1: 평균 15% 손실률 (낮음)
        for i in range(10):
            log = RoastingLog(
                bean_id=1,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.5,  # 15% 손실
                loss_rate_percent=15.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=-2.0,
                roasting_date=date.today() - timedelta(days=i),
                roasting_month=date.today().strftime('%Y-%m')
            )
            db_session.add(log)

        # Bean 2: 평균 17% 손실률 (정상)
        for i in range(10):
            log = RoastingLog(
                bean_id=2,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,  # 17% 손실
                loss_rate_percent=17.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0,
                roasting_date=date.today() - timedelta(days=i),
                roasting_month=date.today().strftime('%Y-%m')
            )
            db_session.add(log)

        # Bean 3: 평균 20% 손실률 (높음)
        for i in range(10):
            log = RoastingLog(
                bean_id=3,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.0,  # 20% 손실
                loss_rate_percent=20.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=3.0,
                roasting_date=date.today() - timedelta(days=i),
                roasting_month=date.today().strftime('%Y-%m')
            )
            db_session.add(log)

        db_session.commit()

        # 분석 실행
        result = LossRateAnalyzer.get_loss_rate_by_bean(db_session, days=30)

        # 검증
        assert len(result) == 3  # 3개 원두
        assert all(isinstance(r, dict) for r in result)

        # 필드 검증
        required_fields = ['bean_id', 'bean_name', 'roast_count', 'avg_loss_rate',
                          'std_deviation', 'min_loss', 'max_loss',
                          'variance_from_global', 'status']
        for r in result:
            for field in required_fields:
                assert field in r

        # 데이터 검증 (손실률 높은 순으로 정렬됨)
        assert result[0]['avg_loss_rate'] == 20.0  # Bean 3
        assert result[1]['avg_loss_rate'] == 17.0  # Bean 2
        assert result[2]['avg_loss_rate'] == 15.0  # Bean 1

        # 상태 검증
        assert result[0]['status'] in ['ATTENTION', 'CRITICAL']  # 20% (높음)
        assert result[2]['status'] in ['NORMAL', 'ATTENTION']    # 15% (낮음)

    def test_get_loss_rate_by_bean_insufficient_data(self, db_session):
        """원두별 손실률 분석 - 데이터 부족 (원두당 1-2개 레코드)"""
        from app.models.database import RoastingLog, Bean

        # Bean 레코드 먼저 생성
        bean1 = Bean(id=1, no=1, name="테스트원두A", roast_level="MEDIUM", price_per_kg=20000)
        bean2 = Bean(id=2, no=2, name="테스트원두B", roast_level="MEDIUM", price_per_kg=18000)
        db_session.add_all([bean1, bean2])
        db_session.commit()

        # Bean 1: 1개 레코드 (표준편차 계산 불가)
        log = RoastingLog(
            bean_id=1,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            loss_rate_percent=17.0,
            expected_loss_rate_percent=17.0,
            loss_variance_percent=0.0,
            roasting_date=date.today(),
            roasting_month=date.today().strftime('%Y-%m')
        )
        db_session.add(log)

        # Bean 2: 2개 레코드 (최소 표준편차 계산 가능)
        for i in range(2):
            log = RoastingLog(
                bean_id=2,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3 if i == 0 else 8.2,
                loss_rate_percent=17.0 if i == 0 else 18.0,
                expected_loss_rate_percent=17.0,
                loss_variance_percent=0.0 if i == 0 else 1.0,
                roasting_date=date.today() - timedelta(days=i),
                roasting_month=date.today().strftime('%Y-%m')
            )
            db_session.add(log)

        db_session.commit()

        # 분석 실행
        result = LossRateAnalyzer.get_loss_rate_by_bean(db_session, days=30)

        # 검증
        assert len(result) == 2

        # Bean 1 (1개 레코드) - 표준편차 0
        bean1 = [r for r in result if r['roast_count'] == 1][0]
        assert bean1['std_deviation'] == 0.0

        # Bean 2 (2개 레코드) - 표준편차 계산됨
        bean2 = [r for r in result if r['roast_count'] == 2][0]
        assert bean2['std_deviation'] > 0.0

    def test_get_loss_rate_by_bean_no_data(self, db_session):
        """원두별 손실률 분석 - 데이터 없음"""
        # 데이터 없이 실행
        result = LossRateAnalyzer.get_loss_rate_by_bean(db_session, days=30)

        # 빈 리스트 반환
        assert result == []
        assert isinstance(result, list)


@pytest.mark.integration
class TestLossRateAnalyzerIntegration:
    """LossRateAnalyzer 통합 테스트"""

    def test_analysis_workflow(self, db_session):
        """분석 워크플로우 통합 테스트"""
        # 고정된 테스트 날짜 사용 (월 중간으로 설정하여 모든 데이터가 같은 달에 있도록 함)
        test_date = date(2025, 11, 15)

        # 1. 정상 + 이상 데이터 혼합 생성 (모두 같은 달에)
        for i in range(5):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,  # 정상
                roasting_date=test_date - timedelta(days=i)
            )

        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 이상
                roasting_date=test_date - timedelta(days=i+5),  # 같은 달 내에 생성
                expected_loss_rate=17.0
            )

        # 2. 트렌드 분석
        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)
        assert trend['data_count'] == 8
        assert trend['anomalies_count'] >= 3

        # 3. 경고 조회
        warnings = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(warnings) >= 3

        # 4. 월별 요약 (테스트 날짜 기준 달 사용)
        month = test_date.strftime('%Y-%m')
        summary = LossRateAnalyzer.get_monthly_summary(db_session, month)
        assert summary['data_count'] >= 5  # 8개 모두 같은 달(11월)에 있음

    def test_warning_lifecycle(self, db_session):
        """경고 생명주기 테스트"""
        # 1. 이상 발생 (경고 생성)
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 2. 경고 확인
        warning = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).first()
        assert warning is not None
        assert warning.is_resolved is False

        # 3. 경고 조회
        recent = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(recent) >= 1

        # 4. 경고 해결
        LossRateAnalyzer.resolve_warning(
            db=db_session,
            warning_id=warning.id,
            notes='조치 완료'
        )

        # 5. 해결 확인
        recent_after = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(recent_after) == 0  # 미해결 경고만 조회되므로 0
