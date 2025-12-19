"""
[FINAL] Recreate and Seed Script (v0.2.0 Compatible)
- Drops all tables
- Creates all tables (latest schema)
- Seeds rich multilingual bean data (from seed_multilingual_beans.py)
- Seeds Suppliers, Blends, Inbound Docs, Inventory Logs
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
from app.models.blend import Blend
# Import InboundDocument to ensure it's registered
try:
    from app.models.inbound_document import InboundDocument
except ImportError:
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==========================================
# 1. Master Data (Consolidated)
# ==========================================

BEAN_MASTER_DATA = [
    # Ethiopia
    {"name_ko": "예가체프", "name_en": "Ethiopia G2 Yirgacheffe Washed", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "G2 Washed", "variety": "Yirgacheffe", "processing_method": "Washed", "avg_price": 18000},
    {"name_ko": "모모라", "name_en": "Ethiopia G1 Danse Mormora Natural", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "G1 Natural", "variety": "Mormora", "processing_method": "Natural", "avg_price": 20000},
    {"name_ko": "코케허니", "name_en": "Ethiopia G1 Yirgacheffe Koke Honey Natural", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "G1 Honey", "variety": "Koke Honey", "processing_method": "Natural", "avg_price": 21000},
    {"name_ko": "우라가", "name_en": "Ethiopia G1 Guji Uraga Washed", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "G1 Washed", "variety": "Uraga", "processing_method": "Washed", "avg_price": 22000},
    {"name_ko": "시다모", "name_en": "Ethiopia G4 Sidamo Natural", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "G4 Natural", "variety": "Sidamo", "processing_method": "Natural", "avg_price": 11000},
    
    # Kenya
    {"name_ko": "마사이", "name_en": "Kenya AA FAQ", "origin": "Kenya", "origin_ko": "케냐", "origin_en": "Kenya", "origin_code": "Ken", "grade": "AA FAQ", "variety": "Masai", "processing_method": "Washed", "avg_price": 24000},
    {"name_ko": "키린야가", "name_en": "Kenya PB TOP Kirinyaga", "origin": "Kenya", "origin_ko": "케냐", "origin_en": "Kenya", "origin_code": "Ken", "grade": "PB", "variety": "Kirinyaga", "processing_method": "Washed", "avg_price": 26000},
    
    # Latin America
    {"name_ko": "후일라", "name_en": "Colombia Supremo Huila", "origin": "Colombia", "origin_ko": "콜롬비아", "origin_en": "Colombia", "origin_code": "Col", "grade": "Supremo", "variety": "Huila", "processing_method": "Washed", "avg_price": 16500},
    {"name_ko": "안티구아", "name_en": "Guatemala SHB Antigua", "origin": "Guatemala", "origin_ko": "과테말라", "origin_en": "Guatemala", "origin_code": "Gua", "grade": "SHB", "variety": "Antigua", "processing_method": "Washed", "avg_price": 17800},
    {"name_ko": "엘탄케", "name_en": "Costa Rica El Tanque", "origin": "Costa Rica", "origin_ko": "코스타리카", "origin_en": "Costa Rica", "origin_code": "Cos", "grade": "SHB", "variety": "El Tanque", "processing_method": "Washed", "avg_price": 19000},
    {"name_ko": "파젠다 카르모", "name_en": "Brazil Fazenda Carmo Estate Natural", "origin": "Brazil", "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Bra", "grade": "SC16UP", "variety": "Fazenda Carmo", "processing_method": "Natural", "avg_price": 12000},
    {"name_ko": "산토스", "name_en": "Brazil NY2 FC Santos", "origin": "Brazil", "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Bra", "grade": "NY2 FC", "variety": "Santos", "processing_method": "Natural", "avg_price": 11500},

    # Decaf
    {"name_ko": "디카페 SDM", "name_en": "Ethiopia Decaf (SDM)", "origin": "Ethiopia", "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth", "grade": "Decaf", "variety": "Decaf", "processing_method": "Mountain Water", "avg_price": 23000},
    {"name_ko": "디카페 SM", "name_en": "Colombia Supremo Popayan Sugarcane Decaf", "origin": "Colombia", "origin_ko": "콜롬비아", "origin_en": "Colombia", "origin_code": "Col", "grade": "Decaf", "variety": "Decaf", "processing_method": "Sugarcane", "avg_price": 22000},
    {"name_ko": "스위스워터", "name_en": "Brazil Swiss Water Decaf", "origin": "Brazil", "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Bra", "grade": "Decaf", "variety": "Decaf", "processing_method": "Swiss Water", "avg_price": 21000},
    
    # Specialty
    {"name_ko": "게이샤", "name_en": "Panama Elida Estate Geisha Natural", "origin": "Panama", "origin_ko": "파나마", "origin_en": "Panama", "origin_code": "Pa", "grade": "Specialty", "variety": "Geisha", "processing_method": "Natural", "avg_price": 250000}
]

BLEND_MASTER_DATA = [
    {
        "name": "풀문 (Full Moon)",
        "description": "더문의 대표 하우스 블렌드",
        "recipe_names": ["마사이", "안티구아", "모모라", "시다모"],
        "ratios": [0.4, 0.4, 0.1, 0.1],
        "target_roast_level": "Medium Dark",
        "notes": "대표 블렌드"
    },
    {
        "name": "뉴문 (New Moon)",
        "description": "대중적인 고소한 맛",
        "recipe_names": ["산토스", "후일라", "시다모"],
        "ratios": [0.6, 0.3, 0.1],
        "target_roast_level": "Medium",
        "notes": "고소한 맛"
    },
    {
        "name": "이클립스문 (Eclipse Moon)",
        "description": "디카페인 블렌드",
        "recipe_names": ["디카페 SM", "스위스워터"],
        "ratios": [0.6, 0.4],
        "target_roast_level": "Medium Dark",
        "notes": "디카페인"
    }
]

SUPPLIER_MASTER_DATA = [
     {"name": "GSC International", "phone": "02-1234-5678", "email": "order@gsc.co.kr", "address": "Seoul, Korea"},
     {"name": "Almacielo", "phone": "02-9876-5432", "email": "info@almacielo.com", "address": "Gyeonggi, Korea"},
     {"name": "Royal Coffee", "phone": "1-510-652-4256", "email": "sales@royalcoffee.com", "address": "USA"},
]

# ==========================================
# 2. Functions
# ==========================================

def recreate_tables():
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")

def seed_suppliers(db):
    print("🌱 Seeding Suppliers...")
    for s_data in SUPPLIER_MASTER_DATA:
        s = Supplier(
            name=s_data["name"],
            contact_phone=s_data["phone"],
            contact_email=s_data["email"],
            address=s_data["address"],
            representative_name="Manager"
        )
        db.add(s)
    db.commit()

def generate_sku(origin_code, name_en):
    # e.g., "GB-ETH-YIR"
    short_name = name_en.split()[0][:3].upper() # Yirgacheffe -> Yir
    if len(name_en.split()) > 1:
        short_name = name_en.split()[1][:3].upper()
    return f"GB-{origin_code.upper()}-{short_name}-{random.randint(100,999)}"

def seed_beans(db):
    print("🌱 Seeding Green Beans...")
    bean_map = {} # name -> bean_id
    
    for item in BEAN_MASTER_DATA:
        sku = generate_sku(item['origin_code'], item['name_en'])
        
        bean = Bean(
            name=item['name_ko'], # Legacy
            name_ko=item['name_ko'],
            name_en=item['name_en'],
            origin=item['origin'], # Legacy
            origin_ko=item['origin_ko'],
            origin_en=item['origin_en'],
            variety=item.get('variety'),
            processing_method=item.get('processing_method'),
            grade=item.get('grade'),
            type=BeanType.GREEN_BEAN,
            avg_price=item['avg_price'],
            sku=sku,
            expected_loss_rate=0.15,
            quantity_kg=0
        )
        db.add(bean)
        db.flush()
        bean_map[item['name_ko']] = bean.id
        
        # Initial Stock Log
        initial_qty = random.randint(20, 100)
        bean.quantity_kg = initial_qty
        
        log = InventoryLog(
            bean_id=bean.id,
            change_type=InventoryChangeType.PURCHASE,
            change_amount=initial_qty,
            current_quantity=initial_qty,
            notes="Initial Seed Stock"
        )
        db.add(log)
        print(f"   Created: {bean.name_ko} ({bean.quantity_kg}kg)")

    # Roasted variants (Sample)
    print("🌱 Seeding Roasted Variants...")
    yirga_id = bean_map.get("예가체프")
    if yirga_id:
        parent = db.query(Bean).get(yirga_id)
        r_bean = Bean(
            name=f"Roasting: {parent.name_ko}",
            name_ko=f"볶은 {parent.name_ko}",
            name_en=f"Roasted {parent.name_en}",
            type=BeanType.ROASTED_BEAN,
            sku=f"RB-{parent.sku.split('-')[1]}-L",
            roast_profile=RoastProfile.LIGHT,
            parent_bean_id=parent.id,
            avg_price=parent.avg_price * 1.2,
            quantity_kg=5.0
        )
        db.add(r_bean)
        db.flush()
        
        log = InventoryLog(
             bean_id=r_bean.id,
             change_type=InventoryChangeType.ROASTING_OUTPUT,
             change_amount=5.0,
             current_quantity=5.0,
             notes="Sample Roasting"
        )
        db.add(log)

    db.commit()
    return bean_map

def seed_blends(db, bean_map):
    print("🌱 Seeding Blends...")
    for b_data in BLEND_MASTER_DATA:
        recipe = []
        for i, b_name in enumerate(b_data['recipe_names']):
            bid = bean_map.get(b_name)
            if bid:
                recipe.append({"bean_id": bid, "ratio": b_data['ratios'][i]})
        
        if recipe:
            blend = Blend(
                name=b_data['name'],
                description=b_data['description'],
                target_roast_level=b_data['target_roast_level'],
                notes=b_data['notes'],
                recipe=recipe
            )
            db.add(blend)
            print(f"   Created Blend: {blend.name}")

    db.commit()

# ==========================================
# 3. Main Execution
# ==========================================

def main():
    recreate_tables()
    
    db = SessionLocal()
    try:
        seed_suppliers(db)
        bean_map = seed_beans(db)
        seed_blends(db, bean_map)
        print("✅ Database Recreated and Seeded Successfully!")
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    main()
