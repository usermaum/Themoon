"""
API v1 라우터

모든 v1 API 엔드포인트를 통합하는 메인 라우터
"""
from fastapi import APIRouter

api_router = APIRouter()

__all__ = ["api_router"]
