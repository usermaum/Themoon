
import sqlite3
import os

db_path = "themoon.db"

if not os.path.exists(db_path):
    print(f"Error: Database file not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table list
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"--- Database Schema for {db_path} ---")
    for table_name in tables:
        table = table_name[0]
        print(f"\n[Table: {table}]")
        
        # Get schema
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
        schema = cursor.fetchone()
        if schema:
            print(schema[0])
            
        # Get row count
        cursor.execute(f"SELECT count(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"-- Row count: {count}")

    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")
