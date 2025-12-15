from app.database import SessionLocal
from app.models.bean import Bean, BeanType
from app.models.blend import Blend
from app.models.inventory_log import InventoryLog

def fix_blend_types():
    db = SessionLocal()
    try:
        # Find beans that should be BLEND_BEAN
        # Based on naming convention in this project (Full Moon, New Moon, Eclipse Moon)
        # And commonly 'Blend' in name
        
        search_terms = ['Moon', 'Blend', '블렌드']
        count = 0
        
        beans = db.query(Bean).all()
        for bean in beans:
            is_blend = False
            for term in search_terms:
                if term in bean.name:
                    is_blend = True
                    break
            
            if is_blend and bean.type != BeanType.BLEND_BEAN:
                print(f"Updating {bean.name} (ID: {bean.id}) from {bean.type} to BLEND_BEAN")
                bean.type = BeanType.BLEND_BEAN
                count += 1
        
        if count > 0:
            db.commit()
            print(f"Successfully updated {count} beans to BLEND_BEAN.")
        else:
            print("No beans needed updating.")
            
    finally:
        db.close()

if __name__ == "__main__":
    fix_blend_types()
