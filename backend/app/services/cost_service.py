from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.bean import Bean
from app.models.inbound_item import InboundItem
from app.models.inventory_log import InventoryLog, InventoryChangeType
from fastapi import HTTPException

def calculate_fifo_cost(db: Session, bean_id: int, quantity_kg: float) -> float:
    """
    Calculate the estimated cost for a specific quantity of beans using FIFO logic.
    
    Args:
        db: Database session
        bean_id: The ID of the bean (Green Bean)
        quantity_kg: The amount of bean to be used
        
    Returns:
        float: The weighted average cost per kg for the requested quantity.
    """
    if quantity_kg <= 0:
        return 0.0

    # 1. Fetch Inbound History (sorted by date)
    inbound_items = db.query(InboundItem).join(InboundItem.inbound_document).filter(
        InboundItem.bean_name.has(Bean.name) | (InboundItem.bean_name == db.query(Bean.name).filter(Bean.id == bean_id).scalar_subquery())
    ).order_by(InboundItem.created_at).all()
    
    # Note on InboundItem linking: 
    # Currently InboundItem stores 'bean_name' as string. 
    # We need to robustly match it to the Bean table. 
    # For this implementation, we try to match by name or context. 
    # A better schema would have InboundItem.bean_id, but per current schema it's loose.
    # Let's verify if we can match by name.
    
    target_bean = db.query(Bean).filter(Bean.id == bean_id).first()
    if not target_bean:
        raise HTTPException(status_code=404, detail="Bean not found")

    # Re-fetch strictly filtering by name matching
    # In a real scenario, we should ensure InboundItem has a linked bean_id or consistent logic.
    # Here we filter in python for safety if strict join fails.
    relevant_inbounds = []
    for item in db.query(InboundItem).order_by(InboundItem.created_at).all():
        # Loose matching logic: check if InboundItem name is part of Bean name or vice versa
        # This is temporary until InboundItem has strict bean_id
        if item.bean_name and (item.bean_name in target_bean.name or target_bean.name in item.bean_name):
            relevant_inbounds.append(item)
            
    if not relevant_inbounds:
        # Fallback to current average price if no inbound history
        return target_bean.avg_price

    # 2. Calculate Total Usage so far
    usage_logs = db.query(InventoryLog).filter(
        InventoryLog.bean_id == bean_id,
        InventoryLog.change_amount < 0  # Usage is negative
    ).all()
    
    total_used_amount = sum(abs(log.change_amount) for log in usage_logs)
    
    # 3. Virtual FIFO matching
    # Skip inbound items that are already depleted
    remaining_inbounds = []
    accumulated_qty = 0.0
    
    for item in relevant_inbounds:
        qty = item.quantity or 0
        if accumulated_qty + qty > total_used_amount:
            # This batch has some remaining stock
            remaining_from_this_batch = (accumulated_qty + qty) - total_used_amount
            # If total_used_amount ate up previous batches, this batch only has 'remaining' part effectively avail
            # But wait, logic:
            # We consumed total_used_amount from the start.
            # So effectively, we effectively skipped 'total_used_amount' of mass from the sorted list.
            
            # The available stock starts from this item with 'remaining_from_this_batch'
            # and subsequent items with full quantity.
            
            # If this is the first item crossing the threshold
            if accumulated_qty <= total_used_amount:
               # This is the "current" batch being used
               item_copy = item
               # We don't modify DB object, just carry value
               remaining_inbounds.append({
                   "price": item.unit_price,
                   "available_qty": remaining_from_this_batch
               })
            else:
               # Fully available
               remaining_inbounds.append({
                   "price": item.unit_price,
                   "available_qty": qty
               })
        else:
            # Fully used
            pass
        accumulated_qty += qty

    # 4. Calculate cost for requested quantity
    cost_accumulator = 0.0
    qty_needed = quantity_kg
    
    for batch in remaining_inbounds:
        if qty_needed <= 0:
            break
            
        take_qty = min(qty_needed, batch["available_qty"])
        unit_price = batch["price"] or target_bean.avg_price # fallback
        
        cost_accumulator += take_qty * unit_price
        qty_needed -= take_qty
        
    if qty_needed > 0:
        # Shortage of inbound history cover? Use avg_price for the rest
        cost_accumulator += qty_needed * target_bean.avg_price
        
    return cost_accumulator / quantity_kg
