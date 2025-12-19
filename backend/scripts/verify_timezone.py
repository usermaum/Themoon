
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.bean import Bean, BeanType
from app.utils.timezone import get_kst_now

def verify_timezone():
    print(f"Testing get_kst_now()...")
    now = get_kst_now()
    print(f"Type: {type(now)}")
    print(f"Value: {now}")
    print(f"Tzinfo: {now.tzinfo}")

    db = SessionLocal()
    try:
        print("\nAttempting DB Insert...")
        bean = Bean(
            name="Timezone Test Bean",
            type=BeanType.GREEN_BEAN,
            quantity_kg=1.0,
            # created_at should default to get_kst_now()
        )
        db.add(bean)
        db.commit()
        db.refresh(bean)
        
        print("✅ Insert Successful")
        print(f"ID: {bean.id}")
        print(f"Created At: {bean.created_at} (Type: {type(bean.created_at)})")
        print(f"Updated At: {bean.updated_at} (Type: {type(bean.updated_at)})")
        
        # Cleanup
        db.delete(bean)
        db.commit()
        print("Cleanup Done")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    verify_timezone()
