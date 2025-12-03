from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Recipe(Base):
    """블렌딩 레시피 모델"""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    
    # 블렌드 제품 (Beans 테이블의 type=BLEND 인 항목)
    blend_bean_id = Column(Integer, ForeignKey('beans.id'), nullable=False, comment="블렌드 제품 ID")
    
    # 재료 원두 (Beans 테이블의 원두)
    ingredient_bean_id = Column(Integer, ForeignKey('beans.id'), nullable=False, comment="재료 원두 ID")
    
    # 배합 비율 (%)
    ratio_percent = Column(Float, nullable=False, comment="배합 비율 (%)")

    # Relationships
    blend_bean = relationship("Bean", foreign_keys=[blend_bean_id], backref="recipes")
    ingredient_bean = relationship("Bean", foreign_keys=[ingredient_bean_id])

    def __repr__(self):
        return f"<Recipe(blend_id={self.blend_bean_id}, ingredient_id={self.ingredient_bean_id}, ratio={self.ratio_percent}%)>"
