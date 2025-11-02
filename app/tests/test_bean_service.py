"""
BeanService 테스트

BeanService의 모든 주요 기능을 테스트합니다:
- CRUD 작업 (생성, 조회, 수정, 삭제)
- 조회 메서드 (ID, No, Name, Country, RoastLevel 등)
- 비즈니스 로직 (재고 자동 생성, 소프트 삭제, 하드 삭제)
- 분석 기능 (요약 통계, 자주 사용되는 원두)
- 초기화 및 내보내기
"""

import pytest
from app.services.bean_service import BeanService
from app.models.database import Bean, Inventory, BlendRecipe


class TestBeanServiceRead:
    """조회 메서드 테스트"""

    def test_get_all_beans(self, db_session, sample_beans):
        """모든 원두 조회"""
        service = BeanService(db_session)

        beans = service.get_all_beans()

        assert len(beans) == 4
        assert beans[0].name == '예가체프'

    def test_get_all_beans_with_pagination(self, db_session, sample_beans):
        """페이지네이션 적용 조회"""
        service = BeanService(db_session)

        # 처음 2개만
        beans = service.get_all_beans(skip=0, limit=2)
        assert len(beans) == 2

        # 2개 건너뛰고 나머지
        beans = service.get_all_beans(skip=2, limit=10)
        assert len(beans) == 2

    def test_get_bean_by_id(self, db_session, sample_beans):
        """ID로 원두 조회"""
        service = BeanService(db_session)

        bean = service.get_bean_by_id(sample_beans[0].id)

        assert bean is not None
        assert bean.name == '예가체프'
        assert bean.price_per_kg == 5500

    def test_get_bean_by_id_not_found(self, db_session):
        """존재하지 않는 ID 조회"""
        service = BeanService(db_session)

        bean = service.get_bean_by_id(999)

        assert bean is None

    def test_get_bean_by_no(self, db_session, sample_beans):
        """번호로 원두 조회"""
        service = BeanService(db_session)

        bean = service.get_bean_by_no(1)

        assert bean is not None
        assert bean.name == '예가체프'

    def test_get_bean_by_name(self, db_session, sample_beans):
        """이름으로 원두 조회"""
        service = BeanService(db_session)

        bean = service.get_bean_by_name('안티구아')

        assert bean is not None
        assert bean.no == 2
        assert bean.price_per_kg == 6000

    def test_get_beans_by_country(self, db_session, sample_beans):
        """국가별 원두 조회"""
        service = BeanService(db_session)

        beans = service.get_beans_by_country('BR')

        assert len(beans) == 2
        assert all(b.country_code == 'BR' for b in beans)

    def test_get_beans_by_roast_level(self, db_session, sample_beans):
        """로스팅 레벨별 원두 조회"""
        service = BeanService(db_session)

        beans = service.get_beans_by_roast_level('Medium')

        assert len(beans) == 4

    def test_get_active_beans(self, db_session, sample_beans):
        """활성 원두만 조회"""
        service = BeanService(db_session)

        # 하나를 비활성화
        sample_beans[0].status = 'inactive'
        db_session.commit()

        active_beans = service.get_active_beans()

        assert len(active_beans) == 3
        assert all(b.status == 'active' for b in active_beans)

    def test_get_bean_count(self, db_session, sample_beans):
        """전체 원두 개수"""
        service = BeanService(db_session)

        count = service.get_bean_count()

        assert count == 4


class TestBeanServiceCreate:
    """생성 메서드 테스트"""

    def test_create_bean(self, db_session):
        """새 원두 생성"""
        service = BeanService(db_session)

        bean = service.create_bean(
            no=10,
            name='케냐 AA',
            roast_level='Light',
            country_code='KE',
            country_name='Kenya',
            description='케냐 최고급 원두',
            price_per_kg=7000
        )

        assert bean.id is not None
        assert bean.no == 10
        assert bean.name == '케냐 AA'
        assert bean.status == 'active'

    def test_create_bean_auto_creates_inventory(self, db_session):
        """원두 생성 시 재고 자동 생성"""
        service = BeanService(db_session)

        bean = service.create_bean(
            no=11,
            name='콜롬비아',
            roast_level='Medium',
            price_per_kg=5800
        )

        # 재고가 자동 생성되었는지 확인
        inventory = db_session.query(Inventory).filter(
            Inventory.bean_id == bean.id
        ).first()

        assert inventory is not None
        assert inventory.bean_id == bean.id

    def test_create_bean_duplicate_no(self, db_session, sample_beans):
        """중복된 번호로 원두 생성 시 오류"""
        service = BeanService(db_session)

        with pytest.raises(ValueError) as exc_info:
            service.create_bean(
                no=1,  # 이미 존재하는 번호
                name='새로운 원두',
                roast_level='Dark',
                price_per_kg=6000
            )

        assert "이미 존재합니다" in str(exc_info.value)

    def test_create_bean_duplicate_name(self, db_session, sample_beans):
        """중복된 이름으로 원두 생성 시 오류"""
        service = BeanService(db_session)

        with pytest.raises(ValueError) as exc_info:
            service.create_bean(
                no=99,
                name='예가체프',  # 이미 존재하는 이름
                roast_level='Dark',
                price_per_kg=6000
            )

        assert "이미 존재합니다" in str(exc_info.value)


class TestBeanServiceUpdate:
    """수정 메서드 테스트"""

    def test_update_bean(self, db_session, sample_beans):
        """원두 정보 수정"""
        service = BeanService(db_session)

        updated = service.update_bean(
            bean_id=sample_beans[0].id,
            name='예가체프 G1',
            price_per_kg=6000
        )

        assert updated is not None
        assert updated.name == '예가체프 G1'
        assert updated.price_per_kg == 6000
        assert updated.updated_at is not None

    def test_update_bean_partial(self, db_session, sample_beans):
        """일부 필드만 수정"""
        service = BeanService(db_session)

        original_name = sample_beans[0].name
        updated = service.update_bean(
            bean_id=sample_beans[0].id,
            price_per_kg=7500
        )

        assert updated.name == original_name  # 이름은 그대로
        assert updated.price_per_kg == 7500  # 가격만 변경

    def test_update_bean_not_found(self, db_session):
        """존재하지 않는 원두 수정 시도"""
        service = BeanService(db_session)

        result = service.update_bean(
            bean_id=999,
            name='없는 원두'
        )

        assert result is None

    def test_update_bean_status(self, db_session, sample_beans):
        """원두 상태 변경"""
        service = BeanService(db_session)

        updated = service.update_bean(
            bean_id=sample_beans[0].id,
            status='inactive'
        )

        assert updated.status == 'inactive'


class TestBeanServiceDelete:
    """삭제 메서드 테스트"""

    def test_delete_bean_soft(self, db_session, sample_beans):
        """소프트 삭제 (상태만 변경)"""
        service = BeanService(db_session)

        result = service.delete_bean(sample_beans[0].id)

        assert result is True

        # DB에서 다시 조회
        bean = db_session.query(Bean).filter(Bean.id == sample_beans[0].id).first()
        assert bean is not None  # 여전히 존재
        assert bean.status == 'inactive'  # 상태만 변경

    def test_delete_bean_not_found(self, db_session):
        """존재하지 않는 원두 삭제"""
        service = BeanService(db_session)

        result = service.delete_bean(999)

        assert result is False

    def test_hard_delete_bean(self, db_session, sample_beans):
        """하드 삭제 (완전 삭제)"""
        service = BeanService(db_session)

        bean_id = sample_beans[3].id  # g4 원두 (블렌드에 사용되지 않음)
        result = service.hard_delete_bean(bean_id)

        assert result is True

        # DB에서 완전히 삭제되었는지 확인
        bean = db_session.query(Bean).filter(Bean.id == bean_id).first()
        assert bean is None

    def test_hard_delete_bean_with_blend_recipes(self, db_session, sample_beans, sample_blend):
        """블렌드 레시피에 포함된 원두는 하드 삭제 불가"""
        service = BeanService(db_session)

        # 예가체프는 블렌드에 사용 중
        with pytest.raises(ValueError) as exc_info:
            service.hard_delete_bean(sample_beans[0].id)

        assert "블렌드에 포함되어 있습니다" in str(exc_info.value)

    def test_hard_delete_bean_not_found(self, db_session):
        """존재하지 않는 원두 하드 삭제"""
        service = BeanService(db_session)

        result = service.hard_delete_bean(999)

        assert result is False


class TestBeanServiceAnalytics:
    """분석 메서드 테스트"""

    def test_get_beans_summary(self, db_session, sample_beans):
        """원두 전체 요약 통계"""
        service = BeanService(db_session)

        summary = service.get_beans_summary()

        assert summary['total_beans'] == 4
        assert 'Medium' in summary['by_roast_level']
        assert summary['by_roast_level']['Medium'] == 4

    def test_get_beans_summary_with_different_roast_levels(self, db_session, sample_beans):
        """다양한 로스팅 레벨 요약"""
        service = BeanService(db_session)

        # 하나를 Dark로 변경
        sample_beans[0].roast_level = 'Dark'
        db_session.commit()

        summary = service.get_beans_summary()

        assert summary['by_roast_level']['Medium'] == 3
        assert summary['by_roast_level']['Dark'] == 1

    def test_get_most_used_beans(self, db_session, sample_beans, sample_blend):
        """자주 사용되는 원두 TOP N"""
        service = BeanService(db_session)

        result = service.get_most_used_beans(limit=3)

        assert len(result) <= 3
        assert result[0]['usage_count'] >= 1  # 블렌드에 사용 중

    def test_get_most_used_beans_no_usage(self, db_session, sample_beans):
        """블렌드에 사용되지 않은 원두"""
        service = BeanService(db_session)

        result = service.get_most_used_beans()

        # 모든 원두의 usage_count가 0
        assert all(r['usage_count'] == 0 for r in result)


class TestBeanServiceUtility:
    """유틸리티 메서드 테스트"""

    def test_init_default_beans(self, db_session):
        """기본 원두 13종 로드"""
        service = BeanService(db_session)

        count = service.init_default_beans()

        # 13개 원두가 로드되어야 함
        assert count > 0

        # 실제로 DB에 저장되었는지 확인
        total = service.get_bean_count()
        assert total == count

    def test_init_default_beans_idempotent(self, db_session):
        """기본 원두 중복 로드 방지"""
        service = BeanService(db_session)

        # 첫 번째 로드
        count1 = service.init_default_beans()

        # 두 번째 로드 (중복 없음)
        count2 = service.init_default_beans()

        assert count1 > 0
        assert count2 == 0  # 이미 존재하므로 0

    def test_export_as_dict(self, db_session, sample_beans):
        """딕셔너리로 내보내기"""
        service = BeanService(db_session)

        data = service.export_as_dict()

        assert len(data) == 4
        assert data[0]['No'] == 1
        assert data[0]['원두명'] == '예가체프'
        assert data[0]['단가(원/kg)'] == 5500

    def test_export_as_dict_excludes_inactive(self, db_session, sample_beans):
        """비활성 원두는 제외"""
        service = BeanService(db_session)

        # 하나를 비활성화
        sample_beans[0].status = 'inactive'
        db_session.commit()

        data = service.export_as_dict()

        assert len(data) == 3
        assert all(d['원두명'] != '예가체프' for d in data)


class TestBeanServiceEdgeCases:
    """경계값 및 예외 상황 테스트"""

    def test_create_bean_with_zero_price(self, db_session):
        """가격이 0인 원두 생성"""
        service = BeanService(db_session)

        bean = service.create_bean(
            no=20,
            name='무료 원두',
            roast_level='Medium',
            price_per_kg=0.0
        )

        assert bean.price_per_kg == 0.0

    def test_create_bean_minimal_fields(self, db_session):
        """필수 필드만으로 원두 생성"""
        service = BeanService(db_session)

        bean = service.create_bean(
            no=21,
            name='최소 원두',
            roast_level='Medium'
        )

        assert bean.id is not None
        assert bean.country_code is None
        assert bean.description is None
        assert bean.price_per_kg == 0.0

    def test_get_beans_by_nonexistent_country(self, db_session, sample_beans):
        """존재하지 않는 국가 코드로 조회"""
        service = BeanService(db_session)

        beans = service.get_beans_by_country('ZZ')

        assert len(beans) == 0

    def test_update_all_fields(self, db_session, sample_beans):
        """모든 필드 동시 수정"""
        service = BeanService(db_session)

        updated = service.update_bean(
            bean_id=sample_beans[0].id,
            name='새 이름',
            roast_level='Dark',
            country_code='CO',
            country_name='Colombia',
            description='새 설명',
            price_per_kg=8000,
            image_url='http://example.com/image.jpg',
            status='inactive'
        )

        assert updated.name == '새 이름'
        assert updated.roast_level == 'Dark'
        assert updated.country_code == 'CO'
        assert updated.price_per_kg == 8000
        assert updated.status == 'inactive'
