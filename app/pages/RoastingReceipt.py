"""
로스팅 일괄 입력 페이지

그리드 형태로 여러 건의 로스팅 기록을 한 번에 입력하는 페이지
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

from app.services.roasting_service import RoastingService
from app.utils.database import get_db
from app.components.sidebar import render_sidebar

# ═══════════════════════════════════════════════════════════════════════════════
# Session State 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if 'db' not in st.session_state:
    st.session_state.db = get_db()

if 'roasting_service' not in st.session_state:
    st.session_state.roasting_service = RoastingService

# 템플릿 DataFrame을 session state에 저장
if 'receipt_template' not in st.session_state:
    st.session_state.receipt_template = None

db = st.session_state.db
roasting_service = st.session_state.roasting_service

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바 렌더링
# ═══════════════════════════════════════════════════════════════════════════════

render_sidebar()

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 헤더
# ═══════════════════════════════════════════════════════════════════════════════

# 현재 페이지 설정 (사이드바 활성 표시)
st.session_state["current_page"] = "RoastingReceipt"

st.title("📊 로스팅 일괄 입력")
st.markdown("여러 건의 로스팅 기록을 엑셀 스타일로 한 번에 입력합니다.")
st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 헬퍼 함수
# ═══════════════════════════════════════════════════════════════════════════════

def create_template(num_rows):
    """빈 템플릿 DataFrame 생성"""
    return pd.DataFrame({
        "날짜": [date.today()] * num_rows,
        "생두(kg)": [0.0] * num_rows,
        "로스팅후(kg)": [0.0] * num_rows,
        "예상손실률(%)": [17.0] * num_rows,
        "메모": [""] * num_rows
    })


def calculate_results(df):
    """실시간 계산 결과 생성"""
    results = []

    for idx, row in df.iterrows():
        # 빈 행 건너뛰기
        if pd.isna(row["날짜"]) or row["생두(kg)"] == 0:
            continue

        raw_weight = row["생두(kg)"]
        roasted_weight = row["로스팅후(kg)"]
        expected_loss = row["예상손실률(%)"]

        if raw_weight > 0:
            actual_loss = ((raw_weight - roasted_weight) / raw_weight) * 100
            variance = actual_loss - expected_loss

            # 상태 판정
            if abs(variance) <= 3.0:
                status = "🟢 정상"
            elif abs(variance) <= 5.0:
                status = "🟡 주의"
            else:
                status = "🔴 위험"

            results.append({
                "행번호": idx + 1,
                "날짜": row["날짜"].strftime("%Y-%m-%d") if not pd.isna(row["날짜"]) else "",
                "생두(kg)": f"{raw_weight:.2f}",
                "로스팅후(kg)": f"{roasted_weight:.2f}",
                "실제손실률(%)": f"{actual_loss:.2f}%",
                "차이(%)": f"{variance:+.2f}%",
                "상태": status
            })

    if not results:
        return pd.DataFrame(columns=["행번호", "날짜", "생두(kg)", "로스팅후(kg)", "실제손실률(%)", "차이(%)", "상태"])

    return pd.DataFrame(results)


def validate_all_rows(df):
    """All or Nothing 검증"""
    errors = []
    valid_rows = []

    for idx, row in df.iterrows():
        # 빈 행 건너뛰기 (모든 필수 필드가 비어있는 경우)
        if (pd.isna(row["날짜"]) or row["날짜"] == "") and row["생두(kg)"] == 0 and row["로스팅후(kg)"] == 0:
            continue

        valid_rows.append(idx)

        # 검증
        if pd.isna(row["날짜"]) or row["날짜"] == "":
            errors.append(f"행 {idx+1}: 날짜를 입력해주세요")

        if row["생두(kg)"] <= 0:
            errors.append(f"행 {idx+1}: 생두 무게는 0보다 커야 합니다")

        if row["로스팅후(kg)"] <= 0:
            errors.append(f"행 {idx+1}: 로스팅 후 무게는 0보다 커야 합니다")

        if row["로스팅후(kg)"] >= row["생두(kg)"]:
            errors.append(f"행 {idx+1}: 로스팅 후 무게는 생두 무게보다 작아야 합니다")

        if not pd.isna(row["날짜"]) and row["날짜"] > date.today():
            errors.append(f"행 {idx+1}: 미래 날짜는 선택할 수 없습니다")

    return errors, valid_rows


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 템플릿 설정
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("### 🔢 템플릿 설정")

col1, col2 = st.columns([3, 1])

with col1:
    num_rows = st.number_input(
        "기본 행 개수",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
        help="한 번에 입력할 로스팅 기록의 개수를 설정합니다."
    )

with col2:
    st.write("")
    st.write("")
    if st.button("📋 템플릿 생성", use_container_width=True, type="primary"):
        st.session_state.receipt_template = create_template(num_rows)
        st.success(f"✅ {num_rows}개 행 템플릿이 생성되었습니다!")
        st.rerun()

# 템플릿이 없으면 생성
if st.session_state.receipt_template is None:
    st.session_state.receipt_template = create_template(num_rows)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 2. 데이터 입력 테이블 (st.data_editor)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("### 📝 데이터 입력")

edited_df = st.data_editor(
    st.session_state.receipt_template,
    column_config={
        "날짜": st.column_config.DateColumn(
            "로스팅 날짜",
            help="로스팅을 수행한 날짜 (미래 날짜 불가)",
            default=date.today(),
            required=True
        ),
        "생두(kg)": st.column_config.NumberColumn(
            "생두 무게 (kg)",
            help="투입한 생두의 무게 (0.1 ~ 100kg)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.2f",
            required=True
        ),
        "로스팅후(kg)": st.column_config.NumberColumn(
            "로스팅 후 무게 (kg)",
            help="로스팅 후 무게 (생두보다 작아야 함)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            format="%.2f",
            required=True
        ),
        "예상손실률(%)": st.column_config.NumberColumn(
            "예상 손실률 (%)",
            help="예상되는 손실률 (기본값: 17.0%)",
            min_value=0.0,
            max_value=50.0,
            step=0.1,
            default=17.0,
            format="%.1f"
        ),
        "메모": st.column_config.TextColumn(
            "메모 (선택)",
            help="로스팅 관련 메모 (최대 500자)",
            max_chars=500
        )
    },
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    key="roasting_editor"
)

# 편집된 DataFrame을 session state에 저장
st.session_state.receipt_template = edited_df

st.caption("💡 팁: 행을 추가하려면 표 아래의 '➕' 버튼을 클릭하세요. 행을 삭제하려면 체크박스를 선택 후 삭제하세요.")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. 실시간 계산 결과 (별도 테이블)
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("### 💡 실시간 계산 결과")

result_df = calculate_results(edited_df)

if len(result_df) > 0:
    st.dataframe(
        result_df,
        hide_index=True,
        use_container_width=True
    )
    st.caption("🟢 정상 (±3% 이내) | 🟡 주의 (±3~5%) | 🔴 위험 (±5% 초과)")
else:
    st.info("데이터를 입력하면 실시간으로 손실률이 계산됩니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. 검증 및 저장
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("### ✅ 저장")

# 검증 실행
errors, valid_rows = validate_all_rows(edited_df)

# 검증 결과 표시
if len(valid_rows) > 0:
    if len(errors) == 0:
        st.success(f"✅ 검증 통과: 총 {len(valid_rows)}개 행이 저장 가능합니다.")
    else:
        st.error(f"❌ 검증 실패: {len(errors)}개의 오류가 있습니다. 모든 오류를 수정해주세요.")
        st.markdown("**오류 목록:**")
        for error in errors:
            st.write(f"- {error}")
else:
    st.info("저장할 데이터가 없습니다. 최소 1개 행을 입력해주세요.")

st.divider()

# 저장 버튼
col1, col2 = st.columns(2)

with col1:
    save_button = st.button(
        "💾 일괄 저장",
        type="primary",
        use_container_width=True,
        disabled=(len(errors) > 0 or len(valid_rows) == 0)
    )

with col2:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.receipt_template = None
        st.rerun()

# 저장 처리 (All or Nothing)
if save_button:
    if len(errors) == 0 and len(valid_rows) > 0:
        try:
            success_count = 0
            failed_rows = []

            for idx in valid_rows:
                row = edited_df.iloc[idx]

                try:
                    roasting_service.create_roasting_log(
                        db=db,
                        raw_weight_kg=float(row["생두(kg)"]),
                        roasted_weight_kg=float(row["로스팅후(kg)"]),
                        roasting_date=row["날짜"],
                        notes=row["메모"] if row["메모"] else None,
                        expected_loss_rate=float(row["예상손실률(%)"])
                    )
                    success_count += 1
                except Exception as e:
                    failed_rows.append((idx + 1, str(e)))

            # 결과 표시
            if len(failed_rows) == 0:
                st.success(f"🎉 성공! {success_count}개의 로스팅 기록이 저장되었습니다!")

                # 템플릿 초기화
                st.session_state.receipt_template = None
                st.balloons()
                st.rerun()
            else:
                st.error(f"⚠️ 일부 실패: {success_count}개 성공, {len(failed_rows)}개 실패")
                st.markdown("**실패한 행:**")
                for row_num, error_msg in failed_rows:
                    st.write(f"- 행 {row_num}: {error_msg}")

        except Exception as e:
            st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")
    else:
        st.error("❌ 오류가 있거나 저장할 데이터가 없습니다.")
