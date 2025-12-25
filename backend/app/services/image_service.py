import io
import json
import logging
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import magic
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageStat
from PIL.Image import Image as PILImage

from app.config import settings

logger = logging.getLogger(__name__)


class ImageService:
    def __init__(self, upload_base_dir: Optional[str] = None):
        self.base_dir = Path(upload_base_dir or settings.IMAGE_UPLOAD_BASE_DIR)
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}
        self.allowed_mime_types = {"image/jpeg", "image/png", "image/webp", "image/tiff"}
        self.max_file_size = settings.IMAGE_MAX_FILE_SIZE

        # Multi-tier configurations
        self.profiles = {
            "original": {
                "max_size": settings.IMAGE_ORIGINAL_MAX_SIZE,
                "quality": settings.IMAGE_ORIGINAL_QUALITY,
                "format": "JPEG",
                "suffix": "",
            },
            "webview": {
                "max_size": settings.IMAGE_WEBVIEW_MAX_SIZE,
                "quality": settings.IMAGE_WEBVIEW_QUALITY,
                "format": "WEBP",
                "suffix": "_web",
            },
            "thumbnail": {
                "max_size": settings.IMAGE_THUMBNAIL_MAX_SIZE,
                "quality": settings.IMAGE_THUMBNAIL_QUALITY,
                "format": "WEBP",
                "suffix": "_thumb",
            },
        }

    def _strip_sensitive_exif(self, img: PILImage) -> PILImage:
        """EXIF 민감 데이터 제거 (GPS, 카메라 정보 등)"""

        # 1. 방향 정보 적용 (회전)
        img = ImageOps.exif_transpose(img)

        # 2. 모든 EXIF 데이터 제거
        data = list(img.getdata())
        img_without_exif = Image.new(img.mode, img.size)
        img_without_exif.putdata(data)

        return img_without_exif

    def preprocess_for_ocr(
        self,
        img: PILImage,
        # Default args are now just fallbacks if config fails
        to_grayscale: bool = True,
        enhance_contrast: bool = False,
        contrast_factor: float = 1.8,
        remove_noise: bool = False,
        median_filter_size: int = 3,
        enhance_sharpness: bool = True,
        sharpness_factor: float = 2.0,
        upscale_image: bool = True,
        auto_rotate: bool = True
    ) -> PILImage:
        """
        OCR 정확도를 높이기 위한 이미지 전처리 (옵션화 + Hot-reload Config 적용)

        [MAINTENANCE GUIDE for AI Agents & Developers]
        - 이 함수는 `backend/app/resources/image_processing_config.json` 파일을 실시간으로 읽어 설정을 적용합니다.
        - 서버 재시작 없이 옵션을 변경하려면 위 JSON 파일을 수정하세요.
        - 파일 읽기 실패 시, 함수 인자로 전달된 기본값(Safe Defaults)을 사용합니다.

        Args:
            img: PIL Image 객체
            (이하 인자는 Config 파일이 없을 경우의 Fallback 값으로 동작합니다)
        """

        # 0. Hot-reload Configuration (via ConfigService)
        try:
            from app.services.config_service import config_service

            config = config_service.get_image_processing_config()

            # Override defaults with config values
            to_grayscale = config.to_grayscale
            enhance_contrast = config.enhance_contrast
            contrast_factor = config.contrast_factor
            remove_noise = config.remove_noise
            median_filter_size = config.median_filter_size
            enhance_sharpness = getattr(config, "enhance_sharpness", enhance_sharpness)
            sharpness_factor = getattr(config, "sharpness_factor", sharpness_factor)
            upscale_image = getattr(config, "upscale_image", upscale_image)
            auto_rotate = getattr(config, "auto_rotate", auto_rotate)

        except Exception as e:
            logger.warning(f"Failed to load configuration from ConfigService: {e}. Using defaults.")

        # 1. 자동 회전 및 수평 보정 (Auto-Deskew with EXIF)
        # LLM은 비뚤어진 텍스트도 잘 읽지만, 정면을 향할 때 표 인식률이 높아짐
        if auto_rotate:
            img = ImageOps.exif_transpose(img)

        # 2. 업스케일링 (Low Resolution Enhancement)
        # 1500px 미만일 경우 2배 확대 (LANCZOS 필터 사용)
        if upscale_image:
            width, height = img.size
            if width < 1500 or height < 1500:
                img = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)

        # 3. 그레이스케일 변환
        if to_grayscale and img.mode != "L":
            img = img.convert("L")

        # 4. 선명도 향상 (Sharpening)
        # 흐릿한 글자의 경계선을 뚜렷하게 만들어 인식률 향상
        if enhance_sharpness:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_factor)

        # 5. 대비 향상 (Contrast Enhancement)
        if enhance_contrast:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)

        # 6. 노이즈 제거 (Median Filter)
        if remove_noise:
            img = img.filter(ImageFilter.MedianFilter(size=median_filter_size))

        return img

    def validate_image_quality_for_ocr(self, img: PILImage) -> dict:
        """
        OCR 품질 검증
        Returns:
            {
                "is_valid": bool,
                "warnings": list[str],
                "metrics": dict
            }
        """
        warnings = []
        is_valid = True

        # 1. 해상도 체크
        width, height = img.size
        min_dimension = 800
        if width < min_dimension or height < min_dimension:
            warnings.append(f"Low resolution: {width}x{height} (Recommended: >{min_dimension}px)")
            # 해상도가 너무 낮으면 False로 처리할 수도 있지만, 일단 경고만

        # 2. 밝기 및 대비 체크 (Grayscale 기준)
        if img.mode != "L":
            gray_img = img.convert("L")
        else:
            gray_img = img

        stat = ImageStat.Stat(gray_img)
        brightness = stat.mean[0]
        contrast = stat.stddev[0]

        # 밝기 체크 (0~255)
        if brightness < 40:
            warnings.append(f"Image too dark (Brightness: {brightness:.1f})")
        elif brightness > 230:
            warnings.append(f"Image too bright (Brightness: {brightness:.1f})")

        # 대비 체크
        if contrast < 20:
            warnings.append(f"Low contrast (StdDev: {contrast:.1f})")

        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings,
            "metrics": {
                "width": width,
                "height": height,
                "brightness": brightness,
                "contrast": contrast,
            },
        }

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
        free_gb = stat.free / (1024**3)

        if free_gb < min_free_gb:
            logger.error(f"Low disk space: {free_gb:.2f}GB < {min_free_gb}GB")
            raise IOError(
                f"Insufficient disk space: {free_gb:.2f}GB available, " f"{min_free_gb}GB required"
            )

        logger.debug(f"Disk space OK: {free_gb:.2f}GB free")

    def _save_atomic(self, img: PILImage, target_path: Path, **save_kwargs) -> None:
        """원자적 이미지 저장 (임시 파일 + rename)"""
        import tempfile

        # 1. 임시 파일 생성 (같은 디렉토리)
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=target_path.suffix, dir=target_path.parent, prefix=".tmp_"
        )

        try:
            # 2. 임시 파일에 저장
            with os.fdopen(temp_fd, "wb") as f:
                img.save(f, **save_kwargs)

            # 3. 원자적 rename
            os.replace(temp_path, target_path)

            logger.debug(f"Atomically saved: {target_path}")
        except Exception:
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

    def process_and_save(
        self,
        file_content: bytes,
        original_filename: str,
        output_dir: Optional[Path] = None,
        custom_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Main entry point to process an image and save it in 3 tiers.
        Returns a dictionary with paths and metadata.

        Args:
            file_content: Raw image bytes
            original_filename: Original filename (for logging/extension)
            output_dir: Optional absolute path to save images (overrides default year/month logic)
            custom_filename: Optional base filename to use (overrides random generation)
        """
        # Determine base filename
        if custom_filename:
            safe_base_name = custom_filename
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            safe_base_name = f"invoice_{timestamp}_{unique_id}"

        # Determine output directory
        if output_dir:
            abs_base_dir = output_dir
            rel_dir = Path(".")  # Relative path is current dir relative to output_dir
        else:
            # Default: Get relative directory based on year/month
            rel_dir = Path(datetime.now().strftime("%Y/%m"))
            abs_base_dir = self.base_dir / rel_dir

        # Ensure directories exist
        if output_dir:
            abs_base_dir.mkdir(parents=True, exist_ok=True)
        else:
            for tier in self.profiles.keys():
                (abs_base_dir / tier).mkdir(parents=True, exist_ok=True)

        if self.base_dir.exists() and not output_dir:
            self._check_disk_space(min_free_gb=settings.IMAGE_MIN_FREE_DISK_SPACE_GB)

        results: Dict[str, Any] = {
            "file_size_bytes": len(file_content),
            "original_filename": original_filename,
            "paths": {},
        }

        saved_paths: list[Path] = []
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
                    # For custom output (e.g. batch processing), we might not want all tiers or want flat structure
                    # But for now, let's keep the logic consistent or adapt based on output_dir presence

                    tier_img = img.copy()

                    # JPEG는 투명도(RGBA)를 지원하지 않으므로 RGB로 변환
                    if config["format"] == "JPEG" and tier_img.mode in ("RGBA", "P", "LA"):
                        if tier_img.mode == "RGBA":
                            # 투명 배경을 흰색으로 채움
                            background = Image.new("RGB", tier_img.size, (255, 255, 255))
                            background.paste(tier_img, mask=tier_img.split()[3])
                            tier_img = background
                        else:
                            tier_img = tier_img.convert("RGB")

                    tier_img.thumbnail(config["max_size"], Image.Resampling.LANCZOS)

                    file_ext: str = str(config["format"]).lower()
                    if file_ext == "jpeg":
                        file_ext = "jpg"

                    tier_filename = f"{safe_base_name}{config['suffix']}.{file_ext}"

                    if output_dir:
                        # Flat structure for batch optimization usually
                        # But let's check if we want flat or tiered.
                        # For bean images, we probably want them in the same folder.
                        abs_path = abs_base_dir / tier_filename
                        rel_path_str = tier_filename  # Just filename
                    else:
                        rel_path_obj = rel_dir / tier / tier_filename
                        abs_path = self.base_dir / rel_path_obj
                        rel_path_str = str(rel_path_obj)

                    # Security Check: Path Validation
                    # Skip for custom output_dir as it implies trusted system operation
                    if not output_dir and not self._validate_path_security(abs_path.parent):
                        raise ValueError(f"Security check failed for path: {abs_path}")

                    # Save image atomically
                    self._save_atomic(
                        img=tier_img,
                        target_path=abs_path,
                        format=config["format"],
                        quality=config["quality"],
                        optimize=True,
                    )

                    saved_paths.append(abs_path)

                    # Store results (using forward slashes for URL compatibility)
                    results["paths"][tier] = rel_path_str.replace("\\", "/")

            elapsed_ms = (time.time() - start_time) * 1000

            # Structured logging
            log_data = {
                "event": "image_processed",
                "original_filename": original_filename,
                "input_size_bytes": len(file_content),
                "processing_time_ms": round(elapsed_ms, 2),
                "paths": results["paths"],
            }
            logger.info(f"Image processing completed: {json.dumps(log_data)}")

        except (IOError, OSError) as e:
            elapsed_ms = (time.time() - start_time) * 1000
            logger.error(f"Image I/O error ({round(elapsed_ms, 2)}ms): {e}", exc_info=True)
            self._cleanup_partial(saved_paths)
            raise
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            logger.exception(
                f"Unexpected error during image processing ({round(elapsed_ms, 2)}ms): {e}"
            )
            self._cleanup_partial(saved_paths)
            raise

        return results


image_service = ImageService()


def get_image_service(upload_dir: str = "static/uploads/inbound") -> ImageService:
    """Dependency Injection Factory for ImageService"""
    return ImageService(upload_dir)
