import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.blend import Blend
from app.services import roasting_service
from sqlalchemy.orm import Session

def print_bean_stock(db: Session, bean_id: int, label: str):
    bean = db.query(Bean).filter(Bean.id == bean_id).first()
    if bean:
        print(f"[{label}] ID: {bean.id}, Name: {bean.name}, Type: {bean.type}, Qty: {bean.quantity_kg}kg, SKU: {bean.sku}")
    else:
        print(f"[{label}] Bean ID {bean_id} not found.")

def test_single_origin_roasting():
    db = SessionLocal()
    try:
        print("\n--- Testing Single Origin Roasting ---")
        # 1. 예가체프(ID 1 가정) 조회
        bean = db.query(Bean).filter(Bean.variety.like("%Yirgacheffe%"), Bean.type == BeanType.GREEN_BEAN).first()
        if not bean:
            print("Yirgacheffe green bean not found. Skipping.")
            return

        print_bean_stock(db, bean.id, "Before Roasting (Green)")
        
        # 2. 로스팅 실행 (5kg 투입 -> 4.2kg 생산, Light Roast)
        input_w = 5.0
        output_w = 4.2
        print(f"Roasting: Input {input_w}kg -> Output {output_w}kg (Light)")
        
        roasted = roasting_service.create_single_origin_roasting(
            db, bean.id, input_w, output_w, RoastProfile.LIGHT, "Test Roasting"
        )
        
        # 3. 결과 확인
        print_bean_stock(db, bean.id, "After Roasting (Green)")
        print_bean_stock(db, roasted.id, "Result (Roasted)")

        # 검증
        if roasted.quantity_kg >= output_w:
             print("SUCCESS: Single Origin Roasting verified.")
        else:
             print("FAIL: Roasted bean quantity mismatch.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

def test_blend_roasting():
    db = SessionLocal()
    try:
        print("\n--- Testing Blend Roasting ---")
        # 1. 블렌드 조회 (없으면 생성)
        blend_name = "Test Blend Full Moon"
        blend = db.query(Blend).filter(Blend.name == blend_name).first()
        
        # 재료 생두 확보
        bean1 = db.query(Bean).filter(Bean.variety.like("%Yirgacheffe%"), Bean.type == BeanType.GREEN_BEAN).first()
        bean2 = db.query(Bean).filter(Bean.variety.like("%Antigua%"), Bean.type == BeanType.GREEN_BEAN).first() # 안티구아

        if not bean1 or not bean2:
             print("Required green beans for blend test not found.")
             return

        if not blend:
            print("Creating Test Blend...")
            # 50:50 비율
            recipe = [
                {"bean_id": bean1.id, "ratio": 0.5},
                {"bean_id": bean2.id, "ratio": 0.5}
            ]
            blend = Blend(name=blend_name, description="Test Blend", recipe=recipe)
            db.add(blend)
            db.commit()
            db.refresh(blend)
        
        print_bean_stock(db, bean1.id, f"Before Blend (Green 1 - {bean1.name})")
        print_bean_stock(db, bean2.id, f"Before Blend (Green 2 - {bean2.name})")

        # 2. 로스팅 실행 (목표 생산량 10kg)
        # 예상 소모량: 
        # Bean1: 5kg / (1-loss) ... loss가 0.15라면 약 5.88kg
        # Bean2: 5kg / (1-loss) ... 약 5.88kg
        output_w = 10.0
        print(f"Roasting Blend: Output {output_w}kg")
        
        roasted_blend = roasting_service.create_blend_roasting(
            db, blend.id, output_w, notes="Test Blend Roasting"
        )

        # 3. 결과 확인
        print_bean_stock(db, bean1.id, f"After Blend (Green 1)")
        print_bean_stock(db, bean2.id, f"After Blend (Green 2)")
        print_bean_stock(db, roasted_blend.id, "Result (Roasted Blend)")

        if roasted_blend.quantity_kg >= output_w:
            print("SUCCESS: Blend Roasting verified.")
        else:
            print("FAIL: Blend roasted quantity mismatch.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_single_origin_roasting()
    test_blend_roasting()
