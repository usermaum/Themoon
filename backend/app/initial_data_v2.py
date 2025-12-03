from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.bean import Bean
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db = SessionLocal()
    try:
        # Clear existing beans (Optional: User asked to initialize, implying reset or upsert. 
        # Safest is to check existence or clear if "reset" is intended. 
        # User said "초기화 하여" (initialize/reset), so let's clear existing GREEN beans or all beans?
        # "기본 원두 리스트 1~16번 기본값으로 입력해줘" -> Let's truncate or delete all beans to be safe and clean.
        # But be careful of foreign keys if we have roasting logs. 
        # Since we are in dev/setup phase, let's try to delete all.
        
        db.query(Bean).delete()
        db.commit()
        logger.info("Cleared existing beans.")

        beans_data = [
            {"name": "예가체프", "english_name": "Ethiopia G2 Yirgacheffe Washed", "origin": "Ethiopia", "origin_code": "Eth", "grade": "G2 Washed", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "모모라", "english_name": "Ethiopia G1 Danse Mormora Natural", "origin": "Ethiopia", "origin_code": "Eth", "grade": "G1 Natural", "variety": "Arabica", "processing_method": "Natural", "notes": "구지 지역"},
            {"name": "코케허니", "english_name": "Ethiopia G1 Yirgacheffe Koke Honey Natural", "origin": "Ethiopia", "origin_code": "Eth", "grade": "G1 Honey", "variety": "Arabica", "processing_method": "Honey"},
            {"name": "우라가", "english_name": "Ethiopia G1 Guji Uraga Washed", "origin": "Ethiopia", "origin_code": "Eth", "grade": "G1 Washed", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "시다모", "english_name": "Ethiopia G4 Sidamo Natural", "origin": "Ethiopia", "origin_code": "Eth", "grade": "G4 Natural", "variety": "Arabica", "processing_method": "Natural"},
            {"name": "마사이", "english_name": "Kenya AA FAQ", "origin": "Kenya", "origin_code": "K", "grade": "AA FAQ", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "키린야가", "english_name": "Kenya PB TOP Kirinyaga", "origin": "Kenya", "origin_code": "K", "grade": "PB", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "후일라", "english_name": "Colombia Supremo Huila", "origin": "Colombia", "origin_code": "Co", "grade": "Supremo", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "안티구아", "english_name": "Guatemala SHB Antigua", "origin": "Guatemala", "origin_code": "Gu", "grade": "SHB", "variety": "Arabica", "processing_method": "Washed"},
            {"name": "엘탄케", "english_name": "Costa Rica El Tanque", "origin": "Costa Rica", "origin_code": "Cos", "grade": None, "variety": "Arabica", "processing_method": "Washed"},
            {"name": "파젠다 카르모", "english_name": "Brazil Fazenda Carmo Estate Natural", "origin": "Brazil", "origin_code": "Br", "grade": "SC16UP", "variety": "Arabica", "processing_method": "Natural"},
            {"name": "산토스", "english_name": "Brazil NY2 FC Santos", "origin": "Brazil", "origin_code": "Br", "grade": "NY2 FC", "variety": "Arabica", "processing_method": "Natural"},
            {"name": "디카페 SDM", "english_name": "Ethiopia Decaf (SDM)", "origin": "Ethiopia", "origin_code": "Eth", "grade": "Decaf", "variety": "Arabica", "processing_method": "Decaf"},
            {"name": "디카페 SM", "english_name": "Colombia Supremo Popayan Sugarcane Decaf", "origin": "Colombia", "origin_code": "Co", "grade": "Decaf (Sugarcane)", "variety": "Arabica", "processing_method": "Decaf"},
            {"name": "스위스워터", "english_name": "Brazil Swiss Water Decaf", "origin": "Brazil", "origin_code": "Br", "grade": "Decaf (Swiss Water)", "variety": "Arabica", "processing_method": "Decaf"},
            {"name": "게이샤", "english_name": "Panama Elida Estate Geisha Natural", "origin": "Panama", "origin_code": "Pa", "grade": "Specialty", "variety": "Geisha", "processing_method": "Natural", "notes": "고가 품목"},
        ]

        for bean_data in beans_data:
            bean = Bean(
                type="GREEN_BEAN",
                quantity_kg=0.0,
                avg_cost_price=0.0,
                **bean_data
            )
            db.add(bean)
        
        db.commit()
        logger.info("Successfully initialized 16 beans.")

    except Exception as e:
        logger.error(f"Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
