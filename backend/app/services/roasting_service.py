from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.bean import Bean, BeanType
from app.models.inventory_log import InventoryLog, TransactionType
from app.models.roasting_log import RoastingLog
from app.schemas.roasting import RoastingCreate, RoastingResponse
from app.services import bean_service

def process_roasting(db: Session, roasting_data: RoastingCreate) -> RoastingResponse:
    # 1. Validate Green Bean
    green_bean = bean_service.get_bean(db, roasting_data.green_bean_id)
    if not green_bean:
        raise HTTPException(status_code=404, detail="Green bean not found")
    if green_bean.type != BeanType.GREEN_BEAN:
        raise HTTPException(status_code=400, detail="Selected bean is not a green bean")
    
    # 2. Check Stock
    if green_bean.quantity_kg < roasting_data.input_amount:
        raise HTTPException(status_code=400, detail=f"Insufficient green bean stock. Current: {green_bean.quantity_kg}kg")
    
    # 3. Determine Output Bean (Roasted Bean)
    roasted_bean = None
    if roasting_data.roasted_bean_id:
        roasted_bean = bean_service.get_bean(db, roasting_data.roasted_bean_id)
        if not roasted_bean:
            raise HTTPException(status_code=404, detail="Target roasted bean not found")
    elif roasting_data.new_bean_name:
        # Create new roasted bean derived from green bean
        from app.schemas.bean import BeanCreate
        # Cost Calculation Init (will be updated later) - Use Green Bean Cost for now
        
        new_bean_data = BeanCreate(
            name=roasting_data.new_bean_name,
            type=BeanType.ROASTED_BEAN,
            roast_profile=roasting_data.roast_profile,
            origin=green_bean.origin,
            variety=green_bean.variety,
            processing_method=green_bean.processing_method,
            parent_bean_id=green_bean.id,
            cost_price=0.0, # Placeholder
            quantity_kg=0.0,
            notes=roasting_data.note
        )
        roasted_bean = bean_service.create_bean(db, new_bean_data)
    else:
         raise HTTPException(status_code=400, detail="Must provide either roasted_bean_id or new_bean_name")

    # 4. Perform Transactions
    
    # 4.1. Consume Green Bean (ROASTING_IN or OUT with reason)
    # Using 'OUT' for consistency with current TransactionType, or add 'ROASTING_IN' if allowed.
    # Current InventoryLog schema uses String for transaction_type.
    # We will use "ROASTING_IN" to be explicit as per plan.
    
    # Calculate Cost Per Kg
    # Green Bean Value = Input Amount * Green Bean Avg Cost
    # We assume 'cost_price' on Green Bean is the Avg Cost.
    # If purchase_price_per_kg exists, use that or cost_price. 
    green_cost_unit = green_bean.cost_price if (green_bean.cost_price and green_bean.cost_price > 0) else (green_bean.purchase_price_per_kg or 0)
    total_input_cost = roasting_data.input_amount * green_cost_unit
    
    # Decrement Green
    green_bean.quantity_kg -= roasting_data.input_amount
    db.add(InventoryLog(
        bean_id=green_bean.id,
        transaction_type="ROASTING_IN", # Input to roasting process (Consumption)
        quantity_change=-roasting_data.input_amount,
        current_quantity=green_bean.quantity_kg,
        reason=f"Roasting to {roasted_bean.name}"
    ))
    
    # 4.2. Produre Roasted Bean
    
    # Calculate New Cost Price
    # Cost per kg of roasted = Total Input Cost / Output Amount
    new_cost_per_kg = 0
    if roasting_data.output_amount > 0:
        new_cost_per_kg = total_input_cost / roasting_data.output_amount
    
    # Update Roasted Bean Cost (Weighted Average or just Update? Plan implies recalculation)
    # If it's a new batch, the cost is strictly this batch.
    # If blending into existing, we might need weighted average.
    # For now, let's update the cost price to the latest batch cost or weighted average.
    # Weighted Average: (OldQty * OldCost + NewQty * NewCost) / (OldQty + NewQty)
    
    current_val = roasted_bean.quantity_kg * (roasted_bean.cost_price or 0)
    new_val = roasting_data.output_amount * new_cost_per_kg
    total_qty = roasted_bean.quantity_kg + roasting_data.output_amount
    
    avg_cost = 0
    if total_qty > 0:
        avg_cost = (current_val + new_val) / total_qty
    
    roasted_bean.cost_price = avg_cost
    roasted_bean.quantity_kg += roasting_data.output_amount
    
    db.add(InventoryLog(
        bean_id=roasted_bean.id,
        transaction_type="ROASTING_OUT", # Output from roasting process (Production)
        quantity_change=roasting_data.output_amount,
        current_quantity=roasted_bean.quantity_kg,
        reason=f"Roasting from {green_bean.name}"
    ))
    
    # 5. Create Roasting Log
    loss_rate = 0
    if roasting_data.input_amount > 0:
        loss_rate = ((roasting_data.input_amount - roasting_data.output_amount) / roasting_data.input_amount) * 100
        
    roasting_log = RoastingLog(
        green_bean_id=green_bean.id,
        roasted_bean_id=roasted_bean.id,
        input_quantity=roasting_data.input_amount,
        output_quantity=roasting_data.output_amount,
        loss_rate=loss_rate,
        note=roasting_data.note
    )
    db.add(roasting_log)
    
    db.commit()
    db.refresh(roasting_log)
    
    return RoastingResponse(
        roasting_log_id=roasting_log.id,
        loss_rate=loss_rate,
        cost_price=new_cost_per_kg,
        roasted_bean_id=roasted_bean.id
    )
