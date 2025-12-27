
from sqlalchemy import create_engine, text

# Hardcoded DB URL for standalone execution
DB_URL = "sqlite:///../themoon.db"

def fix_beans():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            print("Checking all beans...")
            result = conn.execute(text("SELECT id, name, type FROM beans"))
            rows = result.fetchall()
            print(f"Total beans found: {len(rows)}")
            for row in rows:
                print(f"ID: {row[0]}, Name: '{row[1]}', Type: {row[2]}")
                if not row[1] or len(row[1]) < 1:
                     print(f"WARNING: Invalid bean found! ID: {row[0]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_beans()
