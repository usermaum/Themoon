from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import beans, blends, inventory_logs, dashboard
from app.database import engine, Base
from app.models import bean, blend, inventory_log
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트"""
    # 시작 시: 데이터베이스 테이블 생성
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    yield
    # 종료 시: 정리 작업 (필요시)
    print("👋 Shutting down...")


app = FastAPI(
    title="The Moon Drip Bar API",
    description="Roasting Management System API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(beans.router, prefix="/api/v1/beans", tags=["beans"])
app.include_router(blends.router, prefix="/api/v1/blends", tags=["blends"])
app.include_router(inventory_logs.router, prefix="/api/v1/inventory-logs", tags=["inventory"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to The Moon Drip Bar API"}

@app.get("/health")
def health_check():
    """Health check endpoint for Render.com"""
    return {"status": "healthy", "service": "themoon-api"}
