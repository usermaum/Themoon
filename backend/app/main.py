from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import beans, blends, inventory_logs
from app.database import engine, Base
from app.models import bean, blend, inventory_log
from app.config import settings

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="The Moon Drip Bar API",
    description="Roasting Management System API",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(beans.router, prefix="/api/v1/beans", tags=["beans"])
app.include_router(blends.router, prefix="/api/v1/blends", tags=["blends"])
app.include_router(inventory_logs.router, prefix="/api/v1/inventory-logs", tags=["inventory"])

@app.get("/")
def read_root():
    return {"message": "Welcome to The Moon Drip Bar API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "themoon-api"}
