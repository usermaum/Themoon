import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "themoon.db")

def add_column():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(inventory_logs)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "inbound_document_id" in columns:
            print("Column 'inbound_document_id' already exists.")
        else:
            print("Adding 'inbound_document_id' column...")
            cursor.execute("ALTER TABLE inventory_logs ADD COLUMN inbound_document_id INTEGER REFERENCES inbound_documents(id)")
            conn.commit()
            print("Column added successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
