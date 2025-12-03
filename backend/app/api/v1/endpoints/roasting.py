from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.roasting import RoastingCreate, RoastingResponse
from app.models.bean import Bean
from app.models.inventory_log import InventoryLog

router = APIRouter()

@router.post("/", response_model=RoastingResponse)
def create_roasting(roasting: RoastingCreate, db: Session = Depends(get_db)):
    # 1. Validate Green Bean
    green_bean = db.query(Bean).filter(Bean.id == roasting.green_bean_id).first()
    if not green_bean:
        raise HTTPException(status_code=404, detail="Green bean not found")
    
    if green_bean.quantity_kg < roasting.input_amount:
        raise HTTPException(status_code=400, detail="Insufficient green bean stock")

    # 2. Get or Create Roasted Bean
    roasted_bean = None
    if roasting.roasted_bean_id:
        roasted_bean = db.query(Bean).filter(Bean.id == roasting.roasted_bean_id).first()
        if not roasted_bean:
            raise HTTPException(status_code=404, detail="Roasted bean not found")
    elif roasting.new_bean_name:
        # Create new roasted bean inheriting from green bean
        roasted_bean = Bean(
            name=roasting.new_bean_name,
            type="ROASTED_SINGLE",
            origin=green_bean.origin,
            origin_code=green_bean.origin_code,
            variety=green_bean.variety,
            processing_method=green_bean.processing_method,
            parent_bean_id=green_bean.id,
            roast_level=roasting.roast_level,
            quantity_kg=0.0,
            avg_cost_price=0.0
        )
        db.add(roasted_bean)
        db.flush() # Get ID
    else:
        raise HTTPException(status_code=400, detail="Either roasted_bean_id or new_bean_name must be provided")

    # 3. Calculate Cost
    # Cost of this batch = (Green Bean Avg Cost * Input Amount) / Output Amount
    # Note: If Green Bean Avg Cost is 0, we might want to warn or use purchase price? 
    # For now, use avg_cost_price.
    batch_cost_price = 0
    if green_bean.avg_cost_price and roasting.output_amount > 0:
        batch_cost_price = (green_bean.avg_cost_price * roasting.input_amount) / roasting.output_amount

    # 4. Update Inventory & Cost (Weighted Average for Roasted Bean)
    # New Avg Cost = ((Current Qty * Current Avg) + (New Qty * New Cost)) / (Current Qty + New Qty)
    current_total_value = roasted_bean.quantity_kg * roasted_bean.avg_cost_price
    new_total_value = current_total_value + (roasting.output_amount * batch_cost_price)
    new_total_qty = roasted_bean.quantity_kg + roasting.output_amount
    
    if new_total_qty > 0:
        roasted_bean.avg_cost_price = new_total_value / new_total_qty
    
    roasted_bean.quantity_kg = new_total_qty
    
    # Update Green Bean Stock
    green_bean.quantity_kg -= roasting.input_amount

    # 5. Create Inventory Logs
    # Log 1: Green Bean Usage (ROASTING_IN)
    log_in = InventoryLog(
        bean_id=green_bean.id,
        transaction_type="ROASTING_IN",
        quantity_change=-roasting.input_amount,
        current_quantity=green_bean.quantity_kg,
        amount_kg=roasting.input_amount,
        cost_price=green_bean.avg_cost_price, # Cost at the time of usage
        reason=f"Roasting to {roasted_bean.name}"
    )
    db.add(log_in)

    # Log 2: Roasted Bean Production (ROASTING_OUT)
    log_out = InventoryLog(
        bean_id=roasted_bean.id,
        transaction_type="ROASTING_OUT",
        quantity_change=roasting.output_amount,
        current_quantity=roasted_bean.quantity_kg,
        amount_kg=roasting.output_amount,
        cost_price=batch_cost_price,
        reason=f"Roasting from {green_bean.name}"
    )
    db.add(log_out)

    db.commit()

    loss_rate = 0
    if roasting.input_amount > 0:
        loss_rate = (roasting.input_amount - roasting.output_amount) / roasting.input_amount * 100

    return RoastingResponse(
        transaction_id_in=log_in.id,
        transaction_id_out=log_out.id,
        loss_rate=loss_rate,
        cost_price=batch_cost_price
    )
