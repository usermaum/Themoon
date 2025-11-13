"""
Learning 서비스

사용자 수정 내역 학습 및 자동 제안
"""

from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from Levenshtein import distance as levenshtein_distance
import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.invoice import InvoiceLearning, InvoiceItem


class LearningService:
    """
    Learning 서비스

    사용자가 OCR 결과를 수정한 내역을 학습하여
    향후 동일한 오류 발생 시 자동 제안합니다.
    """

    def __init__(self, db: Session):
        """
        Args:
            db: SQLAlchemy Session
        """
        self.db = db

    def save_correction(
        self,
        invoice_item_id: int,
        field_name: str,
        ocr_value: str,
        corrected_value: str
    ) -> InvoiceLearning:
        """
        사용자 수정 내역 저장

        Args:
            invoice_item_id: InvoiceItem ID
            field_name: 수정한 필드명 (예: 'bean_name', 'quantity', 'unit_price')
            ocr_value: OCR 인식값
            corrected_value: 사용자 수정값

        Returns:
            저장된 InvoiceLearning 객체

        Raises:
            ValueError: InvoiceItem을 찾을 수 없음
        """
        # InvoiceItem 존재 확인
        invoice_item = self.db.query(InvoiceItem).filter(
            InvoiceItem.id == invoice_item_id
        ).first()

        if not invoice_item:
            raise ValueError(f"InvoiceItem을 찾을 수 없습니다: {invoice_item_id}")

        # 중복 체크 (동일한 OCR 값 + 필드명 조합)
        existing = self.db.query(InvoiceLearning).filter(
            InvoiceLearning.invoice_item_id == invoice_item_id,
            InvoiceLearning.field_name == field_name,
            InvoiceLearning.ocr_text == ocr_value
        ).first()

        if existing:
            # 이미 존재하면 수정값 업데이트
            existing.corrected_value = corrected_value
            existing.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(existing)
            return existing

        # 신규 학습 데이터 생성
        learning = InvoiceLearning(
            invoice_item_id=invoice_item_id,
            field_name=field_name,
            ocr_text=ocr_value,
            corrected_value=corrected_value
        )

        self.db.add(learning)
        self.db.commit()
        self.db.refresh(learning)

        return learning

    def get_learning_data(
        self,
        field_name: Optional[str] = None,
        limit: int = 100
    ) -> List[InvoiceLearning]:
        """
        학습 데이터 조회

        Args:
            field_name: 필드명 필터 (None이면 전체)
            limit: 조회 개수 (기본값: 100)

        Returns:
            InvoiceLearning 리스트 (최신순)
        """
        query = self.db.query(InvoiceLearning)

        if field_name:
            query = query.filter(InvoiceLearning.field_name == field_name)

        learnings = query.order_by(
            desc(InvoiceLearning.created_at)
        ).limit(limit).all()

        return learnings

    def suggest_correction(
        self,
        ocr_value: str,
        field_name: str,
        threshold: float = 0.8
    ) -> Optional[str]:
        """
        과거 학습 데이터 기반 제안

        유사한 OCR 값에 대한 과거 수정 내역을 찾아 제안합니다.

        Args:
            ocr_value: OCR 인식값
            field_name: 필드명
            threshold: 최소 유사도 (0~1, 기본값 0.8)

        Returns:
            제안값 (없으면 None)
        """
        # 해당 필드의 모든 학습 데이터 조회
        learnings = self.get_learning_data(field_name=field_name, limit=100)

        if not learnings:
            return None

        # 유사도 계산
        best_match = None
        best_score = 0.0

        for learning in learnings:
            # Levenshtein Distance 계산
            ocr_text = learning.ocr_text.lower().strip()
            input_text = ocr_value.lower().strip()

            max_len = max(len(ocr_text), len(input_text))
            if max_len == 0:
                continue

            dist = levenshtein_distance(ocr_text, input_text)
            similarity = 1 - (dist / max_len)

            # 최고 점수 업데이트
            if similarity > best_score:
                best_score = similarity
                best_match = learning.corrected_value

        # 임계값 이상만 반환
        if best_score >= threshold:
            return best_match
        else:
            return None

    def get_correction_stats(self, field_name: Optional[str] = None) -> Dict:
        """
        학습 데이터 통계

        Args:
            field_name: 필드명 필터 (None이면 전체)

        Returns:
            {
                'total_corrections': int,
                'by_field': {
                    'bean_name': int,
                    'quantity': int,
                    'unit_price': int,
                    ...
                },
                'most_common_corrections': [
                    {'ocr_text': str, 'corrected_value': str, 'count': int},
                    ...
                ]
            }
        """
        # 전체 수정 개수
        query = self.db.query(InvoiceLearning)
        if field_name:
            query = query.filter(InvoiceLearning.field_name == field_name)

        total_corrections = query.count()

        # 필드별 통계
        by_field = {}
        if not field_name:
            for field in ['bean_name', 'quantity', 'unit_price', 'invoice_date', 'supplier']:
                count = self.db.query(InvoiceLearning).filter(
                    InvoiceLearning.field_name == field
                ).count()
                by_field[field] = count
        else:
            by_field[field_name] = total_corrections

        # 자주 수정되는 패턴 (상위 10개)
        from sqlalchemy import func

        most_common = self.db.query(
            InvoiceLearning.ocr_text,
            InvoiceLearning.corrected_value,
            func.count(InvoiceLearning.id).label('count')
        ).group_by(
            InvoiceLearning.ocr_text,
            InvoiceLearning.corrected_value
        ).order_by(
            desc('count')
        ).limit(10).all()

        most_common_corrections = [
            {
                'ocr_text': item.ocr_text,
                'corrected_value': item.corrected_value,
                'count': item.count
            }
            for item in most_common
        ]

        return {
            'total_corrections': total_corrections,
            'by_field': by_field,
            'most_common_corrections': most_common_corrections
        }

    def batch_save_corrections(
        self,
        corrections: List[Dict]
    ) -> List[InvoiceLearning]:
        """
        여러 수정 내역 일괄 저장

        Args:
            corrections: [
                {
                    'invoice_item_id': int,
                    'field_name': str,
                    'ocr_value': str,
                    'corrected_value': str
                },
                ...
            ]

        Returns:
            저장된 InvoiceLearning 리스트
        """
        saved_learnings = []

        for correction in corrections:
            try:
                learning = self.save_correction(
                    invoice_item_id=correction['invoice_item_id'],
                    field_name=correction['field_name'],
                    ocr_value=correction['ocr_value'],
                    corrected_value=correction['corrected_value']
                )
                saved_learnings.append(learning)
            except Exception as e:
                # 개별 실패는 스킵하고 계속 진행
                continue

        return saved_learnings

    def delete_learning(self, learning_id: int) -> None:
        """
        학습 데이터 삭제

        Args:
            learning_id: InvoiceLearning ID

        Raises:
            ValueError: 학습 데이터를 찾을 수 없음
        """
        learning = self.db.query(InvoiceLearning).filter(
            InvoiceLearning.id == learning_id
        ).first()

        if not learning:
            raise ValueError(f"학습 데이터를 찾을 수 없습니다: {learning_id}")

        self.db.delete(learning)
        self.db.commit()

    def clear_learning_data(self, field_name: Optional[str] = None) -> int:
        """
        학습 데이터 초기화

        Args:
            field_name: 필드명 (None이면 전체 삭제)

        Returns:
            삭제된 개수
        """
        query = self.db.query(InvoiceLearning)

        if field_name:
            query = query.filter(InvoiceLearning.field_name == field_name)

        count = query.count()
        query.delete()
        self.db.commit()

        return count
