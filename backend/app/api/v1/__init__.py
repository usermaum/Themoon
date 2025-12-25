"""
API v1 라우터

모든 v1 API 엔드포인트를 통합하는 메인 라우터
"""

from fastapi import APIRouter

from app.api.v1 import analytics, blends, roasting
from app.api.v1.endpoints import settings, beans, dashboard, inbound, inventory_logs

api_router = APIRouter()
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(beans.router, prefix="/beans", tags=["beans"])
api_router.include_router(roasting.router, prefix="/roasting", tags=["roasting"])
api_router.include_router(blends.router, prefix="/blends", tags=["blends"])
api_router.include_router(inventory_logs.router, prefix="/inventory-logs", tags=["inventory-logs"])
api_router.include_router(inbound.router, prefix="/inbound", tags=["inbound"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
