-- =====================================================
-- Kenya County Economic Inequality Analysis
-- Analytical SQL Queries
-- =====================================================

-- 1. Top 10 counties with highest poverty rates
-- Why it matters: Identifies counties requiring urgent intervention
SELECT 
    c.county_name,
    d.poverty_rate,
    d.unemployment_rate,
    c.region
FROM counties c
JOIN demographics d ON c.county_id = d.county_id
WHERE d.year = 2023
ORDER BY d.poverty_rate DESC
LIMIT 10;

-- 2. Correlation between electricity access and poverty rate
-- Why it matters: Quantifies the relationship between infrastructure and poverty
SELECT 
    c.county_name,
    i.electricity_access,
    d.poverty_rate,
    c.region,
    CASE 
        WHEN i.electricity_access >= 70 THEN 'High Access'
        WHEN i.electricity_access BETWEEN 40 AND 69 THEN 'Medium Access'
        ELSE 'Low Access'
    END as access_category
FROM counties c
JOIN infrastructure i ON c.county_id = i.county_id
JOIN demographics d ON c.county_id = d.county_id
WHERE i.year = 2023 AND d.year = 2023
ORDER BY i.electricity_access DESC;

-- 3. Counties with best and worst doctor-to-population ratios
-- Why it matters: Healthcare access is critical for human development
SELECT 
    c.county_name,
    h.doctors_per_1000,
    h.hospital_count,
    c.region,
    CASE 
        WHEN h.doctors_per_1000 >= 0.30 THEN 'Excellent'
        WHEN h.doctors_per_1000 BETWEEN 0.20 AND 0.29 THEN 'Adequate'
        WHEN h.doctors_per_1000 BETWEEN 0.10 AND 0.19 THEN 'Inadequate'
        ELSE 'Critical Shortage'
    END as healthcare_status
FROM counties c
JOIN health h ON c.county_id = h.county_id
WHERE h.year = 2023
ORDER BY h.doctors_per_1000 DESC;

-- 4. Which region has the biggest inequality gap between counties?
-- Why it matters: Identifies regions with internal disparities needing targeted policies
WITH region_stats AS (
    SELECT 
        c.region,
        MIN(d.poverty_rate) as min_poverty,
        MAX(d.poverty_rate) as max_poverty,
        AVG(d.poverty_rate) as avg_poverty,
        STDDEV(d.poverty_rate) as poverty_stddev
    FROM counties c
    JOIN demographics d ON c.county_id = d.county_id
    WHERE d.year = 2023
    GROUP BY c.region
)
SELECT 
    region,
    ROUND(min_poverty, 1) as lowest_poverty,
    ROUND(max_poverty, 1) as highest_poverty,
    ROUND(max_poverty - min_poverty, 1) as inequality_gap,
    ROUND(avg_poverty, 1) as regional_average,
    ROUND(poverty_stddev, 1) as standard_deviation
FROM region_stats
ORDER BY inequality_gap DESC;

-- 5. Counties where high education does NOT translate to low poverty (anomalies)
-- Why it matters: Identifies structural barriers where education alone isn't enough
WITH education_poverty_ranking AS (
    SELECT 
        c.county_name,
        e.literacy_rate,
        d.poverty_rate,
        PERCENT_RANK() OVER (ORDER BY e.literacy_rate DESC) as education_rank,
        PERCENT_RANK() OVER (ORDER BY d.poverty_rate ASC) as poverty_rank
    FROM counties c
    JOIN education e ON c.county_id = e.county_id
    JOIN demographics d ON c.county_id = d.county_id
    WHERE e.year = 2023 AND d.year = 2023
)
SELECT 
    county_name,
    literacy_rate,
    poverty_rate,
    CASE 
        WHEN education_rank > 0.7 AND poverty_rank < 0.3 THEN 'Anomaly: High Education but High Poverty'
        ELSE 'Expected Pattern'
    END as anomaly_type
FROM education_poverty_ranking
WHERE education_rank > 0.7 AND poverty_rank < 0.3
ORDER BY poverty_rate DESC;

-- 6. Infrastructure index score per county (composite of road, electricity, internet)
-- Why it matters: Creates a holistic measure of infrastructure development
SELECT 
    c.county_name,
    c.region,
    i.road_density,
    i.electricity_access,
    i.internet_access,
    ROUND(
        (i.road_density / MAX(i.road_density) OVER() * 0.3 +
         i.electricity_access / MAX(i.electricity_access) OVER() * 0.4 +
         i.internet_access / MAX(i.internet_access) OVER() * 0.3) * 100, 1
    ) as infrastructure_index_score
FROM counties c
JOIN infrastructure i ON c.county_id = i.county_id
WHERE i.year = 2023
ORDER BY infrastructure_index_score DESC;

-- 7. Top 10 most underserved counties combining health + education + infrastructure
-- Why it matters: Identifies counties needing multi-sectoral intervention
WITH health_score AS (
    SELECT 
        county_id,
        RANK() OVER (ORDER BY doctors_per_1000 ASC, child_mortality DESC) as health_deficit_rank
    FROM health
    WHERE year = 2023
),
education_score AS (
    SELECT 
        county_id,
        RANK() OVER (ORDER BY literacy_rate ASC, dropout_rate DESC) as education_deficit_rank
    FROM education
    WHERE year = 2023
),
infrastructure_score AS (
    SELECT 
        county_id,
        RANK() OVER (ORDER BY electricity_access ASC, internet_access ASC) as infrastructure_deficit_rank
    FROM infrastructure
    WHERE year = 2023
)
SELECT 
    c.county_name,
    c.region,
    ROUND((hs.health_deficit_rank + es.education_deficit_rank + inf.infrastructure_deficit_rank) / 3.0, 1) as avg_deficit_rank,
    d.poverty_rate
FROM counties c
JOIN health_score hs ON c.county_id = hs.county_id
JOIN education_score es ON c.county_id = es.county_id
JOIN infrastructure_score inf ON c.county_id = inf.county_id
JOIN demographics d ON c.county_id = d.county_id
WHERE d.year = 2023
ORDER BY avg_deficit_rank DESC
LIMIT 10;

-- 8. Poverty rate vs school enrollment relationship
-- Why it matters: Shows how economic status affects educational participation
SELECT 
    c.county_name,
    d.poverty_rate,
    e.school_enrollment,
    e.dropout_rate,
    CASE 
        WHEN d.poverty_rate > 50 THEN 'Extreme Poverty'
        WHEN d.poverty_rate BETWEEN 30 AND 50 THEN 'High Poverty'
        ELSE 'Moderate-Low Poverty'
    END as poverty_category
FROM counties c
JOIN demographics d ON c.county_id = d.county_id
JOIN education e ON c.county_id = e.county_id
WHERE d.year = 2023 AND e.year = 2023
ORDER BY d.poverty_rate DESC;

-- 9. Counties that improved most between years (2018 vs 2023)
-- Why it matters: Identifies successful development patterns to replicate
WITH poverty_2018 AS (
    SELECT county_id, poverty_rate 
    FROM demographics 
    WHERE year = 2018
),
poverty_2023 AS (
    SELECT county_id, poverty_rate 
    FROM demographics 
    WHERE year = 2023
)
SELECT 
    c.county_name,
    p2018.poverty_rate as poverty_2018,
    p2023.poverty_rate as poverty_2023,
    ROUND(p2018.poverty_rate - p2023.poverty_rate, 1) as improvement_points,
    ROUND(((p2018.poverty_rate - p2023.poverty_rate) / p2018.poverty_rate) * 100, 1) as percent_improvement
FROM counties c
JOIN poverty_2018 p2018 ON c.county_id = p2018.county_id
JOIN poverty_2023 p2023 ON c.county_id = p2023.county_id
ORDER BY improvement_points DESC
LIMIT 10;

-- 10. Nairobi vs rest of Kenya comparison across all indicators
-- Why it matters: Quantifies urban-rural divide and sets benchmarks
WITH nairobi_metrics AS (
    SELECT 
        'Nairobi' as area,
        AVG(d.poverty_rate) as avg_poverty,
        AVG(i.electricity_access) as avg_electricity,
        AVG(e.literacy_rate) as avg_literacy,
        AVG(h.doctors_per_1000) as avg_doctors
    FROM counties c
    JOIN demographics d ON c.county_id = d.county_id
    JOIN infrastructure i ON c.county_id = i.county_id
    JOIN education e ON c.county_id = e.county_id
    JOIN health h ON c.county_id = h.county_id
    WHERE c.county_name = 'Nairobi' AND d.year = 2023
),
other_counties AS (
    SELECT 
        'Other Counties' as area,
        AVG(d.poverty_rate) as avg_poverty,
        AVG(i.electricity_access) as avg_electricity,
        AVG(e.literacy_rate) as avg_literacy,
        AVG(h.doctors_per_1000) as avg_doctors
    FROM counties c
    JOIN demographics d ON c.county_id = d.county_id
    JOIN infrastructure i ON c.county_id = i.county_id
    JOIN education e ON c.county_id = e.county_id
    JOIN health h ON c.county_id = h.county_id
    WHERE c.county_name != 'Nairobi' AND d.year = 2023
)
SELECT * FROM nairobi_metrics
UNION ALL
SELECT * FROM other_counties;