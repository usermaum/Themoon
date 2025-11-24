from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Blend(Base):
    __tablename__ = "blends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # 레시피 정보 (JSON 형태로 저장: [{"bean_id": 1, "ratio": 0.4}, ...])
    # 실제 운영 환경에서는 별도의 BlendItem 테이블로 정규화하는 것이 좋으나,
    # MVP 단계에서는 JSON으로 간단하게 처리합니다.
    recipe = Column(JSON, nullable=False)
    
    target_roast_level = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
