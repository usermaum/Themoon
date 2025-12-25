from typing import Dict, Any, AsyncGenerator
from app.repositories.system_repository import SystemRepository

class SystemMonitoringService:
    """
    Service for System Monitoring.
    Uses SystemRepository to fetch data and applies business logic (formatting, alerts).
    """

    def __init__(self, repository: SystemRepository):
        self.repository = repository

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get formatted system stats for the dashboard.
        """
        raw_stats = self.repository.get_system_stats()
        
        # Apply Logic: Convert bytes to GB/MB
        memory_total_gb = raw_stats['memory_total'] / (1024 ** 3)
        memory_usage_gb = (raw_stats['memory_total'] - raw_stats['memory_available']) / (1024 ** 3)
        
        disk_free_gb = raw_stats['disk_free'] / (1024 ** 3)
        images_size_mb = raw_stats['images_folder_size_bytes'] / (1024 ** 2)

        return {
            "cpu": {
                "usage_percent": raw_stats['cpu_percent'],
                "status": "critical" if raw_stats['cpu_percent'] > 90 else "normal"
            },
            "memory": {
                "usage_percent": raw_stats['memory_percent'],
                "total_gb": round(memory_total_gb, 2),
                "used_gb": round(memory_usage_gb, 2)
            },
            "disk": {
                "usage_percent": raw_stats['disk_percent'],
                "free_gb": round(disk_free_gb, 2)
            },
            "storage": {
                "images_size_mb": round(images_size_mb, 2)
            }
        }

    async def stream_logs(self) -> AsyncGenerator[str, None]:
        """
        Stream application logs.
        """
        async for line in self.repository.get_log_stream_generator():
            # Business Logic: Filter out PII or specific noisy logs if needed
            # For now, pass through
            if line.strip(): # Only yield non-empty lines
                yield line
