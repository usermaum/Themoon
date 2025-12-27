import pytest
from unittest.mock import Mock, MagicMock
from app.services.roasting_service import RoastingService
from app.models.bean import RoastProfile
from app.models.inventory_log import InventoryChangeType

@pytest.fixture
def mock_dependencies():
    return {
        "bean_service": Mock(),
        "inventory_service": Mock(),
        "blend_repo": Mock(),
        "roasting_log_repo": Mock(),
    }

@pytest.fixture
def roasting_service(mock_dependencies):
    return RoastingService(
        bean_service=mock_dependencies["bean_service"],
        inventory_service=mock_dependencies["inventory_service"],
        blend_repo=mock_dependencies["blend_repo"],
        roasting_log_repo=mock_dependencies["roasting_log_repo"],
    )

def test_generate_batch_no_new(roasting_service, mock_dependencies):
    mock_dependencies["roasting_log_repo"].get_latest_batch_no.return_value = None
    batch_no = roasting_service.generate_batch_no()
    assert batch_no.startswith("R")
    assert batch_no.endswith("-001")

def test_generate_roasted_bean_sku(roasting_service):
    green_bean = Mock()
    green_bean.name = "KenyaAA"
    sku = roasting_service.generate_roasted_bean_sku(green_bean, RoastProfile.LIGHT)
    assert sku == "KenyaAA-신콩"

def test_single_origin_roasting_flow(roasting_service, mock_dependencies):
    # Setup
    green_bean = Mock()
    green_bean.id = 1
    green_bean.name = "Ethiopia"
    green_bean.quantity_kg = 100.0
    green_bean.origin = "Ethiopia"
    
    mock_dependencies["bean_service"].get_bean.return_value = green_bean
    mock_dependencies["bean_service"].get_bean.return_value = green_bean
    mock_dependencies["inventory_service"].calculate_fifo_cost.return_value = (10000, 50000)
    mock_dependencies["roasting_log_repo"].get_latest_batch_no.return_value = None
    
    roasted_bean_mock = Mock()
    roasted_bean_mock.id = 10
    roasted_bean_mock.quantity_kg = 0 # New bean
    mock_dependencies["bean_service"].repository.create.return_value = roasted_bean_mock
    mock_dependencies["bean_service"].get_bean_by_sku.return_value = None # Not exists yet
    
    log_mock = Mock()
    log_mock.id = 999
    mock_dependencies["roasting_log_repo"].create.return_value = log_mock

    # Execute
    roasting_service.create_single_origin_roasting(
        green_bean_id=1,
        input_weight=5.0,
        output_weight=4.2,
        roast_profile=RoastProfile.MEDIUM,
        roasting_time=600,
        ambient_temp=25.5,
        humidity=45.0,
        notes="Test Roast"
    )
    
    # Verify
    mock_dependencies["inventory_service"].deduct_inventory.assert_called_with(1, 5.0)
    mock_dependencies["bean_service"].update_bean_quantity.assert_any_call(1, -5.0)
    
    # Check Roasting Log creation
    mock_dependencies["roasting_log_repo"].create.assert_called()
    # Check Roasting Log creation
    # Check Roasting Log creation
    mock_dependencies["roasting_log_repo"].create.assert_called()
    call_args = mock_dependencies["roasting_log_repo"].create.call_args[0][0]
    assert call_args["roast_profile"] == "MEDIUM"
    assert call_args["roasting_time"] == 600
    assert call_args["ambient_temp"] == 25.5
    assert call_args["humidity"] == 45.0
    
    # Check Output Processing
    mock_dependencies["bean_service"].repository.create.assert_called() # New roasted bean
    mock_dependencies["bean_service"].update_bean_quantity.assert_any_call(10, 4.2)
