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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 투입량 계산기",
    "🧮 원가 계산",
    "📊 일괄 비교",
    "💰 원두 가격 관리",
    "⚙️ 비용 설정"
])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 투입량 계산기 (신규)
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    from app.services.cost_calculator_service import CostCalculatorService

    st.markdown("### 📐 투입량 계산기")
    st.markdown("목표 산출량(원두)을 입력하면 필요한 생두 투입량을 계산합니다.")

    # 서비스 초기화
    calculator_service = CostCalculatorService(db)

    col1, col2 = st.columns([2, 1])

    with col1:
        # 원두 선택
        beans = bean_service.get_active_beans()
        bean_options = {f"{bean.name} ({bean.country_name})": bean.id for bean in beans}
        bean_options["전체 평균 사용"] = None

        selected_bean_name = st.selectbox(
            "☕ 원두 선택",
            options=list(bean_options.keys()),
            help="특정 원두를 선택하면 해당 원두의 평균 손실률을 사용합니다"
        )
        selected_bean_id = bean_options[selected_bean_name]

    with col2:
        # 안전 여유율 설정
        safety_margin = st.number_input(
            "✨ 안전 여유율 (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
            help="배치 편차를 고려한 여유분"
        ) / 100

    # 목표 산출량 입력
    target_output = st.number_input(
        "🎯 목표 산출량 (kg)",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5,
        help="로스팅 후 얻고자 하는 원두의 무게"
    )

    # 계산 버튼
    if st.button("📊 투입량 계산", type="primary", use_container_width=True):
        with st.spinner("계산 중..."):
            result = calculator_service.calculate_required_input(
                target_output_kg=target_output,
                bean_id=selected_bean_id,
                safety_margin=safety_margin
            )

            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                st.divider()

                # 통계 정보 표시
                st.markdown("### 📊 원두 손실률 통계")

                stat_col1, stat_col2, stat_col3 = st.columns(3)

                with stat_col1:
                    st.metric(
                        "평균 손실률",
                        f"{result['avg_loss_rate']:.2f}%",
                        help="최근 로스팅 기록 기반"
                    )

                with stat_col2:
                    st.metric(
                        "표준편차",
                        f"±{result['std_loss_rate']:.2f}%",
                        help="손실률의 변동 폭"
                    )

                with stat_col3:
                    st.metric(
                        "로스팅 횟수",
                        f"{result['sample_count']}회",
                        help="통계 계산에 사용된 데이터"
                    )

                if result.get('warning'):
                    st.warning(f"⚠️ {result['warning']}")

                st.divider()

                # 계산 결과
                st.markdown("### 💡 계산 결과")

                # 주요 결과 (큰 카드)
                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                        <h4 style='margin: 0; color: #555;'>기본 투입량</h4>
                        <h2 style='margin: 10px 0; color: #1f77b4;'>{result['calculated_input']:.2f} kg</h2>
                        <p style='margin: 0; color: #777; font-size: 14px;'>손실률만 고려한 계산값</p>
                    </div>
                    """, unsafe_allow_html=True)

                with result_col2:
                    st.markdown(f"""
                    <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; text-align: center;'>
                        <h4 style='margin: 0; color: #555;'>⭐ 권장 투입량</h4>
                        <h2 style='margin: 10px 0; color: #2e7d32;'>{result['recommended_input']:.2f} kg</h2>
                        <p style='margin: 0; color: #777; font-size: 14px;'>여유 {safety_margin*100:.1f}% 포함 ({result['safety_margin_kg']:.2f}kg)</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()

                # 예상 산출량 범위
                st.markdown("### 📦 예상 산출량 범위")
                st.markdown(f"권장 투입량({result['recommended_input']:.2f}kg)으로 로스팅 시 예상되는 결과:")

                range_col1, range_col2, range_col3 = st.columns(3)

                with range_col1:
                    st.metric(
                        "최소 예상",
                        f"{result['min_output']:.2f} kg",
                        delta=f"{result['min_output'] - target_output:.2f}kg",
                        delta_color="off"
                    )

                with range_col2:
                    st.metric(
                        "평균 예상",
                        f"{result['expected_output']:.2f} kg",
                        delta=f"{result['expected_output'] - target_output:.2f}kg",
                        delta_color="normal"
                    )

                with range_col3:
                    st.metric(
                        "최대 예상",
                        f"{result['max_output']:.2f} kg",
                        delta=f"{result['max_output'] - target_output:.2f}kg",
                        delta_color="normal"
                    )

                # 도움말
                with st.expander("ℹ️ 계산 방법 및 해석"):
                    st.markdown(f"""
                    **계산 공식:**
                    - 기본 투입량 = 목표 산출량 ÷ (1 - 평균 손실률)
                    - 권장 투입량 = 기본 투입량 × (1 + 안전 여유율)

                    **예상 범위 계산:**
                    - 손실률 범위: {result['avg_loss_rate'] - result['std_loss_rate']:.2f}% ~ {result['avg_loss_rate'] + result['std_loss_rate']:.2f}%
                    - 이 범위 내에서 약 68%의 로스팅 결과가 나옵니다 (1 표준편차)

                    **권장사항:**
                    - 목표량을 정확히 맞추려면 "권장 투입량"을 사용하세요
                    - 여유율은 배치마다 다를 수 있는 변동을 고려한 값입니다
                    - 로스팅 횟수가 많을수록 통계가 정확해집니다
                    """)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 원가 계산
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
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
# Tab 3: 일괄 비교
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
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
# Tab 4: 원두 가격 관리
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
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
            col1, col2 = st.columns([2, 2])

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

            # 변경 사유 (선택사항)
            change_reason = st.text_input(
                "변경 사유 (선택사항)",
                placeholder="예: 생두 가격 인상, 환율 변동, 품질 향상 등",
                key="bean_price_change_reason"
            )

            submit_btn = st.form_submit_button("💾 가격 업데이트", use_container_width=True)

            if submit_btn:
                try:
                    reason = change_reason if change_reason.strip() else None
                    updated_bean = CostService.update_bean_price(db, selected_bean_id, new_price, reason)
                    st.success(f"✅ {updated_bean.name}의 가격이 {new_price:,.0f}원/kg로 업데이트되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 가격 업데이트 실패: {str(e)}")

        st.divider()

        # 가격 변경 이력
        st.markdown("#### 📜 가격 변경 이력")

        # 이력 조회 설정
        col1, col2 = st.columns([3, 1])
        with col1:
            history_bean_name = st.selectbox(
                "이력 조회할 원두 선택",
                options=list(bean_options.keys()),
                key="history_bean_select"
            )
            history_bean_id = bean_options[history_bean_name]

        with col2:
            history_limit = st.number_input(
                "조회 개수",
                min_value=5,
                max_value=100,
                value=10,
                step=5,
                key="history_limit"
            )

        try:
            history = CostService.get_bean_price_history(db, history_bean_id, int(history_limit))

            if not history:
                st.info(f"ℹ️ {history_bean_name}의 가격 변경 이력이 없습니다.")
            else:
                # 이력 테이블
                st.markdown(f"**총 {len(history)}개의 변경 이력**")

                df_history = pd.DataFrame([{
                    '변경일시': h['created_at'].strftime('%Y-%m-%d %H:%M'),
                    '이전 가격': f"{h['old_price']:,.0f}원",
                    '새 가격': f"{h['new_price']:,.0f}원",
                    '변동액': f"{h['price_change']:+,.0f}원",
                    '변동률': f"{h['price_change_percent']:+.1f}%",
                    '변경 사유': h['change_reason'] or "-"
                } for h in history])

                st.dataframe(df_history, use_container_width=True, hide_index=True)

                st.divider()

                # 가격 변동 타임라인 차트
                st.markdown("**📊 가격 변동 추이**")

                # 차트 데이터 준비 (시간순 정렬 - 오래된 것부터)
                chart_data = sorted(history, key=lambda x: x['created_at'])

                # 가격 변동 포인트 (old_price와 new_price 모두 표시)
                dates = []
                prices = []
                labels = []

                for h in chart_data:
                    # old_price 포인트
                    dates.append(h['created_at'])
                    prices.append(h['old_price'])
                    labels.append(f"변경 전: {h['old_price']:,.0f}원")

                    # new_price 포인트
                    dates.append(h['created_at'])
                    prices.append(h['new_price'])
                    change_icon = "📈" if h['price_change'] > 0 else "📉" if h['price_change'] < 0 else "➡️"
                    labels.append(f"변경 후: {h['new_price']:,.0f}원 {change_icon}")

                # Plotly 라인 차트
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=dates,
                    y=prices,
                    mode='lines+markers',
                    name='가격',
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=8, color='#1f77b4'),
                    text=labels,
                    hovertemplate='%{text}<br>%{x|%Y-%m-%d %H:%M}<extra></extra>'
                ))

                fig.update_layout(
                    title=f"{history_bean_name} 가격 변동 추이",
                    xaxis_title="변경일시",
                    yaxis_title="가격 (원/kg)",
                    hovermode='closest',
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ 이력 조회 실패: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 5: 비용 설정
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("### ⚙️ 비용 설정")
    st.markdown("손실률 및 각종 비용 파라미터를 설정합니다.")

    # 현재 설정값 불러오기
    try:
        current_loss_rate = CostService.get_cost_setting(db, "loss_rate_percent") or (CostService.STANDARD_LOSS_RATE * 100)
        current_roasting_cost = CostService.get_cost_setting(db, "roasting_cost_per_kg") or 500
        current_labor_cost = CostService.get_cost_setting(db, "labor_cost_per_batch") or 10000
        current_electric_cost = CostService.get_cost_setting(db, "electric_cost_per_batch") or 3000
        current_misc_cost = CostService.get_cost_setting(db, "misc_cost_per_kg") or 200
    except Exception as e:
        st.error(f"❌ 설정값 불러오기 실패: {str(e)}")
        current_loss_rate = 17.0
        current_roasting_cost = 500
        current_labor_cost = 10000
        current_electric_cost = 3000
        current_misc_cost = 200

    # 현재 설정 표시
    st.markdown("#### 📊 현재 적용 중인 설정")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="손실률",
            value=f"{current_loss_rate:.1f}%",
            help="로스팅 과정에서의 손실률"
        )

    with col2:
        st.metric(
            label="로스팅 비용",
            value=f"{current_roasting_cost:,.0f}원/kg",
            help="로스팅 작업 비용"
        )

    with col3:
        st.metric(
            label="인건비",
            value=f"{current_labor_cost:,.0f}원",
            help="배치당 인건비"
        )

    with col4:
        st.metric(
            label="전기료",
            value=f"{current_electric_cost:,.0f}원",
            help="배치당 전기료"
        )

    st.divider()

    st.markdown("#### ⚙️ 비용 파라미터 설정")

    # 설정 UI
    with st.form("cost_settings_form"):
        st.markdown("##### 🔧 비용 설정 변경")

        loss_rate = st.slider(
            "손실률 (%)",
            min_value=0.0,
            max_value=50.0,
            value=float(current_loss_rate),
            step=0.1,
            help="로스팅 시 발생하는 무게 손실률 (일반적으로 15~20%)"
        )

        col1, col2 = st.columns(2)

        with col1:
            roasting_cost = st.number_input(
                "로스팅 비용 (원/kg)",
                min_value=0,
                max_value=10000,
                value=int(current_roasting_cost),
                step=100,
                help="kg당 로스팅 작업 비용"
            )

            labor_cost = st.number_input(
                "인건비 (원/batch)",
                min_value=0,
                max_value=100000,
                value=int(current_labor_cost),
                step=1000,
                help="로스팅 배치당 인건비"
            )

        with col2:
            electric_cost = st.number_input(
                "전기료 (원/batch)",
                min_value=0,
                max_value=50000,
                value=int(current_electric_cost),
                step=500,
                help="로스팅 배치당 전기료"
            )

            misc_cost = st.number_input(
                "기타 비용 (원/kg)",
                min_value=0,
                max_value=5000,
                value=int(current_misc_cost),
                step=100,
                help="포장비, 소모품 등 기타 비용"
            )

        st.divider()

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            save_btn = st.form_submit_button("💾 설정 저장", use_container_width=True)

        with col2:
            reset_btn = st.form_submit_button("↺ 기본값 복원", use_container_width=True)

        if save_btn:
            try:
                # 설정값 저장
                CostService.update_cost_setting(db, "loss_rate_percent", loss_rate, "로스팅 손실률 (%)")
                CostService.update_cost_setting(db, "roasting_cost_per_kg", roasting_cost, "kg당 로스팅 비용 (원)")
                CostService.update_cost_setting(db, "labor_cost_per_batch", labor_cost, "배치당 인건비 (원)")
                CostService.update_cost_setting(db, "electric_cost_per_batch", electric_cost, "배치당 전기료 (원)")
                CostService.update_cost_setting(db, "misc_cost_per_kg", misc_cost, "kg당 기타 비용 (원)")

                st.success("✅ 비용 설정이 성공적으로 저장되었습니다.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 설정 저장 실패: {str(e)}")

        if reset_btn:
            try:
                # 기본값으로 복원
                CostService.update_cost_setting(db, "loss_rate_percent", 17.0, "로스팅 손실률 (%)")
                CostService.update_cost_setting(db, "roasting_cost_per_kg", 500, "kg당 로스팅 비용 (원)")
                CostService.update_cost_setting(db, "labor_cost_per_batch", 10000, "배치당 인건비 (원)")
                CostService.update_cost_setting(db, "electric_cost_per_batch", 3000, "배치당 전기료 (원)")
                CostService.update_cost_setting(db, "misc_cost_per_kg", 200, "kg당 기타 비용 (원)")

                st.success("✅ 기본값으로 복원되었습니다.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 기본값 복원 실패: {str(e)}")

    st.markdown("---")

    # 설정 정보
    with st.expander("ℹ️ 비용 설정 안내"):
        st.markdown("""
        **손실률 (Loss Rate)**
        - 로스팅 과정에서 생두의 수분이 증발하여 발생하는 무게 감소
        - 일반적으로 15~20% 범위
        - 높을수록 최종 원가가 상승

        **로스팅 비용**
        - 로스터 기계 운영 및 유지보수 비용
        - kg당 비용으로 계산

        **인건비**
        - 로스팅 작업자 인건비
        - 배치(batch)당 비용으로 계산

        **전기료**
        - 로스터 기계 전력 소비 비용
        - 배치당 비용으로 계산

        **기타 비용**
        - 포장재, 소모품, 운송비 등
        - kg당 비용으로 계산
        """)

    st.caption("💡 **참고**: 설정값은 CostSetting 테이블에 저장되며, 원가 계산 시 참고 자료로 활용됩니다.")
