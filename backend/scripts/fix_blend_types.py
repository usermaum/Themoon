import sqlite3
import os

DB_PATH = r"d:\Ai\WslProject\Themoon\themoon.db"

def migrate_blend_types_raw():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    print(f"Connecting to database at {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check existing types
        cursor.execute("SELECT id, name, type FROM beans WHERE type='ROASTED_BEAN' AND (origin='Blend' OR name LIKE '%Blend%' OR name LIKE '%블렌드%' OR sku LIKE '%BLEND%')")
        rows = cursor.fetchall()
        
        print(f"Found {len(rows)} potential roasted blends to fix:")
        for row in rows:
            print(f" - ID: {row[0]}, Name: {row[1]}, Current Type: {row[2]}")

        # Update
        cursor.execute("UPDATE beans SET type='BLEND_BEAN' WHERE type='ROASTED_BEAN' AND (origin='Blend' OR name LIKE '%Blend%' OR name LIKE '%블렌드%' OR sku LIKE '%BLEND%')")
        updated_count = cursor.rowcount
        
        conn.commit()
        print(f"Successfully updated {updated_count} beans to BLEND_BEAN.")
        conn.close()

    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_blend_types_raw()
