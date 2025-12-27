import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)

print("Tables:", inspector.get_table_names())

print("\n--- Inbound Documents Columns ---")
for col in inspector.get_columns('inbound_documents'):
    print(f"{col['name']}: {col['type']}")

print("\n--- Suppliers Columns ---")
if 'suppliers' in inspector.get_table_names():
    for col in inspector.get_columns('suppliers'):
        print(f"{col['name']}: {col['type']}")
else:
    print("Suppliers table NOT FOUND")

print("\n--- Beans Columns ---")
if 'beans' in inspector.get_table_names():
    for col in inspector.get_columns('beans'):
        print(f"{col['name']}: {col['type']}")
else:
    print("Beans table NOT FOUND")

print("\n--- Inventory Logs Columns ---")
if 'inventory_logs' in inspector.get_table_names():
    for col in inspector.get_columns('inventory_logs'):
        print(f"{col['name']}: {col['type']}")
else:
    print("Inventory Logs table NOT FOUND")
