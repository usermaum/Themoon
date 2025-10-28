"""
보고서 생성 페이지
월별 판매, 비용 분석, 원두 사용량, 블렌드 성과 보고서
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.bean_service import BeanService
from services.blend_service import BlendService
from services.report_service import ReportService
from i18n import Translator, LanguageManager

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.report.page_title", "보고서")
st.set_page_config(page_title=page_title, page_icon="📄", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

if "blend_service" not in st.session_state:
    st.session_state.blend_service = BlendService(st.session_state.db)

if "report_service" not in st.session_state:
    st.session_state.report_service = ReportService(st.session_state.db)

db = st.session_state.db
bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service
report_service = st.session_state.report_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📄 보고서</h1>", unsafe_allow_html=True)
st.markdown("다양한 형식의 보고서를 생성하고 다운로드합니다.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 요약 보고서", "💰 비용 분석", "☕ 원두 사용량", "🎨 블렌드 성과", "📥 내보내기"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 요약 보고서
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📊 요약 보고서")

    # 날짜 선택
    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.number_input("년도", min_value=2020, max_value=2030, value=datetime.now().year)

    with col2:
        selected_month = st.selectbox(
            "월",
            options=list(range(1, 13)),
            format_func=lambda x: f"{x}월"
        )

    st.divider()

    # 월별 요약
    monthly_summary = report_service.get_monthly_summary(selected_year, selected_month)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📦 총 입고량",
            value=f"{monthly_summary['total_inflow']:.2f}kg"
        )

    with col2:
        st.metric(
            label="📤 총 출고량",
            value=f"{monthly_summary['total_outflow']:.2f}kg"
        )

    with col3:
        st.metric(
            label="🔄 순변화량",
            value=f"{monthly_summary['net_change']:.2f}kg",
            delta=f"{monthly_summary['net_change']:.2f}kg"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="💰 총 거래액",
            value=f"₩{monthly_summary['total_amount']:,.0f}"
        )

    with col2:
        st.metric(
            label="📝 거래 건수",
            value=monthly_summary['transaction_count'],
            delta="건"
        )

    st.divider()

    # 월별 요약 테이블
    st.markdown("#### 📋 거래 기록 요약")

    if monthly_summary['transactions']:
        transaction_data = []

        for trans in monthly_summary['transactions']:
            transaction_data.append({
                "거래유형": trans.transaction_type,
                "수량": f"{trans.quantity_kg:.2f}kg",
                "단가": f"₩{trans.price_per_unit:,.0f}",
                "합계": f"₩{trans.total_amount:,.0f}",
                "날짜": trans.created_at.strftime("%Y-%m-%d %H:%M"),
                "설명": trans.description or "-"
            })

        df_trans = pd.DataFrame(transaction_data)
        st.dataframe(df_trans, use_container_width=True, hide_index=True)

    else:
        st.info("이 기간에 거래 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 비용 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 💰 비용 분석")

    # 날짜 범위 선택
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "시작 날짜",
            value=datetime.now() - timedelta(days=30)
        )

    with col2:
        end_date = st.date_input(
            "종료 날짜",
            value=datetime.now()
        )

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    st.divider()

    # 비용 분석 데이터
    cost_analysis = report_service.get_cost_analysis(start_dt, end_dt)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📊 분석 기간",
            value=f"{cost_analysis['period_days']}일"
        )

    with col2:
        st.metric(
            label="💰 총 원가",
            value=f"₩{cost_analysis['total_cost']:,.0f}"
        )

    with col3:
        st.metric(
            label="📈 평균 원가",
            value=f"₩{cost_analysis['average_cost']:,.0f}"
        )

    st.divider()

    # 비용 분석 테이블
    st.markdown("#### 📋 블렌드별 비용 상세")

    cost_list = []

    for cost in cost_analysis['cost_analysis']:
        cost_list.append({
            "블렌드명": cost['blend_name'],
            "타입": cost['blend_type'],
            "포션": cost['total_portions'],
            "원두비용": f"₩{cost['bean_cost']:,.0f}",
            "로스팅비용": f"₩{cost['roasting_cost']:,.0f}",
            "인건비": f"₩{cost['labor_cost']:,.0f}",
            "기타비용": f"₩{cost['misc_cost']:,.0f}",
            "총원가": f"₩{cost['total_cost']:,.0f}",
            "포션당": f"₩{cost['cost_per_portion']:,.0f}"
        })

    if cost_list:
        df_cost = pd.DataFrame(cost_list)
        st.dataframe(df_cost, use_container_width=True, hide_index=True)

        # 비용 구성 비교
        st.markdown("#### 📊 비용 구성 분석")

        col1, col2 = st.columns(2)

        with col1:
            # 전체 비용 비율
            total_bean = sum(c['bean_cost'] for c in cost_analysis['cost_analysis'])
            total_roasting = sum(c['roasting_cost'] for c in cost_analysis['cost_analysis'])
            total_labor = sum(c['labor_cost'] for c in cost_analysis['cost_analysis'])
            total_misc = sum(c['misc_cost'] for c in cost_analysis['cost_analysis'])

            fig_pie = go.Figure(data=[go.Pie(
                labels=["원두", "로스팅", "인건비", "기타"],
                values=[total_bean, total_roasting, total_labor, total_misc],
                hovertemplate="<b>%{label}</b><br>₩%{value:,.0f}<br>비율: %{percent}<extra></extra>"
            )])

            fig_pie.update_layout(
                title="전체 비용 구성",
                height=400
            )

            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # 블렌드별 비용 비교
            blend_costs = []
            blend_names = []

            for cost in cost_analysis['cost_analysis']:
                blend_names.append(cost['blend_name'])
                blend_costs.append(cost['total_cost'])

            fig_bar = go.Figure(data=[go.Bar(
                x=blend_names,
                y=blend_costs,
                marker_color="#4472C4",
                text=[f"₩{c:,.0f}" for c in blend_costs],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
            )])

            fig_bar.update_layout(
                title="블렌드별 총 원가",
                xaxis_title="블렌드명",
                yaxis_title="원가 (원)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("이 기간에 데이터가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 원두 사용량
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### ☕ 원두 사용량 분석")

    # 날짜 범위 선택
    col1, col2 = st.columns(2)

    with col1:
        start_date_3 = st.date_input(
            "시작 날짜",
            value=datetime.now() - timedelta(days=30),
            key="start_date_3"
        )

    with col2:
        end_date_3 = st.date_input(
            "종료 날짜",
            value=datetime.now(),
            key="end_date_3"
        )

    start_dt_3 = datetime.combine(start_date_3, datetime.min.time())
    end_dt_3 = datetime.combine(end_date_3, datetime.max.time())

    st.divider()

    # 원두 사용량 분석
    usage_analysis = report_service.get_bean_usage_analysis(start_dt_3, end_dt_3)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📊 분석 기간",
            value=f"{(end_dt_3 - start_dt_3).days}일"
        )

    with col2:
        total_inflow = sum(u['inflow_kg'] for u in usage_analysis['usage_analysis'])
        st.metric(
            label="📥 총 입고량",
            value=f"{total_inflow:.2f}kg"
        )

    with col3:
        total_outflow = sum(u['outflow_kg'] for u in usage_analysis['usage_analysis'])
        st.metric(
            label="📤 총 출고량",
            value=f"{total_outflow:.2f}kg"
        )

    st.divider()

    # 원두 사용량 테이블
    st.markdown("#### 📋 원두별 사용량")

    usage_list = []

    for usage in usage_analysis['usage_analysis']:
        usage_list.append({
            "원두명": usage['bean_name'],
            "국가": usage['country'],
            "로스팅": usage['roast_level'],
            "입고": f"{usage['inflow_kg']:.2f}kg",
            "출고": f"{usage['outflow_kg']:.2f}kg",
            "순변화": f"{usage['net_kg']:.2f}kg",
            "사용비용": f"₩{usage['outflow_cost']:,.0f}"
        })

    if usage_list:
        df_usage = pd.DataFrame(usage_list)
        st.dataframe(df_usage, use_container_width=True, hide_index=True)

        # 시각화
        st.markdown("#### 📊 사용량 분석")

        col1, col2 = st.columns(2)

        with col1:
            # 원두별 사용량
            bean_names = [u['bean_name'] for u in usage_analysis['usage_analysis']]
            outflows = [u['outflow_kg'] for u in usage_analysis['usage_analysis']]

            fig_usage = go.Figure(data=[go.Bar(
                x=bean_names,
                y=outflows,
                marker_color="#70AD47",
                text=[f"{q:.2f}kg" for q in outflows],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>%{y:.2f}kg<extra></extra>"
            )])

            fig_usage.update_layout(
                title="원두별 사용량 (출고량)",
                xaxis_title="원두명",
                yaxis_title="사용량 (kg)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_usage, use_container_width=True)

        with col2:
            # 사용 비용
            costs = [u['outflow_cost'] for u in usage_analysis['usage_analysis']]

            fig_cost = go.Figure(data=[go.Bar(
                x=bean_names,
                y=costs,
                marker_color="#4472C4",
                text=[f"₩{c:,.0f}" for c in costs],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
            )])

            fig_cost.update_layout(
                title="원두별 사용 비용",
                xaxis_title="원두명",
                yaxis_title="비용 (원)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_cost, use_container_width=True)

    else:
        st.info("이 기간에 사용 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 블렌드 성과
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### 🎨 블렌드 성과 분석")

    st.divider()

    # 블렌드 성과 분석
    performance = report_service.get_blend_performance()

    col1, col2 = st.columns(2)

    with col1:
        if performance['best_blend']:
            st.success(f"""
            **🏆 가장 이익이 높은 블렌드**

            블렌드: {performance['best_blend']['blend_name']}
            수익률: {performance['best_blend']['profit_rate']:.1f}%
            포션당 이익: ₩{performance['best_blend']['profit_per_portion']:,.0f}
            """)

    with col2:
        if performance['worst_blend']:
            st.warning(f"""
            **⚠️ 가장 이익이 낮은 블렌드**

            블렌드: {performance['worst_blend']['blend_name']}
            수익률: {performance['worst_blend']['profit_rate']:.1f}%
            포션당 이익: ₩{performance['worst_blend']['profit_per_portion']:,.0f}
            """)

    st.divider()

    # 블렌드 성과 테이블
    st.markdown("#### 📋 블렌드별 성과")

    perf_list = []

    for blend in performance['performance']:
        perf_list.append({
            "블렌드명": blend['blend_name'],
            "타입": blend['blend_type'],
            "포션": blend['total_portions'],
            "포션당원가": f"₩{blend['cost_per_portion']:,.0f}",
            "제안판매가": f"₩{blend['suggested_price']:,.0f}",
            "포션당이익": f"₩{blend['profit_per_portion']:,.0f}",
            "수익률": f"{blend['profit_rate']:.1f}%"
        })

    df_perf = pd.DataFrame(perf_list)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)

    st.divider()

    # 시각화
    st.markdown("#### 📊 성과 분석")

    col1, col2 = st.columns(2)

    with col1:
        # 수익률 비교
        blend_names = [b['blend_name'] for b in performance['performance']]
        profit_rates = [b['profit_rate'] for b in performance['performance']]

        fig_profit = go.Figure(data=[go.Bar(
            x=blend_names,
            y=profit_rates,
            marker_color="#70AD47",
            text=[f"{p:.1f}%" for p in profit_rates],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"
        )])

        fig_profit.update_layout(
            title="블렌드별 수익률",
            xaxis_title="블렌드명",
            yaxis_title="수익률 (%)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_profit, use_container_width=True)

    with col2:
        # 포션당 이익 비교
        profits = [b['profit_per_portion'] for b in performance['performance']]

        fig_margin = go.Figure(data=[go.Bar(
            x=blend_names,
            y=profits,
            marker_color="#4472C4",
            text=[f"₩{p:,.0f}" for p in profits],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
        )])

        fig_margin.update_layout(
            title="블렌드별 포션당 이익",
            xaxis_title="블렌드명",
            yaxis_title="이익 (원)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_margin, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 5: 내보내기
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("### 📥 보고서 내보내기")

    # 보고서 선택
    report_type = st.selectbox(
        "내보낼 보고서 유형",
        options=["all", "summary", "cost", "bean_usage", "blend"],
        format_func=lambda x: {
            "all": "📊 전체 보고서",
            "summary": "📋 요약 보고서",
            "cost": "💰 비용 분석",
            "bean_usage": "☕ 원두 사용량",
            "blend": "🎨 블렌드 성과"
        }.get(x, x)
    )

    st.divider()

    # 내보내기 포맷
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📑 Excel 내보내기")

        try:
            excel_data = report_service.export_to_excel(report_type)

            st.download_button(
                label="📥 Excel 다운로드",
                data=excel_data,
                file_name=f"보고서_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ Excel 형식으로 내보낼 준비가 되었습니다.")

        except Exception as e:
            st.error(f"❌ Excel 내보내기 오류: {str(e)}")

    with col2:
        st.markdown("#### 📑 CSV 내보내기")

        try:
            csv_data = report_service.export_to_csv(report_type)

            st.download_button(
                label="📥 CSV 다운로드",
                data=csv_data,
                file_name=f"보고서_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            st.success("✅ CSV 형식으로 내보낼 준비가 되었습니다.")

        except Exception as e:
            st.error(f"❌ CSV 내보내기 오류: {str(e)}")

    st.divider()

    st.markdown("#### ℹ️ 보고서 설명")

    st.info("""
    **📊 전체 보고서**: 모든 분석 데이터를 포함한 종합 보고서

    **📋 요약 보고서**: 기본 통계 데이터 (원두 종류, 블렌드 개수 등)

    **💰 비용 분석**: 블렌드별 원가 구성 및 비용 분석

    **☕ 원두 사용량**: 원두별 입고/출고 기록 및 사용량

    **🎨 블렌드 성과**: 블렌드별 수익률 및 이익 분석
    """)
