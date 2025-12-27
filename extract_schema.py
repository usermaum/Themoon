import sqlite3
import json

def get_schema_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = {}
    
    for table_name in tables:
        table_name = table_name[0]
        if table_name == 'sqlite_sequence':
            continue
            
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = cursor.fetchall()
        
        schema[table_name] = {
            'columns': [],
            'foreign_keys': []
        }
        
        for col in columns:
            # cid, name, type, notnull, dflt_value, pk
            schema[table_name]['columns'].append({
                'name': col[1],
                'type': col[2],
                'notnull': col[3],
                'default': col[4],
                'pk': col[5]
            })
            
        for fk in fks:
            # id, seq, table, from, to, on_update, on_delete, match
            schema[table_name]['foreign_keys'].append({
                'table': fk[2],
                'from': fk[3],
                'to': fk[4]
            })
            
    conn.close()
    return schema

if __name__ == "__main__":
    db_path = "themoon.db"
    try:
        schema = get_schema_info(db_path)
        print(json.dumps(schema, indent=2))
    except Exception as e:
        print(f"Error: {e}")
