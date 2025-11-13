"""
이미지 처리 유틸리티 단위 테스트
"""

import pytest
from PIL import Image
import numpy as np
import os
import tempfile

from app.utils.image_utils import (
    preprocess_image,
    rotate_image,
    enhance_contrast,
    denoise_image,
    pdf_to_image,
    save_image,
    get_image_info,
    convert_uploaded_file_to_image
)


class TestImagePreprocessing:
    """이미지 전처리 테스트"""

    @pytest.fixture
    def sample_image(self):
        """테스트용 샘플 이미지 생성 (100x100 그레이스케일)"""
        # 100x100 그레이스케일 이미지 생성
        img_array = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        return Image.fromarray(img_array, mode='L')

    @pytest.fixture
    def sample_rgb_image(self):
        """테스트용 RGB 이미지 생성 (100x100)"""
        img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        return Image.fromarray(img_array, mode='RGB')

    def test_preprocess_image_grayscale(self, sample_image):
        """그레이스케일 이미지 전처리 테스트"""
        result = preprocess_image(sample_image)

        assert result is not None
        assert isinstance(result, Image.Image)
        # 전처리 후에도 이미지 크기는 유지되어야 함 (비율은 변할 수 있음)
        assert result.width > 0 and result.height > 0

    def test_preprocess_image_rgb(self, sample_rgb_image):
        """RGB 이미지 전처리 테스트 (자동 그레이스케일 변환)"""
        result = preprocess_image(sample_rgb_image)

        assert result is not None
        assert isinstance(result, Image.Image)

    def test_rotate_image_90(self, sample_image):
        """90도 회전 테스트"""
        result = rotate_image(sample_image, 90)

        assert result is not None
        assert isinstance(result, Image.Image)
        # 90도 회전 시 width와 height가 바뀜
        assert result.width == sample_image.height
        assert result.height == sample_image.width

    def test_rotate_image_180(self, sample_image):
        """180도 회전 테스트"""
        result = rotate_image(sample_image, 180)

        assert result is not None
        # 180도 회전 시 크기는 동일
        assert result.width == sample_image.width
        assert result.height == sample_image.height

    def test_enhance_contrast(self, sample_image):
        """대비 향상 테스트 (CLAHE)"""
        result = enhance_contrast(sample_image)

        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_enhance_contrast_rgb(self, sample_rgb_image):
        """RGB 이미지 대비 향상 (자동 그레이스케일 변환)"""
        result = enhance_contrast(sample_rgb_image)

        assert result is not None
        assert isinstance(result, Image.Image)

    def test_denoise_image_default(self, sample_image):
        """노이즈 제거 테스트 (기본 커널 크기)"""
        result = denoise_image(sample_image)

        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_denoise_image_custom_kernel(self, sample_image):
        """노이즈 제거 테스트 (커스텀 커널 크기)"""
        result = denoise_image(sample_image, kernel_size=5)

        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == sample_image.size

    def test_denoise_image_even_kernel_auto_adjust(self, sample_image):
        """짝수 커널 크기 자동 조정 테스트 (4 → 5)"""
        result = denoise_image(sample_image, kernel_size=4)

        assert result is not None
        # 짝수 커널 크기는 자동으로 홀수로 조정됨


class TestImageSaveLoad:
    """이미지 저장/로드 테스트"""

    @pytest.fixture
    def sample_image(self):
        """테스트용 샘플 이미지"""
        img_array = np.random.randint(0, 256, (50, 50), dtype=np.uint8)
        return Image.fromarray(img_array, mode='L')

    def test_save_image(self, sample_image):
        """이미지 저장 테스트"""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = os.path.join(tmpdir, 'test_image.png')

            # 이미지 저장
            save_image(sample_image, save_path)

            # 파일 존재 확인
            assert os.path.exists(save_path)

            # 저장된 이미지 로드 확인
            loaded_image = Image.open(save_path)
            assert loaded_image.size == sample_image.size

    def test_save_image_auto_create_dir(self, sample_image):
        """디렉토리 자동 생성 테스트"""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = os.path.join(tmpdir, 'subdir', 'test_image.png')

            # 이미지 저장 (subdir이 없어도 자동 생성됨)
            save_image(sample_image, save_path)

            # 파일 존재 확인
            assert os.path.exists(save_path)

    def test_get_image_info(self, sample_image):
        """이미지 메타데이터 추출 테스트"""
        info = get_image_info(sample_image)

        assert info is not None
        assert 'width' in info
        assert 'height' in info
        assert 'mode' in info
        assert info['width'] == 50
        assert info['height'] == 50
        assert info['mode'] == 'L'  # Grayscale


class TestPDFConversion:
    """PDF 변환 테스트"""

    def test_pdf_to_image_file_not_found(self):
        """존재하지 않는 PDF 파일 테스트"""
        # pdf2image는 PDFPageCountError를 발생시키므로
        # FileNotFoundError 대신 Exception을 체크
        with pytest.raises(Exception):
            pdf_to_image('/nonexistent/path/test.pdf')

    # Note: 실제 PDF 파일이 필요한 테스트는 통합 테스트에서 수행
    # 여기서는 에러 케이스만 테스트


class TestImageIntegration:
    """이미지 처리 통합 테스트 (전처리 파이프라인)"""

    @pytest.fixture
    def sample_rgb_image(self):
        """테스트용 RGB 이미지"""
        img_array = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        return Image.fromarray(img_array, mode='RGB')

    def test_full_preprocessing_pipeline(self, sample_rgb_image):
        """전체 전처리 파이프라인 테스트"""
        # 1. 전처리 (그레이스케일 + 대비 + 노이즈 제거 + 이진화)
        preprocessed = preprocess_image(sample_rgb_image)

        assert preprocessed is not None

        # 2. 대비 향상 (별도로 다시 적용)
        enhanced = enhance_contrast(preprocessed)

        assert enhanced is not None

        # 3. 노이즈 제거
        denoised = denoise_image(enhanced)

        assert denoised is not None

        # 4. 회전 보정
        rotated = rotate_image(denoised, 0)  # 0도 회전 (원본 유지)

        assert rotated is not None

    def test_preprocessing_preserves_content(self, sample_rgb_image):
        """전처리 후에도 이미지 내용이 유지되는지 테스트"""
        preprocessed = preprocess_image(sample_rgb_image)

        # 전처리 후 이미지가 완전히 검은색이나 흰색이 아님 (내용 유지)
        img_array = np.array(preprocessed)
        assert not np.all(img_array == 0)  # 완전 검은색 아님
        assert not np.all(img_array == 255)  # 완전 흰색 아님
