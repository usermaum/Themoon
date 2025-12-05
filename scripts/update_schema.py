import sys
import os
import logging
from sqlalchemy import text

# Add backend to sys.path
backend_path = os.path.join(os.getcwd(), "backend")
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.database import engine, Base
# Import models to ensure they are registered with Base
from app.models.bean import Bean
# from app.models.inventory_log import InventoryLog # Import if exists

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_schema():
    logger.info("Checking database connection...")
    
    # Check if we need to drop tables first (Nuclear option for Dev)
    # Uncomment the following lines if you want to RESET the database completely
    # with engine.connect() as conn:
    #     logger.info("Dropping all tables...")
    #     Base.metadata.drop_all(bind=engine)
    #     conn.commit()
    
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Schema update complete.")
    logger.warning("IMPORTANT: If tables already existed, new columns may NOT have been added automatically (SQLite limitation).")
    logger.warning("If you see 'no such column' errors, please delete the database file or uncomment the drop_all lines in this script.")

if __name__ == "__main__":
    update_schema()
