
import sqlite3
import os

db_path = "/mnt/d/Ai/WslProject/Themoon/themoon.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Checking for missing columns in 'inbound_items' table...")
    
    # Check current columns
    cursor.execute("PRAGMA table_info(inbound_items)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if "remaining_quantity" not in columns:
        print("Adding 'remaining_quantity' column to 'inbound_items'...")
        try:
            # We add it as Float, defaulting to 0.0 (or matching the model's quantity if it was already existing, 
            # but for new migrations just default 0 is safe or nullable)
            # Actually, for FIFO, it should probably match 'quantity' if we are migrating existing data.
            cursor.execute("ALTER TABLE inbound_items ADD COLUMN remaining_quantity FLOAT DEFAULT 0.0")
            # If we have existing data, initialized remaining_quantity = quantity
            cursor.execute("UPDATE inbound_items SET remaining_quantity = quantity")
            conn.commit()
            print("Successfully added 'remaining_quantity'.")
        except Exception as e:
            print(f"Error adding 'remaining_quantity': {e}")
    else:
        print("'remaining_quantity' column already exists.")

    conn.close()

if __name__ == "__main__":
    migrate()
