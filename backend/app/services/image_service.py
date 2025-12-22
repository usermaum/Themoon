import os
import io
import uuid
import logging
import json
import magic
from datetime import datetime
from PIL import Image
from pathlib import Path
from typing import Tuple, Dict, Optional, Any

import time
from app.config import settings

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, upload_base_dir: str = None):
        self.base_dir = Path(upload_base_dir or settings.IMAGE_UPLOAD_BASE_DIR)
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff'}
        self.allowed_mime_types = {'image/jpeg', 'image/png', 'image/webp', 'image/tiff'}
        self.max_file_size = settings.IMAGE_MAX_FILE_SIZE

        # Multi-tier configurations
        self.profiles = {
            'original': {'max_size': settings.IMAGE_ORIGINAL_MAX_SIZE, 'quality': settings.IMAGE_ORIGINAL_QUALITY, 'format': 'JPEG', 'suffix': ''},
            'webview': {'max_size': settings.IMAGE_WEBVIEW_MAX_SIZE, 'quality': settings.IMAGE_WEBVIEW_QUALITY, 'format': 'WEBP', 'suffix': '_web'},
            'thumbnail': {'max_size': settings.IMAGE_THUMBNAIL_MAX_SIZE, 'quality': settings.IMAGE_THUMBNAIL_QUALITY, 'format': 'WEBP', 'suffix': '_thumb'}
        }

    def _strip_sensitive_exif(self, img: Image) -> Image:
        """EXIF 민감 데이터 제거 (GPS, 카메라 정보 등)"""
        from PIL import ImageOps
        
        # 1. 방향 정보 적용 (회전)
        img = ImageOps.exif_transpose(img)
        
        # 2. 모든 EXIF 데이터 제거
        data = list(img.getdata())
        img_without_exif = Image.new(img.mode, img.size)
        img_without_exif.putdata(data)
        
        return img_without_exif

    def _validate_path_security(self, path: Path) -> bool:
        """경로 보안 검증 (심볼릭 링크, 경로 순회 방어)"""
        try:
            # 1. 절대 경로로 해석
            resolved_path = path.resolve()
            
            # 2. 기준 경로 확인
            base_path = self.base_dir.resolve()
            
            # 3. 기준 경로 내부에 있는지 확인
            try:
                resolved_path.relative_to(base_path)
            except ValueError:
                logger.error(f"Path traversal attempt: {path}")
                return False
                
            # 4. 심볼릭 링크 확인
            if path.is_symlink():
                logger.warning(f"Symlink detected: {path}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False

    def _check_disk_space(self, min_free_gb: int = 5) -> None:
        """디스크 여유 공간 확인"""
        import shutil

        stat = shutil.disk_usage(self.base_dir)
        free_gb = stat.free / (1024 ** 3)

        if free_gb < min_free_gb:
            logger.error(f"Low disk space: {free_gb:.2f}GB < {min_free_gb}GB")
            raise IOError(
                f"Insufficient disk space: {free_gb:.2f}GB available, "
                f"{min_free_gb}GB required"
            )

        logger.debug(f"Disk space OK: {free_gb:.2f}GB free")

    def _save_atomic(self, img: Image, target_path: Path, **save_kwargs) -> None:
        """원자적 이미지 저장 (임시 파일 + rename)"""
        import tempfile

        # 1. 임시 파일 생성 (같은 디렉토리)
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=target_path.suffix,
            dir=target_path.parent,
            prefix=".tmp_"
        )

        try:
            # 2. 임시 파일에 저장
            with os.fdopen(temp_fd, 'wb') as f:
                img.save(f, **save_kwargs)

            # 3. 원자적 rename
            os.replace(temp_path, target_path)

            logger.debug(f"Atomically saved: {target_path}")
        except Exception as e:
            # 4. 실패 시 임시 파일 정리
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _cleanup_partial(self, paths: list[Path]) -> None:
        """부분 실패 시 생성된 파일 정리"""
        for path in paths:
            if path and path.exists():
                try:
                    path.unlink()
                    logger.info(f"Cleaned up partial file: {path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup {path}: {e}")

    def validate_image(self, file_content: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validates the image for security and integrity.
        Returns (success, error_message)
        """
        # 1. Size check
        if len(file_content) > self.max_file_size:
            return False, f"File size exceeds limit ({self.max_file_size // (1024*1024)}MB)"

        # 2. Extension check
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.allowed_extensions:
            return False, f"Unsupported file extension: {ext}"

        # 3. Magic bytes / MIME type check
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in self.allowed_mime_types:
            return False, f"Invalid file content type: {mime}"

        # 4. Image integrity check using Pillow
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                img.verify()
        except Exception as e:
            logger.error(f"Image integrity check failed: {str(e)}")
            return False, "Corrupted or invalid image file"

        return True, ""

    def process_and_save(self, file_content: bytes, original_filename: str) -> Dict[str, Any]:
        """
        Main entry point to process an image and save it in 3 tiers.
        Returns a dictionary with paths and metadata.
        """
        # Create base filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        safe_base_name = f"invoice_{timestamp}_{unique_id}"

        # Get relative directory based on year/month
        rel_dir = Path(datetime.now().strftime("%Y/%m"))
        abs_base_dir = self.base_dir / rel_dir
        
        # Ensure directories exist
        for tier in self.profiles.keys():
            (abs_base_dir / tier).mkdir(parents=True, exist_ok=True)

        if self.base_dir.exists():
             self._check_disk_space(min_free_gb=settings.IMAGE_MIN_FREE_DISK_SPACE_GB)

        results = {
            "file_size_bytes": len(file_content),
            "original_filename": original_filename,
            "paths": {}
        }
        
        saved_paths = []
        start_time = time.time()

        try:
            with Image.open(io.BytesIO(file_content)) as img:
                # Store original dimensions
                results["width"], results["height"] = img.size
                
                # Strip sensitive EXIF data
                try:
                    img = self._strip_sensitive_exif(img)
                except Exception as e:
                    logger.warning(f"Failed to strip EXIF data: {e}")

                for tier, config in self.profiles.items():
                    tier_img = img.copy()
                    tier_img.thumbnail(config['max_size'], Image.Resampling.LANCZOS)
                    
                    file_ext = config['format'].lower()
                    if file_ext == 'jpeg': file_ext = 'jpg'
                    
                    tier_filename = f"{safe_base_name}{config['suffix']}.{file_ext}"
                    rel_path = rel_dir / tier / tier_filename
                    abs_path = self.base_dir / rel_path
                    
                    # Security Check: Path Validation
                    if not self._validate_path_security(abs_path.parent):
                         raise ValueError(f"Security check failed for path: {abs_path}")
                    
                    # Save image atomically
                    self._save_atomic(
                        img=tier_img,
                        target_path=abs_path,
                        format=config['format'], 
                        quality=config['quality'], 
                        optimize=True
                    )
                    
                    saved_paths.append(abs_path)
                    
                    # Store results (using forward slashes for URL compatibility)
                    results["paths"][tier] = str(rel_path).replace("\\", "/")

            elapsed_ms = (time.time() - start_time) * 1000
            
            # Structured logging
            log_data = {
                "event": "image_processed",
                "original_filename": original_filename,
                "input_size_bytes": len(file_content),
                "processing_time_ms": round(elapsed_ms, 2),
                "paths": results['paths']
            }
            logger.info(f"Image processing completed: {json.dumps(log_data)}")

        except (IOError, OSError) as e:
            elapsed_ms = (time.time() - start_time) * 1000
            logger.error(f"Image I/O error ({round(elapsed_ms, 2)}ms): {e}", exc_info=True)
            self._cleanup_partial(saved_paths)
            raise
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            logger.exception(f"Unexpected error during image processing ({round(elapsed_ms, 2)}ms): {e}")
            self._cleanup_partial(saved_paths)
            raise

        return results

image_service = ImageService()

def get_image_service(upload_dir: str = "static/uploads/inbound") -> ImageService:
    """Dependency Injection Factory for ImageService"""
    return ImageService(upload_dir)
