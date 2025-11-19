from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Inventory(Base):
    """재고 관리"""
    __tablename__ = "inventory"
    __table_args__ = (
        # (bean_id, inventory_type) 조합을 unique로 설정
        UniqueConstraint('bean_id', 'inventory_type', name='_bean_inventory_type_uc'),
    )

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    inventory_type = Column(String(20), nullable=False, default="RAW_BEAN")  # RAW_BEAN(생두), ROASTED_BEAN(원두)
    quantity_kg = Column(Float, default=0.0)  # 현재 재고 (kg)
    min_quantity_kg = Column(Float, default=5.0)  # 최소 재고
    max_quantity_kg = Column(Float, default=50.0)  # 최대 재고
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    bean = relationship("Bean", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory(bean_id={self.bean_id}, type={self.inventory_type}, qty={self.quantity_kg}kg)>"
