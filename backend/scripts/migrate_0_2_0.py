import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import *  # Make sure models are imported
from sqlalchemy import text, inspect

def migrate():
    print("Starting migration to v0.2.0...")
    
    # 1. Create new tables (Suppliers)
    # This will strictly create tables that don't exist.
    print("1. Creating new tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Add columns to inbound_documents
    print("2. Checking inbound_documents schema...")
    inspector = inspect(engine)
    existing_columns = [c['name'] for c in inspector.get_columns('inbound_documents')]
    
    with engine.connect() as conn:
        # Add contract_number
        if 'contract_number' not in existing_columns:
            print("   -> Adding contract_number column...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN contract_number VARCHAR(100)"))
            # Note: SQLite supports CREATE INDEX
            print("   -> Creating index for contract_number...")
            conn.execute(text("CREATE UNIQUE INDEX ix_inbound_documents_contract_number ON inbound_documents (contract_number)"))
        else:
            print("   -> contract_number already exists.")

        # Add supplier_id
        if 'supplier_id' not in existing_columns:
            print("   -> Adding supplier_id column...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN supplier_id INTEGER REFERENCES suppliers(id)"))
        else:
            print("   -> supplier_id already exists.")

        # Add receiver_name
        if 'receiver_name' not in existing_columns:
            print("   -> Adding receiver_name column...")
            conn.execute(text("ALTER TABLE inbound_documents ADD COLUMN receiver_name VARCHAR(100)"))
        else:
            print("   -> receiver_name already exists.")
            
        conn.commit()
    
    print("Migration v0.2.0 completed successfully.")

if __name__ == "__main__":
    migrate()
