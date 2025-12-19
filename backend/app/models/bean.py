"""
Bean 모델 - 원두 정보 관리
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""
import enum
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from app.database import Base
from app.utils.timezone import get_kst_now


class BeanType(str, enum.Enum):
    """원두 유형 (생두/원두/블렌드)"""
    GREEN_BEAN = "GREEN_BEAN"      # 생두
    ROASTED_BEAN = "ROASTED_BEAN"  # 싱글 오리진 원두
    BLEND_BEAN = "BLEND_BEAN"      # 블렌드 원두


class RoastProfile(str, enum.Enum):
    """로스팅 프로필 (신콩/탄콩)"""
    LIGHT = "LIGHT"   # 신콩 (약~중볶음, 산미)
    MEDIUM = "MEDIUM" # (사용 여부 검토 필요, 현재는 LIGHT/DARK 위주)
    DARK = "DARK"     # 탄콩 (강볶음, 바디감)


class Bean(Base):
    """
    원두 통합 모델
    - 생두, 싱글 오리진 원두, 블렌드 원두를 하나의 테이블에서 관리
    - type 컬럼으로 구분
    """
    __tablename__ = "beans"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # --- 핵심 식별 정보 ---
    name = Column(String(100), nullable=False, index=True, comment="품목명 (Legacy/대표명)")
    type = Column(Enum(BeanType), nullable=False, default=BeanType.GREEN_BEAN, comment="품목 유형")
    sku = Column(String(100), unique=True, index=True, comment="SKU 코드 (예: Yirga-LIGHT)")

    # --- 다국어 지원 (New) ---
    name_ko = Column(String(100), index=True, nullable=True, comment="품목명(한글)")
    name_en = Column(String(200), index=True, nullable=True, comment="품목명(영문)")

    # --- 생두 정보 (Green Bean) ---
    origin = Column(String(100), nullable=True, comment="원산지 (Legacy/국가코드)")
    origin_ko = Column(String(50), index=True, nullable=True, comment="원산지(한글)")
    origin_en = Column(String(50), index=True, nullable=True, comment="원산지(영문)")
    
    variety = Column(String(50), nullable=True, comment="품종")
    grade = Column(String(50), nullable=True, comment="등급 (G1, G2, AA 등)")
    processing_method = Column(String(50), nullable=True, comment="가공 방식")
    
    # --- 원두 정보 (Roasted Bean) ---
    roast_profile = Column(Enum(RoastProfile), nullable=True, comment="로스팅 프로필 (신콩/탄콩)")
    parent_bean_id = Column(Integer, ForeignKey('beans.id'), nullable=True, comment="원재료 생두 ID")
    
    # --- 재고 및 가격 정보 ---
    quantity_kg = Column(Float, default=0.0, nullable=False, comment="현재 재고량 (kg)")
    avg_price = Column(Float, default=0.0, nullable=False, comment="kg당 평균 단가 (매입가/원가)")
    purchase_price_per_kg = Column(Float, nullable=True, comment="최근 매입가 (참조용)")
    cost_price = Column(Float, nullable=True, comment="생산 원가 (로스팅 비용 포함)")
    
    # --- 메타 데이터 ---
    description = Column(Text, nullable=True, comment="설명")
    notes = Column(Text, nullable=True, comment="내부 메모")
    
    # 예상 로스팅 손실률 (Pre-roast Blending 계산용)
    expected_loss_rate = Column(Float, default=0.15, nullable=False, comment="예상 로스팅 손실률 (0.0 ~ 1.0)")
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), default=get_kst_now)
    updated_at = Column(DateTime(timezone=True), default=get_kst_now, onupdate=get_kst_now)

    # --- Relationships ---
    # Self-referential relationship (원두 -> 생두)
    parent_bean = relationship("Bean", remote_side=[id], backref=backref("roasted_variants", lazy="dynamic"))
    
    # 재고 로그
    inventory_logs = relationship("InventoryLog", back_populates="bean", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bean(id={self.id}, name='{self.name}', type='{self.type}', sku='{self.sku}')>"
