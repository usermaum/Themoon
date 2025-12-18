"""
[Seeding Script] TheMoon v2.0
- Suppliers
- Beans (Green, Roasted, Blend)
- Inventory Logs
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.supplier import Supplier
from app.models.inventory_log import InventoryLog, InventoryChangeType

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        print("🌱 Seeding Data Started...")

        # 1. Suppliers
        suppliers_data = [
            {"name": "GSC International", "phone": "02-1234-5678", "email": "order@gsc.co.kr", "address": "Seoul, Korea"},
            {"name": "Almacielo", "phone": "02-9876-5432", "email": "info@almacielo.com", "address": "Gyeonggi, Korea"},
            {"name": "Royal Coffee", "phone": "1-510-652-4256", "email": "sales@royalcoffee.com", "address": "USA"},
        ]
        
        suppliers = []
        for s_data in suppliers_data:
            supplier = db.query(Supplier).filter(Supplier.name == s_data["name"]).first()
            if not supplier:
                supplier = Supplier(
                    name=s_data["name"],
                    contact_phone=s_data["phone"],
                    contact_email=s_data["email"],
                    address=s_data["address"]
                )
                db.add(supplier)
                db.flush() # get ID
                print(f"Created Supplier: {supplier.name}")
            suppliers.append(supplier)

        # 2. Green Beans
        green_beans_data = [
            {"name_ko": "예가체프 G2", "name_en": "Ethiopia Yirgacheffe G2", "origin_code": "Eth", "sku": "GB-ETH-YIR-G2", "price": 18000},
            {"name_ko": "케냐 AA", "name_en": "Kenya AA FAQ", "origin_code": "Ken", "sku": "GB-KEN-AA", "price": 22000},
            {"name_ko": "콜롬비아 수프리모", "name_en": "Colombia Supremo", "origin_code": "Col", "sku": "GB-COL-SUP", "price": 16500},
            {"name_ko": "과테말라 안티구아", "name_en": "Guatemala Antigua SHB", "origin_code": "Gua", "sku": "GB-GUA-ANT", "price": 17800},
            {"name_ko": "브라질 세하도", "name_en": "Brazil Cerrado NY2", "origin_code": "Bra", "sku": "GB-BRA-CER", "price": 12000},
        ]

        green_beans = []
        for b_data in green_beans_data:
            bean = db.query(Bean).filter(Bean.sku == b_data["sku"]).first()
            if not bean:
                bean = Bean(
                    name=b_data["name_ko"], # Legacy compatibility
                    name_ko=b_data["name_ko"],
                    name_en=b_data["name_en"],
                    origin=b_data["origin_code"], # Legacy
                    origin_ko=b_data["origin_code"], # Simplified for now
                    type=BeanType.GREEN_BEAN,
                    sku=b_data["sku"],
                    grade="Standard",
                    avg_price=b_data["price"],
                    quantity_kg=0 # Will add logs
                )
                db.add(bean)
                db.flush()
                print(f"Created Green Bean: {bean.name_ko}")
            
            green_beans.append(bean)

            # Add Initial Stock Log
            if bean.quantity_kg == 0:
                initial_qty = random.randint(20, 100)
                log = InventoryLog(
                    bean_id=bean.id,
                    change_type=InventoryChangeType.PURCHASE,
                    change_amount=initial_qty,
                    current_quantity=initial_qty,
                    notes="Initial Seed Stock"
                )
                bean.quantity_kg = initial_qty
                db.add(log)
        
        # 3. Roasted Beans
        if green_beans:
            parent_bean = green_beans[0] # Yirgacheffe
            roasted_sku = "RB-ETH-YIR-L"
            r_bean = db.query(Bean).filter(Bean.sku == roasted_sku).first()
            if not r_bean:
                r_bean = Bean(
                    name=f"Roasting: {parent_bean.name_ko}",
                    name_ko=f"볶은 {parent_bean.name_ko}",
                    type=BeanType.ROASTED_BEAN,
                    sku=roasted_sku,
                    roast_profile=RoastProfile.LIGHT,
                    parent_bean_id=parent_bean.id,
                    quantity_kg=5.0,
                    avg_price=parent_bean.avg_price * 1.2 # Simple calculation
                )
                db.add(r_bean)
                print(f"Created Roasted Bean: {r_bean.name_ko}")

        db.commit()
        print("✅ Seeding Complete!")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
