"""
테스트 데이터 생성 스크립트
Generate sample roasting data for testing
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roasting_data.db')

def create_test_data():
    """Create sample roasting data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Sample bean types
    beans = [
        ("에티오피아 예가체프", 28000),
        ("케냐 AA FAQ", 32000),
        ("콜롬비아 우일라", 26000),
        ("과테말라 안티구아", 27000),
        ("브라질 파젠다 카르모", 22000),
    ]

    # Insert bean prices
    for bean_name, price in beans:
        cursor.execute('''
            INSERT OR IGNORE INTO bean_prices (bean_name, price_per_kg)
            VALUES (?, ?)
        ''', (bean_name, price))

    # Generate sample roasting logs (last 30 days)
    base_date = datetime.now() - timedelta(days=30)

    sample_logs = [
        ("에티오피아 예가체프", 5.0, 4.2, "첫 번째 로스팅"),
        ("케냐 AA FAQ", 6.0, 5.1, "미디엄 로스트"),
        ("콜롬비아 우일라", 5.5, 4.6, "다크 로스트"),
        ("과테말라 안티구아", 5.2, 4.4, "시티 로스트"),
        ("브라질 파젠다 카르모", 6.5, 5.5, "에스프레소 블렌드"),
    ]

    for i in range(6):  # 6 weeks of data
        for bean_name, green_w, roasted_w, note in sample_logs:
            log_date = base_date + timedelta(days=i*5)
            cursor.execute('''
                INSERT INTO roasting_logs
                (date, bean_name, green_weight_kg, roasted_weight_kg, bean_cost_per_kg, notes)
                VALUES (?, ?, ?, ?, (SELECT price_per_kg FROM bean_prices WHERE bean_name = ?), ?)
            ''', (log_date.date().isoformat(), bean_name, green_w, roasted_w, bean_name, note))

    conn.commit()
    conn.close()
    print("✅ 테스트 데이터가 생성되었습니다.")

if __name__ == '__main__':
    create_test_data()
