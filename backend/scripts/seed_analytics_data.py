"""
Seed Analytics Data
-------------------
Generates mock Inbound Documents and Items for the past 6 months
to enable testing of the Analytics Dashboard.
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models import Bean, InboundDocument, InboundItem, Supplier, InboundDocumentDetail, InboundReceiver
from sqlalchemy.orm import Session

def seed_analytics(db: Session):
    print("🌱 Seeding Analytics Data...")

    # 1. Fetch Beans and Suppliers
    beans = db.query(Bean).all()
    suppliers = db.query(Supplier).all()

    if not beans:
        print("❌ No beans found. Run recreate_and_seed_v2.py first.")
        return
    if not suppliers:
        print("❌ No suppliers found. Run recreate_and_seed_v2.py first.")
        return

    # 2. Generate Documents
    # We'll create ~20 documents over the last 6 months (approx 180 days)
    
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(20):
        # Random date within last 6 months
        random_days = random.randint(0, 180)
        doc_date = start_date + timedelta(days=random_days)
        
        supplier = random.choice(suppliers)
        
        # Create Document
        doc = InboundDocument(
            supplier_id=supplier.id,
            supplier_name=supplier.name,
            created_at=doc_date,
            total_amount=0.0 # Will calculate later
        )
        db.add(doc)
        db.flush() # To get doc.id

        # Create Items (1-5 items per doc)
        num_items = random.randint(1, 5)
        doc_total = 0.0
        
        for _ in range(num_items):
            bean = random.choice(beans)
            
            quantity = float(random.randint(10, 60)) # 10kg ~ 60kg
            # Randomize price slightly around average
            variation = random.uniform(0.9, 1.1)
            unit_price = int(bean.avg_price * variation)
            supply_price = unit_price * quantity
            vat = supply_price * 0.1
            total_price = supply_price + vat
            
            item = InboundItem(
                inbound_document_id=doc.id,
                bean_id=bean.id,
                bean_name=bean.name_ko, # Use KO name for display consistency
                quantity=quantity,
                unit_price=unit_price,
                supply_amount=supply_price,
                tax_amount=vat,
            )
            db.add(item)
            doc_total += total_price
            
            # Optional: Update Bean stock for "Current Inventory Value"
            # We add some stock but assume some was used. 
            # Let's say 50% remains.
            bean.quantity_kg += (quantity * 0.5)

        # Update Document Total
        doc.total_amount = doc_total
        
        # Create Dummy Detail (required for schema but simplified)
        detail = InboundDocumentDetail(
            inbound_document_id=doc.id,
            subtotal=doc_total/1.1,
            tax_amount=doc_total - (doc_total/1.1),
            grand_total=doc_total
        )
        db.add(detail)

        print(f"   Created Doc #{doc.id} ({doc_date.strftime('%Y-%m-%d')}): {supplier.name} - ₩{int(doc_total):,}")

    db.commit()
    print("✅ Analytics Data Seeded!")

def main():
    db = SessionLocal()
    try:
        seed_analytics(db)
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
