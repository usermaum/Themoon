from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from app.models.roasting_log import RoastingLog
from app.repositories.base_repository import BaseRepository
from app.schemas.roasting import RoastingLogCreate


class RoastingLogRepository(BaseRepository[RoastingLog, RoastingLogCreate, RoastingLogCreate]):
    def __init__(self, db: Session):
        super().__init__(RoastingLog, db)

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[RoastingLog]:
        """다중 조회 with Filters"""
        query = self.db.query(self.model)

        if filters:
            if filters.get("start_date"):
                query = query.filter(self.model.roast_date >= filters["start_date"])
            if filters.get("end_date"):
                query = query.filter(self.model.roast_date <= filters["end_date"])
            if filters.get("bean_id"):
                query = query.filter(self.model.target_bean_id == filters["bean_id"])
            if filters.get("bean_type"):
                from app.models.bean import Bean
                query = query.join(Bean, self.model.target_bean_id == Bean.id).filter(Bean.type == filters["bean_type"])
            if filters.get("bean_name"):
                # Join Bean table to filter by name if needed, but bean_id is preferred
                pass

        return query.order_by(self.model.roast_date.desc()).offset(skip).limit(limit).all()

    def get_latest_batch_no(self) -> Optional[str]:
        """가장 최근 batch_no 조회"""
        latest = self.db.query(self.model).order_by(self.model.id.desc()).first()
        if latest:
            return str(latest.batch_no) if latest.batch_no else None
        return None

    def get_daily_production_stats(
        self,
        start_date: date,
        end_date: date
    ) -> List[Any]:  # SQLAlchemy Row type
        """일별 생산량 집계 - Returns list of (date, total_weight, batch_count)"""
        from sqlalchemy import func

        return (
            self.db.query(
                func.date(self.model.roast_date).label("date"),
                func.sum(self.model.output_weight_total).label("total_weight"),
                func.count(self.model.id).label("batch_count")
            )
            .filter(self.model.roast_date >= start_date, self.model.roast_date <= end_date)
            .group_by(func.date(self.model.roast_date))
            .all()
        )

    def get_bean_usage_stats(
        self,
        start_date: date,
        end_date: date
    ) -> List[Any]:  # SQLAlchemy Row type
        """원두별 생산 비중 집계 - Returns list of (bean_name, total_output)"""
        from sqlalchemy import func
        from app.models.bean import Bean

        return (
            self.db.query(
                Bean.name,
                func.sum(self.model.output_weight_total).label("total_output")
            )
            .join(Bean, self.model.target_bean_id == Bean.id)
            .filter(self.model.roast_date >= start_date, self.model.roast_date <= end_date)
            .group_by(Bean.name)
            .all()
        )

    def get_recent_loss_rates(self, limit: int = 20) -> List[Any]:  # SQLAlchemy Row type
        """최근 로스팅 손실률 조회 - Returns list of (RoastingLog, bean_name)"""
        from app.models.bean import Bean
        return (
            self.db.query(self.model, Bean.name)
            .join(Bean, self.model.target_bean_id == Bean.id)
            .order_by(self.model.roast_date.desc())
            .limit(limit)
            .all()
        )
