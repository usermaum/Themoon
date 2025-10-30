"""
RoastingService: 로스팅 기록 관리 서비스

로스팅 기록의 CRUD 작업 및 통계 분석을 담당합니다.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, between
from app.models.database import RoastingLog, LossRateWarning
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class RoastingService:
    """로스팅 기록 관리 서비스"""

    @staticmethod
    def create_roasting_log(
        db: Session,
        raw_weight_kg: float,
        roasted_weight_kg: float,
        roasting_date: date,
        blend_recipe_version_id: int = None,
        notes: str = None,
        operator_id: int = None,
        expected_loss_rate: float = 17.0
    ) -> RoastingLog:
        """로스팅 기록 생성

        Args:
            db: SQLAlchemy 세션
            raw_weight_kg: 생두 투입량 (kg)
            roasted_weight_kg: 로스팅 후 무게 (kg)
            roasting_date: 로스팅 날짜
            blend_recipe_version_id: 블렌드 레시피 버전 ID (선택)
            notes: 로스팅 노트 (선택)
            operator_id: 담당자 ID (선택)
            expected_loss_rate: 예상 손실률 (기본값: 17.0%)

        Returns:
            생성된 RoastingLog 객체
        """

        # 손실률 계산
        loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100
        loss_variance = loss_rate - expected_loss_rate

        roasting_log = RoastingLog(
            raw_weight_kg=round(raw_weight_kg, 2),
            roasted_weight_kg=round(roasted_weight_kg, 2),
            loss_rate_percent=round(loss_rate, 2),
            expected_loss_rate_percent=expected_loss_rate,
            loss_variance_percent=round(loss_variance, 2),
            roasting_date=roasting_date,
            roasting_month=roasting_date.strftime('%Y-%m'),
            blend_recipe_version_id=blend_recipe_version_id,
            notes=notes,
            operator_id=operator_id
        )

        db.add(roasting_log)
        db.commit()
        db.refresh(roasting_log)

        logger.info(f"✓ 로스팅 기록 생성: {roasting_date} ({raw_weight_kg}kg → {roasted_weight_kg}kg, 손실률: {loss_rate:.1f}%)")

        # 이상 탐지
        RoastingService._check_loss_rate_anomaly(db, roasting_log)

        return roasting_log

    @staticmethod
    def get_roasting_logs_by_month(db: Session, month: str) -> list:
        """월별 로스팅 기록 조회

        Args:
            db: SQLAlchemy 세션
            month: 조회 월 (YYYY-MM 형식)

        Returns:
            RoastingLog 객체 리스트
        """
        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_month == month
        ).order_by(RoastingLog.roasting_date).all()

        return logs

    @staticmethod
    def get_monthly_statistics(db: Session, month: str) -> dict:
        """월별 로스팅 통계

        Args:
            db: SQLAlchemy 세션
            month: 조회 월 (YYYY-MM 형식)

        Returns:
            월별 통계 딕셔너리
        """
        logs = RoastingService.get_roasting_logs_by_month(db, month)

        if not logs:
            return {
                "month": month,
                "count": 0,
                "status": "데이터 없음"
            }

        total_raw = sum(log.raw_weight_kg for log in logs)
        total_roasted = sum(log.roasted_weight_kg for log in logs)
        avg_loss_rate = sum(log.loss_rate_percent for log in logs) / len(logs)

        return {
            "month": month,
            "total_logs": len(logs),
            "total_raw_weight_kg": round(total_raw, 2),
            "total_roasted_weight_kg": round(total_roasted, 2),
            "avg_loss_rate_percent": round(avg_loss_rate, 2),
            "total_loss_kg": round(total_raw - total_roasted, 2),
            "variance_from_expected": round(avg_loss_rate - 17.0, 2)
        }

    @staticmethod
    def update_roasting_log(
        db: Session,
        log_id: int,
        **kwargs
    ) -> RoastingLog:
        """로스팅 기록 수정

        Args:
            db: SQLAlchemy 세션
            log_id: 로스팅 기록 ID
            **kwargs: 수정할 필드명과 값

        Returns:
            수정된 RoastingLog 객체
        """
        log = db.query(RoastingLog).filter(RoastingLog.id == log_id).first()

        if not log:
            raise ValueError(f"로스팅 기록을 찾을 수 없습니다: {log_id}")

        for key, value in kwargs.items():
            if hasattr(log, key):
                setattr(log, key, value)

        db.commit()
        db.refresh(log)
        logger.info(f"✓ 로스팅 기록 수정: {log_id}")

        return log

    @staticmethod
    def delete_roasting_log(db: Session, log_id: int) -> bool:
        """로스팅 기록 삭제

        Args:
            db: SQLAlchemy 세션
            log_id: 로스팅 기록 ID

        Returns:
            삭제 성공 여부
        """
        log = db.query(RoastingLog).filter(RoastingLog.id == log_id).first()

        if not log:
            return False

        db.delete(log)
        db.commit()
        logger.info(f"✓ 로스팅 기록 삭제: {log_id}")

        return True

    @staticmethod
    def _check_loss_rate_anomaly(db: Session, roasting_log: RoastingLog):
        """손실률 이상 탐지

        Args:
            db: SQLAlchemy 세션
            roasting_log: 검증할 RoastingLog 객체
        """
        variance = roasting_log.loss_variance_percent

        if abs(variance) > 3.0:  # 3% 이상 편차
            warning_type = 'HIGH' if variance > 3.0 else 'LOW'
            severity = 'CRITICAL' if abs(variance) > 5.0 else 'WARNING'

            # 연속 발생 확인 (지난 3회)
            recent_logs = db.query(RoastingLog).filter(
                RoastingLog.roasting_date < roasting_log.roasting_date
            ).order_by(RoastingLog.roasting_date.desc()).limit(3).all()

            consecutive = 0
            for log in recent_logs:
                if abs(log.loss_variance_percent) > 3.0:
                    consecutive += 1
                else:
                    break

            warning = LossRateWarning(
                roasting_log_id=roasting_log.id,
                warning_type=warning_type,
                severity=severity,
                variance_from_expected=round(variance, 2),
                consecutive_occurrences=consecutive + 1
            )

            db.add(warning)
            db.commit()

            logger.warning(f"⚠️ 손실률 이상 탐지: 기록 {roasting_log.id}, 편차: {variance:+.1f}%, 심각도: {severity}")

    @staticmethod
    def get_all_logs(db: Session, limit: int = 100) -> list:
        """모든 로스팅 기록 조회

        Args:
            db: SQLAlchemy 세션
            limit: 조회 제한 수

        Returns:
            RoastingLog 객체 리스트
        """
        logs = db.query(RoastingLog).order_by(
            RoastingLog.roasting_date.desc()
        ).limit(limit).all()

        return logs

    @staticmethod
    def get_roasting_log_by_id(db: Session, log_id: int) -> RoastingLog:
        """ID로 로스팅 기록 조회

        Args:
            db: SQLAlchemy 세션
            log_id: 로스팅 기록 ID

        Returns:
            RoastingLog 객체 또는 None
        """
        return db.query(RoastingLog).filter(RoastingLog.id == log_id).first()
