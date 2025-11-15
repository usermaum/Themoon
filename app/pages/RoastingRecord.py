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

from services.roasting_service import RoastingService
from services.bean_service import BeanService
from services.blend_service import BlendService
from app.models import SessionLocal
from app.components.sidebar import render_sidebar
from app.i18n import Translator, LanguageManager

# ═══════════════════════════════════════════════════════════════════════════════
# Session State 초기화
# ═══════════════════════════════════════════════════════════════════════════════

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 데이터베이스 및 서비스 초기화
if 'db' not in st.session_state:
    st.session_state.db = SessionLocal()

if 'bean_service' not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

if 'blend_service' not in st.session_state:
    st.session_state.blend_service = BlendService(st.session_state.db)

if 'roasting_service' not in st.session_state:
    st.session_state.roasting_service = RoastingService

db = st.session_state.db
roasting_service = st.session_state.roasting_service
bean_service = st.session_state.bean_service

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바 렌더링
# ═══════════════════════════════════════════════════════════════════════════════

render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 헤더
# ═══════════════════════════════════════════════════════════════════════════════

# 현재 페이지 설정 (사이드바 활성 표시)
st.session_state["current_page"] = "RoastingRecord"

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

    # 페이징 설정 초기화
    if 'roasting_page_number' not in st.session_state:
        st.session_state.roasting_page_number = 1
    if 'roasting_page_size' not in st.session_state:
        st.session_state.roasting_page_size = 10

    # 필터 및 페이징 옵션
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        # 조회 기간 선택
        period_option = st.selectbox(
            "조회 기간",
            options=["전체", "날짜조회", "오늘", "1개월", "3개월", "6개월", "1년"],
            key="period_selector"
        )

        # "날짜조회" 선택 시에만 date_input 표시
        if period_option == "날짜조회":
            date_filter = st.date_input(
                "날짜 범위 선택",
                value=(date.today() - timedelta(days=30), date.today()),
                max_value=date.today(),
                key="custom_date_filter"
            )
        else:
            date_filter = None

    with col2:
        sort_option = st.selectbox(
            "정렬 기준",
            options=["최신순", "오래된순", "손실률 높은순", "손실률 낮은순"]
        )

    with col3:
        page_size = st.selectbox(
            "페이지당 표시 개수",
            options=[10, 25, 50, 100],
            index=[10, 25, 50, 100].index(st.session_state.roasting_page_size),
            key="page_size_selector"
        )
        # 페이지 크기가 변경되면 첫 페이지로 이동
        if page_size != st.session_state.roasting_page_size:
            st.session_state.roasting_page_size = page_size
            st.session_state.roasting_page_number = 1

    st.divider()

    # 데이터 조회 (전체 데이터)
    all_logs = roasting_service.get_all_logs(db)

    # 날짜 필터링
    if period_option == "전체":
        # 모든 데이터 표시
        filtered_logs = all_logs
    elif period_option == "날짜조회":
        # 사용자가 선택한 날짜 범위
        if isinstance(date_filter, tuple) and len(date_filter) == 2:
            start_date, end_date = date_filter
            filtered_logs = [
                log for log in all_logs
                if start_date <= log.roasting_date <= end_date
            ]
        else:
            filtered_logs = all_logs
    elif period_option == "오늘":
        # 오늘 날짜만
        today = date.today()
        filtered_logs = [
            log for log in all_logs
            if log.roasting_date == today
        ]
    elif period_option == "1개월":
        # 최근 1개월
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        filtered_logs = [
            log for log in all_logs
            if start_date <= log.roasting_date <= end_date
        ]
    elif period_option == "3개월":
        # 최근 3개월
        start_date = date.today() - timedelta(days=90)
        end_date = date.today()
        filtered_logs = [
            log for log in all_logs
            if start_date <= log.roasting_date <= end_date
        ]
    elif period_option == "6개월":
        # 최근 6개월
        start_date = date.today() - timedelta(days=180)
        end_date = date.today()
        filtered_logs = [
            log for log in all_logs
            if start_date <= log.roasting_date <= end_date
        ]
    elif period_option == "1년":
        # 최근 1년
        start_date = date.today() - timedelta(days=365)
        end_date = date.today()
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

        # DataFrame 생성 (전체 데이터)
        data = []
        for log in filtered_logs:
            # 원두 이름 조회
            bean_name = "-"
            if log.bean_id:
                bean = bean_service.get_bean_by_id(log.bean_id)
                if bean:
                    bean_name = f"{bean.name}"

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
                "원두": bean_name,
                "생두(kg)": f"{log.raw_weight_kg:.2f}",
                "로스팅후(kg)": f"{log.roasted_weight_kg:.2f}",
                "손실률(%)": f"{log.loss_rate_percent:.2f}%",
                "차이(%)": f"{variance:+.2f}%",
                "상태": status,
                "메모": log.notes or "-"
            })

        df = pd.DataFrame(data)

        # 페이징 처리
        total_records = len(df)
        total_pages = (total_records + page_size - 1) // page_size  # 올림 계산

        # 페이지 번호가 범위를 벗어나면 조정
        if st.session_state.roasting_page_number > total_pages:
            st.session_state.roasting_page_number = total_pages if total_pages > 0 else 1

        # 현재 페이지 데이터 추출
        start_idx = (st.session_state.roasting_page_number - 1) * page_size
        end_idx = start_idx + page_size
        df_page = df.iloc[start_idx:end_idx]

        # 페이지 데이터 표시
        st.dataframe(
            df_page,
            use_container_width=True,
            hide_index=True,
            height=400
        )

        # 페이징 컨트롤 (모바일 최적화)
        # 페이지 정보 상단 표시
        st.caption(f"📄 {st.session_state.roasting_page_number} / {total_pages} 페이지 (전체 {total_records}건)")

        # 페이징 버튼 (3개 컬럼으로 간소화)
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("◀️ 이전", disabled=(st.session_state.roasting_page_number == 1), use_container_width=True, key="prev_page"):
                st.session_state.roasting_page_number -= 1
                st.rerun()

        with col2:
            # 페이지 번호 직접 입력
            new_page = st.number_input(
                "페이지 이동",
                min_value=1,
                max_value=total_pages,
                value=st.session_state.roasting_page_number,
                step=1,
                label_visibility="collapsed",
                key="page_number_input"
            )
            if new_page != st.session_state.roasting_page_number:
                st.session_state.roasting_page_number = new_page
                st.rerun()

        with col3:
            if st.button("다음 ▶️", disabled=(st.session_state.roasting_page_number == total_pages), use_container_width=True, key="next_page"):
                st.session_state.roasting_page_number += 1
                st.rerun()

        st.divider()

        # 범례
        st.caption("🟢 정상 (±3% 이내) | 🟡 주의 (±3~5%) | 🔴 위험 (±5% 초과)")

    else:
        st.info("조회된 로스팅 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 기록 추가
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### ➕ 새 로스팅 기록 추가")

    # Session state 초기화
    if 'add_roasting_date' not in st.session_state:
        st.session_state.add_roasting_date = date.today()
    if 'add_bean_id' not in st.session_state:
        st.session_state.add_bean_id = None
    if 'add_raw_weight' not in st.session_state:
        st.session_state.add_raw_weight = 0.0
    if 'add_roasted_weight' not in st.session_state:
        st.session_state.add_roasted_weight = 0.0
    if 'add_notes' not in st.session_state:
        st.session_state.add_notes = ""

    # 원두 목록 조회
    all_beans = bean_service.get_all_beans()

    # 원두 선택 옵션 생성
    bean_options = {"선택 안함 (원두 미지정)": None}
    for bean in all_beans:
        bean_options[f"{bean.name} ({bean.country_name})"] = bean.id

    col1, col2 = st.columns(2)

    with col1:
        roasting_date = st.date_input(
            "📅 로스팅 날짜",
            value=st.session_state.add_roasting_date,
            max_value=date.today(),
            key="add_date_input"
        )
        st.session_state.add_roasting_date = roasting_date

        # 원두 선택
        selected_bean_option = st.selectbox(
            "☕ 원두 선택",
            options=list(bean_options.keys()),
            help="로스팅할 원두를 선택하세요",
            key="add_bean_select"
        )
        st.session_state.add_bean_id = bean_options[selected_bean_option]

        raw_weight_kg = st.number_input(
            "⚖️ 생두 무게 (kg)",
            min_value=0.0,
            max_value=10000.0,
            value=st.session_state.add_raw_weight,
            step=0.1,
            format="%.2f",
            help="생두 투입 무게를 입력하세요 (엔터 또는 포커스 아웃 시 자동 계산)",
            key="add_raw_weight_input"
        )
        st.session_state.add_raw_weight = raw_weight_kg

        roasted_weight_kg = st.number_input(
            "⚖️ 로스팅 후 무게 (kg)",
            min_value=0.0,
            max_value=10000.0,
            value=st.session_state.add_roasted_weight,
            step=0.1,
            format="%.2f",
            help="로스팅 후 무게를 입력하세요 (엔터 또는 포커스 아웃 시 자동 계산)",
            key="add_roasted_weight_input"
        )
        st.session_state.add_roasted_weight = roasted_weight_kg

    with col2:
        # 손실률 자동 계산 및 표시
        if raw_weight_kg > 0 and roasted_weight_kg > 0:
            calculated_loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100
        else:
            calculated_loss_rate = 0.0

        st.info(f"📊 **손실률 (자동 계산):** {calculated_loss_rate:.2f}%")
        st.caption("생두 무게와 로스팅 후 무게를 입력하면 자동으로 계산됩니다.")

        notes = st.text_area(
            "📝 메모 (선택)",
            value=st.session_state.add_notes,
            max_chars=500,
            height=100,
            placeholder="로스팅 관련 메모를 입력하세요...",
            key="add_notes_input"
        )
        st.session_state.add_notes = notes

    # 실시간 계산 결과 표시
    if raw_weight_kg > 0 and roasted_weight_kg > 0:
        actual_loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100
        expected_loss_rate = 17.0  # 기본 예상 손실률
        loss_variance = actual_loss_rate - expected_loss_rate

        # 상태 판정 (손실률이 낮을수록 좋음)
        if loss_variance <= 0:
            # 기준보다 낮음 (좋음)
            status_color = "🟢"
            status_text = "우수"
        elif loss_variance <= 3.0:
            # 기준 대비 +3% 이내 (정상)
            status_color = "🟢"
            status_text = "정상"
        elif loss_variance <= 5.0:
            # 기준 대비 +5% 이내 (주의)
            status_color = "🟡"
            status_text = "주의"
        else:
            # 기준 대비 +5% 초과 (위험)
            status_color = "🔴"
            status_text = "위험"

        st.divider()
        st.markdown("#### 💡 손실률 분석")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("계산된 손실률", f"{actual_loss_rate:.2f}%")
        with col2:
            st.metric("기준 대비 (17%)", f"{loss_variance:+.2f}%")
        with col3:
            st.metric("상태", f"{status_color} {status_text}")

    st.divider()

    # 제출 버튼
    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("✅ 기록 저장", use_container_width=True, type="primary", key="add_submit_button")
    with col2:
        if st.button("🔄 초기화", use_container_width=True, key="add_reset_button"):
            st.session_state.add_roasting_date = date.today()
            st.session_state.add_bean_id = None
            st.session_state.add_raw_weight = 0.0
            st.session_state.add_roasted_weight = 0.0
            st.session_state.add_notes = ""
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
            # 손실률 계산
            calculated_loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100

            # 저장
            try:
                log = roasting_service.create_roasting_log(
                    db=db,
                    raw_weight_kg=raw_weight_kg,
                    roasted_weight_kg=roasted_weight_kg,
                    roasting_date=roasting_date,
                    bean_id=st.session_state.add_bean_id,
                    notes=notes if notes else None,
                    expected_loss_rate=17.0  # 기본 예상 손실률
                )

                st.success(f"✅ 로스팅 기록이 저장되었습니다! (ID: {log.id})")

                # 손실률 경고 확인
                if abs(log.loss_variance_percent) > 3.0:
                    severity = "CRITICAL" if abs(log.loss_variance_percent) > 5.0 else "WARNING"
                    st.warning(
                        f"⚠️ 손실률이 예상보다 {abs(log.loss_variance_percent):.2f}% "
                        f"{'높습니다' if log.loss_variance_percent > 0 else '낮습니다'} ({severity})"
                    )

                # 초기화
                st.session_state.add_roasting_date = date.today()
                st.session_state.add_bean_id = None
                st.session_state.add_raw_weight = 0.0
                st.session_state.add_roasted_weight = 0.0
                st.session_state.add_notes = ""

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
                # 원두 이름 표시 (있을 경우)
                bean_name = ""
                if selected_log.bean_id:
                    bean = bean_service.get_bean_by_id(selected_log.bean_id)
                    if bean:
                        bean_name = f" | 원두: {bean.name} ({bean.country_name})"

                # 현재 기록 정보 표시
                st.info(
                    f"**현재 기록**: {selected_log.roasting_date.strftime('%Y-%m-%d')}{bean_name} | "
                    f"생두: {selected_log.raw_weight_kg}kg → 로스팅후: {selected_log.roasted_weight_kg}kg | "
                    f"손실률: {selected_log.loss_rate_percent}% (예상: {selected_log.expected_loss_rate_percent}%)"
                )

                st.divider()

                # Session state 초기화 (선택된 로그가 변경되었을 때)
                if 'edit_log_id' not in st.session_state or st.session_state.edit_log_id != selected_log.id:
                    st.session_state.edit_log_id = selected_log.id
                    st.session_state.edit_bean_id = selected_log.bean_id
                    st.session_state.edit_roasting_date = selected_log.roasting_date
                    st.session_state.edit_raw_weight = float(selected_log.raw_weight_kg)
                    st.session_state.edit_roasted_weight = float(selected_log.roasted_weight_kg)
                    st.session_state.edit_expected_loss_rate = float(selected_log.expected_loss_rate_percent)
                    st.session_state.edit_notes = selected_log.notes or ""

                # 원두 목록 조회
                all_beans = bean_service.get_all_beans()

                # 원두 선택 옵션 생성
                bean_options = {"선택 안함 (원두 미지정)": None}
                for bean in all_beans:
                    bean_options[f"{bean.name} ({bean.country_name})"] = bean.id

                # 현재 선택된 원두 찾기
                current_bean_option = "선택 안함 (원두 미지정)"
                if st.session_state.edit_bean_id:
                    for option_text, bean_id in bean_options.items():
                        if bean_id == st.session_state.edit_bean_id:
                            current_bean_option = option_text
                            break

                # 편집 폼
                col1, col2 = st.columns(2)

                with col1:
                    new_roasting_date = st.date_input(
                        "📅 로스팅 날짜",
                        value=st.session_state.edit_roasting_date,
                        max_value=date.today(),
                        key="edit_date_input"
                    )
                    st.session_state.edit_roasting_date = new_roasting_date

                    # 원두 선택
                    selected_bean_option = st.selectbox(
                        "☕ 원두 선택",
                        options=list(bean_options.keys()),
                        index=list(bean_options.keys()).index(current_bean_option),
                        help="로스팅할 원두를 선택하세요",
                        key="edit_bean_select"
                    )
                    st.session_state.edit_bean_id = bean_options[selected_bean_option]

                    new_raw_weight_kg = st.number_input(
                        "⚖️ 생두 무게 (kg)",
                        min_value=0.1,
                        max_value=10000.0,
                        value=st.session_state.edit_raw_weight,
                        step=0.1,
                        format="%.2f",
                        help="생두 투입 무게를 입력하세요 (엔터 또는 포커스 아웃 시 자동 계산)",
                        key="edit_raw_weight_input"
                    )
                    st.session_state.edit_raw_weight = new_raw_weight_kg

                    new_roasted_weight_kg = st.number_input(
                        "⚖️ 로스팅 후 무게 (kg)",
                        min_value=0.1,
                        max_value=10000.0,
                        value=st.session_state.edit_roasted_weight,
                        step=0.1,
                        format="%.2f",
                        help="로스팅 후 무게를 입력하세요 (엔터 또는 포커스 아웃 시 자동 계산)",
                        key="edit_roasted_weight_input"
                    )
                    st.session_state.edit_roasted_weight = new_roasted_weight_kg

                with col2:
                    new_expected_loss_rate = st.number_input(
                        "📊 예상 손실률 (%)",
                        min_value=0.0,
                        max_value=50.0,
                        value=st.session_state.edit_expected_loss_rate,
                        step=0.1,
                        format="%.1f",
                        key="edit_expected_loss_rate_input"
                    )
                    st.session_state.edit_expected_loss_rate = new_expected_loss_rate

                    new_notes = st.text_area(
                        "📝 메모 (선택)",
                        value=st.session_state.edit_notes,
                        max_chars=500,
                        height=100,
                        key="edit_notes_input"
                    )
                    st.session_state.edit_notes = new_notes

                # 실시간 계산 결과
                if new_raw_weight_kg > 0:
                    new_actual_loss_rate = ((new_raw_weight_kg - new_roasted_weight_kg) / new_raw_weight_kg) * 100
                    new_loss_variance = new_actual_loss_rate - new_expected_loss_rate

                    # 상태 판정 (손실률이 낮을수록 좋음)
                    if new_loss_variance <= 0:
                        # 기준보다 낮음 (좋음)
                        status_color = "🟢"
                        status_text = "우수"
                    elif new_loss_variance <= 3.0:
                        # 기준 대비 +3% 이내 (정상)
                        status_color = "🟢"
                        status_text = "정상"
                    elif new_loss_variance <= 5.0:
                        # 기준 대비 +5% 이내 (주의)
                        status_color = "🟡"
                        status_text = "주의"
                    else:
                        # 기준 대비 +5% 초과 (위험)
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
                if st.button("✅ 저장", use_container_width=True, type="primary", key="edit_submit_button"):
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
                                bean_id=st.session_state.edit_bean_id,
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

                            # Session state 초기화
                            if 'edit_log_id' in st.session_state:
                                del st.session_state.edit_log_id

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

    if not monthly_stats or monthly_stats.get('status') == "데이터 없음" or monthly_stats.get('total_logs', 0) == 0:
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
