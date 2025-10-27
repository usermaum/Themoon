"""
더문드립바 웹 애플리케이션 - 메인 앱 (v2.0)
The Moon Drip BAR - Roasting Management System
Streamlit 멀티페이지 애플리케이션
"""

import streamlit as st
import sys
import os
from datetime import datetime

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import SessionLocal, init_db
from services.bean_service import BeanService
from services.blend_service import BlendService
from utils.constants import UI_CONFIG

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 페이지 설정
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=UI_CONFIG["app_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 커스텀 스타일
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* 주요 컬러 */
    :root {
        --primary: #1F4E78;
        --secondary: #4472C4;
        --success: #70AD47;
        --danger: #C41E3A;
    }

    /* 메인 헤더 */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F4E78;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    /* 버튼 */
    .stButton > button {
        background-color: #4472C4 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button:hover {
        background-color: #1F4E78 !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state():
    """세션 상태 초기화"""
    if "db" not in st.session_state:
        st.session_state.db = SessionLocal()

    if "bean_service" not in st.session_state:
        st.session_state.bean_service = BeanService(st.session_state.db)

    if "blend_service" not in st.session_state:
        st.session_state.blend_service = BlendService(st.session_state.db)


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 헤더 및 사이드바
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    """헤더 렌더링"""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f'<p class="main-header">☕ {UI_CONFIG["app_title"]}</p>',
                   unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{UI_CONFIG["app_subtitle"]}</p>',
                   unsafe_allow_html=True)

    with col2:
        st.write("")
        st.write("")
        st.metric("현재시간", datetime.now().strftime("%H:%M"))


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("### 🔗 네비게이션")

        st.info("""
        좌측 상단의 ☰ 메뉴를 통해 페이지를 이동합니다:

        - 🏠 **홈** (현재)
        - 🎨 **블렌딩관리**
        - ☕ **원두관리**
        - 📊 **분석**
        - 📦 **재고관리**
        """)

        st.divider()

        # 빠른 통계
        st.markdown("### 📊 현황")

        db = st.session_state.db
        bean_service = st.session_state.bean_service
        blend_service = st.session_state.blend_service

        beans = bean_service.get_active_beans()
        blends = blend_service.get_active_blends()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("☕ 원두", len(beans))
        with col2:
            st.metric("🎨 블렌드", len(blends))

        st.divider()

        # 도구
        st.markdown("### ⚙️ 도구")

        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()

        st.divider()

        # 정보
        st.markdown("### ℹ️ 정보")
        st.caption(f"""
        **{UI_CONFIG["app_title"]}**

        🚀 버전: 2.0.0
        📅 시작: 2025-10-24
        🎯 상태: Phase 2

        **데이터:**
        - 원두: {len(beans)}종
        - 블렌드: {len(blends)}개
        - 포션: 20개
        """)


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 홈 페이지
# ═══════════════════════════════════════════════════════════════════════════════

def render_home():
    """홈 페이지"""
    render_header()

    st.divider()

    # 환영 메시지
    st.markdown("""
    # 👋 더문드립바 웹 시스템에 오신 것을 환영합니다!

    이 시스템은 로스팅 원두를 효율적으로 관리하고 분석하기 위한 통합 플랫폼입니다.
    """)

    st.divider()

    # 빠른 시작
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🎯 시작하기

        **원두 관리**
        - 13종 원두 확인
        - 새 원두 추가
        - 원두 정보 수정
        """)
        if st.button("☕ 원두관리로 이동", use_container_width=True):
            st.switch_page("pages/BeanManagement.py")

    with col2:
        st.markdown("""
        ### 🎨 블렌드 관리

        **블렌딩 레시피**
        - 풀문 블렌드 (3개)
        - 뉴문 블렌딩 (3개)
        - 원가 자동 계산
        """)
        if st.button("🎨 블렌딩관리로 이동", use_container_width=True):
            st.switch_page("pages/BlendManagement.py")

    with col3:
        st.markdown("""
        ### 📊 분석

        **통계 및 분석**
        - 판매 추이
        - 수익 분석
        - 선호도 분석
        """)
        if st.button("📊 분석으로 이동", use_container_width=True):
            st.switch_page("pages/Analysis.py")

    st.divider()

    # 주요 통계
    st.markdown("## 📊 주요 통계")

    db = st.session_state.db
    bean_service = st.session_state.bean_service
    blend_service = st.session_state.blend_service

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        bean_summary = bean_service.get_beans_summary()
        st.metric("☕ 총 원두", f"{bean_summary['total_beans']}종")

    with col2:
        blend_summary = blend_service.get_blends_summary()
        st.metric("🎨 총 블렌드", f"{blend_summary['total_blends']}개")

    with col3:
        st.metric("📦 총 포션", "20개")

    with col4:
        st.metric("🌍 국가", "6개")

    st.divider()

    # 원두 분포
    st.markdown("## 🔥 원두 로스팅 레벨 분포")

    bean_summary = bean_service.get_beans_summary()
    roast_data = bean_summary['by_roast_level']

    if roast_data:
        cols = st.columns(len(roast_data))

        for i, (level, count) in enumerate(roast_data.items()):
            level_names = {
                "W": "Light/White",
                "N": "Normal",
                "Pb": "Plus Black",
                "Rh": "Rheuma",
                "SD": "Semi-Dark",
                "SC": "Semi-Dark"
            }

            with cols[i]:
                st.metric(f"{level}\n({level_names.get(level, level)})", f"{count}개")

    st.divider()

    # 블렌드 분포
    st.markdown("## 🎨 블렌드 타입 분포")

    blend_summary = blend_service.get_blends_summary()
    type_data = blend_summary['by_type']

    if type_data:
        cols = st.columns(3)

        for i, (blend_type, count) in enumerate(type_data.items()):
            if i < len(cols):
                with cols[i]:
                    st.metric(f"{blend_type} 블렌드", f"{count}개")


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 메인 실행
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """메인 함수"""
    # 세션 상태 초기화
    init_session_state()

    # 데이터베이스 초기화 (필요 시)
    if not os.path.exists("Data/roasting_data.db"):
        with st.spinner("📊 데이터베이스 초기화 중..."):
            init_db()
            st.session_state.bean_service.init_default_beans()
            st.session_state.blend_service.init_default_blends()
            st.success("✅ 데이터베이스 초기화 완료!")

    # 사이드바
    render_sidebar()

    # 홈 페이지
    render_home()


if __name__ == "__main__":
    main()
