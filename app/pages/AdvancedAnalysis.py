"""
고급 분석 페이지
트렌드, 예측, ROI, 성능 지표, 효율성 분석
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.analytics_service import AnalyticsService
from i18n import Translator, LanguageManager

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.advanced_analysis.page_title", "고급분석")
st.set_page_config(page_title=page_title, page_icon="📈", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "analytics_service" not in st.session_state:
    st.session_state.analytics_service = AnalyticsService(st.session_state.db)

db = st.session_state.db
analytics_service = st.session_state.analytics_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📈 고급 분석</h1>", unsafe_allow_html=True)
st.markdown("트렌드, 예측, ROI, 성능 지표 등 심화된 분석")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 트렌드", "🔮 예측", "💹 ROI", "⚡ 성능", "🎯 효율성"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 트렌드 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📊 월별 거래 트렌드")

    # 월수 선택
    months = st.slider("표시할 개월 수", min_value=3, max_value=24, value=12)

    st.divider()

    # 트렌드 데이터 로드
    trend_data = analytics_service.get_monthly_trend(months)

    if trend_data:
        # 트렌드 테이블
        st.markdown("#### 📋 월별 통계")

        table_data = []
        for trend in trend_data:
            table_data.append({
                "기간": trend['period'],
                "입고": f"{trend['inflow']:.2f}kg",
                "출고": f"{trend['outflow']:.2f}kg",
                "순변화": f"{trend['net_change']:.2f}kg",
                "거래액": f"₩{trend['amount']:,.0f}",
                "거래건수": trend['transaction_count']
            })

        df_trend = pd.DataFrame(table_data)
        st.dataframe(df_trend, use_container_width=True, hide_index=True)

        st.divider()

        # 트렌드 차트
        st.markdown("#### 📈 거래량 추이")

        col1, col2 = st.columns(2)

        with col1:
            # 입출고 추이
            periods = [t['period'] for t in trend_data]
            inflows = [t['inflow'] for t in trend_data]
            outflows = [t['outflow'] for t in trend_data]

            fig_quantity = go.Figure()

            fig_quantity.add_trace(go.Scatter(
                x=periods, y=inflows,
                mode='lines+markers',
                name='입고',
                line=dict(color='#70AD47', width=2),
                marker=dict(size=6)
            ))

            fig_quantity.add_trace(go.Scatter(
                x=periods, y=outflows,
                mode='lines+markers',
                name='출고',
                line=dict(color='#C41E3A', width=2),
                marker=dict(size=6)
            ))

            fig_quantity.update_layout(
                title="입출고 추이",
                xaxis_title="기간",
                yaxis_title="수량 (kg)",
                height=400,
                hovermode='x unified'
            )

            st.plotly_chart(fig_quantity, use_container_width=True)

        with col2:
            # 거래액 추이
            amounts = [t['amount'] for t in trend_data]

            fig_amount = go.Figure(data=[go.Bar(
                x=periods,
                y=amounts,
                marker_color='#4472C4',
                text=[f"₩{a:,.0f}" for a in amounts],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
            )])

            fig_amount.update_layout(
                title="월별 거래액",
                xaxis_title="기간",
                yaxis_title="거래액 (원)",
                height=400
            )

            st.plotly_chart(fig_amount, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 예측 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 🔮 재고 및 사용량 예측")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📦 재고 예측 (향후 30일)")

        projection_days = st.number_input("예측 기간 (일)", min_value=7, max_value=90, value=30)

    with col2:
        st.markdown("#### 📊 사용량 예측 (향후 60일)")

        forecast_days = st.number_input("예측 기간 (일)", min_value=7, max_value=180, value=60, key="forecast_days")

    st.divider()

    col1, col2 = st.columns(2)

    # 재고 예측
    with col1:
        st.markdown("#### 📦 원두별 재고 예측")

        projections = analytics_service.get_inventory_projection(projection_days)

        if projections:
            projection_data = []

            for proj in projections:
                projection_data.append({
                    "원두명": proj['bean_name'],
                    "현재": f"{proj['current_quantity']:.2f}kg",
                    "일평균": f"{proj['daily_usage']:.2f}kg",
                    f"향후{projection_days}일": f"{proj['projected_quantity']:.2f}kg",
                    "소진예상": f"{proj['days_until_depletion']:.0f}일",
                    "경고": "🔴 위험" if proj['is_critical'] else "✅ 정상"
                })

            df_proj = pd.DataFrame(projection_data)
            st.dataframe(df_proj, use_container_width=True, hide_index=True)

            # 위험 원두 강조
            critical = [p for p in projections if p['is_critical']]
            if critical:
                st.warning(f"⚠️ {len(critical)}개 원두가 예상 기간 내 최소 재고 이하로 내려갈 것으로 예상됩니다.")
                for crit in critical:
                    st.write(f"- {crit['bean_name']}: {crit['projected_quantity']:.2f}kg → {crit['days_until_depletion']:.0f}일 소진")

    # 사용량 예측
    with col2:
        st.markdown("#### 📊 사용량 예측")

        usage_forecast = analytics_service.get_usage_forecast(forecast_days)

        st.metric(
            label="일평균 사용량",
            value=f"{usage_forecast['avg_daily_usage']:.2f}kg"
        )

        st.metric(
            label=f"향후 {forecast_days}일 누적 사용량",
            value=f"{usage_forecast['forecast'][-1]['cumulative_usage']:.2f}kg"
        )

        # 예측 차트
        forecast = usage_forecast['forecast']
        forecast_dates = [f['date'] for f in forecast]
        cumulative_usages = [f['cumulative_usage'] for f in forecast]

        fig_forecast = go.Figure(data=[go.Scatter(
            x=forecast_dates,
            y=cumulative_usages,
            mode='lines+markers',
            name='누적 사용량',
            line=dict(color='#70AD47', width=2),
            fill='tozeroy',
            hovertemplate="<b>%{x}</b><br>%{y:.2f}kg<extra></extra>"
        )])

        fig_forecast.update_layout(
            title=f"향후 {forecast_days}일 누적 사용량 예측",
            xaxis_title="날짜",
            yaxis_title="누적 사용량 (kg)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_forecast, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: ROI 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### 💹 ROI 분석")

    st.divider()

    # ROI 데이터
    roi_analysis = analytics_service.get_roi_analysis()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="평균 ROI",
            value=f"{roi_analysis['average_roi']:.1f}%"
        )

    with col2:
        if roi_analysis['best_roi']:
            st.metric(
                label="최고 ROI",
                value=f"{roi_analysis['best_roi']['roi_percent']:.1f}%",
                delta=roi_analysis['best_roi']['blend_name']
            )

    with col3:
        if roi_analysis['worst_roi']:
            st.metric(
                label="최저 ROI",
                value=f"{roi_analysis['worst_roi']['roi_percent']:.1f}%",
                delta=roi_analysis['worst_roi']['blend_name']
            )

    st.divider()

    # ROI 테이블
    st.markdown("#### 📋 블렌드별 ROI")

    roi_data = []
    for roi in roi_analysis['roi_data']:
        roi_data.append({
            "블렌드명": roi['blend_name'],
            "타입": roi['blend_type'],
            "포션": roi['portioncount'],
            "총원가": f"₩{roi['total_cost']:,.0f}",
            "총수익": f"₩{roi['total_revenue']:,.0f}",
            "총이익": f"₩{roi['total_profit']:,.0f}",
            "ROI": f"{roi['roi_percent']:.1f}%"
        })

    df_roi = pd.DataFrame(roi_data)
    st.dataframe(df_roi, use_container_width=True, hide_index=True)

    st.divider()

    # ROI 시각화
    st.markdown("#### 📊 ROI 비교")

    col1, col2 = st.columns(2)

    with col1:
        roi_values = [roi['roi_percent'] for roi in roi_analysis['roi_data']]
        blend_names = [roi['blend_name'] for roi in roi_analysis['roi_data']]

        fig_roi = go.Figure(data=[go.Bar(
            x=blend_names,
            y=roi_values,
            marker_color=['#70AD47' if v > roi_analysis['average_roi'] else '#C41E3A' for v in roi_values],
            text=[f"{v:.1f}%" for v in roi_values],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"
        )])

        fig_roi.update_layout(
            title="블렌드별 ROI",
            xaxis_title="블렌드명",
            yaxis_title="ROI (%)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_roi, use_container_width=True)

    with col2:
        profits = [roi['total_profit'] for roi in roi_analysis['roi_data']]

        fig_profit = go.Figure(data=[go.Bar(
            x=blend_names,
            y=profits,
            marker_color="#4472C4",
            text=[f"₩{p:,.0f}" for p in profits],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
        )])

        fig_profit.update_layout(
            title="블렌드별 총 이익",
            xaxis_title="블렌드명",
            yaxis_title="이익 (원)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_profit, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 성능 지표
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### ⚡ 성능 지표")

    st.divider()

    # 성능 메트릭 로드
    metrics = analytics_service.get_performance_metrics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📝 총 거래", f"{metrics['total_transactions']:,}")

    with col2:
        st.metric("☕ 활성 원두", f"{metrics['active_beans']}")

    with col3:
        st.metric("🎨 활성 블렌드", f"{metrics['active_blends']}")

    with col4:
        st.metric("📊 월별 거래액", f"₩{metrics['monthly_revenue']:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📦 사용량")

        st.write(f"""
        **월별 사용량:** {metrics['monthly_usage']:.2f}kg

        **일평균 사용량:** {metrics['daily_usage']:.2f}kg
        """)

    with col2:
        st.markdown("#### 💰 거래")

        st.write(f"""
        **월별 거래액:** ₩{metrics['monthly_revenue']:,.0f}

        **거래당 평균액:** ₩{metrics['average_transaction_amount']:,.0f}
        """)

    st.divider()

    # 효율성 점수
    st.markdown("#### 🎯 효율성 점수")

    # 활성도
    activity_score = min(100, (metrics['total_transactions'] / 10))
    diversity_score = min(100, (metrics['active_beans'] / 0.13))  # 13종 기준

    col1, col2 = st.columns(2)

    with col1:
        st.metric("활동성", f"{activity_score:.0f}/100")

    with col2:
        st.metric("다양성", f"{diversity_score:.0f}/100")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 5: 효율성 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("### 🎯 효율성 분석")

    st.divider()

    # 원두 효율성
    st.markdown("#### ☕ 원두별 효율성")

    efficiency = analytics_service.get_bean_efficiency()

    if efficiency['efficiency']:
        efficiency_data = []

        for eff in efficiency['efficiency']:
            efficiency_data.append({
                "원두명": eff['bean_name'],
                "가격/kg": f"₩{eff['price_per_kg']:,.0f}",
                "사용횟수": eff['usage_count'],
                "총사용량": f"{eff['usage_quantity']:.2f}kg",
                "사용비용": f"₩{eff['usage_cost']:,.0f}",
                "평균사용": f"{eff['avg_use_per_transaction']:.2f}kg"
            })

        df_eff = pd.DataFrame(efficiency_data)
        st.dataframe(df_eff, use_container_width=True, hide_index=True)

        # 효율성 차트
        st.markdown("#### 📊 원두 사용 빈도")

        col1, col2 = st.columns(2)

        with col1:
            # 사용 빈도
            bean_names = [e['bean_name'] for e in efficiency['efficiency']]
            usage_counts = [e['usage_count'] for e in efficiency['efficiency']]

            fig_usage = go.Figure(data=[go.Bar(
                x=bean_names,
                y=usage_counts,
                marker_color="#70AD47",
                text=usage_counts,
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>%{y}회<extra></extra>"
            )])

            fig_usage.update_layout(
                title="원두별 사용 빈도 (최근 30일)",
                xaxis_title="원두명",
                yaxis_title="사용 횟수",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_usage, use_container_width=True)

        with col2:
            # 사용량
            quantities = [e['usage_quantity'] for e in efficiency['efficiency']]

            fig_qty = go.Figure(data=[go.Bar(
                x=bean_names,
                y=quantities,
                marker_color="#4472C4",
                text=[f"{q:.2f}kg" for q in quantities],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>%{y:.2f}kg<extra></extra>"
            )])

            fig_qty.update_layout(
                title="원두별 사용량 (최근 30일)",
                xaxis_title="원두명",
                yaxis_title="사용량 (kg)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_qty, use_container_width=True)

    st.divider()

    # 블렌드 비교
    st.markdown("#### 🎨 블렌드 간 비교")

    comparison = analytics_service.get_comparison_analysis()

    if comparison['comparison']:
        comp_data = []

        for comp in comparison['comparison']:
            comp_data.append({
                "블렌드명": comp['blend_name'],
                "타입": comp['blend_type'],
                "원가": f"₩{comp['cost_per_portion']:,.0f}",
                "판매가": f"₩{comp['selling_price']:,.0f}",
                "이익": f"₩{comp['profit_per_portion']:,.0f}",
                "수익률": f"{comp['profit_rate']:.1f}%",
                "배수": f"{comp['price_to_cost_ratio']:.2f}배"
            })

        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        # 비교 차트
        st.markdown("#### 📊 블렌드 비교")

        col1, col2 = st.columns(2)

        with col1:
            # 수익률
            comp_names = [c['blend_name'] for c in comparison['comparison']]
            comp_rates = [c['profit_rate'] for c in comparison['comparison']]

            fig_comp_rate = go.Figure(data=[go.Bar(
                x=comp_names,
                y=comp_rates,
                marker_color="#70AD47",
                text=[f"{r:.1f}%" for r in comp_rates],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"
            )])

            fig_comp_rate.update_layout(
                title="블렌드 수익률 비교",
                xaxis_title="블렌드명",
                yaxis_title="수익률 (%)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_comp_rate, use_container_width=True)

        with col2:
            # 배수
            comp_ratios = [c['price_to_cost_ratio'] for c in comparison['comparison']]

            fig_comp_ratio = go.Figure(data=[go.Bar(
                x=comp_names,
                y=comp_ratios,
                marker_color="#4472C4",
                text=[f"{r:.2f}배" for r in comp_ratios],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>%{y:.2f}배<extra></extra>"
            )])

            fig_comp_ratio.update_layout(
                title="판매가/원가 배수",
                xaxis_title="블렌드명",
                yaxis_title="배수",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_comp_ratio, use_container_width=True)
