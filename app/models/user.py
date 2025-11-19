from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from .base import Base

class User(Base):
    """사용자 관리"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)

    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default='viewer')  # viewer, editor, admin
    department = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"


class UserPermission(Base):
    """사용자 권한"""
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)

    granted_date = Column(DateTime, default=datetime.utcnow)
    granted_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<UserPermission(user_id={self.user_id}, resource={self.resource}, action={self.action})>"


class AuditLog(Base):
    """감사 로그"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, EXPORT
    resource_type = Column(String(255), nullable=False)
    resource_id = Column(Integer, nullable=True)

    old_values = Column(Text, nullable=True)  # JSON
    new_values = Column(Text, nullable=True)  # JSON
    description = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog(action={self.action_type}, resource={self.resource_type}, id={self.resource_id})>"
