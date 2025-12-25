from app.models.roasting_log import RoastingLog
from app.repositories.base_repository import BaseRepository
from app.schemas.roasting import RoastingLogCreate


class RoastingLogRepository(BaseRepository[RoastingLog, RoastingLogCreate, RoastingLogCreate]):
    def __init__(self, db):
        super().__init__(RoastingLog, db)

    def get_latest_batch_no(self) -> str:
        """가장 최근 batch_no 조회"""
        latest = self.db.query(self.model).order_by(self.model.id.desc()).first()
        return latest.batch_no if latest else None

    def get_daily_production_stats(self, start_date, end_date):
        """일별 생산량 집계"""
        from sqlalchemy import func, cast, Date
        
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

    def get_bean_usage_stats(self, start_date, end_date):
        """원두별 생산 비중 집계"""
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

    def get_recent_loss_rates(self, limit=20):
        """최근 로스팅 손실률 조회"""
        from app.models.bean import Bean
        return (
            self.db.query(self.model, Bean.name)
            .join(Bean, self.model.target_bean_id == Bean.id)
            .order_by(self.model.roast_date.desc())
            .limit(limit)
            .all()
        )
