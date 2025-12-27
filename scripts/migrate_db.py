import sqlite3
import os
import sys
from sqlalchemy.orm import Session
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.database import SessionLocal, engine
from app.models import Bean, Inventory, Transaction, RoastingLog, Blend, BlendRecipe, CostSetting, User

# SQLite DB Path
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), '../data/roasting_data.db')

def migrate_beans(sqlite_conn, pg_session: Session):
    print("Migrating Beans...")
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM beans")
    rows = cursor.fetchall()
    # Assuming columns: no, name, country, roast_level, description, ...
    # Need to map columns dynamically or assume order. 
    # Let's assume we need to inspect columns first or use dict factory
    
    # Using row factory for easier access
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM beans")
    rows = cursor.fetchall()

    for row in rows:
        # Check if bean exists
        existing = pg_session.query(Bean).filter(Bean.name == row['name']).first()
        if existing:
            print(f"Bean {row['name']} already exists. Skipping.")
            continue

        bean = Bean(
            no=row['no'],
            name=row['name'],
            country_name=row['country'], # Mapped from country
            roast_level=row['roast_level'],
            description=row['description'],
            # Add other fields if available in SQLite
        )
        pg_session.add(bean)
    pg_session.commit()
    print("Beans migrated.")

def migrate_inventory(sqlite_conn, pg_session: Session):
    print("Migrating Inventory...")
    # Logic to migrate inventory
    # This depends on the exact schema of the SQLite DB which we saw earlier had 'inventory' table
    pass

def main():
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"SQLite database not found at {SQLITE_DB_PATH}")
        return

    print(f"Connecting to SQLite: {SQLITE_DB_PATH}")
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    
    print("Connecting to PostgreSQL...")
    pg_session = SessionLocal()

    try:
        migrate_beans(sqlite_conn, pg_session)
        # migrate_inventory(sqlite_conn, pg_session)
        # Add other migration functions here
        
        print("Migration completed successfully.")
    except Exception as e:
        print(f"Migration failed: {e}")
        pg_session.rollback()
    finally:
        sqlite_conn.close()
        pg_session.close()

if __name__ == "__main__":
    main()
