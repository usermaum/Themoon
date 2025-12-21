from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1 import beans, roasting, blends, analytics
from app.api.v1.endpoints import inbound, inventory_logs, dashboard
from app.database import engine, Base
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트"""
    # 시작 시: 데이터베이스 테이블 생성
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # 초기 데이터 시딩 (개발 편의성)
    try:
        from app.database import SessionLocal
        from app.models.bean import Bean
        # 경로 문제 회피를 위해 동적 임포트 시도 또는 직접 로직 구현
        # 여기서는 간단히 카운트 체크 후 스크립트 모듈 import 시도
        db = SessionLocal()
        if db.query(Bean).count() == 0:
            print("🌱 No beans found. Seeding initial data...")
            # recreate_db 모듈이 scripts에 있으므로 import가 까다로울 수 있음
            # 직접 시딩 로직을 간소화하여 실행하거나 외부에 위임
            # 여기서는 편의를 위해 recreate_db 스크립트가 실행될 수 없으므로(import path), 
            # 핵심 데이터 1개만 샘플로 넣거나 생략하고 로그만 남김.
            # 하지만 recreate_db.py를 app 패키지 내로 옮기지 않았으므로 import 불가.
            # 따라서 사용자가 직접 실행하라는 로그를 남김.
            print("⚠️  To seed data, run: python backend/scripts/recreate_db.py")
        db.close()
    except Exception as e:
        print(f"⚠️  Auto-seeding check failed: {e}")
        
    yield
    # 종료 시: 정리 작업 (필요시)
    print("👋 Shutting down...")


app = FastAPI(
    title="The Moon Drip Bar API",
    description="Roasting Management System API",
    version="0.4.0",
    lifespan=lifespan,
)

# CORS 설정
# CORS 설정 (개발 환경 강력 허용)
origins = [
    "http://localhost:3000",
    "http://localhost:3500",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3500",
    "*"  # 개발 편의를 위해 모든 Origin 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록 (중앙 라우터 사용)
app.include_router(beans.router, prefix="/api/v1/beans", tags=["beans"])
app.include_router(inbound.router, prefix="/api/v1/inbound", tags=["inbound"])
app.include_router(inventory_logs.router, prefix="/api/v1/inventory-logs", tags=["inventory-logs"])
app.include_router(roasting.router, prefix="/api/v1/roasting", tags=["roasting"])
app.include_router(blends.router, prefix="/api/v1/blends", tags=["blends"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to The Moon Drip Bar API"}

from fastapi.staticfiles import StaticFiles
import os

# Create static directory if not exists
os.makedirs("static/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health_check():
    """Health check endpoint for Render.com"""
    return {"status": "healthy", "service": "themoon-api"}
