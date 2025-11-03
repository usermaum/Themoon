"""
로스팅 기록 관리 페이지

단일 로스팅 기록의 입력, 조회, 편집, 삭제 및 통계 분석 기능 제공
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.services.roasting_service import RoastingService
from app.utils.database import get_db

# ═══════════════════════════════════════════════════════════════════════════════
# Session State 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if 'db' not in st.session_state:
    st.session_state.db = get_db()

if 'roasting_service' not in st.session_state:
    st.session_state.roasting_service = RoastingService

db = st.session_state.db
roasting_service = st.session_state.roasting_service

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.title("📊 로스팅 기록 관리")
st.markdown("로스팅 기록을 추가, 조회, 편집하고 손실률 통계를 분석합니다.")
st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 생성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 목록 조회",
    "➕ 기록 추가",
    "✏️ 기록 편집",
    "📊 통계 분석"
])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 목록 조회
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📋 로스팅 기록 목록")

    # 필터 옵션
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        date_filter = st.date_input(
            "조회 기간",
            value=(date.today() - timedelta(days=30), date.today()),
            max_value=date.today()
        )

    with col2:
        limit_count = st.selectbox(
            "표시 개수",
            options=[10, 30, 50, 100],
            index=0
        )

    with col3:
        sort_option = st.selectbox(
            "정렬 기준",
            options=["최신순", "오래된순", "손실률 높은순", "손실률 낮은순"]
        )

    st.divider()

    # 데이터 조회
    all_logs = roasting_service.get_all_logs(db, limit=limit_count)

    # 날짜 필터링
    if isinstance(date_filter, tuple) and len(date_filter) == 2:
        start_date, end_date = date_filter
        filtered_logs = [
            log for log in all_logs
            if start_date <= log.roasting_date <= end_date
        ]
    else:
        filtered_logs = all_logs

    # 정렬
    if sort_option == "최신순":
        filtered_logs.sort(key=lambda x: x.roasting_date, reverse=True)
    elif sort_option == "오래된순":
        filtered_logs.sort(key=lambda x: x.roasting_date)
    elif sort_option == "손실률 높은순":
        filtered_logs.sort(key=lambda x: x.loss_rate_percent, reverse=True)
    elif sort_option == "손실률 낮은순":
        filtered_logs.sort(key=lambda x: x.loss_rate_percent)

    # 통계 카드
    if filtered_logs:
        col1, col2, col3, col4 = st.columns(4)

        total_count = len(filtered_logs)
        total_raw = sum(log.raw_weight_kg for log in filtered_logs)
        total_roasted = sum(log.roasted_weight_kg for log in filtered_logs)
        avg_loss_rate = sum(log.loss_rate_percent for log in filtered_logs) / total_count

        with col1:
            st.metric("📊 총 기록 수", f"{total_count}건")

        with col2:
            st.metric("⚖️ 총 생두 투입", f"{total_raw:.1f}kg")

        with col3:
            st.metric("📦 총 로스팅 후", f"{total_roasted:.1f}kg")

        with col4:
            st.metric("📉 평균 손실률", f"{avg_loss_rate:.2f}%")

        st.divider()

        # 데이터 테이블
        st.markdown("#### 📄 상세 기록")

        # DataFrame 생성
        data = []
        for log in filtered_logs:
            # 손실률 차이에 따른 상태 표시
            variance = log.loss_variance_percent
            if abs(variance) <= 3.0:
                status = "🟢"
            elif abs(variance) <= 5.0:
                status = "🟡"
            else:
                status = "🔴"

            data.append({
                "ID": log.id,
                "날짜": log.roasting_date.strftime("%Y-%m-%d"),
                "생두(kg)": f"{log.raw_weight_kg:.2f}",
                "로스팅후(kg)": f"{log.roasted_weight_kg:.2f}",
                "손실률(%)": f"{log.loss_rate_percent:.2f}%",
                "차이(%)": f"{variance:+.2f}%",
                "상태": status,
                "메모": log.notes or "-"
            })

        df = pd.DataFrame(data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # 범례
        st.caption("🟢 정상 (±3% 이내) | 🟡 주의 (±3~5%) | 🔴 위험 (±5% 초과)")

    else:
        st.info("조회된 로스팅 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 기록 추가
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### ➕ 새 로스팅 기록 추가")

    with st.form("add_roasting_form"):
        col1, col2 = st.columns(2)

        with col1:
            roasting_date = st.date_input(
                "📅 로스팅 날짜",
                value=date.today(),
                max_value=date.today()
            )

            raw_weight_kg = st.number_input(
                "⚖️ 생두 무게 (kg)",
                min_value=0.1,
                max_value=100.0,
                value=10.0,
                step=0.1,
                format="%.2f"
            )

            roasted_weight_kg = st.number_input(
                "⚖️ 로스팅 후 무게 (kg)",
                min_value=0.1,
                max_value=100.0,
                value=8.3,
                step=0.1,
                format="%.2f"
            )

        with col2:
            expected_loss_rate = st.number_input(
                "📊 예상 손실률 (%)",
                min_value=0.0,
                max_value=50.0,
                value=17.0,
                step=0.1,
                format="%.1f"
            )

            notes = st.text_area(
                "📝 메모 (선택)",
                max_chars=500,
                height=100,
                placeholder="로스팅 관련 메모를 입력하세요..."
            )

        # 실시간 계산 결과 표시
        if raw_weight_kg > 0:
            actual_loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100
            loss_variance = actual_loss_rate - expected_loss_rate

            # 상태 판정
            if abs(loss_variance) <= 3.0:
                status_color = "🟢"
                status_text = "정상"
            elif abs(loss_variance) <= 5.0:
                status_color = "🟡"
                status_text = "주의"
            else:
                status_color = "🔴"
                status_text = "위험"

            st.divider()
            st.markdown("#### 💡 실시간 계산 결과")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("실제 손실률", f"{actual_loss_rate:.2f}%")
            with col2:
                st.metric("손실률 차이", f"{loss_variance:+.2f}%")
            with col3:
                st.metric("상태", f"{status_color} {status_text}")

        st.divider()

        # 제출 버튼
        col1, col2 = st.columns([3, 1])
        with col1:
            submit = st.form_submit_button("✅ 기록 저장", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("🔄 초기화", use_container_width=True):
                st.rerun()

        # 저장 처리
        if submit:
            # 검증
            errors = []

            if roasted_weight_kg >= raw_weight_kg:
                errors.append("⚠️ 로스팅 후 무게는 생두 무게보다 작아야 합니다.")

            if raw_weight_kg <= 0:
                errors.append("⚠️ 생두 무게는 0보다 커야 합니다.")

            if roasted_weight_kg <= 0:
                errors.append("⚠️ 로스팅 후 무게는 0보다 커야 합니다.")

            if roasting_date > date.today():
                errors.append("⚠️ 미래 날짜는 선택할 수 없습니다.")

            # 오류가 있으면 표시
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # 저장
                try:
                    log = roasting_service.create_roasting_log(
                        db=db,
                        raw_weight_kg=raw_weight_kg,
                        roasted_weight_kg=roasted_weight_kg,
                        roasting_date=roasting_date,
                        notes=notes if notes else None,
                        expected_loss_rate=expected_loss_rate
                    )

                    st.success(f"✅ 로스팅 기록이 저장되었습니다! (ID: {log.id})")

                    # 손실률 경고 확인
                    if abs(log.loss_variance_percent) > 3.0:
                        severity = "CRITICAL" if abs(log.loss_variance_percent) > 5.0 else "WARNING"
                        st.warning(
                            f"⚠️ 손실률이 예상보다 {abs(log.loss_variance_percent):.2f}% "
                            f"{'높습니다' if log.loss_variance_percent > 0 else '낮습니다'} ({severity})"
                        )

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 기록 편집
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### ✏️ 로스팅 기록 편집")

    # 편집할 기록 조회 (최근 30건)
    all_logs = roasting_service.get_all_logs(db, limit=30)

    if all_logs:
        # 선택 옵션 생성
        log_options = {}
        for log in all_logs:
            option_text = f"{log.roasting_date.strftime('%Y-%m-%d')} - {log.raw_weight_kg:.2f}kg ({log.loss_rate_percent:.2f}%)"
            log_options[option_text] = log.id

        selected_option = st.selectbox(
            "편집할 기록 선택",
            options=list(log_options.keys())
        )

        if selected_option:
            selected_log_id = log_options[selected_option]
            selected_log = roasting_service.get_roasting_log_by_id(db, selected_log_id)

            if selected_log:
                # 현재 기록 정보 표시
                st.info(
                    f"**현재 기록**: {selected_log.roasting_date.strftime('%Y-%m-%d')} | "
                    f"생두: {selected_log.raw_weight_kg}kg → 로스팅후: {selected_log.roasted_weight_kg}kg | "
                    f"손실률: {selected_log.loss_rate_percent}% (예상: {selected_log.expected_loss_rate_percent}%)"
                )

                st.divider()

                # 편집 폼
                with st.form("edit_roasting_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        new_roasting_date = st.date_input(
                            "📅 로스팅 날짜",
                            value=selected_log.roasting_date,
                            max_value=date.today()
                        )

                        new_raw_weight_kg = st.number_input(
                            "⚖️ 생두 무게 (kg)",
                            min_value=0.1,
                            max_value=100.0,
                            value=float(selected_log.raw_weight_kg),
                            step=0.1,
                            format="%.2f"
                        )

                        new_roasted_weight_kg = st.number_input(
                            "⚖️ 로스팅 후 무게 (kg)",
                            min_value=0.1,
                            max_value=100.0,
                            value=float(selected_log.roasted_weight_kg),
                            step=0.1,
                            format="%.2f"
                        )

                    with col2:
                        new_expected_loss_rate = st.number_input(
                            "📊 예상 손실률 (%)",
                            min_value=0.0,
                            max_value=50.0,
                            value=float(selected_log.expected_loss_rate_percent),
                            step=0.1,
                            format="%.1f"
                        )

                        new_notes = st.text_area(
                            "📝 메모 (선택)",
                            value=selected_log.notes or "",
                            max_chars=500,
                            height=100
                        )

                    # 실시간 계산 결과
                    if new_raw_weight_kg > 0:
                        new_actual_loss_rate = ((new_raw_weight_kg - new_roasted_weight_kg) / new_raw_weight_kg) * 100
                        new_loss_variance = new_actual_loss_rate - new_expected_loss_rate

                        # 상태 판정
                        if abs(new_loss_variance) <= 3.0:
                            status_color = "🟢"
                            status_text = "정상"
                        elif abs(new_loss_variance) <= 5.0:
                            status_color = "🟡"
                            status_text = "주의"
                        else:
                            status_color = "🔴"
                            status_text = "위험"

                        st.divider()
                        st.markdown("#### 💡 수정 후 계산 결과")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("실제 손실률", f"{new_actual_loss_rate:.2f}%")
                        with col2:
                            st.metric("손실률 차이", f"{new_loss_variance:+.2f}%")
                        with col3:
                            st.metric("상태", f"{status_color} {status_text}")

                    st.divider()

                    # 저장 버튼
                    if st.form_submit_button("✅ 저장", use_container_width=True, type="primary"):
                        # 검증
                        errors = []

                        if new_roasted_weight_kg >= new_raw_weight_kg:
                            errors.append("⚠️ 로스팅 후 무게는 생두 무게보다 작아야 합니다.")

                        if new_raw_weight_kg <= 0:
                            errors.append("⚠️ 생두 무게는 0보다 커야 합니다.")

                        if new_roasted_weight_kg <= 0:
                            errors.append("⚠️ 로스팅 후 무게는 0보다 커야 합니다.")

                        if new_roasting_date > date.today():
                            errors.append("⚠️ 미래 날짜는 선택할 수 없습니다.")

                        # 오류가 있으면 표시
                        if errors:
                            for error in errors:
                                st.error(error)
                        else:
                            # 저장
                            try:
                                # 손실률 재계산
                                new_loss_rate = ((new_raw_weight_kg - new_roasted_weight_kg) / new_raw_weight_kg) * 100
                                new_variance = new_loss_rate - new_expected_loss_rate

                                roasting_service.update_roasting_log(
                                    db=db,
                                    log_id=selected_log.id,
                                    raw_weight_kg=new_raw_weight_kg,
                                    roasted_weight_kg=new_roasted_weight_kg,
                                    loss_rate_percent=round(new_loss_rate, 2),
                                    expected_loss_rate_percent=new_expected_loss_rate,
                                    loss_variance_percent=round(new_variance, 2),
                                    roasting_date=new_roasting_date,
                                    roasting_month=new_roasting_date.strftime('%Y-%m'),
                                    notes=new_notes if new_notes else None
                                )

                                st.success("✅ 로스팅 기록이 업데이트되었습니다!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")

                # 삭제 버튼 (form 외부)
                st.divider()
                st.markdown("#### 🗑️ 위험한 작업")

                if st.button("🗑️ 이 기록 삭제", use_container_width=True, type="secondary"):
                    try:
                        success = roasting_service.delete_roasting_log(db, selected_log.id)
                        if success:
                            st.success("✅ 로스팅 기록이 삭제되었습니다.")
                            st.rerun()
                        else:
                            st.error("❌ 기록을 찾을 수 없습니다.")
                    except Exception as e:
                        st.error(f"❌ 삭제 중 오류가 발생했습니다: {str(e)}")

    else:
        st.info("편집할 로스팅 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 통계 분석
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### 📊 로스팅 통계 분석")

    # 월 선택
    selected_month_date = st.date_input(
        "조회 월 선택",
        value=date.today(),
        max_value=date.today()
    )

    # YYYY-MM 형식으로 변환
    selected_month = selected_month_date.strftime('%Y-%m')

    st.divider()

    # 월별 통계 조회
    monthly_stats = roasting_service.get_monthly_statistics(db, selected_month)

    if monthly_stats['status'] == "데이터 없음":
        st.info(f"{selected_month}에 로스팅 기록이 없습니다.")
    else:
        # 통계 카드
        st.markdown("#### 📈 월별 요약")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 총 로스팅 횟수", f"{monthly_stats['total_logs']}회")

        with col2:
            st.metric("⚖️ 총 생두 투입", f"{monthly_stats['total_raw_weight_kg']}kg")

        with col3:
            st.metric("📦 총 로스팅 후", f"{monthly_stats['total_roasted_weight_kg']}kg")

        with col4:
            st.metric("📉 평균 손실률", f"{monthly_stats['avg_loss_rate_percent']:.2f}%")

        st.divider()

        # 손실량 및 예상 대비 차이
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🔺 총 손실량",
                f"{monthly_stats['total_loss_kg']:.2f}kg",
                delta=f"{monthly_stats['total_loss_kg'] / monthly_stats['total_raw_weight_kg'] * 100:.1f}%"
            )

        with col2:
            variance_value = monthly_stats['variance_from_expected']
            st.metric(
                "📊 예상 대비 차이",
                f"{variance_value:+.2f}%",
                delta=f"{'높음' if variance_value > 0 else '낮음'}" if variance_value != 0 else "정상"
            )

        st.divider()

        # 날짜별 손실률 추이 그래프
        st.markdown("#### 📈 날짜별 손실률 추이")

        logs = roasting_service.get_roasting_logs_by_month(db, selected_month)

        if logs:
            # DataFrame 생성
            chart_data = pd.DataFrame({
                "날짜": [log.roasting_date for log in logs],
                "손실률(%)": [log.loss_rate_percent for log in logs],
                "예상 손실률(%)": [log.expected_loss_rate_percent for log in logs]
            })

            chart_data = chart_data.set_index("날짜")

            st.line_chart(chart_data)

            # 상세 데이터 테이블
            st.markdown("#### 📄 상세 기록")

            data = []
            for log in logs:
                variance = log.loss_variance_percent
                if abs(variance) <= 3.0:
                    status = "🟢"
                elif abs(variance) <= 5.0:
                    status = "🟡"
                else:
                    status = "🔴"

                data.append({
                    "날짜": log.roasting_date.strftime("%Y-%m-%d"),
                    "생두(kg)": f"{log.raw_weight_kg:.2f}",
                    "로스팅후(kg)": f"{log.roasted_weight_kg:.2f}",
                    "손실률(%)": f"{log.loss_rate_percent:.2f}%",
                    "예상(%)": f"{log.expected_loss_rate_percent:.1f}%",
                    "차이(%)": f"{variance:+.2f}%",
                    "상태": status
                })

            df = pd.DataFrame(data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.caption("🟢 정상 (±3% 이내) | 🟡 주의 (±3~5%) | 🔴 위험 (±5% 초과)")

        else:
            st.info("해당 월의 로스팅 기록이 없습니다.")
