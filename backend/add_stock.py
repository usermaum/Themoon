import sys
import os
from sqlalchemy import text

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal

db = SessionLocal()

print("Checking Bean Names...")
result = db.execute(text("SELECT name FROM beans"))
all_names = [row[0] for row in result]
print("Available Beans:", all_names)

print("Updating stock using Raw SQL...")
target_names = ["마사이", "안티구아", "모모라", "시다모"]

for name in target_names:
    query = text("UPDATE beans SET quantity_kg = quantity_kg + 1000.0 WHERE name LIKE :name")
    result = db.execute(query, {"name": f"%{name}%"})
    print(f"Updated {name}: {result.rowcount} rows affected.")

db.commit()
db.close()
print("Stock refill complete.")
