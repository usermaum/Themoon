"""
이미지 처리 유틸리티

거래 명세서 이미지를 OCR에 최적화된 형태로 전처리합니다.
"""

from typing import List, Optional
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import io


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    이미지 전처리 (OCR 최적화)

    처리 순서:
    1. 그레이스케일 변환
    2. 대비 향상 (CLAHE)
    3. 노이즈 제거 (Gaussian Blur)
    4. 이진화 (Adaptive Threshold)

    Args:
        image: PIL Image 객체

    Returns:
        전처리된 PIL Image 객체
    """
    # PIL → OpenCV (numpy array)
    img_array = np.array(image)

    # 1. 그레이스케일 변환 (이미 그레이스케일이면 스킵)
    if len(img_array.shape) == 3:  # RGB
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    # 2. 대비 향상 (CLAHE)
    enhanced = enhance_contrast(Image.fromarray(gray))
    enhanced_array = np.array(enhanced)

    # 3. 노이즈 제거 (Gaussian Blur)
    denoised = cv2.GaussianBlur(enhanced_array, (3, 3), 0)

    # 4. 이진화 (Adaptive Threshold)
    # 배경 불균일 조명 대응
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,  # Block size
        2    # C constant
    )

    # OpenCV → PIL
    return Image.fromarray(binary)


def rotate_image(image: Image.Image, angle: int) -> Image.Image:
    """
    이미지 회전 보정

    Args:
        image: PIL Image 객체
        angle: 회전 각도 (도, 시계 반대 방향)
               90, 180, 270 또는 임의 각도

    Returns:
        회전된 PIL Image 객체
    """
    # PIL의 rotate는 시계 반대 방향이 양수
    # expand=True: 이미지가 잘리지 않도록 캔버스 확장
    rotated = image.rotate(angle, expand=True, fillcolor=255)

    return rotated


def enhance_contrast(image: Image.Image) -> Image.Image:
    """
    대비 향상 (CLAHE - Contrast Limited Adaptive Histogram Equalization)

    배경과 글자의 대비를 향상시켜 OCR 정확도 개선

    Args:
        image: PIL Image 객체 (그레이스케일 권장)

    Returns:
        대비 향상된 PIL Image 객체
    """
    # PIL → OpenCV
    img_array = np.array(image)

    # RGB인 경우 그레이스케일 변환
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # CLAHE 적용
    clahe = cv2.createCLAHE(
        clipLimit=2.0,     # 대비 제한 (너무 높으면 노이즈 증가)
        tileGridSize=(8, 8) # 타일 크기
    )
    enhanced = clahe.apply(img_array)

    # OpenCV → PIL
    return Image.fromarray(enhanced)


def denoise_image(image: Image.Image, kernel_size: int = 3) -> Image.Image:
    """
    노이즈 제거 (Gaussian Blur)

    Args:
        image: PIL Image 객체
        kernel_size: 블러 커널 크기 (홀수, 기본값: 3)
                     크기가 클수록 강한 블러 효과

    Returns:
        노이즈 제거된 PIL Image 객체
    """
    # kernel_size가 홀수인지 확인
    if kernel_size % 2 == 0:
        kernel_size += 1

    # PIL → OpenCV
    img_array = np.array(image)

    # Gaussian Blur 적용
    denoised = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)

    # OpenCV → PIL
    return Image.fromarray(denoised)


def pdf_to_image(pdf_path: str, dpi: int = 300) -> List[Image.Image]:
    """
    PDF를 이미지로 변환 (첫 페이지만)

    Args:
        pdf_path: PDF 파일 경로
        dpi: 해상도 (기본값: 300, OCR에 적합)
             높을수록 선명하지만 처리 시간 증가

    Returns:
        PIL Image 객체 리스트 (첫 페이지만 포함)

    Raises:
        FileNotFoundError: PDF 파일이 없을 때
        Exception: PDF 변환 실패 시
    """
    try:
        # 첫 페이지만 변환 (last_page=1)
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=1,
            last_page=1
        )

        return images

    except FileNotFoundError:
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    except Exception as e:
        raise Exception(f"PDF 변환 실패: {str(e)}")


def convert_uploaded_file_to_image(uploaded_file) -> Image.Image:
    """
    Streamlit UploadedFile을 PIL Image로 변환

    Args:
        uploaded_file: Streamlit UploadedFile 객체

    Returns:
        PIL Image 객체

    Raises:
        ValueError: 지원하지 않는 파일 형식
    """
    file_type = uploaded_file.type

    # 이미지 파일 (JPG, PNG)
    if file_type in ['image/jpeg', 'image/png', 'image/jpg']:
        image = Image.open(uploaded_file)
        return image

    # PDF 파일
    elif file_type == 'application/pdf':
        # UploadedFile → bytes → 임시 파일 저장
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # PDF → 이미지 변환
            images = pdf_to_image(tmp_path, dpi=300)
            return images[0] if images else None

        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {file_type}")


def save_image(image: Image.Image, save_path: str) -> None:
    """
    이미지 저장

    Args:
        image: PIL Image 객체
        save_path: 저장 경로 (확장자 포함)
    """
    # 디렉토리가 없으면 생성
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 이미지 저장
    image.save(save_path)


def get_image_info(image: Image.Image) -> dict:
    """
    이미지 메타데이터 추출

    Args:
        image: PIL Image 객체

    Returns:
        {
            'width': int,
            'height': int,
            'mode': str,  # 'RGB', 'L' (grayscale), etc.
            'format': str # 'JPEG', 'PNG', etc.
        }
    """
    return {
        'width': image.width,
        'height': image.height,
        'mode': image.mode,
        'format': image.format
    }
