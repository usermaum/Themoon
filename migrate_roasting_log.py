import os
import sys
from sqlalchemy import text

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Force the database URL
os.environ['DATABASE_URL'] = 'sqlite:///D:/Ai/WslProject/Themoon/themoon.db'

from app.database import engine

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text('ALTER TABLE inventory_logs ADD COLUMN roasting_log_id INTEGER REFERENCES roasting_logs(id)'))
            conn.commit()
            print("Successfully added roasting_log_id to inventory_logs")
        except Exception as e:
            print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()
