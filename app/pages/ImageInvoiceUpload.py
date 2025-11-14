"""
거래 명세서 이미지 자동 입고 페이지
이미지 업로드 → OCR 분석 → 결과 확인 → 입고 확정
"""

import streamlit as st
import sys
import os
from datetime import date, datetime
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal
from services.ocr_service import OCRService
from services.invoice_service import InvoiceService
from services.learning_service import LearningService
from services.bean_service import BeanService
from components.sidebar import render_sidebar
from i18n import Translator, LanguageManager

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정
st.set_page_config(
    page_title="거래 명세서 이미지 입고",
    page_icon="📄",
    layout="wide"
)

# 현재 페이지 저장
st.session_state["current_page"] = "ImageInvoiceUpload"

# 사이드바 렌더링
render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

# learning_service 먼저 생성 (다른 서비스에서 사용)
if "learning_service" not in st.session_state:
    st.session_state.learning_service = LearningService(st.session_state.db)

if "ocr_service" not in st.session_state:
    st.session_state.ocr_service = OCRService(
        st.session_state.db,
        learning_service=st.session_state.learning_service
    )

if "invoice_service" not in st.session_state:
    st.session_state.invoice_service = InvoiceService(
        st.session_state.db,
        learning_service=st.session_state.learning_service
    )

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

# 분석 결과 저장용
if "invoice_result" not in st.session_state:
    st.session_state.invoice_result = None

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.title("📄 거래 명세서 이미지 자동 입고")
st.markdown("""
스마트폰으로 촬영한 거래 명세서를 업로드하면 AI가 자동으로 인식하여 입고 처리합니다.

**지원 형식:** JPG, PNG, PDF (최대 10MB)
""")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📤 이미지 업로드",
    "✅ 인식 결과 확인",
    "📋 처리 내역",
    "📚 학습 통계"
])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 이미지 업로드
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.header("1️⃣ 거래 명세서 이미지 업로드")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("이미지 선택")

        uploaded_file = st.file_uploader(
            "거래 명세서 이미지를 선택하세요",
            type=['jpg', 'jpeg', 'png', 'pdf'],
            help="JPG, PNG, PDF 형식 지원 (최대 10MB)"
        )

        if uploaded_file:
            st.success(f"✅ 파일 선택됨: {uploaded_file.name}")
            st.caption(f"크기: {uploaded_file.size / 1024:.1f} KB")

            # 분석 버튼
            if st.button("🤖 AI 분석 시작", type="primary", use_container_width=True):
                with st.spinner("AI가 명세서를 분석하고 있습니다... (약 5~10초 소요)"):
                    try:
                        # 이미지 처리 파이프라인 실행
                        result = st.session_state.invoice_service.process_invoice_image(
                            uploaded_file,
                            st.session_state.ocr_service
                        )

                        # 결과 저장
                        st.session_state.invoice_result = result

                        # OCR 원본 값 저장 (학습용)
                        import copy
                        st.session_state.invoice_result_original = copy.deepcopy(result)

                        st.success("✅ 분석 완료! '인식 결과 확인' 탭으로 이동하세요.")
                        st.balloons()

                    except Exception as e:
                        st.error(f"❌ 분석 실패: {str(e)}")
                        st.info("이미지가 흐릿하거나 형식이 맞지 않을 수 있습니다. 다른 이미지를 시도해주세요.")
        else:
            st.info("📁 거래 명세서 이미지를 업로드해주세요.")

    with col2:
        st.subheader("미리보기")

        if uploaded_file:
            try:
                # 이미지 표시
                if uploaded_file.type in ['image/jpeg', 'image/png', 'image/jpg']:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="업로드된 이미지", use_column_width=True)
                elif uploaded_file.type == 'application/pdf':
                    st.info("📄 PDF 파일이 업로드되었습니다. 분석 시 첫 페이지만 처리됩니다.")
            except Exception as e:
                st.warning("이미지 미리보기 실패")
        else:
            st.image("https://via.placeholder.com/400x300?text=Image+Preview",
                    caption="이미지 미리보기", use_column_width=True)

    # 사용 가이드
    st.divider()
    st.subheader("📖 사용 가이드")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **1. 촬영 팁**
        - 📱 명세서 전체가 보이도록 촬영
        - 💡 조명이 밝은 곳에서 촬영
        - 📐 명세서를 평평하게 펴서 촬영
        """)

    with col2:
        st.markdown("""
        **2. 지원 형식**
        - ✅ GSC 거래명세서 (높은 정확도)
        - ✅ HACIELO 명세서
        - ✅ 기타 표준 명세서
        """)

    with col3:
        st.markdown("""
        **3. 처리 과정**
        - 🤖 AI가 텍스트 자동 추출
        - 🔍 원두명 자동 매칭
        - ✅ 사용자 확인 후 입고
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 인식 결과 확인
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.header("2️⃣ 인식 결과 확인 및 수정")

    result = st.session_state.invoice_result

    if not result:
        st.info("먼저 '이미지 업로드' 탭에서 명세서를 분석해주세요.")
    else:
        # 신뢰도 표시
        confidence = result['confidence']
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("신뢰도", f"{confidence:.1f}%")

        with col2:
            invoice_type = result['invoice_type']
            st.metric("명세서 타입", invoice_type)

        with col3:
            items_count = len(result['items'])
            st.metric("원두 항목 수", f"{items_count}개")

        with col4:
            total_amount = result['invoice_data'].get('total_amount', 0)
            st.metric("총액", f"₩{total_amount:,.0f}")

        # 경고 메시지
        if result['warnings']:
            st.warning("⚠️ **경고사항**")
            for warning in result['warnings']:
                st.write(f"- {warning}")

        st.divider()

        # 명세서 메타데이터
        st.subheader("📋 명세서 정보")

        col1, col2, col3 = st.columns(3)

        with col1:
            supplier = st.text_input(
                "공급업체",
                value=result['invoice_data'].get('supplier', ''),
                key="edit_supplier"
            )

        with col2:
            invoice_date = st.date_input(
                "거래일자",
                value=result['invoice_data'].get('invoice_date', date.today()),
                key="edit_invoice_date"
            )

        with col3:
            total_amount_edit = st.number_input(
                "총액 (원)",
                value=float(result['invoice_data'].get('total_amount', 0)),
                min_value=0.0,
                step=1000.0,
                key="edit_total_amount"
            )

        st.divider()

        # 원두 항목 표시
        st.subheader("☕ 원두 항목")

        if not result['items']:
            st.warning("인식된 원두 항목이 없습니다. 수동으로 추가해주세요.")
        else:
            # 모든 원두 목록 가져오기 (드롭다운용)
            all_beans = st.session_state.bean_service.get_all_beans()
            bean_options = {f"{bean.name} (NO.{bean.no})": bean for bean in all_beans}
            bean_names = list(bean_options.keys())

            # 각 항목마다 수정 폼
            for idx, item in enumerate(result['items']):
                with st.expander(f"**항목 {idx+1}: {item.get('bean_name', '알 수 없음')}**", expanded=(idx==0)):
                    col1, col2 = st.columns(2)

                    with col1:
                        # 원두 선택
                        bean_name_raw = item.get('bean_name', '')

                        # 매칭된 원두 찾기
                        matched_bean, match_score = result['matched_beans'].get(bean_name_raw, (None, 0.0))

                        if matched_bean:
                            default_bean_name = f"{matched_bean.name} (NO.{matched_bean.no})"
                            default_index = bean_names.index(default_bean_name) if default_bean_name in bean_names else 0
                            st.success(f"✅ 자동 매칭됨 (유사도: {match_score:.1%})")
                        else:
                            default_index = 0
                            st.warning("⚠️ 자동 매칭 실패 - 수동 선택 필요")

                        selected_bean_name = st.selectbox(
                            "원두 선택",
                            options=bean_names,
                            index=default_index,
                            key=f"bean_select_{idx}"
                        )

                        selected_bean = bean_options[selected_bean_name]

                        st.caption(f"OCR 인식값: {bean_name_raw}")

                    with col2:
                        # 중량 (kg)
                        weight = st.number_input(
                            "중량 (kg)",
                            value=float(item.get('weight', 0)),
                            min_value=0.0,
                            step=0.1,
                            key=f"weight_{idx}"
                        )

                    col3, col4, col5 = st.columns(3)

                    with col3:
                        # 단가 (원/kg)
                        unit_price = st.number_input(
                            "단가 (원/kg)",
                            value=float(item.get('unit_price', 0)),
                            min_value=0.0,
                            step=100.0,
                            key=f"unit_price_{idx}"
                        )

                    with col4:
                        # 공급가액 (자동 계산)
                        amount = weight * unit_price
                        st.metric("공급가액", f"₩{amount:,.0f}")

                    with col5:
                        # 규격
                        spec = st.text_input(
                            "규격",
                            value=item.get('spec', ''),
                            key=f"spec_{idx}"
                        )

                    # 항목 정보 업데이트 (세션에 저장)
                    result['items'][idx]['bean_id'] = selected_bean.id
                    result['items'][idx]['bean_name'] = selected_bean.name
                    result['items'][idx]['weight'] = weight
                    result['items'][idx]['unit_price'] = unit_price
                    result['items'][idx]['amount'] = amount
                    result['items'][idx]['spec'] = spec

        st.divider()

        # 입고 확정 버튼
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            if st.button("❌ 취소", use_container_width=True):
                st.session_state.invoice_result = None
                st.rerun()

        with col3:
            if st.button("✅ 입고 확정", type="primary", use_container_width=True):
                try:
                    with st.spinner("입고 처리 중..."):
                        # Invoice 데이터 업데이트
                        result['invoice_data']['supplier'] = supplier
                        result['invoice_data']['invoice_date'] = invoice_date
                        result['invoice_data']['total_amount'] = total_amount_edit

                        # Invoice 저장
                        invoice = st.session_state.invoice_service.save_invoice(
                            invoice_data=result['invoice_data'],
                            items=result['items'],
                            image=result['image'],
                            ocr_text=result['ocr_text'],
                            confidence=confidence
                        )

                        # 사용자 수정 내역 저장 (학습용)
                        if hasattr(st.session_state, 'invoice_result_original') and \
                           hasattr(st.session_state, 'learning_service') and \
                           st.session_state.learning_service is not None:
                            try:
                                corrections = []
                                original_result = st.session_state.invoice_result_original

                                # 각 항목별로 원본과 비교
                                for idx, (original_item, current_item) in enumerate(zip(
                                    original_result.get('items', []),
                                    result['items']
                                )):
                                    # invoice_item_id 가져오기 (저장 후 생성된 ID)
                                    if idx < len(invoice.items):
                                        invoice_item_id = invoice.items[idx].id

                                        # 원두명 비교
                                        original_bean_name = original_item.get('bean_name', '')
                                        current_bean_name = current_item.get('bean_name', '')
                                        if original_bean_name and str(original_bean_name) != str(current_bean_name):
                                            corrections.append({
                                                'invoice_item_id': invoice_item_id,
                                                'field_name': 'bean_name',
                                                'ocr_value': str(original_bean_name),
                                                'corrected_value': str(current_bean_name)
                                            })

                                        # 중량 비교
                                        original_weight = original_item.get('weight')
                                        current_weight = current_item.get('weight')
                                        if original_weight is not None and current_weight is not None and \
                                           float(original_weight) != float(current_weight):
                                            corrections.append({
                                                'invoice_item_id': invoice_item_id,
                                                'field_name': 'weight',
                                                'ocr_value': str(original_weight),
                                                'corrected_value': str(current_weight)
                                            })

                                        # 단가 비교
                                        original_unit_price = original_item.get('unit_price')
                                        current_unit_price = current_item.get('unit_price')
                                        if original_unit_price is not None and current_unit_price is not None and \
                                           float(original_unit_price) != float(current_unit_price):
                                            corrections.append({
                                                'invoice_item_id': invoice_item_id,
                                                'field_name': 'unit_price',
                                                'ocr_value': str(original_unit_price),
                                                'corrected_value': str(current_unit_price)
                                            })

                                # corrections 저장
                                if corrections:
                                    saved_count = st.session_state.invoice_service.save_user_corrections(corrections)
                                    # st.info(f"📚 {saved_count}개 수정 내역이 학습되었습니다.")

                            except Exception as e:
                                # 학습 저장 실패해도 입고는 진행
                                pass

                        # 입고 확정 (Inventory + Transaction 생성)
                        st.session_state.invoice_service.confirm_invoice(invoice.id)

                        st.success(f"✅ {len(result['items'])}개 원두 입고 완료!")
                        st.balloons()

                        # 결과 초기화
                        st.session_state.invoice_result = None
                        if hasattr(st.session_state, 'invoice_result_original'):
                            st.session_state.invoice_result_original = None

                        # 2초 후 처리 내역 탭으로 이동
                        import time
                        time.sleep(2)
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ 입고 실패: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 처리 내역
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.header("3️⃣ 처리 내역")

    # 필터
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        status_filter = st.selectbox(
            "상태 필터",
            options=["전체", "PENDING", "COMPLETED", "FAILED"],
            index=1  # 기본값: COMPLETED
        )

    with col2:
        limit = st.number_input(
            "조회 개수",
            value=20,
            min_value=5,
            max_value=100,
            step=5
        )

    with col3:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()

    st.divider()

    # 처리 내역 조회
    status = None if status_filter == "전체" else status_filter
    invoices = st.session_state.invoice_service.get_invoice_history(
        limit=limit,
        status=status
    )

    if not invoices:
        st.info("처리된 명세서가 없습니다.")
    else:
        st.subheader(f"📊 총 {len(invoices)}건")

        # 테이블 형식으로 표시
        for invoice in invoices:
            with st.expander(f"**#{invoice.id} - {invoice.supplier}** ({invoice.invoice_date})"):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("상태", invoice.status)

                with col2:
                    st.metric("신뢰도", f"{invoice.confidence_score:.1f}%")

                with col3:
                    st.metric("총액", f"₩{invoice.total_amount:,.0f}")

                with col4:
                    st.metric("원두 항목", f"{len(invoice.items)}개")

                # 이미지 표시
                if os.path.exists(invoice.image_path):
                    st.image(invoice.image_path, caption="명세서 이미지", width=400)

                # 항목 상세
                st.subheader("원두 항목")
                items_data = []
                for item in invoice.items:
                    items_data.append({
                        "원두명": item.bean_name_raw,
                        "중량(kg)": item.weight,
                        "단가(원/kg)": f"₩{item.unit_price:,.0f}",
                        "공급가액(원)": f"₩{item.amount:,.0f}",
                        "규격": item.spec or "-"
                    })

                st.table(items_data)

                # 삭제 버튼 (PENDING만)
                if invoice.status == "PENDING":
                    if st.button(f"🗑️ 삭제 (Invoice #{invoice.id})", key=f"delete_{invoice.id}"):
                        try:
                            st.session_state.invoice_service.delete_invoice(invoice.id)
                            st.success("✅ 삭제 완료")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ 삭제 실패: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 학습 통계
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.header("📚 학습 통계")
    st.markdown("""
    사용자가 OCR 결과를 수정한 내역을 학습하여 다음 분석의 정확도를 높입니다.
    """)

    if not hasattr(st.session_state, 'learning_service') or st.session_state.learning_service is None:
        st.warning("⚠️ 학습 서비스가 활성화되지 않았습니다.")
    else:
        try:
            # 학습 통계 조회
            stats = st.session_state.learning_service.get_correction_stats()

            if not stats:
                st.info("📝 아직 학습 데이터가 없습니다. OCR 결과를 수정하면 자동으로 학습됩니다.")
            else:
                # ═══════════════════════════════════════════════════════════════
                # 1. 전체 통계
                # ═══════════════════════════════════════════════════════════════
                st.subheader("📊 전체 통계")

                col1, col2, col3 = st.columns(3)

                with col1:
                    total_count = stats.get('total_count', 0)
                    st.metric(
                        "총 학습 데이터 수",
                        f"{total_count:,}건",
                        help="사용자가 수정한 총 횟수"
                    )

                with col2:
                    unique_fields = len(stats.get('by_field', {}))
                    st.metric(
                        "학습된 필드 수",
                        f"{unique_fields}개",
                        help="수정이 발생한 필드 종류"
                    )

                with col3:
                    unique_beans = len(stats.get('by_bean_name', {}))
                    st.metric(
                        "학습된 원두 수",
                        f"{unique_beans}개",
                        help="수정이 발생한 원두 종류"
                    )

                st.divider()

                # ═══════════════════════════════════════════════════════════════
                # 2. 필드별 수정 빈도
                # ═══════════════════════════════════════════════════════════════
                st.subheader("📝 필드별 수정 빈도")

                by_field = stats.get('by_field', {})
                if by_field:
                    # 데이터 준비
                    field_data = []
                    field_name_map = {
                        'bean_name': '원두명',
                        'weight': '중량',
                        'unit_price': '단가',
                        'quantity': '수량',
                        'amount': '금액',
                        'spec': '규격',
                        'origin': '원산지',
                        'supplier': '공급처',
                        'invoice_date': '거래일자',
                        'total_amount': '합계금액',
                        'total_weight': '총 중량'
                    }

                    for field_name, count in sorted(by_field.items(), key=lambda x: x[1], reverse=True):
                        field_data.append({
                            "필드": field_name_map.get(field_name, field_name),
                            "수정 횟수": f"{count}회",
                            "비율": f"{count / total_count * 100:.1f}%"
                        })

                    st.table(field_data)
                else:
                    st.info("필드별 통계가 없습니다.")

                st.divider()

                # ═══════════════════════════════════════════════════════════════
                # 3. 자주 수정되는 원두명 Top 5
                # ═══════════════════════════════════════════════════════════════
                st.subheader("🏆 자주 수정되는 원두명 Top 5")

                by_bean_name = stats.get('by_bean_name', {})
                if by_bean_name:
                    # 상위 5개 추출
                    top_beans = sorted(by_bean_name.items(), key=lambda x: x[1], reverse=True)[:5]

                    bean_data = []
                    for idx, (bean_name, count) in enumerate(top_beans, start=1):
                        bean_data.append({
                            "순위": f"{idx}위",
                            "원두명": bean_name,
                            "수정 횟수": f"{count}회"
                        })

                    st.table(bean_data)

                    st.info("💡 자주 수정되는 원두는 OCR 인식 정확도가 낮을 수 있습니다. 원두명을 더 명확하게 촬영하거나 수동 매칭을 고려하세요.")
                else:
                    st.info("원두명 통계가 없습니다.")

                st.divider()

                # ═══════════════════════════════════════════════════════════════
                # 4. 최근 학습 내역
                # ═══════════════════════════════════════════════════════════════
                st.subheader("📜 최근 학습 내역 (최근 10건)")

                recent_learnings = st.session_state.learning_service.get_learning_data(limit=10)

                if recent_learnings:
                    learning_data = []
                    field_name_map = {
                        'bean_name': '원두명',
                        'weight': '중량',
                        'unit_price': '단가',
                        'quantity': '수량',
                        'amount': '금액',
                        'spec': '규격',
                        'origin': '원산지',
                        'supplier': '공급처',
                        'invoice_date': '거래일자',
                        'total_amount': '합계금액',
                        'total_weight': '총 중량'
                    }

                    for learning in recent_learnings:
                        learning_data.append({
                            "날짜": learning.created_at.strftime("%Y-%m-%d %H:%M"),
                            "필드": field_name_map.get(learning.field_name, learning.field_name),
                            "OCR 값": learning.ocr_value,
                            "수정 값": learning.corrected_value,
                            "Invoice": f"#{learning.invoice_item_id}"
                        })

                    st.table(learning_data)
                else:
                    st.info("최근 학습 내역이 없습니다.")

                st.divider()

                # ═══════════════════════════════════════════════════════════════
                # 5. 학습 데이터 관리
                # ═══════════════════════════════════════════════════════════════
                st.subheader("⚙️ 학습 데이터 관리")

                col1, col2 = st.columns(2)

                with col1:
                    st.info("💡 학습 데이터는 자동으로 축적되며, OCR 정확도 향상에 활용됩니다.")

                with col2:
                    if st.button("🗑️ 모든 학습 데이터 초기화", type="secondary", key="clear_learning"):
                        st.warning("⚠️ 정말로 모든 학습 데이터를 삭제하시겠습니까?")
                        if st.button("✅ 예, 삭제합니다", key="confirm_clear"):
                            try:
                                st.session_state.learning_service.clear_learning_data()
                                st.success("✅ 학습 데이터가 초기화되었습니다.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 초기화 실패: {str(e)}")

        except Exception as e:
            st.error(f"❌ 학습 통계 조회 실패: {str(e)}")
