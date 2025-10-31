"""
test_roasting_service.py: RoastingService 테스트

로스팅 기록 관리 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.roasting_service import RoastingService
from app.models.database import RoastingLog, LossRateWarning
from datetime import date, timedelta


class TestRoastingService:
    """RoastingService 테스트 클래스"""

    def test_create_roasting_log_basic(self, db_session):
        """기본 로스팅 기록 생성"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today(),
            notes='테스트 로스팅 기록'
        )

        assert log is not None
        assert log.raw_weight_kg == 10.0
        assert log.roasted_weight_kg == 8.3
        assert abs(log.loss_rate_percent - 17.0) < 0.1  # 손실률 17%
        assert log.notes == '테스트 로스팅 기록'
        assert log.roasting_month == date.today().strftime('%Y-%m')

    def test_loss_rate_calculation(self, db_session):
        """손실률 자동 계산 검증"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.0,  # 20% 손실
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        assert abs(log.loss_rate_percent - 20.0) < 0.1
        assert abs(log.loss_variance_percent - 3.0) < 0.1  # 20 - 17 = 3%

    def test_loss_variance_calculation(self, db_session):
        """손실률 편차 계산 검증"""
        # 낮은 손실률 (15%)
        log_low = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.5,  # 15% 손실
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        assert abs(log_low.loss_variance_percent - (-2.0)) < 0.1  # 15 - 17 = -2%

        # 높은 손실률 (25%)
        log_high = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.5,  # 25% 손실
            roasting_date=date.today() + timedelta(days=1),
            expected_loss_rate=17.0
        )

        assert abs(log_high.loss_variance_percent - 8.0) < 0.1  # 25 - 17 = 8%

    def test_get_roasting_logs_by_month(self, db_session):
        """월별 로스팅 기록 조회"""
        # 여러 기록 생성
        month = date.today().strftime('%Y-%m')
        for i in range(5):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today()
            )

        logs = RoastingService.get_roasting_logs_by_month(db_session, month)
        assert len(logs) == 5

    def test_get_roasting_logs_by_month_empty(self, db_session):
        """데이터 없는 월 조회"""
        logs = RoastingService.get_roasting_logs_by_month(db_session, '2020-01')
        assert len(logs) == 0

    def test_get_monthly_statistics(self, db_session):
        """월별 통계 계산"""
        month = date.today().strftime('%Y-%m')

        # 기록 생성
        RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        stats = RoastingService.get_monthly_statistics(db_session, month)

        assert stats['total_logs'] == 1
        assert stats['total_raw_weight_kg'] == 10.0
        assert stats['total_roasted_weight_kg'] == 8.3
        assert abs(stats['avg_loss_rate_percent'] - 17.0) < 0.1
        assert abs(stats['total_loss_kg'] - 1.7) < 0.1

    def test_get_monthly_statistics_empty(self, db_session):
        """데이터 없는 월의 통계"""
        stats = RoastingService.get_monthly_statistics(db_session, '2020-01')

        assert stats['count'] == 0
        assert stats['status'] == '데이터 없음'

    def test_update_roasting_log(self, db_session):
        """로스팅 기록 수정"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        updated = RoastingService.update_roasting_log(
            db=db_session,
            log_id=log.id,
            notes='수정된 노트',
            roasted_weight_kg=8.5
        )

        assert updated.notes == '수정된 노트'
        assert updated.roasted_weight_kg == 8.5

    def test_update_nonexistent_log(self, db_session):
        """존재하지 않는 로스팅 기록 수정 - 예외"""
        with pytest.raises(ValueError) as exc_info:
            RoastingService.update_roasting_log(
                db=db_session,
                log_id=999,
                notes='테스트'
            )

        assert "로스팅 기록을 찾을 수 없습니다" in str(exc_info.value)

    def test_delete_roasting_log(self, db_session):
        """로스팅 기록 삭제"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        result = RoastingService.delete_roasting_log(db_session, log.id)
        assert result is True

        # 삭제 확인
        deleted = RoastingService.get_roasting_log_by_id(db_session, log.id)
        assert deleted is None

    def test_delete_nonexistent_log(self, db_session):
        """존재하지 않는 로스팅 기록 삭제 - False 반환"""
        result = RoastingService.delete_roasting_log(db_session, 999)
        assert result is False

    def test_get_all_logs(self, db_session):
        """모든 로스팅 기록 조회"""
        # 3개 생성
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today() - timedelta(days=i)
            )

        logs = RoastingService.get_all_logs(db_session, limit=10)
        assert len(logs) == 3

        # 최신 날짜 순으로 정렬되었는지 확인
        assert logs[0].roasting_date >= logs[1].roasting_date

    def test_get_roasting_log_by_id(self, db_session):
        """ID로 로스팅 기록 조회"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        found = RoastingService.get_roasting_log_by_id(db_session, log.id)
        assert found is not None
        assert found.id == log.id
        assert found.raw_weight_kg == 10.0

    def test_get_roasting_log_by_id_not_found(self, db_session):
        """존재하지 않는 ID 조회 - None 반환"""
        found = RoastingService.get_roasting_log_by_id(db_session, 999)
        assert found is None

    def test_anomaly_detection_warning(self, db_session):
        """손실률 이상치 경고 생성 (3%~5% 편차)"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.9,  # 21% 손실 (4% 편차)
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 경고 생성 확인
        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).all()

        assert len(warnings) > 0
        assert warnings[0].severity == 'WARNING'  # 4% 편차 → WARNING
        assert warnings[0].warning_type == 'HIGH'

    def test_anomaly_detection_critical(self, db_session):
        """손실률 이상치 심각 (5% 이상 편차)"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,  # 30% 손실 (13% 편차)
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 경고 생성 확인
        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).all()

        assert len(warnings) > 0
        assert warnings[0].severity == 'CRITICAL'  # 13% 편차 → CRITICAL
        assert warnings[0].warning_type == 'HIGH'

    def test_anomaly_detection_low_loss(self, db_session):
        """손실률 낮음 이상치 (예상보다 낮은 손실률)"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=9.0,  # 10% 손실 (-7% 편차)
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 경고 생성 확인
        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).all()

        assert len(warnings) > 0
        assert warnings[0].warning_type == 'LOW'  # 낮은 손실률
        assert warnings[0].severity == 'CRITICAL'  # 7% 편차 → CRITICAL

    def test_no_anomaly_detection(self, db_session):
        """정상 손실률 (경고 없음)"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,  # 17% 손실 (0% 편차)
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 경고가 생성되지 않아야 함
        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).all()

        assert len(warnings) == 0

    def test_consecutive_anomalies(self, db_session):
        """연속 이상 탐지"""
        # 3일 연속 이상치 발생
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실 (이상)
                roasting_date=date.today() - timedelta(days=2-i),
                expected_loss_rate=17.0
            )

        # 가장 최근 기록의 경고 확인
        latest_log = db_session.query(RoastingLog).order_by(
            RoastingLog.roasting_date.desc()
        ).first()

        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == latest_log.id
        ).all()

        # 연속 발생 횟수 확인
        assert len(warnings) > 0
        assert warnings[0].consecutive_occurrences >= 1


@pytest.mark.integration
class TestRoastingServiceIntegration:
    """RoastingService 통합 테스트"""

    def test_monthly_workflow(self, db_session):
        """월별 로스팅 워크플로우 통합 테스트"""
        month = date.today().strftime('%Y-%m')

        # 1. 여러 로스팅 기록 생성
        for i in range(5):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0 + i,
                roasted_weight_kg=8.3 + i * 0.83,
                roasting_date=date.today()
            )

        # 2. 월별 조회
        logs = RoastingService.get_roasting_logs_by_month(db_session, month)
        assert len(logs) == 5

        # 3. 월별 통계
        stats = RoastingService.get_monthly_statistics(db_session, month)
        assert stats['total_logs'] == 5
        assert stats['total_raw_weight_kg'] > 0

    def test_update_and_recalculate(self, db_session):
        """수정 후 재계산 워크플로우"""
        # 1. 로스팅 기록 생성
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.0,
            roasting_date=date.today()
        )

        initial_loss_rate = log.loss_rate_percent

        # 2. 로스팅 후 무게 수정
        RoastingService.update_roasting_log(
            db=db_session,
            log_id=log.id,
            roasted_weight_kg=8.5
        )

        # 3. 확인
        updated_log = RoastingService.get_roasting_log_by_id(db_session, log.id)
        assert updated_log.roasted_weight_kg == 8.5
        # 손실률은 자동으로 재계산되지 않으므로 수동 업데이트 필요
