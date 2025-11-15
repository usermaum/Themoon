"""
원두 관리 페이지
13종 원두 CRUD 및 관리 시스템
"""

import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.bean_service import BeanService
from i18n import Translator, LanguageManager
from components.sidebar import render_sidebar

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.bean_management.page_title", "원두관리")
st.set_page_config(page_title=page_title, page_icon="☕", layout="wide")

# 현재 페이지 저장 (사이드바 활성 표시)
st.session_state["current_page"] = "BeanManagement"

# 사이드바 렌더링
render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

bean_service = st.session_state.bean_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>☕ 원두 관리</h1>", unsafe_allow_html=True)
st.markdown("13종 원두의 정보를 관리하고 CRUD 작업을 수행합니다.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📋 목록", "➕ 추가", "✏️ 편집", "📊 통계"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 목록 조회
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📋 원두 목록")

    # 원두 데이터 로드 (필터링 옵션을 위해 먼저 로드)
    beans = bean_service.get_active_beans()

    # 브랜드 목록 추출
    brands = sorted(set(b.brand for b in beans if b.brand))

    # 필터링 옵션
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_country = st.multiselect(
            "국가 필터",
            options=["Eth", "K", "Co", "Gu", "Cos", "Br", "기타"],
            default=None
        )

    with col2:
        filter_roast = st.multiselect(
            "로스팅 레벨 필터",
            options=["W", "N", "Pb", "Rh", "SD", "SC"],
            default=None
        )

    with col3:
        filter_brand = st.multiselect(
            "브랜드 필터",
            options=brands,
            default=None
        ) if brands else None

    with col4:
        search_text = st.text_input("원두명 검색", "")

    st.divider()

    # 필터링 적용
    filtered_beans = beans

    if filter_country:
        filtered_beans = [b for b in filtered_beans if b.country_code in filter_country or b.country_code is None]

    if filter_roast:
        filtered_beans = [b for b in filtered_beans if b.roast_level in filter_roast]

    if filter_brand:
        filtered_beans = [b for b in filtered_beans if b.brand in filter_brand]

    if search_text:
        filtered_beans = [b for b in filtered_beans if search_text.lower() in b.name.lower()]

    # 데이터 표시
    if filtered_beans:
        data = []
        for bean in filtered_beans:
            data.append({
                "No": bean.no,
                "국가코드": bean.country_code or "-",
                "원두명": bean.name,
                "브랜드": bean.brand or "-",
                "로스팅": bean.roast_level,
                "가격(원/kg)": f"₩{bean.price_per_kg:,.0f}" if bean.price_per_kg > 0 else "미정",
                "평균 손실률(%)": f"{bean.avg_loss_rate:.1f}%" if bean.avg_loss_rate else "-",
                "로스팅 횟수": bean.total_roasted_count or 0,
                "마지막 로스팅": bean.last_roasted_date.strftime("%Y-%m-%d") if bean.last_roasted_date else "-",
                "상태": bean.status,
                "설명": bean.description or "-"
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 통계
        st.markdown("#### 📊 필터된 데이터 통계")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("원두 개수", len(filtered_beans))

        with col2:
            roast_levels = set(b.roast_level for b in filtered_beans)
            st.metric("로스팅 레벨", len(roast_levels))

        with col3:
            valid_beans = [b for b in filtered_beans if b.price_per_kg > 0]
            if valid_beans:
                avg_price = sum(b.price_per_kg for b in valid_beans) / len(valid_beans)
                st.metric("평균 가격", f"₩{avg_price:,.0f}")
            else:
                st.metric("평균 가격", "N/A")

    else:
        st.info("필터 조건에 맞는 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 원두 추가
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### ➕ 새 원두 추가")

    with st.form("add_bean_form"):
        col1, col2 = st.columns(2)

        with col1:
            no = st.number_input("원두 번호", min_value=1, max_value=999, value=14)
            name = st.text_input("원두명", "")
            country_code = st.selectbox("국가코드", ["Eth", "K", "Co", "Gu", "Cos", "Br", "기타"])
            brand = st.text_input("브랜드", "", help="원두 브랜드 (선택사항)")

        with col2:
            roast_level = st.selectbox("로스팅 레벨", ["W", "N", "Pb", "Rh", "SD", "SC"])
            price_per_kg = st.number_input("가격 (원/kg)", min_value=0, value=0, step=100)
            description = st.text_input("설명", "")

        if st.form_submit_button("✅ 원두 추가", use_container_width=True):
            if not name:
                st.error("❌ 원두명을 입력해주세요.")
            else:
                try:
                    bean_service.create_bean(
                        no=no,
                        name=name,
                        roast_level=roast_level,
                        country_code=country_code if country_code != "기타" else None,
                        brand=brand if brand else None,
                        description=description,
                        price_per_kg=price_per_kg
                    )
                    st.success(f"✅ '{name}' 원두가 추가되었습니다!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 원두 편집
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### ✏️ 원두 정보 편집")

    beans = bean_service.get_active_beans()

    if beans:
        bean_options = {b.name: b.id for b in beans}
        selected_name = st.selectbox("편집할 원두 선택", list(bean_options.keys()))

        if selected_name:
            selected_bean = bean_service.get_bean_by_id(bean_options[selected_name])

            with st.form("edit_bean_form"):
                col1, col2 = st.columns(2)

                with col1:
                    new_name = st.text_input("원두명", value=selected_bean.name)
                    new_roast = st.selectbox("로스팅 레벨", ["W", "N", "Pb", "Rh", "SD", "SC"],
                                            index=["W", "N", "Pb", "Rh", "SD", "SC"].index(selected_bean.roast_level))
                    new_price = st.number_input("가격 (원/kg)", value=float(selected_bean.price_per_kg), min_value=0.0, step=100.0)

                with col2:
                    new_description = st.text_input("설명", value=selected_bean.description or "")
                    new_status = st.selectbox("상태", ["active", "inactive"],
                                             index=0 if selected_bean.status == "active" else 1)

                if st.form_submit_button("✅ 저장", use_container_width=True):
                    try:
                        bean_service.update_bean(
                            selected_bean.id,
                            name=new_name,
                            roast_level=new_roast,
                            price_per_kg=new_price,
                            description=new_description,
                            status=new_status
                        )
                        st.success("✅ 원두 정보가 업데이트되었습니다!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")

            # 삭제 버튼
            st.divider()
            st.markdown("#### 🗑️ 위험한 작업")

            if st.button("🗑️ 이 원두 삭제 (비활성화)", use_container_width=True, type="secondary"):
                try:
                    bean_service.delete_bean(selected_bean.id)
                    st.success("✅ 원두가 비활성화되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")

    else:
        st.info("편집할 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 통계
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### 📊 원두 통계")

    bean_summary = bean_service.get_beans_summary()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("☕ 총 원두", f"{bean_summary['total_beans']}종")

    with col2:
        st.metric("🔥 로스팅 레벨", len(bean_summary['by_roast_level']))

    with col3:
        beans = bean_service.get_active_beans()
        total_price = sum(b.price_per_kg for b in beans if b.price_per_kg > 0)
        st.metric("💰 총 가격", f"₩{total_price:,.0f}")

    st.divider()

    # 로스팅 레벨 분포
    st.markdown("#### 🔥 로스팅 레벨 분포")

    roast_data = bean_summary['by_roast_level']

    if roast_data:
        cols = st.columns(len(roast_data))

        for i, (level, count) in enumerate(roast_data.items()):
            with cols[i]:
                st.metric(f"로스팅 {level}", f"{count}개")

    # 가장 비싼 원두
    st.markdown("#### 💰 가격대별 원두")

    beans = bean_service.get_active_beans()
    beans_with_price = [b for b in beans if b.price_per_kg > 0]

    if beans_with_price:
        beans_with_price.sort(key=lambda x: x.price_per_kg, reverse=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔝 가장 비싼 원두 (Top 3)**")
            for i, bean in enumerate(beans_with_price[:3], 1):
                st.write(f"{i}. {bean.name}: ₩{bean.price_per_kg:,.0f}/kg")

        with col2:
            st.markdown("**🔻 가장 싼 원두 (Top 3)**")
            for i, bean in enumerate(reversed(beans_with_price[-3:]), 1):
                st.write(f"{i}. {bean.name}: ₩{bean.price_per_kg:,.0f}/kg")

    # 원두별 상세 통계
    st.divider()
    st.markdown("#### 📈 원두별 상세 통계")

    beans_with_stats = [b for b in beans if b.total_roasted_count and b.total_roasted_count > 0]

    if beans_with_stats:
        bean_names = {b.name: b.id for b in beans_with_stats}
        selected_bean_name = st.selectbox(
            "원두 선택",
            list(bean_names.keys()),
            help="로스팅 이력이 있는 원두만 표시됩니다"
        )

        if selected_bean_name:
            selected_bean_id = bean_names[selected_bean_name]
            selected_bean = bean_service.get_bean_by_id(selected_bean_id)

            # 원두 통계 카드
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("📊 평균 손실률",
                         f"{selected_bean.avg_loss_rate:.1f}%" if selected_bean.avg_loss_rate else "N/A")

            with col2:
                st.metric("🎯 표준편차",
                         f"{selected_bean.std_loss_rate:.1f}%" if selected_bean.std_loss_rate else "N/A")

            with col3:
                st.metric("🔥 총 로스팅 횟수",
                         f"{selected_bean.total_roasted_count}회")

            with col4:
                st.metric("📅 마지막 로스팅",
                         selected_bean.last_roasted_date.strftime("%Y-%m-%d") if selected_bean.last_roasted_date else "N/A")

            # 로스팅 이력 조회
            from services.roasting_service import RoastingService
            roasting_service = RoastingService()

            roasting_logs = st.session_state.db.query(
                st.session_state.db.query(RoastingLog).filter(RoastingLog.bean_id == selected_bean_id).order_by(RoastingLog.roasting_date.desc()).limit(10).subquery()
            ).all() if 'RoastingLog' in dir() else []

            # 간단한 방법으로 다시 시도
            try:
                from models.database import RoastingLog
                roasting_logs = st.session_state.db.query(RoastingLog).filter(
                    RoastingLog.bean_id == selected_bean_id
                ).order_by(RoastingLog.roasting_date.desc()).limit(10).all()

                if roasting_logs:
                    st.markdown("##### 📋 최근 로스팅 이력 (최근 10건)")

                    log_data = []
                    for log in reversed(roasting_logs):  # 날짜 오름차순으로 표시
                        log_data.append({
                            "날짜": log.roasting_date.strftime("%Y-%m-%d"),
                            "투입량(kg)": f"{log.raw_weight_kg:.2f}",
                            "산출량(kg)": f"{log.roasted_weight_kg:.2f}",
                            "손실률(%)": f"{log.loss_rate_percent:.1f}%",
                            "편차(%)": f"{log.loss_variance_percent:+.1f}%" if log.loss_variance_percent else "-"
                        })

                    df_logs = pd.DataFrame(log_data)
                    st.dataframe(df_logs, use_container_width=True, hide_index=True)

                    # 손실률 추이 그래프
                    st.markdown("##### 📉 손실률 추이")

                    import plotly.graph_objects as go

                    dates = [log.roasting_date for log in reversed(roasting_logs)]
                    loss_rates = [log.loss_rate_percent for log in reversed(roasting_logs)]

                    fig = go.Figure()

                    # 손실률 라인
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=loss_rates,
                        mode='lines+markers',
                        name='손실률',
                        line=dict(color='#FF6B6B', width=2),
                        marker=dict(size=8)
                    ))

                    # 평균 손실률 라인
                    if selected_bean.avg_loss_rate:
                        fig.add_trace(go.Scatter(
                            x=[dates[0], dates[-1]],
                            y=[selected_bean.avg_loss_rate, selected_bean.avg_loss_rate],
                            mode='lines',
                            name=f'평균 ({selected_bean.avg_loss_rate:.1f}%)',
                            line=dict(color='#4ECDC4', width=2, dash='dash')
                        ))

                    fig.update_layout(
                        title="",
                        xaxis_title="날짜",
                        yaxis_title="손실률 (%)",
                        hovermode='x unified',
                        height=400
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.info("로스팅 이력이 없습니다.")

            except Exception as e:
                st.warning(f"로스팅 이력을 불러올 수 없습니다: {str(e)}")
    else:
        st.info("로스팅 이력이 있는 원두가 없습니다.")

    # 데이터 내보내기
    st.divider()
    st.markdown("#### 📥 데이터 내보내기")

    export_data = bean_service.export_as_dict()
    df_export = pd.DataFrame(export_data)

    csv = df_export.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="📥 CSV로 다운로드",
        data=csv,
        file_name="원두_목록.csv",
        mime="text/csv"
    )
