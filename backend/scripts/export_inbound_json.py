import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "themoon.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def export_inbound_data():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inbound_documents")
        rows = cursor.fetchall()

        # Process data for JSON serialization
        for row in rows:
            # Parse raw_ocr_data if it's a string
            if isinstance(row.get('raw_ocr_data'), str):
                try:
                    row['raw_ocr_data'] = json.loads(row['raw_ocr_data'])
                except:
                    pass
            
            # Convert datetime objects to string
            if isinstance(row.get('upload_date'), datetime):
                row['upload_date'] = row['upload_date'].isoformat()
            if isinstance(row.get('created_at'), datetime):
                row['created_at'] = row['created_at'].isoformat()
            if isinstance(row.get('updated_at'), datetime):
                row['updated_at'] = row['updated_at'].isoformat()

        print(json.dumps(rows, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error exporting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_inbound_data()
