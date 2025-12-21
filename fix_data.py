import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('themoon.db')
cursor = conn.cursor()

# Get all unique bean names
cursor.execute("SELECT DISTINCT bean_name FROM inbound_items")
bean_rows = cursor.fetchall()
bean_names = [r[0] for r in bean_rows if r[0]]

print(f"Found beans: {bean_names}")

now = datetime.now()

for bean_name in bean_names:
    print(f"Processing {bean_name}...")
    # Get IDs for this bean
    cursor.execute("SELECT id FROM inbound_items WHERE bean_name = ? ORDER BY id DESC", (bean_name,))
    item_rows = cursor.fetchall()
    
    if not item_rows:
        continue
        
    ids = [r[0] for r in item_rows]
    
    # Spread them out: newest is today, next is -1 month, etc.
    for i, item_id in enumerate(ids):
        # 0: today
        # 1: -15 days
        # 2: -45 days
        # 3: -75 days...
        days_offset = i * 30
        new_date = now - timedelta(days=days_offset)
        
        new_ts = new_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # print(f"  Updating ID {item_id} to {new_ts}")
        cursor.execute("UPDATE inbound_items SET created_at = ? WHERE id = ?", (new_ts, item_id))

conn.commit()
print("All beans updated.")

conn.close()
