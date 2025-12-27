import sys
import os

# Create a valid path to import 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')
sys.path.append(backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.bean import Bean
from app.config import settings

# Adjust the database URL if necessary. Assuming it is available in settings.
# If implicit relative import fails, we might need to adjust python path.
# For simplicity, assuming running from root with backend in path.

def check_beans():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        beans = db.query(Bean).all()
        print(f"Total beans: {len(beans)}")
        for bean in beans:
            print(f"ID: {bean.id}, Name: '{bean.name}', Type: {bean.type}")
            if not bean.name or len(bean.name) < 1:
                print(f"WARNING: Invalid bean found! ID: {bean.id}")
    finally:
        db.close()

if __name__ == "__main__":
    check_beans()
