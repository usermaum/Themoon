from fastapi import APIRouter, Depends
from typing import Dict, Any
import shutil
import os
from app.config import settings

router = APIRouter()

@router.get("/status")
def get_system_status() -> Dict[str, Any]:
    """
    Get system status including disk usage and storage metrics.
    """
    # 1. Disk Usage
    # Use the configured upload directory or default to current directory
    upload_dir = settings.IMAGE_UPLOAD_DIR if hasattr(settings, 'IMAGE_UPLOAD_DIR') else "."
    
    total, used, free = shutil.disk_usage(upload_dir)
    
    # 2. Simple Storage Stats (Count files)
    # This is a basic implementation. For production, querying DB logs or caching is better.
    image_count = 0
    total_size = 0
    
    upload_path = "static/uploads/inbound"
    if os.path.exists(upload_path):
        for root, dirs, files in os.walk(upload_path):
            image_count += len(files)
            total_size += sum(os.path.getsize(os.path.join(root, name)) for name in files)

    return {
        "disk": {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "percent_used": round((used / total) * 100, 1)
        },
        "storage": {
            "total_images": image_count,
            "total_size_mb": round(total_size / (1024**2), 2),
            "upload_path": upload_path
        }
    }
