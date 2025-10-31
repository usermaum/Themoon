"""
블렌딩 관리 페이지
풀문, 뉴문, 시즈널 블렌드 CRUD 및 원가 계산
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
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
page_title = translator.get("menu.blend_management.page_title", "블렌딩관리")
st.set_page_config(page_title=page_title, page_icon="🎨", layout="wide")

# 현재 페이지 저장 (사이드바 활성 표시)
st.session_state["current_page"] = "BlendManagement"

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

bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>🎨 블렌딩 관리</h1>", unsafe_allow_html=True)
st.markdown("풀문, 뉴문, 시즈널 블렌드의 레시피 및 원가를 관리합니다.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📋 목록", "🎨 상세보기", "➕ 추가", "✏️ 편집"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 블렌드 목록 조회
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📋 블렌드 목록")

    # 블렌드 타입 필터
    col1, col2 = st.columns(2)

    with col1:
        filter_type = st.multiselect(
            "블렌드 타입 필터",
            options=["풀문", "뉴문", "시즈널"],
            default=None
        )

    with col2:
        search_text = st.text_input("블렌드명 검색", "")

    st.divider()

    # 블렌드 데이터 로드
    blends = blend_service.get_active_blends()

    # 필터링 적용
    filtered_blends = blends

    if filter_type:
        filtered_blends = [b for b in filtered_blends if b.blend_type in filter_type]

    if search_text:
        filtered_blends = [b for b in filtered_blends if search_text.lower() in b.name.lower()]

    # 데이터 표시
    if filtered_blends:
        data = []
        for blend in filtered_blends:
            cost_info = blend_service.calculate_blend_cost(blend.id)
            data.append({
                "ID": blend.id,
                "블렌드명": blend.name,
                "타입": blend.blend_type,
                "포션": blend.total_portion,
                "포션당 원가": f"₩{cost_info['cost_per_portion']:,.0f}" if cost_info else "-",
                "제안 가격": f"₩{cost_info['suggested_price']:,.0f}" if cost_info else "-",
                "상태": blend.status,
                "설명": blend.description or "-"
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 통계
        st.markdown("#### 📊 필터된 블렌드 통계")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("블렌드 개수", len(filtered_blends))

        with col2:
            total_portions = sum(b.total_portion for b in filtered_blends)
            st.metric("총 포션", f"{total_portions}개")

        with col3:
            avg_cost = sum(blend_service.calculate_blend_cost(b.id)['cost_per_portion']
                          for b in filtered_blends
                          if blend_service.calculate_blend_cost(b.id)) / len(filtered_blends) if filtered_blends else 0
            st.metric("평균 원가", f"₩{avg_cost:,.0f}")

    else:
        st.info("필터 조건에 맞는 블렌드가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 블렌드 상세보기
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 🎨 블렌드 상세보기")

    blends = blend_service.get_active_blends()

    if blends:
        blend_options = {b.name: b.id for b in blends}
        selected_name = st.selectbox("상세 정보를 볼 블렌드 선택", list(blend_options.keys()))

        if selected_name:
            selected_blend = blend_service.get_blend_by_id(blend_options[selected_name])

            if selected_blend:
                # 기본 정보
                st.markdown(f"#### 📌 {selected_blend.name}")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("타입", selected_blend.blend_type)

                with col2:
                    st.metric("포션", f"{selected_blend.total_portion}개")

                with col3:
                    st.metric("상태", selected_blend.status)

                with col4:
                    if selected_blend.suggested_price:
                        st.metric("제안 가격", f"₩{selected_blend.suggested_price:,.0f}")
                    else:
                        st.metric("제안 가격", "-")

                st.divider()

                # 블렌드 레시피
                st.markdown("#### 🌾 블렌드 레시피")

                recipes = blend_service.get_blend_recipes(selected_blend.id)

                if recipes:
                    recipe_data = []
                    total_ratio = 0

                    for recipe in recipes:
                        bean = bean_service.get_bean_by_id(recipe.bean_id)
                        if bean:
                            ratio = recipe.ratio if recipe.ratio else (recipe.portion_count / selected_blend.total_portion * 100) if selected_blend.total_portion > 0 else 0
                            total_ratio += ratio
                            recipe_data.append({
                                "원두명": bean.name,
                                "국가": bean.country_code,
                                "로스팅": bean.roast_level,
                                "포션": recipe.portion_count,
                                "비율": f"{ratio:.1f}%",
                                "가격/kg": f"₩{bean.price_per_kg:,.0f}"
                            })

                    df_recipes = pd.DataFrame(recipe_data)
                    st.dataframe(df_recipes, use_container_width=True, hide_index=True)

                    # 파이 차트로 포션 구성 시각화
                    st.markdown("#### 📊 포션 구성비")

                    fig = go.Figure(data=[go.Pie(
                        labels=[r["원두명"] for r in recipe_data],
                        values=[r["포션"] for r in recipe_data],
                        hovertemplate="<b>%{label}</b><br>포션: %{value}개<br>비율: %{percent}<extra></extra>"
                    )])

                    fig.update_layout(
                        title=f"{selected_blend.name} - 포션 구성",
                        height=400,
                        showlegend=True
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("이 블렌드에 레시피가 없습니다.")

                st.divider()

                # 원가 계산
                st.markdown("#### 💰 원가 계산")

                cost_info = blend_service.calculate_blend_cost(selected_blend.id)

                if cost_info:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**세부 원가**")
                        cost_details = f"""
                        - 원두 비용: ₩{cost_info.get('bean_cost_total', 0):,.0f}
                        - 로스팅 비용: ₩{cost_info.get('roasting_cost', 0):,.0f}
                        - 인건비: ₩{cost_info.get('labor_cost', 0):,.0f}
                        - 기타 비용: ₩{cost_info.get('misc_cost', 0):,.0f}
                        - **총 원가: ₩{cost_info['total_cost']:,.0f}**
                        """
                        st.write(cost_details)

                    with col2:
                        st.markdown("**포션당 원가**")
                        portion_details = f"""
                        - 포션당 원가: ₩{cost_info['cost_per_portion']:,.0f}
                        - 마진율: {cost_info['margin_rate']:.1f}배
                        - 제안 판매가: ₩{cost_info['suggested_price']:,.0f}
                        - **예상 이익**: ₩{cost_info['profit_margin']:,.0f}
                        """
                        st.write(portion_details)

                    # 비용 분포 차트
                    st.markdown("#### 📈 비용 구성")

                    cost_breakdown = [
                        cost_info.get('bean_cost_total', 0),
                        cost_info.get('roasting_cost', 0),
                        cost_info.get('labor_cost', 0),
                        cost_info.get('misc_cost', 0)
                    ]

                    fig_cost = go.Figure(data=[go.Bar(
                        x=["원두", "로스팅", "인건비", "기타"],
                        y=cost_breakdown,
                        marker_color=["#4472C4", "#70AD47", "#FFC000", "#5B9BD5"]
                    )])

                    fig_cost.update_layout(
                        title="비용 구성 비율",
                        xaxis_title="비용 항목",
                        yaxis_title="금액 (원)",
                        height=400,
                        showlegend=False
                    )

                    st.plotly_chart(fig_cost, use_container_width=True)

                else:
                    st.warning("원가 계산에 실패했습니다.")

    else:
        st.info("상세 정보를 볼 블렌드가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 블렌드 추가
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### ➕ 새 블렌드 추가")

    with st.form("add_blend_form"):
        col1, col2 = st.columns(2)

        with col1:
            blend_name = st.text_input("블렌드명", "")
            blend_type = st.selectbox("블렌드 타입", ["풀문", "뉴문", "시즈널"])

        with col2:
            description = st.text_input("설명", "")
            suggested_price = st.number_input("제안 판매가 (원)", min_value=0, value=0, step=1000)

        st.divider()

        st.markdown("#### 🌾 블렌드 레시피 구성")
        st.info("원두를 선택하고 포션을 입력하여 레시피를 구성하세요.")

        # 동적 레시피 입력
        recipes_input = []
        bean_list = bean_service.get_active_beans()

        if bean_list:
            num_beans = st.number_input("포함할 원두 개수", min_value=1, max_value=len(bean_list), value=2)

            recipe_cols = st.columns(2)

            for i in range(num_beans):
                with recipe_cols[i % 2]:
                    st.markdown(f"**원두 {i+1}**")

                    bean_name = st.selectbox(
                        f"원두 선택 {i+1}",
                        options=[b.name for b in bean_list],
                        key=f"bean_{i}"
                    )

                    portion = st.number_input(
                        f"포션 {i+1}",
                        min_value=1,
                        max_value=20,
                        value=1,
                        key=f"portion_{i}"
                    )

                    bean = next((b for b in bean_list if b.name == bean_name), None)
                    if bean:
                        recipes_input.append({
                            "bean_id": bean.id,
                            "bean_name": bean.name,
                            "portion_count": portion
                        })

        if st.form_submit_button("✅ 블렌드 추가", use_container_width=True):
            if not blend_name:
                st.error("❌ 블렌드명을 입력해주세요.")
            elif not recipes_input:
                st.error("❌ 최소 1개의 원두를 선택해주세요.")
            else:
                try:
                    total_portion = sum(r["portion_count"] for r in recipes_input)

                    blend_service.create_blend(
                        name=blend_name,
                        blend_type=blend_type,
                        description=description,
                        total_portion=total_portion,
                        suggested_price=suggested_price if suggested_price > 0 else None
                    )

                    # 최근 생성한 블렌드 가져오기
                    new_blend = blend_service.get_blend_by_name(blend_name)

                    if new_blend:
                        for recipe in recipes_input:
                            blend_service.add_recipe_to_blend(
                                new_blend.id,
                                recipe["bean_id"],
                                recipe["portion_count"]
                            )

                    st.success(f"✅ '{blend_name}' 블렌드가 추가되었습니다!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 블렌드 편집
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### ✏️ 블렌드 정보 편집")

    blends = blend_service.get_active_blends()

    if blends:
        blend_options = {b.name: b.id for b in blends}
        selected_name = st.selectbox("편집할 블렌드 선택", list(blend_options.keys()))

        if selected_name:
            selected_blend = blend_service.get_blend_by_id(blend_options[selected_name])

            with st.form("edit_blend_form"):
                col1, col2 = st.columns(2)

                with col1:
                    new_name = st.text_input("블렌드명", value=selected_blend.name)
                    new_type = st.selectbox(
                        "블렌드 타입",
                        ["풀문", "뉴문", "시즈널"],
                        index=["풀문", "뉴문", "시즈널"].index(selected_blend.blend_type)
                    )

                with col2:
                    new_description = st.text_input("설명", value=selected_blend.description or "")
                    new_suggested_price = st.number_input(
                        "제안 판매가 (원)",
                        value=int(selected_blend.suggested_price) if selected_blend.suggested_price else 0,
                        min_value=0,
                        step=1000
                    )

                if st.form_submit_button("✅ 저장", use_container_width=True):
                    try:
                        blend_service.update_blend(
                            selected_blend.id,
                            name=new_name,
                            blend_type=new_type,
                            description=new_description,
                            suggested_price=new_suggested_price if new_suggested_price > 0 else None
                        )
                        st.success("✅ 블렌드 정보가 업데이트되었습니다!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")

            # 레시피 편집
            st.divider()
            st.markdown("#### 🌾 레시피 편집")

            recipes = blend_service.get_blend_recipes(selected_blend.id)

            if recipes:
                st.info("현재 레시피:")

                recipe_data = []
                for recipe in recipes:
                    bean = bean_service.get_bean_by_id(recipe.bean_id)
                    if bean:
                        recipe_data.append({
                            "원두": bean.name,
                            "포션": recipe.portion_count,
                            "ID": recipe.id
                        })

                if recipe_data:
                    df_recipes = pd.DataFrame(recipe_data)
                    st.dataframe(df_recipes, use_container_width=True, hide_index=True)

                    st.divider()
                    st.markdown("#### ✏️ 레시피 수정")

                    # 수정할 레시피 선택
                    recipe_names = [f"{r['원두']} ({r['포션']}포션)" for r in recipe_data]
                    selected_recipe_idx = st.selectbox(
                        "수정할 레시피 선택",
                        range(len(recipe_data)),
                        format_func=lambda i: recipe_names[i],
                        key="recipe_edit_select"
                    )

                    selected_recipe = recipes[selected_recipe_idx]
                    selected_bean = bean_service.get_bean_by_id(selected_recipe.bean_id)

                    # 수정 폼
                    col1, col2 = st.columns(2)

                    with col1:
                        # 새로운 원두 선택
                        available_beans = bean_service.get_active_beans()
                        bean_options = {bean.id: f"{bean.name} ({bean.country_code})" for bean in available_beans}
                        new_bean_id = st.selectbox(
                            "원두 변경",
                            options=list(bean_options.keys()),
                            format_func=lambda bid: bean_options[bid],
                            index=list(bean_options.keys()).index(selected_bean.id) if selected_bean.id in bean_options else 0,
                            key="recipe_bean_select"
                        )

                    with col2:
                        # 포션 수 수정
                        new_portion = st.number_input(
                            "포션 개수",
                            min_value=1,
                            max_value=20,
                            value=selected_recipe.portion_count,
                            step=1,
                            key="recipe_portion_input"
                        )

                    # 저장 버튼
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("💾 레시피 수정 저장", use_container_width=True, type="primary", key="save_recipe_edit"):
                            try:
                                # 기존 레시피 삭제
                                blend_service.remove_recipe_from_blend(selected_blend.id, selected_recipe.bean_id)

                                # 새로운 레시피 추가
                                blend_service.add_recipe_to_blend(selected_blend.id, new_bean_id, new_portion)

                                st.success(f"✅ 레시피가 수정되었습니다!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 오류: {str(e)}")

                    with col2:
                        if st.button("🗑️ 레시피 삭제", use_container_width=True, type="secondary", key="delete_recipe"):
                            try:
                                blend_service.remove_recipe_from_blend(selected_blend.id, selected_recipe.bean_id)
                                st.success("✅ 레시피가 삭제되었습니다!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 오류: {str(e)}")

            else:
                st.warning("현재 이 블렌드에 레시피가 없습니다.")

            # 삭제 버튼
            st.divider()
            st.markdown("#### 🗑️ 위험한 작업")

            if st.button("🗑️ 이 블렌드 삭제 (비활성화)", use_container_width=True, type="secondary"):
                try:
                    blend_service.delete_blend(selected_blend.id)
                    st.success("✅ 블렌드가 비활성화되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")

    else:
        st.info("편집할 블렌드가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# 데이터 내보내기 (하단)
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("#### 📥 데이터 내보내기")

blends = blend_service.get_active_blends()

if blends:
    export_data = []
    for blend in blends:
        cost_info = blend_service.calculate_blend_cost(blend.id)
        export_data.append({
            "ID": blend.id,
            "블렌드명": blend.name,
            "타입": blend.blend_type,
            "포션": blend.total_portion,
            "포션당 원가": cost_info['cost_per_portion'] if cost_info else 0,
            "제안 가격": blend.suggested_price or 0,
            "설명": blend.description or ""
        })

    df_export = pd.DataFrame(export_data)
    csv = df_export.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="📥 CSV로 다운로드",
        data=csv,
        file_name="블렌드_목록.csv",
        mime="text/csv"
    )
