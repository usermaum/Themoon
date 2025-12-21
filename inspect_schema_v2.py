import sqlite3
import os

DB_PATH = 'themoon.db'

def get_schema_markdown(db_path):
    if not os.path.exists(db_path):
        return f"Database not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']

    markdown_output = ""

    for table in tables:
        markdown_output += f"\n### {table}\n\n"
        markdown_output += "| Column | Type | Nullable | Default | PK |\n"
        markdown_output += "| --- | --- | --- | --- | --- |\n"
        
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        
        for col in columns:
            # cid, name, type, notnull, dflt_value, pk
            cid, name, dtype, notnull, dflt_value, pk = col
            nullable = "YES" if not notnull else "NO"
            pk_str = "YES" if pk else ""
            default_str = str(dflt_value) if dflt_value is not None else "NULL"
            
            markdown_output += f"| `{name}` | {dtype} | {nullable} | {default_str} | {pk_str} |\n"
        
        # Get Foreign Keys
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()
        if fks:
            markdown_output += "\n**Foreign Keys**:\n"
            for fk in fks:
                # id, seq, table, from, to, on_update, on_delete, match
                _, _, to_table, from_col, to_col, _, _, _ = fk
                markdown_output += f"- `{from_col}` -> `{to_table}.{to_col}`\n"

    conn.close()
    return markdown_output

if __name__ == "__main__":
    print(get_schema_markdown(DB_PATH))
