import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from sqlalchemy import text, inspect

def fix_schema():
    print("Fixing Schema...")
    inspector = inspect(engine)
    
    # ... (Inbound Documents checks omitted for brevity if confirmed, but good to keep idempotency)
    # Keeping only relevant updates for speed and focus on inventory_logs
    
    print("Checking Inventory Logs...")
    cols = [c['name'] for c in inspector.get_columns('inventory_logs')]
    
    with engine.connect() as conn:
        # Rename transaction_type -> change_type
        if 'transaction_type' in cols and 'change_type' not in cols:
            print("Renaming transaction_type to change_type...")
            conn.execute(text("ALTER TABLE inventory_logs RENAME COLUMN transaction_type TO change_type"))
            
        # Rename quantity_change -> change_amount
        if 'quantity_change' in cols and 'change_amount' not in cols:
            print("Renaming quantity_change to change_amount...")
            conn.execute(text("ALTER TABLE inventory_logs RENAME COLUMN quantity_change TO change_amount"))
            
        # Rename reason -> notes
        if 'reason' in cols and 'notes' not in cols:
            print("Renaming reason to notes...")
            conn.execute(text("ALTER TABLE inventory_logs RENAME COLUMN reason TO notes"))
            
        # Add related_id
        if 'related_id' not in cols:
            print("Adding related_id...")
            conn.execute(text("ALTER TABLE inventory_logs ADD COLUMN related_id INTEGER"))
            
        conn.commit()
        
    print("Inventory Logs Schema Fixed.")

if __name__ == "__main__":
    fix_schema()
