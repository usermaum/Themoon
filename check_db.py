import sqlite3
import datetime

conn = sqlite3.connect('themoon.db')
cursor = conn.cursor()

# Check data for '모모라'
print("Checking data for '모모라'...")
cursor.execute("SELECT id, bean_name, unit_price, created_at FROM inbound_items WHERE bean_name LIKE '%모모라%' ORDER BY created_at DESC")
rows = cursor.fetchall()

if not rows:
    print("No data found for '모모라'")
else:
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}, Created: {row[3]}")

conn.close()
