"""
DB 초기화 및 시딩 스크립트
Ref: Documents/Planning/Themoon_Rostings_v2.md

실행 방법:
cd backend
python scripts/recreate_db.py
"""
import sys
import os
from dotenv import load_dotenv

# backend 디렉토리를 sys.path에 추가하여 app 모듈을 찾을 수 있게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# 환경 변수 로드 (.env)
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

from app.database import engine, Base, SessionLocal
from app.models.bean import Bean, BeanType
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.blend import Blend

def init_db():
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")

def seed_data():
    db = SessionLocal()
    try:
        print("🌱 Seeding initial green beans...")
        
        # 2.1 생두 및 원두 마스터 (Bean Master List)
        initial_beans = [
            # 에티오피아
            {"name": "예가체프", "origin": "Ethiopia", "variety": "Yirgacheffe", "grade": "G2 Washed", "processing_method": "Washed", "avg_price": 12000, "quantity_kg": 20},
            {"name": "모모라", "origin": "Ethiopia", "variety": "Mormora", "grade": "G1 Natural", "processing_method": "Natural", "avg_price": 20000, "quantity_kg": 15},
            {"name": "코케허니", "origin": "Ethiopia", "variety": "Koke Honey", "grade": "G1 Honey", "processing_method": "Natural", "avg_price": 21000, "quantity_kg": 10},
            {"name": "우라가", "origin": "Ethiopia", "variety": "Uraga", "grade": "G1 Washed", "processing_method": "Washed", "avg_price": 22000, "quantity_kg": 10},
            {"name": "시다모", "origin": "Ethiopia", "variety": "Sidamo", "grade": "G4 Natural", "processing_method": "Natural", "avg_price": 11000, "quantity_kg": 30},
            
            # 케냐
            {"name": "마사이", "origin": "Kenya", "variety": "Masai", "grade": "AA FAQ", "processing_method": "Washed", "avg_price": 18000, "quantity_kg": 15},
            {"name": "키린야가", "origin": "Kenya", "variety": "Kirinyaga", "grade": "PB TOP", "processing_method": "Washed", "avg_price": 19000, "quantity_kg": 10},
            
            # 중남미
            {"name": "후일라", "origin": "Colombia", "variety": "Huila", "grade": "Supremo", "processing_method": "Washed", "avg_price": 13000, "quantity_kg": 40},
            {"name": "안티구아", "origin": "Guatemala", "variety": "Antigua", "grade": "SHB", "processing_method": "Washed", "avg_price": 14000, "quantity_kg": 25},
            {"name": "엘탄케", "origin": "Costa Rica", "variety": "El Tanque", "grade": "SHB", "processing_method": "Washed", "avg_price": 16000, "quantity_kg": 15},
            {"name": "파젠다 카르모", "origin": "Brazil", "variety": "Fazenda Carmo", "grade": "SC16UP", "processing_method": "Natural", "avg_price": 10000, "quantity_kg": 50},
            {"name": "산토스", "origin": "Brazil", "variety": "Santos", "grade": "NY2 FC", "processing_method": "Natural", "avg_price": 11000, "quantity_kg": 50},
            
            # 디카페인
            {"name": "디카페 SDM", "origin": "Ethiopia", "variety": "Decaf SDM", "grade": "Decaf", "processing_method": "Mountain Water", "avg_price": 18000, "quantity_kg": 10},
            {"name": "디카페 SM", "origin": "Colombia", "variety": "Decaf SM", "grade": "Decaf", "processing_method": "Sugarcane", "avg_price": 17000, "quantity_kg": 10},
            {"name": "스위스워터", "origin": "Brazil", "variety": "Swiss Water", "grade": "Decaf", "processing_method": "Swiss Water", "avg_price": 16000, "quantity_kg": 10},
            
            # 스페셜티
            {"name": "게이샤", "origin": "Panama", "variety": "Geisha", "grade": "Specialty", "processing_method": "Natural", "avg_price": 250000, "quantity_kg": 2},
        ]

        for bean_data in initial_beans:
            bean = Bean(
                name=bean_data["name"],
                type=BeanType.GREEN_BEAN,
                origin=bean_data["origin"],
                variety=bean_data["variety"],
                grade=bean_data["grade"],
                processing_method=bean_data["processing_method"],
                avg_price=bean_data["avg_price"],
                quantity_kg=bean_data["quantity_kg"],
                sku=f"{bean_data['origin'][:3].upper()}-{bean_data['name']}" # 임시 SKU
            )
            db.add(bean)
            db.flush() # ID 생성을 위해
            
            # 초기 재고 로그 생성
            if bean.quantity_kg > 0:
                log = InventoryLog(
                    bean_id=bean.id,
                    change_type=InventoryChangeType.PURCHASE,
                    change_amount=bean.quantity_kg,
                    current_quantity=bean.quantity_kg,
                    notes="Initial Seed Data"
                )
                db.add(log)
        
        # 2.2 블렌드 마스터 (Blend Master List)
        print("🌱 Seeding initial blends...")
        initial_blends = [
            {
                "name": "더 문 시그니처 블렌드",
                "description": "깊은 바디감과 화사한 산미의 조화",
                "recipe": [
                    {"bean_id": 1, "ratio": 0.4}, # 예가체프
                    {"bean_id": 8, "ratio": 0.3}, # 후일라
                    {"bean_id": 11, "ratio": 0.3} # 파젠다 카르모
                ],
                "target_roast_level": "Medium Dark",
                "notes": "대표 블렌드"
            },
            {
                "name": "에스프레소 다크",
                "description": "강렬한 바디와 스모키한 후미",
                "recipe": [
                    {"bean_id": 11, "ratio": 0.5}, # 파젠다 카르모
                    {"bean_id": 12, "ratio": 0.3}, # 산토스
                    {"bean_id": 9, "ratio": 0.2}   # 안티구아
                ],
                "target_roast_level": "Dark",
                "notes": "라떼용 추천"
            }
        ]

        for blend_data in initial_blends:
            blend = Blend(
                name=blend_data["name"],
                description=blend_data["description"],
                recipe=blend_data["recipe"],
                target_roast_level=blend_data["target_roast_level"],
                notes=blend_data["notes"]
            )
            db.add(blend)

        db.commit()
        print(f"🌱 Seeded {len(initial_beans)} green beans and {len(initial_blends)} blends successfully.")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_data()
