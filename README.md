# Kenya County Economic Inequality Analysis

## Author: Kimberly Muthoni Mwaniki
## Institution: Strathmore University

## Problem Statement
Economic inequality in Kenya varies significantly across the 47 counties, with some regions experiencing poverty rates above 70% while others maintain rates below 20%. This project analyzes the drivers of county-level economic inequality to provide evidence-based recommendations for policymakers, NGOs, and development organizations.

## Methodology
This project combines SQL, R, and Python to create a comprehensive analysis pipeline:

1. **SQL Database Setup**: Created a SQLite database with 5 tables containing realistic data for all 47 counties based on KNBS patterns
2. **SQL Analysis**: 10 analytical queries answering key policy questions about poverty, infrastructure, and development
3. **R Statistical Analysis**: Multiple regression modeling to identify predictors of poverty, with visualizations and interpretation
4. **Streamlit Dashboard**: Interactive web application for exploring county-level data and comparing regions

## Key SQL Queries Explained

### 1. Top 10 Counties by Poverty Rate
```sql
SELECT c.county_name, d.poverty_rate, d.unemployment_rate, c.region
FROM counties c
JOIN demographics d ON c.county_id = d.county_id
WHERE d.year = 2023
ORDER BY d.poverty_rate DESC
LIMIT 10;