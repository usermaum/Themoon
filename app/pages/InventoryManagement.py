"""
재고 관리 페이지
원두 재고 추적, 입고/사용 기록, 경고 알림
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SessionLocal, Inventory, Transaction
from services.bean_service import BeanService
from i18n import Translator, LanguageManager

# 다중 언어 지원 초기화
if "translator" not in st.session_state:
    st.session_state.translator = Translator(default_language="ko")

if "language_manager" not in st.session_state:
    st.session_state.language_manager = LanguageManager(st.session_state.translator)

# 페이지 설정 (다중 언어 지원)
translator = st.session_state.translator
page_title = translator.get("menu.inventory_management.page_title", "재고관리")
st.set_page_config(page_title=page_title, page_icon="📦", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()

if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

db = st.session_state.db
bean_service = st.session_state.bean_service

# ═══════════════════════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<h1 style='color: #1F4E78;'>📦 재고 관리</h1>", unsafe_allow_html=True)
st.markdown("원두 재고 현황, 거래 기록, 입고/사용 관리")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📊 현황", "📝 거래 기록", "➕ 입출고", "⚠️ 경고"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: 재고 현황
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📊 현재 재고 현황")

    beans = bean_service.get_active_beans()

    if beans:
        # 재고 데이터 로드
        inventory_data = []
        total_quantity = 0
        low_stock_count = 0

        for bean in beans:
            inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

            if inventory:
                quantity = inventory.quantity_kg
                min_qty = inventory.min_quantity_kg
                max_qty = inventory.max_quantity_kg
                total_quantity += quantity

                # 저재고 판정
                is_low = quantity < min_qty if min_qty > 0 else False
                if is_low:
                    low_stock_count += 1

                # 상태 판정
                if min_qty > 0 and quantity < min_qty:
                    status = "🔴 저재고"
                elif max_qty > 0 and quantity > max_qty:
                    status = "🟡 과재고"
                else:
                    status = "🟢 정상"

                inventory_data.append({
                    "원두명": bean.name,
                    "국가": bean.country_code or "-",
                    "현재": f"{quantity:.2f}kg",
                    "최소": f"{min_qty:.2f}kg",
                    "최대": f"{max_qty:.2f}kg",
                    "상태": status,
                    "가격/kg": f"₩{bean.price_per_kg:,.0f}"
                })

        # 통계
        st.markdown("#### 📈 재고 통계")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("☕ 원두 종류", len(beans))

        with col2:
            st.metric("📦 총 재고", f"{total_quantity:.2f}kg")

        with col3:
            avg_per_bean = total_quantity / len(beans) if beans else 0
            st.metric("평균 보유", f"{avg_per_bean:.2f}kg")

        with col4:
            st.metric("🔴 저재고", low_stock_count)

        st.divider()

        # 재고 테이블
        st.markdown("#### 📋 재고 목록")

        df_inventory = pd.DataFrame(inventory_data)
        st.dataframe(df_inventory, use_container_width=True, hide_index=True)

        st.divider()

        # 재고 시각화
        st.markdown("#### 📊 재고 분포")

        # 현재 재고량 그래프
        inventory_quantity = []
        bean_names = []

        for bean in beans:
            inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()
            if inventory:
                inventory_quantity.append(inventory.quantity_kg)
                bean_names.append(bean.name)

        if inventory_quantity:
            fig = go.Figure(data=[go.Bar(
                x=bean_names,
                y=inventory_quantity,
                marker_color="#4472C4",
                text=[f"{q:.2f}kg" for q in inventory_quantity],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>재고: %{y:.2f}kg<extra></extra>"
            )])

            fig.update_layout(
                title="원두별 현재 재고량",
                xaxis_title="원두명",
                yaxis_title="재고량 (kg)",
                height=400,
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("관리할 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: 거래 기록
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("### 📝 거래 기록")

    # 거래 데이터 로드
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()

    if transactions:
        transaction_data = []

        for transaction in transactions:
            transaction_data.append({
                "ID": transaction.id,
                "거래 유형": transaction.transaction_type,
                "수량": f"{transaction.quantity_kg:.2f}kg",
                "단가": f"₩{transaction.price_per_unit:,.0f}",
                "합계": f"₩{transaction.total_amount:,.0f}",
                "날짜": transaction.created_at.strftime("%Y-%m-%d %H:%M"),
                "설명": transaction.description or "-"
            })

        df_transactions = pd.DataFrame(transaction_data)
        st.dataframe(df_transactions, use_container_width=True, hide_index=True)

        # 통계
        st.markdown("#### 📊 거래 통계")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_transactions = len(transactions)
            st.metric("총 거래 건수", total_transactions)

        with col2:
            inflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "입고")
            st.metric("총 입고량", f"{inflow:.2f}kg")

        with col3:
            outflow = sum(t.quantity_kg for t in transactions if t.transaction_type == "사용")
            st.metric("총 출고량", f"{outflow:.2f}kg")

    else:
        st.info("거래 기록이 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: 입출고 기록
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("### ➕ 입출고 기록")

    beans = bean_service.get_active_beans()

    if beans:
        st.markdown("#### 📥 입고 기록")

        with st.form("inflow_form"):
            col1, col2 = st.columns(2)

            with col1:
                bean_name = st.selectbox(
                    "원두 선택 (입고)",
                    options=[b.name for b in beans]
                )
                quantity = st.number_input("입고량 (kg)", min_value=0.1, value=1.0, step=0.1)

            with col2:
                price_per_unit = st.number_input("단가 (원/kg)", min_value=0, value=0, step=1000)
                description = st.text_input("설명", "")

            if st.form_submit_button("✅ 입고 기록", use_container_width=True):
                bean = next((b for b in beans if b.name == bean_name), None)

                if bean:
                    try:
                        # Inventory 업데이트
                        inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()
                        if inventory:
                            inventory.quantity_kg += quantity
                        else:
                            inventory = Inventory(
                                bean_id=bean.id,
                                quantity_kg=quantity,
                                min_quantity_kg=5.0,
                                max_quantity_kg=50.0
                            )
                            db.add(inventory)

                        # Transaction 기록
                        transaction = Transaction(
                            bean_id=bean.id,
                            transaction_type="입고",
                            quantity_kg=quantity,
                            price_per_unit=price_per_unit,
                            total_amount=quantity * price_per_unit,
                            description=description or f"{bean.name} 입고"
                        )
                        db.add(transaction)
                        db.commit()

                        st.success(f"✅ {bean.name} {quantity:.2f}kg 입고 기록 완료")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")

        st.divider()

        st.markdown("#### 📤 출고 기록 (사용)")

        with st.form("outflow_form"):
            col1, col2 = st.columns(2)

            with col1:
                bean_name_out = st.selectbox(
                    "원두 선택 (출고)",
                    options=[b.name for b in beans],
                    key="bean_outflow"
                )
                quantity_out = st.number_input("출고량 (kg)", min_value=0.1, value=1.0, step=0.1, key="qty_outflow")

            with col2:
                price_per_unit_out = st.number_input("단가 (원/kg)", min_value=0, value=0, step=1000, key="price_outflow")
                description_out = st.text_input("설명", "", key="desc_outflow")

            if st.form_submit_button("✅ 출고 기록", use_container_width=True):
                bean = next((b for b in beans if b.name == bean_name_out), None)

                if bean:
                    try:
                        # Inventory 확인 및 업데이트
                        inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

                        if inventory and inventory.quantity_kg >= quantity_out:
                            inventory.quantity_kg -= quantity_out

                            # Transaction 기록
                            transaction = Transaction(
                                bean_id=bean.id,
                                transaction_type="사용",
                                quantity_kg=quantity_out,
                                price_per_unit=price_per_unit_out,
                                total_amount=quantity_out * price_per_unit_out,
                                description=description_out or f"{bean.name} 사용"
                            )
                            db.add(transaction)
                            db.commit()

                            st.success(f"✅ {bean.name} {quantity_out:.2f}kg 출고 기록 완료")
                            st.rerun()
                        else:
                            available = inventory.quantity_kg if inventory else 0
                            st.error(f"❌ 재고 부족 (보유: {available:.2f}kg, 요청: {quantity_out:.2f}kg)")
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")

    else:
        st.info("관리할 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: 경고 및 알림
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("### ⚠️ 경고 및 알림")

    beans = bean_service.get_active_beans()

    if beans:
        # 저재고 확인
        low_stock_beans = []
        over_stock_beans = []
        normal_beans = []

        for bean in beans:
            inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

            if inventory:
                if inventory.min_quantity_kg > 0 and inventory.quantity_kg < inventory.min_quantity_kg:
                    low_stock_beans.append((bean, inventory))
                elif inventory.max_quantity_kg > 0 and inventory.quantity_kg > inventory.max_quantity_kg:
                    over_stock_beans.append((bean, inventory))
                else:
                    normal_beans.append((bean, inventory))

        # 저재고 경고
        if low_stock_beans:
            st.markdown("#### 🔴 저재고 경고")
            for bean, inventory in low_stock_beans:
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**{bean.name}**")
                    st.write(f"현재: {inventory.quantity_kg:.2f}kg / 최소: {inventory.min_quantity_kg:.2f}kg")

                with col2:
                    shortage = inventory.min_quantity_kg - inventory.quantity_kg
                    st.metric("부족량", f"{shortage:.2f}kg")

                with col3:
                    st.metric("재고율", f"{inventory.quantity_kg/inventory.min_quantity_kg*100:.0f}%")

            st.divider()

        # 과재고 경고
        if over_stock_beans:
            st.markdown("#### 🟡 과재고 경고")
            for bean, inventory in over_stock_beans:
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**{bean.name}**")
                    st.write(f"현재: {inventory.quantity_kg:.2f}kg / 최대: {inventory.max_quantity_kg:.2f}kg")

                with col2:
                    excess = inventory.quantity_kg - inventory.max_quantity_kg
                    st.metric("초과량", f"{excess:.2f}kg")

                with col3:
                    st.metric("재고율", f"{inventory.quantity_kg/inventory.max_quantity_kg*100:.0f}%")

            st.divider()

        # 정상 상태
        if normal_beans:
            st.markdown("#### 🟢 정상 재고")
            normal_data = []
            for bean, inventory in normal_beans:
                normal_data.append({
                    "원두명": bean.name,
                    "현재": f"{inventory.quantity_kg:.2f}kg",
                    "범위": f"{inventory.min_quantity_kg:.2f}~{inventory.max_quantity_kg:.2f}kg",
                    "재고율": f"{inventory.quantity_kg/inventory.min_quantity_kg*100:.0f}%" if inventory.min_quantity_kg > 0 else "N/A"
                })

            if normal_data:
                df_normal = pd.DataFrame(normal_data)
                st.dataframe(df_normal, use_container_width=True, hide_index=True)

        st.divider()

        # 재고 재설정
        st.markdown("#### ⚙️ 재고 범위 설정")

        bean_to_adjust = st.selectbox(
            "재고 범위를 조정할 원두 선택",
            options=[b.name for b in beans]
        )

        bean = next((b for b in beans if b.name == bean_to_adjust), None)

        if bean:
            inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

            if inventory:
                col1, col2 = st.columns(2)

                with col1:
                    new_min = st.number_input(
                        "최소 재고 (kg)",
                        value=float(inventory.min_quantity_kg),
                        min_value=0.0,
                        step=0.5,
                        key="min_qty"
                    )

                with col2:
                    new_max = st.number_input(
                        "최대 재고 (kg)",
                        value=float(inventory.max_quantity_kg),
                        min_value=0.0,
                        step=0.5,
                        key="max_qty"
                    )

                if st.button("💾 재고 범위 저장", use_container_width=True):
                    try:
                        inventory.min_quantity_kg = new_min
                        inventory.max_quantity_kg = new_max
                        db.commit()

                        st.success(f"✅ {bean.name}의 재고 범위가 업데이트되었습니다!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 오류: {str(e)}")

    else:
        st.info("관리할 원두가 없습니다.")

# ═══════════════════════════════════════════════════════════════════════════════
# 데이터 내보내기 (하단)
# ═══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("#### 📥 데이터 내보내기")

beans = bean_service.get_active_beans()

if beans:
    export_data = []

    for bean in beans:
        inventory = db.query(Inventory).filter(Inventory.bean_id == bean.id).first()

        if inventory:
            export_data.append({
                "원두명": bean.name,
                "현재 재고": f"{inventory.quantity_kg:.2f}",
                "최소 재고": f"{inventory.min_quantity_kg:.2f}",
                "최대 재고": f"{inventory.max_quantity_kg:.2f}",
                "가격/kg": f"{bean.price_per_kg}"
            })

    if export_data:
        df_export = pd.DataFrame(export_data)
        csv = df_export.to_csv(index=False, encoding="utf-8-sig")

        st.download_button(
            label="📥 CSV로 다운로드",
            data=csv,
            file_name="재고_목록.csv",
            mime="text/csv"
        )
