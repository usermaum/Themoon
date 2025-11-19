from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    """거래 기록 (판매/사용)"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    blend_id = Column(Integer, ForeignKey("blends.id"), nullable=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=True)
    transaction_type = Column(String(20), nullable=False)  # PURCHASE(입고), ROASTING(로스팅), PRODUCTION(생산), SALES(판매출고), GIFT(증정), WASTE(폐기), ADJUSTMENT(재고조정)

    # 재고 관리 고도화 필드
    inventory_type = Column(String(20), nullable=True)  # RAW_BEAN(생두), ROASTED_BEAN(원두) - 어떤 재고에 영향?
    roasting_log_id = Column(Integer, ForeignKey("roasting_logs.id"), nullable=True)  # 로스팅 기록 연결
    invoice_item_id = Column(Integer, nullable=True)  # 거래 명세서 항목 ID (InvoiceItem 연결)

    quantity_kg = Column(Float, nullable=False)
    price_per_unit = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    user_id = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    blend = relationship("Blend", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(type={self.transaction_type}, qty={self.quantity_kg}, amount={self.total_amount})>"


class RoastingLog(Base):
    """로스팅 기록"""
    __tablename__ = "roasting_logs"

    id = Column(Integer, primary_key=True, index=True)
    bean_id = Column(Integer, ForeignKey("beans.id"), nullable=True)  # 원두 ID
    raw_weight_kg = Column(Float, nullable=False)  # 생두 투입량
    roasted_weight_kg = Column(Float, nullable=False)  # 로스팅 후 무게
    loss_rate_percent = Column(Float, nullable=False)  # 손실률 (자동 계산)
    expected_loss_rate_percent = Column(Float, default=17.0)  # 예상 손실률
    loss_variance_percent = Column(Float, nullable=True)  # 손실률 편차

    roasting_date = Column(Date, nullable=False)  # 로스팅 날짜
    roasting_month = Column(String(7), nullable=True)  # YYYY-MM

    notes = Column(Text, nullable=True)  # 로스팅 노트
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    bean = relationship("Bean", backref="roasting_logs")
    warnings = relationship("LossRateWarning", back_populates="roasting_log", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RoastingLog(date={self.roasting_date}, raw={self.raw_weight_kg}kg, loss={self.loss_rate_percent}%)>"


class LossRateWarning(Base):
    """손실률 이상 경고"""
    __tablename__ = "loss_rate_warnings"

    id = Column(Integer, primary_key=True, index=True)
    roasting_log_id = Column(Integer, ForeignKey("roasting_logs.id"), nullable=False)
    warning_type = Column(String(50), nullable=True)  # HIGH, LOW, TREND
    severity = Column(String(50), nullable=True)  # INFO, WARNING, CRITICAL

    variance_from_expected = Column(Float, nullable=True)
    consecutive_occurrences = Column(Integer, default=1)

    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # 관계
    roasting_log = relationship("RoastingLog", back_populates="warnings")

    def __repr__(self):
        return f"<LossRateWarning(log_id={self.roasting_log_id}, severity={self.severity})>"
