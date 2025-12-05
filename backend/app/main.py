from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.endpoints import beans, blends, inventory_logs, dashboard, roasting, inbound
from app.database import engine, Base
from app.models import bean, blend, inventory_log, roasting_log
from app.config import settings

# ... (middle parts unchanged)

# API 라우터 등록
app.include_router(beans.router, prefix="/api/v1/beans", tags=["beans"])
app.include_router(blends.router, prefix="/api/v1/blends", tags=["blends"])
app.include_router(inventory_logs.router, prefix="/api/v1/inventory-logs", tags=["inventory"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(roasting.router, prefix="/api/v1/roasting", tags=["roasting"])
app.include_router(inbound.router, prefix="/api/v1/inbound", tags=["inbound"])

@app.get("/")
def read_root():
    return {"message": "Welcome to The Moon Drip Bar API"}

@app.get("/health")
def health_check():
    """Health check endpoint for Render.com"""
    return {"status": "healthy", "service": "themoon-api"}
