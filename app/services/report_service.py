"""
보고서 생성 서비스
PDF, Excel 형식의 다양한 보고서 생성
Phase 5: 월별 리포트 및 수익성 분석 추가
"""

from datetime import datetime, timedelta, date
from models.database import SessionLocal, Bean, Blend, Inventory, Transaction, RoastingLog, CostSetting
from services.bean_service import BeanService
from services.blend_service import BlendService
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd
from io import BytesIO, StringIO
from typing import Dict, List, Optional
from app.utils.export_utils import create_monthly_report_excel


class ReportService:
    """보고서 생성 서비스"""

    def __init__(self, db):
        """초기화"""
        self.db = db
        self.bean_service = BeanService(db)
        self.blend_service = BlendService(db)

    def get_monthly_summary(self, year: int, month: int):
        """월별 요약 데이터 조회"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # 해당 월의 거래 데이터
        transactions = self.db.query(Transaction).filter(
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date
        ).all()

        # 통계 계산
        total_inflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "입고")
        total_outflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "사용")
        total_amount = sum(t.total_amount for t in transactions)

        return {
            "year": year,
            "month": month,
            "period": f"{year}년 {month}월",
            "total_inflow": total_inflow,
            "total_outflow": total_outflow,
            "net_change": total_inflow - total_outflow,
            "total_amount": total_amount,
            "transaction_count": len(transactions),
            "transactions": transactions
        }

    def get_cost_analysis(self, start_date: datetime = None, end_date: datetime = None):
        """비용 분석"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        blends = self.blend_service.get_active_blends()

        cost_analysis = []
        total_cost = 0

        for blend in blends:
            cost_info = self.blend_service.calculate_blend_cost(blend.id)

            if cost_info:
                total_cost += cost_info['total_cost']

                cost_analysis.append({
                    "blend_name": blend.name,
                    "blend_type": blend.blend_type,
                    "total_portions": blend.total_portion,
                    "bean_cost": cost_info.get('bean_cost_total', 0),
                    "roasting_cost": cost_info.get('roasting_cost', 0),
                    "labor_cost": cost_info.get('labor_cost', 0),
                    "misc_cost": cost_info.get('misc_cost', 0),
                    "total_cost": cost_info['total_cost'],
                    "cost_per_portion": cost_info['cost_per_portion'],
                    "suggested_price": cost_info['suggested_price'],
                    "profit_margin": cost_info['profit_margin']
                })

        return {
            "start_date": start_date,
            "end_date": end_date,
            "period_days": (end_date - start_date).days,
            "cost_analysis": cost_analysis,
            "total_cost": total_cost,
            "average_cost": total_cost / len(cost_analysis) if cost_analysis else 0
        }

    def get_bean_usage_analysis(self, start_date: datetime = None, end_date: datetime = None):
        """원두 사용량 분석"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        beans = self.bean_service.get_active_beans()

        usage_analysis = []
        total_usage = 0

        for bean in beans:
            # 해당 기간의 출고 기록
            outflow = self.db.query(Transaction).filter(
                Transaction.bean_id == bean.id,
                Transaction.transaction_type == "사용",
                Transaction.created_at >= start_date,
                Transaction.created_at < end_date
            ).all()

            # 해당 기간의 입고 기록
            inflow = self.db.query(Transaction).filter(
                Transaction.bean_id == bean.id,
                Transaction.transaction_type == "입고",
                Transaction.created_at >= start_date,
                Transaction.created_at < end_date
            ).all()

            total_outflow = sum(t.quantity_kg for t in outflow)
            total_inflow = sum(t.quantity_kg for t in inflow)
            total_usage += total_outflow

            if total_outflow > 0 or total_inflow > 0:
                usage_analysis.append({
                    "bean_name": bean.name,
                    "country": bean.country_code or "-",
                    "roast_level": bean.roast_level,
                    "price_per_kg": bean.price_per_kg,
                    "inflow_kg": total_inflow,
                    "outflow_kg": total_outflow,
                    "net_kg": total_inflow - total_outflow,
                    "outflow_cost": total_outflow * bean.price_per_kg
                })

        return {
            "start_date": start_date,
            "end_date": end_date,
            "usage_analysis": usage_analysis,
            "total_usage": total_usage
        }

    def get_blend_performance(self):
        """블렌드 성과 분석"""
        blends = self.blend_service.get_active_blends()

        performance = []

        for blend in blends:
            cost_info = self.blend_service.calculate_blend_cost(blend.id)

            if cost_info:
                performance.append({
                    "blend_name": blend.name,
                    "blend_type": blend.blend_type,
                    "total_portions": blend.total_portion,
                    "cost_per_portion": cost_info['cost_per_portion'],
                    "suggested_price": cost_info['suggested_price'],
                    "profit_per_portion": cost_info['profit_margin'],
                    "profit_rate": (cost_info['profit_margin'] / cost_info['cost_per_portion'] * 100)
                                  if cost_info['cost_per_portion'] > 0 else 0
                })

        return {
            "performance": sorted(performance,
                                 key=lambda x: x['profit_rate'],
                                 reverse=True),
            "best_blend": performance[0] if performance else None,
            "worst_blend": performance[-1] if performance else None
        }

    def export_to_excel(self, report_type: str = "summary", data: dict = None):
        """Excel 형식으로 내보내기"""
        output = BytesIO()
        sheets_created = 0

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if report_type == "summary" or report_type == "all":
                self._create_summary_sheet(writer)
                sheets_created += 1

            if report_type == "cost" or report_type == "all":
                cost_data = self.get_cost_analysis()
                if cost_data.get('cost_analysis'):
                    self._create_cost_sheet(writer, cost_data)
                    sheets_created += 1

            if report_type == "bean_usage" or report_type == "all":
                usage_data = self.get_bean_usage_analysis()
                if usage_data.get('usage_analysis'):
                    self._create_bean_usage_sheet(writer, usage_data)
                    sheets_created += 1

            if report_type == "blend" or report_type == "all":
                performance = self.get_blend_performance()
                if performance.get('performance'):
                    self._create_blend_sheet(writer, performance)
                    sheets_created += 1

            # 시트가 하나도 없으면 빈 요약 시트 생성
            if sheets_created == 0:
                empty_data = {"정보": ["데이터 없음"], "상태": ["생성할 데이터가 없습니다"]}
                df = pd.DataFrame(empty_data)
                df.to_excel(writer, sheet_name="정보", index=False)

        output.seek(0)
        return output

    def _create_summary_sheet(self, writer):
        """요약 시트 생성"""
        try:
            bean_summary = self.bean_service.get_beans_summary()
            blend_summary = self.blend_service.get_blends_summary()

            active_beans = self.bean_service.get_active_beans()
            beans_with_price = [b for b in active_beans if b.price_per_kg > 0]

            avg_price = (sum(b.price_per_kg for b in beans_with_price) / len(beans_with_price)) if beans_with_price else 0

            data = {
                "항목": [
                    "총 원두 종류",
                    "총 블렌드 개수",
                    "총 포션",
                    "총 원두 가격합",
                    "평균 원두 가격"
                ],
                "값": [
                    bean_summary['total_beans'],
                    blend_summary['total_blends'],
                    sum(b.total_portion for b in self.blend_service.get_active_blends()),
                    sum(b.price_per_kg for b in beans_with_price),
                    avg_price
                ]
            }

            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name="요약", index=False)
        except Exception as e:
            # 오류 발생 시 빈 시트 생성
            empty_data = {"오류": [str(e)]}
            df = pd.DataFrame(empty_data)
            df.to_excel(writer, sheet_name="요약", index=False)

    def _create_cost_sheet(self, writer, cost_data):
        """비용 분석 시트 생성"""
        try:
            cost_list = []

            for cost in cost_data['cost_analysis']:
                cost_list.append({
                    "블렌드명": cost['blend_name'],
                    "타입": cost['blend_type'],
                    "포션": cost['total_portions'],
                    "원두비용": f"₩{cost['bean_cost']:,.0f}",
                    "로스팅비용": f"₩{cost['roasting_cost']:,.0f}",
                    "인건비": f"₩{cost['labor_cost']:,.0f}",
                    "기타비용": f"₩{cost['misc_cost']:,.0f}",
                    "총원가": f"₩{cost['total_cost']:,.0f}",
                    "포션당원가": f"₩{cost['cost_per_portion']:,.0f}",
                    "제안판매가": f"₩{cost['suggested_price']:,.0f}",
                    "예상이익": f"₩{cost['profit_margin']:,.0f}"
                })

            if cost_list:
                df = pd.DataFrame(cost_list)
                df.to_excel(writer, sheet_name="비용분석", index=False)
        except Exception as e:
            empty_data = {"오류": [str(e)]}
            df = pd.DataFrame(empty_data)
            df.to_excel(writer, sheet_name="비용분석", index=False)

    def _create_bean_usage_sheet(self, writer, usage_data):
        """원두 사용량 시트 생성"""
        try:
            usage_list = []

            for usage in usage_data['usage_analysis']:
                usage_list.append({
                    "원두명": usage['bean_name'],
                    "국가": usage['country'],
                    "로스팅": usage['roast_level'],
                    "가격/kg": f"₩{usage['price_per_kg']:,.0f}",
                    "입고량": f"{usage['inflow_kg']:.2f}kg",
                    "출고량": f"{usage['outflow_kg']:.2f}kg",
                    "순변화": f"{usage['net_kg']:.2f}kg",
                    "사용비용": f"₩{usage['outflow_cost']:,.0f}"
                })

            if usage_list:
                df = pd.DataFrame(usage_list)
                df.to_excel(writer, sheet_name="원두사용", index=False)
        except Exception as e:
            empty_data = {"오류": [str(e)]}
            df = pd.DataFrame(empty_data)
            df.to_excel(writer, sheet_name="원두사용", index=False)

    def _create_blend_sheet(self, writer, performance):
        """블렌드 성과 시트 생성"""
        try:
            blend_list = []

            for blend in performance['performance']:
                blend_list.append({
                    "블렌드명": blend['blend_name'],
                    "타입": blend['blend_type'],
                    "포션": blend['total_portions'],
                    "포션당원가": f"₩{blend['cost_per_portion']:,.0f}",
                    "제안판매가": f"₩{blend['suggested_price']:,.0f}",
                    "포션당이익": f"₩{blend['profit_per_portion']:,.0f}",
                    "수익률": f"{blend['profit_rate']:.1f}%"
                })

            if blend_list:
                df = pd.DataFrame(blend_list)
                df.to_excel(writer, sheet_name="블렌드성과", index=False)
        except Exception as e:
            empty_data = {"오류": [str(e)]}
            df = pd.DataFrame(empty_data)
            df.to_excel(writer, sheet_name="블렌드성과", index=False)

    def export_to_csv(self, report_type: str = "summary"):
        """CSV 형식으로 내보내기"""
        output = StringIO()

        if report_type == "cost":
            cost_data = self.get_cost_analysis()
            cost_list = []

            for cost in cost_data['cost_analysis']:
                cost_list.append({
                    "블렌드명": cost['blend_name'],
                    "타입": cost['blend_type'],
                    "포션당원가": cost['cost_per_portion'],
                    "제안판매가": cost['suggested_price'],
                    "예상이익": cost['profit_margin']
                })

            df = pd.DataFrame(cost_list)

        elif report_type == "bean_usage":
            usage_data = self.get_bean_usage_analysis()
            df = pd.DataFrame(usage_data['usage_analysis'])

        elif report_type == "blend":
            performance = self.get_blend_performance()
            df = pd.DataFrame(performance['performance'])

        else:  # summary
            bean_summary = self.bean_service.get_beans_summary()
            blend_summary = self.blend_service.get_blends_summary()

            data = {
                "항목": [
                    "총 원두 종류",
                    "총 블렌드 개수",
                    "총 포션"
                ],
                "값": [
                    bean_summary['total_beans'],
                    blend_summary['total_blends'],
                    sum(b.total_portion for b in self.blend_service.get_active_blends())
                ]
            }
            df = pd.DataFrame(data)

        csv_string = df.to_csv(index=False, encoding="utf-8-sig")
        return csv_string

    # ==================== Phase 5: 월별 리포트 및 수익성 분석 ====================

    def get_monthly_transactions_report(self, year: int, month: int) -> Dict:
        """
        월별 거래 리포트 데이터 생성 (Phase 5)

        Args:
            year: 년도
            month: 월 (1-12)

        Returns:
            {
                'summary': Dict,  # 요약 통계
                'daily_trend': pd.DataFrame,  # 일별 추이
                'transaction_type': pd.DataFrame  # 거래 유형별
            }
        """
        # 월의 첫날과 마지막 날
        if month == 12:
            start_date = date(year, month, 1)
            end_date = date(year + 1, 1, 1)
        else:
            start_date = date(year, month, 1)
            end_date = date(year, month + 1, 1)

        # 거래 내역 조회
        transactions = self.db.query(Transaction).filter(
            Transaction.created_at >= datetime.combine(start_date, datetime.min.time()),
            Transaction.created_at < datetime.combine(end_date, datetime.min.time())
        ).all()

        # 1. 요약 통계
        total_in = sum(
            abs(t.quantity_kg) for t in transactions
            if t.transaction_type in ['PURCHASE', 'PRODUCTION'] or
               (t.transaction_type == 'ADJUSTMENT' and t.quantity_kg > 0)
        )

        total_out = sum(
            abs(t.quantity_kg) for t in transactions
            if t.transaction_type in ['SALES', 'GIFT', 'WASTE'] or
               (t.transaction_type == 'ADJUSTMENT' and t.quantity_kg < 0)
        )

        roasting_count = len([t for t in transactions if t.transaction_type == 'ROASTING'])

        summary = {
            '총 입고량 (kg)': round(total_in, 2),
            '총 출고량 (kg)': round(total_out, 2),
            '로스팅 횟수': roasting_count,
            '재고 증감 (kg)': round(total_in - total_out, 2)
        }

        # 2. 일별 추이
        daily_data = [
            {
                '날짜': t.created_at.date(),
                '거래유형': t.transaction_type,
                '수량(kg)': t.quantity_kg
            }
            for t in transactions
        ]

        if daily_data:
            daily_df = pd.DataFrame(daily_data)
            daily_trend = daily_df.groupby(['날짜', '거래유형'])['수량(kg)'].sum().reset_index()
            daily_trend = daily_trend.pivot(index='날짜', columns='거래유형', values='수량(kg)').fillna(0).reset_index()
        else:
            daily_trend = pd.DataFrame(columns=['날짜'])

        # 3. 거래 유형별 분류
        type_data = {}
        for t in transactions:
            if t.transaction_type not in type_data:
                type_data[t.transaction_type] = {'count': 0, 'quantity': 0.0}
            type_data[t.transaction_type]['count'] += 1
            type_data[t.transaction_type]['quantity'] += abs(t.quantity_kg)

        total_quantity = sum(d['quantity'] for d in type_data.values())

        transaction_type_list = [
            {
                '거래 유형': t_type,
                '횟수': data['count'],
                '수량(kg)': round(data['quantity'], 2),
                '비율(%)': round(data['quantity'] / total_quantity * 100, 1) if total_quantity > 0 else 0.0
            }
            for t_type, data in sorted(type_data.items())
        ]

        transaction_type_df = pd.DataFrame(transaction_type_list) if transaction_type_list else pd.DataFrame()

        return {
            'summary': summary,
            'daily_trend': daily_trend,
            'transaction_type': transaction_type_df
        }

    def get_profitability_by_bean(
        self,
        start_date: date,
        end_date: date,
        sort_by: str = 'profit_rate'
    ) -> pd.DataFrame:
        """
        원두별 수익성 분석 (Phase 5)

        Args:
            start_date: 시작일
            end_date: 종료일
            sort_by: 정렬 기준 ('profit_rate', 'total_cost', 'roasting_count')

        Returns:
            DataFrame
        """
        # 로스팅 기록 조회
        roasting_logs = self.db.query(RoastingLog).filter(
            RoastingLog.roasting_date >= start_date,
            RoastingLog.roasting_date <= end_date,
            RoastingLog.bean_id.isnot(None)
        ).all()

        if not roasting_logs:
            return pd.DataFrame()

        # 로스팅 비용 설정
        roasting_cost_setting = self.db.query(CostSetting).filter(
            CostSetting.parameter_name == 'roasting_cost_per_kg'
        ).first()
        roasting_cost_per_kg = roasting_cost_setting.value if roasting_cost_setting else 500.0

        # 원두별 집계
        bean_stats = {}
        for log in roasting_logs:
            bean = log.bean
            if not bean:
                continue

            if bean.name not in bean_stats:
                bean_stats[bean.name] = {
                    'purchase_kg': 0.0,
                    'purchase_cost': 0.0,
                    'roasting_cost': 0.0,
                    'output_kg': 0.0,
                    'roasting_count': 0
                }

            bean_stats[bean.name]['purchase_kg'] += log.raw_weight_kg
            bean_stats[bean.name]['purchase_cost'] += log.raw_weight_kg * bean.price_per_kg
            bean_stats[bean.name]['roasting_cost'] += log.roasted_weight_kg * roasting_cost_per_kg
            bean_stats[bean.name]['output_kg'] += log.roasted_weight_kg
            bean_stats[bean.name]['roasting_count'] += 1

        # DataFrame 생성
        result_list = []
        for bean_name, stats in bean_stats.items():
            total_cost = stats['purchase_cost'] + stats['roasting_cost']

            # 수익률 = (1 - 손실률) * 100 - 100 (간이 계산)
            if stats['purchase_kg'] > 0:
                loss_rate = (1 - stats['output_kg'] / stats['purchase_kg']) * 100
                profit_rate = -loss_rate  # 손실이 적을수록 수익률 높음
            else:
                profit_rate = 0.0

            result_list.append({
                '원두명': bean_name,
                '매입(kg)': round(stats['purchase_kg'], 2),
                '매입비용(원)': int(stats['purchase_cost']),
                '로스팅비용(원)': int(stats['roasting_cost']),
                '산출(kg)': round(stats['output_kg'], 2),
                '총비용(원)': int(total_cost),
                '수익률(%)': round(profit_rate, 2),
                '로스팅횟수': stats['roasting_count']
            })

        df = pd.DataFrame(result_list)

        # 정렬
        if sort_by == 'profit_rate':
            df = df.sort_values('수익률(%)', ascending=False)
        elif sort_by == 'total_cost':
            df = df.sort_values('총비용(원)', ascending=False)
        elif sort_by == 'roasting_count':
            df = df.sort_values('로스팅횟수', ascending=False)

        return df.reset_index(drop=True)

    def get_roasting_logs_dataframe(
        self,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """로스팅 기록 DataFrame 조회 (다운로드용)"""
        logs = self.db.query(RoastingLog).filter(
            RoastingLog.roasting_date >= start_date,
            RoastingLog.roasting_date <= end_date
        ).order_by(RoastingLog.roasting_date.desc()).all()

        return pd.DataFrame([
            {
                '날짜': log.roasting_date,
                '원두': log.bean.name if log.bean else "-",
                '생두(kg)': log.raw_weight_kg,
                '원두(kg)': log.roasted_weight_kg,
                '손실률(%)': log.loss_rate_percent,
                '비고': log.notes or ""
            }
            for log in logs
        ])

    def get_inventory_dataframe(self) -> pd.DataFrame:
        """현재 재고 DataFrame 조회 (다운로드용)"""
        inventories = self.db.query(Inventory).all()

        data = []
        for inv in inventories:
            bean = self.db.query(Bean).filter(Bean.id == inv.bean_id).first()
            data.append({
                '원두명': bean.name if bean else "-",
                '재고 타입': inv.inventory_type,
                '수량(kg)': inv.quantity_kg,
                '최소 재고(kg)': inv.min_stock_kg,
                '최대 재고(kg)': inv.max_stock_kg,
                '마지막 업데이트': inv.last_updated
            })

        return pd.DataFrame(data)

    def get_transactions_dataframe(
        self,
        start_date: date,
        end_date: date,
        transaction_types: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """거래 내역 DataFrame 조회 (다운로드용)"""
        query = self.db.query(Transaction).filter(
            Transaction.created_at >= datetime.combine(start_date, datetime.min.time()),
            Transaction.created_at < datetime.combine(end_date, datetime.max.time())
        )

        if transaction_types:
            query = query.filter(Transaction.transaction_type.in_(transaction_types))

        transactions = query.order_by(Transaction.created_at.desc()).all()

        data = []
        for t in transactions:
            bean_name = "-"
            if t.bean_id:
                bean = self.db.query(Bean).filter(Bean.id == t.bean_id).first()
                bean_name = bean.name if bean else "-"

            data.append({
                '날짜': t.created_at,
                '거래 유형': t.transaction_type,
                '원두': bean_name,
                '재고 타입': t.inventory_type or "-",
                '수량(kg)': t.quantity_kg,
                '단가(원)': t.price_per_unit,
                '금액(원)': t.total_amount,
                '비고': t.notes or ""
            })

        return pd.DataFrame(data)

    def generate_monthly_excel(self, year: int, month: int) -> BytesIO:
        """월별 종합 리포트 Excel 생성"""
        report_data = self.get_monthly_transactions_report(year, month)

        # 거래 내역 조회
        if month == 12:
            start_date = date(year, month, 1)
            end_date = date(year + 1, 1, 1)
        else:
            start_date = date(year, month, 1)
            end_date = date(year, month + 1, 1)

        transactions_df = self.get_transactions_dataframe(start_date, end_date)

        return create_monthly_report_excel(
            summary_data=report_data['summary'],
            daily_trend_df=report_data['daily_trend'],
            transaction_type_df=report_data['transaction_type'],
            transactions_df=transactions_df,
            year=year,
            month=month
        )
