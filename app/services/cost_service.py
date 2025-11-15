"""
CostService: 원가 계산 서비스

블렌드의 최종 원가를 계산합니다.
핵심 공식: Final Cost = (Σ(Bean Cost × Ratio%)) / (1 - Loss Rate)
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from models.database import Bean, Blend, BlendRecipe, CostSetting, BeanPriceHistory
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CostService:
    """원가 계산 서비스 (핵심 비즈니스 로직)"""

    # 손실률 상수
    STANDARD_LOSS_RATE = 0.17  # 17%

    @staticmethod
    def get_blend_cost(
        db: Session,
        blend_id: int,
        unit: str = 'kg',
        use_current_recipes: bool = True
    ) -> dict:
        """
        블렌드의 최종 원가 계산

        공식: Final Cost = (Σ(Bean Cost × Ratio%)) / (1 - Loss Rate)

        예시 (풀문):
        - 예가체프 40% @ 5,500원/kg = 2,200원
        - 안티구아 40% @ 6,000원/kg = 2,400원
        - 모모라 10% @ 4,500원/kg = 450원
        - g4 10% @ 5,200원/kg = 520원
        ------------------------------------------
        - 혼합 원가 = 5,570원
        - 손실률 17% 반영 = 5,570 / 0.83 = 6,711원/kg

        Args:
            db: SQLAlchemy 세션
            blend_id: 블렌드 ID
            unit: 'kg' 또는 'cup' (1cup = 200g)
            use_current_recipes: 현재 레시피만 사용 여부

        Returns:
            {
                'blend_id': int,
                'blend_name': str,
                'component_costs': [
                    {'bean_name': str, 'ratio': float, 'price_per_kg': float, 'component_cost': float}
                ],
                'blend_cost_before_loss': float,  # 혼합 원가
                'loss_rate': float,               # 손실률
                'final_cost_per_kg': float,       # 최종 원가/kg
                'final_cost_per_unit': float,     # 단위당 원가
                'selling_price': float,           # 제안 판매가
                'margin_percent': float           # 마진율 (%)
            }
        """

        blend = db.query(Blend).filter(Blend.id == blend_id).first()
        if not blend:
            raise ValueError(f"블렌드를 찾을 수 없습니다: {blend_id}")

        # 현재 레시피 조회
        recipes = db.query(BlendRecipe).filter(
            BlendRecipe.blend_id == blend_id
        ).all()

        if not recipes:
            logger.warning(f"⚠️ 블렌드 {blend_id}({blend.name})에 레시피가 없습니다")

        # 혼합 원가 계산
        component_costs = []
        total_blend_cost = 0

        for recipe in recipes:
            bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
            if not bean:
                logger.warning(f"⚠️ 원두 ID {recipe.bean_id}를 찾을 수 없습니다")
                continue

            # 원두 가격 (기본값: 5,000원/kg)
            bean_price = bean.price_per_kg if bean.price_per_kg > 0 else 5000

            # 원두 비율을 사용한 원가 계산
            ratio_percent = recipe.ratio if hasattr(recipe, 'ratio') else 0
            component_cost = bean_price * (ratio_percent / 100)
            total_blend_cost += component_cost

            component_costs.append({
                'bean_name': bean.name,
                'ratio': ratio_percent,
                'price_per_kg': bean_price,
                'component_cost': round(component_cost, 0)
            })

        # 손실률 반영한 최종 원가
        loss_rate = CostService.STANDARD_LOSS_RATE
        final_cost_per_kg = total_blend_cost / (1 - loss_rate)

        # 단위별 계산
        final_cost_per_unit = final_cost_per_kg
        if unit == 'cup':
            final_cost_per_unit = (final_cost_per_kg * 0.2)  # 1cup = 200g = 0.2kg

        # 마진율 계산
        margin = 0
        selling_price = blend.suggested_price if blend.suggested_price > 0 else None
        if selling_price and selling_price > 0:
            margin = ((selling_price - final_cost_per_kg) / selling_price * 100)

        logger.info(f"✓ 원가 계산: {blend.name} = {final_cost_per_kg:.0f}원/kg")

        return {
            'blend_id': blend.id,
            'blend_name': blend.name,
            'component_costs': component_costs,
            'blend_cost_before_loss': round(total_blend_cost, 0),
            'loss_rate': CostService.STANDARD_LOSS_RATE * 100,
            'final_cost_per_kg': round(final_cost_per_kg, 0),
            'final_cost_per_unit': round(final_cost_per_unit, 0),
            'selling_price': selling_price,
            'margin_percent': round(margin, 1) if margin else None
        }

    @staticmethod
    def update_bean_price(db: Session, bean_id: int, new_price: float, change_reason: str = None):
        """원두 가격 업데이트 (이력 자동 기록)

        Args:
            db: SQLAlchemy 세션
            bean_id: 원두 ID
            new_price: 새 가격 (원/kg)
            change_reason: 변경 사유 (선택사항)

        Returns:
            업데이트된 Bean 객체

        Raises:
            ValueError: 원두를 찾을 수 없거나 가격이 0 이하인 경우
        """
        if new_price <= 0:
            raise ValueError(f"가격은 0보다 커야 합니다: {new_price}")

        bean = db.query(Bean).filter(Bean.id == bean_id).first()
        if not bean:
            raise ValueError(f"원두를 찾을 수 없습니다: {bean_id}")

        old_price = bean.price_per_kg

        # 가격이 실제로 변경된 경우에만 이력 기록
        if old_price != new_price:
            # 가격 변경 이력 저장
            price_history = BeanPriceHistory(
                bean_id=bean_id,
                old_price=old_price,
                new_price=new_price,
                change_reason=change_reason
            )
            db.add(price_history)

            # 원두 가격 업데이트
            bean.price_per_kg = new_price
            bean.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(bean)

            logger.info(f"✓ 원두 가격 업데이트: {bean.name} ({old_price:.0f}원 → {new_price:.0f}원/kg)")
        else:
            logger.info(f"ℹ️ 가격 변경 없음: {bean.name} ({old_price:.0f}원/kg)")

        return bean

    @staticmethod
    def batch_calculate_all_blends(db: Session) -> list:
        """모든 활성 블렌드의 원가 계산 (일괄)

        Args:
            db: SQLAlchemy 세션

        Returns:
            모든 블렌드의 원가 계산 결과 리스트
        """
        blends = db.query(Blend).filter(Blend.status == 'active').all()
        results = []

        logger.info(f"📊 일괄 원가 계산 시작: {len(blends)}개 블렌드")

        for blend in blends:
            try:
                cost_data = CostService.get_blend_cost(db, blend.id)
                results.append(cost_data)
            except Exception as e:
                error_msg = f"블렌드 {blend.id}({blend.name}) 계산 실패: {str(e)}"
                logger.error(f"❌ {error_msg}")
                results.append({
                    'blend_id': blend.id,
                    'blend_name': blend.name,
                    'error': str(e)
                })

        logger.info(f"✓ 일괄 원가 계산 완료: {len(results)}건")

        return results

    @staticmethod
    def get_cost_setting(db: Session, parameter_name: str) -> float:
        """비용 설정값 조회

        Args:
            db: SQLAlchemy 세션
            parameter_name: 설정 파라미터 명

        Returns:
            설정값 (찾지 못하면 0.0)
        """
        setting = db.query(CostSetting).filter(
            CostSetting.parameter_name == parameter_name
        ).first()

        return setting.value if setting else 0.0

    @staticmethod
    def update_cost_setting(
        db: Session,
        parameter_name: str,
        value: float,
        description: str = None
    ) -> CostSetting:
        """비용 설정값 업데이트

        Args:
            db: SQLAlchemy 세션
            parameter_name: 설정 파라미터 명
            value: 설정값
            description: 설명

        Returns:
            업데이트된 CostSetting 객체
        """
        setting = db.query(CostSetting).filter(
            CostSetting.parameter_name == parameter_name
        ).first()

        if setting:
            setting.value = value
            if description:
                setting.description = description
            setting.updated_at = datetime.utcnow()
        else:
            setting = CostSetting(
                parameter_name=parameter_name,
                value=value,
                description=description
            )
            db.add(setting)

        db.commit()
        db.refresh(setting)

        logger.info(f"✓ 설정 업데이트: {parameter_name} = {value}")

        return setting

    @staticmethod
    def calculate_blend_cost_with_components(
        db: Session,
        blend_id: int
    ) -> dict:
        """원가 상세 분석 (각 원두별 기여도 포함)

        Args:
            db: SQLAlchemy 세션
            blend_id: 블렌드 ID

        Returns:
            상세 원가 분석 결과
        """
        base_result = CostService.get_blend_cost(db, blend_id)

        # 각 원두별 최종 원가 기여도 계산
        components_with_final = []
        for comp in base_result['component_costs']:
            final_contribution = comp['component_cost'] / (1 - CostService.STANDARD_LOSS_RATE)
            components_with_final.append({
                **comp,
                'final_contribution': round(final_contribution, 0)
            })

        return {
            **base_result,
            'component_costs': components_with_final
        }

    @staticmethod
    def get_bean_price_history(db: Session, bean_id: int, limit: int = 10) -> list:
        """원두 가격 변경 이력 조회

        Args:
            db: SQLAlchemy 세션
            bean_id: 원두 ID
            limit: 조회할 이력 개수 (기본 10개)

        Returns:
            가격 변경 이력 리스트 (최신순)
            [
                {
                    'id': int,
                    'bean_id': int,
                    'bean_name': str,
                    'old_price': float,
                    'new_price': float,
                    'price_change': float,  # 변동액
                    'price_change_percent': float,  # 변동률 (%)
                    'change_reason': str,
                    'created_at': datetime
                },
                ...
            ]
        """
        bean = db.query(Bean).filter(Bean.id == bean_id).first()
        if not bean:
            raise ValueError(f"원두를 찾을 수 없습니다: {bean_id}")

        history_records = db.query(BeanPriceHistory).filter(
            BeanPriceHistory.bean_id == bean_id
        ).order_by(desc(BeanPriceHistory.created_at)).limit(limit).all()

        result = []
        for record in history_records:
            price_change = record.new_price - record.old_price
            price_change_percent = (price_change / record.old_price * 100) if record.old_price > 0 else 0

            result.append({
                'id': record.id,
                'bean_id': record.bean_id,
                'bean_name': bean.name,
                'old_price': record.old_price,
                'new_price': record.new_price,
                'price_change': price_change,
                'price_change_percent': round(price_change_percent, 1),
                'change_reason': record.change_reason,
                'created_at': record.created_at
            })

        return result
