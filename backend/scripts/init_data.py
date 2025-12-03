import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.bean import Bean
from app.models.recipe import Recipe

def init_db():
    db = SessionLocal()
    try:
        # Check if data exists
        if db.query(Bean).first():
            print("Data already exists. Skipping initialization.")
            return

        # Create Green Beans
        eth = Bean(name="Ethiopia Yirgacheffe", type="GREEN_BEAN", origin="Ethiopia", origin_code="Eth", quantity_kg=100, cost_price=15000)
        col = Bean(name="Colombia Supremo", type="GREEN_BEAN", origin="Colombia", origin_code="Co", quantity_kg=100, cost_price=12000)
        bra = Bean(name="Brazil Santos", type="GREEN_BEAN", origin="Brazil", origin_code="Br", quantity_kg=100, cost_price=10000)
        
        db.add_all([eth, col, bra])
        db.commit()
        
        # Create Blend Bean
        full_moon = Bean(name="Full Moon Blend", type="BLEND", quantity_kg=0, cost_price=0)
        db.add(full_moon)
        db.commit()
        
        # Create Recipe
        r1 = Recipe(blend_bean_id=full_moon.id, ingredient_bean_id=eth.id, ratio_percent=40)
        r2 = Recipe(blend_bean_id=full_moon.id, ingredient_bean_id=col.id, ratio_percent=30)
        r3 = Recipe(blend_bean_id=full_moon.id, ingredient_bean_id=bra.id, ratio_percent=30)
        
        db.add_all([r1, r2, r3])
        db.commit()
        
        print("Initial data loaded successfully.")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
