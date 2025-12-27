import sqlite3

def check_raw_db():
    conn = sqlite3.connect('themoon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, origin FROM beans WHERE name LIKE '%Blend%' OR name LIKE '%Moon%' OR name LIKE '%Yirgacheffe%'")
    rows = cursor.fetchall()
    print(f"{'ID':<5} {'Name':<35} {'Type':<20} {'Origin':<15}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<35} {row[2]:<20} {row[3]:<15}")
    conn.close()

if __name__ == "__main__":
    check_raw_db()
