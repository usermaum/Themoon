"""
OCR 서비스

거래 명세서 이미지에서 텍스트를 추출하고 구조화된 데이터로 파싱합니다.
"""

from typing import Dict, Tuple, Optional, TYPE_CHECKING
from datetime import datetime
from PIL import Image
import pytesseract
from pytesseract import Output
import easyocr
import numpy as np
from sqlalchemy.orm import Session
import streamlit as st
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
from utils.image_utils import preprocess_image, preprocess_for_easyocr

# Type hints only (순환 참조 방지)
if TYPE_CHECKING:
    from services.learning_service import LearningService


@st.cache_resource
def get_easyocr_reader():
    """
    EasyOCR Reader 싱글톤 (캐싱)

    첫 실행: ~20-30초 (모델 다운로드 + 로드)
    이후 실행: <1초 (캐시된 인스턴스 재사용)

    Returns:
        easyocr.Reader: 한글+영문 OCR Reader
    """
    return easyocr.Reader(['ko', 'en'], gpu=False)


class OCRService:
    """
    OCR 서비스

    EasyOCR을 사용하여 이미지에서 텍스트를 추출하고
    구조화된 데이터로 파싱합니다.
    """

    def __init__(self, db: Session, learning_service: Optional['LearningService'] = None):
        """
        Args:
            db: SQLAlchemy Session
            learning_service: LearningService 인스턴스 (학습 기능 사용 시)
        """
        self.db = db
        self.learning_service = learning_service
        # EasyOCR reader (캐시된 싱글톤 사용)
        self.reader = get_easyocr_reader()

    def extract_text_from_image(
        self,
        image: Image.Image,
        lang: str = 'kor+eng',  # 호환성 유지 (사용 안 함)
        preprocess: bool = False,
        psm_mode: int = 6,  # 호환성 유지 (사용 안 함)
        return_data: bool = False,  # 신뢰도 데이터 반환 옵션
        preprocess_mode: str = 'normal'  # 전처리 모드 ('normal' 또는 'enhanced')
    ):
        """
        이미지에서 텍스트 추출 (EasyOCR)

        Args:
            image: PIL Image 객체
            lang: OCR 언어 (호환성 유지, 사용 안 함)
            preprocess: 전처리 수행 여부 (EasyOCR용 전처리, 기본값: True로 권장)
            psm_mode: Page Segmentation Mode (호환성 유지, 사용 안 함)
            return_data: True면 상세 데이터(좌표, 신뢰도) 반환 (기본값: False)
            preprocess_mode: 전처리 강도 ('normal' 또는 'enhanced')

        Returns:
            return_data=False: 추출된 텍스트 (str)
            return_data=True: {
                'text': str,           # 전체 텍스트
                'words': List[Dict],   # 단어별 상세 정보
                'confidence': float    # 평균 신뢰도
            }

        Raises:
            Exception: OCR 실패 시
        """
        try:
            # 전처리 수행 (EasyOCR용)
            if preprocess:
                image = preprocess_for_easyocr(image, enhance=True, mode=preprocess_mode)

            # PIL Image → numpy array
            image_np = np.array(image)

            # EasyOCR 수행
            results = self.reader.readtext(image_np)
            # results: List of ([box_coordinates], text, confidence)

            if return_data:
                # 단어별 정보 추출
                words = []
                confidences = []
                text_parts = []

                for (bbox, text, conf) in results:
                    if text.strip():  # 빈 문자열 제외
                        # bbox: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                        x_coords = [point[0] for point in bbox]
                        y_coords = [point[1] for point in bbox]

                        left = int(min(x_coords))
                        top = int(min(y_coords))
                        width = int(max(x_coords) - min(x_coords))
                        height = int(max(y_coords) - min(y_coords))

                        words.append({
                            'text': text,
                            'confidence': conf * 100,  # 0~1 → 0~100
                            'left': left,
                            'top': top,
                            'width': width,
                            'height': height
                        })
                        confidences.append(conf * 100)
                        text_parts.append(text)

                # 전체 텍스트 재구성 (줄바꿈으로 연결)
                full_text = '\n'.join(text_parts)

                # 평균 신뢰도 계산
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

                return {
                    'text': full_text,
                    'words': words,
                    'confidence': avg_confidence
                }
            else:
                # 기존 방식 (텍스트만)
                text_parts = [text for (_, text, _) in results if text.strip()]
                full_text = '\n'.join(text_parts)
                return full_text

        except Exception as e:
            raise Exception(f"OCR 실패: {str(e)}")

    def calculate_confidence_score(self, parsed_data: Dict) -> float:
        """
        파싱 결과의 신뢰도 점수 계산 (0~100)

        신뢰도 계산 기준:
        - 필수 필드 존재 여부 (supplier, invoice_date, items)
        - items 개수 (1개 이상)
        - items 각 필드 완성도 (bean_name, quantity, unit_price, amount)

        Args:
            parsed_data: 파싱 결과

        Returns:
            신뢰도 점수 (0~100)
        """
        score = 0.0

        # 1. 공급업체 존재 (20점)
        if parsed_data.get('supplier'):
            score += 20

        # 2. 날짜 존재 (20점)
        if parsed_data.get('invoice_date'):
            score += 20

        # 3. items 존재 및 개수 (30점)
        items = parsed_data.get('items', [])
        if items:
            score += 15  # items 존재
            if len(items) >= 3:
                score += 15  # 3개 이상
            else:
                score += 5 * len(items)  # 개수 비례

        # 4. items 각 필드 완성도 (30점)
        if items:
            field_scores = []
            for item in items:
                item_score = 0
                # 필수 필드: bean_name, quantity, unit_price, amount
                if item.get('bean_name'):
                    item_score += 0.25
                if item.get('quantity') is not None:
                    item_score += 0.25
                if item.get('unit_price') is not None:
                    item_score += 0.25
                if item.get('amount') is not None:
                    item_score += 0.25
                field_scores.append(item_score)

            # 평균 완성도 * 30점
            if field_scores:
                avg_completeness = sum(field_scores) / len(field_scores)
                score += avg_completeness * 30

        return round(score, 1)

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
                'confidence_score': float (0~100),  # 신뢰도 점수
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

        # 신뢰도 점수 계산
        confidence = self.calculate_confidence_score(result)
        result['confidence_score'] = confidence

        return result

    def parse_invoice_data_with_learning(self, ocr_text: str, threshold: float = 0.8) -> Dict:
        """
        학습 데이터를 참고하여 OCR 텍스트 파싱

        기본 파싱 후 과거 학습 데이터를 기반으로 자동 제안을 추가합니다.
        제안은 '{field}_suggested' 키로 추가됩니다.

        Args:
            ocr_text: OCR 결과 텍스트
            threshold: 학습 제안 최소 유사도 (0~1, 기본값 0.8)

        Returns:
            파싱 결과 + 학습 제안
            {
                'bean_name': '...',
                'bean_name_suggested': '...',  # 학습 제안 (있을 경우)
                'quantity': 10,
                'quantity_suggested': 12,      # 학습 제안 (있을 경우)
                ...
            }
        """
        # 1. 기본 파싱
        parsed = self.parse_invoice_data(ocr_text)

        # 2. 학습 서비스가 없으면 기본 파싱 결과만 반환
        if not self.learning_service:
            return parsed

        # 3. GSC 타입: items에 학습 제안 추가
        if parsed.get('invoice_type') == 'GSC':
            items = parsed.get('items', [])
            for item in items:
                # 원두명 제안
                bean_name = item.get('bean_name', '')
                if bean_name:
                    suggestion = self.learning_service.suggest_correction(
                        str(bean_name), 'bean_name', threshold=threshold
                    )
                    if suggestion and suggestion != bean_name:
                        item['bean_name_suggested'] = suggestion

                # 중량 제안
                weight = item.get('weight')
                if weight is not None:
                    suggestion = self.learning_service.suggest_correction(
                        str(weight), 'weight', threshold=threshold
                    )
                    if suggestion:
                        try:
                            suggested_weight = float(suggestion)
                            if suggested_weight != weight:
                                item['weight_suggested'] = suggested_weight
                        except (ValueError, TypeError):
                            pass

                # 단가 제안
                unit_price = item.get('unit_price')
                if unit_price is not None:
                    suggestion = self.learning_service.suggest_correction(
                        str(unit_price), 'unit_price', threshold=threshold
                    )
                    if suggestion:
                        try:
                            suggested_price = float(suggestion)
                            if suggested_price != unit_price:
                                item['unit_price_suggested'] = suggested_price
                        except (ValueError, TypeError):
                            pass

        else:
            # 4. 기본 타입: 단일 필드에 학습 제안 추가
            for field in ['bean_name', 'quantity', 'unit_price']:
                value = parsed.get(field)
                if value is not None:
                    suggestion = self.learning_service.suggest_correction(
                        str(value), field, threshold=threshold
                    )
                    if suggestion and str(suggestion) != str(value):
                        parsed[f'{field}_suggested'] = suggestion

        return parsed

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
            Bean.status == "active"
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
        total_amount = parsed_data.get('total_amount') or 0
        if total_amount > 0:
            score += 5
        total_weight = parsed_data.get('total_weight') or 0
        if total_weight > 0:
            score += 5

        return min(score, 100.0)

    def process_image(
        self,
        image: Image.Image,
        preprocess: bool = True
    ) -> Dict:
        """
        이미지 전체 처리 파이프라인

        1. OCR 텍스트 추출 (상세 데이터 포함)
        2. 데이터 파싱
        3. 신뢰도 계산

        Args:
            image: PIL Image 객체
            preprocess: 전처리 수행 여부

        Returns:
            {
                'success': bool,  # 처리 성공 여부
                'ocr_text': str,
                'ocr_confidence': float,  # OCR 평균 신뢰도 (0~100)
                'ocr_words': List[Dict],  # 단어별 상세 정보
                'parsed_data': Dict,
                'confidence': float,
                'warnings': List[str],
                'timestamp': datetime
            }
        """
        # 1. OCR 수행 (상세 데이터 포함)
        ocr_result = self.extract_text_from_image(
            image,
            preprocess=preprocess,
            return_data=True  # 신뢰도 데이터 포함
        )

        ocr_text = ocr_result['text']
        ocr_words = ocr_result['words']
        ocr_confidence = ocr_result['confidence']

        # 2. 데이터 파싱
        parsed_data = self.parse_invoice_data(ocr_text)

        # 3. 신뢰도 계산
        confidence = self.calculate_confidence(parsed_data, ocr_text)

        # 4. 검증 (경고 메시지)
        warnings = []

        # OCR 신뢰도 낮으면 경고
        if ocr_confidence < 60:
            warnings.append(f"⚠️ OCR 인식 신뢰도가 낮습니다 ({ocr_confidence:.1f}%)")
            warnings.append(f"💡 더 선명한 이미지로 다시 시도해주세요")

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

        # 5. 성공 여부 판단
        success = (
            parsed_data.get('invoice_type') != 'UNKNOWN' and
            len(parsed_data.get('items', [])) > 0
        )

        return {
            'success': success,
            'ocr_text': ocr_text,
            'ocr_confidence': ocr_confidence,
            'ocr_words': ocr_words,
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
