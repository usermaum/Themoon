import sys
import os

# Ensure app is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.config import settings
# Force DATABASE_URL to use explicit path for verification
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "themoon.db")
# Ensure we use standard Windows path separators
settings.DATABASE_URL = f"sqlite:///{DB_PATH}"
print(f"Force set DATABASE_URL: {settings.DATABASE_URL}")

from app.database import SessionLocal
from app.repositories.bean_repository import BeanRepository
from app.services.bean_service import BeanService

def test_bean_service():
    db = SessionLocal()
    try:
        repo = BeanRepository(db)
        service = BeanService(repo)
        
        print("Testing get_beans...")
        beans = service.get_beans(limit=5)
        print(f"Found {len(beans)} beans.")
        
        print("Testing get_beans_count...")
        count = service.get_beans_count()
        print(f"Total beans: {count}")
        
        print("Testing get_total_stock...")
        stock = service.get_total_stock()
        print(f"Total stock: {stock}")

        print("Testing get_low_stock_beans...")
        low_stock = service.get_low_stock_beans()
        print(f"Low stock items: {len(low_stock)}")

        print("Testing check_existing_beans...")
        check = service.check_existing_beans(["Test Bean"])
        print(f"Check result: {check}")
        
        print("SUCCESS: All methods executed without error.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    test_bean_service()
