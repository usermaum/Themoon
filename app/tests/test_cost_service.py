"""
test_cost_service.py: CostService 테스트

원가 계산 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.cost_service import CostService
from app.models.database import Bean, Blend, BlendRecipe, CostSetting


class TestCostService:
    """CostService 테스트 클래스"""

    def test_get_blend_cost_basic(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """
        블렌드 원가 계산 - 기본 케이스

        풀문 블렌드 원가 계산:
        - 예가체프 40% @ 5,500원/kg = 2,200원
        - 안티구아 40% @ 6,000원/kg = 2,400원
        - 모모라 10% @ 4,500원/kg = 450원
        - g4 10% @ 5,200원/kg = 520원
        ------------------------------------------
        - 혼합 원가 = 5,570원
        - 손실률 17% 반영 = 5,570 / 0.83 = 6,711원/kg
        """
        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )

        # 기본 검증
        assert result is not None
        assert result['blend_id'] == sample_blend.id
        assert result['blend_name'] == '풀문'
        assert len(result['component_costs']) == 4
        assert result['loss_rate'] == 0.17

        # 원가 계산 검증
        expected_blend_cost = (5500 * 0.4) + (6000 * 0.4) + (4500 * 0.1) + (5200 * 0.1)
        assert abs(result['blend_cost_before_loss'] - expected_blend_cost) < 1

        # 손실률 반영 원가 검증
        expected_final_cost = expected_blend_cost / (1 - 0.17)
        assert abs(result['final_cost_per_kg'] - expected_final_cost) < 1

        # 개별 컴포넌트 검증
        components = {c['bean_name']: c for c in result['component_costs']}
        assert '예가체프' in components
        assert abs(components['예가체프']['component_cost'] - 2200) < 1
        assert components['예가체프']['ratio'] == 40

    def test_get_blend_cost_invalid_blend(self, db_session):
        """존재하지 않는 블렌드 - 예외 처리"""
        with pytest.raises(ValueError) as exc_info:
            CostService.get_blend_cost(
                db=db_session,
                blend_id=999
            )

        assert "블렌드를 찾을 수 없습니다" in str(exc_info.value)

    def test_get_blend_cost_empty_recipes(self, db_session):
        """레시피가 없는 블렌드 - 경고 로그"""
        # 레시피 없는 블렌드 생성
        blend = Blend(name='빈 블렌드', blend_type='기타', status='active')
        db_session.add(blend)
        db_session.commit()
        db_session.refresh(blend)

        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=blend.id
        )

        # 빈 레시피여도 결과는 반환되어야 함
        assert result is not None
        assert result['blend_cost_before_loss'] == 0
        assert len(result['component_costs']) == 0

    def test_get_blend_cost_cup_unit(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """블렌드 원가 계산 - 컵 단위"""
        result_kg = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )

        result_cup = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='cup'
        )

        # 1 cup = 200g = 0.2kg
        expected_cup_cost = result_kg['final_cost_per_kg'] * 0.2
        assert abs(result_cup['final_cost_per_unit'] - expected_cup_cost) < 0.1

    def test_update_bean_price(self, db_session, sample_beans):
        """원두 가격 업데이트"""
        bean = sample_beans[0]
        old_price = bean.price_per_kg
        new_price = 6000

        updated_bean = CostService.update_bean_price(
            db=db_session,
            bean_id=bean.id,
            new_price=new_price
        )

        assert updated_bean is not None
        assert updated_bean.price_per_kg == new_price
        assert updated_bean.price_per_kg != old_price

        # 데이터베이스에 실제로 반영되었는지 확인
        db_bean = db_session.query(Bean).filter(Bean.id == bean.id).first()
        assert db_bean.price_per_kg == new_price

    def test_update_bean_price_invalid_bean(self, db_session):
        """존재하지 않는 원두 가격 업데이트 - 예외 처리"""
        with pytest.raises(ValueError) as exc_info:
            CostService.update_bean_price(
                db=db_session,
                bean_id=999,
                new_price=5000
            )

        assert "원두를 찾을 수 없습니다" in str(exc_info.value)

    def test_update_bean_price_negative(self, db_session, sample_beans):
        """음수 가격 업데이트 - 예외 처리"""
        bean = sample_beans[0]

        with pytest.raises(ValueError) as exc_info:
            CostService.update_bean_price(
                db=db_session,
                bean_id=bean.id,
                new_price=-1000
            )

        assert "가격은 0보다 커야 합니다" in str(exc_info.value)

    def test_batch_calculate_all_blends(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """모든 블렌드 일괄 계산"""
        # 추가 블렌드 생성
        blend2 = Blend(name='뉴문', blend_type='뉴문', status='active')
        db_session.add(blend2)
        db_session.commit()
        db_session.refresh(blend2)

        # 레시피 추가
        recipe = BlendRecipe(
            blend_id=blend2.id,
            bean_id=sample_beans[0].id,
            ratio=100
        )
        db_session.add(recipe)
        db_session.commit()

        # 일괄 계산
        results = CostService.batch_calculate_all_blends(db=db_session)

        assert results is not None
        assert len(results) == 2
        assert results[0]['blend_name'] in ['풀문', '뉴문']
        assert results[1]['blend_name'] in ['풀문', '뉴문']

    def test_get_cost_setting(self, db_session, sample_cost_setting):
        """비용 설정 조회"""
        setting = CostService.get_cost_setting(db=db_session)

        assert setting is not None
        assert setting.loss_rate == 17.0
        assert setting.margin_multiplier == 2.5
        assert setting.roasting_cost_per_kg == 500

    def test_get_cost_setting_not_exists(self, db_session):
        """비용 설정이 없을 때 - 기본값 반환"""
        setting = CostService.get_cost_setting(db=db_session)

        # 기본 설정이 생성되어야 함
        assert setting is not None
        assert setting.loss_rate > 0

    def test_update_cost_setting(self, db_session, sample_cost_setting):
        """비용 설정 업데이트"""
        new_loss_rate = 18.0
        new_margin = 3.0

        updated_setting = CostService.update_cost_setting(
            db=db_session,
            loss_rate=new_loss_rate,
            margin_multiplier=new_margin
        )

        assert updated_setting is not None
        assert updated_setting.loss_rate == new_loss_rate
        assert updated_setting.margin_multiplier == new_margin

    def test_calculate_blend_cost_with_components(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """블렌드 원가 상세 분석"""
        result = CostService.calculate_blend_cost_with_components(
            db=db_session,
            blend_id=sample_blend.id
        )

        assert result is not None
        assert 'component_breakdown' in result
        assert 'total_cost' in result
        assert 'margin_analysis' in result

        # 컴포넌트 분석 검증
        breakdown = result['component_breakdown']
        assert len(breakdown) == 4

        # 각 원두의 기여도 확인
        total_contribution = sum(comp['contribution_percent'] for comp in breakdown)
        assert abs(total_contribution - 100) < 0.1  # 합이 100%

    def test_cost_calculation_with_zero_ratio(self, db_session, sample_beans, sample_cost_setting):
        """비율이 0인 레시피 - 예외 처리"""
        blend = Blend(name='제로 블렌드', blend_type='기타', status='active')
        db_session.add(blend)
        db_session.commit()
        db_session.refresh(blend)

        # 비율 0인 레시피 추가
        recipe = BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            ratio=0
        )
        db_session.add(recipe)
        db_session.commit()

        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=blend.id
        )

        # 비율이 0이어도 계산은 가능해야 함
        assert result is not None
        assert result['blend_cost_before_loss'] == 0

    def test_cost_calculation_with_high_loss_rate(self, db_session, sample_blend, sample_beans):
        """높은 손실률 (30%) - 경계값 테스트"""
        # 높은 손실률 설정 생성
        high_loss_setting = CostSetting(
            loss_rate=30.0,
            margin_multiplier=2.5,
            roasting_cost_per_kg=500
        )
        db_session.add(high_loss_setting)
        db_session.commit()

        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )

        assert result is not None
        assert result['loss_rate'] == 0.30

        # 손실률 30%이면 원가는 더 높아야 함
        blend_cost = result['blend_cost_before_loss']
        final_cost = result['final_cost_per_kg']
        expected_final = blend_cost / (1 - 0.30)
        assert abs(final_cost - expected_final) < 1


@pytest.mark.integration
class TestCostServiceIntegration:
    """CostService 통합 테스트"""

    def test_price_update_affects_cost_calculation(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """가격 업데이트 후 원가 재계산"""
        # 초기 원가 계산
        initial_cost = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )

        # 가격 업데이트 (예가체프: 5,500 → 7,000)
        CostService.update_bean_price(
            db=db_session,
            bean_id=sample_beans[0].id,
            new_price=7000
        )

        # 재계산
        updated_cost = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )

        # 원가가 증가했는지 확인
        assert updated_cost['final_cost_per_kg'] > initial_cost['final_cost_per_kg']

        # 증가량 검증 (예가체프 40% 비율이므로 1,500 * 0.4 = 600원 증가)
        expected_increase = (7000 - 5500) * 0.4 / (1 - 0.17)
        actual_increase = updated_cost['final_cost_per_kg'] - initial_cost['final_cost_per_kg']
        assert abs(actual_increase - expected_increase) < 1
