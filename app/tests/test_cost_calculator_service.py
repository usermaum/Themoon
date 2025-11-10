"""
CostCalculatorService 단위 테스트
원가계산기 고도화 - Phase 2: 투입량 계산기
"""

import pytest
from datetime import date
from app.services.cost_calculator_service import CostCalculatorService
from app.models.database import Bean, RoastingLog


class TestCostCalculatorService:
    """CostCalculatorService 테스트"""

    def test_get_bean_statistics_with_data(self, db_session, sample_bean_with_logs):
        """원두 통계 조회 테스트 (데이터 있음)"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        stats = service.get_bean_statistics(bean.id)

        assert 'error' not in stats
        assert stats['bean_id'] == bean.id
        assert stats['bean_name'] == bean.name
        assert stats['avg_loss_rate'] == 17.0  # 테스트 데이터
        assert stats['std_loss_rate'] == 1.0
        assert stats['sample_count'] == 3

    def test_get_bean_statistics_without_data(self, db_session, sample_bean):
        """원두 통계 조회 테스트 (데이터 없음)"""
        service = CostCalculatorService(db_session)

        stats = service.get_bean_statistics(sample_bean.id)

        assert 'error' not in stats
        assert stats['avg_loss_rate'] == 17.0  # 기본값
        assert stats['std_loss_rate'] == 2.0
        assert stats['sample_count'] == 0
        assert 'warning' in stats

    def test_get_bean_statistics_all_average(self, db_session, sample_bean_with_logs):
        """전체 평균 통계 조회 테스트"""
        service = CostCalculatorService(db_session)

        stats = service.get_bean_statistics(None)  # None = 전체 평균

        assert 'error' not in stats
        assert stats['bean_name'] == '전체 평균'
        assert 'avg_loss_rate' in stats
        assert 'sample_count' in stats

    def test_calculate_required_input_basic(self, db_session, sample_bean_with_logs):
        """투입량 계산 (기본) 테스트"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        result = service.calculate_required_input(
            target_output_kg=10.0,
            bean_id=bean.id,
            safety_margin=0.02  # 2%
        )

        assert 'error' not in result
        assert result['target_output'] == 10.0
        assert result['bean_id'] == bean.id
        assert result['avg_loss_rate'] == 17.0

        # 계산 검증: 10 / (1 - 0.17) = 12.048
        expected_calculated = 10.0 / (1 - 0.17)
        assert abs(result['calculated_input'] - expected_calculated) < 0.01

        # 권장 투입량: 12.048 * 1.02 = 12.289
        expected_recommended = expected_calculated * 1.02
        assert abs(result['recommended_input'] - expected_recommended) < 0.01

    def test_calculate_required_input_different_safety_margin(self, db_session, sample_bean_with_logs):
        """투입량 계산 (여유율 변경) 테스트"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        # 여유율 5%
        result = service.calculate_required_input(
            target_output_kg=10.0,
            bean_id=bean.id,
            safety_margin=0.05  # 5%
        )

        assert 'error' not in result
        calculated = result['calculated_input']
        recommended = result['recommended_input']

        # 권장량이 기본량보다 5% 많아야 함
        assert abs(recommended - calculated * 1.05) < 0.01

    def test_calculate_required_input_with_all_average(self, db_session, sample_bean_with_logs):
        """투입량 계산 (전체 평균 사용) 테스트"""
        service = CostCalculatorService(db_session)

        result = service.calculate_required_input(
            target_output_kg=10.0,
            bean_id=None,  # 전체 평균
            safety_margin=0.02
        )

        assert 'error' not in result
        assert result['bean_name'] == '전체 평균'
        assert 'calculated_input' in result
        assert 'recommended_input' in result

    def test_calculate_required_input_output_range(self, db_session, sample_bean_with_logs):
        """투입량 계산 - 예상 산출량 범위 검증"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        result = service.calculate_required_input(
            target_output_kg=10.0,
            bean_id=bean.id,
            safety_margin=0.02
        )

        # 예상 범위 검증
        assert 'min_output' in result
        assert 'expected_output' in result
        assert 'max_output' in result

        # min < expected < max
        assert result['min_output'] < result['expected_output']
        assert result['expected_output'] < result['max_output']

        # expected_output이 target_output에 가까워야 함
        assert abs(result['expected_output'] - 10.0) < 1.0

    def test_predict_output_basic(self, db_session, sample_bean_with_logs):
        """산출량 예측 테스트"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        result = service.predict_output(
            input_weight_kg=12.0,
            bean_id=bean.id
        )

        assert 'error' not in result
        assert result['input_weight'] == 12.0
        assert result['bean_id'] == bean.id

        # 예상 산출량: 12 * (1 - 0.17) = 9.96
        expected_output = 12.0 * (1 - 0.17)
        assert abs(result['expected_output'] - expected_output) < 0.01

    def test_predict_output_range(self, db_session, sample_bean_with_logs):
        """산출량 예측 - 범위 검증"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        result = service.predict_output(
            input_weight_kg=12.0,
            bean_id=bean.id
        )

        # 범위 검증
        assert result['min_output'] < result['expected_output']
        assert result['expected_output'] < result['max_output']

        # 손실량 검증
        assert result['min_loss_kg'] < result['expected_loss_kg']
        assert result['expected_loss_kg'] < result['max_loss_kg']

        # 산출량 + 손실량 = 투입량
        assert abs((result['expected_output'] + result['expected_loss_kg']) - 12.0) < 0.01

    def test_update_bean_statistics(self, db_session, sample_bean):
        """원두 통계 업데이트 테스트"""
        service = CostCalculatorService(db_session)

        # 로스팅 기록 생성
        logs = [
            RoastingLog(
                bean_id=sample_bean.id,
                raw_weight_kg=12.0,
                roasted_weight_kg=10.0,
                loss_rate_percent=16.67,
                roasting_date=date.today()
            ),
            RoastingLog(
                bean_id=sample_bean.id,
                raw_weight_kg=12.0,
                roasted_weight_kg=9.8,
                loss_rate_percent=18.33,
                roasting_date=date.today()
            ),
            RoastingLog(
                bean_id=sample_bean.id,
                raw_weight_kg=12.0,
                roasted_weight_kg=10.2,
                loss_rate_percent=15.0,
                roasting_date=date.today()
            )
        ]
        for log in logs:
            db_session.add(log)
        db_session.commit()

        # 통계 업데이트
        success = service.update_bean_statistics(sample_bean.id)
        assert success is True

        # Bean 조회
        db_session.refresh(sample_bean)

        # 평균 손실률: (16.67 + 18.33 + 15.0) / 3 = 16.67
        expected_avg = (16.67 + 18.33 + 15.0) / 3
        assert abs(sample_bean.avg_loss_rate - expected_avg) < 0.1

        assert sample_bean.total_roasted_count == 3
        assert sample_bean.last_roasted_date == date.today()

    def test_update_bean_statistics_no_data(self, db_session, sample_bean):
        """원두 통계 업데이트 (데이터 없음) 테스트"""
        service = CostCalculatorService(db_session)

        # 로스팅 기록 없이 업데이트
        success = service.update_bean_statistics(sample_bean.id)
        assert success is True

        # Bean 조회
        db_session.refresh(sample_bean)

        # 통계가 None이어야 함
        assert sample_bean.avg_loss_rate is None
        assert sample_bean.total_roasted_count == 0

    def test_calculate_cost_with_loss(self, db_session, sample_bean_with_logs):
        """원가 계산 (손실률 포함) 테스트"""
        service = CostCalculatorService(db_session)
        bean = sample_bean_with_logs

        result = service.calculate_cost(
            bean_id=bean.id,
            quantity_kg=10.0,
            include_loss=True
        )

        assert 'error' not in result
        assert result['bean_id'] == bean.id
        assert result['quantity_kg'] == 10.0

        # 손실률 포함 원가 계산
        # 필요한 생두: 10 / (1 - 0.17) = 12.048kg
        # 원가: 12.048 * 30000 = 361,440원
        expected_raw_needed = 10.0 / (1 - 0.17)
        expected_cost = expected_raw_needed * bean.price_per_kg

        assert abs(result['raw_bean_needed'] - expected_raw_needed) < 0.1
        assert abs(result['raw_bean_cost'] - expected_cost) < 100

    def test_calculate_cost_without_loss(self, db_session, sample_bean):
        """원가 계산 (손실률 제외) 테스트"""
        service = CostCalculatorService(db_session)

        result = service.calculate_cost(
            bean_id=sample_bean.id,
            quantity_kg=10.0,
            include_loss=False
        )

        assert 'error' not in result
        assert result['quantity_kg'] == 10.0

        # 손실률 제외 원가: 10 * 30000 = 300,000원
        expected_cost = 10.0 * sample_bean.price_per_kg
        assert result['roasted_bean_cost'] == expected_cost


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def sample_bean(db_session):
    """테스트용 원두 생성"""
    bean = Bean(
        no=99,
        name="테스트 원두",
        country_name="테스트 국가",
        roast_level="MEDIUM",
        price_per_kg=30000.0,
        status="active"
    )
    db_session.add(bean)
    db_session.commit()
    db_session.refresh(bean)
    return bean


@pytest.fixture
def sample_bean_with_logs(db_session):
    """로스팅 기록이 있는 테스트용 원두 생성"""
    bean = Bean(
        no=98,
        name="테스트 원두 (로그 있음)",
        country_name="테스트 국가",
        roast_level="MEDIUM",
        price_per_kg=30000.0,
        status="active",
        avg_loss_rate=17.0,
        std_loss_rate=1.0,
        total_roasted_count=3,
        last_roasted_date=date.today()
    )
    db_session.add(bean)
    db_session.commit()

    # 로스팅 기록 추가
    logs = [
        RoastingLog(
            bean_id=bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=10.0,
            loss_rate_percent=16.67,
            roasting_date=date.today()
        ),
        RoastingLog(
            bean_id=bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=9.96,
            loss_rate_percent=17.0,
            roasting_date=date.today()
        ),
        RoastingLog(
            bean_id=bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=9.84,
            loss_rate_percent=18.0,
            roasting_date=date.today()
        )
    ]
    for log in logs:
        db_session.add(log)
    db_session.commit()

    db_session.refresh(bean)
    return bean
