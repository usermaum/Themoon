"""
LossRateAnalyzer: 손실률 이상 탐지 및 분석 서비스

로스팅 기록의 손실률 트렌드를 분석하고 이상치를 탐지합니다.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import RoastingLog, LossRateWarning, Bean
from datetime import datetime, timedelta
import statistics
import logging

logger = logging.getLogger(__name__)


class LossRateAnalyzer:
    """손실률 이상 탐지 및 분석 서비스"""

    # 설정
    NORMAL_LOSS_RATE = 17.0         # 정상 손실률 (%)
    WARNING_THRESHOLD = 3.0         # 경고 임계값 (편차 3% 이상)
    CRITICAL_THRESHOLD = 5.0        # 심각 임계값 (편차 5% 이상)
    TREND_WINDOW = 5                # 트렌드 분석 윈도우 (최근 5회)

    @staticmethod
    def analyze_loss_rate_trend(db: Session, days: int = 30) -> dict:
        """
        지정된 기간의 손실률 트렌드 분석

        Args:
            db: SQLAlchemy 세션
            days: 분석 기간 (일 단위)

        Returns:
            {
                'period_days': int,
                'data_count': int,
                'avg_loss_rate': float,
                'median_loss_rate': float,
                'std_deviation': float,
                'min_loss_rate': float,
                'max_loss_rate': float,
                'anomalies_count': int,
                'anomaly_rate_percent': float,
                'status': str ('NORMAL', 'ATTENTION', 'CRITICAL')
            }
        """

        # 조회 기간 계산
        start_date = datetime.now().date() - timedelta(days=days)

        # 로스팅 로그 조회
        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_date >= start_date
        ).order_by(RoastingLog.roasting_date).all()

        if not logs:
            logger.warning(f"⚠️ {days}일 기간의 로스팅 데이터가 없습니다")
            return {
                "period_days": days,
                "data_count": 0,
                "status": "NO_DATA"
            }

        # 손실률 및 편차 추출
        loss_rates = [log.loss_rate_percent for log in logs]
        variances = [log.loss_variance_percent for log in logs]

        # 통계 계산
        avg_loss = statistics.mean(loss_rates)
        median_loss = statistics.median(loss_rates)
        stdev_loss = statistics.stdev(loss_rates) if len(loss_rates) > 1 else 0

        # 이상치 개수 계산
        anomalies = sum(1 for v in variances if abs(v) > LossRateAnalyzer.WARNING_THRESHOLD)

        # 상태 판단
        if anomalies < 2:
            status = "NORMAL"
        elif anomalies < 5:
            status = "ATTENTION"
        else:
            status = "CRITICAL"

        result = {
            "period_days": days,
            "data_count": len(logs),
            "avg_loss_rate": round(avg_loss, 2),
            "median_loss_rate": round(median_loss, 2),
            "std_deviation": round(stdev_loss, 2),
            "min_loss_rate": round(min(loss_rates), 2),
            "max_loss_rate": round(max(loss_rates), 2),
            "anomalies_count": anomalies,
            "anomaly_rate_percent": round((anomalies / len(logs) * 100), 1),
            "status": status
        }

        logger.info(
            f"✓ 손실률 트렌드 분석 완료: "
            f"평균={result['avg_loss_rate']}%, "
            f"이상치={anomalies}건, "
            f"상태={status}"
        )

        return result

    @staticmethod
    def get_recent_warnings(db: Session, limit: int = 10) -> list:
        """
        최근 미해결 경고 조회

        Args:
            db: SQLAlchemy 세션
            limit: 조회 제한 건수

        Returns:
            경고 정보 리스트
        """

        warnings = db.query(LossRateWarning).filter(
            LossRateWarning.is_resolved == False
        ).order_by(LossRateWarning.created_at.desc()).limit(limit).all()

        result = []
        for w in warnings:
            result.append({
                'id': w.id,
                'roasting_date': w.roasting_log.roasting_date,
                'severity': w.severity,
                'variance': w.variance_from_expected,
                'consecutive': w.consecutive_occurrences,
                'created_at': w.created_at
            })

        logger.info(f"✓ 미해결 경고 조회: {len(result)}건")

        return result

    @staticmethod
    def resolve_warning(
        db: Session,
        warning_id: int,
        notes: str = None
    ) -> LossRateWarning:
        """
        경고 해결 처리

        Args:
            db: SQLAlchemy 세션
            warning_id: 경고 ID
            notes: 해결 노트

        Returns:
            업데이트된 LossRateWarning 객체

        Raises:
            ValueError: 경고를 찾을 수 없는 경우
        """

        warning = db.query(LossRateWarning).filter(
            LossRateWarning.id == warning_id
        ).first()

        if not warning:
            raise ValueError(f"경고를 찾을 수 없습니다: {warning_id}")

        warning.is_resolved = True
        warning.resolution_notes = notes
        warning.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(warning)

        logger.info(f"✓ 경고 해결: warning_id={warning_id}")

        return warning

    @staticmethod
    def get_loss_rate_by_bean(db: Session, days: int = 30) -> list:
        """
        최근 로스팅의 원두별 손실률 분석

        Args:
            db: SQLAlchemy 세션
            days: 분석 기간 (일 단위)

        Returns:
            원두별 손실률 통계 리스트
            [
                {
                    'bean_id': int,
                    'bean_name': str,
                    'roast_count': int,
                    'avg_loss_rate': float,
                    'std_deviation': float,
                    'min_loss': float,
                    'max_loss': float,
                    'variance_from_global': float,
                    'status': str ('NORMAL' | 'ATTENTION' | 'CRITICAL')
                },
                ...
            ]
        """
        # 조회 기간 계산
        start_date = datetime.now().date() - timedelta(days=days)

        # 전체 로스팅 로그 조회 (원두별 통계를 Python에서 계산)
        logs = db.query(
            RoastingLog.bean_id,
            RoastingLog.loss_rate_percent
        ).filter(
            RoastingLog.roasting_date >= start_date
        ).all()

        if not logs:
            logger.warning(f"⚠️ {days}일 기간의 로스팅 데이터가 없습니다")
            return []

        # 전체 평균 손실률 계산
        all_loss_rates = [log.loss_rate_percent for log in logs]
        global_avg = statistics.mean(all_loss_rates)

        # 원두별 그룹화
        bean_data = {}
        for log in logs:
            bean_id = log.bean_id
            if bean_id not in bean_data:
                bean_data[bean_id] = []
            bean_data[bean_id].append(log.loss_rate_percent)

        # 원두별 통계 계산
        bean_stats = []
        for bean_id, loss_rates in bean_data.items():
            # Bean 정보 조회
            bean = db.query(Bean).filter(Bean.id == bean_id).first()
            if not bean:
                continue

            # 통계 계산
            avg_loss = statistics.mean(loss_rates)
            std_loss = statistics.stdev(loss_rates) if len(loss_rates) > 1 else 0.0
            min_loss = min(loss_rates)
            max_loss = max(loss_rates)
            variance = avg_loss - global_avg

            # 상태 판단
            if abs(variance) > 3:
                status = "CRITICAL"
            elif abs(variance) > 2:
                status = "ATTENTION"
            else:
                status = "NORMAL"

            bean_stats.append({
                "bean_id": bean.id,
                "bean_name": bean.name,
                "roast_count": len(loss_rates),
                "avg_loss_rate": round(avg_loss, 2),
                "std_deviation": round(std_loss, 2),
                "min_loss": round(min_loss, 2),
                "max_loss": round(max_loss, 2),
                "variance_from_global": round(variance, 2),
                "status": status
            })

        logger.info(f"✓ 원두별 손실률 분석 완료: {len(bean_stats)}종 원두")

        # 손실률 높은 순으로 정렬
        return sorted(bean_stats, key=lambda x: x['avg_loss_rate'], reverse=True)

    @staticmethod
    def get_monthly_summary(db: Session, month: str) -> dict:
        """
        월별 손실률 요약

        Args:
            db: SQLAlchemy 세션
            month: 조회 월 (YYYY-MM 형식)

        Returns:
            월별 통계 정보
        """

        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_month == month
        ).all()

        if not logs:
            logger.warning(f"⚠️ {month}의 로스팅 데이터가 없습니다")
            return {
                "month": month,
                "data_count": 0,
                "status": "NO_DATA"
            }

        loss_rates = [log.loss_rate_percent for log in logs]
        variances = [log.loss_variance_percent for log in logs]

        avg_loss = statistics.mean(loss_rates)
        anomalies = sum(1 for v in variances if abs(v) > LossRateAnalyzer.WARNING_THRESHOLD)

        result = {
            "month": month,
            "data_count": len(logs),
            "avg_loss_rate": round(avg_loss, 2),
            "std_deviation": round(statistics.stdev(loss_rates), 2) if len(loss_rates) > 1 else 0,
            "anomalies_count": anomalies,
            "min_loss_rate": round(min(loss_rates), 2),
            "max_loss_rate": round(max(loss_rates), 2),
        }

        logger.info(f"✓ 월별 요약: {month} - 이상치 {anomalies}건")

        return result

    @staticmethod
    def detect_continuous_anomalies(db: Session, threshold: int = 3) -> list:
        """
        연속 이상치 탐지

        Args:
            db: SQLAlchemy 세션
            threshold: 연속 이상 발생 임계값 (기본: 3회 연속)

        Returns:
            연속 이상이 발생한 경고 리스트
        """

        warnings = db.query(LossRateWarning).filter(
            LossRateWarning.consecutive_occurrences >= threshold
        ).order_by(LossRateWarning.created_at.desc()).all()

        result = []
        for w in warnings:
            result.append({
                'id': w.id,
                'roasting_date': w.roasting_log.roasting_date,
                'severity': w.severity,
                'consecutive_count': w.consecutive_occurrences,
                'variance': w.variance_from_expected
            })

        logger.info(f"✓ 연속 이상치 탐지: {len(result)}건 (임계값: {threshold}회)")

        return result

    @staticmethod
    def get_severity_distribution(db: Session, days: int = 30) -> dict:
        """
        심각도별 경고 분포

        Args:
            db: SQLAlchemy 세션
            days: 분석 기간 (일 단위)

        Returns:
            심각도별 경고 개수
        """

        start_date = datetime.utcnow() - timedelta(days=days)

        warnings = db.query(LossRateWarning).filter(
            LossRateWarning.created_at >= start_date
        ).all()

        distribution = {
            'CRITICAL': 0,
            'WARNING': 0,
            'INFO': 0
        }

        for w in warnings:
            if w.severity in distribution:
                distribution[w.severity] += 1

        result = {
            "period_days": days,
            "total_warnings": len(warnings),
            "severity_distribution": distribution,
            "critical_ratio": round(
                distribution['CRITICAL'] / len(warnings) * 100, 1
            ) if warnings else 0
        }

        logger.info(f"✓ 심각도별 분포: Critical={distribution['CRITICAL']}, Warning={distribution['WARNING']}")

        return result
