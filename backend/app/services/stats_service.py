import re
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.inbound_document import InboundDocument
from app.models.inbound_item import InboundItem
from app.models.bean import Bean


def get_supplier_stats(
    db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
):
    """
    Get aggregated statistics by supplier.
    Returns total purchase amount and count for each supplier.

    Args:
        db: Database session
        start_date: Start date for filtering (inclusive)
        end_date: End date for filtering (inclusive)
    """
    # Join InboundItem -> InboundDocument -> Supplier (via name or relationship)
    # Since relationships might be loose, we'll group by InboundDocument.supplier_name

    query = db.query(
        InboundDocument.supplier_name,
        func.sum(InboundDocument.total_amount).label("total_amount"),
        func.count(InboundDocument.id).label("doc_count"),
    )

    # Apply date filters if provided
    if start_date:
        query = query.filter(InboundDocument.created_at >= start_date)
    if end_date:
        query = query.filter(InboundDocument.created_at <= end_date)

    results = query.group_by(InboundDocument.supplier_name).order_by(desc("total_amount")).all()

    # Python-side aggregation for normalization
    aggregated = {}

    for r in results:
        raw_name = r.supplier_name or "Unknown"

        # 1. Remove text in parenthesis (e.g. (주), (Inc))
        norm_name = re.sub(r"\([^)]*\)", "", raw_name)
        # 2. Remove dangling (주 if OCR failed to close it
        norm_name = norm_name.replace("(주", "").replace("주)", "")
        # 3. Remove 주식회사
        norm_name = norm_name.replace("주식회사", "")

        # 4. Strip whitespace
        norm_name = norm_name.strip()

        # 5. Fix common spelling variations (GSC)
        if "지에스씨" in norm_name:
            norm_name = norm_name.replace("인터네셔날", "인터내셔날")

        if norm_name == "":
            norm_name = "Unknown"

        if norm_name not in aggregated:
            aggregated[norm_name] = {"name": norm_name, "total_amount": 0.0, "count": 0}

        aggregated[norm_name]["total_amount"] += r.total_amount or 0
        aggregated[norm_name]["count"] += r.doc_count

    # Convert to list and sort descendling by amount
    final_results = list(aggregated.values())
    final_results.sort(key=lambda x: x["total_amount"], reverse=True)

    return final_results


def get_monthly_buying_stats(db: Session, months: int = 12):
    """
    Get monthly buying trends for the last N months.
    """
    start_date = datetime.now() - timedelta(days=30 * months)

    results = (
        db.query(
            func.strftime("%Y-%m", InboundDocument.created_at).label("month"),
            func.sum(InboundDocument.total_amount).label("total_amount"),
        )
        .filter(InboundDocument.created_at >= start_date)
        .group_by("month")
        .order_by("month")
        .all()
    )

    return [{"month": r.month, "amount": r.total_amount} for r in results]


def get_item_price_trends(
    db: Session,
    bean_name: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """
    Get unit price history for a specific bean/item.

    Args:
        db: Database session
        bean_name: Bean name to search for
        start_date: Start date for filtering (inclusive)
        end_date: End date for filtering (inclusive)
    """
    query = db.query(InboundItem.created_at, InboundItem.unit_price, InboundItem.bean_name).filter(
        InboundItem.bean_name.like(f"%{bean_name}%")
    )

    # Apply date filters if provided
    if start_date:
        query = query.filter(InboundItem.created_at >= start_date)
    if end_date:
        query = query.filter(InboundItem.created_at <= end_date)

    results = query.order_by(InboundItem.created_at).all()

    return [
        {"date": r.created_at.strftime("%Y-%m-%d %H:%M"), "price": r.unit_price} for r in results
    ]


def get_inventory_stats(
    db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
):
    """
    Calculate the current inventory value of items purchased within a specific date range,
    using FIFO (First-In-First-Out) logic. Returns aggregated stats by bean, supplier, and top items.
    """
    from app.models.bean import Bean
    from app.models.inbound_document import InboundDocument
    from app.models.inventory_log import InventoryLog

    beans = db.query(Bean).all()

    bean_results = []
    supplier_results = {}
    total_inventory_value = 0.0

    for bean in beans:
        # Fetch Inbound History with supplier info joined
        relevant_inbounds = (
            db.query(InboundItem)
            .join(InboundDocument)
            .filter(InboundItem.bean_id == bean.id)
            .order_by(InboundItem.created_at)
            .all()
        )

        if not relevant_inbounds:
            continue

        usage_logs = (
            db.query(InventoryLog)
            .filter(InventoryLog.bean_id == bean.id, InventoryLog.change_amount < 0)
            .all()
        )

        total_used_amount = sum(abs(log.change_amount) for log in usage_logs)

        bean_total_qty = 0.0
        bean_total_value = 0.0
        accumulated_qty = 0.0

        for item in relevant_inbounds:
            qty = item.quantity or 0
            if accumulated_qty + qty > total_used_amount:
                remaining_qty = (accumulated_qty + qty) - max(accumulated_qty, total_used_amount)

                is_in_range = True
                if start_date and item.created_at < start_date:
                    is_in_range = False
                if end_date and item.created_at > end_date:
                    is_in_range = False

                if is_in_range:
                    item_value = remaining_qty * (item.unit_price or 0)
                    bean_total_qty += remaining_qty
                    bean_total_value += item_value
                    total_inventory_value += item_value

                    # Aggregate by supplier
                    supplier_name = item.inbound_document.supplier_name or "Unknown"
                    supplier_results[supplier_name] = (
                        supplier_results.get(supplier_name, 0.0) + item_value
                    )

            accumulated_qty += qty

        if bean_total_qty > 0:
            bean_results.append(
                {
                    "bean_name": bean.name,
                    "quantity_kg": bean_total_qty,
                    "avg_price": bean_total_value / bean_total_qty,
                    "total_value": bean_total_value,
                }
            )

    # Sort and refine
    bean_results.sort(key=lambda x: x["total_value"], reverse=True)

    # Format suppliers list with percentages
    supplier_list = []
    for name, value in supplier_results.items():
        supplier_list.append(
            {
                "name": name,
                "value": value,
                "percentage": (
                    (value / total_inventory_value * 100) if total_inventory_value > 0 else 0
                ),
            }
        )
    supplier_list.sort(key=lambda x: x["value"], reverse=True)

    return {
        "items": bean_results,
        "suppliers": supplier_list,
        "top_items": bean_results[:3],
        "total_value": total_inventory_value,
    }


def get_inventory_summary(db: Session) -> dict:
    """
    Get current inventory summary statistics.

    Returns:
        - total_weight: Total weight of all beans in stock (kg)
        - low_stock_count: Number of beans with quantity < 5kg
        - active_varieties: Total number of active bean varieties
    """
    # Calculate total weight
    total_weight_result = db.query(func.sum(Bean.quantity_kg)).scalar()
    total_weight = float(total_weight_result) if total_weight_result else 0.0

    # Count low stock beans (< 5kg)
    low_stock_count = db.query(Bean).filter(Bean.quantity_kg < 5).count()

    # Count active varieties (all beans)
    active_varieties = db.query(Bean).count()

    return {
        "total_weight": round(total_weight, 2),
        "low_stock_count": low_stock_count,
        "active_varieties": active_varieties
    }
