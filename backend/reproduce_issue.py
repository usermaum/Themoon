import sys
import os

# Add backend dir to path
current_dir = os.path.dirname(os.path.abspath(__file__))
# backend/reproduce_issue.py -> backend is current_dir
# We need to add parent of backend to path if we import app as 'app'
# But 'app' is inside backend. So we need to add 'backend' path?
# Wait, if I am in 'backend', 'app' is a subdir.
# So adding current_dir to sys.path should be enough.

sys.path.append(current_dir)

from app.database import SessionLocal
from app.models.bean import Bean as BeanModel
from app.models.inventory_log import InventoryLog
from app.schemas.bean import Bean as BeanSchema
from pydantic import ValidationError

def reproduce():
    db = SessionLocal()
    try:
        print("Querying beans...")
        beans = db.query(BeanModel).all()
        print(f"Found {len(beans)} beans in DB.")
        
        for i, b in enumerate(beans):
            try:
                # Mimic the endpoint logic
                schema_bean = BeanSchema.model_validate(b)
                # print(f"Bean {b.id} OK: {schema_bean.name}")
            except ValidationError as e:
                print(f"VALIDATION ERROR for Bean ID {b.id}:")
                print(f"Name in DB: '{b.name}' (Type: {type(b.name)})")
                print(e)
                return
            except Exception as e:
                print(f"OTHER ERROR for Bean ID {b.id}: {e}")
                return
        
        print("All beans validated successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    reproduce()
