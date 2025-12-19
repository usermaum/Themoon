"""
Render.com PostgreSQL 데이터베이스 확인
"""
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.bean import Bean
from app.models.supplier import Supplier
from app.models.blend import Blend
from app.models.inventory_log import InventoryLog

# DATABASE_URL from environment
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_data():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("📊 Render.com PostgreSQL 데이터 확인")
        print("=" * 60)

        # Count tables
        suppliers_count = db.query(Supplier).count()
        beans_count = db.query(Bean).count()
        blends_count = db.query(Blend).count()
        logs_count = db.query(InventoryLog).count()

        print(f"\n✅ 데이터 요약:")
        print(f"   - Suppliers: {suppliers_count}개")
        print(f"   - Beans: {beans_count}개")
        print(f"   - Blends: {blends_count}개")
        print(f"   - Inventory Logs: {logs_count}개")

        # Sample data
        print(f"\n📦 샘플 Beans (처음 5개):")
        beans = db.query(Bean).limit(5).all()
        for bean in beans:
            print(f"   - {bean.name} ({bean.type.value}) - {bean.quantity_kg}kg")

        print(f"\n🌱 Blends:")
        blends = db.query(Blend).all()
        for blend in blends:
            print(f"   - {blend.name}: {blend.description}")

        print("\n✅ 데이터베이스 확인 완료!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()
