
import sqlite3
import os

db_path = "themoon.db"

if not os.path.exists(db_path):
    print(f"❌ DB file not found: {db_path}")
else:
    print(f"✅ DB file found: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check Tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Items in DB: {tables}")

        # Check Beans
        try:
            cursor.execute("SELECT count(*) FROM beans")
            count = cursor.fetchone()[0]
            print(f"✅ Beans count: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, name, type FROM beans LIMIT 5")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"   - {row}")
        except Exception as e:
            print(f"❌ Error querying beans: {e}")

        conn.close()
    except Exception as e:
        print(f"❌ Error connecting to DB: {e}")
