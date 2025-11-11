"""
📊 분석 보고서 페이지 (Phase 5)
월별 리포트, 수익성 분석, 데이터 다운로드
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.report_service import ReportService
from utils.export_utils import dataframe_to_excel, dataframe_to_csv


def main():
    """분석 보고서 메인 페이지"""
    st.title("📊 분석 보고서")
    st.markdown("월별 거래 리포트, 원두별 수익성 분석, 데이터 다운로드")

    # DB 연결
    if "db" not in st.session_state:
        st.error("❌ 데이터베이스 연결이 필요합니다.")
        return

    db = st.session_state.db
    report_service = ReportService(db)

    # 탭 생성
    tab1, tab2, tab3 = st.tabs([
        "📈 월별 리포트",
        "💰 수익성 분석",
        "📥 데이터 다운로드"
    ])

    # Tab 1: 월별 리포트
    with tab1:
        render_monthly_report_tab(report_service)

    # Tab 2: 수익성 분석
    with tab2:
        render_profitability_tab(report_service)

    # Tab 3: 데이터 다운로드
    with tab3:
        render_download_tab(report_service)


def render_monthly_report_tab(report_service: ReportService):
    """Tab 1: 월별 리포트"""
    st.subheader("📈 월별 거래 리포트")

    # 조회 기간 선택
    col1, col2 = st.columns(2)

    with col1:
        # 최근 12개월 목록 생성
        today = date.today()
        months_list = []
        for i in range(12):
            month_date = today - relativedelta(months=i)
            months_list.append((month_date.year, month_date.month, f"{month_date.year}년 {month_date.month}월"))

        selected_option = st.selectbox(
            "조회 월 선택",
            options=range(len(months_list)),
            format_func=lambda x: months_list[x][2],
            index=0
        )

        selected_year, selected_month, _ = months_list[selected_option]

    with col2:
        # 보고서 유형 (향후 확장 가능)
        report_type = st.selectbox(
            "보고서 유형",
            options=["전체", "원두별"],
            index=0
        )

    # 리포트 데이터 조회
    try:
        report_data = report_service.get_monthly_transactions_report(selected_year, selected_month)

        # 1. 요약 통계 메트릭
        st.markdown("### 📊 월별 요약 통계")

        summary = report_data['summary']
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "총 입고량",
                f"{summary.get('총 입고량 (kg)', 0):.2f} kg",
                help="PURCHASE, PRODUCTION, ADJUSTMENT(+) 합계"
            )

        with col2:
            st.metric(
                "총 출고량",
                f"{summary.get('총 출고량 (kg)', 0):.2f} kg",
                help="SALES, GIFT, WASTE, ADJUSTMENT(-) 합계"
            )

        with col3:
            st.metric(
                "로스팅 횟수",
                f"{summary.get('로스팅 횟수', 0)}회",
                help="ROASTING 거래 횟수"
            )

        with col4:
            net_change = summary.get('재고 증감 (kg)', 0)
            delta_color = "normal" if net_change >= 0 else "inverse"
            st.metric(
                "재고 증감",
                f"{net_change:+.2f} kg",
                delta=f"{net_change:+.2f} kg",
                help="입고량 - 출고량"
            )

        st.divider()

        # 2. 일별 추이 그래프
        st.markdown("### 📉 일별 입출고 추이")

        daily_trend_df = report_data['daily_trend']

        if not daily_trend_df.empty and len(daily_trend_df) > 0:
            # Plotly Line Chart
            fig = go.Figure()

            # 날짜 컬럼 제외한 모든 거래 유형 컬럼 추가
            for col in daily_trend_df.columns:
                if col != '날짜':
                    fig.add_trace(go.Scatter(
                        x=daily_trend_df['날짜'],
                        y=daily_trend_df[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(width=2),
                        marker=dict(size=6)
                    ))

            fig.update_layout(
                xaxis_title="날짜",
                yaxis_title="수량 (kg)",
                hovermode='x unified',
                height=400,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 해당 월에 거래 내역이 없습니다.")

        st.divider()

        # 3. 거래 유형별 분류 테이블
        st.markdown("### 📋 거래 유형별 통계")

        transaction_type_df = report_data['transaction_type']

        if not transaction_type_df.empty:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.dataframe(
                    transaction_type_df,
                    use_container_width=True,
                    hide_index=True
                )

            with col2:
                # 파이 차트
                if len(transaction_type_df) > 0:
                    fig_pie = px.pie(
                        transaction_type_df,
                        values='수량(kg)',
                        names='거래 유형',
                        title='거래 유형별 비율'
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📭 거래 유형별 데이터가 없습니다.")

    except Exception as e:
        st.error(f"❌ 리포트 생성 중 오류 발생: {str(e)}")
        st.exception(e)


def render_profitability_tab(report_service: ReportService):
    """Tab 2: 수익성 분석"""
    st.subheader("💰 원두별 수익성 분석")

    # 분석 기간 선택
    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input(
            "시작일",
            value=date.today() - timedelta(days=30),
            max_value=date.today()
        )

    with col2:
        end_date = st.date_input(
            "종료일",
            value=date.today(),
            max_value=date.today()
        )

    with col3:
        sort_by = st.selectbox(
            "정렬 기준",
            options=['profit_rate', 'total_cost', 'roasting_count'],
            format_func=lambda x: {
                'profit_rate': '수익률',
                'total_cost': '총 비용',
                'roasting_count': '로스팅 횟수'
            }[x],
            index=0
        )

    if start_date > end_date:
        st.warning("⚠️ 시작일은 종료일보다 이전이어야 합니다.")
        return

    # 수익성 분석 데이터 조회
    try:
        df = report_service.get_profitability_by_bean(
            start_date=start_date,
            end_date=end_date,
            sort_by=sort_by
        )

        if df.empty:
            st.info("📭 선택한 기간에 로스팅 기록이 없습니다.")
            return

        # 1. 전체 요약 메트릭
        st.markdown("### 📊 전체 수익 요약")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_purchase = df['매입비용(원)'].sum()
            st.metric(
                "총 매입 비용",
                f"₩{total_purchase:,.0f}",
                help="모든 원두의 매입 비용 합계"
            )

        with col2:
            total_roasting = df['로스팅비용(원)'].sum()
            st.metric(
                "총 로스팅 비용",
                f"₩{total_roasting:,.0f}",
                help="모든 원두의 로스팅 비용 합계"
            )

        with col3:
            avg_profit_rate = df['수익률(%)'].mean()
            st.metric(
                "평균 수익률",
                f"{avg_profit_rate:.2f}%",
                delta=f"{avg_profit_rate:.2f}%",
                help="모든 원두의 평균 수익률"
            )

        st.divider()

        # 2. 원두별 수익성 테이블
        st.markdown("### 📋 원두별 상세 분석")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=400
        )

        st.caption(f"📄 총 {len(df)}개 원두 | 기간: {start_date} ~ {end_date}")

        st.divider()

        # 3. 수익률 순위 바 차트
        st.markdown("### 📊 수익률 순위")

        # 상위/하위 5개만 표시
        top_5 = df.head(5)
        bottom_5 = df.tail(5)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🟢 상위 5개 원두")
            if not top_5.empty:
                fig_top = go.Figure(go.Bar(
                    x=top_5['수익률(%)'],
                    y=top_5['원두명'],
                    orientation='h',
                    marker=dict(
                        color=top_5['수익률(%)'],
                        colorscale='Greens',
                        showscale=False
                    ),
                    text=top_5['수익률(%)'].apply(lambda x: f"{x:.2f}%"),
                    textposition='auto'
                ))
                fig_top.update_layout(
                    xaxis_title="수익률 (%)",
                    yaxis_title="",
                    height=300
                )
                st.plotly_chart(fig_top, use_container_width=True)

        with col2:
            st.markdown("#### 🔴 하위 5개 원두")
            if not bottom_5.empty:
                fig_bottom = go.Figure(go.Bar(
                    x=bottom_5['수익률(%)'],
                    y=bottom_5['원두명'],
                    orientation='h',
                    marker=dict(
                        color=bottom_5['수익률(%)'],
                        colorscale='Reds',
                        showscale=False
                    ),
                    text=bottom_5['수익률(%)'].apply(lambda x: f"{x:.2f}%"),
                    textposition='auto'
                ))
                fig_bottom.update_layout(
                    xaxis_title="수익률 (%)",
                    yaxis_title="",
                    height=300
                )
                st.plotly_chart(fig_bottom, use_container_width=True)

        # 도움말
        with st.expander("ℹ️ 수익률 계산 방법"):
            st.markdown("""
            **수익률 계산 공식 (간이 계산)**:
            ```
            수익률(%) = -(손실률%)
            손실률(%) = (1 - 산출량/매입량) × 100
            ```

            **해석**:
            - **양수 (예: +5%)**: 손실률이 낮아 효율적 (실제로는 손실이 있지만 상대적으로 낮음)
            - **음수 (예: -18%)**: 손실률이 높아 비효율적

            **참고**: 실제 수익률은 판매가격을 고려해야 정확하지만,
            여기서는 손실률 역수로 간이 계산합니다.
            """)

    except Exception as e:
        st.error(f"❌ 수익성 분석 중 오류 발생: {str(e)}")
        st.exception(e)


def render_download_tab(report_service: ReportService):
    """Tab 3: 데이터 다운로드"""
    st.subheader("📥 데이터 다운로드")
    st.markdown("로스팅 기록, 재고 현황, 거래 내역을 Excel/CSV로 다운로드하세요.")

    # 1. 로스팅 기록 다운로드
    st.markdown("### 🔥 로스팅 기록 다운로드")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        roasting_start = st.date_input(
            "시작일",
            value=date.today() - timedelta(days=30),
            max_value=date.today(),
            key="roasting_start"
        )

    with col2:
        roasting_end = st.date_input(
            "종료일",
            value=date.today(),
            max_value=date.today(),
            key="roasting_end"
        )

    with col3:
        roasting_format = st.selectbox(
            "형식",
            options=["Excel", "CSV"],
            key="roasting_format"
        )

    if st.button("📥 로스팅 기록 다운로드", key="download_roasting"):
        try:
            df = report_service.get_roasting_logs_dataframe(roasting_start, roasting_end)

            if df.empty:
                st.warning("📭 선택한 기간에 로스팅 기록이 없습니다.")
            else:
                if roasting_format == "Excel":
                    excel_file = dataframe_to_excel(df, sheet_name="로스팅기록")
                    st.download_button(
                        label="📥 Excel 파일 다운로드",
                        data=excel_file,
                        file_name=f"로스팅기록_{roasting_start}_{roasting_end}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    csv_file = dataframe_to_csv(df)
                    st.download_button(
                        label="📥 CSV 파일 다운로드",
                        data=csv_file,
                        file_name=f"로스팅기록_{roasting_start}_{roasting_end}.csv",
                        mime="text/csv"
                    )

                st.success(f"✅ {len(df)}건의 로스팅 기록을 준비했습니다.")

        except Exception as e:
            st.error(f"❌ 다운로드 중 오류 발생: {str(e)}")

    st.divider()

    # 2. 재고 현황 다운로드
    st.markdown("### 📦 재고 현황 다운로드")

    col1, col2 = st.columns([3, 1])

    with col2:
        inventory_format = st.selectbox(
            "형식",
            options=["Excel", "CSV"],
            key="inventory_format"
        )

    if st.button("📥 재고 현황 다운로드", key="download_inventory"):
        try:
            df = report_service.get_inventory_dataframe()

            if df.empty:
                st.warning("📭 재고 데이터가 없습니다.")
            else:
                if inventory_format == "Excel":
                    excel_file = dataframe_to_excel(df, sheet_name="재고현황")
                    st.download_button(
                        label="📥 Excel 파일 다운로드",
                        data=excel_file,
                        file_name=f"재고현황_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    csv_file = dataframe_to_csv(df)
                    st.download_button(
                        label="📥 CSV 파일 다운로드",
                        data=csv_file,
                        file_name=f"재고현황_{date.today()}.csv",
                        mime="text/csv"
                    )

                st.success(f"✅ {len(df)}건의 재고 데이터를 준비했습니다.")

        except Exception as e:
            st.error(f"❌ 다운로드 중 오류 발생: {str(e)}")

    st.divider()

    # 3. 입출고 거래 내역 다운로드
    st.markdown("### 📊 입출고 거래 내역 다운로드")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        transaction_start = st.date_input(
            "시작일",
            value=date.today() - timedelta(days=30),
            max_value=date.today(),
            key="transaction_start"
        )

    with col2:
        transaction_end = st.date_input(
            "종료일",
            value=date.today(),
            max_value=date.today(),
            key="transaction_end"
        )

    with col3:
        transaction_format = st.selectbox(
            "형식",
            options=["Excel", "CSV"],
            key="transaction_format"
        )

    # 거래 유형 필터
    transaction_types = st.multiselect(
        "거래 유형 필터 (선택 안 하면 전체)",
        options=['PURCHASE', 'ROASTING', 'PRODUCTION', 'SALES', 'GIFT', 'WASTE', 'ADJUSTMENT'],
        default=None,
        key="transaction_types_filter"
    )

    if st.button("📥 거래 내역 다운로드", key="download_transactions"):
        try:
            df = report_service.get_transactions_dataframe(
                transaction_start,
                transaction_end,
                transaction_types if transaction_types else None
            )

            if df.empty:
                st.warning("📭 선택한 조건에 맞는 거래 내역이 없습니다.")
            else:
                if transaction_format == "Excel":
                    excel_file = dataframe_to_excel(df, sheet_name="거래내역")
                    st.download_button(
                        label="📥 Excel 파일 다운로드",
                        data=excel_file,
                        file_name=f"거래내역_{transaction_start}_{transaction_end}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    csv_file = dataframe_to_csv(df)
                    st.download_button(
                        label="📥 CSV 파일 다운로드",
                        data=csv_file,
                        file_name=f"거래내역_{transaction_start}_{transaction_end}.csv",
                        mime="text/csv"
                    )

                st.success(f"✅ {len(df)}건의 거래 내역을 준비했습니다.")

        except Exception as e:
            st.error(f"❌ 다운로드 중 오류 발생: {str(e)}")

    st.divider()

    # 4. 월별 종합 리포트 다운로드
    st.markdown("### 📑 월별 종합 리포트 다운로드 (Excel)")
    st.caption("요약, 일별 추이, 거래 유형별, 전체 거래 내역을 포함한 다중 시트 Excel 파일")

    col1, col2 = st.columns([3, 1])

    with col1:
        # 최근 12개월 목록
        today = date.today()
        months_list = []
        for i in range(12):
            month_date = today - relativedelta(months=i)
            months_list.append((month_date.year, month_date.month, f"{month_date.year}년 {month_date.month}월"))

        selected_month_idx = st.selectbox(
            "조회 월 선택",
            options=range(len(months_list)),
            format_func=lambda x: months_list[x][2],
            index=0,
            key="monthly_report_month"
        )

        report_year, report_month, _ = months_list[selected_month_idx]

    if st.button("📥 월별 종합 리포트 다운로드", key="download_monthly_report"):
        try:
            excel_file = report_service.generate_monthly_excel(report_year, report_month)

            st.download_button(
                label="📥 Excel 파일 다운로드 (다중 시트)",
                data=excel_file,
                file_name=f"월별종합리포트_{report_year}년{report_month}월.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.success(f"✅ {report_year}년 {report_month}월 종합 리포트를 준비했습니다.")

        except Exception as e:
            st.error(f"❌ 리포트 생성 중 오류 발생: {str(e)}")


# 페이지 실행
if __name__ == "__main__":
    main()
