"""
BlendService 테스트

BlendService의 모든 주요 기능을 테스트합니다:
- CRUD 작업 (블렌드 생성, 조회, 수정, 삭제)
- 레시피 관리 (원두 추가/제거, 비율 재계산)
- 조회 메서드 (ID, Name, Type, Active 등)
- 원가 계산 (블렌드 원가, 제안 가격)
- 분석 기능 (요약 통계)
- 초기화 및 내보내기
"""

import pytest
from app.services.blend_service import BlendService
from app.services.bean_service import BeanService
from app.models.database import Blend, BlendRecipe


class TestBlendServiceRead:
    """조회 메서드 테스트"""

    def test_get_all_blends(self, db_session, sample_blend):
        """모든 블렌드 조회"""
        service = BlendService(db_session)

        blends = service.get_all_blends()

        assert len(blends) == 1
        assert blends[0].name == '풀문'

    def test_get_all_blends_with_pagination(self, db_session, sample_blend):
        """페이지네이션 적용 조회"""
        service = BlendService(db_session)

        # 추가 블렌드 생성
        service.create_blend(name='뉴문', blend_type='뉴문')

        # 처음 1개만
        blends = service.get_all_blends(skip=0, limit=1)
        assert len(blends) == 1

        # 1개 건너뛰고 나머지
        blends = service.get_all_blends(skip=1, limit=10)
        assert len(blends) == 1

    def test_get_blend_by_id(self, db_session, sample_blend):
        """ID로 블렌드 조회"""
        service = BlendService(db_session)

        blend = service.get_blend_by_id(sample_blend.id)

        assert blend is not None
        assert blend.name == '풀문'

    def test_get_blend_by_id_not_found(self, db_session):
        """존재하지 않는 ID 조회"""
        service = BlendService(db_session)

        blend = service.get_blend_by_id(999)

        assert blend is None

    def test_get_blend_by_name(self, db_session, sample_blend):
        """이름으로 블렌드 조회"""
        service = BlendService(db_session)

        blend = service.get_blend_by_name('풀문')

        assert blend is not None
        assert blend.blend_type == '풀문'

    def test_get_blends_by_type(self, db_session, sample_blend):
        """타입별 블렌드 조회"""
        service = BlendService(db_session)

        # 다른 타입 블렌드 추가
        service.create_blend(name='뉴문', blend_type='뉴문')

        blends = service.get_blends_by_type('풀문')

        assert len(blends) == 1
        assert blends[0].name == '풀문'

    def test_get_active_blends(self, db_session, sample_blend):
        """활성 블렌드만 조회"""
        service = BlendService(db_session)

        # 비활성 블렌드 추가
        inactive = service.create_blend(name='비활성', blend_type='기타')
        inactive.status = 'inactive'
        db_session.commit()

        active_blends = service.get_active_blends()

        assert len(active_blends) == 1
        assert active_blends[0].status == 'active'

    def test_get_blend_recipes(self, db_session, sample_blend):
        """블렌드 구성 조회"""
        service = BlendService(db_session)

        recipes = service.get_blend_recipes(sample_blend.id)

        assert len(recipes) == 4  # 풀문은 4가지 원두

    def test_get_blend_with_details(self, db_session, sample_blend):
        """블렌드 상세 정보 (구성 포함)"""
        service = BlendService(db_session)

        details = service.get_blend_with_details(sample_blend.id)

        assert details is not None
        assert details['name'] == '풀문'
        assert len(details['recipes']) == 4
        assert details['recipes'][0]['bean_name'] == '예가체프'

    def test_get_blend_with_details_not_found(self, db_session):
        """존재하지 않는 블렌드 상세 조회"""
        service = BlendService(db_session)

        details = service.get_blend_with_details(999)

        assert details is None


class TestBlendServiceCreate:
    """생성 메서드 테스트"""

    def test_create_blend(self, db_session):
        """새 블렌드 생성"""
        service = BlendService(db_session)

        blend = service.create_blend(
            name='시즈널',
            blend_type='시즈널',
            description='계절 한정 블렌드',
            suggested_price=25000
        )

        assert blend.id is not None
        assert blend.name == '시즈널'
        assert blend.status == 'active'
        assert blend.suggested_price == 25000

    def test_create_blend_duplicate_name(self, db_session, sample_blend):
        """중복된 이름으로 블렌드 생성 시 오류"""
        service = BlendService(db_session)

        with pytest.raises(ValueError) as exc_info:
            service.create_blend(name='풀문', blend_type='기타')

        assert "이미 존재합니다" in str(exc_info.value)

    def test_add_recipe_to_blend(self, db_session, sample_beans):
        """블렌드에 원두 추가"""
        service = BlendService(db_session)

        # 빈 블렌드 생성
        blend = service.create_blend(name='테스트', blend_type='기타')

        # 원두 추가
        recipe = service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=5,
            ratio=50.0
        )

        assert recipe is not None
        assert recipe.portion_count == 5
        assert recipe.ratio == 50.0

    def test_add_recipe_updates_total_portion(self, db_session, sample_beans):
        """레시피 추가 시 total_portion 업데이트"""
        service = BlendService(db_session)

        blend = service.create_blend(name='테스트', blend_type='기타')

        # 첫 번째 원두 추가
        service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=5,
            ratio=50.0
        )

        db_session.refresh(blend)
        assert blend.total_portion == 1

        # 두 번째 원두 추가
        service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[1].id,
            portion_count=5,
            ratio=50.0
        )

        db_session.refresh(blend)
        assert blend.total_portion == 2

    def test_add_recipe_updates_existing(self, db_session, sample_beans):
        """이미 존재하는 원두 추가 시 업데이트"""
        service = BlendService(db_session)

        blend = service.create_blend(name='테스트', blend_type='기타')

        # 첫 번째 추가
        service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=5,
            ratio=50.0
        )

        # 같은 원두 다시 추가 (업데이트)
        recipe = service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=8,
            ratio=80.0
        )

        assert recipe.portion_count == 8
        assert recipe.ratio == 80.0

        # 레시피는 1개만 존재
        recipes = service.get_blend_recipes(blend.id)
        assert len(recipes) == 1

    def test_add_recipe_invalid_blend(self, db_session, sample_beans):
        """존재하지 않는 블렌드에 레시피 추가"""
        service = BlendService(db_session)

        result = service.add_recipe_to_blend(
            blend_id=999,
            bean_id=sample_beans[0].id,
            portion_count=5,
            ratio=50.0
        )

        assert result is None

    def test_add_recipe_invalid_bean(self, db_session, sample_blend):
        """존재하지 않는 원두로 레시피 추가"""
        service = BlendService(db_session)

        result = service.add_recipe_to_blend(
            blend_id=sample_blend.id,
            bean_id=999,
            portion_count=5,
            ratio=50.0
        )

        assert result is None


class TestBlendServiceUpdate:
    """수정 메서드 테스트"""

    def test_update_blend(self, db_session, sample_blend):
        """블렌드 정보 수정"""
        service = BlendService(db_session)

        updated = service.update_blend(
            blend_id=sample_blend.id,
            name='풀문 시즌2',
            suggested_price=30000
        )

        assert updated is not None
        assert updated.name == '풀문 시즌2'
        assert updated.suggested_price == 30000

    def test_update_blend_partial(self, db_session, sample_blend):
        """일부 필드만 수정"""
        service = BlendService(db_session)

        original_name = sample_blend.name
        updated = service.update_blend(
            blend_id=sample_blend.id,
            suggested_price=28000
        )

        assert updated.name == original_name
        assert updated.suggested_price == 28000

    def test_update_blend_not_found(self, db_session):
        """존재하지 않는 블렌드 수정"""
        service = BlendService(db_session)

        result = service.update_blend(
            blend_id=999,
            name='없음'
        )

        assert result is None

    def test_update_recipe_ratio(self, db_session, sample_beans):
        """레시피 비율 재계산"""
        service = BlendService(db_session)

        blend = service.create_blend(name='테스트', blend_type='기타')

        # 3개 원두 추가 (portion: 2, 3, 5 = 총 10)
        service.add_recipe_to_blend(blend.id, sample_beans[0].id, 2, 0)
        service.add_recipe_to_blend(blend.id, sample_beans[1].id, 3, 0)
        service.add_recipe_to_blend(blend.id, sample_beans[2].id, 5, 0)

        # 비율 재계산
        result = service.update_recipe_ratio(blend.id)
        assert result is True

        # 비율 확인 (20%, 30%, 50%)
        recipes = service.get_blend_recipes(blend.id)
        ratios = sorted([r.ratio for r in recipes])

        assert abs(ratios[0] - 20.0) < 0.01
        assert abs(ratios[1] - 30.0) < 0.01
        assert abs(ratios[2] - 50.0) < 0.01

    def test_update_recipe_ratio_no_recipes(self, db_session):
        """레시피 없는 블렌드의 비율 재계산"""
        service = BlendService(db_session)

        blend = service.create_blend(name='빈 블렌드', blend_type='기타')

        result = service.update_recipe_ratio(blend.id)

        assert result is False

    def test_update_recipe_ratio_invalid_blend(self, db_session):
        """존재하지 않는 블렌드 비율 재계산"""
        service = BlendService(db_session)

        result = service.update_recipe_ratio(999)

        assert result is False


class TestBlendServiceDelete:
    """삭제 메서드 테스트"""

    def test_delete_blend(self, db_session, sample_blend):
        """블렌드 소프트 삭제"""
        service = BlendService(db_session)

        result = service.delete_blend(sample_blend.id)

        assert result is True

        # 여전히 존재하지만 상태가 inactive
        db_session.refresh(sample_blend)
        assert sample_blend.status == 'inactive'

    def test_delete_blend_not_found(self, db_session):
        """존재하지 않는 블렌드 삭제"""
        service = BlendService(db_session)

        result = service.delete_blend(999)

        assert result is False

    def test_remove_recipe_from_blend(self, db_session, sample_blend, sample_beans):
        """블렌드에서 원두 제거"""
        service = BlendService(db_session)

        # 제거 전 레시피 개수
        recipes_before = service.get_blend_recipes(sample_blend.id)
        count_before = len(recipes_before)

        # 첫 번째 원두 제거
        result = service.remove_recipe_from_blend(
            blend_id=sample_blend.id,
            bean_id=sample_beans[0].id
        )

        assert result is True

        # 제거 후 레시피 개수
        recipes_after = service.get_blend_recipes(sample_blend.id)
        assert len(recipes_after) == count_before - 1

    def test_remove_recipe_not_found(self, db_session, sample_blend):
        """존재하지 않는 레시피 제거"""
        service = BlendService(db_session)

        result = service.remove_recipe_from_blend(
            blend_id=sample_blend.id,
            bean_id=999
        )

        assert result is False


class TestBlendServiceCostCalculation:
    """원가 계산 메서드 테스트"""

    def test_calculate_blend_cost(self, db_session, sample_blend):
        """블렌드 원가 계산"""
        service = BlendService(db_session)

        cost_info = service.calculate_blend_cost(sample_blend.id)

        assert cost_info is not None
        assert 'blend_name' in cost_info
        assert 'total_cost' in cost_info
        assert 'suggested_price' in cost_info
        assert 'recipes' in cost_info

        # 레시피 개수 확인
        assert len(cost_info['recipes']) == 4

        # 비용이 양수인지 확인
        assert cost_info['total_cost'] > 0
        assert cost_info['suggested_price'] > cost_info['total_cost']

    def test_calculate_blend_cost_includes_all_costs(self, db_session, sample_blend):
        """모든 비용 항목 포함 확인"""
        service = BlendService(db_session)

        cost_info = service.calculate_blend_cost(sample_blend.id)

        # 모든 비용 항목 확인
        assert 'bean_cost_total' in cost_info
        assert 'roasting_cost' in cost_info
        assert 'labor_cost' in cost_info
        assert 'misc_cost' in cost_info
        assert 'cost_per_portion' in cost_info
        assert 'margin_rate' in cost_info
        assert 'profit_margin' in cost_info

    def test_calculate_blend_cost_invalid_blend(self, db_session):
        """존재하지 않는 블렌드 원가 계산"""
        service = BlendService(db_session)

        cost_info = service.calculate_blend_cost(999)

        assert cost_info == {}


class TestBlendServiceAnalytics:
    """분석 메서드 테스트"""

    def test_get_blends_summary(self, db_session, sample_blend):
        """블렌드 전체 요약"""
        service = BlendService(db_session)

        summary = service.get_blends_summary()

        assert summary['total_blends'] == 1
        assert '풀문' in summary['by_type']

    def test_get_blends_summary_multiple_types(self, db_session, sample_blend):
        """다양한 타입의 블렌드 요약"""
        service = BlendService(db_session)

        # 추가 블렌드 생성
        service.create_blend(name='뉴문', blend_type='뉴문')
        service.create_blend(name='시즈널', blend_type='시즈널')

        summary = service.get_blends_summary()

        assert summary['total_blends'] == 3
        assert summary['by_type']['풀문'] == 1
        assert summary['by_type']['뉴문'] == 1
        assert summary['by_type']['시즈널'] == 1


class TestBlendServiceUtility:
    """유틸리티 메서드 테스트"""

    def test_init_default_blends(self, db_session):
        """기본 블렌드 로드"""
        # BeanService로 기본 원두 먼저 로드
        bean_service = BeanService(db_session)
        bean_service.init_default_beans()

        service = BlendService(db_session)
        count = service.init_default_blends()

        # 기본 블렌드가 로드되어야 함
        assert count > 0

        # 실제로 DB에 저장되었는지 확인
        blends = service.get_active_blends()
        assert len(blends) == count

    def test_init_default_blends_with_recipes(self, db_session):
        """기본 블렌드 로드 시 레시피 포함"""
        # 원두 먼저 로드
        bean_service = BeanService(db_session)
        bean_service.init_default_beans()

        service = BlendService(db_session)
        service.init_default_blends()

        # 첫 번째 블렌드의 레시피 확인
        blends = service.get_active_blends()
        if blends:
            recipes = service.get_blend_recipes(blends[0].id)
            assert len(recipes) > 0

    def test_export_as_dict(self, db_session, sample_blend):
        """딕셔너리로 내보내기"""
        service = BlendService(db_session)

        data = service.export_as_dict()

        assert len(data) == 1
        assert data[0]['이름'] == '풀문'
        assert data[0]['타입'] == '풀문'
        assert '구성' in data[0]


class TestBlendServiceEdgeCases:
    """경계값 및 예외 상황 테스트"""

    def test_create_blend_minimal_fields(self, db_session):
        """필수 필드만으로 블렌드 생성"""
        service = BlendService(db_session)

        blend = service.create_blend(
            name='최소 블렌드',
            blend_type='기타'
        )

        assert blend.id is not None
        assert blend.description is None
        assert blend.suggested_price == 0.0

    def test_add_recipe_zero_portion(self, db_session, sample_beans):
        """포션이 0인 레시피 추가"""
        service = BlendService(db_session)

        blend = service.create_blend(name='테스트', blend_type='기타')

        recipe = service.add_recipe_to_blend(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=0,
            ratio=0.0
        )

        assert recipe is not None
        assert recipe.portion_count == 0

    def test_update_recipe_ratio_zero_total_portion(self, db_session, sample_beans):
        """총 포션이 0일 때 비율 재계산"""
        service = BlendService(db_session)

        blend = service.create_blend(name='테스트', blend_type='기타')

        # 포션이 모두 0
        service.add_recipe_to_blend(blend.id, sample_beans[0].id, 0, 0)
        service.add_recipe_to_blend(blend.id, sample_beans[1].id, 0, 0)

        result = service.update_recipe_ratio(blend.id)

        assert result is False

    def test_update_all_blend_fields(self, db_session, sample_blend):
        """모든 필드 동시 수정"""
        service = BlendService(db_session)

        updated = service.update_blend(
            blend_id=sample_blend.id,
            name='새 이름',
            description='새 설명',
            suggested_price=35000,
            status='inactive'
        )

        assert updated.name == '새 이름'
        assert updated.description == '새 설명'
        assert updated.suggested_price == 35000
        assert updated.status == 'inactive'
