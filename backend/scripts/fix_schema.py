import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from sqlalchemy import text, inspect

def fix_schema():
    print("Fixing Schema...")
    inspector = inspect(engine)
    existing_columns = [c['name'] for c in inspector.get_columns('inbound_documents')]
    
    with engine.connect() as conn:
        if 'invoice_date' not in existing_columns:
            print("Adding invoice_date...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN invoice_date VARCHAR(50)"))
            
        if 'total_amount' not in existing_columns:
            print("Adding total_amount...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN total_amount FLOAT"))
            
        if 'image_url' not in existing_columns:
            print("Adding image_url...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN image_url VARCHAR(500)"))

        if 'drive_file_id' not in existing_columns:
            print("Adding drive_file_id...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN drive_file_id VARCHAR(200)"))
            
        if 'notes' not in existing_columns:
            print("Adding notes...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN notes TEXT"))
            
        conn.commit()
    print("Schema Fix Completed.")

if __name__ == "__main__":
    fix_schema()
