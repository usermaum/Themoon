from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from .base import Base

class CostSetting(Base):
    """비용 설정"""
    __tablename__ = "cost_settings"

    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String(100), unique=True, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CostSetting({self.parameter_name}={self.value})>"
