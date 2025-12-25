import sys
import os
from unittest.mock import MagicMock

# Mock dependencies before importing app modules
sys.modules['psutil'] = MagicMock()
sys.modules['magic'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()

# Override DATABASE_URL for Windows environment
os.environ['DATABASE_URL'] = 'sqlite:///D:/Ai/WslProject/Themoon/themoon.db'

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal
from app.api.v1.roasting import get_roasting_service
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.roasting_log import RoastingLog
from app.models.inventory_log import InventoryLog

def verify_enhancement():
    db = SessionLocal()
    try:
        service = get_roasting_service(db)
        
        # 1. Find a green bean
        green_bean = db.query(Bean).filter(Bean.type == BeanType.GREEN_BEAN, Bean.quantity_kg > 5.0).first()
        if not green_bean:
            print("No green bean for test.")
            return

        print(f"Test Start: Roasting {green_bean.name} (ID: {green_bean.id})")
        
        # 2. Roast!
        input_w = 2.0
        output_w = 1.7
        roasted_bean = service.create_single_origin_roasting(
            green_bean_id=green_bean.id,
            input_weight=input_w,
            output_weight=output_w,
            roast_profile=RoastProfile.DARK,
            notes="Log Enhancement Verify"
        )
        
        # 3. Verify Batch Log
        latest_log = db.query(RoastingLog).order_by(RoastingLog.id.desc()).first()
        if not latest_log:
            print("[FAIL] RoastingLog not created!")
            return
            
        print(f"[OK] RoastingLog Created: {latest_log.batch_no} (ID: {latest_log.id})")
        print(f"   - Target Bean: {roasted_bean.name} (ID: {latest_log.target_bean_id})")
        print(f"   - Input: {latest_log.input_weight_total}kg, Output: {latest_log.output_weight_total}kg")
        print(f"   - Loss Rate: {latest_log.loss_rate:.2f}%")
        
        # 4. Verify InventoryLog Link
        linked_inv_logs = db.query(InventoryLog).filter(InventoryLog.roasting_log_id == latest_log.id).all()
        print(f"[OK] Found {len(linked_inv_logs)} inventory logs linked to batch.")
        
        for ilog in linked_inv_logs:
            print(f"   - InvLog ID: {ilog.id}, Type: {ilog.change_type}, Amount: {ilog.change_amount}")
            
        if len(linked_inv_logs) >= 2:
            print("[OK] Batch linking successful.")
        else:
            print("[FAIL] Batch linking failed (insufficient logs).")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_enhancement()
