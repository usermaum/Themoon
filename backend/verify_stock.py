import sys
import os

# Add backend directory to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.bean import Bean

def verify_stock():
    db = SessionLocal()
    try:
        beans = db.query(Bean).all()
        total_kg = sum(b.quantity_kg for b in beans)
        count = len(beans)
        
        print(f"Total Beans Count: {count}")
        print(f"Total Stock (kg): {total_kg}")
        
        # Check if any single bean has a huge amount that might look weird
        print("\nTop 5 Stock Holdings:")
        sorted_beans = sorted(beans, key=lambda b: b.quantity_kg, reverse=True)[:5]
        for b in sorted_beans:
            print(f"- {b.name}: {b.quantity_kg} kg")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_stock()
