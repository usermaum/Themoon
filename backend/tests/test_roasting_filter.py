
import pytest
from datetime import date, timedelta
from app.models.roasting_log import RoastingLog
from app.models.bean import Bean, BeanType
from app.repositories.roasting_log_repository import RoastingLogRepository

def test_filter_roasting_logs(db_session):
    # Setup: Create Beans
    green_bean = Bean(name="Test Green", type=BeanType.GREEN_BEAN)
    blend_bean = Bean(name="Test Blend", type=BeanType.BLEND_BEAN)
    db_session.add(green_bean)
    db_session.add(blend_bean)
    db_session.commit()
    
    # Setup: Create Roasting Logs
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    log1 = RoastingLog(
        roast_date=today,
        target_bean_id=green_bean.id,
        output_weight_total=10.0,
        batch_no="BATCH-001"
    )
    log2 = RoastingLog(
        roast_date=yesterday,
        target_bean_id=blend_bean.id,
        output_weight_total=20.0,
        batch_no="BATCH-002"
    )
    db_session.add(log1)
    db_session.add(log2)
    db_session.commit()
    
    repo = RoastingLogRepository(db_session)
    
    # Test 1: No Filter
    results = repo.get_multi()
    assert len(results) >= 2
    
    # Test 2: Filter by Date (Today)
    results = repo.get_multi(filters={"start_date": today})
    # Should contain log1 (today), not log2 (yesterday)
    # Note: Logic depends on if previous data exists, so checking containment
    ids = [l.id for l in results]
    assert log1.id in ids
    assert log2.id not in ids
    
    # Test 3: Filter by Bean Type (GREEN_BEAN)
    results = repo.get_multi(filters={"bean_type": "GREEN_BEAN"})
    ids = [l.id for l in results]
    assert log1.id in ids
    assert log2.id not in ids
    
    # Test 4: Filter by Bean Type (BLEND_BEAN)
    results = repo.get_multi(filters={"bean_type": "BLEND_BEAN"})
    ids = [l.id for l in results]
    assert log1.id not in ids
    assert log2.id in ids
    
    # Test 5: Filter by Bean ID
    results = repo.get_multi(filters={"bean_id": green_bean.id})
    ids = [l.id for l in results]
    assert log1.id in ids
    assert log2.id not in ids

