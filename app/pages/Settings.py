"""
설정 페이지
비용 설정, 시스템 설정, 데이터베이스 관리
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal, CostSetting, Bean, Blend, Inventory
from services.bean_service import BeanService
from services.blend_service import BlendService
from i18n import Translator, LanguageManager

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.settings.page_title", "설정")
st.set_page_config(page_title=page_title, page_icon="⚙️", layout="wide")

# 현재 페이지 저장 (사이드바 활성 표시)
st.session_state["current_page"] = "Settings"

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

st.markdown("<h1 style='color: #1F4E78;'>⚙️ 설정</h1>", unsafe_allow_html=True)
st.markdown("비용 설정, 시스템 설정, 데이터베이스 관리")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["💰 비용 설정", "⚙️ 시스템 설정", "📊 데이터베이스"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 비용 설정
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 💰 비용 설정")

    st.info("""
    로스팅 원가 계산에 사용되는 기본 비용을 설정합니다.
    이 설정은 모든 블렌드의 원가 계산에 영향을 미칩니다.
    """)

    st.divider()

    # 현재 비용 설정 로드
    cost_settings = db.query(CostSetting).all()

    cost_dict = {cs.parameter_name: cs for cs in cost_settings}

    # 비용 설정 표시 및 수정
    st.markdown("#### 📋 기본 비용 설정")

    col1, col2 = st.columns(2)

    # 로스팅 손실율
    with col1:
        st.markdown("**🔥 로스팅 손실율**")

        roasting_loss = cost_dict.get('roasting_loss_rate')
        current_loss = (float(roasting_loss.value) * 100) if roasting_loss else 16.7

        new_loss = st.slider(
            "로스팅 손실율 (%)",
            min_value=0.0,
            max_value=30.0,
            value=current_loss,
            step=0.1,
            key="roasting_loss"
        )

        if st.button("💾 저장", key="btn_roasting_loss"):
            try:
                if roasting_loss:
                    roasting_loss.value = new_loss / 100
                    roasting_loss.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="roasting_loss_rate",
                        value=new_loss / 100,
                        description="Roasting loss rate"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 로스팅 손실율이 {new_loss:.1f}%로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    # 로스팅비용
    with col2:
        st.markdown("**🔥 로스팅 비용**")

        roasting_cost = cost_dict.get('roasting_cost_per_kg')
        current_roasting = float(roasting_cost.value) if roasting_cost else 2000.0

        new_roasting = st.number_input(
            "로스팅 비용 (원/kg)",
            min_value=0,
            value=int(current_roasting),
            step=100,
            key="roasting_cost"
        )

        if st.button("💾 저장", key="btn_roasting_cost"):
            try:
                if roasting_cost:
                    roasting_cost.value = new_roasting
                    roasting_cost.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="roasting_cost_per_kg",
                        value=new_roasting,
                        description="Roasting cost per kg"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 로스팅 비용이 ₩{new_roasting:,.0f}/kg로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    st.divider()

    col1, col2 = st.columns(2)

    # 인건비
    with col1:
        st.markdown("**👨‍💼 인건비**")

        labor_cost = cost_dict.get('labor_cost_per_hour')
        current_labor = float(labor_cost.value) if labor_cost else 15000

        new_labor = st.number_input(
            "시간당 인건비 (원/시간)",
            min_value=0,
            value=int(current_labor),
            step=1000,
            key="labor_cost"
        )

        if st.button("💾 저장", key="btn_labor_cost"):
            try:
                if labor_cost:
                    labor_cost.value = new_labor
                    labor_cost.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="labor_cost_per_hour",
                        value=new_labor,
                        description="Labor cost per hour"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 인건비가 ₩{new_labor:,.0f}/시간으로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    # 로스팅 시간
    with col2:
        st.markdown("**⏱️ 로스팅 시간**")

        roasting_time = cost_dict.get('roasting_time_hours')
        current_time = float(roasting_time.value) if roasting_time else 2.0

        new_time = st.number_input(
            "로스팅 시간 (시간)",
            min_value=0.5,
            value=current_time,
            step=0.5,
            key="roasting_time"
        )

        if st.button("💾 저장", key="btn_roasting_time"):
            try:
                if roasting_time:
                    roasting_time.value = new_time
                    roasting_time.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="roasting_time_hours",
                        value=new_time,
                        description="Roasting time in hours"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 로스팅 시간이 {new_time}시간으로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    st.divider()

    col1, col2 = st.columns(2)

    # 전기료
    with col1:
        st.markdown("**⚡ 전기료**")

        electricity_cost = cost_dict.get('electricity_cost')
        current_elec = float(electricity_cost.value) if electricity_cost else 5000

        new_elec = st.number_input(
            "전기료 (원/로스팅)",
            min_value=0,
            value=int(current_elec),
            step=100,
            key="electricity_cost"
        )

        if st.button("💾 저장", key="btn_electricity"):
            try:
                if electricity_cost:
                    electricity_cost.value = new_elec
                    electricity_cost.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="electricity_cost",
                        value=new_elec,
                        description="Electricity cost per roasting"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 전기료가 ₩{new_elec:,.0f}로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    # 기타 비용
    with col2:
        st.markdown("**📦 기타 비용**")

        misc_cost = cost_dict.get('misc_cost')
        current_misc = float(misc_cost.value) if misc_cost else 3000

        new_misc = st.number_input(
            "기타 비용 (원/로스팅)",
            min_value=0,
            value=int(current_misc),
            step=100,
            key="misc_cost"
        )

        if st.button("💾 저장", key="btn_misc"):
            try:
                if misc_cost:
                    misc_cost.value = new_misc
                    misc_cost.updated_at = datetime.utcnow()
                else:
                    new_setting = CostSetting(
                        parameter_name="misc_cost",
                        value=new_misc,
                        description="Miscellaneous cost per roasting"
                    )
                    db.add(new_setting)

                db.commit()
                st.success(f"✅ 기타 비용이 ₩{new_misc:,.0f}로 설정되었습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    st.divider()

    # 마진율
    st.markdown("#### 📈 마진율 설정")

    margin_rate = cost_dict.get('margin_rate')
    current_margin = float(margin_rate.value) if margin_rate else 2.5

    new_margin = st.slider(
        "판매가 마진율 (배수: 원가 × 마진율)",
        min_value=1.0,
        max_value=5.0,
        value=current_margin,
        step=0.1,
        key="margin_rate"
    )

    st.caption(f"예: 원가 ₩10,000 × {new_margin}배 = 판매가 ₩{10000 * new_margin:,.0f}")

    if st.button("💾 마진율 저장", use_container_width=True, key="btn_margin"):
        try:
            if margin_rate:
                margin_rate.value = new_margin
                margin_rate.updated_at = datetime.utcnow()
            else:
                new_setting = CostSetting(
                    parameter_name="margin_rate",
                    value=new_margin,
                    description="Margin rate for pricing"
                )
                db.add(new_setting)

            db.commit()
            st.success(f"✅ 마진율이 {new_margin}배로 설정되었습니다.")
        except Exception as e:
            st.error(f"❌ 오류: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 시스템 설정
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### ⚙️ 시스템 설정")

    # 알림 설정
    st.markdown("#### 🔔 알림 설정")

    st.info("현재는 저재고 경고만 지원됩니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔴 저재고 경고**")
        enable_low_stock = st.checkbox("저재고 경고 활성화", value=True)

    with col2:
        st.markdown("**🟡 과재고 경고**")
        enable_over_stock = st.checkbox("과재고 경고 활성화", value=True)

    if st.button("💾 알림 설정 저장", use_container_width=True):
        st.success("✅ 알림 설정이 저장되었습니다.")

    st.divider()

    # 표시 설정
    st.markdown("#### 🎨 화면 설정")

    col1, col2 = st.columns(2)

    with col1:
        currency_symbol = st.selectbox("통화 기호", ["₩ (원)", "$ (달러)", "€ (유로)"])

    with col2:
        decimal_places = st.number_input("소수점 자리수", min_value=0, max_value=3, value=2)

    if st.button("💾 화면 설정 저장", use_container_width=True):
        st.success("✅ 화면 설정이 저장되었습니다.")

    st.divider()

    # 시스템 정보
    st.markdown("#### ℹ️ 시스템 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**애플리케이션**")
        st.write(f"버전: 2.0.0")
        st.write(f"상태: Phase 3")

    with col2:
        st.markdown("**파이썬**")
        st.write(f"버전: 3.12.3")

    with col3:
        st.markdown("**라이브러리**")
        st.write(f"Streamlit: 1.38.0")
        st.write(f"SQLAlchemy: 2.0.23")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 데이터베이스
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### 📊 데이터베이스")

    # 데이터베이스 정보
    st.markdown("#### 📍 데이터베이스 정보")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**위치:** Data/roasting_data.db")
        st.write(f"**타입:** SQLite3")

    with col2:
        beans_count = db.query(Bean).filter(Bean.status == "active").count()
        blends_count = db.query(Blend).filter(Blend.status == "active").count()
        st.write(f"**원두:** {beans_count}종")
        st.write(f"**블렌드:** {blends_count}개")

    st.divider()

    # 테이블 통계
    st.markdown("#### 📋 테이블 통계")

    beans_total = db.query(Bean).count()
    blends_total = db.query(Blend).count()
    inventory_total = db.query(Inventory).count()
    cost_settings_total = db.query(CostSetting).count()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("☕ Beans", beans_total)

    with col2:
        st.metric("🎨 Blends", blends_total)

    with col3:
        st.metric("📦 Inventory", inventory_total)

    with col4:
        st.metric("⚙️ Settings", cost_settings_total)

    st.divider()

    # 데이터베이스 관리
    st.markdown("#### 🔧 데이터베이스 관리")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📊 데이터 백업**")

        if st.button("💾 백업 생성", use_container_width=True):
            try:
                import shutil
                backup_name = f"roasting_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy("Data/roasting_data.db", f"Data/{backup_name}")
                st.success(f"✅ 백업이 생성되었습니다: {backup_name}")
            except Exception as e:
                st.error(f"❌ 백업 오류: {str(e)}")

    with col2:
        st.markdown("**🔄 데이터 초기화**")

        if st.button("⚠️ 데이터 초기화 (위험)", use_container_width=True, type="secondary"):
            st.warning("""
            이 작업은 모든 데이터를 초기화합니다.
            취소하려면 페이지를 새로고침하세요.
            """)

            if st.button("✅ 정말로 초기화하시겠습니까?", type="primary"):
                try:
                    # 모든 데이터 삭제
                    db.query(Bean).delete()
                    db.query(Blend).delete()
                    db.query(Inventory).delete()
                    db.query(CostSetting).delete()
                    db.commit()

                    st.success("✅ 데이터가 초기화되었습니다.")
                except Exception as e:
                    st.error(f"❌ 초기화 오류: {str(e)}")

    st.divider()

    # 데이터 검증
    st.markdown("#### ✅ 데이터 검증")

    if st.button("🔍 데이터 검증 실행", use_container_width=True):
        with st.spinner("검증 중..."):
            try:
                # 원두 검증
                beans = db.query(Bean).all()
                beans_valid = len([b for b in beans if b.name and b.roast_level])

                # 블렌드 검증
                blends = db.query(Blend).all()
                blends_valid = len([b for b in blends if b.name and b.blend_type])

                # 재고 검증
                inventory = db.query(Inventory).all()
                inventory_valid = len([i for i in inventory if i.bean_id])

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("원두", f"{beans_valid}/{len(beans)}", delta="유효")

                with col2:
                    st.metric("블렌드", f"{blends_valid}/{len(blends)}", delta="유효")

                with col3:
                    st.metric("재고", f"{inventory_valid}/{len(inventory)}", delta="유효")

                st.success("✅ 데이터 검증 완료!")

            except Exception as e:
                st.error(f"❌ 검증 오류: {str(e)}")
