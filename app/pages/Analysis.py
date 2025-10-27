"""
분석 페이지
통계, 차트, 비용 분석, 수익 분석
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.bean_service import BeanService
from services.blend_service import BlendService

st.set_page_config(page_title="분석", page_icon="📊", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

if "blend_service" not in st.session_state:
    st.session_state.blend_service = BlendService(st.session_state.db)

bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📊 분석</h1>", unsafe_allow_html=True)
st.markdown("원두, 블렌드, 비용 및 수익에 대한 상세 분석")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 개요", "☕ 원두 분석", "🎨 블렌드 분석", "💰 비용 분석", "📊 통계"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 개요
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📈 주요 지표 개요")

    # 기본 통계 로드
    bean_summary = bean_service.get_beans_summary()
    blend_summary = blend_service.get_blends_summary()

    # 핵심 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("☕ 원두 종류", f"{bean_summary['total_beans']}종")

    with col2:
        st.metric("🎨 블렌드 개수", f"{blend_summary['total_blends']}개")

    with col3:
        beans = bean_service.get_active_beans()
        total_price = sum(b.price_per_kg for b in beans if b.price_per_kg > 0)
        st.metric("💰 원두 총 가격", f"₩{total_price:,.0f}")

    with col4:
        blends = blend_service.get_active_blends()
        total_suggested = sum(b.suggested_price or 0 for b in blends)
        st.metric("🎯 블렌드 총 제안가", f"₩{total_suggested:,.0f}")

    st.divider()

    # 로스팅 레벨 분포
    st.markdown("#### 🔥 로스팅 레벨 분포")

    roast_data = bean_summary['by_roast_level']

    if roast_data:
        fig_roast = go.Figure(data=[go.Pie(
            labels=list(roast_data.keys()),
            values=list(roast_data.values()),
            hovertemplate="<b>%{label}</b><br>개수: %{value}개<br>비율: %{percent}<extra></extra>"
        )])

        fig_roast.update_layout(
            title="로스팅 레벨별 원두 분포",
            height=400
        )

        st.plotly_chart(fig_roast, use_container_width=True)

    # 블렌드 타입 분포
    st.markdown("#### 🎨 블렌드 타입 분포")

    type_data = blend_summary['by_type']

    if type_data:
        col1, col2 = st.columns(2)

        with col1:
            fig_type = go.Figure(data=[go.Pie(
                labels=list(type_data.keys()),
                values=list(type_data.values()),
                hovertemplate="<b>%{label}</b><br>개수: %{value}개<br>비율: %{percent}<extra></extra>"
            )])

            fig_type.update_layout(
                title="블렌드 타입별 분포",
                height=400
            )

            st.plotly_chart(fig_type, use_container_width=True)

        with col2:
            type_info = f"""
            **블렌드 타입별 상세:**
            """
            for blend_type, count in type_data.items():
                type_info += f"\n- **{blend_type}**: {count}개"

            st.markdown(type_info)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 원두 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### ☕ 원두 분석")

    beans = bean_service.get_active_beans()

    if beans:
        # 원두별 가격 분석
        st.markdown("#### 💰 원두별 가격 분석")

        bean_prices = []
        for bean in beans:
            if bean.price_per_kg > 0:
                bean_prices.append({
                    "원두명": bean.name,
                    "국가": bean.country_code,
                    "로스팅": bean.roast_level,
                    "가격/kg": bean.price_per_kg
                })

        if bean_prices:
            df_prices = pd.DataFrame(bean_prices)
            df_prices = df_prices.sort_values("가격/kg", ascending=False)

            fig_price = go.Figure(data=[go.Bar(
                x=df_prices["원두명"],
                y=df_prices["가격/kg"],
                marker_color="#4472C4",
                hovertemplate="<b>%{x}</b><br>가격: ₩%{y:,.0f}/kg<extra></extra>"
            )])

            fig_price.update_layout(
                title="원두별 가격 분포",
                xaxis_title="원두명",
                yaxis_title="가격 (원/kg)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_price, use_container_width=True)

        # 로스팅별 원두 분포
        st.markdown("#### 🔥 로스팅 레벨별 원두 분포")

        roast_distribution = {}
        for bean in beans:
            roast = bean.roast_level
            if roast not in roast_distribution:
                roast_distribution[roast] = []
            roast_distribution[roast].append(bean.name)

        col1, col2 = st.columns(2)

        with col1:
            fig_roast_dist = go.Figure(data=[go.Bar(
                x=list(roast_distribution.keys()),
                y=[len(beans_list) for beans_list in roast_distribution.values()],
                marker_color=["#70AD47", "#4472C4", "#FFC000", "#5B9BD5", "#C41E3A", "#ED7D31"],
                text=[len(beans_list) for beans_list in roast_distribution.values()],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>개수: %{y}개<extra></extra>"
            )])

            fig_roast_dist.update_layout(
                title="로스팅별 원두 개수",
                xaxis_title="로스팅 레벨",
                yaxis_title="개수",
                height=400,
                showlegend=False
            )

            st.plotly_chart(fig_roast_dist, use_container_width=True)

        with col2:
            st.markdown("**로스팅별 원두 목록:**")
            for roast, bean_list in sorted(roast_distribution.items()):
                st.write(f"- **{roast}**: {', '.join(bean_list)}")

        # 국가별 원두 분포
        st.markdown("#### 🌍 국가별 원두 분포")

        country_distribution = {}
        for bean in beans:
            country = bean.country_code or "기타"
            if country not in country_distribution:
                country_distribution[country] = []
            country_distribution[country].append(bean.name)

        col1, col2 = st.columns(2)

        with col1:
            fig_country = go.Figure(data=[go.Bar(
                x=list(country_distribution.keys()),
                y=[len(beans_list) for beans_list in country_distribution.values()],
                marker_color="#5B9BD5",
                text=[len(beans_list) for beans_list in country_distribution.values()],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>개수: %{y}개<extra></extra>"
            )])

            fig_country.update_layout(
                title="국가별 원두 개수",
                xaxis_title="국가",
                yaxis_title="개수",
                height=400,
                showlegend=False
            )

            st.plotly_chart(fig_country, use_container_width=True)

        with col2:
            st.markdown("**국가별 원두 목록:**")
            for country, bean_list in sorted(country_distribution.items()):
                st.write(f"- **{country}**: {', '.join(bean_list)}")

    else:
        st.info("분석할 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 블렌드 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### 🎨 블렌드 분석")

    blends = blend_service.get_active_blends()

    if blends:
        # 블렌드별 원가 분석
        st.markdown("#### 💰 블렌드별 원가 분석")

        blend_costs = []
        for blend in blends:
            cost_info = blend_service.calculate_blend_cost(blend.id)
            if cost_info:
                blend_costs.append({
                    "블렌드명": blend.name,
                    "타입": blend.blend_type,
                    "포션당 원가": cost_info['cost_per_portion'],
                    "제안 판매가": cost_info['suggested_price'],
                    "예상 이익": cost_info['profit_margin']
                })

        if blend_costs:
            df_costs = pd.DataFrame(blend_costs)

            # 원가 비교
            col1, col2 = st.columns(2)

            with col1:
                fig_cost = go.Figure(data=[go.Bar(
                    x=df_costs["블렌드명"],
                    y=df_costs["포션당 원가"],
                    marker_color="#70AD47",
                    hovertemplate="<b>%{x}</b><br>원가: ₩%{y:,.0f}<extra></extra>"
                )])

                fig_cost.update_layout(
                    title="블렌드별 포션당 원가",
                    xaxis_title="블렌드명",
                    yaxis_title="원가 (원)",
                    height=400,
                    xaxis_tickangle=-45
                )

                st.plotly_chart(fig_cost, use_container_width=True)

            with col2:
                fig_price = go.Figure(data=[go.Bar(
                    x=df_costs["블렌드명"],
                    y=df_costs["제안 판매가"],
                    marker_color="#4472C4",
                    hovertemplate="<b>%{x}</b><br>판매가: ₩%{y:,.0f}<extra></extra>"
                )])

                fig_price.update_layout(
                    title="블렌드별 제안 판매가",
                    xaxis_title="블렌드명",
                    yaxis_title="판매가 (원)",
                    height=400,
                    xaxis_tickangle=-45
                )

                st.plotly_chart(fig_price, use_container_width=True)

            # 예상 이익 분석
            st.markdown("#### 📈 예상 이익 분석")

            fig_profit = go.Figure(data=[go.Bar(
                x=df_costs["블렌드명"],
                y=df_costs["예상 이익"],
                marker_color="#FFC000",
                hovertemplate="<b>%{x}</b><br>이익: ₩%{y:,.0f}<extra></extra>"
            )])

            fig_profit.update_layout(
                title="블렌드별 예상 이익 (포션당)",
                xaxis_title="블렌드명",
                yaxis_title="이익 (원)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_profit, use_container_width=True)

            # 테이블 표시
            st.markdown("#### 📊 블렌드 비용 상세")

            st.dataframe(df_costs, use_container_width=True, hide_index=True)

    else:
        st.info("분석할 블렌드가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 비용 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### 💰 비용 분석")

    blends = blend_service.get_active_blends()

    if blends:
        # 블렌드별 비용 구성 분석
        st.markdown("#### 📊 비용 구성 분석")

        selected_blend_name = st.selectbox(
            "블렌드 선택",
            options=[b.name for b in blends]
        )

        selected_blend = next((b for b in blends if b.name == selected_blend_name), None)

        if selected_blend:
            cost_info = blend_service.calculate_blend_cost(selected_blend.id)

            if cost_info:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("포션당 원가", f"₩{cost_info['cost_per_portion']:,.0f}")

                with col2:
                    st.metric("제안 판매가", f"₩{cost_info['suggested_price']:,.0f}")

                with col3:
                    st.metric("예상 이익", f"₩{cost_info['profit_margin']:,.0f}")

                st.divider()

                # 비용 구성 파이 차트
                cost_breakdown = [
                    cost_info.get('bean_cost_total', 0),
                    cost_info.get('roasting_cost', 0),
                    cost_info.get('labor_cost', 0),
                    cost_info.get('misc_cost', 0)
                ]

                cost_labels = ["원두 비용", "로스팅 비용", "인건비", "기타 비용"]

                fig_pie = go.Figure(data=[go.Pie(
                    labels=cost_labels,
                    values=cost_breakdown,
                    hovertemplate="<b>%{label}</b><br>₩%{value:,.0f}<br>비율: %{percent}<extra></extra>"
                )])

                fig_pie.update_layout(
                    title=f"{selected_blend.name} - 비용 구성",
                    height=400
                )

                st.plotly_chart(fig_pie, use_container_width=True)

                # 상세 비용 정보
                st.markdown("#### 📈 세부 비용 내역")

                cost_detail_data = {
                    "비용항목": cost_labels,
                    "금액": cost_breakdown,
                    "비율": [f"{v/sum(cost_breakdown)*100:.1f}%" for v in cost_breakdown]
                }

                df_cost_detail = pd.DataFrame(cost_detail_data)
                st.dataframe(df_cost_detail, use_container_width=True, hide_index=True)

                # 모든 블렌드의 비용 비교
                st.divider()
                st.markdown("#### 🔍 모든 블렌드 비용 비교")

                all_costs = []
                for blend in blends:
                    cost = blend_service.calculate_blend_cost(blend.id)
                    if cost:
                        all_costs.append({
                            "블렌드명": blend.name,
                            "원두 비용": cost.get('bean_cost_total', 0),
                            "로스팅 비용": cost.get('roasting_cost', 0),
                            "인건비": cost.get('labor_cost', 0),
                            "기타": cost.get('misc_cost', 0)
                        })

                if all_costs:
                    df_all_costs = pd.DataFrame(all_costs)

                    # 누적 막대 차트
                    fig_stacked = go.Figure(data=[
                        go.Bar(name="원두 비용", x=df_all_costs["블렌드명"], y=df_all_costs["원두 비용"]),
                        go.Bar(name="로스팅 비용", x=df_all_costs["블렌드명"], y=df_all_costs["로스팅 비용"]),
                        go.Bar(name="인건비", x=df_all_costs["블렌드명"], y=df_all_costs["인건비"]),
                        go.Bar(name="기타", x=df_all_costs["블렌드명"], y=df_all_costs["기타"])
                    ])

                    fig_stacked.update_layout(
                        barmode="stack",
                        title="블렌드별 비용 구성 (누적)",
                        xaxis_title="블렌드명",
                        yaxis_title="비용 (원)",
                        height=400,
                        xaxis_tickangle=-45
                    )

                    st.plotly_chart(fig_stacked, use_container_width=True)

    else:
        st.info("분석할 블렌드가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 5: 통계
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("### 📊 종합 통계")

    # 전체 통계 요약
    bean_summary = bean_service.get_beans_summary()
    blend_summary = blend_service.get_blends_summary()

    st.markdown("#### 📈 데이터 요약")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**원두 통계**")
        st.write(f"- 총 원두: {bean_summary['total_beans']}종")
        st.write(f"- 활성 원두: {len(bean_service.get_active_beans())}종")

    with col2:
        st.markdown("**블렌드 통계**")
        st.write(f"- 총 블렌드: {blend_summary['total_blends']}개")
        st.write(f"- 활성 블렌드: {len(blend_service.get_active_blends())}개")

    with col3:
        st.markdown("**포션 통계**")
        total_portions = sum(b.total_portion for b in blend_service.get_active_blends())
        st.write(f"- 총 포션: {total_portions}개")

    st.divider()

    # 로스팅 레벨 상세 통계
    st.markdown("#### 🔥 로스팅 레벨 상세 통계")

    roast_stats = bean_summary['by_roast_level']
    roast_data_table = {
        "로스팅 레벨": list(roast_stats.keys()),
        "원두 개수": list(roast_stats.values()),
        "비율": [f"{count/sum(roast_stats.values())*100:.1f}%" for count in roast_stats.values()]
    }

    df_roast = pd.DataFrame(roast_data_table)
    st.dataframe(df_roast, use_container_width=True, hide_index=True)

    st.divider()

    # 블렌드 타입 상세 통계
    st.markdown("#### 🎨 블렌드 타입 상세 통계")

    type_stats = blend_summary['by_type']
    type_data_table = {
        "블렌드 타입": list(type_stats.keys()),
        "개수": list(type_stats.values()),
        "비율": [f"{count/sum(type_stats.values())*100:.1f}%" for count in type_stats.values()]
    }

    df_type = pd.DataFrame(type_data_table)
    st.dataframe(df_type, use_container_width=True, hide_index=True)

    st.divider()

    # 비용 통계
    st.markdown("#### 💰 비용 통계")

    beans = bean_service.get_active_beans()
    blends = blend_service.get_active_blends()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        bean_prices = [b.price_per_kg for b in beans if b.price_per_kg > 0]
        avg_bean_price = sum(bean_prices) / len(bean_prices) if bean_prices else 0
        st.metric("평균 원두 가격", f"₩{avg_bean_price:,.0f}/kg")

    with col2:
        blend_costs = [blend_service.calculate_blend_cost(b.id)['cost_per_portion']
                      for b in blends
                      if blend_service.calculate_blend_cost(b.id)]
        avg_blend_cost = sum(blend_costs) / len(blend_costs) if blend_costs else 0
        st.metric("평균 블렌드 원가", f"₩{avg_blend_cost:,.0f}")

    with col3:
        blend_prices = [b.suggested_price for b in blends if b.suggested_price]
        avg_suggested = sum(blend_prices) / len(blend_prices) if blend_prices else 0
        st.metric("평균 제안 판매가", f"₩{avg_suggested:,.0f}")

    with col4:
        total_bean_cost = sum(b.price_per_kg for b in beans if b.price_per_kg > 0)
        st.metric("총 원두 비용", f"₩{total_bean_cost:,.0f}")

    st.divider()

    # 최고/최저 통계
    st.markdown("#### 🏆 최고/최저 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**가장 비싼 원두**")
        expensive_beans = sorted(beans, key=lambda x: x.price_per_kg, reverse=True)[:3]
        for i, bean in enumerate(expensive_beans, 1):
            st.write(f"{i}. {bean.name}: ₩{bean.price_per_kg:,.0f}/kg")

    with col2:
        st.markdown("**가장 싼 원두**")
        cheap_beans = sorted(beans, key=lambda x: x.price_per_kg)[:3]
        for i, bean in enumerate(cheap_beans, 1):
            if bean.price_per_kg > 0:
                st.write(f"{i}. {bean.name}: ₩{bean.price_per_kg:,.0f}/kg")

    st.divider()

    # 블렌드별 최고 이익
    st.markdown("#### 💎 가장 이익이 높은 블렌드")

    blend_profits = []
    for blend in blends:
        cost_info = blend_service.calculate_blend_cost(blend.id)
        if cost_info:
            blend_profits.append({
                "블렌드": blend.name,
                "이익": cost_info['profit_margin']
            })

    if blend_profits:
        df_profits = pd.DataFrame(blend_profits)
        df_profits = df_profits.sort_values("이익", ascending=False)

        for i, row in enumerate(df_profits.head(3).itertuples(), 1):
            st.write(f"{i}. {row[1]}: ₩{row[2]:,.0f}")
