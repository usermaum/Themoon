import pytest
from sqlalchemy.orm import Session
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.inventory_log import InventoryLog
from app.models.roasting_log import RoastingLog
from app.models.inbound_document import InboundDocument
from app.schemas.inventory_log import InventoryLogCreate
from app.services.inventory_log_service import inventory_log_service

def test_inventory_log_lifecycle(db_session: Session):
    # 1. Create a test bean
    bean = Bean(
        name="Test Bean",
        type=BeanType.GREEN_BEAN,
        quantity_kg=10.0,
        origin="Test Origin"
    )
    db_session.add(bean)
    db_session.commit()
    db_session.refresh(bean)
    
    initial_qty = bean.quantity_kg
    
    # 2. Create Inventory Log (IN)
    log_in = InventoryLogCreate(
        bean_id=bean.id,
        change_type="PURCHASE",
        change_amount=5.0,
        notes="Initial Stock"
    )
    
    created_log = inventory_log_service.create_log(db_session, log_in)
    
    # Verify
    assert created_log.id is not None
    assert created_log.change_amount == 5.0
    assert created_log.current_quantity == 15.0
    
    db_session.refresh(bean)
    assert bean.quantity_kg == 15.0
    
    # 3. Update Log (Correction)
    # Changed from 5.0 to 3.0 (So quantity should become 10 + 3 = 13)
    updated_log = inventory_log_service.update_log(db_session, created_log.id, 3.0, "Updated Note")
    
    # Verify
    assert updated_log.change_amount == 3.0
    assert updated_log.current_quantity == 13.0
    
    db_session.refresh(bean)
    assert bean.quantity_kg == 13.0
    
    # 4. Get Logs
    logs = inventory_log_service.get_logs(db_session, bean_id=bean.id)
    assert len(logs) == 1
    assert logs[0].id == created_log.id
    
    count = inventory_log_service.get_logs_count(db_session, bean_id=bean.id)
    assert count == 1
    
    # 5. Delete Log
    # Quantity should revert to 10.0 (13.0 - 3.0)
    inventory_log_service.delete_log(db_session, created_log.id)
    
    db_session.refresh(bean)
    assert bean.quantity_kg == 10.0
    
    # Verify log is gone
    logs = inventory_log_service.get_logs(db_session, bean_id=bean.id)
    assert len(logs) == 0
