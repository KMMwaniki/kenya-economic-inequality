import sqlite3
import os

print("=" * 50)
print("Creating Kenya Counties Database")
print("=" * 50)

if not os.path.exists('setup.sql'):
    print("ERROR: setup.sql not found!")
    exit(1)

with open('setup.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

conn = sqlite3.connect('kenya_counties.db')
cursor = conn.cursor()

try:
    conn.executescript(sql_script)
    conn.commit()
    print("✅ Database created successfully!")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"📊 Tables: {[t[0] for t in tables]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
finally:
    conn.close()

print("=" * 50)