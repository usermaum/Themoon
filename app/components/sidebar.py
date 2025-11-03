"""
사이드바 컴포넌트 (Claude Desktop 스타일)
"""

import streamlit as st
from utils.constants import UI_CONFIG


def render_sidebar():
    """사이드바 렌더링 (Claude Desktop 스타일)"""
    with st.sidebar:
        # ═══════════════════════════════════════════════════════════
        # 1️⃣ 로고 영역
        # ═══════════════════════════════════════════════════════════
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0 1.5rem 0;'>
            <h2 style='margin: 0; color: #1F4E78; font-size: 28px;'>☕ The Moon</h2>
            <p style='margin: 4px 0 0 0; font-size: 12px; color: #999;'>Drip BAR Roasting System</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 2️⃣ 언어 선택
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 🌐 언어")

        lang_manager = st.session_state.language_manager
        translator = st.session_state.translator
        current_lang = lang_manager.get_current_language()

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "🇰🇷 한글",
                use_container_width=True,
                key="lang_ko",
                type="primary" if current_lang == "ko" else "secondary"
            ):
                if lang_manager.set_current_language("ko"):
                    st.rerun()

        with col2:
            if st.button(
                "🇬🇧 English",
                use_container_width=True,
                key="lang_en",
                type="primary" if current_lang == "en" else "secondary"
            ):
                if lang_manager.set_current_language("en"):
                    st.rerun()

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 3️⃣ 핵심 기능 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📌 핵심 기능")

        # 현재 페이지 감지
        current_page = st.session_state.get("current_page", "home")

        # 홈
        if st.button(
            "🏠 홈",
            type="primary" if current_page == "home" else "secondary",
            use_container_width=True,
            key="nav_home"
        ):
            st.session_state["current_page"] = "home"
            st.switch_page("app.py")

        # 원두관리
        if st.button(
            "☕ 원두관리",
            type="primary" if current_page == "BeanManagement" else "secondary",
            use_container_width=True,
            key="nav_bean"
        ):
            st.session_state["current_page"] = "BeanManagement"
            st.switch_page("pages/BeanManagement.py")

        # 블렌딩관리
        if st.button(
            "🎨 블렌딩관리",
            type="primary" if current_page == "BlendManagement" else "secondary",
            use_container_width=True,
            key="nav_blend"
        ):
            st.session_state["current_page"] = "BlendManagement"
            st.switch_page("pages/BlendManagement.py")

        # 분석
        if st.button(
            "📊 분석",
            type="primary" if current_page == "Analysis" else "secondary",
            use_container_width=True,
            key="nav_analysis"
        ):
            st.session_state["current_page"] = "Analysis"
            st.switch_page("pages/Analysis.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 4️⃣ 운영 관리 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📦 운영 관리")

        # 로스팅 기록
        if st.button(
            "📊 로스팅 기록",
            type="primary" if current_page == "RoastingRecord" else "secondary",
            use_container_width=True,
            key="nav_roasting"
        ):
            st.session_state["current_page"] = "RoastingRecord"
            st.switch_page("pages/RoastingRecord.py")

        # 재고관리
        if st.button(
            "📦 재고관리",
            type="primary" if current_page == "InventoryManagement" else "secondary",
            use_container_width=True,
            key="nav_inventory"
        ):
            st.session_state["current_page"] = "InventoryManagement"
            st.switch_page("pages/InventoryManagement.py")

        # 보고서
        if st.button(
            "📋 보고서",
            type="primary" if current_page == "Report" else "secondary",
            use_container_width=True,
            key="nav_report"
        ):
            st.session_state["current_page"] = "Report"
            st.switch_page("pages/Report.py")

        # Excel동기화
        if st.button(
            "📑 Excel동기화",
            type="primary" if current_page == "ExcelSync" else "secondary",
            use_container_width=True,
            key="nav_excel"
        ):
            st.session_state["current_page"] = "ExcelSync"
            st.switch_page("pages/ExcelSync.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 5️⃣ 고급 기능 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### ⭐ 고급 기능")

        # 고급분석
        if st.button(
            "🔬 고급분석",
            type="primary" if current_page == "AdvancedAnalysis" else "secondary",
            use_container_width=True,
            key="nav_advanced"
        ):
            st.session_state["current_page"] = "AdvancedAnalysis"
            st.switch_page("pages/AdvancedAnalysis.py")

        # 설정
        if st.button(
            "⚙️ 설정",
            type="primary" if current_page == "Settings" else "secondary",
            use_container_width=True,
            key="nav_settings"
        ):
            st.session_state["current_page"] = "Settings"
            st.switch_page("pages/Settings.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 6️⃣ 빠른 통계
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📊 현황")

        db = st.session_state.db
        bean_service = st.session_state.bean_service
        blend_service = st.session_state.blend_service

        beans = bean_service.get_active_beans()
        blends = blend_service.get_active_blends()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("☕ 원두", f"{len(beans)}종")
        with col2:
            st.metric("🎨 블렌드", f"{len(blends)}개")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 7️⃣ 도구
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 🔧 도구")

        if st.button("🔄 새로고침", use_container_width=True, key="btn_refresh"):
            st.rerun()

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 8️⃣ 정보
        # ═══════════════════════════════════════════════════════════
        st.markdown("### ℹ️ 정보")
        st.caption(f"""
        **{UI_CONFIG["app_title"]}** v0.1.0

        🚀 Claude Desktop Style UI
        📅 업데이트: 2025-10-29
        🎯 상태: 개발 중

        **현재 데이터:**
        - 원두: {len(beans)}종
        - 블렌드: {len(blends)}개
        - 포션: 20개
        """)
