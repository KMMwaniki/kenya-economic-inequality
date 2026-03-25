import sqlite3

print("=" * 50)
print("Kenya County Economic Inequality Analysis")
print("Setting up database...")
print("=" * 50)

# Step 1: Create database connection
conn = sqlite3.connect('kenya_counties.db')
cursor = conn.cursor()

# Step 2: Read and run setup.sql
print("\n📁 Reading setup.sql...")
with open('setup.sql', 'r', encoding='utf-8') as f:
    setup_sql = f.read()

print("🏗️  Creating tables and inserting data...")
try:
    conn.executescript(setup_sql)
    print("✅ Database setup complete!")
except Exception as e:
    print(f"❌ Error: {e}")

# Step 3: Verify tables were created
print("\n📊 Verifying tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(f"   ✅ {table[0]}")

# Step 4: Count records in each table
print("\n📈 Record counts:")
for table in ['counties', 'demographics', 'infrastructure', 'health', 'education']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"   {table}: {count} records")

# Step 5: Show sample data
print("\n📋 Sample data from counties:")
cursor.execute("SELECT county_name, region FROM counties LIMIT 5")
sample = cursor.fetchall()
for county in sample:
    print(f"   {county[0]} - {county[1]}")

# Close connection
conn.close()

print("\n" + "=" * 50)
print("✅ Database is ready!")
print("=" * 50)