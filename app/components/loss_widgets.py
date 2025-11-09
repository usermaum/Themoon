"""
loss_widgets.py: 손실률 분석 Streamlit 위젯

Dashboard 페이지에서 사용할 손실률 분석 관련 시각화 컴포넌트
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import statistics

from app.models.database import RoastingLog
from app.services.loss_rate_analyzer import LossRateAnalyzer


def render_loss_trend_chart(db: Session, days: int = 30):
    """
    손실률 트렌드 차트 (Plotly)

    실제 손실률, 예상 손실률(17%), ±3σ 범위를 표시

    Args:
        db: SQLAlchemy 세션
        days: 조회 기간 (일)
    """
    # 1. 데이터 조회
    start_date = datetime.now().date() - timedelta(days=days)
    logs = db.query(RoastingLog).filter(
        RoastingLog.roasting_date >= start_date
    ).order_by(RoastingLog.roasting_date).all()

    if not logs:
        st.warning(f"⚠️ 최근 {days}일 동안의 로스팅 데이터가 없습니다.")
        return

    dates = [log.roasting_date for log in logs]
    loss_rates = [log.loss_rate_percent for log in logs]

    # 2. 3σ 범위 계산
    avg = statistics.mean(loss_rates)
    std = statistics.stdev(loss_rates) if len(loss_rates) > 1 else 0
    upper_3sigma = avg + 3 * std
    lower_3sigma = avg - 3 * std

    # 3. Plotly 차트 생성
    fig = go.Figure()

    # 실제 손실률
    fig.add_trace(go.Scatter(
        x=dates,
        y=loss_rates,
        mode='lines+markers',
        name='실제 손실률',
        line=dict(color='#4A90E2', width=2),
        marker=dict(size=6)
    ))

    # 예상 손실률 (17%)
    fig.add_trace(go.Scatter(
        x=dates,
        y=[17.0] * len(dates),
        mode='lines',
        name='예상 손실률 (17%)',
        line=dict(color='gray', dash='dash', width=2)
    ))

    # ±3σ 범위 (음영)
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=[upper_3sigma] * len(dates) + [lower_3sigma] * len(dates)[::-1],
        fill='toself',
        fillcolor='rgba(74, 144, 226, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        showlegend=True,
        name='±3σ 범위'
    ))

    fig.update_layout(
        title=f'손실률 트렌드 (최근 {days}일)',
        xaxis_title='날짜',
        yaxis_title='손실률 (%)',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # 통계 정보 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("평균 손실률", f"{avg:.2f}%")
    with col2:
        st.metric("표준편차", f"{std:.2f}%")
    with col3:
        st.metric("최소", f"{min(loss_rates):.2f}%")
    with col4:
        st.metric("최대", f"{max(loss_rates):.2f}%")


def render_bean_comparison(db: Session, days: int = 30):
    """
    원두별 손실률 비교 (막대 그래프)

    원두별 평균 손실률과 표준편차를 막대 그래프로 표시
    상태(NORMAL/ATTENTION/CRITICAL)에 따라 색상 구분

    Args:
        db: SQLAlchemy 세션
        days: 조회 기간 (일)
    """
    # 1. 원두별 통계 조회
    bean_stats = LossRateAnalyzer.get_loss_rate_by_bean(db, days)

    if not bean_stats:
        st.warning(f"⚠️ 최근 {days}일 동안의 원두별 데이터가 없습니다.")
        return

    bean_names = [s['bean_name'] for s in bean_stats]
    avg_losses = [s['avg_loss_rate'] for s in bean_stats]
    std_devs = [s['std_deviation'] for s in bean_stats]

    # 2. 색상 (상태별)
    colors = []
    for s in bean_stats:
        if s['status'] == 'CRITICAL':
            colors.append('#E74C3C')  # 빨강
        elif s['status'] == 'ATTENTION':
            colors.append('#F39C12')  # 주황
        else:
            colors.append('#50C878')  # 초록

    # 3. Plotly 막대 그래프
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bean_names,
        y=avg_losses,
        error_y=dict(type='data', array=std_devs),
        marker_color=colors,
        text=[f"{l:.1f}%" for l in avg_losses],
        textposition='outside'
    ))

    fig.update_layout(
        title=f'원두별 평균 손실률 (최근 {days}일)',
        xaxis_title='원두',
        yaxis_title='평균 손실률 (%)',
        yaxis_range=[0, max(avg_losses) + 5] if avg_losses else [0, 25],
        height=400,
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

    # 상태 범례
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟢 **NORMAL**: 글로벌 평균 대비 ±2% 이내")
    with col2:
        st.markdown("🟠 **ATTENTION**: 글로벌 평균 대비 ±2~3%")
    with col3:
        st.markdown("🔴 **CRITICAL**: 글로벌 평균 대비 ±3% 이상")


def render_warning_card(db: Session, limit: int = 5):
    """
    경고 알림 카드

    미해결 경고를 테이블로 표시하고 해결 기능 제공

    Args:
        db: SQLAlchemy 세션
        limit: 표시할 경고 최대 개수
    """
    warnings = LossRateAnalyzer.get_recent_warnings(db, limit)

    if not warnings:
        st.success("✅ 미해결 경고 없음")
        return

    st.warning(f"⚠️ 미해결 경고 {len(warnings)}건")

    # 테이블 데이터 가공
    table_data = []
    for w in warnings:
        table_data.append({
            '날짜': w['roasting_date'],
            '심각도': w['severity'],
            '편차': f"{w['variance']:.2f}%",
            '연속발생': f"{w['consecutive']}회",
            '경고ID': w['id']
        })

    df = pd.DataFrame(table_data)

    # 경고ID 제외하고 표시
    st.dataframe(
        df[['날짜', '심각도', '편차', '연속발생']],
        use_container_width=True,
        hide_index=True
    )

    # 해결 버튼
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("모두 해결", type="primary"):
            for w in warnings:
                LossRateAnalyzer.resolve_warning(
                    db,
                    w['id'],
                    notes="Dashboard에서 일괄 해결"
                )
            st.success("✅ 모든 경고가 해결되었습니다.")
            st.rerun()


def render_seasonal_prediction(db: Session, months: int = 3):
    """
    계절성 예측 차트

    향후 N개월의 예측 손실률을 차트로 표시

    Args:
        db: SQLAlchemy 세션
        months: 예측할 개월 수
    """
    from app.services.loss_analytics_service import LossAnalyticsService

    try:
        # 예측 실행
        forecasts = LossAnalyticsService.get_monthly_forecast(db, months)

        if not forecasts:
            st.warning("⚠️ 예측을 위한 데이터가 부족합니다.")
            return

        # 차트 데이터 준비
        months_labels = [f['prediction_month'] for f in forecasts]
        predicted_values = [f['predicted_loss_rate'] for f in forecasts]
        ci_lower = [f['confidence_interval_lower'] for f in forecasts]
        ci_upper = [f['confidence_interval_upper'] for f in forecasts]

        # Plotly 차트 생성
        fig = go.Figure()

        # 예측값
        fig.add_trace(go.Scatter(
            x=months_labels,
            y=predicted_values,
            mode='lines+markers',
            name='예측 손실률',
            line=dict(color='#E74C3C', width=3),
            marker=dict(size=10)
        ))

        # 신뢰구간
        fig.add_trace(go.Scatter(
            x=months_labels + months_labels[::-1],
            y=ci_upper + ci_lower[::-1],
            fill='toself',
            fillcolor='rgba(231, 76, 60, 0.2)',
            line=dict(color='rgba(255, 255, 255, 0)'),
            showlegend=True,
            name='95% 신뢰구간'
        ))

        fig.update_layout(
            title=f'향후 {months}개월 손실률 예측',
            xaxis_title='예측 월',
            yaxis_title='손실률 (%)',
            hovermode='x unified',
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

        # 예측 상세 정보
        with st.expander("📊 예측 상세 정보"):
            for f in forecasts:
                st.write(f"**{f['prediction_month']}**")
                st.write(f"- 예측 손실률: {f['predicted_loss_rate']}%")
                st.write(f"- 신뢰구간: {f['confidence_interval_lower']}% ~ {f['confidence_interval_upper']}%")
                st.write(f"- 계절 지수: {f['seasonal_index']}")
                st.write(f"- 사용 데이터: {f['data_points_used']}개")
                st.divider()

    except ValueError as e:
        st.error(f"❌ 예측 실패: {e}")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
