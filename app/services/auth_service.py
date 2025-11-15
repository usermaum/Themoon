"""
AuthService: 인증 및 권한 관리 서비스

사용자 생성, 인증, 권한 관리를 담당합니다.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.database import User, UserPermission
from passlib.context import CryptContext
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """인증 및 권한 관리 서비스"""

    @staticmethod
    def create_user(
        db: Session,
        username: str,
        password: str,
        email: str = None,
        full_name: str = None,
        role: str = 'viewer',
        department: str = None
    ) -> User:
        """
        사용자 생성

        Args:
            db: SQLAlchemy 세션
            username: 사용자명 (유일)
            password: 비밀번호 (해싱됨)
            email: 이메일 주소
            full_name: 전체 이름
            role: 역할 ('viewer', 'editor', 'admin')
            department: 부서

        Returns:
            생성된 User 객체

        Raises:
            ValueError: 사용자명이 이미 존재하는 경우
        """

        # 중복 확인
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError(f"이미 존재하는 사용자명: {username}")

        # 비밀번호 해싱
        password_hash = pwd_context.hash(password)

        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            full_name=full_name,
            role=role,
            department=department,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # 기본 권한 설정 (모든 사용자가 읽기 권한 보유)
        default_permissions = [
            ('blends', 'read'),
            ('beans', 'read'),
            ('roasting_logs', 'read'),
        ]

        for resource, action in default_permissions:
            AuthService.grant_permission(db, user.id, resource, action, user.id)

        logger.info(f"✓ 사용자 생성: {username} (역할: {role})")

        return user

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> User:
        """
        사용자 인증

        Args:
            db: SQLAlchemy 세션
            username: 사용자명
            password: 비밀번호

        Returns:
            인증된 User 객체 또는 None
        """
        user = db.query(User).filter(
            and_(User.username == username, User.is_active == True)
        ).first()

        if not user:
            logger.warning(f"⚠️ 인증 실패: 사용자 없음 ({username})")
            return None

        # 비밀번호 검증
        if not pwd_context.verify(password, user.password_hash):
            logger.warning(f"⚠️ 인증 실패: 잘못된 비밀번호 ({username})")
            return None

        # 마지막 로그인 시간 업데이트
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)

        logger.info(f"✓ 인증 성공: {username}")

        return user

    @staticmethod
    def grant_permission(
        db: Session,
        user_id: int,
        resource: str,
        action: str,
        granted_by: int
    ) -> UserPermission:
        """
        사용자에게 권한 부여

        Args:
            db: SQLAlchemy 세션
            user_id: 대상 사용자 ID
            resource: 리소스명 (예: 'blends', 'beans')
            action: 동작 (예: 'read', 'write', 'delete')
            granted_by: 권한 부여자 사용자 ID

        Returns:
            생성된 UserPermission 객체
        """

        # 기존 권한 확인
        existing = db.query(UserPermission).filter(
            and_(
                UserPermission.user_id == user_id,
                UserPermission.resource == resource,
                UserPermission.action == action
            )
        ).first()

        if existing:
            logger.info(f"ℹ️ 이미 존재하는 권한: user_id={user_id}, {resource}:{action}")
            return existing

        permission = UserPermission(
            user_id=user_id,
            resource=resource,
            action=action,
            granted_by=granted_by
        )

        db.add(permission)
        db.commit()
        db.refresh(permission)

        logger.info(f"✓ 권한 부여: user_id={user_id}, {resource}:{action}")

        return permission

    @staticmethod
    def revoke_permission(
        db: Session,
        user_id: int,
        resource: str,
        action: str
    ) -> bool:
        """
        사용자 권한 취소

        Args:
            db: SQLAlchemy 세션
            user_id: 대상 사용자 ID
            resource: 리소스명
            action: 동작

        Returns:
            취소 성공 여부
        """

        permission = db.query(UserPermission).filter(
            and_(
                UserPermission.user_id == user_id,
                UserPermission.resource == resource,
                UserPermission.action == action
            )
        ).first()

        if not permission:
            logger.warning(f"⚠️ 권한을 찾을 수 없음: user_id={user_id}, {resource}:{action}")
            return False

        db.delete(permission)
        db.commit()

        logger.info(f"✓ 권한 취소: user_id={user_id}, {resource}:{action}")

        return True

    @staticmethod
    def has_permission(
        db: Session,
        user_id: int,
        resource: str,
        action: str
    ) -> bool:
        """
        사용자 권한 확인

        Args:
            db: SQLAlchemy 세션
            user_id: 사용자 ID
            resource: 리소스명
            action: 동작

        Returns:
            권한 보유 여부
        """

        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            return False

        # Admin은 모든 권한 보유
        if user.role == 'admin':
            return True

        # 특정 권한 확인
        permission = db.query(UserPermission).filter(
            and_(
                UserPermission.user_id == user_id,
                UserPermission.resource == resource,
                UserPermission.action == action
            )
        ).first()

        return permission is not None

    @staticmethod
    def get_user_permissions(
        db: Session,
        user_id: int
    ) -> list:
        """
        사용자의 모든 권한 조회

        Args:
            db: SQLAlchemy 세션
            user_id: 사용자 ID

        Returns:
            권한 정보 리스트
        """

        permissions = db.query(UserPermission).filter(
            UserPermission.user_id == user_id
        ).all()

        return [{
            'id': p.id,
            'resource': p.resource,
            'action': p.action,
            'granted_date': p.granted_date
        } for p in permissions]

    @staticmethod
    def change_password(
        db: Session,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        사용자 비밀번호 변경

        Args:
            db: SQLAlchemy 세션
            user_id: 사용자 ID
            old_password: 기존 비밀번호
            new_password: 새 비밀번호

        Returns:
            변경 성공 여부
        """

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"⚠️ 사용자를 찾을 수 없음: {user_id}")
            return False

        # 기존 비밀번호 확인
        if not pwd_context.verify(old_password, user.password_hash):
            logger.warning(f"⚠️ 비밀번호 변경 실패: 잘못된 기존 비밀번호 (user_id={user_id})")
            return False

        # 새 비밀번호로 변경
        user.password_hash = pwd_context.hash(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()

        logger.info(f"✓ 비밀번호 변경: {user.username}")

        return True

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """
        사용자 비활성화

        Args:
            db: SQLAlchemy 세션
            user_id: 사용자 ID

        Returns:
            비활성화 성공 여부
        """

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.commit()

        logger.info(f"✓ 사용자 비활성화: {user.username}")

        return True

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """
        사용자명으로 사용자 조회

        Args:
            db: SQLAlchemy 세션
            username: 사용자명

        Returns:
            User 객체 또는 None
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        ID로 사용자 조회

        Args:
            db: SQLAlchemy 세션
            user_id: 사용자 ID

        Returns:
            User 객체 또는 None
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def list_all_users(db: Session, active_only: bool = True) -> list:
        """
        모든 사용자 조회

        Args:
            db: SQLAlchemy 세션
            active_only: 활성 사용자만 조회 여부

        Returns:
            사용자 정보 리스트
        """

        query = db.query(User)
        if active_only:
            query = query.filter(User.is_active == True)

        users = query.all()

        return [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'full_name': u.full_name,
            'role': u.role,
            'is_active': u.is_active,
            'last_login': u.last_login,
            'created_at': u.created_at
        } for u in users]
