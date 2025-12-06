"""
API v1 라우터

모든 v1 API 엔드포인트를 통합하는 메인 라우터
"""
from fastapi import APIRouter
from app.api.v1 import beans, roasting

api_router = APIRouter()
api_router.include_router(beans.router, prefix="/beans", tags=["beans"])
api_router.include_router(roasting.router, prefix="/roasting", tags=["roasting"])
