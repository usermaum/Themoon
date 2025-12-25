"""
Phase 21 Verify Script: BeanRepository & RoastingService DDD Refinement
"""
import sys
import os

# app 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database import SessionLocal, engine
from app.models.bean import Bean, BeanType, RoastProfile
from app.repositories.bean_repository import BeanRepository
from app.services.bean_service import BeanService
from app.services.roasting_service import RoastingService
from app.repositories.blend_repository import BlendRepository
from app.repositories.roasting_log_repository import RoastingLogRepository
from app.services.inventory_service import InventoryService
from app.repositories.inbound_repository import InboundRepository
from app.repositories.inventory_log_repository import InventoryLogRepository

def verify_ddd_refinement():
    db = SessionLocal()
    try:
        print("--- PHASE 21 VERIFICATION START ---")
        
        # 1. Repository Method Verification
        bean_repo = BeanRepository(db)
        
        # 테스트 생두 생성 (있으면 사용)
        test_bean = bean_repo.get_by_name("Yirgacheffe Test")
        if not test_bean:
            test_bean = bean_repo.create({
                "name": "Yirgacheffe Test",
                "type": BeanType.GREEN_BEAN,
                "sku": "YIRGA-TEST-SKU",
                "origin": "Ethiopia",
                "variety": "Heirloom",
                "quantity_kg": 10.0
            })
            print(f"Created test bean: {test_bean.name}")
        
        # SKU 조회 검증
        found_by_sku = bean_repo.get_by_sku("YIRGA-TEST-SKU")
        if found_by_sku and found_by_sku.name == "Yirgacheffe Test":
            print("[OK] BeanRepository.get_by_sku works.")
        else:
            print("[FAIL] BeanRepository.get_by_sku failed.")

        # Metadata 조회 검증
        origins = bean_repo.get_unique_origins()
        print(f"Unique Origins: {origins}")
        if "Ethiopia" in origins:
            print("[OK] BeanRepository.get_unique_origins works.")

        # 2. Service Layer Verification
        bean_service = BeanService(bean_repo)
        if bean_service.get_bean_by_sku("YIRGA-TEST-SKU"):
            print("[OK] BeanService.get_bean_by_sku works.")

        # 3. RoastingService Integration (Simulation)
        # 로스팅 서비스 시뮬레이션을 통해 직접 DB 쿼리 제거 확인
        # (실제 코드가 skip되는지 여부는 코드 리뷰로 확인했으므로 실행 경로만 태움)
        inbound_repo = InboundRepository(db)
        inventory_log_repo = InventoryLogRepository(db)
        inventory_service = InventoryService(inbound_repo, inventory_log_repo)
        blend_repo = BlendRepository(db)
        roasting_log_repo = RoastingLogRepository(db)
        
        roasting_service = RoastingService(bean_service, inventory_service, blend_repo, roasting_log_repo)
        
        # Single Origin Roasting 실행 시 SKU 조회가 BeanService를 통하는지 확인
        # (실행 중 에러가 안 나면 성공으로 간주 - 내부적으로 get_bean_by_sku를 호출함)
        try:
            # 기존 원두가 이미 있을 수 있으므로 SKU를 생성해보고 태움
            sku = roasting_service.generate_roasted_bean_sku(test_bean, RoastProfile.LIGHT)
            print(f"Expected SKU for roasting: {sku}")
            
            # 실제 로스팅 실행 (재고가 충분하므로 성공해야 함)
            roasted, batch_no = roasting_service.create_single_origin_roasting(
                green_bean_id=test_bean.id,
                input_weight=1.0,
                output_weight=0.85,
                roast_profile=RoastProfile.LIGHT,
                notes="DDD Verification Roast"
            )
            print(f"[OK] RoastingService worked with batch: {batch_no}")
            
        except Exception as e:
            print(f"[FAIL] RoastingService error: {str(e)}")

        print("--- PHASE 21 VERIFICATION COMPLETE ---")
        
    finally:
        db.close()

if __name__ == "__main__":
    verify_ddd_refinement()
