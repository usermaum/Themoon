from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Blend(Base):
    """블렌드 모델"""
    __tablename__ = "blends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    blend_type = Column(String(20), nullable=False)  # 풀문, 뉴문, 시즈널
    description = Column(Text, nullable=True)
    total_portion = Column(Integer, default=0)
    suggested_price = Column(Float, default=0.0)
    status = Column(String(20), default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    recipes = relationship("BlendRecipe", back_populates="blend", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="blend", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Blend(name={self.name}, type={self.blend_type})>"


class BlendRecipe(Base):
    """블렌드 구성 (다대다)"""
    __tablename__ = "blend_recipes"

    id = Column(Integer, primary_key=True, index=True)
    blend_id = Column(Integer, ForeignKey("blends.id"), nullable=False)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    portion_count = Column(Integer, nullable=False)  # 포션 개수
    ratio = Column(Float, default=0.0)  # 비율 (%)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    blend = relationship("Blend", back_populates="recipes")
    bean = relationship("Bean", back_populates="blend_recipes")

    def __repr__(self):
        return f"<BlendRecipe(blend_id={self.blend_id}, bean_id={self.bean_id}, portion={self.portion_count})>"


class BlendRecipesHistory(Base):
    """블렌드 레시피 버전 관리"""
    __tablename__ = "blend_recipes_history"

    id = Column(Integer, primary_key=True, index=True)
    blend_id = Column(Integer, ForeignKey("blends.id"), nullable=False)
    version = Column(Integer, nullable=False)
    blending_ratio_percent = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
    obsolete_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=True)

    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    bean_name = Column(String(255), nullable=True)
    change_reason = Column(Text, nullable=True)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BlendRecipesHistory(blend_id={self.blend_id}, version={self.version}, ratio={self.blending_ratio_percent}%)>"
