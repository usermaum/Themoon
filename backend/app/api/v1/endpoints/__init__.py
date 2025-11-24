"""
API v1 엔드포인트

모든 v1 API 라우터를 여기서 통합
"""
from app.api.v1.endpoints import beans
from app.api.v1.endpoints import blends
from app.api.v1.endpoints import inventory_logs

__all__ = ["beans", "blends", "inventory_logs"]
