import sys
import os
from unittest.mock import MagicMock

# Mock dependencies before importing app modules
sys.modules['psutil'] = MagicMock()
sys.modules['magic'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()

# Override DATABASE_URL for Windows environment before any app imports
os.environ['DATABASE_URL'] = 'sqlite:///D:/Ai/WslProject/Themoon/themoon.db'

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal
from app.api.v1.roasting import get_roasting_service
from app.models.bean import Bean, BeanType, RoastProfile
from app.repositories.bean_repository import BeanRepository

def verify_roasting():
    db: Session = SessionLocal()
    try:
        service = get_roasting_service(db)
        bean_repo = BeanRepository(db)
        
        # 1. Find a green bean for testing
        green_bean = db.query(Bean).filter(Bean.type == BeanType.GREEN_BEAN, Bean.quantity_kg > 5.0).first()
        if not green_bean:
            print("No suitable green bean found for testing.")
            return

        print(f"Testing with Bean: {green_bean.name} (ID: {green_bean.id}, Current Qty: {green_bean.quantity_kg}kg)")
        
        initial_qty = green_bean.quantity_kg
        roast_amount = 1.0
        
        # 2. Test Single Origin Roasting (Dry Run/Simulation or real execution depending on environment)
        # Note: Since this is a local session, we can attempt a real roasting if it's a dev DB
        print("\n--- Testing Single Origin Roasting ---")
        try:
            roasted_bean = service.create_single_origin_roasting(
                green_bean_id=green_bean.id,
                input_weight=roast_amount,
                output_weight=0.85, # 15% loss
                roast_profile=RoastProfile.LIGHT,
                notes="Refactor Verification Roast"
            )
            print(f"Success! Roasted Bean created/updated: {roasted_bean.name} (ID: {roasted_bean.id})")
            
            # 3. Verify Quantity Sync
            db.refresh(green_bean)
            print(f"Green Bean Qty after roast: {green_bean.quantity_kg}kg (Expected: {initial_qty - roast_amount})")
            
            if abs(green_bean.quantity_kg - (initial_qty - roast_amount)) < 0.001:
                print("✅ Quantity sync successful.")
            else:
                print("❌ Quantity sync failed!")
                
        except Exception as e:
            print(f"Roasting failed: {str(e)}")
            
        print("\nVerification Complete.")
        
    finally:
        db.close()

if __name__ == "__main__":
    verify_roasting()
