"""
test_auth_service.py: AuthService 테스트

사용자 인증 및 권한 관리 로직의 정확성을 검증합니다.
"""

import pytest
from app.services.auth_service import AuthService
from app.models.database import User, UserPermission


class TestAuthService:
    """AuthService 테스트 클래스"""

    def test_create_user_basic(self, db_session):
        """기본 사용자 생성"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123',
            email='test@example.com',
            full_name='Test User',
            role='editor',
            department='IT'
        )

        assert user is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'
        assert user.role == 'editor'
        assert user.department == 'IT'
        assert user.is_active is True

        # 비밀번호는 해시되어야 함
        assert user.password_hash != 'password123'
        assert len(user.password_hash) > 20  # 해시 길이 확인

    def test_create_user_default_role(self, db_session):
        """기본 역할로 사용자 생성"""
        user = AuthService.create_user(
            db=db_session,
            username='vieweruser',
            password='password123'
        )

        assert user.role == 'viewer'  # 기본값

    def test_create_duplicate_user(self, db_session):
        """중복 사용자명 - 예외 발생"""
        AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        with pytest.raises(ValueError) as exc_info:
            AuthService.create_user(
                db=db_session,
                username='testuser',
                password='password456'
            )

        assert "이미 존재하는 사용자명" in str(exc_info.value)

    def test_authenticate_success(self, db_session):
        """인증 성공"""
        AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        user = AuthService.authenticate(
            db=db_session,
            username='testuser',
            password='password123'
        )

        assert user is not None
        assert user.username == 'testuser'
        assert user.last_login is not None  # 로그인 시간 업데이트

    def test_authenticate_wrong_password(self, db_session):
        """인증 실패 - 잘못된 비밀번호"""
        AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        user = AuthService.authenticate(
            db=db_session,
            username='testuser',
            password='wrongpassword'
        )

        assert user is None

    def test_authenticate_nonexistent_user(self, db_session):
        """인증 실패 - 존재하지 않는 사용자"""
        user = AuthService.authenticate(
            db=db_session,
            username='nonexistent',
            password='password123'
        )

        assert user is None

    def test_authenticate_inactive_user(self, db_session):
        """인증 실패 - 비활성화된 사용자"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 사용자 비활성화
        AuthService.deactivate_user(db=db_session, user_id=user.id)

        # 비활성화된 사용자는 인증 불가
        auth_user = AuthService.authenticate(
            db=db_session,
            username='testuser',
            password='password123'
        )

        assert auth_user is None

    def test_grant_permission(self, db_session):
        """권한 부여"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        perm = AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write',
            granted_by=user.id
        )

        assert perm is not None
        assert perm.user_id == user.id
        assert perm.resource == 'blends'
        assert perm.action == 'write'
        assert perm.granted_by == user.id

    def test_grant_duplicate_permission(self, db_session):
        """중복 권한 부여 - 기존 권한 반환"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 첫 번째 권한 부여
        perm1 = AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        # 동일한 권한 재부여
        perm2 = AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        assert perm1.id == perm2.id  # 같은 권한 객체

    def test_has_permission(self, db_session):
        """권한 확인"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        # 권한 확인
        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        assert has_perm is True

        # 없는 권한 확인
        has_write = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='beans',
            action='delete'
        )

        assert has_write is False

    def test_admin_has_all_permissions(self, db_session):
        """Admin 역할은 모든 권한 보유"""
        admin = AuthService.create_user(
            db=db_session,
            username='admin',
            password='password123',
            role='admin'
        )

        # 권한을 명시적으로 부여하지 않아도 모든 권한 보유
        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=admin.id,
            resource='any_resource',
            action='any_action'
        )

        assert has_perm is True

    def test_has_permission_inactive_user(self, db_session):
        """비활성화된 사용자의 권한 확인 - False 반환"""
        # Admin 생성 (권한 부여자)
        admin = AuthService.create_user(
            db=db_session,
            username='admin',
            password='password123',
            role='admin'
        )

        # 일반 사용자 생성
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='beans',
            action='read',
            granted_by=admin.id
        )

        # 사용자 비활성화
        AuthService.deactivate_user(db=db_session, user_id=user.id)

        # 비활성화된 사용자는 권한이 있어도 False 반환
        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='beans',
            action='read'
        )

        assert has_perm is False

    def test_revoke_permission(self, db_session):
        """권한 취소"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        # 권한 취소
        result = AuthService.revoke_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        assert result is True

        # 권한 재확인
        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        assert has_perm is False

    def test_revoke_nonexistent_permission(self, db_session):
        """존재하지 않는 권한 취소 - False 반환"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        result = AuthService.revoke_permission(
            db=db_session,
            user_id=user.id,
            resource='nonexistent',
            action='delete'
        )

        assert result is False

    def test_get_user_permissions(self, db_session):
        """사용자 권한 조회"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        perms = AuthService.get_user_permissions(db=db_session, user_id=user.id)

        # 기본 권한 3개 (blends:read, beans:read, roasting_logs:read)
        assert len(perms) >= 3
        assert any(p['resource'] == 'blends' and p['action'] == 'read' for p in perms)

    def test_change_password_success(self, db_session):
        """비밀번호 변경 성공"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='oldpassword'
        )

        result = AuthService.change_password(
            db=db_session,
            user_id=user.id,
            old_password='oldpassword',
            new_password='newpassword'
        )

        assert result is True

        # 새 비밀번호로 인증 확인
        auth_user = AuthService.authenticate(
            db=db_session,
            username='testuser',
            password='newpassword'
        )

        assert auth_user is not None

        # 기존 비밀번호로는 인증 실패
        old_auth = AuthService.authenticate(
            db=db_session,
            username='testuser',
            password='oldpassword'
        )

        assert old_auth is None

    def test_change_password_wrong_old_password(self, db_session):
        """비밀번호 변경 실패 - 잘못된 기존 비밀번호"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        result = AuthService.change_password(
            db=db_session,
            user_id=user.id,
            old_password='wrongpassword',
            new_password='newpassword'
        )

        assert result is False

    def test_change_password_nonexistent_user(self, db_session):
        """비밀번호 변경 실패 - 존재하지 않는 사용자"""
        result = AuthService.change_password(
            db=db_session,
            user_id=999,  # 존재하지 않는 ID
            old_password='oldpass',
            new_password='newpass'
        )

        assert result is False

    def test_deactivate_user(self, db_session):
        """사용자 비활성화"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        result = AuthService.deactivate_user(db=db_session, user_id=user.id)
        assert result is True

        # 비활성화된 사용자 확인
        deactivated_user = AuthService.get_user_by_id(db=db_session, user_id=user.id)
        assert deactivated_user.is_active is False

    def test_deactivate_nonexistent_user(self, db_session):
        """사용자 비활성화 실패 - 존재하지 않는 사용자"""
        result = AuthService.deactivate_user(db=db_session, user_id=999)
        assert result is False

    def test_get_user_by_username(self, db_session):
        """사용자명으로 조회"""
        AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        user = AuthService.get_user_by_username(db=db_session, username='testuser')
        assert user is not None
        assert user.username == 'testuser'

    def test_get_user_by_username_not_found(self, db_session):
        """사용자명으로 조회 - 없음"""
        user = AuthService.get_user_by_username(db=db_session, username='nonexistent')
        assert user is None

    def test_get_user_by_id(self, db_session):
        """ID로 조회"""
        created = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        user = AuthService.get_user_by_id(db=db_session, user_id=created.id)
        assert user is not None
        assert user.id == created.id
        assert user.username == 'testuser'

    def test_list_all_users(self, db_session):
        """모든 사용자 조회"""
        for i in range(3):
            AuthService.create_user(
                db=db_session,
                username=f'user{i}',
                password='password123'
            )

        users = AuthService.list_all_users(db=db_session)
        assert len(users) == 3

    def test_list_all_users_active_only(self, db_session):
        """활성 사용자만 조회"""
        # 3명 생성
        user_ids = []
        for i in range(3):
            user = AuthService.create_user(
                db=db_session,
                username=f'user{i}',
                password='password123'
            )
            user_ids.append(user.id)

        # 1명 비활성화
        AuthService.deactivate_user(db=db_session, user_id=user_ids[0])

        # 활성 사용자만 조회
        active_users = AuthService.list_all_users(db=db_session, active_only=True)
        assert len(active_users) == 2

        # 모든 사용자 조회
        all_users = AuthService.list_all_users(db=db_session, active_only=False)
        assert len(all_users) == 3

    def test_default_permissions_granted(self, db_session):
        """기본 권한 자동 설정 확인"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 기본 읽기 권한 확인
        has_blend_read = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='read'
        )
        assert has_blend_read is True

        has_bean_read = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='beans',
            action='read'
        )
        assert has_bean_read is True

        has_log_read = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='roasting_logs',
            action='read'
        )
        assert has_log_read is True


@pytest.mark.integration
class TestAuthServiceIntegration:
    """AuthService 통합 테스트"""

    def test_user_auth_workflow(self, db_session):
        """사용자 인증 워크플로우"""
        # 1. 사용자 생성
        user = AuthService.create_user(
            db=db_session,
            username='workflowuser',
            password='password123',
            role='editor'
        )

        # 2. 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write',
            granted_by=user.id
        )

        # 3. 인증 시도
        auth_user = AuthService.authenticate(
            db=db_session,
            username='workflowuser',
            password='password123'
        )
        assert auth_user is not None

        # 4. 권한 확인
        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=auth_user.id,
            resource='blends',
            action='write'
        )
        assert has_perm is True

    def test_permission_lifecycle(self, db_session):
        """권한 생명주기 테스트"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123'
        )

        # 1. 권한 부여
        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='test_resource',
            action='test_action',
            granted_by=user.id
        )

        # 2. 권한 확인
        assert AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='test_resource',
            action='test_action'
        ) is True

        # 3. 권한 취소
        AuthService.revoke_permission(
            db=db_session,
            user_id=user.id,
            resource='test_resource',
            action='test_action'
        )

        # 4. 취소 확인
        assert AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='test_resource',
            action='test_action'
        ) is False
