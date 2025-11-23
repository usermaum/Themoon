"""
FastAPI 메인 애플리케이션

원본 참조: /mnt/d/Ai/WslProject/TheMoon_Project/app/app.py
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import Bean  # Import all models here
from app.api.v1 import api_router

app = FastAPI(
    title="TheMoon API",
    description="커피 로스팅 원가 계산 시스템",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 데이터베이스 테이블 생성"""
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "TheMoon API v1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")
