import json
import logging
from pathlib import Path
from typing import Optional

from app.schemas.config import (
    ImageProcessingConfig,
    OCRConfig,
    SystemConfig,
)

logger = logging.getLogger(__name__)


class ConfigService:
    """
    중앙 집중식 설정 관리 서비스 (Singleton)
    system_config.json을 로드하고 관리함
    """

    _instance = None
    _config: Optional[SystemConfig] = None
    _config_path: Path = Path(__file__).parent.parent / "configs" / "system_config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """설정 파일 로드"""
        try:
            if not self._config_path.exists():
                logger.error(f"Config file not found at {self._config_path}")
                raise FileNotFoundError(f"Config file not found at {self._config_path}")

            with open(self._config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._config = SystemConfig(**data)
                logger.info("System configuration loaded successfully")

        except Exception as e:
            logger.critical(f"Failed to load system config: {str(e)}")
            raise

    def get_system_config(self) -> SystemConfig:
        """전체 설정 반환"""
        if self._config is None:
            self._load_config()
        if self._config is None:  # Mypy check
            raise RuntimeError("Config not loaded")
        return self._config

    def get_image_processing_config(self) -> ImageProcessingConfig:
        """이미지 처리 설정 반환"""
        return self.get_system_config().image_processing.preprocess_for_ocr

    def get_ocr_config(self) -> OCRConfig:
        """OCR 설정 반환"""
        return self.get_system_config().ocr

    def reload_config(self) -> None:
        """설정 강제 리로드"""
        self._load_config()

    def save_config(self, new_config: SystemConfig) -> None:
        """설정 저장 (Admin 용)"""
        try:
            # 1. Validate by dumping model
            config_dict = new_config.model_dump(by_alias=True)

            # 2. Save to file
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)

            # 3. Reload
            self._config = new_config
            logger.info("System configuration updated and saved")

        except Exception as e:
            logger.error(f"Failed to save system config: {str(e)}")
            raise


# Global Instance
config_service = ConfigService()
