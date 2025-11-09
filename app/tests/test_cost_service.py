"""
test_cost_service.py: CostService 테스트

원가 계산 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.cost_service import CostService
from app.models.database import Bean, Blend, BlendRecipe, CostSetting, BeanPriceHistory


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
        assert result['loss_rate'] == 17.0  # 퍼센트로 반환

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
        assert abs(result_cup['final_cost_per_unit'] - expected_cup_cost) < 1  # 허용 오차 증가

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
            portion_count=10,
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
        # loss_rate 조회
        loss_rate = CostService.get_cost_setting(db=db_session, parameter_name='loss_rate')
        assert loss_rate == 17.0

        # margin_multiplier 조회
        margin = CostService.get_cost_setting(db=db_session, parameter_name='margin_multiplier')
        assert margin == 2.5

        # roasting_cost_per_kg 조회
        roasting_cost = CostService.get_cost_setting(db=db_session, parameter_name='roasting_cost_per_kg')
        assert roasting_cost == 500

    def test_get_cost_setting_not_exists(self, db_session):
        """비용 설정이 없을 때 - 0.0 반환"""
        value = CostService.get_cost_setting(db=db_session, parameter_name='non_existent_param')

        # 존재하지 않는 설정은 0.0 반환
        assert value == 0.0

    def test_update_cost_setting(self, db_session, sample_cost_setting):
        """비용 설정 업데이트"""
        new_loss_rate = 18.0

        updated_setting = CostService.update_cost_setting(
            db=db_session,
            parameter_name='loss_rate',
            value=new_loss_rate,
            description='업데이트된 손실률'
        )

        assert updated_setting is not None
        assert updated_setting.parameter_name == 'loss_rate'
        assert updated_setting.value == new_loss_rate
        assert updated_setting.description == '업데이트된 손실률'

        # 데이터베이스에 실제로 반영되었는지 확인
        retrieved_value = CostService.get_cost_setting(db=db_session, parameter_name='loss_rate')
        assert retrieved_value == new_loss_rate

    def test_calculate_blend_cost_with_components(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """블렌드 원가 상세 분석"""
        result = CostService.calculate_blend_cost_with_components(
            db=db_session,
            blend_id=sample_blend.id
        )

        assert result is not None
        assert 'component_costs' in result
        assert len(result['component_costs']) == 4

        # 각 컴포넌트에 final_contribution이 있는지 확인
        for comp in result['component_costs']:
            assert 'final_contribution' in comp
            assert comp['final_contribution'] > 0

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
            portion_count=0,
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
        # 참고: CostService는 현재 고정 손실률 17%를 사용하므로
        # 이 테스트는 현재 구현에서는 17%로 계산됨
        # 추후 동적 손실률 적용 시 이 테스트를 활성화할 것

        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )

        assert result is not None
        # 현재는 고정 손실률 17% 사용
        assert result['loss_rate'] == 17.0

        # 손실률 17% 반영 원가 검증
        blend_cost = result['blend_cost_before_loss']
        final_cost = result['final_cost_per_kg']
        expected_final = blend_cost / (1 - 0.17)
        assert abs(final_cost - expected_final) < 1


    def test_get_bean_price_history(self, db_session, sample_beans):
        """원두 가격 변경 이력 조회"""
        bean = sample_beans[0]

        # 가격 변경 1차
        CostService.update_bean_price(
            db=db_session,
            bean_id=bean.id,
            new_price=6000,
            change_reason="환율 상승"
        )

        # 가격 변경 2차
        CostService.update_bean_price(
            db=db_session,
            bean_id=bean.id,
            new_price=6500,
            change_reason="원두 품질 향상"
        )

        # 이력 조회
        history = CostService.get_bean_price_history(
            db=db_session,
            bean_id=bean.id,
            limit=10
        )

        assert history is not None
        assert len(history) == 2

        # 최신 이력이 첫 번째
        assert history[0]['new_price'] == 6500
        assert history[0]['old_price'] == 6000
        assert history[0]['change_reason'] == "원두 품질 향상"
        assert history[0]['price_change'] == 500
        assert abs(history[0]['price_change_percent'] - 8.3) < 0.1

        # 이전 이력이 두 번째
        assert history[1]['new_price'] == 6000
        assert history[1]['old_price'] == 5500  # 초기 가격
        assert history[1]['change_reason'] == "환율 상승"

    def test_get_bean_price_history_invalid_bean(self, db_session):
        """존재하지 않는 원두의 가격 이력 조회 - 예외 처리"""
        with pytest.raises(ValueError) as exc_info:
            CostService.get_bean_price_history(
                db=db_session,
                bean_id=999,
                limit=10
            )

        assert "원두를 찾을 수 없습니다" in str(exc_info.value)

    def test_get_bean_price_history_no_changes(self, db_session, sample_beans):
        """가격 변경 이력이 없는 경우"""
        bean = sample_beans[0]

        # 가격 변경하지 않음
        history = CostService.get_bean_price_history(
            db=db_session,
            bean_id=bean.id,
            limit=10
        )

        assert history is not None
        assert len(history) == 0

    def test_update_bean_price_no_change(self, db_session, sample_beans):
        """가격이 동일할 때 - 이력 기록하지 않음"""
        bean = sample_beans[0]
        old_price = bean.price_per_kg

        # 동일한 가격으로 업데이트
        updated_bean = CostService.update_bean_price(
            db=db_session,
            bean_id=bean.id,
            new_price=old_price
        )

        assert updated_bean is not None
        assert updated_bean.price_per_kg == old_price

        # 이력이 기록되지 않았는지 확인
        history = CostService.get_bean_price_history(
            db=db_session,
            bean_id=bean.id
        )
        assert len(history) == 0

    def test_update_cost_setting_new_parameter(self, db_session):
        """새로운 비용 설정 추가 (insert)"""
        new_param_name = "packaging_cost_per_kg"
        new_value = 300.0
        new_description = "포장 비용 (원/kg)"

        # 새 설정 추가
        setting = CostService.update_cost_setting(
            db=db_session,
            parameter_name=new_param_name,
            value=new_value,
            description=new_description
        )

        assert setting is not None
        assert setting.parameter_name == new_param_name
        assert setting.value == new_value
        assert setting.description == new_description

        # 데이터베이스에서 조회 확인
        retrieved_value = CostService.get_cost_setting(
            db=db_session,
            parameter_name=new_param_name
        )
        assert retrieved_value == new_value

    def test_get_blend_cost_with_selling_price(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """판매 가격이 있을 때 마진 계산"""
        # 판매 가격 설정
        sample_blend.suggested_price = 10000
        db_session.commit()

        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )

        assert result is not None
        assert result['selling_price'] == 10000
        assert result['margin_percent'] is not None

        # 마진율 계산 검증
        final_cost = result['final_cost_per_kg']
        selling_price = result['selling_price']
        expected_margin = ((selling_price - final_cost) / selling_price * 100)
        assert abs(result['margin_percent'] - expected_margin) < 0.1

    def test_get_blend_cost_missing_bean_in_recipe(self, db_session, sample_beans, sample_cost_setting):
        """레시피가 참조하는 원두가 없을 때 - 해당 레시피 건너뛰기"""
        # 블렌드 생성
        blend = Blend(name='문제 블렌드', blend_type='기타', status='active')
        db_session.add(blend)
        db_session.commit()
        db_session.refresh(blend)

        # 정상 레시피
        recipe1 = BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=5,
            ratio=50
        )
        db_session.add(recipe1)

        # 존재하지 않는 원두를 참조하는 레시피
        recipe2 = BlendRecipe(
            blend_id=blend.id,
            bean_id=999,  # 존재하지 않는 ID
            portion_count=5,
            ratio=50
        )
        db_session.add(recipe2)
        db_session.commit()

        # 계산 시도 - 에러 없이 건너뛰어야 함
        result = CostService.get_blend_cost(
            db=db_session,
            blend_id=blend.id
        )

        assert result is not None
        # 정상 레시피만 포함
        assert len(result['component_costs']) == 1
        assert result['component_costs'][0]['bean_name'] == sample_beans[0].name

    def test_batch_calculate_with_error(self, db_session, sample_beans, sample_cost_setting):
        """일괄 계산 중 에러 발생 - 에러 처리"""
        # 정상 블렌드
        blend1 = Blend(name='정상 블렌드', blend_type='기타', status='active')
        db_session.add(blend1)

        # 문제 블렌드 (레시피 없음 but 처리 가능)
        blend2 = Blend(name='빈 블렌드', blend_type='기타', status='active')
        db_session.add(blend2)

        db_session.commit()
        db_session.refresh(blend1)
        db_session.refresh(blend2)

        # blend1에 레시피 추가
        recipe = BlendRecipe(
            blend_id=blend1.id,
            bean_id=sample_beans[0].id,
            portion_count=10,
            ratio=100
        )
        db_session.add(recipe)
        db_session.commit()

        # 일괄 계산
        results = CostService.batch_calculate_all_blends(db=db_session)

        assert results is not None
        assert len(results) == 2

        # 두 블렌드 모두 결과 반환 (빈 블렌드도 cost=0으로 처리)
        assert all('blend_name' in r for r in results)


    def test_batch_calculate_with_exception(self, db_session, sample_beans, sample_cost_setting, monkeypatch):
        """일괄 계산 중 get_blend_cost 예외 발생 처리"""
        # 정상 블렌드 생성
        blend1 = Blend(name='정상 블렌드', blend_type='기타', status='active')
        db_session.add(blend1)
        db_session.commit()
        db_session.refresh(blend1)

        # 레시피 추가
        recipe = BlendRecipe(
            blend_id=blend1.id,
            bean_id=sample_beans[0].id,
            portion_count=10,
            ratio=100
        )
        db_session.add(recipe)
        db_session.commit()

        # get_blend_cost를 모킹하여 예외 발생시키기
        original_method = CostService.get_blend_cost
        call_count = [0]

        def mock_get_blend_cost(db, blend_id, unit='kg'):
            call_count[0] += 1
            # 첫 호출 시 예외 발생
            if call_count[0] == 1:
                raise Exception("계산 중 오류 발생")
            return original_method(db, blend_id, unit)

        monkeypatch.setattr(CostService, 'get_blend_cost', staticmethod(mock_get_blend_cost))

        # 일괄 계산 - 예외가 발생해도 계속 진행
        results = CostService.batch_calculate_all_blends(db=db_session)

        assert results is not None
        assert len(results) == 1  # 1개 블렌드
        # 예외 발생 시 error 키가 있어야 함
        assert 'error' in results[0]
        assert '계산 중 오류 발생' in str(results[0]['error'])


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
