"""
고급 분석 서비스
트렌드, 예측, ROI 분석
"""

from datetime import datetime, timedelta
from models.database import SessionLocal, Transaction, Inventory, Bean, Blend
from services.blend_service import BlendService
import numpy as np


class AnalyticsService:
    """고급 분석 서비스"""

    def __init__(self, db):
        """초기화"""
        self.db = db
        self.blend_service = BlendService(db)

    def get_monthly_trend(self, months: int = 12):
        """월별 거래 추이 분석"""
        trend_data = []

        for i in range(months, -1, -1):
            target_date = datetime.now() - timedelta(days=30 * i)
            month_start = datetime(target_date.year, target_date.month, 1)

            if target_date.month == 12:
                month_end = datetime(target_date.year + 1, 1, 1)
            else:
                month_end = datetime(target_date.year, target_date.month + 1, 1)

            # 해당 월의 거래
            transactions = self.db.query(Transaction).filter(
                Transaction.created_at >= month_start,
                Transaction.created_at < month_end
            ).all()

            # 통계 계산
            inflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "입고")
            outflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "사용")
            amount = sum(t.total_amount for t in transactions)

            trend_data.append({
                "period": month_start.strftime("%Y-%m"),
                "month_name": month_start.strftime("%m월"),
                "inflow": inflow,
                "outflow": outflow,
                "net_change": inflow - outflow,
                "amount": amount,
                "transaction_count": len(transactions)
            })

        return trend_data

    def get_inventory_projection(self, days: int = 30):
        """재고 예측"""
        inventory = self.db.query(Inventory).all()

        projections = []

        for inv in inventory:
            bean = self.db.query(Bean).filter(Bean.id == inv.bean_id).first()

            if bean:
                # 지난 30일 사용량
                past_transactions = self.db.query(Transaction).filter(
                    Transaction.bean_id == bean.id,
                    Transaction.transaction_type == "사용",
                    Transaction.created_at >= datetime.now() - timedelta(days=30)
                ).all()

                past_usage = sum(t.quantity_kg for t in past_transactions)
                daily_usage = past_usage / 30 if past_usage > 0 else 0

                # 예측 재고
                projected_quantity = inv.quantity_kg - (daily_usage * days)

                # 소진 날짜 예측
                if daily_usage > 0:
                    days_until_depletion = inv.quantity_kg / daily_usage
                else:
                    days_until_depletion = float('inf')

                projections.append({
                    "bean_name": bean.name,
                    "current_quantity": inv.quantity_kg,
                    "daily_usage": daily_usage,
                    "projected_quantity": max(0, projected_quantity),
                    "days_until_depletion": days_until_depletion if days_until_depletion != float('inf') else 999,
                    "is_critical": projected_quantity <= inv.min_quantity_kg
                })

        return projections

    def get_roi_analysis(self):
        """ROI 분석"""
        blends = self.blend_service.get_active_blends()

        roi_data = []

        for blend in blends:
            cost_info = self.blend_service.calculate_blend_cost(blend.id)

            if cost_info:
                total_portions = blend.total_portion
                total_cost = cost_info['total_cost']
                total_revenue = cost_info['suggested_price'] * total_portions

                roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0

                roi_data.append({
                    "blend_name": blend.name,
                    "blend_type": blend.blend_type,
                    "total_cost": total_cost,
                    "total_revenue": total_revenue,
                    "total_profit": total_revenue - total_cost,
                    "roi_percent": roi,
                    "portioncount": total_portions
                })

        return {
            "roi_data": roi_data,
            "average_roi": np.mean([r['roi_percent'] for r in roi_data]) if roi_data else 0,
            "best_roi": max(roi_data, key=lambda x: x['roi_percent']) if roi_data else None,
            "worst_roi": min(roi_data, key=lambda x: x['roi_percent']) if roi_data else None
        }

    def get_performance_metrics(self):
        """성능 지표"""
        blends = self.blend_service.get_active_blends()
        beans = self.db.query(Bean).all()

        # 월별 사용량
        past_30_transactions = self.db.query(Transaction).filter(
            Transaction.transaction_type == "사용",
            Transaction.created_at >= datetime.now() - timedelta(days=30)
        ).all()

        # 월별 수익
        past_30_revenue = sum(t.total_amount for t in past_30_transactions)
        past_30_quantity = sum(t.quantity_kg for t in past_30_transactions)

        # 효율성
        total_transactions = self.db.query(Transaction).count()
        active_beans = len([b for b in beans if b.status == "active"])
        active_blends = len([b for b in blends if b.status == "active"])

        metrics = {
            "total_transactions": total_transactions,
            "active_beans": active_beans,
            "active_blends": active_blends,
            "monthly_usage": past_30_quantity,
            "monthly_revenue": past_30_revenue,
            "average_transaction_amount": past_30_revenue / len(past_30_transactions) if past_30_transactions else 0,
            "daily_usage": past_30_quantity / 30 if past_30_quantity > 0 else 0
        }

        return metrics

    def get_usage_forecast(self, days: int = 60):
        """사용량 예측 (향후 N일)"""
        # 지난 90일 사용량
        past_90_transactions = self.db.query(Transaction).filter(
            Transaction.transaction_type == "사용",
            Transaction.created_at >= datetime.now() - timedelta(days=90)
        ).all()

        daily_usages = {}

        # 일별 사용량 계산
        for trans in past_90_transactions:
            date_key = trans.created_at.strftime("%Y-%m-%d")
            if date_key not in daily_usages:
                daily_usages[date_key] = 0
            daily_usages[date_key] += trans.quantity_kg

        # 평균 사용량
        if daily_usages:
            avg_daily_usage = sum(daily_usages.values()) / len(daily_usages)
        else:
            avg_daily_usage = 0

        # 향후 예측
        forecast = []
        for i in range(days):
            future_date = datetime.now() + timedelta(days=i)

            forecast.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "projected_usage": avg_daily_usage,
                "cumulative_usage": avg_daily_usage * (i + 1)
            })

        return {
            "avg_daily_usage": avg_daily_usage,
            "forecast": forecast
        }

    def get_bean_efficiency(self):
        """원두별 효율성 분석"""
        beans = self.db.query(Bean).all()

        efficiency_data = []

        for bean in beans:
            # 지난 30일 사용량
            transactions = self.db.query(Transaction).filter(
                Transaction.bean_id == bean.id,
                Transaction.transaction_type == "사용",
                Transaction.created_at >= datetime.now() - timedelta(days=30)
            ).all()

            usage_count = len(transactions)
            usage_quantity = sum(t.quantity_kg for t in transactions)
            usage_cost = sum(t.total_amount for t in transactions)

            efficiency_data.append({
                "bean_name": bean.name,
                "price_per_kg": bean.price_per_kg,
                "usage_count": usage_count,
                "usage_quantity": usage_quantity,
                "usage_cost": usage_cost,
                "avg_use_per_transaction": usage_quantity / usage_count if usage_count > 0 else 0
            })

        return {
            "efficiency": sorted(efficiency_data,
                               key=lambda x: x['usage_count'],
                               reverse=True),
            "most_used": max(efficiency_data, key=lambda x: x['usage_count']) if efficiency_data else None,
            "least_used": min(efficiency_data, key=lambda x: x['usage_count']) if efficiency_data else None
        }

    def get_comparison_analysis(self):
        """블렌드 간 비교 분석"""
        blends = self.blend_service.get_active_blends()

        comparison = []

        for blend in blends:
            cost_info = self.blend_service.calculate_blend_cost(blend.id)

            if cost_info:
                cost_per_portion = cost_info['cost_per_portion']
                selling_price = cost_info['suggested_price']
                profit_per_portion = cost_info['profit_margin']

                # 수익률
                profit_rate = (profit_per_portion / cost_per_portion * 100) if cost_per_portion > 0 else 0

                # 비용 효율성 (비용 대비 판매가)
                price_to_cost_ratio = selling_price / cost_per_portion if cost_per_portion > 0 else 0

                comparison.append({
                    "blend_name": blend.name,
                    "blend_type": blend.blend_type,
                    "portions": blend.total_portion,
                    "cost_per_portion": cost_per_portion,
                    "selling_price": selling_price,
                    "profit_per_portion": profit_per_portion,
                    "profit_rate": profit_rate,
                    "price_to_cost_ratio": price_to_cost_ratio
                })

        return {
            "comparison": sorted(comparison, key=lambda x: x['profit_rate'], reverse=True),
            "highest_profit": max(comparison, key=lambda x: x['profit_per_portion']) if comparison else None,
            "highest_ratio": max(comparison, key=lambda x: x['price_to_cost_ratio']) if comparison else None
        }
