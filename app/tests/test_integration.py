"""
test_integration.py: 통합 테스트

여러 서비스가 함께 동작하는 전체 워크플로우를 검증합니다.
"""

import pytest
from datetime import date, timedelta
from app.services.roasting_service import RoastingService
from app.services.loss_rate_analyzer import LossRateAnalyzer
from app.services.cost_service import CostService
from app.services.auth_service import AuthService
from app.models.database import (
    Bean, Blend, BlendRecipe, RoastingLog,
    LossRateWarning, User, UserPermission
)


@pytest.mark.integration
class TestRoastingWorkflow:
    """로스팅 전체 워크플로우 통합 테스트"""

    def test_complete_roasting_workflow(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """
        완전한 로스팅 워크플로우 테스트

        시나리오:
        1. 블렌드 원가 계산
        2. 로스팅 기록 생성 (정상)
        3. 로스팅 기록 생성 (이상)
        4. 손실률 트렌드 분석
        5. 경고 조회 및 해결
        """

        # 1. 블렌드 원가 계산
        blend_cost = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )
        assert blend_cost is not None
        assert blend_cost['final_cost_per_kg'] > 0

        # 2. 정상 로스팅 기록 생성
        normal_log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,  # 17% 손실 (정상)
            roasting_date=date.today(),
            notes='정상 로스팅'
        )
        assert normal_log.loss_rate_percent == 17.0

        # 경고가 생성되지 않아야 함
        normal_warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == normal_log.id
        ).all()
        assert len(normal_warnings) == 0

        # 3. 이상 로스팅 기록 생성
        anomaly_log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,  # 30% 손실 (이상)
            roasting_date=date.today() + timedelta(days=1),
            expected_loss_rate=17.0,
            notes='이상 로스팅'
        )
        assert anomaly_log.loss_rate_percent == 30.0

        # 경고가 생성되어야 함
        anomaly_warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == anomaly_log.id
        ).all()
        assert len(anomaly_warnings) > 0
        assert anomaly_warnings[0].severity == 'CRITICAL'

        # 4. 손실률 트렌드 분석
        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)
        assert trend['data_count'] == 2
        assert trend['anomalies_count'] >= 1

        # 5. 경고 조회
        recent_warnings = LossRateAnalyzer.get_recent_warnings(db_session, limit=10)
        assert len(recent_warnings) >= 1

        # 6. 경고 해결
        warning_to_resolve = recent_warnings[0]
        resolved_warning = LossRateAnalyzer.resolve_warning(
            db=db_session,
            warning_id=warning_to_resolve['id'],
            notes='로스팅 설정 조정함'
        )
        assert resolved_warning.is_resolved is True
        assert resolved_warning.resolution_notes == '로스팅 설정 조정함'

        # 7. 해결 후 미해결 경고 재조회
        unresolved_warnings = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(unresolved_warnings) == 0  # 모두 해결됨

    def test_monthly_roasting_analysis(self, db_session):
        """월별 로스팅 분석 워크플로우"""
        month = date.today().strftime('%Y-%m')

        # 1. 다양한 손실률로 로스팅 기록 생성
        loss_rates = [
            (10.0, 8.3, 17.0),   # 정상
            (10.0, 8.2, 18.0),   # 정상
            (10.0, 7.9, 21.0),   # 경고
            (10.0, 7.0, 30.0),   # 심각
            (10.0, 8.5, 15.0),   # 정상
        ]

        for raw, roasted, expected_loss in loss_rates:
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=raw,
                roasted_weight_kg=roasted,
                roasting_date=date.today(),
                expected_loss_rate=17.0
            )

        # 2. 월별 통계 계산
        stats = RoastingService.get_monthly_statistics(db_session, month)
        assert stats['total_logs'] == 5
        assert stats['total_raw_weight_kg'] == 50.0

        # 3. 월별 손실률 요약
        monthly_summary = LossRateAnalyzer.get_monthly_summary(db_session, month)
        assert monthly_summary['data_count'] == 5
        assert monthly_summary['anomalies_count'] >= 2  # 경고 + 심각

        # 4. 심각도별 분포
        severity_dist = LossRateAnalyzer.get_severity_distribution(db_session, days=30)
        assert severity_dist['total_warnings'] >= 2


@pytest.mark.integration
class TestAuthenticationWorkflow:
    """사용자 인증 및 권한 워크플로우 통합 테스트"""

    def test_complete_user_lifecycle(self, db_session):
        """
        완전한 사용자 생명주기 테스트

        시나리오:
        1. 사용자 생성
        2. 인증
        3. 권한 부여
        4. 권한 확인
        5. 비밀번호 변경
        6. 재인증
        7. 권한 취소
        8. 사용자 비활성화
        """

        # 1. 사용자 생성
        user = AuthService.create_user(
            db=db_session,
            username='integration_user',
            password='password123',
            email='integration@example.com',
            full_name='Integration Test User',
            role='editor'
        )
        assert user is not None
        assert user.username == 'integration_user'

        # 2. 인증
        auth_user = AuthService.authenticate(
            db=db_session,
            username='integration_user',
            password='password123'
        )
        assert auth_user is not None
        assert auth_user.id == user.id
        assert auth_user.last_login is not None

        # 3. 권한 부여
        permission = AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write',
            granted_by=user.id
        )
        assert permission is not None

        # 4. 권한 확인
        has_write = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write'
        )
        assert has_write is True

        has_delete = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )
        assert has_delete is False

        # 5. 비밀번호 변경
        password_changed = AuthService.change_password(
            db=db_session,
            user_id=user.id,
            old_password='password123',
            new_password='newpassword456'
        )
        assert password_changed is True

        # 6. 재인증 (새 비밀번호)
        reauth_user = AuthService.authenticate(
            db=db_session,
            username='integration_user',
            password='newpassword456'
        )
        assert reauth_user is not None

        # 기존 비밀번호로는 인증 실패
        old_auth = AuthService.authenticate(
            db=db_session,
            username='integration_user',
            password='password123'
        )
        assert old_auth is None

        # 7. 권한 취소
        revoked = AuthService.revoke_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write'
        )
        assert revoked is True

        has_write_after_revoke = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write'
        )
        assert has_write_after_revoke is False

        # 8. 사용자 비활성화
        deactivated = AuthService.deactivate_user(
            db=db_session,
            user_id=user.id
        )
        assert deactivated is True

        # 비활성화된 사용자는 인증 불가
        inactive_auth = AuthService.authenticate(
            db=db_session,
            username='integration_user',
            password='newpassword456'
        )
        assert inactive_auth is None

    def test_admin_role_permissions(self, db_session):
        """Admin 역할의 전체 권한 테스트"""
        # Admin 사용자 생성
        admin = AuthService.create_user(
            db=db_session,
            username='admin_user',
            password='admin123',
            role='admin'
        )

        # Admin은 권한 부여 없이도 모든 리소스 접근 가능
        resources = ['blends', 'beans', 'roasting_logs', 'users', 'settings']
        actions = ['read', 'write', 'delete']

        for resource in resources:
            for action in actions:
                has_perm = AuthService.has_permission(
                    db=db_session,
                    user_id=admin.id,
                    resource=resource,
                    action=action
                )
                assert has_perm is True, f"Admin should have {action} permission on {resource}"


@pytest.mark.integration
class TestCostCalculationWorkflow:
    """원가 계산 워크플로우 통합 테스트"""

    def test_price_update_propagation(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """
        가격 업데이트가 원가 계산에 즉시 반영되는지 테스트

        시나리오:
        1. 초기 원가 계산
        2. 원두 가격 업데이트
        3. 원가 재계산 및 증가 확인
        4. 다른 원두 가격 업데이트
        5. 원가 재계산 및 추가 증가 확인
        """

        # 1. 초기 원가 계산
        initial_cost = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )
        initial_price = initial_cost['final_cost_per_kg']

        # 2. 예가체프 가격 인상 (5,500 → 7,000)
        bean_yirgacheffe = sample_beans[0]
        CostService.update_bean_price(
            db=db_session,
            bean_id=bean_yirgacheffe.id,
            new_price=7000
        )

        # 3. 원가 재계산
        updated_cost_1 = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )
        updated_price_1 = updated_cost_1['final_cost_per_kg']

        # 가격이 증가했는지 확인
        assert updated_price_1 > initial_price

        # 증가량 검증 (예가체프 40% 비율)
        expected_increase_1 = (7000 - 5500) * 0.4 / (1 - 0.17)
        actual_increase_1 = updated_price_1 - initial_price
        assert abs(actual_increase_1 - expected_increase_1) < 1

        # 4. 안티구아 가격 인상 (6,000 → 8,000)
        bean_antigua = sample_beans[1]
        CostService.update_bean_price(
            db=db_session,
            bean_id=bean_antigua.id,
            new_price=8000
        )

        # 5. 원가 재계산
        updated_cost_2 = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id,
            unit='kg'
        )
        updated_price_2 = updated_cost_2['final_cost_per_kg']

        # 추가 증가 확인
        assert updated_price_2 > updated_price_1

        # 추가 증가량 검증 (안티구아 40% 비율)
        expected_increase_2 = (8000 - 6000) * 0.4 / (1 - 0.17)
        actual_increase_2 = updated_price_2 - updated_price_1
        assert abs(actual_increase_2 - expected_increase_2) < 1

    def test_batch_cost_calculation(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """여러 블렌드 일괄 원가 계산 테스트"""
        # 추가 블렌드 생성
        blend2 = Blend(name='뉴문', blend_type='뉴문', status='active')
        db_session.add(blend2)
        db_session.commit()
        db_session.refresh(blend2)

        # 레시피 추가 (단순 블렌드)
        recipe1 = BlendRecipe(
            blend_id=blend2.id,
            bean_id=sample_beans[0].id,
            portion_count=10,
            ratio=100
        )
        db_session.add(recipe1)
        db_session.commit()

        # 일괄 계산
        results = CostService.batch_calculate_all_blends(db=db_session)

        assert len(results) == 2
        assert all('final_cost_per_kg' in result for result in results)
        assert all(result['final_cost_per_kg'] > 0 for result in results)


@pytest.mark.integration
class TestEndToEndScenarios:
    """엔드투엔드 시나리오 통합 테스트"""

    def test_new_user_creates_roasting_log(self, db_session, sample_cost_setting):
        """
        신규 사용자가 로스팅 기록을 생성하는 전체 시나리오

        시나리오:
        1. 사용자 생성 (editor 역할)
        2. 로그 생성 권한 부여
        3. 인증
        4. 권한 확인
        5. 로스팅 기록 생성 (정상)
        6. 로스팅 기록 생성 (이상)
        7. 경고 조회
        """

        # 1. 사용자 생성
        user = AuthService.create_user(
            db=db_session,
            username='roaster_user',
            password='roaster123',
            role='editor'
        )

        # 2. 로그 생성 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='roasting_logs',
            action='write',
            granted_by=user.id
        )

        # 3. 인증
        auth_user = AuthService.authenticate(
            db=db_session,
            username='roaster_user',
            password='roaster123'
        )
        assert auth_user is not None

        # 4. 권한 확인
        can_write = AuthService.has_permission(
            db=db_session,
            user_id=auth_user.id,
            resource='roasting_logs',
            action='write'
        )
        assert can_write is True

        # 5. 로스팅 기록 생성 (정상)
        log1 = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=15.0,
            roasted_weight_kg=12.45,  # 17% 손실
            roasting_date=date.today()
        )
        assert log1 is not None

        # 6. 로스팅 기록 생성 (이상)
        log2 = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=15.0,
            roasted_weight_kg=10.5,  # 30% 손실 (이상)
            roasting_date=date.today() + timedelta(days=1),
            expected_loss_rate=17.0
        )
        assert log2 is not None

        # 7. 경고 조회
        warnings = LossRateAnalyzer.get_recent_warnings(db_session)
        assert len(warnings) >= 1
        # 가장 최근 경고가 log2의 날짜와 일치하는지 확인
        assert warnings[0]['roasting_date'] == log2.roasting_date
        assert warnings[0]['severity'] == 'CRITICAL'

    def test_multi_user_concurrent_operations(self, db_session, sample_blend, sample_beans, sample_cost_setting):
        """
        여러 사용자의 동시 작업 시나리오

        시나리오:
        1. Admin 사용자가 원두 가격 업데이트
        2. Viewer 사용자가 원가 조회 (읽기만 가능)
        3. Editor 사용자가 로스팅 기록 생성
        4. Admin 사용자가 경고 해결
        """

        # 1. Admin 사용자 생성 및 가격 업데이트
        admin = AuthService.create_user(
            db=db_session,
            username='admin',
            password='admin123',
            role='admin'
        )

        CostService.update_bean_price(
            db=db_session,
            bean_id=sample_beans[0].id,
            new_price=6500
        )

        # 2. Viewer 사용자 생성 및 조회
        viewer = AuthService.create_user(
            db=db_session,
            username='viewer',
            password='viewer123',
            role='viewer'
        )

        # Viewer는 읽기 권한만 있음
        can_read = AuthService.has_permission(
            db=db_session,
            user_id=viewer.id,
            resource='blends',
            action='read'
        )
        assert can_read is True

        # 원가 조회는 가능
        cost = CostService.get_blend_cost(
            db=db_session,
            blend_id=sample_blend.id
        )
        assert cost is not None

        # 3. Editor 사용자 생성 및 로스팅 기록 생성
        editor = AuthService.create_user(
            db=db_session,
            username='editor',
            password='editor123',
            role='editor'
        )

        AuthService.grant_permission(
            db=db_session,
            user_id=editor.id,
            resource='roasting_logs',
            action='write',
            granted_by=admin.id
        )

        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,  # 이상치
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 4. Admin이 경고 해결
        warnings = LossRateAnalyzer.get_recent_warnings(db_session)
        if len(warnings) > 0:
            # Admin은 모든 권한 보유
            can_resolve = AuthService.has_permission(
                db=db_session,
                user_id=admin.id,
                resource='warnings',
                action='write'
            )
            assert can_resolve is True

            LossRateAnalyzer.resolve_warning(
                db=db_session,
                warning_id=warnings[0]['id'],
                notes='Admin이 확인 및 조치 완료'
            )
