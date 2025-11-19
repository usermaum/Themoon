"""
데이터베이스 설정 및 초기화 (Deprecated)
이 파일은 하위 호환성을 위해 유지되며, 실제 정의는 개별 파일로 분리되었습니다.
"""

from .base import Base, engine, SessionLocal, init_db, get_db, reset_db
from .bean import Bean, BeanPriceHistory
from .blend import Blend, BlendRecipe, BlendRecipesHistory
from .inventory import Inventory
from .transaction import Transaction, RoastingLog, LossRateWarning
from .cost_setting import CostSetting
from .user import User, UserPermission, AuditLog

# Invoice 관련 모델 (순환 참조 주의)
from .invoice import Invoice, InvoiceItem, InvoiceLearning

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "init_db",
    "get_db",
    "reset_db",
    "Bean",
    "BeanPriceHistory",
    "Blend",
    "BlendRecipe",
    "BlendRecipesHistory",
    "Inventory",
    "Transaction",
    "RoastingLog",
    "LossRateWarning",
    "CostSetting",
    "User",
    "UserPermission",
    "AuditLog",
    "Invoice",
    "InvoiceItem",
    "InvoiceLearning"
]
