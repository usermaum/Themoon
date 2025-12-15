"""
다국어 데이터 마이그레이션 및 시딩 스크립트
1. DB 테이블 스키마 자동 업데이트 (ALTER TABLE)
2. Themoon_Rostings_v2.md 기준 데이터 업데이트 (한글/영문 매핑)
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models.bean import Bean, BeanType
# Import InventoryLog to ensure it's registered with Base to avoid relationship errors
try:
    from app.models.inventory_log import InventoryLog
except ImportError:
    pass # Might fail if table doesn't exist yet but usually fine for model registration

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 마스터 데이터 정의 (from Themoon_Rostings_v2.md)
BEAN_MASTER_DATA = [
    {
        "name_ko": "예가체프", "name_en": "Ethiopia G2 Yirgacheffe Washed",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "G2 Washed"
    },
    {
        "name_ko": "모모라", "name_en": "Ethiopia G1 Danse Mormora Natural",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "G1 Natural"
    },
    {
        "name_ko": "코케허니", "name_en": "Ethiopia G1 Yirgacheffe Koke Honey Natural",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "G1 Honey"
    },
    {
        "name_ko": "우라가", "name_en": "Ethiopia G1 Guji Uraga Washed",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "G1 Washed"
    },
    {
        "name_ko": "시다모", "name_en": "Ethiopia G4 Sidamo Natural",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "G4 Natural"
    },
    {
        "name_ko": "마사이", "name_en": "Kenya AA FAQ",
        "origin_ko": "케냐", "origin_en": "Kenya", "origin_code": "K",
        "grade": "AA FAQ"
    },
    {
        "name_ko": "키린야가", "name_en": "Kenya PB TOP Kirinyaga",
        "origin_ko": "케냐", "origin_en": "Kenya", "origin_code": "K",
        "grade": "PB"
    },
    {
        "name_ko": "후일라", "name_en": "Colombia Supremo Huila",
        "origin_ko": "콜롬비아", "origin_en": "Colombia", "origin_code": "Co",
        "grade": "Supremo"
    },
    {
        "name_ko": "안티구아", "name_en": "Guatemala SHB Antigua",
        "origin_ko": "과테말라", "origin_en": "Guatemala", "origin_code": "Gu",
        "grade": "SHB"
    },
    {
        "name_ko": "엘탄케", "name_en": "Costa Rica El Tanque",
        "origin_ko": "코스타리카", "origin_en": "Costa Rica", "origin_code": "Cos",
        "grade": ""
    },
    {
        "name_ko": "파젠다 카르모", "name_en": "Brazil Fazenda Carmo Estate Natural",
        "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Br",
        "grade": "SC16UP"
    },
    {
        "name_ko": "산토스", "name_en": "Brazil NY2 FC Santos",
        "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Br",
        "grade": "NY2 FC"
    },
    {
        "name_ko": "디카페 SDM", "name_en": "Ethiopia Decaf (SDM)",
        "origin_ko": "에티오피아", "origin_en": "Ethiopia", "origin_code": "Eth",
        "grade": "Decaf"
    },
    {
        "name_ko": "디카페 SM", "name_en": "Colombia Supremo Popayan Sugarcane Decaf",
        "origin_ko": "콜롬비아", "origin_en": "Colombia", "origin_code": "Co",
        "grade": "Decaf"
    },
    {
        "name_ko": "스위스워터", "name_en": "Brazil Swiss Water Decaf",
        "origin_ko": "브라질", "origin_en": "Brazil", "origin_code": "Br",
        "grade": "Decaf"
    },
    {
        "name_ko": "게이샤", "name_en": "Panama Elida Estate Geisha Natural",
        "origin_ko": "파나마", "origin_en": "Panama", "origin_code": "Pa",
        "grade": "Specialty"
    }
]

def update_schema(engine):
    """DB 스키마 변경 (컬럼 추가)"""
    with engine.connect() as conn:
        # SQLite 특성상 add column은 하나씩
        try:
            conn.execute(text("ALTER TABLE beans ADD COLUMN name_ko VARCHAR(100)"))
            print("Added name_ko column")
        except Exception as e:
            print(f"Skipping name_ko (maybe exists): {e}")

        try:
            conn.execute(text("ALTER TABLE beans ADD COLUMN name_en VARCHAR(200)"))
            print("Added name_en column")
        except Exception as e:
            print(f"Skipping name_en (maybe exists): {e}")

        try:
            conn.execute(text("ALTER TABLE beans ADD COLUMN origin_ko VARCHAR(50)"))
            print("Added origin_ko column")
        except Exception as e:
            print(f"Skipping origin_ko (maybe exists): {e}")
            
        try:
            conn.execute(text("ALTER TABLE beans ADD COLUMN origin_en VARCHAR(50)"))
            print("Added origin_en column")
        except Exception as e:
            print(f"Skipping origin_en (maybe exists): {e}")

def seed_data(db: Session):
    """데이터 업데이트 및 시딩"""
    print("Updating Bean Data...")
    
    for item in BEAN_MASTER_DATA:
        # 1. 이름으로 조회 (Legacy name or name_ko)
        bean = db.query(Bean).filter(Bean.name == item['name_ko']).first()
        
        if not bean:
            # 새로 생성
            print(f"Creating new bean: {item['name_ko']}")
            bean = Bean(
                name=item['name_ko'],
                type=BeanType.GREEN_BEAN,
                origin=item['origin_code']
            )
            db.add(bean)
        
        # 데이터 업데이트
        bean.name_ko = item['name_ko']
        bean.name_en = item['name_en']
        bean.origin_ko = item['origin_ko']
        bean.origin_en = item['origin_en']
        if item['grade']:
            bean.grade = item['grade']
            
        print(f"Updated: {bean.name_ko} / {bean.name_en}")

    db.commit()
    print("Seed completed successfully!")

if __name__ == "__main__":
    # 1. Schema Migration (Manual)
    update_schema(engine)
    
    # 2. Data Seeding
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
