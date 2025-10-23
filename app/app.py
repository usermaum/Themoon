"""
더문 드립바 로스팅 원가 계산기
The Moon Drip BAR - Roasting Cost Calculator

Streamlit Web Application for calculating roasting costs and profit margins
for specialty coffee roasting business.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="더문 로스팅 원가 계산기",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
    }
    h2 {
        color: #34495e;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Database Path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roasting_data.db')

def init_database():
    """Initialize SQLite database with required tables"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create roasting_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roasting_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            bean_name TEXT NOT NULL,
            bean_code TEXT,
            green_weight_kg REAL NOT NULL,
            roasted_weight_kg REAL NOT NULL,
            roasting_loss_rate REAL DEFAULT 16.7,
            bean_cost_per_kg REAL NOT NULL,
            roasting_cost_per_kg REAL DEFAULT 2000,
            labor_cost REAL DEFAULT 15000,
            electricity_cost REAL DEFAULT 5000,
            misc_cost REAL DEFAULT 3000,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create bean_prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bean_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bean_name TEXT UNIQUE NOT NULL,
            price_per_kg REAL NOT NULL,
            updated_date TEXT DEFAULT CURRENT_DATE
        )
    ''')

    # Create cost_settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cost_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter_name TEXT UNIQUE NOT NULL,
            value REAL NOT NULL,
            description TEXT
        )
    ''')

    # Insert default cost settings
    default_settings = [
        ('roasting_loss_rate', 16.7, '로스팅 손실률 (%)'),
        ('roasting_cost_per_kg', 2000, '킬로그램당 로스팅 비용 (₩)'),
        ('labor_cost_per_hour', 15000, '시간당 인건비 (₩)'),
        ('roasting_time_hours', 2, '로스팅 시간 (시간)'),
        ('electricity_cost', 5000, '전기료 (₩)'),
        ('misc_cost', 3000, '기타 비용 (₩)'),
    ]

    for param_name, value, description in default_settings:
        cursor.execute('''
            INSERT OR IGNORE INTO cost_settings (parameter_name, value, description)
            VALUES (?, ?, ?)
        ''', (param_name, value, description))

    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize session state
if 'initialized' not in st.session_state:
    init_database()
    st.session_state.initialized = True

# Main UI
st.title("☕ 더문 로스팅 원가 계산기")
st.markdown("### The Moon Drip BAR - Roasting Cost Calculator")

# Sidebar
with st.sidebar:
    st.header("메뉴")
    page = st.radio(
        "페이지 선택",
        ["홈", "로스팅 기록", "원가 설정", "분석", "통계"]
    )

# Home Page
if page == "홈":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("총 로스팅 건수", "0")
    with col2:
        st.metric("평균 원가", "₩ 0")
    with col3:
        st.metric("총 로스팅량", "0 kg")

    st.markdown("""
    ---
    ## 소개

    **더문 드립바 로스팅 원가 계산기**는 전문 커피 로스팅 사업의 원가 분석과
    수익성 계산을 위한 도구입니다.

    ### 주요 기능
    - 💾 로스팅 기록 저장 및 관리
    - 💰 실시간 원가 계산
    - 📊 수익성 분석 및 시각화
    - 🔧 비용 설정 커스터마이징
    """)

# Roasting Logs Page
elif page == "로스팅 기록":
    st.header("로스팅 기록")

    with st.form("roasting_form"):
        col1, col2 = st.columns(2)

        with col1:
            record_date = st.date_input("로스팅 날짜")
            bean_name = st.text_input("원두 이름")
            green_weight = st.number_input("생두 무게 (kg)", min_value=0.1, step=0.1)

        with col2:
            roasted_weight = st.number_input("로스팅 후 무게 (kg)", min_value=0.1, step=0.1)
            bean_cost = st.number_input("원두 비용 (₩/kg)", min_value=0, step=100)
            notes = st.text_area("메모")

        if st.form_submit_button("저장"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO roasting_logs
                    (date, bean_name, green_weight_kg, roasted_weight_kg, bean_cost_per_kg, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (record_date.isoformat(), bean_name, green_weight, roasted_weight, bean_cost, notes))

                conn.commit()
                conn.close()

                st.success("✅ 기록이 저장되었습니다!")
            except Exception as e:
                st.error(f"❌ 오류: {str(e)}")

# Cost Settings Page
elif page == "원가 설정":
    st.header("원가 설정")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cost_settings")
        settings = cursor.fetchall()
        conn.close()

        for setting in settings:
            st.number_input(
                f"{setting['description']}",
                value=float(setting['value']),
                key=setting['parameter_name']
            )
    except Exception as e:
        st.error(f"설정 로드 오류: {str(e)}")

# Analysis Page
elif page == "분석":
    st.header("원가 분석")
    st.info("아직 데이터가 없습니다. 로스팅 기록을 추가해주세요.")

# Statistics Page
elif page == "통계":
    st.header("통계")
    st.info("아직 데이터가 없습니다. 로스팅 기록을 추가해주세요.")

st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 더문 드립바 | Version 0.1.0")
