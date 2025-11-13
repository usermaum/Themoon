"""
OCR 서비스

거래 명세서 이미지에서 텍스트를 추출하고 구조화된 데이터로 파싱합니다.
"""

from typing import Dict, Tuple, Optional
from datetime import datetime
from PIL import Image
import pytesseract
from sqlalchemy.orm import Session
import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Bean
from utils.text_parser import (
    parse_invoice,
    fuzzy_match_bean,
    validate_parsed_data
)
from utils.image_utils import preprocess_image


class OCRService:
    """
    OCR 서비스

    Tesseract OCR을 사용하여 이미지에서 텍스트를 추출하고
    구조화된 데이터로 파싱합니다.
    """

    def __init__(self, db: Session):
        """
        Args:
            db: SQLAlchemy Session
        """
        self.db = db

    def extract_text_from_image(
        self,
        image: Image.Image,
        lang: str = 'kor+eng',
        preprocess: bool = True
    ) -> str:
        """
        이미지에서 텍스트 추출 (Tesseract OCR)

        Args:
            image: PIL Image 객체
            lang: OCR 언어 (기본값: 'kor+eng')
            preprocess: 전처리 수행 여부 (기본값: True)

        Returns:
            추출된 텍스트 (원본)

        Raises:
            Exception: OCR 실패 시
        """
        try:
            # 전처리 수행 (옵션)
            if preprocess:
                image = preprocess_image(image)

            # Tesseract OCR 설정
            custom_config = r'--oem 3 --psm 6'
            # --oem 3: LSTM 엔진 사용
            # --psm 6: 균일한 텍스트 블록 가정

            # OCR 수행
            text = pytesseract.image_to_string(
                image,
                lang=lang,
                config=custom_config
            )

            return text

        except Exception as e:
            raise Exception(f"OCR 실패: {str(e)}")

    def parse_invoice_data(self, ocr_text: str) -> Dict:
        """
        OCR 텍스트를 구조화된 데이터로 파싱

        Args:
            ocr_text: OCR 결과 텍스트

        Returns:
            {
                'invoice_type': str ('GSC' | 'HACIELO' | 'UNKNOWN'),
                'supplier': str | None,
                'invoice_date': date | None,
                'total_amount': float | None,
                'total_weight': float | None,
                'contract_number': str | None (GSC only),
                'items': [
                    {
                        'no': int,
                        'bean_name': str,
                        'spec': str,
                        'quantity': int,
                        'weight': float,
                        'unit_price': float,
                        'amount': float
                    },
                    ...
                ] | []
            }
        """
        # 타입 자동 감지 및 파싱
        result = parse_invoice(ocr_text)

        return result

    def match_bean_to_db(
        self,
        bean_name: str,
        threshold: float = 0.7
    ) -> Tuple[Optional[Bean], float]:
        """
        원두명을 DB의 원두와 매칭 (유사도 기반)

        Args:
            bean_name: OCR 추출 원두명
            threshold: 최소 유사도 (0~1, 기본값 0.7)

        Returns:
            (매칭된 Bean 객체, 유사도 점수)
            매칭 실패 시 (None, 0.0)
        """
        # DB에서 모든 원두 조회
        beans = self.db.query(Bean).filter(
            Bean.is_active == True
        ).all()

        if not beans:
            return None, 0.0

        # 유사도 매칭
        matched_bean, score = fuzzy_match_bean(
            bean_name,
            beans,
            threshold=threshold
        )

        return matched_bean, score

    def calculate_confidence(
        self,
        parsed_data: Dict,
        ocr_text: str
    ) -> float:
        """
        인식 결과의 신뢰도 계산 (0~100)

        계산 로직:
        - 필수 필드 존재 여부 (60점)
        - 원두명 매칭 점수 (20점)
        - OCR 텍스트 길이 (10점)
        - 숫자 형식 유효성 (10점)

        Args:
            parsed_data: 파싱된 데이터 (parse_invoice_data 반환값)
            ocr_text: OCR 원본 텍스트

        Returns:
            신뢰도 점수 (0~100)
        """
        score = 0.0

        # GSC 타입: items 기반 검증
        if parsed_data.get('invoice_type') == 'GSC':
            items = parsed_data.get('items', [])

            # 1. 필수 필드 존재 (60점)
            # - invoice_date (15점)
            # - total_amount (15점)
            # - items (30점, 최소 1개 이상)
            if parsed_data.get('invoice_date'):
                score += 15
            if parsed_data.get('total_amount'):
                score += 15
            if len(items) > 0:
                score += 30

            # 2. 원두명 매칭 점수 (20점)
            # items가 있으면 첫 번째 항목의 원두명으로 매칭
            if items:
                first_item = items[0]
                bean_name = first_item.get('bean_name', '')
                if bean_name:
                    _, match_score = self.match_bean_to_db(bean_name)
                    score += match_score * 20

        else:
            # 기본 타입: 단일 항목 검증
            # 1. 필수 필드 존재 (각 15점)
            required_fields = ['bean_name', 'quantity', 'unit_price', 'invoice_date']
            for field in required_fields:
                if parsed_data.get(field):
                    score += 15

            # 2. 원두명 매칭 점수 (0~20점)
            bean_name = parsed_data.get('bean_name', '')
            if bean_name:
                _, match_score = self.match_bean_to_db(bean_name)
                score += match_score * 20

        # 3. OCR 텍스트 길이 (최소 100자 이상이면 만점)
        text_length_score = min(len(ocr_text) / 100, 1.0) * 10
        score += text_length_score

        # 4. 숫자 형식 유효성 (총액/중량이 양수면 각 5점)
        if parsed_data.get('total_amount', 0) > 0:
            score += 5
        if parsed_data.get('total_weight', 0) > 0:
            score += 5

        return min(score, 100.0)

    def process_image(
        self,
        image: Image.Image,
        preprocess: bool = True
    ) -> Dict:
        """
        이미지 전체 처리 파이프라인

        1. OCR 텍스트 추출
        2. 데이터 파싱
        3. 신뢰도 계산

        Args:
            image: PIL Image 객체
            preprocess: 전처리 수행 여부

        Returns:
            {
                'ocr_text': str,
                'parsed_data': Dict,
                'confidence': float,
                'warnings': List[str],
                'timestamp': datetime
            }
        """
        # 1. OCR 수행
        ocr_text = self.extract_text_from_image(image, preprocess=preprocess)

        # 2. 데이터 파싱
        parsed_data = self.parse_invoice_data(ocr_text)

        # 3. 신뢰도 계산
        confidence = self.calculate_confidence(parsed_data, ocr_text)

        # 4. 검증 (경고 메시지)
        warnings = []
        if parsed_data.get('invoice_type') == 'UNKNOWN':
            warnings.append("⚠️ 명세서 타입을 인식할 수 없습니다")

        # GSC 타입
        if parsed_data.get('invoice_type') == 'GSC':
            if not parsed_data.get('invoice_date'):
                warnings.append("⚠️ 거래일자를 찾을 수 없습니다")
            if not parsed_data.get('total_amount'):
                warnings.append("⚠️ 합계금액을 찾을 수 없습니다")
            if len(parsed_data.get('items', [])) == 0:
                warnings.append("⚠️ 원두 항목을 찾을 수 없습니다")
        else:
            # 기본 타입 검증
            _, validation_warnings = validate_parsed_data(parsed_data)
            warnings.extend(validation_warnings)

        return {
            'ocr_text': ocr_text,
            'parsed_data': parsed_data,
            'confidence': confidence,
            'warnings': warnings,
            'timestamp': datetime.now()
        }

    def get_supported_languages(self) -> list:
        """
        Tesseract가 지원하는 언어 목록 반환

        Returns:
            언어 코드 리스트 (예: ['eng', 'kor', 'osd'])
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            return []
