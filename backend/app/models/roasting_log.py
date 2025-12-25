from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.timezone import get_kst_now


class RoastingLog(Base):
    """로스팅 생산 배치 기록"""
    __tablename__ = "roasting_logs"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String(50), unique=True, index=True, comment="생산 배치 번호")
    roast_date = Column(DateTime(timezone=True), default=get_kst_now, comment="로스팅 일시")

    target_bean_id = Column(Integer, ForeignKey("beans.id"), nullable=False, comment="생산된 원두 ID")
    
    input_weight_total = Column(Float, nullable=False, comment="총 투입량 (kg)")
    output_weight_total = Column(Float, nullable=False, comment="총 생산량 (kg)")
    
    loss_rate = Column(Float, nullable=True, comment="손실률 (%)")
    production_cost = Column(Float, nullable=True, comment="총 투입 생두 원가")

    notes = Column(Text, nullable=True, comment="비고")
    created_at = Column(DateTime(timezone=True), default=get_kst_now)

    # Relationships
    target_bean = relationship("app.models.bean.Bean", foreign_keys=[target_bean_id])
    inventory_logs = relationship("app.models.inventory_log.InventoryLog", back_populates="roasting_log")
