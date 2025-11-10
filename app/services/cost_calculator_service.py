"""
투입량 계산기 서비스
원가계산기 고도화 - Phase 2: 투입량 계산기

기능:
- 목표 산출량 기반 투입량 계산 (역산)
- 원두별 손실률 통계 조회
- 산출량 예측
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from app.models.database import Bean, RoastingLog
import math


class CostCalculatorService:
    """투입량 계산기 서비스"""

    def __init__(self, db: Session):
        self.db = db

    # ═══════════════════════════════════════════════════════════════
    # 원두별 통계 조회
    # ═══════════════════════════════════════════════════════════════

    def get_bean_statistics(self, bean_id: Optional[int] = None) -> Dict:
        """
        원두별 손실률 통계 조회

        Args:
            bean_id: 원두 ID (None이면 전체 평균)

        Returns:
            {
                'bean_id': 1,
                'bean_name': '예가체프',
                'avg_loss_rate': 18.36,
                'std_loss_rate': 3.19,
                'sample_count': 12,
                'min_loss_rate': 14.0,
                'max_loss_rate': 23.5,
                'last_roasted_date': '2025-11-08'
            }
        """
        if bean_id:
            # 특정 원두 통계
            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            if not bean:
                return {
                    'error': '원두를 찾을 수 없습니다',
                    'bean_id': bean_id
                }

            # Bean 테이블에 저장된 통계 사용
            if bean.avg_loss_rate is not None:
                return {
                    'bean_id': bean.id,
                    'bean_name': bean.name,
                    'avg_loss_rate': bean.avg_loss_rate,
                    'std_loss_rate': bean.std_loss_rate or 0.0,
                    'sample_count': bean.total_roasted_count or 0,
                    'last_roasted_date': bean.last_roasted_date.isoformat() if bean.last_roasted_date else None
                }
            else:
                # 통계가 없으면 기본값 (17%)
                return {
                    'bean_id': bean.id,
                    'bean_name': bean.name,
                    'avg_loss_rate': 17.0,
                    'std_loss_rate': 2.0,
                    'sample_count': 0,
                    'last_roasted_date': None,
                    'warning': '로스팅 기록이 없어 기본값(17%)을 사용합니다'
                }
        else:
            # 전체 평균 통계
            beans_with_stats = self.db.query(Bean).filter(
                Bean.avg_loss_rate.isnot(None),
                Bean.status == "active"
            ).all()

            if not beans_with_stats:
                return {
                    'bean_id': None,
                    'bean_name': '전체 평균',
                    'avg_loss_rate': 17.0,
                    'std_loss_rate': 2.0,
                    'sample_count': 0,
                    'warning': '로스팅 기록이 없어 기본값(17%)을 사용합니다'
                }

            # 가중 평균 계산 (로스팅 횟수를 가중치로)
            total_weighted_loss = 0.0
            total_count = 0

            for bean in beans_with_stats:
                if bean.total_roasted_count and bean.total_roasted_count > 0:
                    total_weighted_loss += bean.avg_loss_rate * bean.total_roasted_count
                    total_count += bean.total_roasted_count

            if total_count > 0:
                avg_loss = total_weighted_loss / total_count
            else:
                avg_loss = 17.0

            # 표준편차 계산 (간단히 평균으로)
            std_values = [bean.std_loss_rate for bean in beans_with_stats if bean.std_loss_rate]
            avg_std = sum(std_values) / len(std_values) if std_values else 2.0

            return {
                'bean_id': None,
                'bean_name': '전체 평균',
                'avg_loss_rate': round(avg_loss, 2),
                'std_loss_rate': round(avg_std, 2),
                'sample_count': total_count,
                'bean_count': len(beans_with_stats)
            }

    # ═══════════════════════════════════════════════════════════════
    # 투입량 계산 (역산)
    # ═══════════════════════════════════════════════════════════════

    def calculate_required_input(
        self,
        target_output_kg: float,
        bean_id: Optional[int] = None,
        safety_margin: float = 0.02
    ) -> Dict:
        """
        목표 산출량 기반 투입량 계산 (역산)

        Args:
            target_output_kg: 목표 산출량 (kg)
            bean_id: 원두 ID (None이면 전체 평균 사용)
            safety_margin: 안전 여유율 (기본 2%)

        Returns:
            {
                'target_output': 10.0,
                'bean_id': 1,
                'bean_name': '예가체프',
                'avg_loss_rate': 18.36,
                'std_loss_rate': 3.19,
                'sample_count': 12,
                'calculated_input': 12.21,
                'recommended_input': 12.45,
                'safety_margin_kg': 0.24,
                'min_output': 9.68,
                'expected_output': 10.0,
                'max_output': 10.32
            }
        """
        # 1. 원두 통계 조회
        stats = self.get_bean_statistics(bean_id)

        if 'error' in stats:
            return stats

        avg_loss_rate = stats['avg_loss_rate'] / 100  # 18.36 → 0.1836
        std_loss_rate = stats['std_loss_rate'] / 100  # 3.19 → 0.0319

        # 2. 기본 투입량 계산
        # 공식: 투입량 = 산출량 ÷ (1 - 손실률)
        calculated_input = target_output_kg / (1 - avg_loss_rate)

        # 3. 여유분 추가
        recommended_input = calculated_input * (1 + safety_margin)

        # 4. 예상 범위 계산 (표준편차 고려)
        # 손실률 범위: [평균 - 표준편차, 평균 + 표준편차]
        min_loss = max(0.0, avg_loss_rate - std_loss_rate)
        max_loss = min(1.0, avg_loss_rate + std_loss_rate)

        # 권장 투입량으로 로스팅 시 예상 산출량 범위
        min_output = recommended_input * (1 - max_loss)
        expected_output = recommended_input * (1 - avg_loss_rate)
        max_output = recommended_input * (1 - min_loss)

        # 5. 반올림
        return {
            'target_output': target_output_kg,
            'bean_id': stats.get('bean_id'),
            'bean_name': stats['bean_name'],
            'avg_loss_rate': stats['avg_loss_rate'],
            'std_loss_rate': stats['std_loss_rate'],
            'sample_count': stats['sample_count'],
            'calculated_input': round(calculated_input, 2),
            'recommended_input': round(recommended_input, 2),
            'safety_margin_kg': round(recommended_input - calculated_input, 2),
            'min_output': round(min_output, 2),
            'expected_output': round(expected_output, 2),
            'max_output': round(max_output, 2),
            'warning': stats.get('warning')
        }

    # ═══════════════════════════════════════════════════════════════
    # 산출량 예측
    # ═══════════════════════════════════════════════════════════════

    def predict_output(
        self,
        input_weight_kg: float,
        bean_id: Optional[int] = None
    ) -> Dict:
        """
        투입량 기반 산출량 예측 (정방향)

        Args:
            input_weight_kg: 투입량 (kg)
            bean_id: 원두 ID (None이면 전체 평균 사용)

        Returns:
            {
                'input_weight': 12.0,
                'bean_name': '예가체프',
                'avg_loss_rate': 18.36,
                'std_loss_rate': 3.19,
                'min_output': 9.17,
                'expected_output': 9.80,
                'max_output': 10.43,
                'min_loss_kg': 1.57,
                'expected_loss_kg': 2.20,
                'max_loss_kg': 2.83
            }
        """
        # 1. 원두 통계 조회
        stats = self.get_bean_statistics(bean_id)

        if 'error' in stats:
            return stats

        avg_loss_rate = stats['avg_loss_rate'] / 100
        std_loss_rate = stats['std_loss_rate'] / 100

        # 2. 손실률 범위
        min_loss = max(0.0, avg_loss_rate - std_loss_rate)
        max_loss = min(1.0, avg_loss_rate + std_loss_rate)

        # 3. 산출량 예측
        min_output = input_weight_kg * (1 - max_loss)
        expected_output = input_weight_kg * (1 - avg_loss_rate)
        max_output = input_weight_kg * (1 - min_loss)

        # 4. 손실량 예측
        min_loss_kg = input_weight_kg - max_output
        expected_loss_kg = input_weight_kg - expected_output
        max_loss_kg = input_weight_kg - min_output

        return {
            'input_weight': input_weight_kg,
            'bean_id': stats.get('bean_id'),
            'bean_name': stats['bean_name'],
            'avg_loss_rate': stats['avg_loss_rate'],
            'std_loss_rate': stats['std_loss_rate'],
            'sample_count': stats['sample_count'],
            'min_output': round(min_output, 2),
            'expected_output': round(expected_output, 2),
            'max_output': round(max_output, 2),
            'min_loss_kg': round(min_loss_kg, 2),
            'expected_loss_kg': round(expected_loss_kg, 2),
            'max_loss_kg': round(max_loss_kg, 2),
            'warning': stats.get('warning')
        }

    # ═══════════════════════════════════════════════════════════════
    # 원두별 로스팅 기록 통계 업데이트
    # ═══════════════════════════════════════════════════════════════

    def update_bean_statistics(self, bean_id: int) -> bool:
        """
        특정 원두의 손실률 통계 재계산 및 업데이트

        Args:
            bean_id: 원두 ID

        Returns:
            성공 여부
        """
        try:
            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            if not bean:
                return False

            # 해당 원두의 로스팅 기록 조회
            roasting_logs = self.db.query(RoastingLog).filter(
                RoastingLog.bean_id == bean_id
            ).all()

            if roasting_logs:
                # 손실률 리스트
                loss_rates = [log.loss_rate_percent for log in roasting_logs]

                # 평균 계산
                avg_loss = sum(loss_rates) / len(loss_rates)

                # 표준편차 계산
                variance = sum((x - avg_loss) ** 2 for x in loss_rates) / len(loss_rates)
                std_loss = math.sqrt(variance)

                # 마지막 로스팅 날짜
                last_date = max(log.roasting_date for log in roasting_logs)

                # Bean 통계 업데이트
                bean.avg_loss_rate = round(avg_loss, 2)
                bean.std_loss_rate = round(std_loss, 2)
                bean.total_roasted_count = len(roasting_logs)
                bean.last_roasted_date = last_date

                self.db.commit()
                return True
            else:
                # 로스팅 기록이 없으면 통계 초기화
                bean.avg_loss_rate = None
                bean.std_loss_rate = None
                bean.total_roasted_count = 0
                bean.last_roasted_date = None

                self.db.commit()
                return True

        except Exception as e:
            self.db.rollback()
            print(f"❌ 통계 업데이트 실패: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════
    # 원가 계산 (기존 기능 통합)
    # ═══════════════════════════════════════════════════════════════

    def calculate_cost(
        self,
        bean_id: int,
        quantity_kg: float,
        include_loss: bool = True
    ) -> Dict:
        """
        원두 원가 계산 (손실률 고려 옵션)

        Args:
            bean_id: 원두 ID
            quantity_kg: 원두 수량 (kg)
            include_loss: 손실률 포함 여부 (True면 생두 기준 계산)

        Returns:
            {
                'bean_name': '예가체프',
                'quantity_kg': 10.0,
                'price_per_kg': 30000,
                'raw_bean_cost': 366300,  # 손실률 고려한 생두 원가
                'roasted_bean_cost': 300000,  # 원두 직접 원가
                'avg_loss_rate': 18.36,
                'raw_bean_needed': 12.21
            }
        """
        bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
        if not bean:
            return {'error': '원두를 찾을 수 없습니다'}

        roasted_bean_cost = quantity_kg * bean.price_per_kg

        if include_loss:
            # 손실률 고려
            stats = self.get_bean_statistics(bean_id)
            avg_loss_rate = stats['avg_loss_rate'] / 100

            # 필요한 생두량 계산
            raw_bean_needed = quantity_kg / (1 - avg_loss_rate)
            raw_bean_cost = raw_bean_needed * bean.price_per_kg

            return {
                'bean_id': bean.id,
                'bean_name': bean.name,
                'quantity_kg': quantity_kg,
                'price_per_kg': bean.price_per_kg,
                'raw_bean_cost': round(raw_bean_cost, 0),
                'roasted_bean_cost': round(roasted_bean_cost, 0),
                'avg_loss_rate': stats['avg_loss_rate'],
                'raw_bean_needed': round(raw_bean_needed, 2)
            }
        else:
            return {
                'bean_id': bean.id,
                'bean_name': bean.name,
                'quantity_kg': quantity_kg,
                'price_per_kg': bean.price_per_kg,
                'roasted_bean_cost': round(roasted_bean_cost, 0)
            }
