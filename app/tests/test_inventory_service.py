"""
InventoryService 단위 테스트
원가계산기 고도화 - Phase 1: 재고 관리 시스템
"""

import pytest
from datetime import date
from app.services.inventory_service import InventoryService, InventoryType, TransactionType
from app.models.database import Bean, Inventory, Transaction, RoastingLog


class TestInventoryService:
    """InventoryService 테스트"""

    def test_get_inventory_raw_bean(self, db_session, sample_bean):
        """생두 재고 조회 테스트"""
        service = InventoryService(db_session)

        # 생두 재고 생성
        raw_inv = Inventory(
            bean_id=sample_bean.id,
            inventory_type=InventoryType.RAW_BEAN,
            quantity_kg=20.0
        )
        db_session.add(raw_inv)
        db_session.commit()

        # 조회
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)

        assert inventory is not None
        assert inventory.bean_id == sample_bean.id
        assert inventory.inventory_type == InventoryType.RAW_BEAN
        assert inventory.quantity_kg == 20.0

    def test_get_inventory_roasted_bean(self, db_session, sample_bean):
        """원두 재고 조회 테스트"""
        service = InventoryService(db_session)

        # 원두 재고 생성
        roasted_inv = Inventory(
            bean_id=sample_bean.id,
            inventory_type=InventoryType.ROASTED_BEAN,
            quantity_kg=15.5
        )
        db_session.add(roasted_inv)
        db_session.commit()

        # 조회
        inventory = service.get_inventory(sample_bean.id, InventoryType.ROASTED_BEAN)

        assert inventory is not None
        assert inventory.inventory_type == InventoryType.ROASTED_BEAN
        assert inventory.quantity_kg == 15.5

    def test_get_all_inventory(self, db_session, sample_bean):
        """전체 재고 조회 테스트"""
        service = InventoryService(db_session)

        # 생두/원두 재고 생성
        raw_inv = Inventory(
            bean_id=sample_bean.id,
            inventory_type=InventoryType.RAW_BEAN,
            quantity_kg=20.0
        )
        roasted_inv = Inventory(
            bean_id=sample_bean.id,
            inventory_type=InventoryType.ROASTED_BEAN,
            quantity_kg=10.0
        )
        db_session.add_all([raw_inv, roasted_inv])
        db_session.commit()

        # 조회
        all_inventory = service.get_all_inventory()

        assert len(all_inventory) > 0
        found = False
        for item in all_inventory:
            if item['bean_id'] == sample_bean.id:
                assert item['raw_bean_qty'] == 20.0
                assert item['roasted_bean_qty'] == 10.0
                assert item['total_qty'] == 30.0
                found = True
                break
        assert found, "sample_bean의 재고를 찾을 수 없습니다"

    def test_add_stock_purchase(self, db_session, sample_bean):
        """재고 추가 (입고) 테스트"""
        service = InventoryService(db_session)

        # 입고
        success, msg, transaction = service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=50.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.PURCHASE,
            price_per_kg=30000.0,
            notes="테스트 입고"
        )

        assert success is True
        assert "추가 완료" in msg
        assert transaction is not None
        assert transaction.quantity_kg == 50.0
        assert transaction.total_amount == 50.0 * 30000.0

        # 재고 확인
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert inventory.quantity_kg == 50.0

    def test_add_stock_multiple_times(self, db_session, sample_bean):
        """재고 여러 번 추가 테스트"""
        service = InventoryService(db_session)

        # 첫 번째 입고
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=20.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.PURCHASE
        )

        # 두 번째 입고
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=30.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.PURCHASE
        )

        # 재고 확인
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert inventory.quantity_kg == 50.0

    def test_reduce_stock_success(self, db_session, sample_bean):
        """재고 차감 (성공) 테스트"""
        service = InventoryService(db_session)

        # 먼저 재고 추가
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=50.0,
            inventory_type=InventoryType.RAW_BEAN
        )

        # 재고 차감
        success, msg, transaction = service.reduce_stock(
            bean_id=sample_bean.id,
            quantity_kg=20.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.SALES,
            notes="테스트 출고"
        )

        assert success is True
        assert "차감 완료" in msg
        assert transaction is not None
        assert transaction.quantity_kg == -20.0  # 차감은 음수

        # 재고 확인
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert inventory.quantity_kg == 30.0

    def test_reduce_stock_insufficient(self, db_session, sample_bean):
        """재고 부족 시 차감 실패 테스트"""
        service = InventoryService(db_session)

        # 재고 10kg만 추가
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=10.0,
            inventory_type=InventoryType.RAW_BEAN
        )

        # 20kg 차감 시도 (실패해야 함)
        success, msg, transaction = service.reduce_stock(
            bean_id=sample_bean.id,
            quantity_kg=20.0,
            inventory_type=InventoryType.RAW_BEAN,
            allow_negative=False
        )

        assert success is False
        assert "재고 부족" in msg
        assert transaction is None

        # 재고 확인 (변경 없어야 함)
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert inventory.quantity_kg == 10.0

    def test_process_roasting_transaction(self, db_session, sample_bean):
        """로스팅 재고 처리 테스트"""
        service = InventoryService(db_session)

        # 생두 재고 추가
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=50.0,
            inventory_type=InventoryType.RAW_BEAN
        )

        # 로스팅 기록 생성
        roasting_log = RoastingLog(
            bean_id=sample_bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=10.0,
            loss_rate_percent=16.67,
            roasting_date=date.today()
        )
        db_session.add(roasting_log)
        db_session.commit()

        # 로스팅 재고 처리
        success, msg = service.process_roasting_transaction(
            bean_id=sample_bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=10.0,
            roasting_log_id=roasting_log.id
        )

        assert success is True
        assert "완료" in msg

        # 생두 재고 확인 (50 - 12 = 38)
        raw_inv = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert raw_inv.quantity_kg == 38.0

        # 원두 재고 확인 (0 + 10 = 10)
        roasted_inv = service.get_inventory(sample_bean.id, InventoryType.ROASTED_BEAN)
        assert roasted_inv.quantity_kg == 10.0

    def test_process_roasting_transaction_insufficient_raw(self, db_session, sample_bean):
        """생두 부족 시 로스팅 실패 테스트"""
        service = InventoryService(db_session)

        # 생두 재고 5kg만 추가
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=5.0,
            inventory_type=InventoryType.RAW_BEAN
        )

        # 로스팅 기록 생성
        roasting_log = RoastingLog(
            bean_id=sample_bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=10.0,
            loss_rate_percent=16.67,
            roasting_date=date.today()
        )
        db_session.add(roasting_log)
        db_session.commit()

        # 로스팅 재고 처리 (실패해야 함)
        success, msg = service.process_roasting_transaction(
            bean_id=sample_bean.id,
            raw_weight_kg=12.0,
            roasted_weight_kg=10.0,
            roasting_log_id=roasting_log.id
        )

        assert success is False
        assert "부족" in msg

        # 재고 확인 (변경 없어야 함)
        raw_inv = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert raw_inv.quantity_kg == 5.0

    def test_adjust_inventory(self, db_session, sample_bean):
        """재고 조정 테스트"""
        service = InventoryService(db_session)

        # 재고 추가
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=50.0,
            inventory_type=InventoryType.RAW_BEAN
        )

        # 재고 조정 (50 → 45)
        success, msg = service.adjust_inventory(
            bean_id=sample_bean.id,
            new_quantity_kg=45.0,
            inventory_type=InventoryType.RAW_BEAN,
            reason="실사 후 조정"
        )

        assert success is True
        assert "조정 완료" in msg

        # 재고 확인
        inventory = service.get_inventory(sample_bean.id, InventoryType.RAW_BEAN)
        assert inventory.quantity_kg == 45.0

    def test_get_low_stock_items(self, db_session, sample_bean):
        """저재고 항목 조회 테스트"""
        service = InventoryService(db_session)

        # 재고 생성 (최소 재고보다 적게)
        raw_inv = Inventory(
            bean_id=sample_bean.id,
            inventory_type=InventoryType.RAW_BEAN,
            quantity_kg=3.0,
            min_quantity_kg=5.0
        )
        db_session.add(raw_inv)
        db_session.commit()

        # 저재고 조회
        low_stock_items = service.get_low_stock_items()

        assert len(low_stock_items) > 0
        found = False
        for item in low_stock_items:
            if item['inventory'].bean_id == sample_bean.id:
                assert item['current_qty'] == 3.0
                assert item['min_qty'] == 5.0
                assert item['shortage'] == 2.0
                found = True
                break
        assert found, "저재고 항목을 찾을 수 없습니다"

    def test_get_transactions(self, db_session, sample_bean):
        """거래 기록 조회 테스트"""
        service = InventoryService(db_session)

        # 여러 거래 생성
        service.add_stock(
            bean_id=sample_bean.id,
            quantity_kg=50.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.PURCHASE
        )

        service.reduce_stock(
            bean_id=sample_bean.id,
            quantity_kg=10.0,
            inventory_type=InventoryType.RAW_BEAN,
            transaction_type=TransactionType.SALES
        )

        # 거래 기록 조회
        transactions = service.get_transactions(bean_id=sample_bean.id, limit=10)

        assert len(transactions) == 2
        assert transactions[0].transaction_type in [TransactionType.PURCHASE, TransactionType.SALES]


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def sample_bean(db_session):
    """테스트용 원두 생성"""
    bean = Bean(
        no=99,
        name="테스트 원두",
        country_name="테스트 국가",
        roast_level="MEDIUM",
        price_per_kg=30000.0,
        status="active"
    )
    db_session.add(bean)
    db_session.commit()
    db_session.refresh(bean)
    return bean
