"""
원가 계산 페이지

블렌드 원가 계산, 원두 가격 관리, 비용 설정 및 마진율 분석 기능 제공
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.services.cost_service import CostService
from app.services.bean_service import BeanService
from app.services.blend_service import BlendService
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

db = st.session_state.db
bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바 렌더링
# ═══════════════════════════════════════════════════════════════════════════════

render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 헤더
# ═══════════════════════════════════════════════════════════════════════════════

# 현재 페이지 설정 (사이드바 활성 표시)
st.session_state["current_page"] = "CostCalculation"

st.title("🧮 원가 계산")
st.markdown("블렌드 원가를 계산하고 원두 가격을 관리하며 비용 설정을 조정합니다.")
st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 생성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 원가 계산",
    "📊 일괄 비교",
    "💰 원두 가격 관리",
    "⚙️ 비용 설정"
])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 원가 계산
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 🧮 블렌드 원가 계산")
    st.markdown("선택한 블렌드의 상세 원가를 계산하고 분석합니다.")

    # 블렌드 목록 조회
    blends = blend_service.get_active_blends()

    if not blends:
        st.warning("⚠️ 활성 블렌드가 없습니다. 먼저 블렌드를 등록해주세요.")
    else:
        # 블렌드 선택 및 단위 선택
        col1, col2 = st.columns([3, 1])

        with col1:
            blend_options = {f"{b.name} ({b.blend_type})": b.id for b in blends}
            selected_blend_name = st.selectbox(
                "블렌드 선택",
                options=list(blend_options.keys()),
                key="cost_calc_blend_select"
            )
            selected_blend_id = blend_options[selected_blend_name]

        with col2:
            unit = st.radio(
                "계산 단위",
                options=["kg", "cup"],
                horizontal=True,
                key="cost_calc_unit"
            )

        # 원가 계산
        try:
            cost_data = CostService.get_blend_cost(db, selected_blend_id, unit=unit)

            # 메트릭 카드 (4개)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    label="혼합 원가",
                    value=f"{cost_data['blend_cost_before_loss']:,.0f}원",
                    help="손실률 반영 전 원두 혼합 원가"
                )

            with col2:
                st.metric(
                    label=f"최종 원가 (/{unit})",
                    value=f"{cost_data['final_cost_per_unit']:,.0f}원",
                    help=f"손실률 {cost_data['loss_rate']:.1f}% 반영 후 최종 원가"
                )

            with col3:
                if cost_data['selling_price']:
                    st.metric(
                        label="제안 판매가",
                        value=f"{cost_data['selling_price']:,.0f}원",
                        help="블렌드에 설정된 제안 판매가"
                    )
                else:
                    st.metric(
                        label="제안 판매가",
                        value="미설정",
                        help="판매가가 설정되지 않았습니다"
                    )

            with col4:
                if cost_data['margin_percent']:
                    margin_color = "🟢" if cost_data['margin_percent'] > 50 else "🟡" if cost_data['margin_percent'] > 30 else "🔴"
                    st.metric(
                        label="마진율",
                        value=f"{margin_color} {cost_data['margin_percent']:.1f}%",
                        help="(판매가 - 최종원가) / 판매가 × 100"
                    )
                else:
                    st.metric(
                        label="마진율",
                        value="N/A",
                        help="판매가가 없어 계산 불가"
                    )

            st.divider()

            # 원두 구성 테이블
            st.markdown("#### 📋 원두 구성")

            if cost_data['component_costs']:
                df_components = pd.DataFrame(cost_data['component_costs'])
                df_components = df_components.rename(columns={
                    'bean_name': '원두명',
                    'ratio': '비율(%)',
                    'price_per_kg': '단가(원/kg)',
                    'component_cost': '기여도(원)'
                })

                # 최종 기여도 계산
                loss_rate = CostService.STANDARD_LOSS_RATE
                df_components['최종 기여도(원)'] = (df_components['기여도(원)'] / (1 - loss_rate)).round(0)

                # 포맷팅
                df_components['단가(원/kg)'] = df_components['단가(원/kg)'].apply(lambda x: f"{x:,.0f}")
                df_components['기여도(원)'] = df_components['기여도(원)'].apply(lambda x: f"{x:,.0f}")
                df_components['최종 기여도(원)'] = df_components['최종 기여도(원)'].apply(lambda x: f"{x:,.0f}")

                st.dataframe(
                    df_components,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("⚠️ 레시피 정보가 없습니다.")

            # 계산 공식 설명 (expander)
            with st.expander("📐 원가 계산 공식"):
                st.markdown(f"""
                **1단계: 혼합 원가 계산**
                ```
                혼합 원가 = Σ (원두 단가 × 비율%)
                         = {' + '.join([f"{c['price_per_kg']}원 × {c['ratio']}%" for c in cost_data['component_costs']])}
                         = {cost_data['blend_cost_before_loss']:,.0f}원
                ```

                **2단계: 손실률 반영**
                ```
                최종 원가 = 혼합 원가 / (1 - 손실률)
                         = {cost_data['blend_cost_before_loss']:,.0f}원 / (1 - {cost_data['loss_rate'] / 100:.2f})
                         = {cost_data['final_cost_per_kg']:,.0f}원/kg
                ```

                **3단계: 단위 변환 (cup 선택 시)**
                ```
                1 cup = 200g = 0.2kg
                최종 원가/cup = {cost_data['final_cost_per_kg']:,.0f}원/kg × 0.2
                              = {cost_data['final_cost_per_unit']:,.0f}원/cup
                ```

                **4단계: 마진율 계산**
                ```
                마진율 = (판매가 - 최종원가) / 판매가 × 100
                      = ({cost_data['selling_price'] if cost_data['selling_price'] else 0:,.0f} - {cost_data['final_cost_per_kg']:,.0f}) / {cost_data['selling_price'] if cost_data['selling_price'] else 0:,.0f} × 100
                      = {cost_data['margin_percent']:.1f}% if cost_data['margin_percent'] else 'N/A'
                ```
                """)

        except Exception as e:
            st.error(f"❌ 원가 계산 오류: {str(e)}")
            st.exception(e)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 일괄 비교
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 📊 블렌드 일괄 비교")
    st.markdown("모든 블렌드의 원가를 일괄 계산하여 비교 분석합니다.")

    # 일괄 계산 버튼
    if st.button("🔄 모든 블렌드 원가 일괄 계산", key="batch_calc_btn", use_container_width=True):
        with st.spinner("계산 중..."):
            try:
                # 일괄 계산 실행
                results = CostService.batch_calculate_all_blends(db)

                if results:
                    # 에러가 있는 결과 필터링
                    success_results = [r for r in results if 'error' not in r]
                    error_results = [r for r in results if 'error' in r]

                    # 성공 결과 표시
                    if success_results:
                        # DataFrame 생성
                        df_results = pd.DataFrame(success_results)

                        # 필요한 컬럼 선택 및 이름 변경
                        df_display = pd.DataFrame({
                            '블렌드명': df_results['blend_name'],
                            '혼합원가(원)': df_results['blend_cost_before_loss'].apply(lambda x: f"{x:,.0f}"),
                            '최종원가(원/kg)': df_results['final_cost_per_kg'].apply(lambda x: f"{x:,.0f}"),
                            '판매가(원)': df_results['selling_price'].apply(lambda x: f"{x:,.0f}" if x else "미설정"),
                            '마진율(%)': df_results['margin_percent'].apply(lambda x: f"{x:.1f}" if x else "N/A"),
                            '손실률(%)': df_results['loss_rate']
                        })

                        # 정렬 옵션
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            sort_by = st.selectbox(
                                "정렬 기준",
                                options=["블렌드명", "혼합원가(원)", "최종원가(원/kg)", "마진율(%)"],
                                key="batch_sort_by"
                            )

                        # 테이블 표시
                        st.dataframe(df_display, use_container_width=True, hide_index=True)

                        st.success(f"✅ {len(success_results)}개 블렌드 계산 완료")

                        # 차트 표시
                        st.divider()

                        # 차트 1: 원가 비교 (Bar Chart)
                        st.markdown("#### 📊 블렌드별 원가 비교")

                        fig1 = px.bar(
                            df_results,
                            x='blend_name',
                            y=['blend_cost_before_loss', 'final_cost_per_kg'],
                            title="블렌드별 혼합원가 vs 최종원가",
                            labels={
                                'blend_name': '블렌드명',
                                'value': '원가 (원)',
                                'variable': '구분'
                            },
                            barmode='group',
                            color_discrete_sequence=['#1f77b4', '#ff7f0e']
                        )

                        # 범례 이름 변경
                        fig1.for_each_trace(lambda t: t.update(name='혼합원가' if t.name == 'blend_cost_before_loss' else '최종원가'))

                        fig1.update_layout(
                            xaxis_title="",
                            yaxis_title="원가 (원)",
                            legend_title="",
                            hovermode='x unified'
                        )

                        st.plotly_chart(fig1, use_container_width=True)

                        # 차트 2: 마진율 비교 (Bar Chart)
                        st.markdown("#### 💰 블렌드별 마진율 비교")

                        # 마진율이 있는 데이터만 필터링
                        df_with_margin = df_results[df_results['margin_percent'].notna()].copy()

                        if not df_with_margin.empty:
                            # 마진율에 따른 색상 지정
                            df_with_margin['color'] = df_with_margin['margin_percent'].apply(
                                lambda x: '🟢 높음 (50%+)' if x > 50 else '🟡 보통 (30-50%)' if x > 30 else '🔴 낮음 (<30%)'
                            )

                            fig2 = px.bar(
                                df_with_margin,
                                x='blend_name',
                                y='margin_percent',
                                title="블렌드별 마진율",
                                labels={
                                    'blend_name': '블렌드명',
                                    'margin_percent': '마진율 (%)',
                                    'color': '상태'
                                },
                                color='color',
                                color_discrete_map={
                                    '🟢 높음 (50%+)': '#2ecc71',
                                    '🟡 보통 (30-50%)': '#f39c12',
                                    '🔴 낮음 (<30%)': '#e74c3c'
                                }
                            )

                            fig2.update_layout(
                                xaxis_title="",
                                yaxis_title="마진율 (%)",
                                legend_title="",
                                hovermode='x'
                            )

                            st.plotly_chart(fig2, use_container_width=True)
                        else:
                            st.info("ℹ️ 판매가가 설정된 블렌드가 없어 마진율을 표시할 수 없습니다.")

                    # 에러 결과 표시
                    if error_results:
                        st.warning(f"⚠️ {len(error_results)}개 블렌드 계산 실패")
                        with st.expander("실패한 블렌드 보기"):
                            for err in error_results:
                                st.error(f"- {err['blend_name']}: {err['error']}")

                else:
                    st.warning("⚠️ 계산할 블렌드가 없습니다.")

            except Exception as e:
                st.error(f"❌ 일괄 계산 오류: {str(e)}")
                st.exception(e)
    else:
        st.info("👆 위 버튼을 클릭하여 모든 블렌드의 원가를 계산하세요.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 원두 가격 관리
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### 💰 원두 가격 관리")
    st.markdown("원두 가격을 조회하고 수정합니다.")

    # 원두 목록 조회
    beans = bean_service.get_active_beans()

    if not beans:
        st.warning("⚠️ 등록된 원두가 없습니다.")
    else:
        # 원두 목록 테이블
        st.markdown("#### 📋 원두 가격 목록")

        df_beans = pd.DataFrame([{
            '원두명': b.name,
            '국가': b.country_code or "-",
            '로스팅': b.roast_level,
            '현재 가격(원/kg)': f"{b.price_per_kg:,.0f}",
            '상태': b.status
        } for b in beans])

        st.dataframe(df_beans, use_container_width=True, hide_index=True)

        st.divider()

        # 가격 수정 폼
        st.markdown("#### ✏️ 가격 수정")

        with st.form("bean_price_update_form"):
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                bean_options = {b.name: b.id for b in beans}
                selected_bean_name = st.selectbox(
                    "원두 선택",
                    options=list(bean_options.keys()),
                    key="bean_price_select"
                )
                selected_bean_id = bean_options[selected_bean_name]

            with col2:
                selected_bean = next(b for b in beans if b.id == selected_bean_id)
                new_price = st.number_input(
                    "새 가격 (원/kg)",
                    min_value=100,
                    max_value=50000,
                    value=int(selected_bean.price_per_kg),
                    step=100,
                    key="bean_new_price"
                )

            with col3:
                st.write("")  # 공백
                st.write("")  # 공백
                submit_btn = st.form_submit_button("💾 가격 업데이트", use_container_width=True)

            if submit_btn:
                try:
                    updated_bean = CostService.update_bean_price(db, selected_bean_id, new_price)
                    st.success(f"✅ {updated_bean.name}의 가격이 {new_price:,.0f}원/kg로 업데이트되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 가격 업데이트 실패: {str(e)}")

        # 히스토리는 추후 추가 (간소화)
        with st.expander("💡 가격 변경 히스토리 (향후 추가 예정)"):
            st.info("가격 변경 이력 추적 기능은 향후 업데이트 예정입니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 비용 설정
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### ⚙️ 비용 설정")
    st.markdown("손실률 및 각종 비용 파라미터를 설정합니다.")

    st.info("ℹ️ 현재 CostService의 STANDARD_LOSS_RATE (17%)가 사용됩니다. 사용자 정의 설정은 향후 CostSetting 테이블 연동을 통해 제공됩니다.")

    # 현재 설정 표시
    st.markdown("#### 📊 현재 적용 중인 설정")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="손실률",
            value=f"{CostService.STANDARD_LOSS_RATE * 100:.1f}%",
            help="로스팅 과정에서의 표준 손실률"
        )

    with col2:
        st.metric(
            label="적용 대상",
            value="모든 블렌드",
            help="현재 모든 블렌드에 동일한 손실률이 적용됩니다"
        )

    st.divider()

    st.markdown("#### ⚙️ 비용 파라미터 설정 (향후 추가)")

    # 간소화된 설정 UI (향후 확장)
    with st.form("cost_settings_form"):
        st.markdown("##### 🔧 고급 설정 (향후 구현)")

        loss_rate = st.slider(
            "손실률 (%)",
            min_value=0.0,
            max_value=50.0,
            value=17.0,
            step=0.1,
            help="로스팅 시 발생하는 무게 손실률",
            disabled=True  # 현재는 비활성화
        )

        col1, col2 = st.columns(2)

        with col1:
            roasting_cost = st.number_input(
                "로스팅 비용 (원/kg)",
                min_value=0,
                max_value=10000,
                value=500,
                step=100,
                disabled=True  # 현재는 비활성화
            )

            labor_cost = st.number_input(
                "인건비 (원/batch)",
                min_value=0,
                max_value=100000,
                value=10000,
                step=1000,
                disabled=True  # 현재는 비활성화
            )

        with col2:
            electric_cost = st.number_input(
                "전기료 (원/batch)",
                min_value=0,
                max_value=50000,
                value=3000,
                step=500,
                disabled=True  # 현재는 비활성화
            )

            misc_cost = st.number_input(
                "기타 비용 (원/kg)",
                min_value=0,
                max_value=5000,
                value=200,
                step=100,
                disabled=True  # 현재는 비활성화
            )

        st.divider()

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            save_btn = st.form_submit_button("💾 설정 저장", disabled=True)

        with col2:
            reset_btn = st.form_submit_button("↺ 기본값 복원", disabled=True)

        if save_btn:
            st.warning("⚠️ 설정 저장 기능은 향후 업데이트 예정입니다.")

        if reset_btn:
            st.info("ℹ️ 기본값 복원 기능은 향후 업데이트 예정입니다.")

    st.markdown("---")
    st.caption("💡 **참고**: 고급 비용 설정 기능은 CostSetting 모델 연동 후 활성화됩니다.")
