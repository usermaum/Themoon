from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RoastingLog(Base):
    __tablename__ = "roasting_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Input (Green Bean)
    green_bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    input_quantity = Column(Float, nullable=False, comment="투입량 (kg)")
    
    # Output (Roasted Bean)
    roasted_bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False)
    output_quantity = Column(Float, nullable=False, comment="생산량 (kg)")
    
    # Performance
    loss_rate = Column(Float, nullable=False, comment="손실률 (%)")
    
    # Time
    roast_date = Column(DateTime(timezone=True), server_default=func.current_timestamp(), comment="로스팅 일시")
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

    # Note
    note = Column(String(255), nullable=True)

    # Relationships
    green_bean = relationship("Bean", foreign_keys=[green_bean_id], backref="roastings_as_green")
    roasted_bean = relationship("Bean", foreign_keys=[roasted_bean_id], backref="roastings_as_roasted")
