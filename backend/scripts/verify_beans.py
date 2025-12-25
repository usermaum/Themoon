import sqlite3
import os

DB_PATH = r"d:\Ai\WslProject\Themoon\themoon.db"

def verify_beans():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    print("--- Bean Verification Report ---")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check non-green beans
        cursor.execute("SELECT id, name, type, origin FROM beans WHERE type != 'GREEN_BEAN'")
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}, Origin: {row[3]}")
            
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_beans()
