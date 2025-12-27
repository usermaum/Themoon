"""
DB 상태 검증 스크립트
"""
import sys
import os
from sqlalchemy import text
from dotenv import load_dotenv

# backend 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# 환경 변수 로드
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

from app.database import engine, SessionLocal
from app.models.bean import Bean

def check_db_status():
    print("🔍 Checking Database Status...")
    db = SessionLocal()
    try:
        # Check Tables
        print("\n[1] Checking Tables and Columns:")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]
            print(f"   Found Tables: {tables}")
            
            if 'beans' in tables:
                columns = conn.execute(text("PRAGMA table_info(beans);")).fetchall()
                col_names = [col[1] for col in columns]
                print(f"   'beans' Columns: {col_names}")
                
                if 'expected_loss_rate' in col_names:
                     print("   ✅ 'expected_loss_rate' column exists.")
                else:
                     print("   ❌ 'expected_loss_rate' column missing!")

            if 'inventory_logs' in tables:
                columns = conn.execute(text("PRAGMA table_info(inventory_logs);")).fetchall()
                col_names = [col[1] for col in columns]
                print(f"   'inventory_logs' Columns: {col_names}")

        # Check Data Count
        print("\n[2] Checking Data Count:")
        bean_count = db.query(Bean).count()
        print(f"   Total Beans: {bean_count}")
        
        # Check Specific Data
        print("\n[3] Checking Specific Data (First 3):")
        beans = db.query(Bean).limit(3).all()
        for b in beans:
            loss_rate = getattr(b, 'expected_loss_rate', 'N/A')
            print(f"   - ID: {b.id}, Name: {b.name}, LossRate: {loss_rate}")

    except Exception as e:
        print(f"\n❌ Error checking DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db_status()
