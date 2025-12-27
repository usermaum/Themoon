
import os
import sys
# Make sure we can find 'app'
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.database import engine, Base
import app.models # This triggers the __init__.py which imports all models

def reset():
    print("🗑️  Nuclear Reset: Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("🔨 Nuclear Reset: Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Nuclear Reset: Done.")

if __name__ == "__main__":
    reset()
