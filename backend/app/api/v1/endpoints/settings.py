from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser
from app.schemas.config import SystemConfig
from app.services.config_service import config_service
from app.config import settings, _ROOT_DIR
import json
import os
import shutil
import subprocess
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class MemoCreate(BaseModel):
    content: str

class MemoUpdate(BaseModel):
    status: Optional[str] = None
    admin_reply: Optional[str] = None

class Memo(BaseModel):
    id: int
    content: str
    created_at: str
    status: str = "pending"
    admin_reply: Optional[str] = None

router = APIRouter()


@router.get("/config", response_model=SystemConfig)
def get_system_config(
    # current_user=Depends(get_current_active_superuser),
):
    """
    [Admin] 시스템 설정 전체 조회
    """
    return config_service.get_system_config()


@router.put("/config", response_model=SystemConfig)
def update_system_config(
    config: SystemConfig,
    # current_user=Depends(get_current_active_superuser),
):
    """
    [Admin] 시스템 설정 업데이트 (Hot-reload)
    """
    try:
        config_service.save_config(config)
        return config_service.get_system_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save config: {str(e)}")


# --- Observability Endpoints ---

from fastapi import WebSocket, WebSocketDisconnect
from app.repositories.system_repository import SystemRepository
from app.services.system_monitoring_service import SystemMonitoringService

# Dependency Injection Helper
def get_monitoring_service(log_type: str = 'backend'):
    return SystemMonitoringService(SystemRepository(log_type=log_type))

@router.get("/status")
def get_system_status(
    # current_user=Depends(get_current_active_superuser),
    service: SystemMonitoringService = Depends(get_monitoring_service)
):
    """
    [Admin] 시스템 상태 조회 (CPU, Memory, Disk)
    """
    return service.get_dashboard_stats()

@router.websocket("/ws/logs")
async def websocket_logs(
    websocket: WebSocket,
    service: SystemMonitoringService = Depends(get_monitoring_service)
):
    """
    [Admin] 로그 실시간 스트리밍
    Auth: WebSocket은 헤더 인증이 복잡하므로, MVP에서는 내부 네트워크/로컬 사용을 가정합니다.
    """
    await websocket.accept()
    try:
        async for line in service.stream_logs():
            await websocket.send_text(line)
    except WebSocketDisconnect:
        # Normal disconnection
        pass
    except Exception as e:
        # Log error?
        print(f"WebSocket Error: {e}")


# --- Memo Endpoints ---

@router.get("/memos", response_model=List[Memo])
def get_memos():
    """
    [Admin] 개발자 메모 목록 조회
    """
    if not os.path.exists(settings.MEMO_FILE_PATH):
        return []
    try:
        with open(settings.MEMO_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

@router.post("/memos", response_model=Memo)
def add_memo(memo_in: MemoCreate):
    """
    [Admin] 새로운 개발자 메모 추가
    """
    memos = []
    if os.path.exists(settings.MEMO_FILE_PATH):
        try:
            with open(settings.MEMO_FILE_PATH, "r", encoding="utf-8") as f:
                memos = json.load(f)
        except Exception:
            memos = []
    
    new_id = max([m["id"] for m in memos], default=0) + 1
    new_memo = {
        "id": new_id,
        "content": memo_in.content,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "admin_reply": None
    }
    memos.append(new_memo)
    
    # Keep only last 50 memos
    if len(memos) > 50:
        memos = memos[-50:]
        
    os.makedirs(os.path.dirname(settings.MEMO_FILE_PATH), exist_ok=True)
    with open(settings.MEMO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)
        
    return new_memo

@router.put("/memos/{memo_id}", response_model=Memo)
def update_memo(memo_id: int, memo_update: MemoUpdate):
    """
    [Admin] 메모 상태/답변 수정
    """
    if not os.path.exists(settings.MEMO_FILE_PATH):
        raise HTTPException(status_code=404, detail="Memo file not found")
    
    with open(settings.MEMO_FILE_PATH, "r", encoding="utf-8") as f:
        memos = json.load(f)
    
    target_idx = next((i for i, m in enumerate(memos) if m["id"] == memo_id), -1)
    if target_idx == -1:
        raise HTTPException(status_code=404, detail="Memo not found")
        
    # Update fields
    current_memo = memos[target_idx]
    if memo_update.status is not None:
        current_memo["status"] = memo_update.status
    if memo_update.admin_reply is not None:
        current_memo["admin_reply"] = memo_update.admin_reply
        
    memos[target_idx] = current_memo
        
    with open(settings.MEMO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)
        
    return current_memo

@router.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    """
    [Admin] 메모 삭제
    """
    if not os.path.exists(settings.MEMO_FILE_PATH):
        return {"status": "success"}
    
    with open(settings.MEMO_FILE_PATH, "r", encoding="utf-8") as f:
        memos = json.load(f)
    
    memos = [m for m in memos if m["id"] != memo_id]
    
    with open(settings.MEMO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)
        
    return {"status": "success"}

@router.delete("/cache")
def clear_cache():
    """
    [Admin] 프론트엔드 캐시 삭제 (.next/cache)
    """
    cache_dir = settings.FRONTEND_CACHE_DIR
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)
            return {"status": "success", "message": "Cache cleared successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")
    return {"status": "success", "message": "Cache directory not found (already clean)"}

@router.post("/restart/frontend")
def restart_frontend(clean_cache: bool = True):
    """
    [Admin] 프론트엔드 서버 재시작
    - clean_cache: True일 경우 .next 캐시 삭제 포함
    """
    script_path = os.path.join(_ROOT_DIR, "start_frontend.sh")
    
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Start script not found")
        
    # Sleep briefly to ensure API response is sent before server dies
    cmd = ["bash", "-c", f"sleep 1.5; bash \"{script_path}\" --auto --force" + (" --clean" if clean_cache else "")]
        
    try:
        # Run as independent process
        subprocess.Popen(
            cmd,
            cwd=_ROOT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return {"status": "success", "message": "Frontend restart triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger restart: {str(e)}")


@router.post("/restart/backend")
def restart_backend():
    """
    [Admin] 백엔드 서버 재시작
    """
    script_path = os.path.join(_ROOT_DIR, "start_backend.sh")
    
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Start script not found")
        
    cmd = ["bash", "-c", f"sleep 1.5; bash \"{script_path}\" --auto --force"]
        
    try:
        # Run as independent process
        subprocess.Popen(
            cmd,
            cwd=_ROOT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return {"status": "success", "message": "Backend restart triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger restart: {str(e)}")

