"""
Excel 동기화 페이지
Excel 파일에서 데이터 임포트 및 내보내기
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.bean_service import BeanService
from services.blend_service import BlendService
from services.excel_service import ExcelService

st.set_page_config(page_title="Excel동기화", page_icon="📊", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

if "blend_service" not in st.session_state:
    st.session_state.blend_service = BlendService(st.session_state.db)

if "excel_service" not in st.session_state:
    st.session_state.excel_service = ExcelService(st.session_state.db)

db = st.session_state.db
bean_service = st.session_state.bean_service
blend_service = st.session_state.blend_service
excel_service = st.session_state.excel_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📊 Excel 동기화</h1>", unsafe_allow_html=True)
st.markdown("Excel 파일에서 데이터를 임포트하거나 내보냅니다.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📥 임포트", "📤 내보내기", "📋 템플릿"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 임포트
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📥 데이터 임포트")

    st.info("""
    Excel 파일에서 데이터를 읽어 데이터베이스에 추가합니다.
    이미 존재하는 데이터는 업데이트됩니다.
    """)

    st.divider()

    # 임포트 대상 선택
    import_type = st.selectbox(
        "임포트할 데이터 유형",
        options=["beans", "blends"],
        format_func=lambda x: {
            "beans": "☕ 원두 데이터",
            "blends": "🎨 블렌드 데이터"
        }.get(x, x)
    )

    st.divider()

    # 파일 업로드
    st.markdown("#### 📁 파일 선택")

    uploaded_file = st.file_uploader(
        "Excel 파일 선택 (.xlsx, .xls)",
        type=["xlsx", "xls"],
        help="임포트할 Excel 파일을 선택하세요."
    )

    if uploaded_file:
        st.info(f"선택된 파일: {uploaded_file.name}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**파일 정보**")
            st.write(f"파일명: {uploaded_file.name}")
            st.write(f"파일크기: {uploaded_file.size / 1024:.1f} KB")

        with col2:
            st.markdown("**임포트 옵션**")

            merge_existing = st.checkbox(
                "기존 데이터 병합 (기존 데이터 업데이트)",
                value=True
            )

        st.divider()

        # 임포트 버튼
        if st.button("✅ 임포트 실행", use_container_width=True, type="primary"):
            with st.spinner("임포트 중..."):
                try:
                    file_bytes = uploaded_file.read()

                    if import_type == "beans":
                        result = excel_service.import_beans_from_excel(file_bytes)
                        success_text = "원두"
                    else:  # blends
                        result = excel_service.import_blends_from_excel(file_bytes)
                        success_text = "블렌드"

                    if result["success"]:
                        st.success(f"""
                        ✅ {success_text} 임포트 완료!

                        **결과:**
                        - 성공: {result['imported_count']}개
                        - 오류: {result['error_count']}개
                        """)

                        if result['error_count'] > 0:
                            st.warning("**오류 목록:**")
                            for error in result['errors']:
                                st.write(f"- {error}")

                    else:
                        st.error(f"❌ 임포트 실패: {result['error']}")

                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 내보내기
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 📤 데이터 내보내기")

    st.info("""
    현재 데이터를 Excel 형식으로 내보냅니다.
    각 데이터 유형별로 다른 파일로 내보낼 수 있습니다.
    """)

    st.divider()

    # 내보내기 옵션
    st.markdown("#### 📋 내보내기 대상")

    col1, col2 = st.columns(2)

    with col1:
        # 원두 내보내기
        st.markdown("**☕ 원두 데이터**")

        if st.button("📤 원두 내보내기", use_container_width=True):
            try:
                excel_data = excel_service.export_beans_to_excel()

                st.download_button(
                    label="📥 Excel 다운로드",
                    data=excel_data,
                    file_name=f"원두_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ 원두 데이터 내보내기 준비 완료!")

            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    with col2:
        # 블렌드 내보내기
        st.markdown("**🎨 블렌드 데이터**")

        if st.button("📤 블렌드 내보내기", use_container_width=True):
            try:
                excel_data = excel_service.export_blends_to_excel()

                st.download_button(
                    label="📥 Excel 다운로드",
                    data=excel_data,
                    file_name=f"블렌드_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ 블렌드 데이터 내보내기 준비 완료!")

            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # 재고 내보내기
        st.markdown("**📦 재고 데이터**")

        if st.button("📤 재고 내보내기", use_container_width=True):
            try:
                excel_data = excel_service.export_inventory_to_excel()

                st.download_button(
                    label="📥 Excel 다운로드",
                    data=excel_data,
                    file_name=f"재고_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ 재고 데이터 내보내기 준비 완료!")

            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    with col2:
        # 거래 기록 내보내기
        st.markdown("**📝 거래 기록 (최근 30일)**")

        if st.button("📤 거래기록 내보내기", use_container_width=True):
            try:
                excel_data = excel_service.export_transactions_to_excel(days=30)

                st.download_button(
                    label="📥 Excel 다운로드",
                    data=excel_data,
                    file_name=f"거래기록_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ 거래 기록 내보내기 준비 완료!")

            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

    st.divider()

    # 전체 내보내기
    st.markdown("#### 📋 전체 데이터 내보내기")

    if st.button("📤 모든 데이터 내보내기", use_container_width=True, type="secondary"):
        try:
            excel_data = excel_service.export_all_to_excel()

            st.download_button(
                label="📥 Excel 다운로드 (전체)",
                data=excel_data,
                file_name=f"전체데이터_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ 전체 데이터 내보내기 준비 완료!")

        except Exception as e:
            st.error(f"❌ 오류: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 템플릿
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### 📋 임포트 템플릿")

    st.info("""
    임포트할 데이터의 형식을 맞추기 위해 템플릿을 다운로드할 수 있습니다.
    이 템플릿을 참고하여 데이터를 입력하고 임포트하세요.
    """)

    st.divider()

    # 템플릿 다운로드
    if st.button("📋 임포트 템플릿 다운로드", use_container_width=True, type="secondary"):
        try:
            template_data = excel_service.create_import_template()

            st.download_button(
                label="📥 템플릿 Excel 다운로드",
                data=template_data,
                file_name=f"임포트_템플릿_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ 템플릿 다운로드 준비 완료!")

        except Exception as e:
            st.error(f"❌ 오류: {str(e)}")

    st.divider()

    # 템플릿 설명
    st.markdown("#### 📖 템플릿 설명")

    st.markdown("""
    **원두 템플릿 (원두_템플릿)**

    | 컬럼명 | 설명 | 예시 |
    |--------|------|------|
    | No | 원두 번호 | 1 |
    | 원두명 | 원두 이름 (필수) | 에티오피아 |
    | 국가 | 국가 코드 | Eth, K, Co |
    | 로스팅 | 로스팅 레벨 (필수) | W, N, Pb |
    | 가격/kg | 가격 (필수) | 25000 |
    | 설명 | 원두 설명 | 가벼운 로스팅 |

    **블렌드 템플릿 (블렌드_템플릿)**

    | 컬럼명 | 설명 | 예시 |
    |--------|------|------|
    | 블렌드명 | 블렌드 이름 (필수) | 풀문 블렌드 |
    | 타입 | 블렌드 타입 (필수) | 풀문, 뉴문 |
    | 포션 | 포션 개수 | 4 |
    | 설명 | 블렌드 설명 | 부드러운 맛 |

    **주의사항**

    - 필수 컬럼을 반드시 입력해야 합니다.
    - 첫 번째 행은 컬럼명이므로 삭제하면 안 됩니다.
    - 숫자 형식이 올바른지 확인하세요.
    """)

    st.divider()

    # 파일 형식 확인
    st.markdown("#### ✅ 지원되는 파일 형식")

    st.write("""
    - **Excel 형식**: .xlsx, .xls
    - **권장**: .xlsx (Microsoft Excel 2007+)
    - **인코딩**: UTF-8 (한글 지원)
    """)

    st.divider()

    # FAQ
    st.markdown("#### ❓ 자주 묻는 질문")

    with st.expander("Q: 같은 이름의 원두가 있으면 어떻게 되나요?"):
        st.write("A: 기존 원두의 정보가 업데이트됩니다. 새로운 원두로 추가되지 않습니다.")

    with st.expander("Q: 임포트 중 오류가 발생하면?"):
        st.write("A: 오류 메시지를 확인하고 템플릿 형식에 맞게 수정 후 다시 시도하세요.")

    with st.expander("Q: 임포트한 데이터를 되돌릴 수 있나요?"):
        st.write("A: 설정 페이지에서 데이터베이스 백업/복원 기능을 사용하세요.")
