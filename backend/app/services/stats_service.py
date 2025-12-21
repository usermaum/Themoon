from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.inbound_item import InboundItem
from app.models.inbound_document import InboundDocument
from app.models.supplier import Supplier
from datetime import datetime, timedelta

import re

def get_supplier_stats(db: Session):
    """
    Get aggregated statistics by supplier.
    Returns total purchase amount and count for each supplier.
    """
    # Join InboundItem -> InboundDocument -> Supplier (via name or relationship)
    # Since relationships might be loose, we'll group by InboundDocument.supplier_name
    
    results = db.query(
        InboundDocument.supplier_name,
        func.sum(InboundDocument.total_amount).label("total_amount"),
        func.count(InboundDocument.id).label("doc_count")
    ).group_by(InboundDocument.supplier_name).order_by(desc("total_amount")).all()
    
    # Python-side aggregation for normalization
    aggregated = {}
    
    for r in results:
        raw_name = r.supplier_name or "Unknown"
        
        # 1. Remove text in parenthesis (e.g. (주), (Inc))
        norm_name = re.sub(r'\([^)]*\)', '', raw_name)
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
        
        aggregated[norm_name]["total_amount"] += (r.total_amount or 0)
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
    
    results = db.query(
        func.strftime("%Y-%m", InboundDocument.created_at).label("month"),
        func.sum(InboundDocument.total_amount).label("total_amount")
    ).filter(
        InboundDocument.created_at >= start_date
    ).group_by("month").order_by("month").all()
    
    return [
        {"month": r.month, "amount": r.total_amount}
        for r in results
    ]

def get_item_price_trends(db: Session, bean_name: str):
    """
    Get unit price history for a specific bean/item.
    """
    results = db.query(
        InboundItem.created_at,
        InboundItem.unit_price,
        InboundItem.bean_name
    ).filter(
        InboundItem.bean_name.like(f"%{bean_name}%")
    ).order_by(InboundItem.created_at).all()
    
    return [
        {"date": r.created_at.strftime("%Y-%m-%d"), "price": r.unit_price}
        for r in results
    ]
