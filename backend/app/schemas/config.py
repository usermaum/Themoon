from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CommentsGuide(BaseModel):
    """설정 파일 주석 가이드"""

    to_grayscale: str
    enhance_contrast: str
    contrast_factor: str
    remove_noise: str
    median_filter_size: str


class ImageProcessingConfig(BaseModel):
    """이미지 처리 설정"""

    to_grayscale: bool = True
    enhance_contrast: bool = False
    contrast_factor: float = 1.8
    remove_noise: bool = False
    median_filter_size: int = 3
    enhance_sharpness: bool = True
    sharpness_factor: float = 2.0
    upscale_image: bool = True
    auto_rotate: bool = True


class ImageProcessingSection(BaseModel):
    """이미지 처리 섹션"""

    comments_guide: Optional[Dict[str, str]] = Field(None, alias="_comments_guide")
    preprocess_for_ocr: ImageProcessingConfig


class OCRPromptStructure(BaseModel):
    """OCR 프롬프트 구조"""

    error: Optional[Any] = None
    debug_raw_text: str
    document_info: Dict[str, str]
    supplier: Dict[str, str]
    receiver: Dict[str, str]
    amounts: Dict[str, str]
    items: List[Dict[str, Any]]
    additional_info: Dict[str, str]


class OCRConfig(BaseModel):
    """OCR 설정"""

    model_priority_rule: Optional[str] = Field(None, alias="_model_priority_rule")
    model_priority: List[str]
    prompt_structure: OCRPromptStructure


class SystemInfo(BaseModel):
    """시스템 메타데이터"""

    version: str
    last_updated: str


class SystemConfig(BaseModel):
    """전체 시스템 설정"""

    system: SystemInfo
    image_processing: ImageProcessingSection
    ocr: OCRConfig
