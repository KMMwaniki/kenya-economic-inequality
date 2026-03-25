import sqlite3
import pandas as pd

print("=" * 50)
print("Running SQL Analysis on Kenya Counties Data")
print("=" * 50)

conn = sqlite3.connect('kenya_counties.db')

# Read the analysis.sql file
with open('analysis.sql', 'r', encoding='utf-8') as f:
    sql_queries = f.read()

# Split into individual queries (split by semicolon)
queries = [q.strip() for q in sql_queries.split(';') if q.strip()]

# Results storage
results = {}

print("\n📊 Executing 10 analytical queries...\n")

for i, query in enumerate(queries, 1):
    try:
        # Get first few words of query for description
        query_start = query.split()[0:4]
        query_desc = ' '.join(query_start)
        
        print(f"Query {i}: {query_desc}...")
        
        # Execute and get results
        df = pd.read_sql_query(query, conn)
        
        # Store results
        results[f"query_{i}"] = df
        
        # Display results
        print(f"   ✅ {len(df)} rows returned")
        print(df.head(10))
        print("-" * 50)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Save all results to Excel file
print("\n💾 Saving all results to analysis_results.xlsx...")
with pd.ExcelWriter('analysis_results.xlsx') as writer:
    for name, df in results.items():
        df.to_excel(writer, sheet_name=name, index=False)

print("✅ Results saved to analysis_results.xlsx")

conn.close()

print("\n" + "=" * 50)
print("✅ SQL Analysis Complete!")
print("=" * 50)