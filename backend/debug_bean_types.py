from app.database import SessionLocal
from app.models.bean import Bean
from app.models.blend import Blend
from app.models.inventory_log import InventoryLog

def check_bean_types():
    db = SessionLocal()
    try:
        beans = db.query(Bean).all()
        print(f"{'ID':<5} {'Name':<30} {'Type':<15} {'Origin':<15}")
        print("-" * 70)
        for bean in beans:
            print(f"{bean.id:<5} {bean.name:<30} {bean.type:<15} {bean.origin:<15}")
    finally:
        db.close()

if __name__ == "__main__":
    check_bean_types()
