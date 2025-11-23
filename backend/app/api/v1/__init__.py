"""
API v1 라우터

모든 v1 API 엔드포인트를 통합하는 메인 라우터
"""
from fastapi import APIRouter
from app.api.v1.endpoints import beans_router

api_router = APIRouter()

# 각 엔드포인트 라우터 등록
api_router.include_router(beans_router)

__all__ = ["api_router"]
