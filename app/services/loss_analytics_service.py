"""
LossAnalyticsService: 손실률 예측 및 계절성 분석 서비스

이동평균과 계절 지수를 활용한 손실률 예측 모델을 제공합니다.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import RoastingLog
from datetime import datetime, timedelta
import statistics
import logging

logger = logging.getLogger(__name__)


class LossAnalyticsService:
    """손실률 예측 및 계절성 분석 서비스"""

    # 계절 지수 캐시 (메모리)
    _seasonal_index_cache = None
    _cache_updated_at = None

    @classmethod
    def calculate_seasonal_index(cls, db: Session) -> dict:
        """
        월별 계절 지수 계산

        계절 지수 = 월별 평균 손실률 / 전체 평균 손실률
        1.0보다 크면 해당 월의 손실률이 평균보다 높음 (여름)
        1.0보다 작으면 해당 월의 손실률이 평균보다 낮음 (겨울)

        Args:
            db: SQLAlchemy 세션

        Returns:
            {
                '01': 0.95,  # 1월: 평균보다 5% 낮음
                '02': 0.97,
                ...
                '07': 1.15,  # 7월: 평균보다 15% 높음
                ...
            }
        """
        # 1. 월별 평균 손실률 조회
        monthly_avg = db.query(
            func.substr(RoastingLog.roasting_month, 6, 2).label('month'),
            func.avg(RoastingLog.loss_rate_percent).label('avg_loss')
        ).group_by('month').all()

        if not monthly_avg:
            logger.warning("⚠️ 월별 데이터가 없어 계절 지수를 계산할 수 없습니다")
            return {}

        # 2. 전체 평균 계산
        global_avg = db.query(
            func.avg(RoastingLog.loss_rate_percent)
        ).scalar()

        if not global_avg or global_avg == 0:
            logger.warning("⚠️ 전체 평균 손실률이 0이거나 없습니다")
            return {}

        # 3. 계절 지수 = 월별 평균 / 전체 평균
        seasonal_index = {}
        for month, avg_loss in monthly_avg:
            seasonal_index[month] = avg_loss / global_avg

        # 4. 캐싱
        cls._seasonal_index_cache = seasonal_index
        cls._cache_updated_at = datetime.now()

        logger.info(f"✓ 계절 지수 계산 완료: {len(seasonal_index)}개월 데이터")

        return seasonal_index

    @classmethod
    def get_seasonal_index(cls, db: Session, force_refresh: bool = False) -> dict:
        """
        계절 지수 조회 (캐시 사용)

        Args:
            db: SQLAlchemy 세션
            force_refresh: 강제 재계산 여부

        Returns:
            계절 지수 dict
        """
        # 캐시가 없거나 강제 갱신 시 재계산
        if force_refresh or not cls._seasonal_index_cache:
            return cls.calculate_seasonal_index(db)

        # 캐시가 24시간 이상 지났으면 재계산
        if cls._cache_updated_at:
            cache_age = datetime.now() - cls._cache_updated_at
            if cache_age > timedelta(hours=24):
                logger.info("🔄 계절 지수 캐시가 24시간 경과하여 재계산합니다")
                return cls.calculate_seasonal_index(db)

        return cls._seasonal_index_cache

    @classmethod
    def predict_loss_rate(
        cls,
        db: Session,
        bean_id: int = None,
        months_ahead: int = 1
    ) -> dict:
        """
        손실률 예측

        이동평균 + 계절 지수를 사용한 예측 모델
        - 최근 30개 데이터의 이동평균 계산
        - 다음 달 계절 지수 적용
        - 95% 신뢰구간 (±2σ) 제공

        Args:
            db: SQLAlchemy 세션
            bean_id: 특정 원두 ID (None이면 전체)
            months_ahead: 예측할 달 (1: 다음달, 2: 다다음달, ...)

        Returns:
            {
                'bean_id': int | None,
                'current_avg_loss_rate': float,
                'predicted_loss_rate': float,
                'confidence_interval_lower': float,
                'confidence_interval_upper': float,
                'seasonal_index': float,
                'model_type': str,
                'prediction_month': str,
                'data_points_used': int,
                'last_updated': str
            }

        Raises:
            ValueError: 데이터가 부족한 경우
        """
        # 1. 계절 지수 확인/생성
        seasonal_index = cls.get_seasonal_index(db)

        if not seasonal_index:
            raise ValueError("계절 지수를 계산할 수 없습니다. 충분한 데이터가 필요합니다.")

        # 2. 최근 30개 데이터 조회
        query = db.query(RoastingLog.loss_rate_percent)
        if bean_id:
            query = query.filter(RoastingLog.bean_id == bean_id)

        recent_losses = query.order_by(
            RoastingLog.roasting_date.desc()
        ).limit(30).all()

        if len(recent_losses) < 5:
            raise ValueError(
                f"예측을 위한 데이터가 부족합니다 "
                f"(최소 5개 필요, 현재 {len(recent_losses)}개)"
            )

        # 3. 이동평균 및 표준편차 계산
        loss_values = [r.loss_rate_percent for r in recent_losses]
        moving_avg = statistics.mean(loss_values)
        std_dev = statistics.stdev(loss_values) if len(loss_values) > 1 else 0.0

        # 4. 다음 달 계절 지수
        current_month = datetime.now().month
        next_month = ((current_month + months_ahead - 1) % 12) + 1
        next_month_str = f"{next_month:02d}"

        seasonal_factor = seasonal_index.get(next_month_str, 1.0)

        # 5. 예측값 및 신뢰구간 (95% CI = ±2σ)
        predicted = moving_avg * seasonal_factor
        ci_lower = predicted - 2 * std_dev
        ci_upper = predicted + 2 * std_dev

        # 6. 예측 월 계산
        next_year = datetime.now().year
        if current_month + months_ahead > 12:
            next_year += 1

        result = {
            "bean_id": bean_id,
            "current_avg_loss_rate": round(moving_avg, 2),
            "predicted_loss_rate": round(predicted, 2),
            "confidence_interval_lower": round(ci_lower, 2),
            "confidence_interval_upper": round(ci_upper, 2),
            "seasonal_index": round(seasonal_factor, 3),
            "model_type": "moving_average_with_seasonality",
            "prediction_month": f"{next_year}-{next_month:02d}",
            "data_points_used": len(recent_losses),
            "last_updated": datetime.now().isoformat()
        }

        logger.info(
            f"✓ 손실률 예측 완료: "
            f"bean_id={bean_id}, "
            f"predicted={result['predicted_loss_rate']}%, "
            f"month={result['prediction_month']}"
        )

        return result

    @classmethod
    def get_monthly_forecast(cls, db: Session, months: int = 3) -> list:
        """
        향후 N개월 예측

        Args:
            db: SQLAlchemy 세션
            months: 예측할 개월 수

        Returns:
            예측 결과 리스트 (월별)
        """
        forecasts = []

        for i in range(1, months + 1):
            try:
                forecast = cls.predict_loss_rate(db, months_ahead=i)
                forecasts.append(forecast)
            except ValueError as e:
                logger.warning(f"⚠️ {i}개월 후 예측 실패: {e}")
                break

        logger.info(f"✓ {len(forecasts)}개월 예측 완료")

        return forecasts

    @classmethod
    def clear_cache(cls):
        """캐시 초기화"""
        cls._seasonal_index_cache = None
        cls._cache_updated_at = None
        logger.info("🗑️ 계절 지수 캐시 초기화")
