"""
대시보드 페이지
핵심 지표, 실시간 모니터링, 빠른 통계
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal, Inventory
from services.bean_service import BeanService
from services.blend_service import BlendService
from i18n import Translator, LanguageManager
from components.sidebar import render_sidebar

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.dashboard.page_title", "대시보드")
st.set_page_config(page_title=page_title, page_icon="📊", layout="wide")

# 현재 페이지 저장 (사이드바 활성 표시)
st.session_state["current_page"] = "Dashboard"

# 사이드바 렌더링
render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

if "blend_service" not in st.session_state:
    st.session_state.blend_service = BlendService(st.session_state.db)

db = st.session_state.db
bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📊 더문드립바 대시보드</h1>", unsafe_allow_html=True)
st.markdown("핵심 지표 및 실시간 모니터링")

# 새로고침 시간
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🔄", help="새로고침"):
        st.rerun()

with col1:
    st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 핵심 지표
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 🎯 핵심 지표")

bean_summary = bean_service.get_beans_summary()
blend_summary = blend_service.get_blends_summary()

beans = bean_service.get_active_beans()
blends = blend_service.get_active_blends()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="☕ 원두 종류",
        value=bean_summary['total_beans'],
        delta="종류"
    )

with col2:
    st.metric(
        label="🎨 블렌드",
        value=blend_summary['total_blends'],
        delta="개"
    )

with col3:
    total_portions = sum(b.total_portion for b in blends)
    st.metric(
        label="🔀 총 포션",
        value=total_portions,
        delta="개"
    )

with col4:
    total_price = sum(b.price_per_kg for b in beans if b.price_per_kg > 0)
    st.metric(
        label="💰 원두 가격 합",
        value=f"₩{total_price:,.0f}",
        delta=None
    )

with col5:
    blends_with_price = [b for b in blends if b.suggested_price]
    avg_price = sum(b.suggested_price for b in blends_with_price) / len(blends_with_price) if blends_with_price else 0
    st.metric(
        label="🎯 평균 판매가",
        value=f"₩{avg_price:,.0f}",
        delta=None
    )

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 원두 현황
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## ☕ 원두 현황")

col1, col2 = st.columns(2)

# 로스팅 레벨 분포
with col1:
    st.markdown("### 🔥 로스팅 레벨 분포")

    roast_data = bean_summary['by_roast_level']

    if roast_data:
        fig_roast = go.Figure(data=[go.Pie(
            labels=list(roast_data.keys()),
            values=list(roast_data.values()),
            marker=dict(colors=["#70AD47", "#4472C4", "#FFC000", "#5B9BD5", "#C41E3A", "#ED7D31"]),
            hovertemplate="<b>%{label}</b><br>%{value}개<br>비율: %{percent}<extra></extra>"
        )])

        fig_roast.update_layout(
            height=350,
            showlegend=True
        )

        st.plotly_chart(fig_roast, use_container_width=True)

# 가격 범위별 분포
with col2:
    st.markdown("### 💰 가격 범위별 분포")

    price_ranges = {
        "~10k": len([b for b in beans if b.price_per_kg > 0 and b.price_per_kg <= 10000]),
        "10k~20k": len([b for b in beans if b.price_per_kg > 10000 and b.price_per_kg <= 20000]),
        "20k~30k": len([b for b in beans if b.price_per_kg > 20000 and b.price_per_kg <= 30000]),
        "30k+": len([b for b in beans if b.price_per_kg > 30000])
    }

    fig_price_dist = go.Figure(data=[go.Bar(
        x=list(price_ranges.keys()),
        y=list(price_ranges.values()),
        marker_color="#4472C4",
        text=list(price_ranges.values()),
        textposition="auto",
        hovertemplate="<b>%{x}</b><br>%{y}개<extra></extra>"
    )])

    fig_price_dist.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="가격 범위 (원/kg)",
        yaxis_title="개수"
    )

    st.plotly_chart(fig_price_dist, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 블렌드 현황
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 🎨 블렌드 현황")

col1, col2 = st.columns(2)

# 블렌드 타입 분포
with col1:
    st.markdown("### 🎯 블렌드 타입 분포")

    type_data = blend_summary['by_type']

    if type_data:
        fig_type = go.Figure(data=[go.Pie(
            labels=list(type_data.keys()),
            values=list(type_data.values()),
            hovertemplate="<b>%{label}</b><br>%{value}개<br>비율: %{percent}<extra></extra>"
        )])

        fig_type.update_layout(
            height=350,
            showlegend=True
        )

        st.plotly_chart(fig_type, use_container_width=True)

# 블렌드별 포션 분포
with col2:
    st.markdown("### 🔀 블렌드별 포션 분포")

    blend_portions = []
    blend_names = []

    for blend in blends:
        blend_portions.append(blend.total_portion)
        blend_names.append(blend.name)

    if blend_portions:
        fig_portion = go.Figure(data=[go.Bar(
            x=blend_names,
            y=blend_portions,
            marker_color="#5B9BD5",
            text=blend_portions,
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>%{y}개<extra></extra>"
        )])

        fig_portion.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="블렌드명",
            yaxis_title="포션 개수",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_portion, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 원가 분석
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 💰 원가 분석")

col1, col2 = st.columns(2)

# 블렌드별 원가 비교
with col1:
    st.markdown("### 포션당 원가")

    blend_costs = []
    for blend in blends:
        cost_info = blend_service.calculate_blend_cost(blend.id)
        if cost_info:
            blend_costs.append({
                "blend_name": blend.name,
                "cost": cost_info['cost_per_portion']
            })

    if blend_costs:
        df_costs = pd.DataFrame(blend_costs)
        df_costs = df_costs.sort_values("cost", ascending=False)

        fig_cost = go.Figure(data=[go.Bar(
            x=df_costs["blend_name"],
            y=df_costs["cost"],
            marker_color="#70AD47",
            text=[f"₩{v:,.0f}" for v in df_costs["cost"]],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
        )])

        fig_cost.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="블렌드명",
            yaxis_title="원가 (원)",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_cost, use_container_width=True)

# 제안 판매가 비교
with col2:
    st.markdown("### 제안 판매가")

    blend_prices = []
    for blend in blends:
        if blend.suggested_price:
            blend_prices.append({
                "blend_name": blend.name,
                "price": blend.suggested_price
            })

    if blend_prices:
        df_prices = pd.DataFrame(blend_prices)
        df_prices = df_prices.sort_values("price", ascending=False)

        fig_price = go.Figure(data=[go.Bar(
            x=df_prices["blend_name"],
            y=df_prices["price"],
            marker_color="#4472C4",
            text=[f"₩{v:,.0f}" for v in df_prices["price"]],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>₩%{y:,.0f}<extra></extra>"
        )])

        fig_price.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="블렌드명",
            yaxis_title="판매가 (원)",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_price, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 재고 상태
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 📦 재고 상태")

# 저재고 확인
low_stock = []
normal_stock = []
over_stock = []

for bean in beans:
    inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

    if inventory:
        if inventory.min_quantity_kg > 0 and inventory.quantity_kg < inventory.min_quantity_kg:
            low_stock.append((bean, inventory))
        elif inventory.max_quantity_kg > 0 and inventory.quantity_kg > inventory.max_quantity_kg:
            over_stock.append((bean, inventory))
        else:
            normal_stock.append((bean, inventory))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🟢 정상 재고",
        value=len(normal_stock),
        delta="개"
    )

with col2:
    st.metric(
        label="🔴 저재고",
        value=len(low_stock),
        delta="개" if len(low_stock) == 0 else f"{len(low_stock)}개 ⚠️"
    )

with col3:
    st.metric(
        label="🟡 과재고",
        value=len(over_stock),
        delta="개" if len(over_stock) == 0 else f"{len(over_stock)}개 ⚠️"
    )

# 저재고 경고
if low_stock:
    st.warning("🔴 **저재고 경고!** 다음 원두들의 재고가 최소 수준 이하입니다:")

    for bean, inventory in low_stock:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"**{bean.name}**: {inventory.quantity_kg:.2f}kg (최소: {inventory.min_quantity_kg:.2f}kg)")

        with col2:
            if st.button("📦 입고", key=f"restock_{bean.id}"):
                st.info(f"{bean.name}의 입고를 진행하시려면 '재고관리' 페이지를 방문하세요.")

if over_stock:
    st.info("🟡 **과재고 알림!** 다음 원두들의 재고가 최대 수준을 초과했습니다:")

    for bean, inventory in over_stock:
        st.write(f"**{bean.name}**: {inventory.quantity_kg:.2f}kg (최대: {inventory.max_quantity_kg:.2f}kg)")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 빠른 링크
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 🔗 빠른 메뉴")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("☕ 원두 관리", use_container_width=True):
        st.switch_page("pages/BeanManagement.py")

with col2:
    if st.button("🎨 블렌딩 관리", use_container_width=True):
        st.switch_page("pages/BlendManagement.py")

with col3:
    if st.button("📊 분석", use_container_width=True):
        st.switch_page("pages/Analysis.py")

with col4:
    if st.button("📦 재고 관리", use_container_width=True):
        st.switch_page("pages/InventoryManagement.py")

with col5:
    if st.button("🔄 새로고침", use_container_width=True):
        st.rerun()

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 시스템 정보
# ═══════════════════════════════════════════════════════════════════════════════
# 손실률 분석 섹션
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📊 손실률 분석")

# 위젯 import
from components.loss_widgets import (
    render_loss_trend_chart,
    render_bean_comparison,
    render_warning_card,
    render_seasonal_prediction
)

# 기간 선택
loss_analysis_days = st.selectbox(
    "분석 기간 선택",
    options=[7, 14, 30, 60, 90],
    index=2,  # 기본 30일
    key="loss_analysis_days"
)

# 탭으로 구분
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 손실률 트렌드",
    "🌾 원두별 비교",
    "⚠️ 경고 알림",
    "🔮 계절성 예측"
])

with tab1:
    st.markdown("### 손실률 트렌드")
    render_loss_trend_chart(st.session_state.db, days=loss_analysis_days)

with tab2:
    st.markdown("### 원두별 손실률 비교")
    render_bean_comparison(st.session_state.db, days=loss_analysis_days)

with tab3:
    st.markdown("### 미해결 경고 알림")
    render_warning_card(st.session_state.db, limit=10)

with tab4:
    st.markdown("### 향후 3개월 손실률 예측")
    render_seasonal_prediction(st.session_state.db, months=3)

# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## ℹ️ 시스템 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    **애플리케이션**
    - 이름: 더문드립바
    - 버전: 2.0.0
    - 상태: Phase 2 (핵심 페이지)
    """)

with col2:
    st.markdown(f"""
    **데이터베이스**
    - 유형: SQLite
    - 위치: data/roasting_data.db
    - 테이블: 6개
    """)

with col3:
    st.markdown(f"""
    **실시간 통계**
    - 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    - 활성 원두: {len(beans)}종
    - 활성 블렌드: {len(blends)}개
    """)
