import os
import time
import psutil
from typing import Generator, Dict, Any, Optional
from pathlib import Path
from app.config import settings

class SystemRepository:
    """
    Repository for accessing System Resources (CPU, Memory, Disk) and Log Files.
    Abides by Clean Architecture: No business logic, only data access.
    """

    def __init__(self, log_type: str = 'backend'):
        self.log_type = log_type
        if log_type == 'frontend':
            self.log_file_path = Path(settings.FRONTEND_LOG_FILE_PATH)
        else:
            self.log_file_path = Path(settings.LOG_FILE_PATH)

    def get_system_stats(self) -> Dict[str, Any]:
        """
        Fetch current system resource usage.
        """
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Calculate size of images directory project specific
        # Ideally this path should be injected or configured
        images_size = 0
        images_path = Path("images")
        if images_path.exists():
             images_size = sum(f.stat().st_size for f in images_path.glob('**/*') if f.is_file())

        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": memory.percent,
            "memory_total": memory.total,
            "memory_available": memory.available,
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "images_folder_size_bytes": images_size
        }

    async def get_log_stream_generator(self) -> Generator[str, None, None]:
        """
        Yields new lines from the log file as they are written (tail -f).
        Async generator for non-blocking streaming.
        """
        import asyncio
        
        if not self.log_file_path.exists():
            yield "Log file not found.\n"
            return

        # Open file in non-blocking way? 
        # Standard open() is blocking, but for read-only tailing log files it's acceptable in this scale.
        # Alternatively use aiofiles if available, but staying dependency-light:
        with open(self.log_file_path, "r", encoding="utf-8") as f:
            # Move to the end of file
            f.seek(0, os.SEEK_END)
            
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    await asyncio.sleep(0.5) # Non-blocking sleep
